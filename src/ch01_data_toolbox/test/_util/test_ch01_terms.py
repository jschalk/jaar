from src.ch01_data_toolbox._ref.ch01_terms import (
    INSERT_str,
    UPDATE_str,
    sqlite_datatype_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert INSERT_str() == "INSERT"
    assert UPDATE_str() == "UPDATE"
    assert sqlite_datatype_str() == "sqlite_datatype"
