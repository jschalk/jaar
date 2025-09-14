from src.a21_lobby_logic._ref.a21_terms import (
    lobby_id_str,
    lobby_mstr_dir_str,
    lobbys_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert lobbys_str() == "lobbys"
    assert lobby_id_str() == "lobby_id"
    assert lobby_mstr_dir_str() == "lobby_mstr_dir"
