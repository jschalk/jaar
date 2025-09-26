from src.ch21_lobby_logic._ref.ch21_keywords import (
    LobbyID_str,
    lobby_id_str,
    lobby_mstr_dir_str,
    lobbys_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert LobbyID_str() == "LobbyID"
    assert lobbys_str() == "lobbys"
    assert lobby_id_str() == "lobby_id"
    assert lobby_mstr_dir_str() == "lobby_mstr_dir"
