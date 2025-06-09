from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_tools.hub_path import create_gut_path, create_vow_json_path
from src.a15_vow_logic.vow import vowunit_shop
from src.a17_idea_logic.idea_csv_tool import (
    add_planunit_to_stance_csv_strs,
    add_vowunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import get_sheet_names
from src.a18_etl_toolbox._test_util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.stance_tool import (
    collect_stance_csv_strs,
    create_stance0001_file,
)
from src.a18_etl_toolbox.tran_path import create_stance0001_path


def test_collect_stance_csv_strs_ReturnsObj_Scenario0_NoVowUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(vow_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario1_SingleVowUnit_NoPlanUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    vow_json_path = create_vow_json_path(vow_mstr_dir, a23_str)
    save_file(vow_json_path, None, a23_vow.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(vow_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_vowunit_to_stance_csv_strs(a23_vow, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_gut_PlanUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    vow_json_path = create_vow_json_path(vow_mstr_dir, a23_str)
    save_file(vow_json_path, None, a23_vow.get_json())
    # create plan gut file
    bob_gut = planunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit("Yao", 44, 55)
    a23_bob_gut_path = create_gut_path(vow_mstr_dir, a23_str, bob_str)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(vow_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_vowunit_to_stance_csv_strs(a23_vow, expected_stance_csv_strs, ",")
    add_planunit_to_stance_csv_strs(bob_gut, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_create_stance0001_file_CreatesFile_Scenario0_NoVowUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    stance0001_path = create_stance0001_path(vow_mstr_dir)
    assert os_path_exists(stance0001_path) is False

    # WHEN
    create_stance0001_file(vow_mstr_dir)

    # THEN
    assert os_path_exists(stance0001_path)
    bob_stance0001_sheetnames = get_sheet_names(stance0001_path)
    stance_csv_strs = create_init_stance_idea_csv_strs()
    assert set(bob_stance0001_sheetnames) == set(stance_csv_strs.keys())
