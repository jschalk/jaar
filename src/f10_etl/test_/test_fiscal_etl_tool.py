from src.f00_instrument.file import create_path, open_file, set_dir
from src.f03_chrono.chrono import timelineunit_shop, timeline_config_shop
from src.f04_gift.atom_config import (
    face_name_str,
    fiscal_title_str,
    acct_name_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f05_listen.hub_tool import create_fiscal_json_path
from src.f07_fiscal.fiscal import get_from_json as fiscal_get_from_json, fiscalunit_shop
from src.f07_fiscal.fiscal_config import (
    fiscalunit_str,
    fiscal_cashbook_str,
    fiscal_deal_episode_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    get_fiscal_config_args,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_db_tool import sheet_exists, upsert_sheet, get_custom_sorted_list
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
    create_init_fiscal_prime_files,
    create_fiscalunit_jsons_from_prime_files,
    get_fiscalunit_sorted_args,
    get_fiscaldeal_sorted_args,
    get_fiscalcash_sorted_args,
    get_fiscalhour_sorted_args,
    get_fiscalmont_sorted_args,
    get_fiscalweek_sorted_args,
    collect_events_dir_owner_events_sets,
    get_owners_downhill_event_ints,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


# br00000 fiscal_title c400_number,present_time,fund_coin,monthday_distortion,penny,respect_bit,bridge,timeline_title,yr1_jan1_offset
# br00001 fiscal_title owner_name,acct_name,time_int,quota
# br00002 fiscal_title owner_name,acct_name,time_int,amount
# br00003 fiscal_title hour_title,cumlative_minute
# br00004 fiscal_title month_title,cumlative_day
# br00005 fiscal_title weekday_title,weekday_order


def test_get_fiscalunit_sorted_args_ReturnsObj():
    # ESTABLISH / WHEN
    unit_sorted_args = get_fiscalunit_sorted_args()
    # THEN
    expected_unit_args = set(get_fiscal_config_args(fiscalunit_str()).keys())
    # expected_unit_args.add(face_name_str())
    # expected_unit_args.add(event_int_str())
    expected_unit_sorted_args = get_custom_sorted_list(expected_unit_args)
    print(f"{expected_unit_sorted_args=}")
    assert unit_sorted_args == expected_unit_sorted_args


def test_get_fiscaldeal_sorted_args_ReturnsObj():
    # ESTABLISH / WHEN
    deal_sorted_args = get_fiscaldeal_sorted_args()
    # THEN
    expected_deal_args = set(get_fiscal_config_args(fiscal_deal_episode_str()).keys())
    # expected_deal_args.add(face_name_str())
    # expected_deal_args.add(event_int_str())
    expected_deal_sorted_args = get_custom_sorted_list(expected_deal_args)
    print(f"{expected_deal_sorted_args=}")
    assert deal_sorted_args == expected_deal_sorted_args


def test_get_fiscalcash_sorted_args_ReturnsObj():
    # ESTABLISH / WHEN
    cash_sorted_args = get_fiscalcash_sorted_args()
    # THEN
    expected_cash_args = set(get_fiscal_config_args(fiscal_cashbook_str()).keys())
    # expected_cash_args.add(face_name_str())
    # expected_cash_args.add(event_int_str())
    expected_cash_sorted_args = get_custom_sorted_list(expected_cash_args)
    print(f"{expected_cash_sorted_args=}")
    assert cash_sorted_args == expected_cash_sorted_args


def test_get_fiscalhour_sorted_args_ReturnsObj():
    # ESTABLISH / WHEN
    hour_sorted_args = get_fiscalhour_sorted_args()
    # THEN
    expected_hour_args = set(get_fiscal_config_args(fiscal_timeline_hour_str()).keys())
    # expected_hour_args.add(face_name_str())
    # expected_hour_args.add(event_int_str())
    expected_hour_sorted_args = get_custom_sorted_list(expected_hour_args)
    print(f"{expected_hour_sorted_args=}")
    assert hour_sorted_args == expected_hour_sorted_args


def test_get_fiscalmont_sorted_args_ReturnsObj():
    # ESTABLISH / WHEN
    mont_sorted_args = get_fiscalmont_sorted_args()
    # THEN
    expected_mont_args = set(get_fiscal_config_args(fiscal_timeline_month_str()).keys())
    # expected_mont_args.add(face_name_str())
    # expected_mont_args.add(event_int_str())
    expected_mont_sorted_args = get_custom_sorted_list(expected_mont_args)
    print(f"{expected_mont_sorted_args=}")
    assert mont_sorted_args == expected_mont_sorted_args


def test_get_fiscalweek_sorted_args_ReturnsObj():
    # ESTABLISH / WHEN
    week_sorted_args = get_fiscalweek_sorted_args()
    # THEN
    expected_week_args = set(
        get_fiscal_config_args(fiscal_timeline_weekday_str()).keys()
    )
    # expected_week_args.add(face_name_str())
    # expected_week_args.add(event_int_str())
    expected_week_sorted_args = get_custom_sorted_list(expected_week_args)
    print(f"{expected_week_sorted_args=}")
    assert week_sorted_args == expected_week_sorted_args


def test_FiscalPrimeObjsRef_Exists():
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    xp = FiscalPrimeObjsRef(x_dir)

    # THEN
    assert xp
    agg_str = "_agg"
    assert xp.unit_agg_tablename == f"{fiscalunit_str()}{agg_str}"
    assert xp.deal_agg_tablename == f"{fiscal_deal_episode_str()}{agg_str}"
    assert xp.cash_agg_tablename == f"{fiscal_cashbook_str()}{agg_str}"
    assert xp.hour_agg_tablename == f"{fiscal_timeline_hour_str()}{agg_str}"
    assert xp.mont_agg_tablename == f"{fiscal_timeline_month_str()}{agg_str}"
    assert xp.week_agg_tablename == f"{fiscal_timeline_weekday_str()}{agg_str}"
    staging_str = "_staging"
    assert xp.unit_stage_tablename == f"{fiscalunit_str()}{staging_str}"
    assert xp.deal_stage_tablename == f"{fiscal_deal_episode_str()}{staging_str}"
    assert xp.cash_stage_tablename == f"{fiscal_cashbook_str()}{staging_str}"
    assert xp.hour_stage_tablename == f"{fiscal_timeline_hour_str()}{staging_str}"
    assert xp.mont_stage_tablename == f"{fiscal_timeline_month_str()}{staging_str}"
    assert xp.week_stage_tablename == f"{fiscal_timeline_weekday_str()}{staging_str}"
    assert xp.unit_agg_csv_filename == f"{xp.unit_agg_tablename}.csv"
    assert xp.deal_agg_csv_filename == f"{xp.deal_agg_tablename}.csv"
    assert xp.cash_agg_csv_filename == f"{xp.cash_agg_tablename}.csv"
    assert xp.hour_agg_csv_filename == f"{xp.hour_agg_tablename}.csv"
    assert xp.mont_agg_csv_filename == f"{xp.mont_agg_tablename}.csv"
    assert xp.week_agg_csv_filename == f"{xp.week_agg_tablename}.csv"
    assert xp.unit_stage_csv_filename == f"{xp.unit_stage_tablename}.csv"
    assert xp.deal_stage_csv_filename == f"{xp.deal_stage_tablename}.csv"
    assert xp.cash_stage_csv_filename == f"{xp.cash_stage_tablename}.csv"
    assert xp.hour_stage_csv_filename == f"{xp.hour_stage_tablename}.csv"
    assert xp.mont_stage_csv_filename == f"{xp.mont_stage_tablename}.csv"
    assert xp.week_stage_csv_filename == f"{xp.week_stage_tablename}.csv"
    assert xp.unit_agg_csv_path == create_path(x_dir, xp.unit_agg_csv_filename)
    assert xp.deal_agg_csv_path == create_path(x_dir, xp.deal_agg_csv_filename)
    assert xp.cash_agg_csv_path == create_path(x_dir, xp.cash_agg_csv_filename)
    assert xp.hour_agg_csv_path == create_path(x_dir, xp.hour_agg_csv_filename)
    assert xp.mont_agg_csv_path == create_path(x_dir, xp.mont_agg_csv_filename)
    assert xp.week_agg_csv_path == create_path(x_dir, xp.week_agg_csv_filename)
    assert xp.unit_stage_csv_path == create_path(x_dir, xp.unit_stage_csv_filename)
    assert xp.deal_stage_csv_path == create_path(x_dir, xp.deal_stage_csv_filename)
    assert xp.cash_stage_csv_path == create_path(x_dir, xp.cash_stage_csv_filename)
    assert xp.hour_stage_csv_path == create_path(x_dir, xp.hour_stage_csv_filename)
    assert xp.mont_stage_csv_path == create_path(x_dir, xp.mont_stage_csv_filename)
    assert xp.week_stage_csv_path == create_path(x_dir, xp.week_stage_csv_filename)
    assert xp.unit_excel_filename == f"{fiscalunit_str()}.xlsx"
    assert xp.deal_excel_filename == f"{fiscal_deal_episode_str()}.xlsx"
    assert xp.cash_excel_filename == f"{fiscal_cashbook_str()}.xlsx"
    assert xp.hour_excel_filename == f"{fiscal_timeline_hour_str()}.xlsx"
    assert xp.mont_excel_filename == f"{fiscal_timeline_month_str()}.xlsx"
    assert xp.week_excel_filename == f"{fiscal_timeline_weekday_str()}.xlsx"
    assert xp.unit_excel_path == create_path(x_dir, xp.unit_excel_filename)
    assert xp.deal_excel_path == create_path(x_dir, xp.deal_excel_filename)
    assert xp.cash_excel_path == create_path(x_dir, xp.cash_excel_filename)
    assert xp.hour_excel_path == create_path(x_dir, xp.hour_excel_filename)
    assert xp.mont_excel_path == create_path(x_dir, xp.mont_excel_filename)
    assert xp.week_excel_path == create_path(x_dir, xp.week_excel_filename)


def test_FiscalPrimeColumnsRef_Exists():
    # ESTABLISH / WHEN
    fis_cols = FiscalPrimeColumnsRef()

    # THEN
    unit_args = set(get_fiscal_config_args(fiscalunit_str()).keys())
    cash_args = set(get_fiscal_config_args(fiscal_cashbook_str()).keys())
    deal_args = set(get_fiscal_config_args(fiscal_deal_episode_str()).keys())
    hour_args = set(get_fiscal_config_args(fiscal_timeline_hour_str()).keys())
    mont_args = set(get_fiscal_config_args(fiscal_timeline_month_str()).keys())
    week_args = set(get_fiscal_config_args(fiscal_timeline_weekday_str()).keys())
    print(f"           {fis_cols.unit_agg_columns=}")
    print(f"{get_custom_sorted_list(list(unit_args))=}")
    assert fis_cols.unit_agg_columns == get_custom_sorted_list(unit_args)
    assert fis_cols.cash_agg_columns == get_custom_sorted_list(cash_args)
    assert fis_cols.deal_agg_columns == get_custom_sorted_list(deal_args)
    assert fis_cols.hour_agg_columns == get_custom_sorted_list(hour_args)
    assert fis_cols.mont_agg_columns == get_custom_sorted_list(mont_args)
    assert fis_cols.week_agg_columns == get_custom_sorted_list(week_args)

    staging_args = {"idea_number", face_name_str(), event_int_str(), "error_message"}
    unit_staging_args = unit_args.union(staging_args)
    cash_staging_args = cash_args.union(staging_args)
    deal_staging_args = deal_args.union(staging_args)
    hour_staging_args = hour_args.union(staging_args)
    mont_staging_args = mont_args.union(staging_args)
    week_staging_args = week_args.union(staging_args)
    assert fis_cols.unit_staging_columns == get_custom_sorted_list(unit_staging_args)
    assert fis_cols.cash_staging_columns == get_custom_sorted_list(cash_staging_args)
    assert fis_cols.deal_staging_columns == get_custom_sorted_list(deal_staging_args)
    assert fis_cols.hour_staging_columns == get_custom_sorted_list(hour_staging_args)
    assert fis_cols.mont_staging_columns == get_custom_sorted_list(mont_staging_args)
    assert fis_cols.week_staging_columns == get_custom_sorted_list(week_staging_args)

    # unit_staging_csv_header = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}"""
    unit_staging_csv_header = ",".join(fis_cols.unit_staging_columns)
    deal_staging_csv_header = ",".join(fis_cols.deal_staging_columns)
    cash_staging_csv_header = ",".join(fis_cols.cash_staging_columns)
    hour_staging_csv_header = ",".join(fis_cols.hour_staging_columns)
    mont_staging_csv_header = ",".join(fis_cols.mont_staging_columns)
    week_staging_csv_header = ",".join(fis_cols.week_staging_columns)

    assert fis_cols.unit_staging_csv_header == unit_staging_csv_header
    assert fis_cols.deal_staging_csv_header == deal_staging_csv_header
    assert fis_cols.cash_staging_csv_header == cash_staging_csv_header
    assert fis_cols.hour_staging_csv_header == hour_staging_csv_header
    assert fis_cols.mont_staging_csv_header == mont_staging_csv_header
    assert fis_cols.week_staging_csv_header == week_staging_csv_header
    unit_agg_csv_header = ",".join(fis_cols.unit_agg_columns)
    deal_agg_csv_header = ",".join(fis_cols.deal_agg_columns)
    cash_agg_csv_header = ",".join(fis_cols.cash_agg_columns)
    hour_agg_csv_header = ",".join(fis_cols.hour_agg_columns)
    mont_agg_csv_header = ",".join(fis_cols.mont_agg_columns)
    week_agg_csv_header = ",".join(fis_cols.week_agg_columns)

    assert fis_cols.unit_agg_csv_header == unit_agg_csv_header
    assert fis_cols.deal_agg_csv_header == deal_agg_csv_header
    assert fis_cols.cash_agg_csv_header == cash_agg_csv_header
    assert fis_cols.hour_agg_csv_header == hour_agg_csv_header
    assert fis_cols.mont_agg_csv_header == mont_agg_csv_header
    assert fis_cols.week_agg_csv_header == week_agg_csv_header
    assert fis_cols.unit_agg_empty_csv == f"{unit_agg_csv_header}\n"
    assert fis_cols.deal_agg_empty_csv == f"{deal_agg_csv_header}\n"
    assert fis_cols.cash_agg_empty_csv == f"{cash_agg_csv_header}\n"
    assert fis_cols.hour_agg_empty_csv == f"{hour_agg_csv_header}\n"
    assert fis_cols.mont_agg_empty_csv == f"{mont_agg_csv_header}\n"
    assert fis_cols.week_agg_empty_csv == f"{week_agg_csv_header}\n"


def test_create_init_fiscal_prime_files_CreatesFiles_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    staging_str = "staging"
    fiscalref = FiscalPrimeObjsRef(x_dir)
    assert sheet_exists(fiscalref.unit_excel_path, staging_str) is False
    assert sheet_exists(fiscalref.deal_excel_path, staging_str) is False
    assert sheet_exists(fiscalref.cash_excel_path, staging_str) is False
    assert sheet_exists(fiscalref.hour_excel_path, staging_str) is False
    assert sheet_exists(fiscalref.mont_excel_path, staging_str) is False
    assert sheet_exists(fiscalref.week_excel_path, staging_str) is False

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    assert sheet_exists(fiscalref.unit_excel_path, staging_str)
    assert sheet_exists(fiscalref.deal_excel_path, staging_str)
    assert sheet_exists(fiscalref.cash_excel_path, staging_str)
    assert sheet_exists(fiscalref.hour_excel_path, staging_str)
    assert sheet_exists(fiscalref.mont_excel_path, staging_str)
    assert sheet_exists(fiscalref.week_excel_path, staging_str)


def test_create_init_fiscal_prime_files_HasCorrectColumns_staging(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    staging_str = "staging"
    xp = FiscalPrimeObjsRef(x_dir)
    fiscalunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=staging_str)
    fiscaldeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=staging_str)
    fiscalcash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=staging_str)
    fiscalhour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=staging_str)
    fiscalmont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=staging_str)
    fiscalweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=staging_str)

    expected_cols = FiscalPrimeColumnsRef()
    print(f"{list(fiscalunit_df.columns)=}")
    assert list(fiscalunit_df.columns) == expected_cols.unit_staging_columns
    assert list(fiscaldeal_df.columns) == expected_cols.deal_staging_columns
    assert list(fiscalcash_df.columns) == expected_cols.cash_staging_columns
    assert list(fiscalhour_df.columns) == expected_cols.hour_staging_columns
    assert list(fiscalmont_df.columns) == expected_cols.mont_staging_columns
    assert list(fiscalweek_df.columns) == expected_cols.week_staging_columns


def test_create_init_fiscal_prime_files_CreatesFiles_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    agg_str = "agg"
    xp = FiscalPrimeObjsRef(x_dir)
    assert sheet_exists(xp.unit_excel_path, agg_str) is False
    assert sheet_exists(xp.deal_excel_path, agg_str) is False
    assert sheet_exists(xp.cash_excel_path, agg_str) is False
    assert sheet_exists(xp.hour_excel_path, agg_str) is False
    assert sheet_exists(xp.mont_excel_path, agg_str) is False
    assert sheet_exists(xp.week_excel_path, agg_str) is False

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.unit_excel_path, agg_str)
    assert sheet_exists(xp.deal_excel_path, agg_str)
    assert sheet_exists(xp.cash_excel_path, agg_str)
    assert sheet_exists(xp.hour_excel_path, agg_str)
    assert sheet_exists(xp.mont_excel_path, agg_str)
    assert sheet_exists(xp.week_excel_path, agg_str)


def test_create_init_fiscal_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    agg_str = "agg"
    xp = FiscalPrimeObjsRef(x_dir)
    fiscalunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=agg_str)
    fiscaldeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=agg_str)
    fiscalcash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=agg_str)
    fiscalhour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=agg_str)
    fiscalmont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=agg_str)
    fiscalweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=agg_str)

    expected_cols = FiscalPrimeColumnsRef()
    print(f"{list(fiscalunit_df.columns)=}")
    assert list(fiscalunit_df.columns) == expected_cols.unit_agg_columns
    assert list(fiscaldeal_df.columns) == expected_cols.deal_agg_columns
    assert list(fiscalcash_df.columns) == expected_cols.cash_agg_columns
    assert list(fiscalhour_df.columns) == expected_cols.hour_agg_columns
    assert list(fiscalmont_df.columns) == expected_cols.mont_agg_columns
    assert list(fiscalweek_df.columns) == expected_cols.week_agg_columns


def test_create_fiscalunit_jsons_from_prime_files_Scenario0_MinimumNecessaryParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_row = [
        accord56_str,
        "",  # accord56_c400_number_str,
        "",  # accord56_present_time_str,
        "",  # accord56_fund_coin_str,
        "",  # accord56_monthday_distortion_str,
        "",  # accord56_penny_str,
        "",  # accord56_respect_bit_str,
        "",  # accord56_bridge_str,
        "",  # accord56_timeline_title_str,
        "",  # accord56_yr1_jan1_offset_str,
    ]
    fiscalunit_rows = [accord56_row]
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.unit_agg_columns)
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    accord56_fiscalunit.fiscals_dir = fiscal_mstr_dir
    accord56_fiscalunit._set_fiscal_dirs()
    assert accord56_fiscalunit
    assert accord56_fiscalunit.fiscal_title == accord56_str
    assert accord56_fiscalunit.fiscals_dir == fiscal_mstr_dir
    expected_fiscalunit = fiscalunit_shop(accord56_str, fiscal_mstr_dir)
    assert accord56_fiscalunit.timeline == expected_fiscalunit.timeline
    assert accord56_fiscalunit == expected_fiscalunit


def test_create_fiscalunit_jsons_from_prime_files_Scenario1_IncludeNoneTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_present_time = 77
    accord56_fund_coin = 3
    accord56_penny = 2
    accord56_respect_bit = 55
    accord56_bridge = "/"
    accord56 = [
        accord56_str,
        accord56_fund_coin,
        accord56_penny,
        accord56_respect_bit,
        accord56_present_time,
        accord56_bridge,
        "",  # accord56_c400_number_str,
        "",  # accord56_yr1_jan1_offset_str,
        "",  # accord56_monthday_distortion_str,
        "",  # accord56_timeline_title_str,
    ]
    print(f"{xc.unit_agg_columns=}")
    fiscalunit_rows = [accord56]
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.unit_agg_columns)
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    assert accord56_fiscalunit
    assert accord56_fiscalunit.fiscal_title == accord56_str
    assert accord56_fiscalunit.present_time == accord56_present_time
    assert accord56_fiscalunit.fund_coin == accord56_fund_coin
    assert accord56_fiscalunit.penny == accord56_penny
    assert accord56_fiscalunit.respect_bit == accord56_respect_bit
    assert accord56_fiscalunit.bridge == accord56_bridge
    default_fiscalunit = fiscalunit_shop(accord56_str)
    assert accord56_fiscalunit.timeline == default_fiscalunit.timeline
    assert accord56_fiscalunit.fiscal_title == accord56_str
    assert accord56_fiscalunit.present_time != default_fiscalunit.present_time
    assert accord56_fiscalunit.fund_coin != default_fiscalunit.fund_coin
    assert accord56_fiscalunit.penny != default_fiscalunit.penny
    assert accord56_fiscalunit.respect_bit != default_fiscalunit.respect_bit
    assert accord56_fiscalunit.bridge != default_fiscalunit.bridge
    assert accord56_fiscalunit != default_fiscalunit


def test_create_fiscalunit_jsons_from_prime_files_Scenario2_PartialTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_c400_number = 9
    accord56_monthday_distortion = 7
    accord56_timeline_title = "timelineX3"
    accord56_yr1_jan1_offset = 555
    accord56 = [
        accord56_str,
        "",  # accord56_fund_coin,
        "",  # accord56_penny,
        "",  # accord56_respect_bit,
        "",  # accord56_present_time,
        "",  # accord56_bridge,
        accord56_c400_number,
        accord56_yr1_jan1_offset,
        accord56_monthday_distortion,
        accord56_timeline_title,
    ]
    fiscalunit_rows = [accord56]
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.unit_agg_columns)
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    assert accord56_fiscalunit
    assert accord56_fiscalunit.fiscal_title == accord56_str
    expected_timeline_config = timeline_config_shop(
        c400_number=accord56_c400_number,
        monthday_distortion=accord56_monthday_distortion,
        timeline_title=accord56_timeline_title,
        yr1_jan1_offset=accord56_yr1_jan1_offset,
    )
    expected_timelineunit = timelineunit_shop(expected_timeline_config)
    expected_fiscalunit = fiscalunit_shop(accord56_str, timeline=expected_timelineunit)
    assert accord56_fiscalunit.timeline.timeline_title == accord56_timeline_title
    assert accord56_fiscalunit.timeline.c400_number == accord56_c400_number
    assert accord56_fiscalunit.timeline == expected_timelineunit
    assert accord56_fiscalunit.timeline == expected_fiscalunit.timeline
    assert accord56_fiscalunit == expected_fiscalunit


def test_create_fiscalunit_jsons_from_prime_files_Scenario3_fiscal_timeline_weekday(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    monday_str = "Monday"
    tuesday_str = "Tuesday"
    accord56_fiscal_row = [accord56_str, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_weekday_t3 = [accord56_str, monday_str, 3]
    a56_weekday_t7 = [accord56_str, tuesday_str, 4]
    a56_weekday_rows = [a56_weekday_t3, a56_weekday_t7]
    a56_weekday_df = DataFrame(a56_weekday_rows, columns=xc.week_agg_columns)
    print(f"{a56_weekday_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.week_excel_path, agg_str, a56_weekday_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(accord56_str, fiscal_mstr_dir, x_timelineunit)
    expected_fiscalunit.timeline.weekdays_config = [monday_str, tuesday_str]
    print(f"{expected_fiscalunit.timeline.weekdays_config=}")
    assert accord56_fiscalunit.timeline.weekdays_config == [monday_str, tuesday_str]
    assert (
        accord56_fiscalunit.timeline.weekdays_config == x_timelineunit.weekdays_config
    )


def test_create_fiscalunit_jsons_from_prime_files_Scenario4_fiscal_timeline_month(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    july_str = "July"
    june_str = "June"
    accord56_fiscal_row = [accord56_str, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_june = [accord56_str, june_str, 150]
    a56_july = [accord56_str, july_str, 365]
    a56_month_rows = [a56_july, a56_june]
    a56_month_df = DataFrame(a56_month_rows, columns=xc.mont_agg_columns)
    print(f"{a56_month_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.mont_excel_path, agg_str, a56_month_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(accord56_str, fiscal_mstr_dir, x_timelineunit)
    expected_fiscalunit.timeline.months_config = [[june_str, 150], [july_str, 365]]
    print(f"{expected_fiscalunit.timeline.months_config=}")
    assert accord56_fiscalunit.timeline.months_config == [
        [june_str, 150],
        [july_str, 365],
    ]
    assert accord56_fiscalunit.timeline.months_config == x_timelineunit.months_config


def test_create_fiscalunit_jsons_from_prime_files_Scenario5_fiscal_timeline_hour(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    a56_0hr = "0hour"
    a56_5hr = "5hour"
    a56_8hr = "8hour"
    accord56_fiscal_row = [accord56_str, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_0hour_row = [accord56_str, a56_0hr, 60]
    a56_5hour_row = [accord56_str, a56_5hr, 500]
    a56_8hour_row = [accord56_str, a56_8hr, 1440]
    a56_hour_rows = [a56_0hour_row, a56_5hour_row, a56_8hour_row]
    a56_hour_df = DataFrame(a56_hour_rows, columns=xc.hour_agg_columns)
    print(f"{a56_hour_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.hour_excel_path, agg_str, a56_hour_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(accord56_str, fiscal_mstr_dir, x_timelineunit)
    expected_hour_config = [[a56_0hr, 60], [a56_5hr, 500], [a56_8hr, 1440]]
    expected_fiscalunit.timeline.hours_config = expected_hour_config
    print(f"{expected_fiscalunit.timeline.hours_config=}")
    assert accord56_fiscalunit.timeline.hours_config == expected_hour_config
    assert accord56_fiscalunit.timeline.hours_config == x_timelineunit.hours_config


def test_create_fiscalunit_jsons_from_prime_files_Scenario6_fiscal_cashbook(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    t3 = 3
    t7 = 7
    amount3 = 555
    amount7 = 777
    accord56_fiscal_row = [accord56_str, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_cashbook_t3 = [accord56_str, sue_str, bob_str, t3, amount3]
    a56_cashbook_t7 = [accord56_str, sue_str, bob_str, t7, amount7]
    a56_cashbook_rows = [a56_cashbook_t3, a56_cashbook_t7]
    fiscal_cashbook_df = DataFrame(a56_cashbook_rows, columns=xc.cash_agg_columns)
    # print(f"{fiscal_cashbook_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.cash_excel_path, agg_str, fiscal_cashbook_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(accord56_str, fiscal_mstr_dir, x_timelineunit)
    expected_fiscalunit.add_cashpurchase(sue_str, bob_str, t3, amount3)
    expected_fiscalunit.add_cashpurchase(sue_str, bob_str, t7, amount7)
    print(f"{expected_fiscalunit.cashbook=}")
    print(f"{accord56_fiscalunit.cashbook=}")
    # print(f"{accord56_fiscalunit=}")
    assert accord56_fiscalunit.cashbook == expected_fiscalunit.cashbook


def test_create_fiscalunit_jsons_from_prime_files_Scenario7_fiscal_deal_episode(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    sue_str = "Sue"
    t3 = 3
    t7 = 7
    quota3 = 555
    quota7 = 777
    accord56_fiscal_row = [accord56_str, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_deal_t3 = [accord56_str, sue_str, t3, quota3, None]
    a56_deal_t7 = [accord56_str, sue_str, t7, quota7, None]
    a56_deal_rows = [a56_deal_t3, a56_deal_t7]
    fiscal_deal_df = DataFrame(a56_deal_rows, columns=xc.deal_agg_columns)
    print(f"{fiscal_deal_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.deal_excel_path, agg_str, fiscal_deal_df)
    accord56_json_path = create_fiscal_json_path(fiscal_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(accord56_str, fiscal_mstr_dir, x_timelineunit)
    expected_fiscalunit.add_dealepisode(sue_str, t3, quota3)
    expected_fiscalunit.add_dealepisode(sue_str, t7, quota7)
    print(f"{expected_fiscalunit.deallogs=}")
    print(f"{expected_fiscalunit=}")
    assert accord56_fiscalunit.deallogs == expected_fiscalunit.deallogs


def test_collect_events_dir_owner_events_sets_ReturnsObj_Scenario0_none(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_events_dir = get_test_etl_dir()
    # WHEN
    owner_events_sets = collect_events_dir_owner_events_sets(fiscal_events_dir)
    # THEN
    assert owner_events_sets == {}


def test_collect_events_dir_owner_events_sets_ReturnsObj_Scenario1_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_events_dir = get_test_etl_dir()
    bob_str = "Bob"
    bob_dir = create_path(fiscal_events_dir, bob_str)
    event1 = 1
    event2 = 2
    bob_event1_dir = create_path(bob_dir, event1)
    bob_event2_dir = create_path(bob_dir, event2)
    set_dir(bob_event1_dir)
    set_dir(bob_event2_dir)

    # WHEN
    owner_events_sets = collect_events_dir_owner_events_sets(fiscal_events_dir)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}}


def test_collect_events_dir_owner_events_sets_ReturnsObj_Scenario2_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_events_dir = get_test_etl_dir()
    bob_str = "Bob"
    sue_str = "Sue"
    bob_dir = create_path(fiscal_events_dir, bob_str)
    sue_dir = create_path(fiscal_events_dir, sue_str)
    event1 = 1
    event2 = 2
    event7 = 7
    bob_event1_dir = create_path(bob_dir, event1)
    bob_event2_dir = create_path(bob_dir, event2)
    sue_event2_dir = create_path(sue_dir, event2)
    sue_event7_dir = create_path(sue_dir, event7)
    set_dir(bob_event1_dir)
    set_dir(bob_event2_dir)
    set_dir(sue_event2_dir)
    set_dir(sue_event7_dir)

    # WHEN
    owner_events_sets = collect_events_dir_owner_events_sets(fiscal_events_dir)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}, sue_str: {event2, event7}}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event2 = 2
    owner_events_sets = {}
    downhill_event_int = event2
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners, downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario1_simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {bob_str: {event1, event2}, sue_str: {event2, event7}}
    downhill_event_int = event2
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners, downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario2Empty_downhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event7}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario3Empty_downhill_owners():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(owner_events_sets)

    # THEN
    assert owners_downhill_event_ints == {
        bob_str: event2,
        sue_str: event7,
        yao_str: event7,
    }


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario4Empty_downhill_owners_Withdownhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event7},
    }
    downhill_event_int = 2

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, ref_event_int=downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event2}
