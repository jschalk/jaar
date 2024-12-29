from src.f09_brick.pandas_tool import dataframe_to_dict
from pandas import DataFrame


def test_dataframe_to_dict_ReturnsObj_Empty():
    # ESTABLISH
    data = {
        "id": [],
        "name": [],
        "age": [],
        "city": [],
    }
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, "name")

    # THEN
    expected_dict = {}
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str


def test_dataframe_to_dict_ReturnsObj_WithValues():
    # ESTABLISH
    data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["New York", "Los Angeles", "Chicago"],
    }
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, "name")

    # THEN
    expected_dict = {
        "Alice": {"name": "Alice", "age": 25, "city": "New York"},
        "Bob": {"name": "Bob", "age": 30, "city": "Los Angeles"},
        "Charlie": {"name": "Charlie", "age": 35, "city": "Chicago"},
    }
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str


def test_dataframe_to_dict_ReturnsObj_WithOutIndex():
    # ESTABLISH
    data = {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["New York", "Los Angeles", "Chicago"],
    }
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, "name")

    # THEN
    expected_dict = {
        "Alice": {"name": "Alice", "age": 25, "city": "New York"},
        "Bob": {"name": "Bob", "age": 30, "city": "Los Angeles"},
        "Charlie": {"name": "Charlie", "age": 35, "city": "Chicago"},
    }
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str
