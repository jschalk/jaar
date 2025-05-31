from pandas import DataFrame
from pytest import raises as pytest_raises
from src.a17_idea_logic.idea_db_tool import is_column_type_valid


def test_is_column_type_valid_ReturnsObjs():
    assert is_column_type_valid(DataFrame({"ID": [1, 2, 3]}), "ID", "INT")
    assert is_column_type_valid(DataFrame({"Age": [1.5, 2.5, 3.0]}), "Age", "REAL")
    assert is_column_type_valid(DataFrame({"Per": ["Sue", "Bob"]}), "Per", "TEXT")
    assert not is_column_type_valid(DataFrame({"Per": ["Sue", "Bob"]}), "Age", "INT")
    assert not is_column_type_valid(DataFrame({"Age": [20, 30, 40]}), "Age", "REAL")
    assert is_column_type_valid(DataFrame({"Num": [1.0, None]}), "Num", "REAL")
    assert is_column_type_valid(DataFrame({"Num": [None, None]}), "Num", "REAL")
    assert not is_column_type_valid(DataFrame({"Num": [None, None]}), "Per", "REAL")
    with pytest_raises(Exception) as excinfo:
        is_column_type_valid(DataFrame({"Num": [None, None]}), "Per", "int64")
    assert str(excinfo.value) == "int64 is not valid sqlite_type"
