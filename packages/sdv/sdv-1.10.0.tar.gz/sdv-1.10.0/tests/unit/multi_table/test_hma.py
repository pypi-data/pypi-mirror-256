import re
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pandas as pd
import pytest

from sdv.errors import SynthesizerInputError
from sdv.metadata.multi_table import MultiTableMetadata
from sdv.multi_table.hma import HMASynthesizer
from sdv.single_table.copulas import GaussianCopulaSynthesizer
from tests.utils import get_multi_table_data, get_multi_table_metadata


class TestHMASynthesizer:

    def test___init__(self):
        """Test the default initialization of the ``HMASynthesizer``."""
        # Run
        metadata = get_multi_table_metadata()
        metadata.validate = Mock()
        instance = HMASynthesizer(metadata)

        # Assert
        assert instance.metadata == metadata
        assert isinstance(instance._table_synthesizers['nesreca'], GaussianCopulaSynthesizer)
        assert isinstance(instance._table_synthesizers['oseba'], GaussianCopulaSynthesizer)
        assert isinstance(instance._table_synthesizers['upravna_enota'], GaussianCopulaSynthesizer)
        assert instance._table_parameters == {
            'nesreca': {'default_distribution': 'beta'},
            'oseba': {'default_distribution': 'beta'},
            'upravna_enota': {'default_distribution': 'beta'},
        }
        instance.metadata.validate.assert_called_once_with()

    def test_set_table_parameters_errors_gaussian_kde(self):
        """Test that ``set_table_parameters`` errors with 'gaussian_kde'."""
        # Setup
        default_table_parameters = {'default_distribution': 'gaussian_kde'}
        numerical_distribution_parameters = {
            'numerical_distributions': {
                'id_nesreca': 'gaussian_kde'
            }
        }
        metadata = get_multi_table_metadata()
        instance = HMASynthesizer(metadata)

        # Run and Assert
        err_msg = re.escape(
            "The 'gaussian_kde' is not compatible with the HMA algorithm. Please choose a "
            "different distribution such as 'beta' or 'truncnorm'. Or try a different "
            'algorithm such as HSA.'
        )
        with pytest.raises(SynthesizerInputError, match=err_msg):
            instance.set_table_parameters('nesreca', default_table_parameters)

        with pytest.raises(SynthesizerInputError, match=err_msg):
            instance.set_table_parameters('nesreca', numerical_distribution_parameters)

    def test__get_extension(self):
        """Test the ``_get_extension`` method.

        Test that the resulting dataframe contains extended columns using the names
        and parameters from a trained ``copulas.univariate`` model.
        """
        # Setup
        metadata = get_multi_table_metadata()
        child_table = pd.DataFrame({
            'id_nesreca': [0, 1, 2, 3],
            'upravna_enota': [0, 1, 2, 3]
        })
        instance = HMASynthesizer(metadata)

        # Run
        result = instance._get_extension('nesreca', child_table, 'upravna_enota', '')

        # Assert
        expected = pd.DataFrame({
            '__nesreca__upravna_enota__univariates__id_nesreca__a': [1., 1., 1., 1.],
            '__nesreca__upravna_enota__univariates__id_nesreca__b': [1., 1., 1., 1.],
            '__nesreca__upravna_enota__univariates__id_nesreca__loc': [0., 1., 2., 3.],
            '__nesreca__upravna_enota__univariates__id_nesreca__scale': [np.nan] * 4,
            '__nesreca__upravna_enota__num_rows': [1., 1., 1., 1.]
        })

        pd.testing.assert_frame_equal(result, expected)

    def test__print_estimate_warning(self, capsys):
        """Test that a warning appears if there are more than 1000 expected columns"""
        # Setup
        metadata = get_multi_table_metadata()

        key_phrases = [
            r'PerformanceAlert:',
            r'large number of columns.',
            r'contact us at info@sdv.dev for enterprise solutions.'
        ]

        # Run
        with patch.object(HMASynthesizer,
                          '_estimate_num_columns',
                          return_value={'nesreca': 2000}):
            HMASynthesizer(metadata)

        captured = capsys.readouterr()

        # Assert
        for pattern in key_phrases:
            match = re.search(pattern, captured.out + captured.err)
            assert match is not None

        # Run
        with patch.object(HMASynthesizer,
                          '_estimate_num_columns',
                          return_value={'nesreca': 10}):
            HMASynthesizer(metadata)

        captured = capsys.readouterr()

        # Assert that small amount of columns don't trigger the message
        for pattern in key_phrases:
            match = re.search(pattern, captured.out + captured.err)
            assert match is None

    def test__get_extension_foreign_key_only(self):
        """Test the ``_get_extension`` method.

        Test when foreign key only is passed, just the ``num_rows`` is being captured.
        """
        # Setup
        instance = Mock()
        instance._get_pbar_args.return_value = {'desc': "(1/2) Tables 'A' and 'B' ('user_id')"}
        instance.metadata._get_all_foreign_keys.return_value = ['id_upravna_enota']
        instance._table_synthesizers = {'nesreca': Mock()}
        child_table = pd.DataFrame({
            'id_upravna_enota': [0, 1, 2, 3]
        })

        # Run
        result = HMASynthesizer._get_extension(
            instance,
            'nesreca',
            child_table,
            'id_upravna_enota',
            "(1/2) Tables 'A' and 'B' ('user_id')"
        )

        # Assert
        expected = pd.DataFrame({
            '__nesreca__id_upravna_enota__num_rows': [1, 1, 1, 1]
        })
        instance._get_pbar_args.assert_called_once_with(
            desc="(1/2) Tables 'A' and 'B' ('user_id')")

        pd.testing.assert_frame_equal(result, expected)

    def test__augment_table(self):
        """Test that ``augment_table`` extends the current table with extra columns.

        This also updates ``self._augmented_tables`` and ``self._max_child_rows``.
        """
        # Setup
        metadata = get_multi_table_metadata()
        instance = HMASynthesizer(metadata)
        metadata.add_column('nesreca', 'value', sdtype='numerical')
        metadata.add_column('oseba', 'oseba_value', sdtype='numerical')
        metadata.add_column('upravna_enota', 'name', sdtype='categorical')

        data = get_multi_table_data()
        data['nesreca']['value'] = [0, 1, 2, 3]
        data['oseba']['oseba_value'] = [0, 1, 2, 3]
        mock_get_pbar_args = Mock()
        mock_get_pbar_args.return_value = {}
        instance._get_pbar_args = mock_get_pbar_args

        # Run
        result = instance._augment_table(data['nesreca'], data, 'nesreca')

        # Assert
        expected_result = pd.DataFrame({
            'id_nesreca': [0, 1, 2, 3],
            'upravna_enota': [0, 1, 2, 3],
            'nesreca_val': [0, 1, 2, 3],
            'value': [0, 1, 2, 3],
            '__oseba__id_nesreca__correlation__0__0': [0.] * 4,
            '__oseba__id_nesreca__univariates__oseba_val__a': [1.] * 4,
            '__oseba__id_nesreca__univariates__oseba_val__b': [1.] * 4,
            '__oseba__id_nesreca__univariates__oseba_val__loc': [0., 1., 2., 3.],
            '__oseba__id_nesreca__univariates__oseba_val__scale': [1e-6] * 4,
            '__oseba__id_nesreca__univariates__oseba_value__a': [1.] * 4,
            '__oseba__id_nesreca__univariates__oseba_value__b': [1.] * 4,
            '__oseba__id_nesreca__univariates__oseba_value__loc': [0., 1., 2., 3.],
            '__oseba__id_nesreca__univariates__oseba_value__scale': [1e-6] * 4,
            '__oseba__id_nesreca__num_rows': [1.] * 4,
        })

        pd.testing.assert_frame_equal(expected_result, result)
        assert instance._augmented_tables == ['oseba', 'nesreca']
        assert instance._max_child_rows['__oseba__id_nesreca__num_rows'] == 1
        mock_get_pbar_args.assert_called_once_with(
            desc="(1/3) Tables 'nesreca' and 'oseba' ('id_nesreca')"
        )

    def test__pop_foreign_keys(self):
        """Test that this method removes the foreign keys from the ``table_data``."""
        # Setup
        instance = Mock()
        instance.metadata._get_all_foreign_keys.return_value = ['a', 'b']
        table_data = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': ['John', 'Doe', 'Johanna']
        })

        # Run
        result = HMASynthesizer._pop_foreign_keys(instance, table_data, 'table_name')

        # Assert
        pd.testing.assert_frame_equal(pd.DataFrame({'c': ['John', 'Doe', 'Johanna']}), table_data)
        np.testing.assert_array_equal(result['a'], [1, 2, 3])
        np.testing.assert_array_equal(result['b'], [2, 3, 4])

    def test__clear_nans(self):
        """Test that this method clears all the nans and substitutes them with expected values."""
        # Setup
        data = pd.DataFrame({
            'numerical': [0, 1, 2, 3, np.nan, np.nan],
            'categorical': ['John', np.nan, 'Johanna', 'John', np.nan, 'Doe'],
        })

        # Run
        HMASynthesizer._clear_nans(data)

        # Assert
        expected_data = pd.DataFrame({
            'numerical': [0, 1, 2, 3, 1.5, 1.5],
            'categorical': ['John', 'John', 'Johanna', 'John', 'John', 'Doe']
        })
        pd.testing.assert_frame_equal(expected_data, data)

    def test__model_tables(self):
        """Test that ``_model_tables`` performs the modeling.

        Modeling consists of getting the table for the given table name,
        learning the size of this table, removing the foreign keys and clearing
        any null values by using the ``_clear_nans`` method. Then, fitting the table model by
        calling ``fit_processed_data``,  adding back the foreign keys, updating the ``tables`` and
        marking the table name as modeled within the ``instance._augmented_tables``. This
        task has to be performed only on the root tables, the childs are being skipped
        since each row is being re-created from the parent.
        """
        # Setup
        upravna_enota_model = Mock()
        instance = Mock()
        instance._synthesizer = GaussianCopulaSynthesizer
        instance._get_pbar_args.return_value = {'desc': 'Modeling Tables'}

        metadata = get_multi_table_metadata()
        instance.metadata = metadata
        instance._augmented_tables = ['upravna_enota']
        instance._table_sizes = {'upravna_enota': 3}
        instance._table_synthesizers = {'upravna_enota': upravna_enota_model}
        instance._pop_foreign_keys.return_value = {'fk': [1, 2, 3]}
        input_data = {
            'upravna_enota': pd.DataFrame({
                'id_nesreca': [0, 1, 2],
                'upravna_enota': [0, 1, 2],
                'extended': ['a', 'b', 'c']
            }),
            'oseba': pd.DataFrame({
                'id_oseba': [0, 1, 2],
                'note': [0, 1, 2],
            })
        }
        augmented_data = input_data.copy()

        # Run
        HMASynthesizer._model_tables(instance, augmented_data)

        # Assert
        expected_result = pd.DataFrame({
            'id_nesreca': [0, 1, 2],
            'upravna_enota': [0, 1, 2],
            'extended': ['a', 'b', 'c'],
            'fk': [1, 2, 3]
        })
        pd.testing.assert_frame_equal(expected_result, augmented_data['upravna_enota'])

        instance._pop_foreign_keys.assert_called_once_with(
            input_data['upravna_enota'],
            'upravna_enota'
        )
        instance._clear_nans.assert_called_once_with(input_data['upravna_enota'])
        upravna_enota_model.fit_processed_data.assert_called_once_with(
            augmented_data['upravna_enota']
        )

    def test__augment_tables(self):
        """Test that ``_fit`` calls ``_model_tables`` only if the table has no parents."""
        # Setup
        metadata = get_multi_table_metadata()
        instance = HMASynthesizer(metadata)
        instance._augment_table = Mock()
        data = get_multi_table_data()
        data['nesreca']['value'] = [0, 1, 2, 3]
        data['oseba']['oseba_value'] = [0, 1, 2, 3]

        # Run
        instance._augment_tables(data)

        # Assert
        call_table = instance._augment_table.call_args[0][0]
        call_augmented_data = instance._augment_table.call_args[0][1]
        call_table_name = instance._augment_table.call_args[0][2]

        pd.testing.assert_frame_equal(call_table, data['upravna_enota'])
        for input_table, orig_table in zip(call_augmented_data.values(), data.values()):
            pd.testing.assert_frame_equal(input_table, orig_table)

        assert list(call_augmented_data) == list(data)
        assert call_table_name == 'upravna_enota'

    def test__finalize(self):
        """Test that the finalize method applies the final touches to the generated data.

        The process consists of applying the propper data types to each table, and dropping
        extra columns not present in the metadata.
        """
        # Setup
        instance = Mock()
        metadata = Mock()
        metadata._get_parent_map.return_value = {
            'sessions': ['users'],
            'transactions': ['sessions']
        }
        instance.metadata = metadata

        sampled_data = {
            'users': pd.DataFrame({
                'user_id': pd.Series([0, 1, 2], dtype=np.int64),
                'name': pd.Series(['John', 'Doe', 'Johanna'], dtype=object),
                'additional_column': pd.Series([0.1, 0.2, 0.3], dtype=float),
                'another_additional_column': pd.Series([0.1, 0.2, 0.5], dtype=float),
            }),
            'sessions': pd.DataFrame({
                'user_id': pd.Series([1, 2, 1], dtype=np.int64),
                'session_id': pd.Series(['a', 'b', 'c'], dtype=object),
                'os': pd.Series(['linux', 'mac', 'win'], dtype=object),
                'country': pd.Series(['us', 'us', 'es'], dtype=object),
            }),
            'transactions': pd.DataFrame({
                'transaction_id': pd.Series([1, 2, 3], dtype=np.int64),
                'session_id': pd.Series(['a', 'a', 'b'], dtype=object),
            }),
        }

        users_synth = Mock()
        users_synth._data_processor._dtypes = {'user_id': np.int64, 'name': str}
        sessions_synth = Mock()
        sessions_synth._data_processor._dtypes = {
            'user_id': np.int64,
            'session_id': str,
            'os': str,
            'country': str
        }
        transactions_synth = Mock()
        transactions_synth._data_processor._dtypes = {
            'transaction_id': np.int64,
            'session_id': str
        }

        instance._table_synthesizers = {
            'users': users_synth,
            'sessions': sessions_synth,
            'transactions': transactions_synth
        }

        # Run
        result = HMASynthesizer._finalize(instance, sampled_data)

        # Assert
        expected_result = {
            'users': pd.DataFrame({
                'user_id': pd.Series([0, 1, 2], dtype=np.int64),
                'name': pd.Series(['John', 'Doe', 'Johanna'], dtype=object),
            }),
            'sessions': pd.DataFrame({
                'user_id': pd.Series([1, 2, 1], dtype=np.int64),
                'session_id': pd.Series(['a', 'b', 'c'], dtype=object),
                'os': pd.Series(['linux', 'mac', 'win'], dtype=object),
                'country': pd.Series(['us', 'us', 'es'], dtype=object),
            }),
            'transactions': pd.DataFrame({
                'transaction_id': pd.Series([1, 2, 3], dtype=np.int64),
                'session_id': pd.Series(['a', 'a', 'b'], dtype=object),
            }),
        }
        for result_frame, expected_frame in zip(result.values(), expected_result.values()):
            pd.testing.assert_frame_equal(result_frame, expected_frame)

    def test__extract_parameters(self):
        """Test that parameters are being returned without the prefix."""
        # Setup
        parent_row = pd.Series({
            '__sessions__user_id__num_rows': 10,
            '__sessions__user_id__a': -1.0,
            '__sessions__user_id__b': 0.2,
            '__sessions__user_id__loc': 0.3,
        })
        instance = Mock()
        instance._max_child_rows = {'__sessions__user_id__num_rows': 10}

        float_formatter1 = MagicMock()
        float_formatter1._min_value = 0.
        float_formatter1._max_value = 5

        float_formatter2 = MagicMock()
        float_formatter2._min_value = 0.1
        float_formatter2._max_value = 5

        float_formatter3 = MagicMock()
        float_formatter3._min_value = 0
        float_formatter3._max_value = 1

        float_formatter4 = MagicMock()
        float_formatter4._min_value = 0.3
        float_formatter4._max_value = 0.7

        instance.extended_columns = {
            'sessions': {
                '__sessions__user_id__num_rows': float_formatter1,
                '__sessions__user_id__a': float_formatter2,
                '__sessions__user_id__b': float_formatter3,
                '__sessions__user_id__loc': float_formatter4,
            }
        }

        # Run
        result = HMASynthesizer._extract_parameters(instance, parent_row, 'sessions', 'user_id')

        # Assert
        expected_result = {
            'a': .1,
            'b': 0.2,
            'loc': 0.3,
            'num_rows': 5,
        }

        assert result == expected_result

    def test__recreate_child_synthesizer(self):
        """Test that this method returns a synthesizer for the given child table."""
        # Setup
        instance = Mock()
        parent_row = 'row'
        table_name = 'users'
        parent_table_name = 'sessions'
        table_meta = Mock()
        table_synthesizer = Mock()
        instance.metadata.tables = {'users': table_meta}
        instance.metadata._get_foreign_keys.return_value = ['session_id']
        instance._table_parameters = {'users': {'a': 1}}
        instance._table_synthesizers = {'users': table_synthesizer}

        # Run
        synthesizer = HMASynthesizer._recreate_child_synthesizer(
            instance,
            table_name,
            parent_table_name,
            parent_row,
        )

        # Assert
        assert synthesizer == instance._synthesizer.return_value
        assert synthesizer._data_processor == table_synthesizer._data_processor
        instance._synthesizer.assert_called_once_with(table_meta, a=1)
        synthesizer._set_parameters.assert_called_once_with(
            instance._extract_parameters.return_value
        )
        instance._extract_parameters.assert_called_once_with(parent_row, table_name, 'session_id')

    def test_get_learned_distributions(self):
        """Test that ``get_learned_distributions`` returns a dict.

        Test that it returns a dictionary with the name of the columns and the learned
        distribution and its parameters.
        """
        # Setup
        metadata = get_multi_table_metadata()
        instance = HMASynthesizer(metadata)
        data = {
            'nesreca': pd.DataFrame({
                'id_nesreca': np.arange(10),
                'upravna_enota': np.arange(10),
                'nesreca_val': np.arange(10),
            }),
            'oseba': pd.DataFrame({
                'upravna_enota': np.arange(10),
                'id_nesreca': np.arange(10),
                'oseba_val': np.arange(10),
            }),
            'upravna_enota': pd.DataFrame({
                'id_upravna_enota': np.arange(10),
                'upravna_val': [10, np.nan] * 5,
            }),
        }

        instance.fit(data)

        # Run
        result = instance.get_learned_distributions('upravna_enota')

        # Assert
        assert list(result) == ['upravna_val']
        assert result['upravna_val'] == {
            'distribution': 'beta',
            'learned_parameters': {
                'a': 1.0,
                'b': 1.0,
                'loc': 10.0,
                'scale': 0.0
            }
        }

    def test_get_learned_distributions_raises_an_error(self):
        """Test that ``get_learned_distributions`` raises an error."""
        # Setup
        metadata = get_multi_table_metadata()
        metadata.add_column('nesreca', 'value', sdtype='numerical')
        metadata.add_column('oseba', 'value', sdtype='numerical')
        metadata.add_column('upravna_enota', 'a_value', sdtype='numerical')
        instance = HMASynthesizer(metadata)

        # Run and Assert
        error_msg = re.escape(
            "Distributions have not been learned yet. Please fit your model first using 'fit'."
        )
        with pytest.raises(ValueError, match=error_msg):
            instance.get_learned_distributions('upravna_enota')

    def test__add_foreign_key_columns(self):
        """Test that the ``_add_foreign_key_columns`` method adds foreign keys."""
        # Setup
        instance = Mock()
        metadata = Mock()
        metadata._get_foreign_keys.return_value = ['primary_user_id', 'secondary_user_id']
        instance.metadata = metadata

        instance._find_parent_ids.return_value = pd.Series([2, 1, 2], name='secondary_user_id')

        parent_table = pd.DataFrame({
            'user_id': pd.Series([0, 1, 2], dtype=np.int64),
            'name': pd.Series(['John', 'Doe', 'Johanna'], dtype=object),
        })
        child_table = pd.DataFrame({
            'transaction_id': pd.Series([1, 2, 3], dtype=np.int64),
            'primary_user_id': pd.Series([0, 0, 1], dtype=np.int64)
        })

        instance._table_synthesizers = {
            'users': Mock(),
            'transactions': Mock()
        }

        # Run
        HMASynthesizer._add_foreign_key_columns(
            instance,
            child_table,
            parent_table,
            'transactions',
            'users')

        # Assert
        expected_parent_table = pd.DataFrame({
            'user_id': pd.Series([0, 1, 2], dtype=np.int64),
            'name': pd.Series(['John', 'Doe', 'Johanna'], dtype=object),
        })
        expected_child_table = pd.DataFrame({
            'transaction_id': pd.Series([1, 2, 3], dtype=np.int64),
            'primary_user_id': pd.Series([0, 0, 1], dtype=np.int64),
            'secondary_user_id': pd.Series([2, 1, 2], dtype=np.int64)
        })
        pd.testing.assert_frame_equal(expected_parent_table, parent_table)
        pd.testing.assert_frame_equal(expected_child_table, child_table)

    def test__estimate_num_columns_to_be_modeled_multiple_foreign_keys(self):
        """Test it when there are two relationships between a parent and a child tables.

        To check that the number columns is correct we Mock the ``_finalize`` method
        and compare its output with the estimated number of columns.
        """
        # Setup
        parent = pd.DataFrame({'id': [0, 1, 2]})
        child = pd.DataFrame({
            'id': [0, 1, 2],
            'id1': [0, 1, 2],
            'id2': [0, 1, 2],
            'col1': [0, 1, 2]
        })
        data = {'parent': parent, 'child': child}
        metadata = MultiTableMetadata.load_from_dict({
            'tables': {
                'parent': {
                    'primary_key': 'id',
                    'columns': {
                        'id': {'sdtype': 'id'},
                    }
                },
                'child': {
                    'primary_key': 'id',
                    'columns': {
                        'id': {'sdtype': 'id'},
                        'id1': {'sdtype': 'id'},
                        'id2': {'sdtype': 'id'},
                        'col1': {'sdtype': 'numerical'},
                    }
                },
            },
            'relationships': [
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child',
                    'child_foreign_key': 'id1'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child',
                    'child_foreign_key': 'id2'
                },
            ]
        })
        synthesizer = HMASynthesizer(metadata)
        synthesizer._finalize = Mock()

        # Run estimation
        estimated_num_columns = synthesizer._estimate_num_columns()

        # Run actual modeling
        synthesizer.fit(data)
        synthesizer.sample()

        # Assert estimated number of columns is correct
        tables = synthesizer._finalize.call_args[0][0]
        for table_name, table in tables.items():
            # Subract all the id columns present in the data, as those are not estimated
            num_table_cols = len(table.columns)
            if table_name == 'parent':
                num_table_cols -= 1
            if table_name == 'child':
                num_table_cols -= 3

            assert num_table_cols == estimated_num_columns[table_name]

    def test__estimate_num_columns_to_be_modeled_different_distributions(self):
        """Test it when there the default distributions of the tables have been changed.

        The schema will be 1 parent and 5 children, all of which have different distributions,
        all of which have two foreign keys to the parent table.

        To check that the number columns is correct we Mock the ``_finalize`` method
        and compare its output with the estimated number of columns.
        """
        # Setup
        parent = pd.DataFrame({'id': [0, 1, 2]})
        child = pd.DataFrame({
            'id': [0, 1, 2],
            'id1': [0, 1, 2],
            'id2': [0, 1, 2],
            'col': [.2, .3, .2]
        })
        data = {
            'parent': parent,
            'child_norm': child,
            'child_beta': child,
            'child_gamma': child,
            'child_truncnorm': child,
            'child_uniform': child
        }
        child_dict = {
            'primary_key': 'id',
            'columns': {
                'id': {'sdtype': 'id'},
                'id1': {'sdtype': 'id'},
                'id2': {'sdtype': 'id'},
                'col': {'sdtype': 'numerical'},
            }
        }
        metadata = MultiTableMetadata.load_from_dict({
            'tables': {
                'parent': {
                    'primary_key': 'id',
                    'columns': {
                        'id': {'sdtype': 'id'},
                    }
                },
                'child_norm': child_dict,
                'child_beta': child_dict,
                'child_gamma': child_dict,
                'child_truncnorm': child_dict,
                'child_uniform': child_dict,
            },
            'relationships': [
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_norm',
                    'child_foreign_key': 'id1'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_norm',
                    'child_foreign_key': 'id2'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_beta',
                    'child_foreign_key': 'id1'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_beta',
                    'child_foreign_key': 'id2'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_truncnorm',
                    'child_foreign_key': 'id1'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_truncnorm',
                    'child_foreign_key': 'id2'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_uniform',
                    'child_foreign_key': 'id1'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_uniform',
                    'child_foreign_key': 'id2'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_gamma',
                    'child_foreign_key': 'id1'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'id',
                    'child_table_name': 'child_gamma',
                    'child_foreign_key': 'id2'
                },
            ]
        })
        synthesizer = HMASynthesizer(metadata)
        synthesizer.set_table_parameters(
            table_name='child_norm',
            table_parameters={'default_distribution': 'norm'}
        )
        synthesizer.set_table_parameters(
            table_name='child_gamma',
            table_parameters={'default_distribution': 'gamma'}
        )
        synthesizer.set_table_parameters(
            table_name='child_truncnorm',
            table_parameters={'default_distribution': 'truncnorm'}
        )
        synthesizer.set_table_parameters(
            table_name='child_uniform',
            table_parameters={'default_distribution': 'uniform'}
        )
        synthesizer._finalize = Mock()

        # Run estimation
        estimated_num_columns = synthesizer._estimate_num_columns()

        # Run actual modeling
        synthesizer.fit(data)
        synthesizer.sample()

        # Assert estimated number of columns is correct
        tables = synthesizer._finalize.call_args[0][0]
        for table_name, table in tables.items():
            # Subract all the id columns present in the data, as those are not estimated
            num_table_cols = len(table.columns)
            if table_name == 'parent':
                num_table_cols -= 1
            else:
                num_table_cols -= 3

            assert num_table_cols == estimated_num_columns[table_name]

    def test__estimate_num_columns_to_be_modeled(self):
        """Test the estimated number of columns is exactly the number of columns to be modeled.

        To check that the number columns is correct we Mock the ``_finalize`` method
        and compare its output with the estimated number of columns.

        The dataset used follows the structure below:
            R1 R2
            || /
            GP
            | \
            P-C
        """
        # Setup
        root1 = pd.DataFrame({'R1': [0, 1, 2]})
        root2 = pd.DataFrame({'R2': [0, 1, 2], 'data': [0, 1, 2]})
        grandparent = pd.DataFrame({
            'GP': [0, 1, 2], 'R1_1': [0, 1, 2], 'R1_2': [0, 1, 2], 'R2': [0, 1, 2]
        })
        parent = pd.DataFrame({'P': [0, 1, 2], 'GP': [0, 1, 2]})
        child = pd.DataFrame({'C': [0, 1, 2], 'P': [0, 1, 2], 'GP': [0, 1, 2]})
        data = {
            'root1': root1,
            'root2': root2,
            'grandparent': grandparent,
            'parent': parent,
            'child': child
        }
        metadata = MultiTableMetadata.load_from_dict({
            'tables': {
                'root1': {
                    'primary_key': 'R1',
                    'columns': {
                        'R1': {'sdtype': 'id'},
                    }
                },
                'root2': {
                    'primary_key': 'R2',
                    'columns': {
                        'R2': {'sdtype': 'id'},
                        'data': {'sdtype': 'numerical'}
                    }
                },
                'grandparent': {
                    'primary_key': 'GP',
                    'columns': {
                        'GP': {'sdtype': 'id'},
                        'R1_1': {'sdtype': 'id'},
                        'R1_2': {'sdtype': 'id'},
                        'R2': {'sdtype': 'id'},
                    }
                },
                'parent': {
                    'primary_key': 'P',
                    'columns': {
                        'P': {'sdtype': 'id'},
                        'GP': {'sdtype': 'id'},
                    }
                },
                'child': {
                    'primary_key': 'C',
                    'columns': {
                        'C': {'sdtype': 'id'},
                        'P': {'sdtype': 'id'},
                        'GP': {'sdtype': 'id'},
                    }
                }
            },
            'relationships': [
                {
                    'parent_table_name': 'root1',
                    'parent_primary_key': 'R1',
                    'child_table_name': 'grandparent',
                    'child_foreign_key': 'R1_1'
                },
                {
                    'parent_table_name': 'root1',
                    'parent_primary_key': 'R1',
                    'child_table_name': 'grandparent',
                    'child_foreign_key': 'R1_2'
                },
                {
                    'parent_table_name': 'root2',
                    'parent_primary_key': 'R2',
                    'child_table_name': 'grandparent',
                    'child_foreign_key': 'R2'
                },
                {
                    'parent_table_name': 'grandparent',
                    'parent_primary_key': 'GP',
                    'child_table_name': 'parent',
                    'child_foreign_key': 'GP'
                },
                {
                    'parent_table_name': 'grandparent',
                    'parent_primary_key': 'GP',
                    'child_table_name': 'child',
                    'child_foreign_key': 'GP'
                },
                {
                    'parent_table_name': 'parent',
                    'parent_primary_key': 'P',
                    'child_table_name': 'child',
                    'child_foreign_key': 'P'
                },
            ]
        })
        synthesizer = HMASynthesizer(metadata)
        synthesizer._finalize = Mock()

        # Run estimation
        estimated_num_columns = synthesizer._estimate_num_columns()

        # Run actual modeling
        synthesizer.fit(data)
        synthesizer.sample(scale=1)

        # Assert estimated number of columns is correct
        tables = synthesizer._finalize.call_args[0][0]
        for table_name, table in tables.items():
            # Subract all the id columns present in the data, as those are not estimated
            num_table_cols = len(table.columns)
            if table_name == 'child':
                num_table_cols -= 3
            if table_name == 'parent':
                num_table_cols -= 2
            if table_name == 'grandparent':
                num_table_cols -= 4
            if table_name in {'root1', 'root2'}:
                num_table_cols -= 1

            assert num_table_cols == estimated_num_columns[table_name]

    def test__estimate_num_columns_to_be_modeled_various_sdtypes(self):
        """Test the estimated number of columns is correct for various sdtypes.

        To check that the number columns is correct we Mock the ``_finalize`` method
        and compare its output with the estimated number of columns.

        The dataset used follows the structure below:
            R1 R2
            | /
            GP
            |
            P
        """
        # Setup
        root1 = pd.DataFrame({'R1': [0, 1, 2]})
        root2 = pd.DataFrame({'R2': [0, 1, 2], 'data': [0, 1, 2]})
        grandparent = pd.DataFrame({'GP': [0, 1, 2], 'R1': [0, 1, 2], 'R2': [0, 1, 2]})
        parent = pd.DataFrame({
            'P': [0, 1, 2],
            'GP': [0, 1, 2],
            'numerical': [.1, .5, np.nan],
            'categorical': ['a', np.nan, 'c'],
            'datetime': [None, '2019-01-02', '2019-01-03'],
            'boolean': [float('nan'), False, True],
            'id': [0, 1, 2],
        })
        data = {
            'root1': root1,
            'root2': root2,
            'grandparent': grandparent,
            'parent': parent,
        }
        metadata = MultiTableMetadata.load_from_dict({
            'tables': {
                'root1': {
                    'primary_key': 'R1',
                    'columns': {
                        'R1': {'sdtype': 'id'},
                    }
                },
                'root2': {
                    'primary_key': 'R2',
                    'columns': {
                        'R2': {'sdtype': 'id'},
                        'data': {'sdtype': 'numerical'}
                    }
                },
                'grandparent': {
                    'primary_key': 'GP',
                    'columns': {
                        'GP': {'sdtype': 'id'},
                        'R1': {'sdtype': 'id'},
                        'R2': {'sdtype': 'id'},
                    }
                },
                'parent': {
                    'primary_key': 'P',
                    'columns': {
                        'P': {'sdtype': 'id'},
                        'GP': {'sdtype': 'id'},
                        'numerical': {'sdtype': 'numerical'},
                        'categorical': {'sdtype': 'categorical'},
                        'datetime': {'sdtype': 'datetime'},
                        'boolean': {'sdtype': 'boolean'},
                        'id': {'sdtype': 'id'},
                    }
                }
            },
            'relationships': [
                {
                    'parent_table_name': 'root1',
                    'parent_primary_key': 'R1',
                    'child_table_name': 'grandparent',
                    'child_foreign_key': 'R1'
                },
                {
                    'parent_table_name': 'root2',
                    'parent_primary_key': 'R2',
                    'child_table_name': 'grandparent',
                    'child_foreign_key': 'R2'
                },
                {
                    'parent_table_name': 'grandparent',
                    'parent_primary_key': 'GP',
                    'child_table_name': 'parent',
                    'child_foreign_key': 'GP'
                },
            ]
        })
        synthesizer = HMASynthesizer(metadata)
        synthesizer._finalize = Mock()

        # Run estimation
        estimated_num_columns = synthesizer._estimate_num_columns()

        # Run actual modeling
        synthesizer.fit(data)
        synthesizer.sample()

        # Assert estimated number of columns is correct
        tables = synthesizer._finalize.call_args[0][0]
        for table_name, table in tables.items():
            # Subract all the id columns present in the data, as those are not estimated
            num_table_cols = len(table.columns)
            if table_name in {'parent', 'grandparent'}:
                num_table_cols -= 3
            if table_name in {'root1', 'root2'}:
                num_table_cols -= 1

            assert num_table_cols == estimated_num_columns[table_name]
