from src.a20_lobby_logic._test_util.a20_str import (
    lobbys_str,
    lobby_id_str,
    lobby_mstr_dir_str,
)


def test_str_functions_ReturnsObj():
    assert lobbys_str() == "lobbys"
    assert lobby_id_str() == "lobby_id"
    assert lobby_mstr_dir_str() == "lobby_mstr_dir"
