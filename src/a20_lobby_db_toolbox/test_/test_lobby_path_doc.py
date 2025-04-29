from src.a02_finance_logic._utils.strs_a02 import (
    owner_name_str,
    deal_time_str,
    fisc_tag_str,
    world_id_str,
)
from src.a06_bud_logic._utils.str_a06 import event_int_str
from src.a20_lobby_db_toolbox._utils.str_a20 import (
    lobbys_str,
    lobby_id_str,
    lobby_mstr_dir_str,
)
from src.a20_lobby_db_toolbox.lobby_path import (
    create_lobby_dir_path,
    create_world_dir_path,
    create_fisc_mstr_dir_path,
)
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system

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


def test_create_fisc_mstr_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_mstr_dir_path(
        lobby_mstr_dir_str(), lobby_id_str(), world_id_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_mstr_dir_path) == doc_str
