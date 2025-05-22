from src.a02_finance_logic._utils.strs_a02 import owner_name_str
from src.a06_bud_logic._utils.str_a06 import event_int_str, face_name_str
from src.a18_etl_toolbox.tran_path import (
    create_stances_dir_path,
    create_stances_owner_dir_path,
    create_stance0001_path,
)
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system

LINUX_OS = platform_system() == "Linux"


def test_create_stances_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_dir_path(fisc_mstr_dir="fisc_mstr_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_dir_path) == doc_str


def test_create_stances_owner_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_owner_dir_path(
        fisc_mstr_dir="fisc_mstr_dir", owner_name=owner_name_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_owner_dir_path) == doc_str


def test_create_stance0001_path_HasDocString():
    # ESTABLISH
    doc_str = create_stance0001_path(fisc_mstr_dir="fisc_mstr_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stance0001_path) == doc_str
