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
    fiscal_title_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_fiscal.fiscal import (
    fiscalunit_shop,
    get_from_json as fiscalunit_get_from_json,
)
from src.f07_fiscal.fiscal_config import (
    get_fiscal_config_args,
    fiscalunit_str,
    fiscal_deal_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    current_time_str,
)
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_WorldUnit_fiscal_csvs_to_jsons_Scenario0_CreateFilesWithOnlyFiscalTitle(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    fizz_world = worldunit_shop("fizz")
    fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
    x_objs = FiscalPrimeObjsRef(fiscal_mstr_dir)
    x_cols = FiscalPrimeColumnsRef()
    fiscalunit_csv_str = f"""{x_cols.unit_agg_csv_header}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
    save_file(fiscal_mstr_dir, x_objs.unit_agg_csv_filename, fiscalunit_csv_str)
    save_file(fiscal_mstr_dir, x_objs.deal_agg_csv_filename, x_cols.deal_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.cash_agg_csv_filename, x_cols.cash_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.hour_agg_csv_filename, x_cols.hour_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.mont_agg_csv_filename, x_cols.mont_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.week_agg_csv_filename, x_cols.week_agg_empty_csv)

    accord23_json_filename = f"{accord23_str}.json"
    accord45_json_filename = f"{accord45_str}.json"
    fiscals_dir = create_path(fizz_world._fiscal_mstr_dir, "fiscals")
    accord23_dir = create_path(fiscals_dir, accord23_str)
    accord45_dir = create_path(fiscals_dir, accord45_str)
    accord23_json_path = create_path(accord23_dir, accord23_json_filename)
    accord45_json_path = create_path(accord45_dir, accord45_json_filename)
    assert os_path_exists(accord23_json_path) is False
    assert os_path_exists(accord45_json_path) is False

    # WHEN
    fizz_world.fiscal_csvs_to_jsons()

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_fiscal = fiscalunit_get_from_json(open_file(accord23_json_path))
    accord45_fiscal = fiscalunit_get_from_json(open_file(accord45_json_path))
    assert accord23_fiscal == fiscalunit_shop(accord23_str)
    assert accord45_fiscal == fiscalunit_shop(accord45_str)


def test_WorldUnit_fiscal_csvs_to_jsons_Scenario1_CreateFilesWithFiscalUnitAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    a45_fund_coin = 3
    a45_penny = 5
    a45_respect_bit = 7
    a45_current_time = 11
    a45_bridge = "/"
    a45_c400_number = 88
    a45_yr1_jan1_offset = 501
    a45_monthday_distortion = 17
    a45_timeline_title = "a45_timeline"
    fizz_world = worldunit_shop("fizz")
    fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
    x_objs = FiscalPrimeObjsRef(fiscal_mstr_dir)
    x_cols = FiscalPrimeColumnsRef()
    fiscalunit_csv_str = f"""{x_cols.unit_agg_csv_header}
{accord23_str},,,,,,,,,
{accord45_str},{a45_fund_coin},{a45_penny},{a45_respect_bit},{a45_current_time},{a45_bridge},{a45_c400_number},{a45_yr1_jan1_offset},{a45_monthday_distortion},{a45_timeline_title}
"""
    fizz_world = worldunit_shop("fizz")
    save_file(fiscal_mstr_dir, x_objs.unit_agg_csv_filename, fiscalunit_csv_str)
    save_file(fiscal_mstr_dir, x_objs.deal_agg_csv_filename, x_cols.deal_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.cash_agg_csv_filename, x_cols.cash_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.hour_agg_csv_filename, x_cols.hour_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.mont_agg_csv_filename, x_cols.mont_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_objs.week_agg_csv_filename, x_cols.week_agg_empty_csv)

    accord23_json_filename = f"{accord23_str}.json"
    accord45_json_filename = f"{accord45_str}.json"
    fiscals_dir = create_path(fizz_world._fiscal_mstr_dir, "fiscals")
    accord23_dir = create_path(fiscals_dir, accord23_str)
    accord45_dir = create_path(fiscals_dir, accord45_str)
    accord23_json_path = create_path(accord23_dir, accord23_json_filename)
    accord45_json_path = create_path(accord45_dir, accord45_json_filename)
    assert os_path_exists(accord23_json_path) is False
    assert os_path_exists(accord45_json_path) is False

    # WHEN
    fizz_world.fiscal_csvs_to_jsons()

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_fiscal = fiscalunit_get_from_json(open_file(accord23_json_path))
    accord45_fiscal = fiscalunit_get_from_json(open_file(accord45_json_path))
    assert accord23_fiscal == fiscalunit_shop(accord23_str)
    expected_45_tl = timelineunit_shop(
        timeline_config_shop(
            timeline_title=a45_timeline_title,
            c400_number=a45_c400_number,
            yr1_jan1_offset=a45_yr1_jan1_offset,
            monthday_distortion=a45_monthday_distortion,
        )
    )
    accord_45_timeline = accord45_fiscal.timeline
    assert accord_45_timeline.c400_number == expected_45_tl.c400_number
    assert accord_45_timeline.monthday_distortion == expected_45_tl.monthday_distortion
    assert accord_45_timeline.timeline_title == expected_45_tl.timeline_title
    assert accord_45_timeline.yr1_jan1_offset == expected_45_tl.yr1_jan1_offset
    assert accord_45_timeline == expected_45_tl
    assert accord45_fiscal == fiscalunit_shop(
        fiscal_title=accord45_str,
        fund_coin=a45_fund_coin,
        penny=a45_penny,
        respect_bit=a45_respect_bit,
        current_time=a45_current_time,
        bridge=a45_bridge,
        timeline=expected_45_tl,
    )
