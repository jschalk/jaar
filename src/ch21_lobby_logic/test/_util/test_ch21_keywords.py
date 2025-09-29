from src.ch21_lobby_logic._ref.ch21_keywords import (
    Ch21Keywords,
    LobbyID_str,
    lobby_id_str,
    lobby_mstr_dir_str,
    lobbys_str,
)


def test_Ch21Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch21Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert LobbyID_str() == "LobbyID"
    assert lobbys_str() == "lobbys"
    assert lobby_id_str() == "lobby_id"
    assert lobby_mstr_dir_str() == "lobby_mstr_dir"
