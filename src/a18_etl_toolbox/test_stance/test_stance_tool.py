from src.a00_data_toolbox.file_toolbox import create_path, save_file, open_file
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import create_fisc_json_path, create_gut_path
from src.a15_fisc_logic.fisc import fiscunit_shop
from src.a17_idea_logic.idea_db_tool import get_sheet_names
from src.a17_idea_logic.idea_csv_tool import (
    create_init_stance_idea_csv_strs,
    add_budunit_to_stance_csv_strs,
    add_fiscunit_to_stance_csv_strs,
)
from src.a18_etl_toolbox.tran_path import create_stance0001_path
from src.a18_etl_toolbox.stance_tool import (
    collect_stance_csv_strs,
    create_stance0001_file,
)
from src.a18_etl_toolbox._test_util.a18_env import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_collect_stance_csv_strs_ReturnsObj_Scenario0_NoFiscUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(fisc_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario1_SingleFiscUnit_NoBudUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, a23_fisc.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(fisc_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_fiscunit_to_stance_csv_strs(a23_fisc, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_gut_BudUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, a23_fisc.get_json())
    # create bud gut file
    bob_gut = budunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit("Yao", 44, 55)
    a23_bob_gut_path = create_gut_path(fisc_mstr_dir, a23_str, bob_str)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(fisc_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_fiscunit_to_stance_csv_strs(a23_fisc, expected_stance_csv_strs, ",")
    add_budunit_to_stance_csv_strs(bob_gut, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_create_stance0001_file_CreatesFile_Scenario0_NoFiscUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    stance0001_path = create_stance0001_path(fisc_mstr_dir)
    assert os_path_exists(stance0001_path) is False

    # WHEN
    create_stance0001_file(fisc_mstr_dir)

    # THEN
    assert os_path_exists(stance0001_path)
    bob_stance0001_sheetnames = get_sheet_names(stance0001_path)
    stance_csv_strs = create_init_stance_idea_csv_strs()
    assert set(bob_stance0001_sheetnames) == set(stance_csv_strs.keys())
