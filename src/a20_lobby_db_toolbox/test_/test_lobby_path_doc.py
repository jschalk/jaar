from src.a02_finance_toolboxs.deal import owner_name_str, deal_time_str, fisc_title_str
from src.a08_bud_atom_logic.atom_config import event_int_str
from src.a20_lobby_db_toolbox.lobby_path import create_lobby_dir_path, lobby_id_str
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system

LINUX_OS = platform_system() == "Linux"


def test_create_lobby_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_lobby_dir_path("lobby_mstr_dir", lobby_id_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_lobby_dir_path) == doc_str
