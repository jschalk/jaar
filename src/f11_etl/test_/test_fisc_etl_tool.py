from src.f00_data_toolboxs.file_toolbox import create_path, open_file, set_dir
from src.f02_finance_toolboxs.deal import owner_name_str, fisc_title_str
from src.f03_chrono.chrono import timelineunit_shop, timeline_config_shop
from src.f04_pack.atom_config import (
    face_name_str,
    event_int_str,
    acct_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f06_listen.hub_path import create_fisc_json_path
from src.f08_fisc.fisc import get_from_json as fisc_get_from_json, fiscunit_shop
from src.f08_fisc.fisc_config import (
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
    get_fisc_config_args,
)
from src.f10_idea.idea_db_tool import (
    sheet_exists,
    upsert_sheet,
    get_default_sorted_list,
)
from src.f11_etl.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
    create_init_fisc_prime_files,
)
from src.f11_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
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
    assert xp.offi_agg_tablename == f"{fisc_timeoffi_str()}{agg_str}"
    staging_str = "_staging"
    assert xp.unit_stage_tablename == f"{fiscunit_str()}{staging_str}"
    assert xp.deal_stage_tablename == f"{fisc_dealunit_str()}{staging_str}"
    assert xp.cash_stage_tablename == f"{fisc_cashbook_str()}{staging_str}"
    assert xp.hour_stage_tablename == f"{fisc_timeline_hour_str()}{staging_str}"
    assert xp.mont_stage_tablename == f"{fisc_timeline_month_str()}{staging_str}"
    assert xp.week_stage_tablename == f"{fisc_timeline_weekday_str()}{staging_str}"
    assert xp.offi_stage_tablename == f"{fisc_timeoffi_str()}{staging_str}"
    assert xp.unit_agg_csv_filename == f"{xp.unit_agg_tablename}.csv"
    assert xp.deal_agg_csv_filename == f"{xp.deal_agg_tablename}.csv"
    assert xp.cash_agg_csv_filename == f"{xp.cash_agg_tablename}.csv"
    assert xp.hour_agg_csv_filename == f"{xp.hour_agg_tablename}.csv"
    assert xp.mont_agg_csv_filename == f"{xp.mont_agg_tablename}.csv"
    assert xp.week_agg_csv_filename == f"{xp.week_agg_tablename}.csv"
    assert xp.offi_agg_csv_filename == f"{xp.offi_agg_tablename}.csv"
    assert xp.unit_stage_csv_filename == f"{xp.unit_stage_tablename}.csv"
    assert xp.deal_stage_csv_filename == f"{xp.deal_stage_tablename}.csv"
    assert xp.cash_stage_csv_filename == f"{xp.cash_stage_tablename}.csv"
    assert xp.hour_stage_csv_filename == f"{xp.hour_stage_tablename}.csv"
    assert xp.mont_stage_csv_filename == f"{xp.mont_stage_tablename}.csv"
    assert xp.week_stage_csv_filename == f"{xp.week_stage_tablename}.csv"
    assert xp.offi_stage_csv_filename == f"{xp.offi_stage_tablename}.csv"
    assert xp.unit_agg_csv_path == create_path(x_dir, xp.unit_agg_csv_filename)
    assert xp.deal_agg_csv_path == create_path(x_dir, xp.deal_agg_csv_filename)
    assert xp.cash_agg_csv_path == create_path(x_dir, xp.cash_agg_csv_filename)
    assert xp.hour_agg_csv_path == create_path(x_dir, xp.hour_agg_csv_filename)
    assert xp.mont_agg_csv_path == create_path(x_dir, xp.mont_agg_csv_filename)
    assert xp.week_agg_csv_path == create_path(x_dir, xp.week_agg_csv_filename)
    assert xp.offi_agg_csv_path == create_path(x_dir, xp.offi_agg_csv_filename)
    assert xp.unit_stage_csv_path == create_path(x_dir, xp.unit_stage_csv_filename)
    assert xp.deal_stage_csv_path == create_path(x_dir, xp.deal_stage_csv_filename)
    assert xp.cash_stage_csv_path == create_path(x_dir, xp.cash_stage_csv_filename)
    assert xp.hour_stage_csv_path == create_path(x_dir, xp.hour_stage_csv_filename)
    assert xp.mont_stage_csv_path == create_path(x_dir, xp.mont_stage_csv_filename)
    assert xp.week_stage_csv_path == create_path(x_dir, xp.week_stage_csv_filename)
    assert xp.offi_stage_csv_path == create_path(x_dir, xp.offi_stage_csv_filename)
    assert xp.unit_excel_filename == f"{fiscunit_str()}.xlsx"
    assert xp.deal_excel_filename == f"{fisc_dealunit_str()}.xlsx"
    assert xp.cash_excel_filename == f"{fisc_cashbook_str()}.xlsx"
    assert xp.hour_excel_filename == f"{fisc_timeline_hour_str()}.xlsx"
    assert xp.mont_excel_filename == f"{fisc_timeline_month_str()}.xlsx"
    assert xp.week_excel_filename == f"{fisc_timeline_weekday_str()}.xlsx"
    assert xp.offi_excel_filename == f"{fisc_timeoffi_str()}.xlsx"
    assert xp.unit_excel_path == create_path(x_dir, xp.unit_excel_filename)
    assert xp.deal_excel_path == create_path(x_dir, xp.deal_excel_filename)
    assert xp.cash_excel_path == create_path(x_dir, xp.cash_excel_filename)
    assert xp.hour_excel_path == create_path(x_dir, xp.hour_excel_filename)
    assert xp.mont_excel_path == create_path(x_dir, xp.mont_excel_filename)
    assert xp.week_excel_path == create_path(x_dir, xp.week_excel_filename)
    assert xp.offi_excel_path == create_path(x_dir, xp.offi_excel_filename)


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
    offi_args = set(get_fisc_config_args(fisc_timeoffi_str()).keys())
    print(f"           {fisc_cols.cash_agg_columns=}")
    print(f"{get_default_sorted_list(list(cash_args))=}")
    assert fisc_cols.unit_agg_columns == get_default_sorted_list(unit_args)
    assert fisc_cols.cash_agg_columns == get_default_sorted_list(cash_args)
    assert fisc_cols.deal_agg_columns == get_default_sorted_list(deal_args)
    assert fisc_cols.hour_agg_columns == get_default_sorted_list(hour_args)
    assert fisc_cols.mont_agg_columns == get_default_sorted_list(mont_args)
    assert fisc_cols.week_agg_columns == get_default_sorted_list(week_args)
    assert fisc_cols.offi_agg_columns == get_default_sorted_list(offi_args)

    staging_args = {"idea_number", face_name_str(), event_int_str(), "error_message"}
    unit_staging_args = unit_args.union(staging_args)
    cash_staging_args = cash_args.union(staging_args)
    deal_staging_args = deal_args.union(staging_args)
    hour_staging_args = hour_args.union(staging_args)
    mont_staging_args = mont_args.union(staging_args)
    week_staging_args = week_args.union(staging_args)
    offi_staging_args = offi_args.union(staging_args)
    assert fisc_cols.unit_staging_columns == get_default_sorted_list(unit_staging_args)
    assert fisc_cols.cash_staging_columns == get_default_sorted_list(cash_staging_args)
    assert fisc_cols.deal_staging_columns == get_default_sorted_list(deal_staging_args)
    assert fisc_cols.hour_staging_columns == get_default_sorted_list(hour_staging_args)
    assert fisc_cols.mont_staging_columns == get_default_sorted_list(mont_staging_args)
    assert fisc_cols.week_staging_columns == get_default_sorted_list(week_staging_args)
    assert fisc_cols.offi_staging_columns == get_default_sorted_list(offi_staging_args)

    # unit_staging_csv_header = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}"""
    unit_staging_csv_header = ",".join(fisc_cols.unit_staging_columns)
    deal_staging_csv_header = ",".join(fisc_cols.deal_staging_columns)
    cash_staging_csv_header = ",".join(fisc_cols.cash_staging_columns)
    hour_staging_csv_header = ",".join(fisc_cols.hour_staging_columns)
    mont_staging_csv_header = ",".join(fisc_cols.mont_staging_columns)
    week_staging_csv_header = ",".join(fisc_cols.week_staging_columns)
    offi_staging_csv_header = ",".join(fisc_cols.offi_staging_columns)

    assert fisc_cols.unit_staging_csv_header == unit_staging_csv_header
    assert fisc_cols.deal_staging_csv_header == deal_staging_csv_header
    assert fisc_cols.cash_staging_csv_header == cash_staging_csv_header
    assert fisc_cols.hour_staging_csv_header == hour_staging_csv_header
    assert fisc_cols.mont_staging_csv_header == mont_staging_csv_header
    assert fisc_cols.week_staging_csv_header == week_staging_csv_header
    assert fisc_cols.offi_staging_csv_header == offi_staging_csv_header
    unit_agg_csv_header = ",".join(fisc_cols.unit_agg_columns)
    deal_agg_csv_header = ",".join(fisc_cols.deal_agg_columns)
    cash_agg_csv_header = ",".join(fisc_cols.cash_agg_columns)
    hour_agg_csv_header = ",".join(fisc_cols.hour_agg_columns)
    mont_agg_csv_header = ",".join(fisc_cols.mont_agg_columns)
    week_agg_csv_header = ",".join(fisc_cols.week_agg_columns)
    offi_agg_csv_header = ",".join(fisc_cols.offi_agg_columns)

    assert fisc_cols.unit_agg_csv_header == unit_agg_csv_header
    assert fisc_cols.deal_agg_csv_header == deal_agg_csv_header
    assert fisc_cols.cash_agg_csv_header == cash_agg_csv_header
    assert fisc_cols.hour_agg_csv_header == hour_agg_csv_header
    assert fisc_cols.mont_agg_csv_header == mont_agg_csv_header
    assert fisc_cols.week_agg_csv_header == week_agg_csv_header
    assert fisc_cols.offi_agg_csv_header == offi_agg_csv_header
    assert fisc_cols.unit_agg_empty_csv == f"{unit_agg_csv_header}\n"
    assert fisc_cols.deal_agg_empty_csv == f"{deal_agg_csv_header}\n"
    assert fisc_cols.cash_agg_empty_csv == f"{cash_agg_csv_header}\n"
    assert fisc_cols.hour_agg_empty_csv == f"{hour_agg_csv_header}\n"
    assert fisc_cols.mont_agg_empty_csv == f"{mont_agg_csv_header}\n"
    assert fisc_cols.week_agg_empty_csv == f"{week_agg_csv_header}\n"
    assert fisc_cols.offi_agg_empty_csv == f"{offi_agg_csv_header}\n"


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
    assert sheet_exists(fiscref.offi_excel_path, staging_str) is False

    # WHEN
    create_init_fisc_prime_files(x_dir)

    # THEN
    assert sheet_exists(fiscref.unit_excel_path, staging_str)
    assert sheet_exists(fiscref.deal_excel_path, staging_str)
    assert sheet_exists(fiscref.cash_excel_path, staging_str)
    assert sheet_exists(fiscref.hour_excel_path, staging_str)
    assert sheet_exists(fiscref.mont_excel_path, staging_str)
    assert sheet_exists(fiscref.week_excel_path, staging_str)
    assert sheet_exists(fiscref.offi_excel_path, staging_str)


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
    fiscoffi_df = pandas_read_excel(xp.offi_excel_path, sheet_name=staging_str)

    expected_cols = FiscPrimeColumnsRef()
    print(f"{list(fiscunit_df.columns)=}")
    assert list(fiscunit_df.columns) == expected_cols.unit_staging_columns
    assert list(fiscdeal_df.columns) == expected_cols.deal_staging_columns
    assert list(fisccash_df.columns) == expected_cols.cash_staging_columns
    assert list(fischour_df.columns) == expected_cols.hour_staging_columns
    assert list(fiscmont_df.columns) == expected_cols.mont_staging_columns
    assert list(fiscweek_df.columns) == expected_cols.week_staging_columns
    assert list(fiscoffi_df.columns) == expected_cols.offi_staging_columns


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
    assert sheet_exists(xp.offi_excel_path, agg_str) is False

    # WHEN
    create_init_fisc_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.unit_excel_path, agg_str)
    assert sheet_exists(xp.deal_excel_path, agg_str)
    assert sheet_exists(xp.cash_excel_path, agg_str)
    assert sheet_exists(xp.hour_excel_path, agg_str)
    assert sheet_exists(xp.mont_excel_path, agg_str)
    assert sheet_exists(xp.week_excel_path, agg_str)
    assert sheet_exists(xp.offi_excel_path, agg_str)


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
    fiscoffi_df = pandas_read_excel(xp.offi_excel_path, sheet_name=agg_str)

    expected_cols = FiscPrimeColumnsRef()
    print(f"{list(fiscunit_df.columns)=}")
    assert list(fiscunit_df.columns) == expected_cols.unit_agg_columns
    assert list(fiscdeal_df.columns) == expected_cols.deal_agg_columns
    assert list(fisccash_df.columns) == expected_cols.cash_agg_columns
    assert list(fischour_df.columns) == expected_cols.hour_agg_columns
    assert list(fiscmont_df.columns) == expected_cols.mont_agg_columns
    assert list(fiscweek_df.columns) == expected_cols.week_agg_columns
    assert list(fiscoffi_df.columns) == expected_cols.offi_agg_columns
