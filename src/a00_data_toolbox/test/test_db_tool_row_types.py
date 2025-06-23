import pytest
from src.a00_data_toolbox.db_toolbox import get_nonconvertible_columns


def test_get_nonconvertible_columns_Scenario0_AllValid():
    # ESTABLISH
    row = {"id": "123", "score": "98.6", "name": "Alice"}
    col_types = {"id": "Integer", "score": "Real", "name": "Text"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == []


def test_get_nonconvertible_columns_Scenario1_InvalidInteger():
    # ESTABLISH
    row = {"id": "abc", "score": "98.6", "name": "Alice"}
    col_types = {"id": "Integer", "score": "Real", "name": "Text"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == ["id"]


def test_get_nonconvertible_columns_Scenario2_InvalidReal():
    # ESTABLISH
    row = {"id": "123", "score": "not_a_number", "name": "Bob"}
    col_types = {"id": "Integer", "score": "Real", "name": "Text"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == ["score"]


def test_get_nonconvertible_columns_Scenario3_MultipleInvalid():
    # ESTABLISH
    row = {"id": "xyz", "score": "none", "name": "Charlie"}
    col_types = {"id": "Integer", "score": "Real", "name": "Text"}
    result = get_nonconvertible_columns(row, col_types)

    # WHEN / THEN
    assert set(result) == {"id", "score"}


def test_get_nonconvertible_columns_Scenario4_UnsupportedType():
    # ESTABLISH
    row = {"id": "123", "score": "90", "active": "yes"}
    col_types = {
        "id": "Integer",
        "score": "Real",
        "active": "Boolean",
    }

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == ["active"]


def test_get_nonconvertible_columns_Scenario5_MissingColumnsAreIgnored():
    # ESTABLISH
    row = {"score": "100.0"}
    col_types = {"id": "Integer", "score": "Real"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == []
