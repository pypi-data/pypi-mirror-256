from datetime import datetime
from unittest.mock import patch

import numpy as np
import pandas as pd

from sdv.utils import (
    convert_to_timedelta, create_unique_name, get_datetime_format, is_datetime_type)
from tests.utils import SeriesMatcher


@patch('sdv.utils.pd.to_timedelta')
def test_convert_to_timedelta(to_timedelta_mock):
    """Test that nans and values are properly converted to timedeltas."""
    # Setup
    column = pd.Series([7200, 3600, np.nan])
    to_timedelta_mock.return_value = pd.Series([
        pd.Timedelta(hours=1),
        pd.Timedelta(hours=2),
        pd.Timedelta(hours=0)
    ], dtype='timedelta64[ns]')

    # Run
    converted_column = convert_to_timedelta(column)

    # Assert
    to_timedelta_mock.assert_called_with(SeriesMatcher(pd.Series([7200, 3600, 0.0])))
    expected_column = pd.Series([
        pd.Timedelta(hours=1),
        pd.Timedelta(hours=2),
        pd.NaT
    ], dtype='timedelta64[ns]')
    pd.testing.assert_series_equal(converted_column, expected_column)


def test_get_datetime_format():
    """Test the ``get_datetime_format``.

    Setup:
        - string value representing datetime.
        - list of values with a datetime.
        - series with a datetime.

    Output:
        - The expected output is the format of the datetime representation.
    """
    # Setup
    string_value = '2021-02-02'
    list_value = [np.nan, '2021-02-02']
    series_value = pd.Series(['2021-02-02T12:10:59'])

    # Run
    string_out = get_datetime_format(string_value)
    list_out = get_datetime_format(list_value)
    series_out = get_datetime_format(series_value)

    # Assert
    expected_output = '%Y-%m-%d'
    assert string_out == expected_output
    assert list_out == expected_output
    assert series_out == '%Y-%m-%dT%H:%M:%S'


def test_is_datetime_type_with_datetime_series():
    """Test the ``is_datetime_type`` function when a datetime series is passed.

    Expect to return True when a datetime series is passed.

    Input:
    - A pandas.Series of type `datetime64[ns]`
    Output:
    - True
    """
    # Setup
    data = pd.Series([
        pd.to_datetime('2020-01-01'),
        pd.to_datetime('2020-01-02'),
        pd.to_datetime('2020-01-03')
    ],
    )

    # Run
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime


def test_is_datetime_type_with_mixed_array():
    """Test the ``is_datetime_type`` function with a list of mixed datetime types."""
    # Setup
    data = [
        pd.to_datetime('2020-01-01'),
        '1890-03-05',
        pd.Timestamp('01-01-01'),
        datetime(2020, 1, 1),
        np.nan
    ]

    # Run
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime


def test_is_datetime_type_with_invalid_strings_in_list():
    """Test the ``is_datetime_type`` function with a invalid datetime in a list."""
    # Setup
    data = [
        pd.to_datetime('2020-01-01'),
        '1890-03-05',
        pd.Timestamp('01-01-01'),
        datetime(2020, 1, 1),
        'invalid',
        np.nan
    ]

    # Run
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime is False


def test_is_datetime_type_with_datetime():
    """Test the ``is_datetime_type`` function when a datetime is passed.

    Expect to return True when a datetime variable is passed.

    Input:
    - datetime.Datetime
    Output:
    - True
    """
    # Setup
    data = datetime(2020, 1, 1)

    # Run
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime


def test_is_datetime_type_with_timestamp():
    """Test the ``is_datetime_type`` function when a Timestamp is passed.

    Expect to return True when a datetime variable is passed.

    Input:
    - datetime.Datetime
    Output:
    - True
    """
    # Setup
    data = pd.Timestamp('2020-01-10')
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime


def test_is_datetime_type_with_pandas_datetime():
    """Test the ``is_datetime_type`` function when a pandas.datetime is passed.

    Expect to return True when a datetime variable is passed.

    Input:
    - pandas.Datetime
    Output:
    - True
    """
    # Setup
    data = pd.to_datetime('2020-01-01')

    # Run
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime


def test_is_datetime_type_with_int():
    """Test the ``is_datetime_type`` function when an int is passed.

    Expect to return False when an int variable is passed.

    Input:
    - int
    Output:
    - False
    """
    # Setup
    data = 2

    # Run
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime is False


def test_is_datetime_type_with_datetime_str():
    """Test the ``is_datetime_type`` function when an valid datetime string is passed.

    Expect to return True when a valid string representing datetime is passed.

    Input:
    - string
    Output:
    - True
    """
    # Setup
    value = '2021-02-02'

    # Run
    is_datetime = is_datetime_type(value)

    # Assert
    assert is_datetime


def test_is_datetime_type_with_invalid_str():
    """Test the ``is_datetime_type`` function when an invalid string is passed.

    Expect to return False when an invalid string is passed.

    Input:
    - string
    Output:
    - False
    """
    # Setup
    value = 'abcd'

    # Run
    is_datetime = is_datetime_type(value)

    # Assert
    assert is_datetime is False


def test_is_datetime_type_with_int_series():
    """Test the ``is_datetime_type`` function when an int series is passed.

    Expect to return False when an int series variable is passed.

    Input:
    -  pd.Series of type int
    Output:
    - False
    """
    # Setup
    data = pd.Series([1, 2, 3, 4])

    # Run
    is_datetime = is_datetime_type(data)

    # Assert
    assert is_datetime is False


def test_create_unique_name():
    """Test the ``create_unique_name`` method."""
    # Setup
    name = 'name'
    existing_names = ['name', 'name_', 'name__']

    # Run
    result = create_unique_name(name, existing_names)

    # Assert
    assert result == 'name___'
