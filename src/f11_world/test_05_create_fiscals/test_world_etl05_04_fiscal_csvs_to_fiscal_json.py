from src.f00_instrument.file import create_path, save_file, open_file
from src.f03_chrono.chrono import timelineunit_shop, timeline_config_shop
from src.f05_listen.hub_paths import create_fiscal_json_path
from src.f07_fiscal.fiscal import (
    fiscalunit_shop,
    get_from_json as fiscalunit_get_from_json,
)
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_fiscal_csvs_to_jsons_Scenario0_CreateFilesWithOnlyFiscalTitle(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    fizz_world = worldunit_shop("fizz")
    fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
    x_fis = FiscalPrimeObjsRef(fiscal_mstr_dir)
    x_cols = FiscalPrimeColumnsRef()
    fiscalunit_csv_str = f"""{x_cols.unit_agg_csv_header}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
    save_file(fiscal_mstr_dir, x_fis.unit_agg_csv_filename, fiscalunit_csv_str)
    save_file(fiscal_mstr_dir, x_fis.deal_agg_csv_filename, x_cols.deal_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.cash_agg_csv_filename, x_cols.cash_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.hour_agg_csv_filename, x_cols.hour_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.mont_agg_csv_filename, x_cols.mont_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.week_agg_csv_filename, x_cols.week_agg_empty_csv)

    # accord23_json_filename = f"{accord23_str}.json"
    # accord45_json_filename = f"{accord45_str}.json"
    fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
    accord23_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord23_str)
    accord45_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord45_str)
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
    a45_present_time = 11
    a45_bridge = "/"
    a45_c400_number = 88
    a45_yr1_jan1_offset = 501
    a45_monthday_distortion = 17
    a45_timeline_title = "a45_timeline"
    fizz_world = worldunit_shop("fizz")
    fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
    x_fis = FiscalPrimeObjsRef(fiscal_mstr_dir)
    x_cols = FiscalPrimeColumnsRef()
    fiscalunit_csv_str = f"""{x_cols.unit_agg_csv_header}
{accord23_str},,,,,,,,,
{accord45_str},{a45_fund_coin},{a45_penny},{a45_respect_bit},{a45_present_time},{a45_bridge},{a45_c400_number},{a45_yr1_jan1_offset},{a45_monthday_distortion},{a45_timeline_title}
"""
    fizz_world = worldunit_shop("fizz")
    save_file(fiscal_mstr_dir, x_fis.unit_agg_csv_filename, fiscalunit_csv_str)
    save_file(fiscal_mstr_dir, x_fis.deal_agg_csv_filename, x_cols.deal_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.cash_agg_csv_filename, x_cols.cash_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.hour_agg_csv_filename, x_cols.hour_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.mont_agg_csv_filename, x_cols.mont_agg_empty_csv)
    save_file(fiscal_mstr_dir, x_fis.week_agg_csv_filename, x_cols.week_agg_empty_csv)

    fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
    accord23_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord23_str)
    accord45_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord45_str)
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
        present_time=a45_present_time,
        bridge=a45_bridge,
        timeline=expected_45_tl,
    )
