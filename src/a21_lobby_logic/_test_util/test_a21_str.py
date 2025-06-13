from src.a21_lobby_logic._test_util.a21_str import (
    lobby_id_str,
    lobby_mstr_dir_str,
    lobbys_str,
)


def test_str_functions_ReturnsObj():
    assert lobbys_str() == "lobbys"
    assert lobby_id_str() == "lobby_id"
    assert lobby_mstr_dir_str() == "lobby_mstr_dir"
