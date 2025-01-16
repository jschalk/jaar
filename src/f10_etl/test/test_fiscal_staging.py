from src.f00_instrument.file import create_path, open_file
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
from src.f07_fiscal.fiscal import get_from_json as fiscal_get_from_json, fiscalunit_shop
from src.f07_fiscal.fiscal_config import (
    fiscal_cashbook_str,
    fiscal_deal_episode_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    fiscalunit_str,
    get_fiscal_config_args,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.pandas_tool import sheet_exists, upsert_sheet
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsTestingRef,
    FiscalPrimeColumnsTestingRef,
    create_init_fiscal_prime_files,
    create_fiscalunit_jsons_from_prime_files,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


# br00000 fiscal_title c400_number,current_time,fund_coin,monthday_distortion,penny,respect_bit,bridge,timeline_title,yr1_jan1_offset
# br00001 fiscal_title owner_name,acct_name,time_int,quota
# br00002 fiscal_title owner_name,acct_name,time_int,amount
# br00003 fiscal_title hour_title,cumlative_minute
# br00004 fiscal_title month_title,cumlative_day
# br00005 fiscal_title weekday_title,weekday_order


def test_FiscalPrimeObjsTestingRef_Exists():
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    xp = FiscalPrimeObjsTestingRef(x_dir)

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


def test_FiscalPrimeColumnsTestingRef_Exists():
    # ESTABLISH / WHEN
    x_fiscalprimecols = FiscalPrimeColumnsTestingRef()

    # THEN
    fiscalcash_args = set(get_fiscal_config_args(fiscal_cashbook_str()).keys())
    fiscaldeal_args = set(get_fiscal_config_args(fiscal_deal_episode_str()).keys())
    fiscalhour_args = set(get_fiscal_config_args(fiscal_timeline_hour_str()).keys())
    fiscalmont_args = set(get_fiscal_config_args(fiscal_timeline_month_str()).keys())
    fiscalweek_args = set(get_fiscal_config_args(fiscal_timeline_weekday_str()).keys())
    fiscalunit_args = set(get_fiscal_config_args(fiscalunit_str()).keys())
    assert set(x_fiscalprimecols.cash_agg_columns) == fiscalcash_args
    assert set(x_fiscalprimecols.deal_agg_columns) == fiscaldeal_args
    assert set(x_fiscalprimecols.hour_agg_columns) == fiscalhour_args
    assert set(x_fiscalprimecols.mont_agg_columns) == fiscalmont_args
    assert set(x_fiscalprimecols.week_agg_columns) == fiscalweek_args
    assert set(x_fiscalprimecols.unit_agg_columns) == fiscalunit_args

    staging_args = {"source_br", face_name_str(), event_int_str(), "note"}
    fiscalcash_staging = fiscalcash_args.union(staging_args)
    fiscaldeal_staging = fiscaldeal_args.union(staging_args)
    fiscalhour_staging = fiscalhour_args.union(staging_args)
    fiscalmont_staging = fiscalmont_args.union(staging_args)
    fiscalweek_staging = fiscalweek_args.union(staging_args)
    fiscalunit_staging = fiscalunit_args.union(staging_args)
    assert set(x_fiscalprimecols.cash_staging_columns) == fiscalcash_staging
    assert set(x_fiscalprimecols.deal_staging_columns) == fiscaldeal_staging
    assert set(x_fiscalprimecols.hour_staging_columns) == fiscalhour_staging
    assert set(x_fiscalprimecols.mont_staging_columns) == fiscalmont_staging
    assert set(x_fiscalprimecols.week_staging_columns) == fiscalweek_staging
    assert set(x_fiscalprimecols.unit_staging_columns) == fiscalunit_staging

    # unit_staging_csv_header = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}"""
    unit_staging_csv_header = """source_br,face_name,event_int,fiscal_title,fund_coin,penny,respect_bit,current_time,bridge,c400_number,yr1_jan1_offset,monthday_distortion,timeline_title,note"""
    deal_staging_csv_header = (
        """source_br,face_name,event_int,fiscal_title,owner_name,time_int,quota,note"""
    )
    cash_staging_csv_header = """source_br,face_name,event_int,fiscal_title,owner_name,acct_name,time_int,amount,note"""
    hour_staging_csv_header = """source_br,face_name,event_int,fiscal_title,hour_title,cumlative_minute,note"""
    mont_staging_csv_header = (
        """source_br,face_name,event_int,fiscal_title,month_title,cumlative_day,note"""
    )
    week_staging_csv_header = """source_br,face_name,event_int,fiscal_title,weekday_title,weekday_order,note"""
    assert x_fiscalprimecols.unit_staging_csv_header == unit_staging_csv_header
    assert x_fiscalprimecols.deal_staging_csv_header == deal_staging_csv_header
    assert x_fiscalprimecols.cash_staging_csv_header == cash_staging_csv_header
    assert x_fiscalprimecols.hour_staging_csv_header == hour_staging_csv_header
    assert x_fiscalprimecols.mont_staging_csv_header == mont_staging_csv_header
    assert x_fiscalprimecols.week_staging_csv_header == week_staging_csv_header
    unit_agg_csv_header = """fiscal_title,fund_coin,penny,respect_bit,current_time,bridge,c400_number,yr1_jan1_offset,monthday_distortion,timeline_title"""
    deal_agg_csv_header = """fiscal_title,owner_name,time_int,quota"""
    cash_agg_csv_header = """fiscal_title,owner_name,acct_name,time_int,amount"""
    hour_agg_csv_header = """fiscal_title,hour_title,cumlative_minute"""
    mont_agg_csv_header = """fiscal_title,month_title,cumlative_day"""
    week_agg_csv_header = """fiscal_title,weekday_title,weekday_order"""
    assert x_fiscalprimecols.unit_agg_csv_header == unit_agg_csv_header
    assert x_fiscalprimecols.deal_agg_csv_header == deal_agg_csv_header
    assert x_fiscalprimecols.cash_agg_csv_header == cash_agg_csv_header
    assert x_fiscalprimecols.hour_agg_csv_header == hour_agg_csv_header
    assert x_fiscalprimecols.mont_agg_csv_header == mont_agg_csv_header
    assert x_fiscalprimecols.week_agg_csv_header == week_agg_csv_header
    assert x_fiscalprimecols.unit_agg_empty_csv == f"{unit_agg_csv_header}\n"
    assert x_fiscalprimecols.deal_agg_empty_csv == f"{deal_agg_csv_header}\n"
    assert x_fiscalprimecols.cash_agg_empty_csv == f"{cash_agg_csv_header}\n"
    assert x_fiscalprimecols.hour_agg_empty_csv == f"{hour_agg_csv_header}\n"
    assert x_fiscalprimecols.mont_agg_empty_csv == f"{mont_agg_csv_header}\n"
    assert x_fiscalprimecols.week_agg_empty_csv == f"{week_agg_csv_header}\n"


def test_create_init_fiscal_prime_files_CreatesFiles_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    staging_str = "staging"
    fiscalref = FiscalPrimeObjsTestingRef(x_dir)
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
    xp = FiscalPrimeObjsTestingRef(x_dir)
    fiscalunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=staging_str)
    fiscaldeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=staging_str)
    fiscalcash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=staging_str)
    fiscalhour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=staging_str)
    fiscalmont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=staging_str)
    fiscalweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=staging_str)

    expected_cols = FiscalPrimeColumnsTestingRef()
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
    xp = FiscalPrimeObjsTestingRef(x_dir)
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
    xp = FiscalPrimeObjsTestingRef(x_dir)
    fiscalunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=agg_str)
    fiscaldeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=agg_str)
    fiscalcash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=agg_str)
    fiscalhour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=agg_str)
    fiscalmont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=agg_str)
    fiscalweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=agg_str)

    expected_cols = FiscalPrimeColumnsTestingRef()
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
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title_str = "accord56"
    accord56 = [
        accord56_fiscal_title_str,
        "",  # accord56_c400_number_str,
        "",  # accord56_current_time_str,
        "",  # accord56_fund_coin_str,
        "",  # accord56_monthday_distortion_str,
        "",  # accord56_penny_str,
        "",  # accord56_respect_bit_str,
        "",  # accord56_bridge_str,
        "",  # accord56_timeline_title_str,
        "",  # accord56_yr1_jan1_offset_str,
    ]
    fiscalunit_rows = [accord56]
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.unit_agg_columns)
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    accord56_fiscalunit.fiscals_dir = fiscal_mstr_dir
    accord56_fiscalunit._set_fiscal_dirs()
    assert accord56_fiscalunit
    assert accord56_fiscalunit.fiscal_title == accord56_fiscal_title_str
    assert accord56_fiscalunit.fiscals_dir == fiscal_mstr_dir
    expected_fiscalunit = fiscalunit_shop(accord56_fiscal_title_str, fiscal_mstr_dir)
    assert accord56_fiscalunit.timeline == expected_fiscalunit.timeline
    assert accord56_fiscalunit == expected_fiscalunit


def test_create_fiscalunit_jsons_from_prime_files_Scenario1_IncludeNoneTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title_str = "accord56"
    accord56_current_time = 77
    accord56_fund_coin = 3
    accord56_penny = 2
    accord56_respect_bit = 55
    accord56_bridge = "/"
    accord56 = [
        accord56_fiscal_title_str,
        accord56_fund_coin,
        accord56_penny,
        accord56_respect_bit,
        accord56_current_time,
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
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    assert accord56_fiscalunit
    assert accord56_fiscalunit.fiscal_title == accord56_fiscal_title_str
    assert accord56_fiscalunit.current_time == accord56_current_time
    assert accord56_fiscalunit.fund_coin == accord56_fund_coin
    assert accord56_fiscalunit.penny == accord56_penny
    assert accord56_fiscalunit.respect_bit == accord56_respect_bit
    assert accord56_fiscalunit.bridge == accord56_bridge
    default_fiscalunit = fiscalunit_shop(accord56_fiscal_title_str)
    assert accord56_fiscalunit.timeline == default_fiscalunit.timeline
    assert accord56_fiscalunit.fiscal_title == accord56_fiscal_title_str
    assert accord56_fiscalunit.current_time != default_fiscalunit.current_time
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
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_c400_number = 9
    accord56_monthday_distortion = 7
    accord56_timeline_title = "timelineX3"
    accord56_yr1_jan1_offset = 555
    accord56 = [
        accord56_fiscal_title,
        "",  # accord56_fund_coin,
        "",  # accord56_penny,
        "",  # accord56_respect_bit,
        "",  # accord56_current_time,
        "",  # accord56_bridge,
        accord56_c400_number,
        accord56_yr1_jan1_offset,
        accord56_monthday_distortion,
        accord56_timeline_title,
    ]
    fiscalunit_rows = [accord56]
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.unit_agg_columns)
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    assert accord56_fiscalunit
    assert accord56_fiscalunit.fiscal_title == accord56_fiscal_title
    expected_timeline_config = timeline_config_shop(
        c400_number=accord56_c400_number,
        monthday_distortion=accord56_monthday_distortion,
        timeline_title=accord56_timeline_title,
        yr1_jan1_offset=accord56_yr1_jan1_offset,
    )
    expected_timelineunit = timelineunit_shop(expected_timeline_config)
    expected_fiscalunit = fiscalunit_shop(
        accord56_fiscal_title, timeline=expected_timelineunit
    )
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
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    monday_str = "Monday"
    tuesday_str = "Tuesday"
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_weekday_t3 = [accord56_fiscal_title, monday_str, 3]
    a56_weekday_t7 = [accord56_fiscal_title, tuesday_str, 4]
    a56_weekday_rows = [a56_weekday_t3, a56_weekday_t7]
    a56_weekday_df = DataFrame(a56_weekday_rows, columns=xc.week_agg_columns)
    print(f"{a56_weekday_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.week_excel_path, agg_str, a56_weekday_df)
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(
        accord56_fiscal_title, fiscal_mstr_dir, x_timelineunit
    )
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
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    july_str = "July"
    june_str = "June"
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_june = [accord56_fiscal_title, june_str, 150]
    a56_july = [accord56_fiscal_title, july_str, 365]
    a56_month_rows = [a56_july, a56_june]
    a56_month_df = DataFrame(a56_month_rows, columns=xc.mont_agg_columns)
    print(f"{a56_month_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.mont_excel_path, agg_str, a56_month_df)
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(
        accord56_fiscal_title, fiscal_mstr_dir, x_timelineunit
    )
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
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    a56_0hr = "0hour"
    a56_5hr = "5hour"
    a56_8hr = "8hour"
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_0hour_row = [accord56_fiscal_title, a56_0hr, 60]
    a56_5hour_row = [accord56_fiscal_title, a56_5hr, 500]
    a56_8hour_row = [accord56_fiscal_title, a56_8hr, 1440]
    a56_hour_rows = [a56_0hour_row, a56_5hour_row, a56_8hour_row]
    a56_hour_df = DataFrame(a56_hour_rows, columns=xc.hour_agg_columns)
    print(f"{a56_hour_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.hour_excel_path, agg_str, a56_hour_df)
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(
        accord56_fiscal_title, fiscal_mstr_dir, x_timelineunit
    )
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
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    t3 = 3
    t7 = 7
    amount3 = 555
    amount7 = 777
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_cashbook_t3 = [accord56_fiscal_title, sue_str, bob_str, t3, amount3]
    a56_cashbook_t7 = [accord56_fiscal_title, sue_str, bob_str, t7, amount7]
    a56_cashbook_rows = [a56_cashbook_t3, a56_cashbook_t7]
    fiscal_cashbook_df = DataFrame(a56_cashbook_rows, columns=xc.cash_agg_columns)
    # print(f"{fiscal_cashbook_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.cash_excel_path, agg_str, fiscal_cashbook_df)
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(
        accord56_fiscal_title, fiscal_mstr_dir, x_timelineunit
    )
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
    xp = FiscalPrimeObjsTestingRef(fiscal_mstr_dir)
    xc = FiscalPrimeColumnsTestingRef()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    sue_str = "Sue"
    t3 = 3
    t7 = 7
    quota3 = 555
    quota7 = 777
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.unit_agg_columns)
    a56_deal_t3 = [accord56_fiscal_title, sue_str, t3, quota3]
    a56_deal_t7 = [accord56_fiscal_title, sue_str, t7, quota7]
    a56_deal_rows = [a56_deal_t3, a56_deal_t7]
    fiscal_deal_df = DataFrame(a56_deal_rows, columns=xc.deal_agg_columns)
    print(f"{fiscal_deal_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.deal_excel_path, agg_str, fiscal_deal_df)
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    accord56_dir = create_path(fiscals_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscalunit = fiscal_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscalunit = fiscalunit_shop(
        accord56_fiscal_title, fiscal_mstr_dir, x_timelineunit
    )
    expected_fiscalunit.add_dealepisode(sue_str, t3, quota3)
    expected_fiscalunit.add_dealepisode(sue_str, t7, quota7)
    print(f"{expected_fiscalunit.deallogs=}")
    print(f"{expected_fiscalunit=}")
    assert accord56_fiscalunit.deallogs == expected_fiscalunit.deallogs
