from src.a00_data_toolbox.test._util.a00_str import (
    INSERT_str,
    UPDATE_str,
    sqlite_datatype_str,
)


def test_str_functions_ReturnsObj():
    assert INSERT_str() == "INSERT"
    assert UPDATE_str() == "UPDATE"
    assert sqlite_datatype_str() == "sqlite_datatype"
