from src.a00_data_toolbox.file_toolbox import create_path
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import (
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
)
from src.a15_fisc_logic.fisc_config import get_fisc_config_args
from src.a17_creed_logic.creed_db_tool import get_default_sorted_list
from src.a18_etl_toolbox.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
    # create_init_fisc_prime_files,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)


def test_FiscPrimeObjsRef_Exists():
    # ESTABLISH
    x_dir = get_module_temp_dir()

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
    raw_str = "_raw"
    assert xp.unit_raw_tablename == f"{fiscunit_str()}{raw_str}"
    assert xp.deal_raw_tablename == f"{fisc_dealunit_str()}{raw_str}"
    assert xp.cash_raw_tablename == f"{fisc_cashbook_str()}{raw_str}"
    assert xp.hour_raw_tablename == f"{fisc_timeline_hour_str()}{raw_str}"
    assert xp.mont_raw_tablename == f"{fisc_timeline_month_str()}{raw_str}"
    assert xp.week_raw_tablename == f"{fisc_timeline_weekday_str()}{raw_str}"
    assert xp.offi_raw_tablename == f"{fisc_timeoffi_str()}{raw_str}"
    assert xp.unit_agg_csv_filename == f"{xp.unit_agg_tablename}.csv"
    assert xp.deal_agg_csv_filename == f"{xp.deal_agg_tablename}.csv"
    assert xp.cash_agg_csv_filename == f"{xp.cash_agg_tablename}.csv"
    assert xp.hour_agg_csv_filename == f"{xp.hour_agg_tablename}.csv"
    assert xp.mont_agg_csv_filename == f"{xp.mont_agg_tablename}.csv"
    assert xp.week_agg_csv_filename == f"{xp.week_agg_tablename}.csv"
    assert xp.offi_agg_csv_filename == f"{xp.offi_agg_tablename}.csv"
    assert xp.unit_raw_csv_filename == f"{xp.unit_raw_tablename}.csv"
    assert xp.deal_raw_csv_filename == f"{xp.deal_raw_tablename}.csv"
    assert xp.cash_raw_csv_filename == f"{xp.cash_raw_tablename}.csv"
    assert xp.hour_raw_csv_filename == f"{xp.hour_raw_tablename}.csv"
    assert xp.mont_raw_csv_filename == f"{xp.mont_raw_tablename}.csv"
    assert xp.week_raw_csv_filename == f"{xp.week_raw_tablename}.csv"
    assert xp.offi_raw_csv_filename == f"{xp.offi_raw_tablename}.csv"
    assert xp.unit_agg_csv_path == create_path(x_dir, xp.unit_agg_csv_filename)
    assert xp.deal_agg_csv_path == create_path(x_dir, xp.deal_agg_csv_filename)
    assert xp.cash_agg_csv_path == create_path(x_dir, xp.cash_agg_csv_filename)
    assert xp.hour_agg_csv_path == create_path(x_dir, xp.hour_agg_csv_filename)
    assert xp.mont_agg_csv_path == create_path(x_dir, xp.mont_agg_csv_filename)
    assert xp.week_agg_csv_path == create_path(x_dir, xp.week_agg_csv_filename)
    assert xp.offi_agg_csv_path == create_path(x_dir, xp.offi_agg_csv_filename)
    assert xp.unit_raw_csv_path == create_path(x_dir, xp.unit_raw_csv_filename)
    assert xp.deal_raw_csv_path == create_path(x_dir, xp.deal_raw_csv_filename)
    assert xp.cash_raw_csv_path == create_path(x_dir, xp.cash_raw_csv_filename)
    assert xp.hour_raw_csv_path == create_path(x_dir, xp.hour_raw_csv_filename)
    assert xp.mont_raw_csv_path == create_path(x_dir, xp.mont_raw_csv_filename)
    assert xp.week_raw_csv_path == create_path(x_dir, xp.week_raw_csv_filename)
    assert xp.offi_raw_csv_path == create_path(x_dir, xp.offi_raw_csv_filename)
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

    raw_args = {"creed_number", face_name_str(), event_int_str(), "error_message"}
    unit_raw_args = unit_args.union(raw_args)
    cash_raw_args = cash_args.union(raw_args)
    deal_raw_args = deal_args.union(raw_args)
    hour_raw_args = hour_args.union(raw_args)
    mont_raw_args = mont_args.union(raw_args)
    week_raw_args = week_args.union(raw_args)
    offi_raw_args = offi_args.union(raw_args)
    assert fisc_cols.unit_raw_columns == get_default_sorted_list(unit_raw_args)
    assert fisc_cols.cash_raw_columns == get_default_sorted_list(cash_raw_args)
    assert fisc_cols.deal_raw_columns == get_default_sorted_list(deal_raw_args)
    assert fisc_cols.hour_raw_columns == get_default_sorted_list(hour_raw_args)
    assert fisc_cols.mont_raw_columns == get_default_sorted_list(mont_raw_args)
    assert fisc_cols.week_raw_columns == get_default_sorted_list(week_raw_args)
    assert fisc_cols.offi_raw_columns == get_default_sorted_list(offi_raw_args)

    # unit_raw_csv_header = f"""{event_int_str()},{face_name_str()},{fisc_word_str()},{owner_name_str()},{acct_name_str()}"""
    unit_raw_csv_header = ",".join(fisc_cols.unit_raw_columns)
    deal_raw_csv_header = ",".join(fisc_cols.deal_raw_columns)
    cash_raw_csv_header = ",".join(fisc_cols.cash_raw_columns)
    hour_raw_csv_header = ",".join(fisc_cols.hour_raw_columns)
    mont_raw_csv_header = ",".join(fisc_cols.mont_raw_columns)
    week_raw_csv_header = ",".join(fisc_cols.week_raw_columns)
    offi_raw_csv_header = ",".join(fisc_cols.offi_raw_columns)

    assert fisc_cols.unit_raw_csv_header == unit_raw_csv_header
    assert fisc_cols.deal_raw_csv_header == deal_raw_csv_header
    assert fisc_cols.cash_raw_csv_header == cash_raw_csv_header
    assert fisc_cols.hour_raw_csv_header == hour_raw_csv_header
    assert fisc_cols.mont_raw_csv_header == mont_raw_csv_header
    assert fisc_cols.week_raw_csv_header == week_raw_csv_header
    assert fisc_cols.offi_raw_csv_header == offi_raw_csv_header
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


# def test_create_init_fisc_prime_files_CreatesFiles_raw(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_dir = get_module_temp_dir()
#     raw_str = "raw"
#     fiscref = FiscPrimeObjsRef(x_dir)
#     assert sheet_exists(fiscref.unit_excel_path, raw_str) is False
#     assert sheet_exists(fiscref.deal_excel_path, raw_str) is False
#     assert sheet_exists(fiscref.cash_excel_path, raw_str) is False
#     assert sheet_exists(fiscref.hour_excel_path, raw_str) is False
#     assert sheet_exists(fiscref.mont_excel_path, raw_str) is False
#     assert sheet_exists(fiscref.week_excel_path, raw_str) is False
#     assert sheet_exists(fiscref.offi_excel_path, raw_str) is False

#     # WHEN
#     create_init_fisc_prime_files(x_dir)

#     # THEN
#     assert sheet_exists(fiscref.unit_excel_path, raw_str)
#     assert sheet_exists(fiscref.deal_excel_path, raw_str)
#     assert sheet_exists(fiscref.cash_excel_path, raw_str)
#     assert sheet_exists(fiscref.hour_excel_path, raw_str)
#     assert sheet_exists(fiscref.mont_excel_path, raw_str)
#     assert sheet_exists(fiscref.week_excel_path, raw_str)
#     assert sheet_exists(fiscref.offi_excel_path, raw_str)


# def test_create_init_fisc_prime_files_HasCorrectColumns_raw(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     x_dir = get_module_temp_dir()

#     # WHEN
#     create_init_fisc_prime_files(x_dir)

#     # THEN
#     raw_str = "raw"
#     xp = FiscPrimeObjsRef(x_dir)
#     fisunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=raw_str)
#     fisdeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=raw_str)
#     fiscash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=raw_str)
#     fishour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=raw_str)
#     fismont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=raw_str)
#     fisweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=raw_str)
#     fisoffi_df = pandas_read_excel(xp.offi_excel_path, sheet_name=raw_str)

#     expected_cols = FiscPrimeColumnsRef()
#     print(f"{list(fisunit_df.columns)=}")
#     assert list(fisunit_df.columns) == expected_cols.unit_raw_columns
#     assert list(fisdeal_df.columns) == expected_cols.deal_raw_columns
#     assert list(fiscash_df.columns) == expected_cols.cash_raw_columns
#     assert list(fishour_df.columns) == expected_cols.hour_raw_columns
#     assert list(fismont_df.columns) == expected_cols.mont_raw_columns
#     assert list(fisweek_df.columns) == expected_cols.week_raw_columns
#     assert list(fisoffi_df.columns) == expected_cols.offi_raw_columns


# def test_create_init_fisc_prime_files_CreatesFiles_agg(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_dir = get_module_temp_dir()
#     agg_str = "agg"
#     xp = FiscPrimeObjsRef(x_dir)
#     assert sheet_exists(xp.unit_excel_path, agg_str) is False
#     assert sheet_exists(xp.deal_excel_path, agg_str) is False
#     assert sheet_exists(xp.cash_excel_path, agg_str) is False
#     assert sheet_exists(xp.hour_excel_path, agg_str) is False
#     assert sheet_exists(xp.mont_excel_path, agg_str) is False
#     assert sheet_exists(xp.week_excel_path, agg_str) is False
#     assert sheet_exists(xp.offi_excel_path, agg_str) is False

#     # WHEN
#     create_init_fisc_prime_files(x_dir)

#     # THEN
#     assert sheet_exists(xp.unit_excel_path, agg_str)
#     assert sheet_exists(xp.deal_excel_path, agg_str)
#     assert sheet_exists(xp.cash_excel_path, agg_str)
#     assert sheet_exists(xp.hour_excel_path, agg_str)
#     assert sheet_exists(xp.mont_excel_path, agg_str)
#     assert sheet_exists(xp.week_excel_path, agg_str)
#     assert sheet_exists(xp.offi_excel_path, agg_str)


# def test_create_init_fisc_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_dir = get_module_temp_dir()

#     # WHEN
#     create_init_fisc_prime_files(x_dir)

#     # THEN
#     agg_str = "agg"
#     xp = FiscPrimeObjsRef(x_dir)
#     fisunit_df = pandas_read_excel(xp.unit_excel_path, sheet_name=agg_str)
#     fisdeal_df = pandas_read_excel(xp.deal_excel_path, sheet_name=agg_str)
#     fiscash_df = pandas_read_excel(xp.cash_excel_path, sheet_name=agg_str)
#     fishour_df = pandas_read_excel(xp.hour_excel_path, sheet_name=agg_str)
#     fismont_df = pandas_read_excel(xp.mont_excel_path, sheet_name=agg_str)
#     fisweek_df = pandas_read_excel(xp.week_excel_path, sheet_name=agg_str)
#     fisoffi_df = pandas_read_excel(xp.offi_excel_path, sheet_name=agg_str)

#     expected_cols = FiscPrimeColumnsRef()
#     print(f"{list(fisunit_df.columns)=}")
#     assert list(fisunit_df.columns) == expected_cols.unit_agg_columns
#     assert list(fisdeal_df.columns) == expected_cols.deal_agg_columns
#     assert list(fiscash_df.columns) == expected_cols.cash_agg_columns
#     assert list(fishour_df.columns) == expected_cols.hour_agg_columns
#     assert list(fismont_df.columns) == expected_cols.mont_agg_columns
#     assert list(fisweek_df.columns) == expected_cols.week_agg_columns
#     assert list(fisoffi_df.columns) == expected_cols.offi_agg_columns
