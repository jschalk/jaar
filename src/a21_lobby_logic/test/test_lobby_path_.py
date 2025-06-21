from src.a00_data_toolbox.file_toolbox import create_path
from src.a21_lobby_logic.lobby_path import (
    LobbyID,
    create_bank_mstr_dir_path,
    create_fis_dir_path,
    create_lobby_dir_path,
)
from src.a21_lobby_logic.test._util.a21_env import get_module_temp_dir
from src.a21_lobby_logic.test._util.a21_str import (
    lobby_id_str,
    lobby_mstr_dir_str,
    lobbys_str,
)


def test_str_functions_ReturnsObjs():
    assert lobbys_str() == "lobbys"
    assert lobby_id_str() == "lobby_id"
    assert lobby_mstr_dir_str() == "lobby_mstr_dir"


def test_LobbyID_Exists():
    assert LobbyID("chat23") == "chat23"


def test_create_lobby_dir_path_ReturnsObj():
    # ESTABLISH
    x_lobby_mstr_dir = get_module_temp_dir()
    c23_str = "chat23"

    # WHEN
    gen_c23_dir_path = create_lobby_dir_path(x_lobby_mstr_dir, c23_str)

    # THEN
    lobbys_dir = create_path(x_lobby_mstr_dir, lobbys_str())
    expected_c23_path = create_path(lobbys_dir, c23_str)
    assert gen_c23_dir_path == expected_c23_path


def test_create_fis_dir_path_ReturnsObj():
    # ESTABLISH
    x_lobby_mstr_dir = get_module_temp_dir()
    c23_str = "chat23"
    m23_str = "music23"

    # WHEN
    gen_m23_dir_path = create_fis_dir_path(x_lobby_mstr_dir, c23_str, m23_str)

    # THEN
    lobbys_dir = create_path(x_lobby_mstr_dir, lobbys_str())
    c23_dir = create_path(lobbys_dir, c23_str)
    fiss_path = create_path(c23_dir, "fiss")
    expected_m23_path = create_path(fiss_path, m23_str)
    assert gen_m23_dir_path == expected_m23_path


def test_create_bank_mstr_dir_path_ReturnsObj():
    # ESTABLISH
    x_lobby_mstr_dir = get_module_temp_dir()
    c23_str = "chat23"
    m23_str = "music23"

    # WHEN
    gen_m23_dir_path = create_bank_mstr_dir_path(x_lobby_mstr_dir, c23_str, m23_str)

    # THEN
    lobbys_dir = create_path(x_lobby_mstr_dir, lobbys_str())
    c23_dir = create_path(lobbys_dir, c23_str)
    fiss_dir = create_path(c23_dir, "fiss")
    m23_dir = create_path(fiss_dir, m23_str)
    expected_m23_path = create_path(m23_dir, "bank_mstr_dir")
    assert gen_m23_dir_path == expected_m23_path
