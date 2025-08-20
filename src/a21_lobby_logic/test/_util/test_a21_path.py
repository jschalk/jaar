from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_idea_logic.test._util.a17_str import world_name_str
from src.a21_lobby_logic.a21_path import (
    LobbyID,
    create_lobby_dir_path,
    create_moment_mstr_dir_path,
    create_world_dir_path,
)
from src.a21_lobby_logic.test._util.a21_env import get_module_temp_dir
from src.a21_lobby_logic.test._util.a21_str import (
    lobby_id_str,
    lobby_mstr_dir_str,
    lobbys_str,
)


def test_str_functions_ReturnsObjs():
    # ESTABLISH / WHEN / THEN
    assert lobbys_str() == "lobbys"
    assert lobby_id_str() == "lobby_id"
    assert lobby_mstr_dir_str() == "lobby_mstr_dir"


def test_LobbyID_Exists():
    # ESTABLISH / WHEN / THEN
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


def test_create_world_dir_path_ReturnsObj():
    # ESTABLISH
    x_lobby_mstr_dir = get_module_temp_dir()
    c23_str = "chat23"
    m23_str = "music23"

    # WHEN
    gen_m23_dir_path = create_world_dir_path(x_lobby_mstr_dir, c23_str, m23_str)

    # THEN
    lobbys_dir = create_path(x_lobby_mstr_dir, lobbys_str())
    c23_dir = create_path(lobbys_dir, c23_str)
    worlds_path = create_path(c23_dir, "worlds")
    expected_m23_path = create_path(worlds_path, m23_str)
    assert gen_m23_dir_path == expected_m23_path


def test_create_moment_mstr_dir_path_ReturnsObj():
    # ESTABLISH
    x_lobby_mstr_dir = get_module_temp_dir()
    c23_str = "chat23"
    m23_str = "music23"

    # WHEN
    gen_m23_dir_path = create_moment_mstr_dir_path(x_lobby_mstr_dir, c23_str, m23_str)

    # THEN
    lobbys_dir = create_path(x_lobby_mstr_dir, lobbys_str())
    c23_dir = create_path(lobbys_dir, c23_str)
    worlds_dir = create_path(c23_dir, "worlds")
    m23_dir = create_path(worlds_dir, m23_str)
    expected_m23_path = create_path(m23_dir, "moment_mstr_dir")
    assert gen_m23_dir_path == expected_m23_path


LINUX_OS = platform_system() == "Linux"


def test_create_lobby_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_lobby_dir_path(lobby_mstr_dir_str(), lobby_id_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_lobby_dir_path) == doc_str


def test_create_world_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_world_dir_path(
        lobby_mstr_dir_str(), lobby_id_str(), world_name_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_world_dir_path) == doc_str


def test_create_moment_mstr_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_mstr_dir_path(
        lobby_mstr_dir_str(), lobby_id_str(), world_name_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_mstr_dir_path) == doc_str
