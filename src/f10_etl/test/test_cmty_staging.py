from src.f00_instrument.file import create_path, open_file
from src.f03_chrono.chrono import timelineunit_shop, create_timeline_config
from src.f04_gift.atom_config import face_name_str
from src.f07_cmty.cmty import get_from_json as cmty_get_from_json, cmtyunit_shop
from src.f07_cmty.cmty_config import (
    cmty_cashbook_str,
    cmty_deal_episode_str,
    cmty_timeline_hour_str as cmty_hour_str,
    cmty_timeline_month_str as cmty_month_str,
    cmty_timeline_weekday_str as cmty_weekday_str,
    cmtyunit_str,
    get_cmty_config_args,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.pandas_tool import sheet_exists, upsert_sheet
from src.f10_etl.cmty_agg import (
    CmtyPrimeFilePaths,
    CmtyPrimeColumns,
    create_init_cmty_prime_files,
    create_cmtyunit_jsons_from_prime_files,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


# br00000 cmty_title c400_number,current_time,fund_coin,monthday_distortion,penny,respect_bit,bridge,timeline_title,yr1_jan1_offset
# br00001 cmty_title owner_name,acct_name,time_int,quota
# br00002 cmty_title owner_name,acct_name,time_int,amount
# br00003 cmty_title hour_title,cumlative_minute
# br00004 cmty_title month_title,cumlative_day
# br00005 cmty_title weekday_title,weekday_order


def test_CmtyPrimeFilePaths_Exists():
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    x_cmtyprimefilepaths = CmtyPrimeFilePaths(x_dir)

    # THEN
    x_cmtyunit_path = create_path(x_dir, "cmtyunit.xlsx")
    x_cmty_deal_path = create_path(x_dir, "cmty_deal_episode.xlsx")
    x_cmty_cashbook_path = create_path(x_dir, "cmty_cashbook.xlsx")
    x_cmty_hour_path = create_path(x_dir, "cmty_timeline_hour.xlsx")
    x_cmty_month_path = create_path(x_dir, "cmty_timeline_month.xlsx")
    x_cmty_weekday_path = create_path(x_dir, "cmty_timeline_weekday.xlsx")
    assert x_cmtyprimefilepaths
    assert x_cmtyprimefilepaths.cmtyunit_path == x_cmtyunit_path
    assert x_cmtyprimefilepaths.cmty_deal_path == x_cmty_deal_path
    assert x_cmtyprimefilepaths.cmty_cashbook_path == x_cmty_cashbook_path
    assert x_cmtyprimefilepaths.cmty_hour_path == x_cmty_hour_path
    assert x_cmtyprimefilepaths.cmty_month_path == x_cmty_month_path
    assert x_cmtyprimefilepaths.cmty_weekday_path == x_cmty_weekday_path


def test_CmtyPrimeColumns_Exists():
    # ESTABLISH / WHEN
    x_cmtyprimecols = CmtyPrimeColumns()

    # THEN
    cmty_cashbook_args = set(get_cmty_config_args(cmty_cashbook_str()).keys())
    cmty_deal_episode_args = set(get_cmty_config_args(cmty_deal_episode_str()).keys())
    cmty_hour_args = set(get_cmty_config_args(cmty_hour_str()).keys())
    cmty_month_args = set(get_cmty_config_args(cmty_month_str()).keys())
    cmty_weekday_args = set(get_cmty_config_args(cmty_weekday_str()).keys())
    cmtyunit_args = set(get_cmty_config_args(cmtyunit_str()).keys())
    assert set(x_cmtyprimecols.cmty_cashbook_agg_columns) == cmty_cashbook_args
    assert set(x_cmtyprimecols.cmty_deal_agg_columns) == cmty_deal_episode_args
    assert set(x_cmtyprimecols.cmty_hour_agg_columns) == cmty_hour_args
    assert set(x_cmtyprimecols.cmty_month_agg_columns) == cmty_month_args
    assert set(x_cmtyprimecols.cmty_weekday_agg_columns) == cmty_weekday_args
    assert set(x_cmtyprimecols.cmtyunit_agg_columns) == cmtyunit_args

    staging_args = {"source_br", face_name_str(), event_int_str(), "note"}
    cmty_cashbook_staging = cmty_cashbook_args.union(staging_args)
    cmty_deal_episode_staging = cmty_deal_episode_args.union(staging_args)
    cmty_hour_staging = cmty_hour_args.union(staging_args)
    cmty_month_staging = cmty_month_args.union(staging_args)
    cmty_weekday_staging = cmty_weekday_args.union(staging_args)
    cmtyunit_staging = cmtyunit_args.union(staging_args)
    assert set(x_cmtyprimecols.cmty_cashbook_staging_columns) == cmty_cashbook_staging
    assert set(x_cmtyprimecols.cmty_deal_staging_columns) == cmty_deal_episode_staging
    assert set(x_cmtyprimecols.cmty_hour_staging_columns) == cmty_hour_staging
    assert set(x_cmtyprimecols.cmty_month_staging_columns) == cmty_month_staging
    assert set(x_cmtyprimecols.cmty_weekday_staging_columns) == cmty_weekday_staging
    assert set(x_cmtyprimecols.cmtyunit_staging_columns) == cmtyunit_staging


def test_create_init_cmty_prime_files_CreatesFiles_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    staging_str = "staging"
    xp = CmtyPrimeFilePaths(x_dir)
    assert sheet_exists(xp.cmtyunit_path, staging_str) is False
    assert sheet_exists(xp.cmty_deal_path, staging_str) is False
    assert sheet_exists(xp.cmty_cashbook_path, staging_str) is False
    assert sheet_exists(xp.cmty_hour_path, staging_str) is False
    assert sheet_exists(xp.cmty_month_path, staging_str) is False
    assert sheet_exists(xp.cmty_weekday_path, staging_str) is False

    # WHEN
    create_init_cmty_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.cmtyunit_path, staging_str)
    assert sheet_exists(xp.cmty_deal_path, staging_str)
    assert sheet_exists(xp.cmty_cashbook_path, staging_str)
    assert sheet_exists(xp.cmty_hour_path, staging_str)
    assert sheet_exists(xp.cmty_month_path, staging_str)
    assert sheet_exists(xp.cmty_weekday_path, staging_str)


def test_create_init_cmty_prime_files_HasCorrectColumns_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_cmty_prime_files(x_dir)

    # THEN
    staging_str = "staging"
    xp = CmtyPrimeFilePaths(x_dir)
    cmtyunit_df = pandas_read_excel(xp.cmtyunit_path, sheet_name=staging_str)
    cmty_deal_df = pandas_read_excel(xp.cmty_deal_path, sheet_name=staging_str)
    cmty_cashbook_df = pandas_read_excel(xp.cmty_cashbook_path, sheet_name=staging_str)
    cmty_hour_df = pandas_read_excel(xp.cmty_hour_path, sheet_name=staging_str)
    cmty_month_df = pandas_read_excel(xp.cmty_month_path, sheet_name=staging_str)
    cmty_weekday_df = pandas_read_excel(xp.cmty_weekday_path, sheet_name=staging_str)

    expected_cols = CmtyPrimeColumns()
    print(f"{list(cmtyunit_df.columns)=}")
    assert list(cmtyunit_df.columns) == expected_cols.cmtyunit_staging_columns
    assert list(cmty_deal_df.columns) == expected_cols.cmty_deal_staging_columns
    assert list(cmty_cashbook_df.columns) == expected_cols.cmty_cashbook_staging_columns
    assert list(cmty_hour_df.columns) == expected_cols.cmty_hour_staging_columns
    assert list(cmty_month_df.columns) == expected_cols.cmty_month_staging_columns
    assert list(cmty_weekday_df.columns) == expected_cols.cmty_weekday_staging_columns


def test_create_init_cmty_prime_files_CreatesFiles_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    agg_str = "agg"
    xp = CmtyPrimeFilePaths(x_dir)
    assert sheet_exists(xp.cmtyunit_path, agg_str) is False
    assert sheet_exists(xp.cmty_deal_path, agg_str) is False
    assert sheet_exists(xp.cmty_cashbook_path, agg_str) is False
    assert sheet_exists(xp.cmty_hour_path, agg_str) is False
    assert sheet_exists(xp.cmty_month_path, agg_str) is False
    assert sheet_exists(xp.cmty_weekday_path, agg_str) is False

    # WHEN
    create_init_cmty_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.cmtyunit_path, agg_str)
    assert sheet_exists(xp.cmty_deal_path, agg_str)
    assert sheet_exists(xp.cmty_cashbook_path, agg_str)
    assert sheet_exists(xp.cmty_hour_path, agg_str)
    assert sheet_exists(xp.cmty_month_path, agg_str)
    assert sheet_exists(xp.cmty_weekday_path, agg_str)


def test_create_init_cmty_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_cmty_prime_files(x_dir)

    # THEN
    agg_str = "agg"
    xp = CmtyPrimeFilePaths(x_dir)
    cmtyunit_df = pandas_read_excel(xp.cmtyunit_path, sheet_name=agg_str)
    cmty_deal_df = pandas_read_excel(xp.cmty_deal_path, sheet_name=agg_str)
    cmty_cashbook_df = pandas_read_excel(xp.cmty_cashbook_path, sheet_name=agg_str)
    cmty_hour_df = pandas_read_excel(xp.cmty_hour_path, sheet_name=agg_str)
    cmty_month_df = pandas_read_excel(xp.cmty_month_path, sheet_name=agg_str)
    cmty_weekday_df = pandas_read_excel(xp.cmty_weekday_path, sheet_name=agg_str)

    expected_cols = CmtyPrimeColumns()
    print(f"{list(cmtyunit_df.columns)=}")
    assert list(cmtyunit_df.columns) == expected_cols.cmtyunit_agg_columns
    assert list(cmty_deal_df.columns) == expected_cols.cmty_deal_agg_columns
    assert list(cmty_cashbook_df.columns) == expected_cols.cmty_cashbook_agg_columns
    assert list(cmty_hour_df.columns) == expected_cols.cmty_hour_agg_columns
    assert list(cmty_month_df.columns) == expected_cols.cmty_month_agg_columns
    assert list(cmty_weekday_df.columns) == expected_cols.cmty_weekday_agg_columns


def test_create_cmtyunit_jsons_from_prime_files_Scenario0_MinimumNecessaryParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title_str = "accord56"
    accord56 = [
        accord56_cmty_title_str,
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
    cmtyunit_rows = [accord56]
    cmtyunit_df = DataFrame(cmtyunit_rows, columns=xc.cmtyunit_agg_columns)
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    accord56_cmtyunit.cmtys_dir = cmty_mstr_dir
    accord56_cmtyunit._set_cmty_dirs()
    assert accord56_cmtyunit
    assert accord56_cmtyunit.cmty_title == accord56_cmty_title_str
    assert accord56_cmtyunit.cmtys_dir == cmty_mstr_dir
    expected_cmtyunit = cmtyunit_shop(accord56_cmty_title_str, cmty_mstr_dir)
    assert accord56_cmtyunit.timeline == expected_cmtyunit.timeline
    assert accord56_cmtyunit == expected_cmtyunit


def test_create_cmtyunit_jsons_from_prime_files_Scenario1_IncludeNoneTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title_str = "accord56"
    accord56_current_time = 77
    accord56_fund_coin = 3
    accord56_penny = 2
    accord56_respect_bit = 55
    accord56_bridge = "/"
    accord56 = [
        accord56_cmty_title_str,
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
    cmtyunit_rows = [accord56]
    cmtyunit_df = DataFrame(cmtyunit_rows, columns=xc.cmtyunit_agg_columns)
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    assert accord56_cmtyunit
    assert accord56_cmtyunit.cmty_title == accord56_cmty_title_str
    assert accord56_cmtyunit.current_time == accord56_current_time
    assert accord56_cmtyunit.fund_coin == accord56_fund_coin
    assert accord56_cmtyunit.penny == accord56_penny
    assert accord56_cmtyunit.respect_bit == accord56_respect_bit
    assert accord56_cmtyunit.bridge == accord56_bridge
    default_cmtyunit = cmtyunit_shop(accord56_cmty_title_str)
    assert accord56_cmtyunit.timeline == default_cmtyunit.timeline
    assert accord56_cmtyunit.cmty_title == accord56_cmty_title_str
    assert accord56_cmtyunit.current_time != default_cmtyunit.current_time
    assert accord56_cmtyunit.fund_coin != default_cmtyunit.fund_coin
    assert accord56_cmtyunit.penny != default_cmtyunit.penny
    assert accord56_cmtyunit.respect_bit != default_cmtyunit.respect_bit
    assert accord56_cmtyunit.bridge != default_cmtyunit.bridge
    assert accord56_cmtyunit != default_cmtyunit


def test_create_cmtyunit_jsons_from_prime_files_Scenario2_PartialTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title = "accord56"
    accord56_c400_number = 9
    accord56_timeline_title = "timelineX3"
    accord56_yr1_jan1_offset = 555
    accord56 = [
        accord56_cmty_title,
        accord56_c400_number,
        "",  # current_time_str(),
        "",  # fund_coin_str(),
        "",  # monthday_distortion_str(),
        "",  # penny_str(),
        "",  # respect_bit_str(),
        "",  # bridge_str(),
        accord56_timeline_title,
        accord56_yr1_jan1_offset,
    ]
    cmtyunit_rows = [accord56]
    cmtyunit_df = DataFrame(cmtyunit_rows, columns=xc.cmtyunit_agg_columns)
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    assert accord56_cmtyunit
    assert accord56_cmtyunit.cmty_title == accord56_cmty_title
    expected_timeline_config = create_timeline_config(
        timeline_title=accord56_timeline_title,
        c400_count=accord56_c400_number,
        yr1_jan1_offset=accord56_yr1_jan1_offset,
    )
    expected_timelineunit = timelineunit_shop(expected_timeline_config)
    expected_cmtyunit = cmtyunit_shop(
        accord56_cmty_title, timeline=expected_timelineunit
    )
    assert accord56_cmtyunit.timeline.timeline_title == accord56_timeline_title
    assert accord56_cmtyunit.timeline.c400_number == accord56_c400_number
    assert accord56_cmtyunit.timeline == expected_timelineunit
    assert accord56_cmtyunit.timeline == expected_cmtyunit.timeline
    assert accord56_cmtyunit == expected_cmtyunit


def test_create_cmtyunit_jsons_from_prime_files_Scenario3_cmty_timeline_weekday(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title = "accord56"
    accord56_cmty_title
    monday_str = "Monday"
    tuesday_str = "Tuesday"
    accord56_cmty_row = [accord56_cmty_title, "", "", "", "", "", "", "", "", ""]
    cmtyunit_df = DataFrame([accord56_cmty_row], columns=xc.cmtyunit_agg_columns)
    a56_weekday_t3 = [accord56_cmty_title, monday_str, 3]
    a56_weekday_t7 = [accord56_cmty_title, tuesday_str, 4]
    a56_weekday_rows = [a56_weekday_t3, a56_weekday_t7]
    a56_weekday_df = DataFrame(a56_weekday_rows, columns=xc.cmty_weekday_agg_columns)
    print(f"{a56_weekday_df=}")
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    upsert_sheet(xp.cmty_weekday_path, agg_str, a56_weekday_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_cmtyunit = cmtyunit_shop(
        accord56_cmty_title, cmty_mstr_dir, x_timelineunit
    )
    expected_cmtyunit.timeline.weekdays_config = [monday_str, tuesday_str]
    print(f"{expected_cmtyunit.timeline.weekdays_config=}")
    assert accord56_cmtyunit.timeline.weekdays_config == [monday_str, tuesday_str]
    assert accord56_cmtyunit.timeline.weekdays_config == x_timelineunit.weekdays_config


def test_create_cmtyunit_jsons_from_prime_files_Scenario4_cmty_timeline_month(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title = "accord56"
    accord56_cmty_title
    july_str = "July"
    june_str = "June"
    accord56_cmty_row = [accord56_cmty_title, "", "", "", "", "", "", "", "", ""]
    cmtyunit_df = DataFrame([accord56_cmty_row], columns=xc.cmtyunit_agg_columns)
    a56_june = [accord56_cmty_title, june_str, 150]
    a56_july = [accord56_cmty_title, july_str, 365]
    a56_month_rows = [a56_july, a56_june]
    a56_month_df = DataFrame(a56_month_rows, columns=xc.cmty_month_agg_columns)
    print(f"{a56_month_df=}")
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    upsert_sheet(xp.cmty_month_path, agg_str, a56_month_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_cmtyunit = cmtyunit_shop(
        accord56_cmty_title, cmty_mstr_dir, x_timelineunit
    )
    expected_cmtyunit.timeline.months_config = [[june_str, 150], [july_str, 365]]
    print(f"{expected_cmtyunit.timeline.months_config=}")
    assert accord56_cmtyunit.timeline.months_config == [
        [june_str, 150],
        [july_str, 365],
    ]
    assert accord56_cmtyunit.timeline.months_config == x_timelineunit.months_config


def test_create_cmtyunit_jsons_from_prime_files_Scenario5_cmty_timeline_hour(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title = "accord56"
    accord56_cmty_title
    a56_0hr = "0hour"
    a56_5hr = "5hour"
    a56_8hr = "8hour"
    accord56_cmty_row = [accord56_cmty_title, "", "", "", "", "", "", "", "", ""]
    cmtyunit_df = DataFrame([accord56_cmty_row], columns=xc.cmtyunit_agg_columns)
    a56_0hour_row = [accord56_cmty_title, a56_0hr, 60]
    a56_5hour_row = [accord56_cmty_title, a56_5hr, 500]
    a56_8hour_row = [accord56_cmty_title, a56_8hr, 1440]
    a56_hour_rows = [a56_0hour_row, a56_5hour_row, a56_8hour_row]
    a56_hour_df = DataFrame(a56_hour_rows, columns=xc.cmty_hour_agg_columns)
    print(f"{a56_hour_df=}")
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    upsert_sheet(xp.cmty_hour_path, agg_str, a56_hour_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_cmtyunit = cmtyunit_shop(
        accord56_cmty_title, cmty_mstr_dir, x_timelineunit
    )
    expected_hour_config = [[a56_0hr, 60], [a56_5hr, 500], [a56_8hr, 1440]]
    expected_cmtyunit.timeline.hours_config = expected_hour_config
    print(f"{expected_cmtyunit.timeline.hours_config=}")
    assert accord56_cmtyunit.timeline.hours_config == expected_hour_config
    assert accord56_cmtyunit.timeline.hours_config == x_timelineunit.hours_config


def test_create_cmtyunit_jsons_from_prime_files_Scenario6_cmty_cashbook(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    t3 = 3
    t7 = 7
    amount3 = 555
    amount7 = 777
    accord56_cmty_row = [accord56_cmty_title, "", "", "", "", "", "", "", "", ""]
    cmtyunit_df = DataFrame([accord56_cmty_row], columns=xc.cmtyunit_agg_columns)
    a56_cashbook_t3 = [accord56_cmty_title, sue_str, bob_str, t3, amount3]
    a56_cashbook_t7 = [accord56_cmty_title, sue_str, bob_str, t7, amount7]
    a56_cashbook_rows = [a56_cashbook_t3, a56_cashbook_t7]
    cmty_cashbook_df = DataFrame(
        a56_cashbook_rows, columns=xc.cmty_cashbook_agg_columns
    )
    # print(f"{cmty_cashbook_df=}")
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    upsert_sheet(xp.cmty_cashbook_path, agg_str, cmty_cashbook_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_cmtyunit = cmtyunit_shop(
        accord56_cmty_title, cmty_mstr_dir, x_timelineunit
    )
    expected_cmtyunit.add_cashpurchase(sue_str, bob_str, t3, amount3)
    expected_cmtyunit.add_cashpurchase(sue_str, bob_str, t7, amount7)
    print(f"{expected_cmtyunit.cashbook=}")
    print(f"{accord56_cmtyunit.cashbook=}")
    # print(f"{accord56_cmtyunit=}")
    assert accord56_cmtyunit.cashbook == expected_cmtyunit.cashbook


def test_create_cmtyunit_jsons_from_prime_files_Scenario7_cmty_deal_episode(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cmty_mstr_dir = create_path(get_test_etl_dir(), "cmty_mstr")
    create_init_cmty_prime_files(cmty_mstr_dir)
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    xc = CmtyPrimeColumns()
    agg_str = "agg"
    accord56_cmty_title = "accord56"
    accord56_cmty_title
    sue_str = "Sue"
    t3 = 3
    t7 = 7
    quota3 = 555
    quota7 = 777
    accord56_cmty_row = [accord56_cmty_title, "", "", "", "", "", "", "", "", ""]
    cmtyunit_df = DataFrame([accord56_cmty_row], columns=xc.cmtyunit_agg_columns)
    a56_deal_t3 = [accord56_cmty_title, sue_str, t3, quota3]
    a56_deal_t7 = [accord56_cmty_title, sue_str, t7, quota7]
    a56_deal_rows = [a56_deal_t3, a56_deal_t7]
    cmty_deal_df = DataFrame(a56_deal_rows, columns=xc.cmty_deal_agg_columns)
    print(f"{cmty_deal_df=}")
    upsert_sheet(xp.cmtyunit_path, agg_str, cmtyunit_df)
    upsert_sheet(xp.cmty_deal_path, agg_str, cmty_deal_df)
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    accord56_dir = create_path(cmtys_dir, "accord56")
    accord56_json_path = create_path(accord56_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_cmtyunit = cmty_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_cmtyunit = cmtyunit_shop(
        accord56_cmty_title, cmty_mstr_dir, x_timelineunit
    )
    expected_cmtyunit.add_dealepisode(sue_str, t3, quota3)
    expected_cmtyunit.add_dealepisode(sue_str, t7, quota7)
    print(f"{expected_cmtyunit.deallogs=}")
    print(f"{expected_cmtyunit=}")
    assert accord56_cmtyunit.deallogs == expected_cmtyunit.deallogs
