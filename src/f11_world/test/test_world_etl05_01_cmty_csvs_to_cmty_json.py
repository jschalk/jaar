from src.f00_instrument.file import create_path, save_file, open_file
from src.f01_road.finance_tran import bridge_str
from src.f03_chrono.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
    timelineunit_shop,
    timeline_config_shop,
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
from src.f07_cmty.cmty_config import (
    get_cmty_config_args,
    cmtyunit_str,
    cmty_deal_episode_str,
    cmty_cashbook_str,
    cmty_timeline_hour_str,
    cmty_timeline_month_str,
    cmty_timeline_weekday_str,
    current_time_str,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_WorldUnit_cmty_csvs_to_jsons_Scenario0_CreateFilesWithOnlyCmtyTitle(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    cmtyunit_agg_tablename = f"{cmtyunit_str()}_agg"
    cmtyunit_csv_filename = f"{cmtyunit_agg_tablename}.csv"
    cmtyunit_csv_str = f"""{cmty_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
    fizz_world = worldunit_shop("Fizz")
    save_file(fizz_world._cmty_mstr_dir, cmtyunit_csv_filename, cmtyunit_csv_str)

    accord23_json_filename = f"{accord23_str}.json"
    accord45_json_filename = f"{accord45_str}.json"
    cmtys_dir = create_path(fizz_world._cmty_mstr_dir, "cmtys")
    accord23_dir = create_path(cmtys_dir, accord23_str)
    accord45_dir = create_path(cmtys_dir, accord45_str)
    accord23_json_path = create_path(accord23_dir, accord23_json_filename)
    accord45_json_path = create_path(accord45_dir, accord45_json_filename)
    assert os_path_exists(accord23_json_path) is False
    assert os_path_exists(accord45_json_path) is False

    # WHEN
    fizz_world.cmty_csvs_to_jsons()

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_cmty = cmtyunit_get_from_json(open_file(accord23_json_path))
    accord45_cmty = cmtyunit_get_from_json(open_file(accord45_json_path))
    assert accord23_cmty == cmtyunit_shop(accord23_str)
    assert accord45_cmty == cmtyunit_shop(accord45_str)


def test_WorldUnit_cmty_csvs_to_jsons_Scenario1_CreateFilesWithCmtyUnitAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    cmtyunit_agg_tablename = f"{cmtyunit_str()}_agg"
    cmtyunit_csv_filename = f"{cmtyunit_agg_tablename}.csv"
    a45_fund_coin = 3
    a45_penny = 5
    a45_respect_bit = 7
    a45_current_time = 11
    a45_bridge = "/"
    a45_c400_number = 88
    a45_yr1_jan1_offset = 501
    a45_monthday_distortion = 17
    a45_timeline_title = "a45_timeline"
    cmtyunit_csv_str = f"""{cmty_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},{a45_fund_coin},{a45_penny},{a45_respect_bit},{a45_current_time},{a45_bridge},{a45_c400_number},{a45_yr1_jan1_offset},{a45_monthday_distortion},{a45_timeline_title}
"""
    fizz_world = worldunit_shop("Fizz")
    save_file(fizz_world._cmty_mstr_dir, cmtyunit_csv_filename, cmtyunit_csv_str)

    accord23_json_filename = f"{accord23_str}.json"
    accord45_json_filename = f"{accord45_str}.json"
    cmtys_dir = create_path(fizz_world._cmty_mstr_dir, "cmtys")
    accord23_dir = create_path(cmtys_dir, accord23_str)
    accord45_dir = create_path(cmtys_dir, accord45_str)
    accord23_json_path = create_path(accord23_dir, accord23_json_filename)
    accord45_json_path = create_path(accord45_dir, accord45_json_filename)
    assert os_path_exists(accord23_json_path) is False
    assert os_path_exists(accord45_json_path) is False

    # WHEN
    fizz_world.cmty_csvs_to_jsons()

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_cmty = cmtyunit_get_from_json(open_file(accord23_json_path))
    accord45_cmty = cmtyunit_get_from_json(open_file(accord45_json_path))
    assert accord23_cmty == cmtyunit_shop(accord23_str)
    expected_45_tl = timelineunit_shop(
        timeline_config_shop(
            timeline_title=a45_timeline_title,
            c400_number=a45_c400_number,
            yr1_jan1_offset=a45_yr1_jan1_offset,
            monthday_distortion=a45_monthday_distortion,
        )
    )
    accord_45_timeline = accord45_cmty.timeline
    assert accord_45_timeline.c400_number == expected_45_tl.c400_number
    assert accord_45_timeline.monthday_distortion == expected_45_tl.monthday_distortion
    assert accord_45_timeline.timeline_title == expected_45_tl.timeline_title
    assert accord_45_timeline.yr1_jan1_offset == expected_45_tl.yr1_jan1_offset
    assert accord_45_timeline == expected_45_tl
    assert accord45_cmty == cmtyunit_shop(
        cmty_title=accord45_str,
        fund_coin=a45_fund_coin,
        penny=a45_penny,
        respect_bit=a45_respect_bit,
        current_time=a45_current_time,
        bridge=a45_bridge,
        timeline=expected_45_tl,
    )
