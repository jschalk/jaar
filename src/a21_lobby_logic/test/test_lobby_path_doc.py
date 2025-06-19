from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.a17_idea_logic.test._util.a17_str import world_id_str
from src.a21_lobby_logic.lobby_path import (
    create_lobby_dir_path,
    create_vow_mstr_dir_path,
    create_world_dir_path,
)
from src.a21_lobby_logic.test._util.a21_str import lobby_id_str, lobby_mstr_dir_str

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
        lobby_mstr_dir_str(), lobby_id_str(), world_id_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_world_dir_path) == doc_str


def test_create_vow_mstr_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_vow_mstr_dir_path(
        lobby_mstr_dir_str(), lobby_id_str(), world_id_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_vow_mstr_dir_path) == doc_str
