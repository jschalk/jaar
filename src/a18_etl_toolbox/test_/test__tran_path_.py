from src.a00_data_toolbox.file_toolbox import create_path
from src.a18_etl_toolbox._util.a18_env import env_dir_setup_cleanup, get_module_temp_dir
from src.a18_etl_toolbox.tran_path import (
    STANCE0001_FILENAME,
    create_stance0001_path,
    create_stances_dir_path,
    create_stances_owner_dir_path,
)


def test_hub_path_constants_are_values():
    # ESTABLISH / WHEN / THEN
    assert STANCE0001_FILENAME == "stance0001.xlsx"


def test_create_stances_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()

    # WHEN
    gen_bob_stance_dir = create_stances_dir_path(x_vow_mstr_dir)

    # THEN
    expected_stances_dir = create_path(x_vow_mstr_dir, "stances")
    assert gen_bob_stance_dir == expected_stances_dir


def test_create_stances_owner_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_bob_stance_dir = create_stances_owner_dir_path(x_vow_mstr_dir, bob_str)

    # THEN
    stances_dir = create_path(x_vow_mstr_dir, "stances")
    expected_bob_stance_dir = create_path(stances_dir, bob_str)
    assert gen_bob_stance_dir == expected_bob_stance_dir


def test_create_stance0001_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()

    # WHEN
    gen_stance0001_xlsx_path = create_stance0001_path(x_vow_mstr_dir)

    # THEN
    stances_dir = create_path(x_vow_mstr_dir, "stances")
    expected_stance000001_path = create_path(stances_dir, STANCE0001_FILENAME)
    assert gen_stance0001_xlsx_path == expected_stance000001_path
