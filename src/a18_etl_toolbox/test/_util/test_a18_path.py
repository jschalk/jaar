from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.a00_data_toolbox.file_toolbox import create_path
from src.a09_pack_logic.test._util.a09_str import believer_name_str
from src.a18_etl_toolbox.a18_path import (
    STANCE0001_FILENAME,
    create_stance0001_path,
    create_stances_believer_dir_path,
    create_stances_dir_path,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_hub_path_constants_are_values():
    # ESTABLISH / WHEN / THEN
    assert STANCE0001_FILENAME == "stance0001.xlsx"


def test_create_stances_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()

    # WHEN
    gen_bob_stance_dir = create_stances_dir_path(x_belief_mstr_dir)

    # THEN
    expected_stances_dir = create_path(x_belief_mstr_dir, "stances")
    assert gen_bob_stance_dir == expected_stances_dir


def test_create_stances_believer_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_bob_stance_dir = create_stances_believer_dir_path(x_belief_mstr_dir, bob_str)

    # THEN
    stances_dir = create_stances_dir_path(x_belief_mstr_dir)
    expected_bob_stance_dir = create_path(stances_dir, bob_str)
    assert gen_bob_stance_dir == expected_bob_stance_dir


def test_create_stance0001_path_ReturnsObj():
    # ESTABLISH
    output_dir = get_module_temp_dir()

    # WHEN
    gen_stance0001_xlsx_path = create_stance0001_path(output_dir)

    # THEN
    expected_stance000001_path = create_path(output_dir, STANCE0001_FILENAME)
    assert gen_stance0001_xlsx_path == expected_stance000001_path


LINUX_OS = platform_system() == "Linux"


def test_create_stances_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_dir_path(belief_mstr_dir="belief_mstr_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_dir_path) == doc_str


def test_create_stances_believer_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_believer_dir_path(
        belief_mstr_dir="belief_mstr_dir", believer_name=believer_name_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_believer_dir_path) == doc_str


def test_create_stance0001_path_HasDocString():
    # ESTABLISH
    doc_str = create_stance0001_path(output_dir="output_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stance0001_path) == doc_str
