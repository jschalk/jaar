from src.a00_data_toolboxs.file_toolbox import create_path, save_file, open_file
from src.a02_finance_toolboxs.deal import bridge_str, owner_name_str, fisc_title_str
from src.a06_bud_logic.bud import budunit_shop
from src.a07_calendar_logic.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
    timeline_config_shop,
    timelineunit_shop,
)
from src.a08_bud_atom_logic.atom_config import (
    acct_name_str,
    face_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.a12_hub_tools.hub_path import create_fisc_json_path, create_gut_path
from src.a15_fisc_logic.fisc import (
    fiscunit_shop,
    get_from_json as fiscunit_get_from_json,
)
from src.a15_fisc_logic.fisc_config import fiscunit_str
from src.f10_idea.idea_db_tool import get_sheet_names
from src.f10_idea.idea_csv_tool import (
    create_init_stance_idea_brick_csv_strs,
    add_budunit_to_stance_csv_strs,
    add_fiscunit_to_stance_csv_strs,
    add_pidginunit_to_stance_csv_strs,
)
from src.f11_etl.tran_path import create_stances_owner_dir_path, create_stance0001_path
from src.f11_etl.stance_tool import collect_stance_csv_strs, create_stance0001_file
from src.f11_etl.transformers import etl_fisc_agg_tables_to_fisc_jsons
from src.f11_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_collect_stance_csv_strs_ReturnsObj_Scenario0_NoFiscUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_etl_dir()
    bob_str = "Bob"

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(fisc_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_brick_csv_strs()
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario1_SingleFiscUnit_NoBudUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_etl_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, a23_fisc.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(fisc_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_brick_csv_strs()
    add_fiscunit_to_stance_csv_strs(a23_fisc, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_gut_BudUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_etl_dir()
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
    expected_stance_csv_strs = create_init_stance_idea_brick_csv_strs()
    add_fiscunit_to_stance_csv_strs(a23_fisc, expected_stance_csv_strs, ",")
    add_budunit_to_stance_csv_strs(bob_gut, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_create_stance0001_file_CreatesFile_Scenario0_NoFiscUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_etl_dir()
    stance0001_path = create_stance0001_path(fisc_mstr_dir)
    assert os_path_exists(stance0001_path) is False

    # WHEN
    create_stance0001_file(fisc_mstr_dir)

    # THEN
    assert os_path_exists(stance0001_path)
    bob_stance0001_sheetnames = get_sheet_names(stance0001_path)
    stance_csv_strs = create_init_stance_idea_brick_csv_strs()
    assert set(bob_stance0001_sheetnames) == set(stance_csv_strs.keys())
