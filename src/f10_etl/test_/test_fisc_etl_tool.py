from src.f00_instrument.file import create_path, open_file, set_dir
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f03_chrono.chrono import timelineunit_shop, timeline_config_shop
from src.f04_gift.atom_config import (
    face_name_str,
    event_int_str,
    acct_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f05_listen.hub_path import create_fisc_json_path
from src.f07_fisc.fisc import get_from_json as fisc_get_from_json, fiscunit_shop
from src.f07_fisc.fisc_config import (
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    get_fisc_config_args,
)
from src.f09_idea.idea_db_tool import sheet_exists, upsert_sheet, get_custom_sorted_list
from src.f10_etl.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
    create_init_fisc_prime_files,
    create_fiscunit_jsons_from_prime_files,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_FiscPrimeObjsRef_Exists():
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    xp = FiscPrimeObjsRef(x_dir)

    # THEN
    assert xp
    agg_str = "_agg"
    assert xp.unit_agg_tablename == f"{fiscunit_str()}{agg_str}"
    assert xp.deal_agg_tablename == f"{fisc_dealunit_str()}{agg_str}"
    assert xp.cash_agg_tablename == f"{fisc_cashbook_str()}{agg_str}"
    assert xp.hour_agg_tablename == f"{fisc_timeline_hour_str()}{agg_str}"
    assert xp.mont_agg_tablename == f"{fisc_timeline_month_str()}{agg_str}"
    assert xp.week_agg_tablename == f"{fisc_timeline_weekday_str()}{agg_str}"
    staging_str = "_staging"
    assert xp.unit_stage_tablename == f"{fiscunit_str()}{staging_str}"
    assert xp.deal_stage_tablename == f"{fisc_dealunit_str()}{staging_str}"
    assert xp.cash_stage_tablename == f"{fisc_cashbook_str()}{staging_str}"
    assert xp.hour_stage_tablename == f"{fisc_timeline_hour_str()}{staging_str}"
    assert xp.mont_stage_tablename == f"{fisc_timeline_month_str()}{staging_str}"
    assert xp.week_stage_tablename == f"{fisc_timeline_weekday_str()}{staging_str}"
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
    assert xp.unit_excel_filename == f"{fiscunit_str()}.xlsx"
    assert xp.deal_excel_filename == f"{fisc_dealunit_str()}.xlsx"
    assert xp.cash_excel_filename == f"{fisc_cashbook_str()}.xlsx"
    assert xp.hour_excel_filename == f"{fisc_timeline_hour_str()}.xlsx"
    assert xp.mont_excel_filename == f"{fisc_timeline_month_str()}.xlsx"
    assert xp.week_excel_filename == f"{fisc_timeline_weekday_str()}.xlsx"
    assert xp.unit_excel_path == create_path(x_dir, xp.unit_excel_filename)
    assert xp.deal_excel_path == create_path(x_dir, xp.deal_excel_filename)
    assert xp.cash_excel_path == create_path(x_dir, xp.cash_excel_filename)
    assert xp.hour_excel_path == create_path(x_dir, xp.hour_excel_filename)
    assert xp.mont_excel_path == create_path(x_dir, xp.mont_excel_filename)
    assert xp.week_excel_path == create_path(x_dir, xp.week_excel_filename)


def test_FiscPrimeColumnsRef_Exists():
    # ESTABLISH / WHEN
    fisc_cols = FiscPrimeColumnsRef()

    # THEN
    unit_args = set(get_fisc_config_args(fiscunit_str()).keys())
    cash_args = set(get_fisc_config_args(fisc_cashbook_str()).keys())
    deal_args = set(get_fisc_config_args(fisc_dealunit_str()).keys())
    hour_args = set(get_fisc_config_args(fisc_timeline_hour_str()).keys())
    mont_args = set(get_fisc_config_args(fisc_timeline_month_str()).keys())
    week_args = set(get_fisc_config_args(fisc_timeline_weekday_str()).keys())
    print(f"           {fisc_cols.unit_agg_columns=}")
    print(f"{get_custom_sorted_list(list(unit_args))=}")
    assert fisc_cols.unit_agg_columns == get_custom_sorted_list(unit_args)
    assert fisc_cols.cash_agg_columns == get_custom_sorted_list(cash_args)
    assert fisc_cols.deal_agg_columns == get_custom_sorted_list(deal_args)
    assert fisc_cols.hour_agg_columns == get_custom_sorted_list(hour_args)
    assert fisc_cols.mont_agg_columns == get_custom_sorted_list(mont_args)
    assert fisc_cols.week_agg_columns == get_custom_sorted_list(week_args)

    staging_args = {"idea_number", face_name_str(), event_int_str(), "error_message"}
    unit_staging_args = unit_args.union(staging_args)
    cash_staging_args = cash_args.union(staging_args)
    deal_staging_args = deal_args.union(staging_args)
    hour_staging_args = hour_args.union(staging_args)
    mont_staging_args = mont_args.union(staging_args)
    week_staging_args = week_args.union(staging_args)
    assert fisc_cols.unit_staging_columns == get_custom_sorted_list(unit_staging_args)
    assert fisc_cols.cash_staging_columns == get_custom_sorted_list(cash_staging_args)
    assert fisc_cols.deal_staging_columns == get_custom_sorted_list(deal_staging_args)
    assert fisc_cols.hour_staging_columns == get_custom_sorted_list(hour_staging_args)
    assert fisc_cols.mont_staging_columns == get_custom_sorted_list(mont_staging_args)
    assert fisc_cols.week_staging_columns == get_custom_sorted_list(week_staging_args)

    # unit_staging_csv_header = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}"""
    unit_staging_csv_header = ",".join(fisc_cols.unit_staging_columns)
    deal_staging_csv_header = ",".join(fisc_cols.deal_staging_columns)
    cash_staging_csv_header = ",".join(fisc_cols.cash_staging_columns)
    hour_staging_csv_header = ",".join(fisc_cols.hour_staging_columns)
    mont_staging_csv_header = ",".join(fisc_cols.mont_staging_columns)
    week_staging_csv_header = ",".join(fisc_cols.week_staging_columns)

    assert fisc_cols.unit_staging_csv_header == unit_staging_csv_header
    assert fisc_cols.deal_staging_csv_header == deal_staging_csv_header
    assert fisc_cols.cash_staging_csv_header == cash_staging_csv_header
    assert fisc_cols.hour_staging_csv_header == hour_staging_csv_header
    assert fisc_cols.mont_staging_csv_header == mont_staging_csv_header
    assert fisc_cols.week_staging_csv_header == week_staging_csv_header
    unit_agg_csv_header = ",".join(fisc_cols.unit_agg_columns)
    deal_agg_csv_header = ",".join(fisc_cols.deal_agg_columns)
    cash_agg_csv_header = ",".join(fisc_cols.cash_agg_columns)
    hour_agg_csv_header = ",".join(fisc_cols.hour_agg_columns)
    mont_agg_csv_header = ",".join(fisc_cols.mont_agg_columns)
    week_agg_csv_header = ",".join(fisc_cols.week_agg_columns)

    assert fisc_cols.unit_agg_csv_header == unit_agg_csv_header
    assert fisc_cols.deal_agg_csv_header == deal_agg_csv_header
    assert fisc_cols.cash_agg_csv_header == cash_agg_csv_header
    assert fisc_cols.hour_agg_csv_header == hour_agg_csv_header
    assert fisc_cols.mont_agg_csv_header == mont_agg_csv_header
    assert fisc_cols.week_agg_csv_header == week_agg_csv_header
    assert fisc_cols.unit_agg_empty_csv == f"{unit_agg_csv_header}\n"
    assert fisc_cols.deal_agg_empty_csv == f"{deal_agg_csv_header}\n"
    assert fisc_cols.cash_agg_empty_csv == f"{cash_agg_csv_header}\n"
    assert fisc_cols.hour_agg_empty_csv == f"{hour_agg_csv_header}\n"
    assert fisc_cols.mont_agg_empty_csv == f"{mont_agg_csv_header}\n"
    assert fisc_cols.week_agg_empty_csv == f"{week_agg_csv_header}\n"


def test_create_init_fisc_prime_files_CreatesFiles_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    staging_str = "staging"
    fiscref = FiscPrimeObjsRef(x_dir)
    assert sheet_exists(fiscref.unit_excel_path, staging_str) is False
    assert sheet_exists(fiscref.deal_excel_path, staging_str) is False
    assert sheet_exists(fiscref.cash_excel_path, staging_str) is False
    assert sheet_exists(fiscref.hour_excel_path, staging_str) is False
    assert sheet_exists(fiscref.mont_excel_path, staging_str) is False
    assert sheet_exists(fiscref.week_excel_path, staging_str) is False

    # WHEN
    create_init_fisc_prime_files(x_dir)

    # THEN
    assert sheet_exists(fiscref.unit_excel_path, staging_str)
    assert sheet_exists(fiscref.deal_excel_path, staging_str)
    assert sheet_exists(fiscref.cash_excel_path, staging_str)
    assert sheet_exists(fiscref.hour_excel_path, staging_str)
    assert sheet_exists(fiscref.mont_excel_path, staging_str)
    assert sheet_exists(fiscref.week_excel_path, staging_str)


def test_create_init_fisc_prime_files_HasCorrectColumns_staging(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_fisc_prime_files(x_dir)

    # THEN
    staging_str = "staging"
    xp = FiscPrimeObjsRef(x_dir)
    fiscunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=staging_str)
    fiscdeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=staging_str)
    fisccash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=staging_str)
    fischour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=staging_str)
    fiscmont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=staging_str)
    fiscweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=staging_str)

    expected_cols = FiscPrimeColumnsRef()
    print(f"{list(fiscunit_df.columns)=}")
    assert list(fiscunit_df.columns) == expected_cols.unit_staging_columns
    assert list(fiscdeal_df.columns) == expected_cols.deal_staging_columns
    assert list(fisccash_df.columns) == expected_cols.cash_staging_columns
    assert list(fischour_df.columns) == expected_cols.hour_staging_columns
    assert list(fiscmont_df.columns) == expected_cols.mont_staging_columns
    assert list(fiscweek_df.columns) == expected_cols.week_staging_columns


def test_create_init_fisc_prime_files_CreatesFiles_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    agg_str = "agg"
    xp = FiscPrimeObjsRef(x_dir)
    assert sheet_exists(xp.unit_excel_path, agg_str) is False
    assert sheet_exists(xp.deal_excel_path, agg_str) is False
    assert sheet_exists(xp.cash_excel_path, agg_str) is False
    assert sheet_exists(xp.hour_excel_path, agg_str) is False
    assert sheet_exists(xp.mont_excel_path, agg_str) is False
    assert sheet_exists(xp.week_excel_path, agg_str) is False

    # WHEN
    create_init_fisc_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.unit_excel_path, agg_str)
    assert sheet_exists(xp.deal_excel_path, agg_str)
    assert sheet_exists(xp.cash_excel_path, agg_str)
    assert sheet_exists(xp.hour_excel_path, agg_str)
    assert sheet_exists(xp.mont_excel_path, agg_str)
    assert sheet_exists(xp.week_excel_path, agg_str)


def test_create_init_fisc_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_fisc_prime_files(x_dir)

    # THEN
    agg_str = "agg"
    xp = FiscPrimeObjsRef(x_dir)
    fiscunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=agg_str)
    fiscdeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=agg_str)
    fisccash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=agg_str)
    fischour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=agg_str)
    fiscmont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=agg_str)
    fiscweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=agg_str)

    expected_cols = FiscPrimeColumnsRef()
    print(f"{list(fiscunit_df.columns)=}")
    assert list(fiscunit_df.columns) == expected_cols.unit_agg_columns
    assert list(fiscdeal_df.columns) == expected_cols.deal_agg_columns
    assert list(fisccash_df.columns) == expected_cols.cash_agg_columns
    assert list(fischour_df.columns) == expected_cols.hour_agg_columns
    assert list(fiscmont_df.columns) == expected_cols.mont_agg_columns
    assert list(fiscweek_df.columns) == expected_cols.week_agg_columns


def test_create_fiscunit_jsons_from_prime_files_Scenario0_MinimumNecessaryParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_row = [
        accord56_str,
        "",  # accord56_c400_number_str,
        "",  # accord56_fund_coin_str,
        "",  # accord56_monthday_distortion_str,
        "",  # accord56_penny_str,
        "",  # accord56_respect_bit_str,
        "",  # accord56_bridge_str,
        "",  # accord56_timeline_title_str,
        "",  # accord56_yr1_jan1_offset_str,
    ]
    fiscunit_rows = [accord56_row]
    fiscunit_df = DataFrame(fiscunit_rows, columns=xc.unit_agg_columns)
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    accord56_fiscunit.fisc_mstr_dir = fisc_mstr_dir
    accord56_fiscunit._set_fisc_dirs()
    assert accord56_fiscunit
    assert accord56_fiscunit.fisc_title == accord56_str
    assert accord56_fiscunit.fisc_mstr_dir == fisc_mstr_dir
    expected_fiscunit = fiscunit_shop(accord56_str, fisc_mstr_dir)
    assert accord56_fiscunit.timeline == expected_fiscunit.timeline
    assert accord56_fiscunit == expected_fiscunit


def test_create_fiscunit_jsons_from_prime_files_Scenario1_IncludeNoneTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    # accord56_offi_time_max = 77
    accord56_fund_coin = 3
    accord56_penny = 2
    accord56_respect_bit = 55
    accord56_bridge = "/"
    accord56 = [
        accord56_str,
        "",  # accord56_timeline_title_str,
        "",  # accord56_c400_number_str,
        "",  # accord56_yr1_jan1_offset_str,
        "",  # accord56_monthday_distortion_str,
        accord56_fund_coin,
        accord56_penny,
        accord56_respect_bit,
        accord56_bridge,
    ]
    print(f"{xc.unit_agg_columns=}")
    fiscunit_rows = [accord56]
    fiscunit_df = DataFrame(fiscunit_rows, columns=xc.unit_agg_columns)
    print(f"{xc.unit_agg_columns=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    assert accord56_fiscunit
    assert accord56_fiscunit.fisc_title == accord56_str
    # assert accord56_fiscunit._offi_time_max == accord56_offi_time_max
    assert accord56_fiscunit.fund_coin == accord56_fund_coin
    assert accord56_fiscunit.penny == accord56_penny
    assert accord56_fiscunit.respect_bit == accord56_respect_bit
    assert accord56_fiscunit.bridge == accord56_bridge
    default_fiscunit = fiscunit_shop(accord56_str)
    assert accord56_fiscunit.timeline == default_fiscunit.timeline
    assert accord56_fiscunit.fisc_title == accord56_str
    # assert accord56_fiscunit._offi_time_max != default_fiscunit._offi_time_max
    assert accord56_fiscunit.fund_coin != default_fiscunit.fund_coin
    assert accord56_fiscunit.penny != default_fiscunit.penny
    assert accord56_fiscunit.respect_bit != default_fiscunit.respect_bit
    assert accord56_fiscunit.bridge != default_fiscunit.bridge
    assert accord56_fiscunit != default_fiscunit


def test_create_fiscunit_jsons_from_prime_files_Scenario2_PartialTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_c400_number = 9
    accord56_monthday_distortion = 7
    accord56_timeline_title = "timelineX3"
    accord56_yr1_jan1_offset = 555
    accord56 = [
        accord56_str,
        accord56_timeline_title,
        accord56_c400_number,
        accord56_yr1_jan1_offset,
        accord56_monthday_distortion,
        "",  # accord56_fund_coin,
        "",  # accord56_penny,
        "",  # accord56_respect_bit,
        # "",  # accord56_offi_time_max,
        "",  # accord56_bridge,
    ]
    fiscunit_rows = [accord56]
    fiscunit_df = DataFrame(fiscunit_rows, columns=xc.unit_agg_columns)
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    assert accord56_fiscunit
    assert accord56_fiscunit.fisc_title == accord56_str
    expected_timeline_config = timeline_config_shop(
        c400_number=accord56_c400_number,
        monthday_distortion=accord56_monthday_distortion,
        timeline_title=accord56_timeline_title,
        yr1_jan1_offset=accord56_yr1_jan1_offset,
    )
    expected_timelineunit = timelineunit_shop(expected_timeline_config)
    expected_fiscunit = fiscunit_shop(accord56_str, timeline=expected_timelineunit)
    assert accord56_fiscunit.timeline.timeline_title == accord56_timeline_title
    assert accord56_fiscunit.timeline.c400_number == accord56_c400_number
    assert accord56_fiscunit.timeline == expected_timelineunit
    assert accord56_fiscunit.timeline == expected_fiscunit.timeline
    assert accord56_fiscunit == expected_fiscunit


def test_create_fiscunit_jsons_from_prime_files_Scenario3_fisc_timeline_weekday(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    monday_str = "Monday"
    tuesday_str = "Tuesday"
    accord56_fisc_row = [accord56_str, "", "", "", "", "", "", "", ""]
    fiscunit_df = DataFrame([accord56_fisc_row], columns=xc.unit_agg_columns)
    a56_weekday_t3 = [accord56_str, 3, monday_str]
    a56_weekday_t7 = [accord56_str, 4, tuesday_str]
    a56_weekday_rows = [a56_weekday_t3, a56_weekday_t7]
    a56_weekday_df = DataFrame(a56_weekday_rows, columns=xc.week_agg_columns)
    print(f"{a56_weekday_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    upsert_sheet(xp.week_excel_path, agg_str, a56_weekday_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscunit = fiscunit_shop(accord56_str, fisc_mstr_dir, x_timelineunit)
    expected_fiscunit.timeline.weekdays_config = [monday_str, tuesday_str]
    print(f"{expected_fiscunit.timeline.weekdays_config=}")
    assert accord56_fiscunit.timeline.weekdays_config == [monday_str, tuesday_str]
    assert accord56_fiscunit.timeline.weekdays_config == x_timelineunit.weekdays_config


def test_create_fiscunit_jsons_from_prime_files_Scenario4_fisc_timeline_month(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    july_str = "July"
    june_str = "June"
    accord56_fisc_row = [accord56_str, "", "", "", "", "", "", "", ""]
    fiscunit_df = DataFrame([accord56_fisc_row], columns=xc.unit_agg_columns)
    a56_june = [accord56_str, 150, june_str]
    a56_july = [accord56_str, 365, july_str]
    a56_month_rows = [a56_july, a56_june]
    a56_month_df = DataFrame(a56_month_rows, columns=xc.mont_agg_columns)
    print(f"{a56_month_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    upsert_sheet(xp.mont_excel_path, agg_str, a56_month_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscunit = fiscunit_shop(accord56_str, fisc_mstr_dir, x_timelineunit)
    expected_fiscunit.timeline.months_config = [[june_str, 150], [july_str, 365]]
    print(f"{expected_fiscunit.timeline.months_config=}")
    assert accord56_fiscunit.timeline.months_config == [
        [june_str, 150],
        [july_str, 365],
    ]
    assert accord56_fiscunit.timeline.months_config == x_timelineunit.months_config


def test_create_fiscunit_jsons_from_prime_files_Scenario5_fisc_timeline_hour(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    a56_0hr = "0hour"
    a56_5hr = "5hour"
    a56_8hr = "8hour"
    accord56_fisc_row = [accord56_str, "", "", "", "", "", "", "", ""]
    fiscunit_df = DataFrame([accord56_fisc_row], columns=xc.unit_agg_columns)
    a56_0hour_row = [accord56_str, 60, a56_0hr]
    a56_5hour_row = [accord56_str, 500, a56_5hr]
    a56_8hour_row = [accord56_str, 1440, a56_8hr]
    a56_hour_rows = [a56_0hour_row, a56_5hour_row, a56_8hour_row]
    a56_hour_df = DataFrame(a56_hour_rows, columns=xc.hour_agg_columns)
    print(f"{a56_hour_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    upsert_sheet(xp.hour_excel_path, agg_str, a56_hour_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscunit = fiscunit_shop(accord56_str, fisc_mstr_dir, x_timelineunit)
    expected_hour_config = [[a56_0hr, 60], [a56_5hr, 500], [a56_8hr, 1440]]
    expected_fiscunit.timeline.hours_config = expected_hour_config
    print(f"{expected_fiscunit.timeline.hours_config=}")
    assert accord56_fiscunit.timeline.hours_config == expected_hour_config
    assert accord56_fiscunit.timeline.hours_config == x_timelineunit.hours_config


def test_create_fiscunit_jsons_from_prime_files_Scenario6_fisc_cashbook(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    t3 = 3
    t7 = 7
    amount3 = 555
    amount7 = 777
    accord56_fisc_row = [accord56_str, "", "", "", "", "", "", "", ""]
    fiscunit_df = DataFrame([accord56_fisc_row], columns=xc.unit_agg_columns)
    a56_cashbook_t3 = [accord56_str, sue_str, bob_str, t3, amount3]
    a56_cashbook_t7 = [accord56_str, sue_str, bob_str, t7, amount7]
    a56_cashbook_rows = [a56_cashbook_t3, a56_cashbook_t7]
    fisc_cashbook_df = DataFrame(a56_cashbook_rows, columns=xc.cash_agg_columns)
    # print(f"{fisc_cashbook_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    upsert_sheet(xp.cash_excel_path, agg_str, fisc_cashbook_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscunit = fiscunit_shop(accord56_str, fisc_mstr_dir, x_timelineunit)
    expected_fiscunit.add_cashpurchase(sue_str, bob_str, t3, amount3)
    expected_fiscunit.add_cashpurchase(sue_str, bob_str, t7, amount7)
    print(f"{expected_fiscunit.cashbook=}")
    print(f"{accord56_fiscunit.cashbook=}")
    # print(f"{accord56_fiscunit=}")
    assert accord56_fiscunit.cashbook == expected_fiscunit.cashbook


def test_create_fiscunit_jsons_from_prime_files_Scenario7_fisc_dealunit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = create_path(get_test_etl_dir(), "fisc_mstr")
    create_init_fisc_prime_files(fisc_mstr_dir)
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    xc = FiscPrimeColumnsRef()
    agg_str = "agg"
    accord56_str = "accord56"
    accord56_str
    sue_str = "Sue"
    t3 = 3
    t7 = 7
    quota3 = 555
    quota7 = 777
    accord56_fisc_row = [accord56_str, "", "", "", "", "", "", "", ""]
    fiscunit_df = DataFrame([accord56_fisc_row], columns=xc.unit_agg_columns)
    a56_deal_t3 = [accord56_str, sue_str, t3, quota3, None]
    a56_deal_t7 = [accord56_str, sue_str, t7, quota7, None]
    a56_deal_rows = [a56_deal_t3, a56_deal_t7]
    fisc_deal_df = DataFrame(a56_deal_rows, columns=xc.deal_agg_columns)
    print(f"{fisc_deal_df=}")
    upsert_sheet(xp.unit_excel_path, agg_str, fiscunit_df)
    upsert_sheet(xp.deal_excel_path, agg_str, fisc_deal_df)
    accord56_json_path = create_fisc_json_path(fisc_mstr_dir, accord56_str)
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_fiscunit_jsons_from_prime_files(fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_fiscunit = fisc_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(timeline_config_shop())
    expected_fiscunit = fiscunit_shop(accord56_str, fisc_mstr_dir, x_timelineunit)
    expected_fiscunit.add_dealunit(sue_str, t3, quota3)
    expected_fiscunit.add_dealunit(sue_str, t7, quota7)
    print(f"{expected_fiscunit.brokerunits=}")
    print(f"{accord56_fiscunit.brokerunits=}")
    # print(f"{expected_fiscunit=}")
    assert accord56_fiscunit.brokerunits == expected_fiscunit.brokerunits
