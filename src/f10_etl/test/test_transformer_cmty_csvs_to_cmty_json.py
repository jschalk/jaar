from src.f00_instrument.file import create_path, save_file, open_file
from src.f01_road.finance_tran import bridge_str
from src.f03_chrono.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
)
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    cmty_title_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_cmty.cmty import cmtyunit_shop, get_from_json as cmtyunit_get_from_json
from src.f07_cmty.cmty_config import cmtyunit_str, current_time_str
from src.f10_etl.transformers import etl_cmty_csvs_to_jsons
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_etl_cmty_csvs_to_jsons_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    cmtyunit_agg_tablename = f"{cmtyunit_str()}_agg"
    cmty_mstr_dir = get_test_etl_dir()
    cmtyunit_csv_filename = f"{cmtyunit_agg_tablename}.csv"
    cmtyunit_csv_str = f"""{cmty_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
    save_file(cmty_mstr_dir, cmtyunit_csv_filename, cmtyunit_csv_str)

    accord23_json_filename = f"{accord23_str}.json"
    accord45_json_filename = f"{accord45_str}.json"
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord23_dir = create_path(cmtys_dir, accord23_str)
    accord45_dir = create_path(cmtys_dir, accord45_str)
    accord23_json_path = create_path(accord23_dir, accord23_json_filename)
    accord45_json_path = create_path(accord45_dir, accord45_json_filename)
    assert os_path_exists(accord23_json_path) is False
    assert os_path_exists(accord45_json_path) is False

    # WHEN
    etl_cmty_csvs_to_jsons(cmty_mstr_dir=cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_cmty = cmtyunit_get_from_json(open_file(accord23_json_path))
    accord45_cmty = cmtyunit_get_from_json(open_file(accord45_json_path))
    assert accord23_cmty == cmtyunit_shop(accord23_str)
    assert accord45_cmty == cmtyunit_shop(accord45_str)
