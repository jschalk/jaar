from src.f00_instrument.file import create_path, open_file
from src.f03_chrono.chrono import timelineunit_shop, timeline_config_shop
from src.f04_gift.atom_config import face_name_str
from src.f07_fiscal.fiscal import get_from_json as fiscal_get_from_json, fiscalunit_shop
from src.f07_fiscal.fiscal_config import (
    fiscal_cashbook_str,
    fiscal_deal_episode_str,
    fiscal_timeline_hour_str as fiscal_hour_str,
    fiscal_timeline_month_str as fiscal_month_str,
    fiscal_timeline_weekday_str as fiscal_weekday_str,
    fiscalunit_str,
    get_fiscal_config_args,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.pandas_tool import sheet_exists, upsert_sheet
from src.f10_etl.fiscal_agg import (
    FiscalPrimeFilePaths,
    FiscalPrimeColumns,
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


def test_FiscalPrimeFilePaths_Exists():
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    x_fiscalprimefilepaths = FiscalPrimeFilePaths(x_dir)

    # THEN
    x_fiscalunit_path = create_path(x_dir, "fiscalunit.xlsx")
    x_fiscal_deal_path = create_path(x_dir, "fiscal_deal_episode.xlsx")
    x_fiscal_cashbook_path = create_path(x_dir, "fiscal_cashbook.xlsx")
    x_fiscal_hour_path = create_path(x_dir, "fiscal_timeline_hour.xlsx")
    x_fiscal_month_path = create_path(x_dir, "fiscal_timeline_month.xlsx")
    x_fiscal_weekday_path = create_path(x_dir, "fiscal_timeline_weekday.xlsx")
    assert x_fiscalprimefilepaths
    assert x_fiscalprimefilepaths.fiscalunit_path == x_fiscalunit_path
    assert x_fiscalprimefilepaths.fiscal_deal_path == x_fiscal_deal_path
    assert x_fiscalprimefilepaths.fiscal_cashbook_path == x_fiscal_cashbook_path
    assert x_fiscalprimefilepaths.fiscal_hour_path == x_fiscal_hour_path
    assert x_fiscalprimefilepaths.fiscal_month_path == x_fiscal_month_path
    assert x_fiscalprimefilepaths.fiscal_weekday_path == x_fiscal_weekday_path


def test_FiscalPrimeColumns_Exists():
    # ESTABLISH / WHEN
    x_fiscalprimecols = FiscalPrimeColumns()

    # THEN
    fiscal_cashbook_args = set(get_fiscal_config_args(fiscal_cashbook_str()).keys())
    fiscal_deal_episode_args = set(
        get_fiscal_config_args(fiscal_deal_episode_str()).keys()
    )
    fiscal_hour_args = set(get_fiscal_config_args(fiscal_hour_str()).keys())
    fiscal_month_args = set(get_fiscal_config_args(fiscal_month_str()).keys())
    fiscal_weekday_args = set(get_fiscal_config_args(fiscal_weekday_str()).keys())
    fiscalunit_args = set(get_fiscal_config_args(fiscalunit_str()).keys())
    assert set(x_fiscalprimecols.fiscal_cashbook_agg_columns) == fiscal_cashbook_args
    assert set(x_fiscalprimecols.fiscal_deal_agg_columns) == fiscal_deal_episode_args
    assert set(x_fiscalprimecols.fiscal_hour_agg_columns) == fiscal_hour_args
    assert set(x_fiscalprimecols.fiscal_month_agg_columns) == fiscal_month_args
    assert set(x_fiscalprimecols.fiscal_weekday_agg_columns) == fiscal_weekday_args
    assert set(x_fiscalprimecols.fiscalunit_agg_columns) == fiscalunit_args

    staging_args = {"source_br", face_name_str(), event_int_str(), "note"}
    fiscal_cashbook_staging = fiscal_cashbook_args.union(staging_args)
    fiscal_deal_episode_staging = fiscal_deal_episode_args.union(staging_args)
    fiscal_hour_staging = fiscal_hour_args.union(staging_args)
    fiscal_month_staging = fiscal_month_args.union(staging_args)
    fiscal_weekday_staging = fiscal_weekday_args.union(staging_args)
    fiscalunit_staging = fiscalunit_args.union(staging_args)
    assert (
        set(x_fiscalprimecols.fiscal_cashbook_staging_columns)
        == fiscal_cashbook_staging
    )
    assert (
        set(x_fiscalprimecols.fiscal_deal_staging_columns)
        == fiscal_deal_episode_staging
    )
    assert set(x_fiscalprimecols.fiscal_hour_staging_columns) == fiscal_hour_staging
    assert set(x_fiscalprimecols.fiscal_month_staging_columns) == fiscal_month_staging
    assert (
        set(x_fiscalprimecols.fiscal_weekday_staging_columns) == fiscal_weekday_staging
    )
    assert set(x_fiscalprimecols.fiscalunit_staging_columns) == fiscalunit_staging


def test_create_init_fiscal_prime_files_CreatesFiles_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    staging_str = "staging"
    xp = FiscalPrimeFilePaths(x_dir)
    assert sheet_exists(xp.fiscalunit_path, staging_str) is False
    assert sheet_exists(xp.fiscal_deal_path, staging_str) is False
    assert sheet_exists(xp.fiscal_cashbook_path, staging_str) is False
    assert sheet_exists(xp.fiscal_hour_path, staging_str) is False
    assert sheet_exists(xp.fiscal_month_path, staging_str) is False
    assert sheet_exists(xp.fiscal_weekday_path, staging_str) is False

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.fiscalunit_path, staging_str)
    assert sheet_exists(xp.fiscal_deal_path, staging_str)
    assert sheet_exists(xp.fiscal_cashbook_path, staging_str)
    assert sheet_exists(xp.fiscal_hour_path, staging_str)
    assert sheet_exists(xp.fiscal_month_path, staging_str)
    assert sheet_exists(xp.fiscal_weekday_path, staging_str)


def test_create_init_fiscal_prime_files_HasCorrectColumns_staging(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    staging_str = "staging"
    xp = FiscalPrimeFilePaths(x_dir)
    fiscalunit_df = pandas_read_excel(xp.fiscalunit_path, sheet_name=staging_str)
    fiscal_deal_df = pandas_read_excel(xp.fiscal_deal_path, sheet_name=staging_str)
    fiscal_cashbook_df = pandas_read_excel(
        xp.fiscal_cashbook_path, sheet_name=staging_str
    )
    fiscal_hour_df = pandas_read_excel(xp.fiscal_hour_path, sheet_name=staging_str)
    fiscal_month_df = pandas_read_excel(xp.fiscal_month_path, sheet_name=staging_str)
    fiscal_weekday_df = pandas_read_excel(
        xp.fiscal_weekday_path, sheet_name=staging_str
    )

    expected_cols = FiscalPrimeColumns()
    print(f"{list(fiscalunit_df.columns)=}")
    assert list(fiscalunit_df.columns) == expected_cols.fiscalunit_staging_columns
    assert list(fiscal_deal_df.columns) == expected_cols.fiscal_deal_staging_columns
    assert (
        list(fiscal_cashbook_df.columns)
        == expected_cols.fiscal_cashbook_staging_columns
    )
    assert list(fiscal_hour_df.columns) == expected_cols.fiscal_hour_staging_columns
    assert list(fiscal_month_df.columns) == expected_cols.fiscal_month_staging_columns
    assert (
        list(fiscal_weekday_df.columns) == expected_cols.fiscal_weekday_staging_columns
    )


def test_create_init_fiscal_prime_files_CreatesFiles_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    agg_str = "agg"
    xp = FiscalPrimeFilePaths(x_dir)
    assert sheet_exists(xp.fiscalunit_path, agg_str) is False
    assert sheet_exists(xp.fiscal_deal_path, agg_str) is False
    assert sheet_exists(xp.fiscal_cashbook_path, agg_str) is False
    assert sheet_exists(xp.fiscal_hour_path, agg_str) is False
    assert sheet_exists(xp.fiscal_month_path, agg_str) is False
    assert sheet_exists(xp.fiscal_weekday_path, agg_str) is False

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.fiscalunit_path, agg_str)
    assert sheet_exists(xp.fiscal_deal_path, agg_str)
    assert sheet_exists(xp.fiscal_cashbook_path, agg_str)
    assert sheet_exists(xp.fiscal_hour_path, agg_str)
    assert sheet_exists(xp.fiscal_month_path, agg_str)
    assert sheet_exists(xp.fiscal_weekday_path, agg_str)


def test_create_init_fiscal_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_fiscal_prime_files(x_dir)

    # THEN
    agg_str = "agg"
    xp = FiscalPrimeFilePaths(x_dir)
    fiscalunit_df = pandas_read_excel(xp.fiscalunit_path, sheet_name=agg_str)
    fiscal_deal_df = pandas_read_excel(xp.fiscal_deal_path, sheet_name=agg_str)
    fiscal_cashbook_df = pandas_read_excel(xp.fiscal_cashbook_path, sheet_name=agg_str)
    fiscal_hour_df = pandas_read_excel(xp.fiscal_hour_path, sheet_name=agg_str)
    fiscal_month_df = pandas_read_excel(xp.fiscal_month_path, sheet_name=agg_str)
    fiscal_weekday_df = pandas_read_excel(xp.fiscal_weekday_path, sheet_name=agg_str)

    expected_cols = FiscalPrimeColumns()
    print(f"{list(fiscalunit_df.columns)=}")
    assert list(fiscalunit_df.columns) == expected_cols.fiscalunit_agg_columns
    assert list(fiscal_deal_df.columns) == expected_cols.fiscal_deal_agg_columns
    assert list(fiscal_cashbook_df.columns) == expected_cols.fiscal_cashbook_agg_columns
    assert list(fiscal_hour_df.columns) == expected_cols.fiscal_hour_agg_columns
    assert list(fiscal_month_df.columns) == expected_cols.fiscal_month_agg_columns
    assert list(fiscal_weekday_df.columns) == expected_cols.fiscal_weekday_agg_columns


def test_create_fiscalunit_jsons_from_prime_files_Scenario0_MinimumNecessaryParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fiscal_mstr_dir = create_path(get_test_etl_dir(), "fiscal_mstr")
    create_init_fiscal_prime_files(fiscal_mstr_dir)
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
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
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.fiscalunit_agg_columns)
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
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
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
    agg_str = "agg"
    accord56_fiscal_title_str = "accord56"
    accord56_current_time = 77
    accord56_fund_coin = 3
    accord56_penny = 2
    accord56_respect_bit = 55
    accord56_bridge = "/"
    accord56 = [
        accord56_fiscal_title_str,
        "",  # accord56_c400_number_str,
        accord56_current_time,
        accord56_fund_coin,
        "",  # accord56_monthday_distortion_str,
        accord56_penny,
        accord56_respect_bit,
        accord56_bridge,
        "",  # accord56_timeline_title_str,
        "",  # accord56_yr1_jan1_offset_str,
    ]
    fiscalunit_rows = [accord56]
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.fiscalunit_agg_columns)
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
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
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_c400_number = 9
    accord56_monthday_distortion = 7
    accord56_timeline_title = "timelineX3"
    accord56_yr1_jan1_offset = 555
    accord56 = [
        accord56_fiscal_title,
        accord56_c400_number,
        "",  # current_time_str(),
        "",  # fund_coin_str(),
        accord56_monthday_distortion,
        "",  # penny_str(),
        "",  # respect_bit_str(),
        "",  # bridge_str(),
        accord56_timeline_title,
        accord56_yr1_jan1_offset,
    ]
    fiscalunit_rows = [accord56]
    fiscalunit_df = DataFrame(fiscalunit_rows, columns=xc.fiscalunit_agg_columns)
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
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
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    monday_str = "Monday"
    tuesday_str = "Tuesday"
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.fiscalunit_agg_columns)
    a56_weekday_t3 = [accord56_fiscal_title, monday_str, 3]
    a56_weekday_t7 = [accord56_fiscal_title, tuesday_str, 4]
    a56_weekday_rows = [a56_weekday_t3, a56_weekday_t7]
    a56_weekday_df = DataFrame(a56_weekday_rows, columns=xc.fiscal_weekday_agg_columns)
    print(f"{a56_weekday_df=}")
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.fiscal_weekday_path, agg_str, a56_weekday_df)
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
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    july_str = "July"
    june_str = "June"
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.fiscalunit_agg_columns)
    a56_june = [accord56_fiscal_title, june_str, 150]
    a56_july = [accord56_fiscal_title, july_str, 365]
    a56_month_rows = [a56_july, a56_june]
    a56_month_df = DataFrame(a56_month_rows, columns=xc.fiscal_month_agg_columns)
    print(f"{a56_month_df=}")
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.fiscal_month_path, agg_str, a56_month_df)
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
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    a56_0hr = "0hour"
    a56_5hr = "5hour"
    a56_8hr = "8hour"
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.fiscalunit_agg_columns)
    a56_0hour_row = [accord56_fiscal_title, a56_0hr, 60]
    a56_5hour_row = [accord56_fiscal_title, a56_5hr, 500]
    a56_8hour_row = [accord56_fiscal_title, a56_8hr, 1440]
    a56_hour_rows = [a56_0hour_row, a56_5hour_row, a56_8hour_row]
    a56_hour_df = DataFrame(a56_hour_rows, columns=xc.fiscal_hour_agg_columns)
    print(f"{a56_hour_df=}")
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.fiscal_hour_path, agg_str, a56_hour_df)
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
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    t3 = 3
    t7 = 7
    amount3 = 555
    amount7 = 777
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.fiscalunit_agg_columns)
    a56_cashbook_t3 = [accord56_fiscal_title, sue_str, bob_str, t3, amount3]
    a56_cashbook_t7 = [accord56_fiscal_title, sue_str, bob_str, t7, amount7]
    a56_cashbook_rows = [a56_cashbook_t3, a56_cashbook_t7]
    fiscal_cashbook_df = DataFrame(
        a56_cashbook_rows, columns=xc.fiscal_cashbook_agg_columns
    )
    # print(f"{fiscal_cashbook_df=}")
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.fiscal_cashbook_path, agg_str, fiscal_cashbook_df)
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
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    xc = FiscalPrimeColumns()
    agg_str = "agg"
    accord56_fiscal_title = "accord56"
    accord56_fiscal_title
    sue_str = "Sue"
    t3 = 3
    t7 = 7
    quota3 = 555
    quota7 = 777
    accord56_fiscal_row = [accord56_fiscal_title, "", "", "", "", "", "", "", "", ""]
    fiscalunit_df = DataFrame([accord56_fiscal_row], columns=xc.fiscalunit_agg_columns)
    a56_deal_t3 = [accord56_fiscal_title, sue_str, t3, quota3]
    a56_deal_t7 = [accord56_fiscal_title, sue_str, t7, quota7]
    a56_deal_rows = [a56_deal_t3, a56_deal_t7]
    fiscal_deal_df = DataFrame(a56_deal_rows, columns=xc.fiscal_deal_agg_columns)
    print(f"{fiscal_deal_df=}")
    upsert_sheet(xp.fiscalunit_path, agg_str, fiscalunit_df)
    upsert_sheet(xp.fiscal_deal_path, agg_str, fiscal_deal_df)
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
