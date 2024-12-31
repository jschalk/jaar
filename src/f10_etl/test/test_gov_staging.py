from src.f00_instrument.file import create_path, open_file
from src.f01_road.finance_tran import quota_str, time_int_str, bridge_str
from src.f03_chrono.chrono import (
    c400_number_str,
    monthday_distortion_str,
    timeline_idea_str,
    yr1_jan1_offset_str,
    timelineunit_shop,
    create_timeline_config,
)
from src.f04_gift.atom_config import (
    face_name_str,
    gov_idea_str,
    acct_name_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_gov.gov import get_from_json as gov_get_from_json, govunit_shop
from src.f07_gov.gov_config import (
    current_time_str,
    amount_str,
    month_idea_str,
    hour_idea_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_idea_str,
    weekday_order_str,
    gov_cashbook_str,
    gov_deal_episode_str,
    gov_timeline_hour_str as gov_hour_str,
    gov_timeline_month_str as gov_month_str,
    gov_timeline_weekday_str as gov_weekday_str,
    govunit_str,
    get_gov_config_args,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_brick.pandas_tool import sheet_exists, upsert_sheet
from src.f10_etl.gov_agg import (
    GovPrimeFilePaths,
    GovPrimeColumns,
    create_init_gov_prime_files,
    create_govunit_jsons_from_prime_files,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from copy import copy as copy_copy


# br00000 gov_idea c400_number,current_time,fund_coin,monthday_distortion,penny,respect_bit,bridge,timeline_idea,yr1_jan1_offset
# br00001 gov_idea owner_name,acct_name,time_int,quota
# br00002 gov_idea owner_name,acct_name,time_int,amount
# br00003 gov_idea hour_idea,cumlative_minute
# br00004 gov_idea month_idea,cumlative_day
# br00005 gov_idea weekday_idea,weekday_order


def test_GovPrimeFilePaths_Exists():
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    x_govprimefilepaths = GovPrimeFilePaths(x_dir)

    # THEN
    x_govunit_path = create_path(x_dir, "govunit.xlsx")
    x_gov_deal_path = create_path(x_dir, "gov_deal_episode.xlsx")
    x_gov_cashbook_path = create_path(x_dir, "gov_cashbook.xlsx")
    x_gov_hour_path = create_path(x_dir, "gov_timeline_hour.xlsx")
    x_gov_month_path = create_path(x_dir, "gov_timeline_month.xlsx")
    x_gov_weekday_path = create_path(x_dir, "gov_timeline_weekday.xlsx")
    assert x_govprimefilepaths
    assert x_govprimefilepaths.govunit_path == x_govunit_path
    assert x_govprimefilepaths.gov_deal_path == x_gov_deal_path
    assert x_govprimefilepaths.gov_cashbook_path == x_gov_cashbook_path
    assert x_govprimefilepaths.gov_hour_path == x_gov_hour_path
    assert x_govprimefilepaths.gov_month_path == x_gov_month_path
    assert x_govprimefilepaths.gov_weekday_path == x_gov_weekday_path


def test_GovPrimeColumns_Exists():
    # ESTABLISH / WHEN
    x_govprimecolumns = GovPrimeColumns()

    # THEN
    gov_cashbook_args = set(get_gov_config_args(gov_cashbook_str()).keys())
    gov_deal_episode_args = set(get_gov_config_args(gov_deal_episode_str()).keys())
    gov_timeline_hour_args = set(get_gov_config_args(gov_hour_str()).keys())
    gov_timeline_month_args = set(get_gov_config_args(gov_month_str()).keys())
    gov_timeline_weekday_args = set(get_gov_config_args(gov_weekday_str()).keys())
    govunit_args = set(get_gov_config_args(govunit_str()).keys())
    assert set(x_govprimecolumns.gov_cashbook_agg_columns) == gov_cashbook_args
    assert set(x_govprimecolumns.gov_deal_agg_columns) == gov_deal_episode_args
    assert set(x_govprimecolumns.gov_hour_agg_columns) == gov_timeline_hour_args
    assert set(x_govprimecolumns.gov_month_agg_columns) == gov_timeline_month_args
    assert set(x_govprimecolumns.gov_weekday_agg_columns) == gov_timeline_weekday_args
    assert set(x_govprimecolumns.govunit_agg_columns) == govunit_args

    staging_args = {"source_br", face_name_str(), event_int_str(), "note"}
    gov_cashbook_staging = gov_cashbook_args.union(staging_args)
    gov_deal_episode_staging = gov_deal_episode_args.union(staging_args)
    gov_hour_staging = gov_timeline_hour_args.union(staging_args)
    gov_month_staging = gov_timeline_month_args.union(staging_args)
    gov_weekday_staging = gov_timeline_weekday_args.union(staging_args)
    govunit_staging = govunit_args.union(staging_args)

    assert set(x_govprimecolumns.gov_cashbook_staging_columns) == gov_cashbook_staging
    assert set(x_govprimecolumns.gov_deal_staging_columns) == gov_deal_episode_staging
    assert set(x_govprimecolumns.gov_hour_staging_columns) == gov_hour_staging
    assert set(x_govprimecolumns.gov_month_staging_columns) == gov_month_staging
    assert set(x_govprimecolumns.gov_weekday_staging_columns) == gov_weekday_staging
    assert set(x_govprimecolumns.govunit_staging_columns) == govunit_staging


def test_create_init_gov_prime_files_CreatesFiles_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    staging_str = "staging"
    xp = GovPrimeFilePaths(x_dir)
    assert sheet_exists(xp.govunit_path, staging_str) is False
    assert sheet_exists(xp.gov_deal_path, staging_str) is False
    assert sheet_exists(xp.gov_cashbook_path, staging_str) is False
    assert sheet_exists(xp.gov_hour_path, staging_str) is False
    assert sheet_exists(xp.gov_month_path, staging_str) is False
    assert sheet_exists(xp.gov_weekday_path, staging_str) is False

    # WHEN
    create_init_gov_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.govunit_path, staging_str)
    assert sheet_exists(xp.gov_deal_path, staging_str)
    assert sheet_exists(xp.gov_cashbook_path, staging_str)
    assert sheet_exists(xp.gov_hour_path, staging_str)
    assert sheet_exists(xp.gov_month_path, staging_str)
    assert sheet_exists(xp.gov_weekday_path, staging_str)


def test_create_init_gov_prime_files_HasCorrectColumns_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_gov_prime_files(x_dir)

    # THEN
    staging_str = "staging"
    xp = GovPrimeFilePaths(x_dir)
    govunit_df = pandas_read_excel(xp.govunit_path, sheet_name=staging_str)
    gov_deal_df = pandas_read_excel(xp.gov_deal_path, sheet_name=staging_str)
    gov_cashbook_df = pandas_read_excel(xp.gov_cashbook_path, sheet_name=staging_str)
    gov_hour_df = pandas_read_excel(xp.gov_hour_path, sheet_name=staging_str)
    gov_month_df = pandas_read_excel(xp.gov_month_path, sheet_name=staging_str)
    gov_weekday_df = pandas_read_excel(xp.gov_weekday_path, sheet_name=staging_str)

    expected_cols = GovPrimeColumns()
    print(f"{list(govunit_df.columns)=}")
    assert list(govunit_df.columns) == expected_cols.govunit_staging_columns
    assert list(gov_deal_df.columns) == expected_cols.gov_deal_staging_columns
    assert list(gov_cashbook_df.columns) == expected_cols.gov_cashbook_staging_columns
    assert list(gov_hour_df.columns) == expected_cols.gov_hour_staging_columns
    assert list(gov_month_df.columns) == expected_cols.gov_month_staging_columns
    assert list(gov_weekday_df.columns) == expected_cols.gov_weekday_staging_columns


def test_create_init_gov_prime_files_CreatesFiles_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    agg_str = "agg"
    xp = GovPrimeFilePaths(x_dir)
    assert sheet_exists(xp.govunit_path, agg_str) is False
    assert sheet_exists(xp.gov_deal_path, agg_str) is False
    assert sheet_exists(xp.gov_cashbook_path, agg_str) is False
    assert sheet_exists(xp.gov_hour_path, agg_str) is False
    assert sheet_exists(xp.gov_month_path, agg_str) is False
    assert sheet_exists(xp.gov_weekday_path, agg_str) is False

    # WHEN
    create_init_gov_prime_files(x_dir)

    # THEN
    assert sheet_exists(xp.govunit_path, agg_str)
    assert sheet_exists(xp.gov_deal_path, agg_str)
    assert sheet_exists(xp.gov_cashbook_path, agg_str)
    assert sheet_exists(xp.gov_hour_path, agg_str)
    assert sheet_exists(xp.gov_month_path, agg_str)
    assert sheet_exists(xp.gov_weekday_path, agg_str)


def test_create_init_gov_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_gov_prime_files(x_dir)

    # THEN
    agg_str = "agg"
    xp = GovPrimeFilePaths(x_dir)
    govunit_df = pandas_read_excel(xp.govunit_path, sheet_name=agg_str)
    gov_deal_df = pandas_read_excel(xp.gov_deal_path, sheet_name=agg_str)
    gov_cashbook_df = pandas_read_excel(xp.gov_cashbook_path, sheet_name=agg_str)
    gov_hour_df = pandas_read_excel(xp.gov_hour_path, sheet_name=agg_str)
    gov_month_df = pandas_read_excel(xp.gov_month_path, sheet_name=agg_str)
    gov_weekday_df = pandas_read_excel(xp.gov_weekday_path, sheet_name=agg_str)

    expected_cols = GovPrimeColumns()
    print(f"{list(govunit_df.columns)=}")
    assert list(govunit_df.columns) == expected_cols.govunit_agg_columns
    assert list(gov_deal_df.columns) == expected_cols.gov_deal_agg_columns
    assert list(gov_cashbook_df.columns) == expected_cols.gov_cashbook_agg_columns
    assert list(gov_hour_df.columns) == expected_cols.gov_hour_agg_columns
    assert list(gov_month_df.columns) == expected_cols.gov_month_agg_columns
    assert list(gov_weekday_df.columns) == expected_cols.gov_weekday_agg_columns


def test_create_govunit_jsons_from_prime_files_Scenario0_MinimumNecessaryParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea_str = "accord56"
    accord56 = [
        accord56_gov_idea_str,
        "",  # accord56_c400_number_str,
        "",  # accord56_current_time_str,
        "",  # accord56_fund_coin_str,
        "",  # accord56_monthday_distortion_str,
        "",  # accord56_penny_str,
        "",  # accord56_respect_bit_str,
        "",  # accord56_bridge_str,
        "",  # accord56_timeline_idea_str,
        "",  # accord56_yr1_jan1_offset_str,
    ]
    govunit_rows = [accord56]
    govunit_df = DataFrame(govunit_rows, columns=xc.govunit_agg_columns)
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    accord56_govunit.govs_dir = govs_dir
    accord56_govunit._set_gov_dirs()
    assert accord56_govunit
    assert accord56_govunit.gov_idea == accord56_gov_idea_str
    assert accord56_govunit.govs_dir == govs_dir
    expected_govunit = govunit_shop(accord56_gov_idea_str, govs_dir)
    assert accord56_govunit.timeline == expected_govunit.timeline
    assert accord56_govunit == expected_govunit


def test_create_govunit_jsons_from_prime_files_Scenario1_IncludeNoneTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea_str = "accord56"
    accord56_current_time = 77
    accord56_fund_coin = 3
    accord56_penny = 2
    accord56_respect_bit = 55
    accord56_bridge = "/"
    accord56 = [
        accord56_gov_idea_str,
        "",  # accord56_c400_number_str,
        accord56_current_time,
        accord56_fund_coin,
        "",  # accord56_monthday_distortion_str,
        accord56_penny,
        accord56_respect_bit,
        accord56_bridge,
        "",  # accord56_timeline_idea_str,
        "",  # accord56_yr1_jan1_offset_str,
    ]
    govunit_rows = [accord56]
    govunit_df = DataFrame(govunit_rows, columns=xc.govunit_agg_columns)
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    assert accord56_govunit
    assert accord56_govunit.gov_idea == accord56_gov_idea_str
    assert accord56_govunit.current_time == accord56_current_time
    assert accord56_govunit.fund_coin == accord56_fund_coin
    assert accord56_govunit.penny == accord56_penny
    assert accord56_govunit.respect_bit == accord56_respect_bit
    assert accord56_govunit.bridge == accord56_bridge
    default_govunit = govunit_shop(accord56_gov_idea_str)
    assert accord56_govunit.timeline == default_govunit.timeline
    assert accord56_govunit.gov_idea == accord56_gov_idea_str
    assert accord56_govunit.current_time != default_govunit.current_time
    assert accord56_govunit.fund_coin != default_govunit.fund_coin
    assert accord56_govunit.penny != default_govunit.penny
    assert accord56_govunit.respect_bit != default_govunit.respect_bit
    assert accord56_govunit.bridge != default_govunit.bridge
    assert accord56_govunit != default_govunit


def test_create_govunit_jsons_from_prime_files_Scenario2_PartialTimeLineUnitParameters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea = "accord56"
    accord56_c400_number = 9
    accord56_timeline_idea = "timelineX3"
    accord56_yr1_jan1_offset = 555
    accord56 = [
        accord56_gov_idea,
        accord56_c400_number,
        "",  # current_time_str(),
        "",  # fund_coin_str(),
        "",  # monthday_distortion_str(),
        "",  # penny_str(),
        "",  # respect_bit_str(),
        "",  # bridge_str(),
        accord56_timeline_idea,
        accord56_yr1_jan1_offset,
    ]
    govunit_rows = [accord56]
    govunit_df = DataFrame(govunit_rows, columns=xc.govunit_agg_columns)
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    assert accord56_govunit
    assert accord56_govunit.gov_idea == accord56_gov_idea
    expected_timeline_config = create_timeline_config(
        timeline_idea=accord56_timeline_idea,
        c400_count=accord56_c400_number,
        yr1_jan1_offset=accord56_yr1_jan1_offset,
    )
    expected_timelineunit = timelineunit_shop(expected_timeline_config)
    expected_govunit = govunit_shop(accord56_gov_idea, timeline=expected_timelineunit)
    assert accord56_govunit.timeline.timeline_idea == accord56_timeline_idea
    assert accord56_govunit.timeline.c400_number == accord56_c400_number
    assert accord56_govunit.timeline == expected_timelineunit
    assert accord56_govunit.timeline == expected_govunit.timeline
    assert accord56_govunit == expected_govunit


def test_create_govunit_jsons_from_prime_files_Scenario3_gov_timeline_weekday(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea = "accord56"
    accord56_gov_idea
    monday_str = "Monday"
    tuesday_str = "Tuesday"
    accord56_gov_row = [accord56_gov_idea, "", "", "", "", "", "", "", "", ""]
    govunit_df = DataFrame([accord56_gov_row], columns=xc.govunit_agg_columns)
    a56_weekday_t3 = [accord56_gov_idea, monday_str, 3]
    a56_weekday_t7 = [accord56_gov_idea, tuesday_str, 4]
    a56_weekday_rows = [a56_weekday_t3, a56_weekday_t7]
    a56_weekday_df = DataFrame(a56_weekday_rows, columns=xc.gov_weekday_agg_columns)
    print(f"{a56_weekday_df=}")
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    upsert_sheet(xp.gov_weekday_path, agg_str, a56_weekday_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_govunit = govunit_shop(accord56_gov_idea, govs_dir, x_timelineunit)
    expected_govunit.timeline.weekdays_config = [monday_str, tuesday_str]
    print(f"{expected_govunit.timeline.weekdays_config=}")
    assert accord56_govunit.timeline.weekdays_config == [monday_str, tuesday_str]
    assert accord56_govunit.timeline.weekdays_config == x_timelineunit.weekdays_config


def test_create_govunit_jsons_from_prime_files_Scenario4_gov_timeline_month(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea = "accord56"
    accord56_gov_idea
    july_str = "July"
    june_str = "June"
    accord56_gov_row = [accord56_gov_idea, "", "", "", "", "", "", "", "", ""]
    govunit_df = DataFrame([accord56_gov_row], columns=xc.govunit_agg_columns)
    a56_june = [accord56_gov_idea, june_str, 150]
    a56_july = [accord56_gov_idea, july_str, 365]
    a56_month_rows = [a56_july, a56_june]
    a56_month_df = DataFrame(a56_month_rows, columns=xc.gov_month_agg_columns)
    print(f"{a56_month_df=}")
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    upsert_sheet(xp.gov_month_path, agg_str, a56_month_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_govunit = govunit_shop(accord56_gov_idea, govs_dir, x_timelineunit)
    expected_govunit.timeline.months_config = [[june_str, 150], [july_str, 365]]
    print(f"{expected_govunit.timeline.months_config=}")
    assert accord56_govunit.timeline.months_config == [
        [june_str, 150],
        [july_str, 365],
    ]
    assert accord56_govunit.timeline.months_config == x_timelineunit.months_config


def test_create_govunit_jsons_from_prime_files_Scenario5_gov_timeline_hour(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea = "accord56"
    accord56_gov_idea
    a56_0hr = "0hour"
    a56_5hr = "5hour"
    a56_8hr = "8hour"
    accord56_gov_row = [accord56_gov_idea, "", "", "", "", "", "", "", "", ""]
    govunit_df = DataFrame([accord56_gov_row], columns=xc.govunit_agg_columns)
    a56_0hour_row = [accord56_gov_idea, a56_0hr, 60]
    a56_5hour_row = [accord56_gov_idea, a56_5hr, 500]
    a56_8hour_row = [accord56_gov_idea, a56_8hr, 1440]
    a56_hour_rows = [a56_0hour_row, a56_5hour_row, a56_8hour_row]
    a56_hour_df = DataFrame(a56_hour_rows, columns=xc.gov_hour_agg_columns)
    print(f"{a56_hour_df=}")
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    upsert_sheet(xp.gov_hour_path, agg_str, a56_hour_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_govunit = govunit_shop(accord56_gov_idea, govs_dir, x_timelineunit)
    expected_hour_config = [[a56_0hr, 60], [a56_5hr, 500], [a56_8hr, 1440]]
    expected_govunit.timeline.hours_config = expected_hour_config
    print(f"{expected_govunit.timeline.hours_config=}")
    assert accord56_govunit.timeline.hours_config == expected_hour_config
    assert accord56_govunit.timeline.hours_config == x_timelineunit.hours_config


def test_create_govunit_jsons_from_prime_files_Scenario6_gov_cashbook(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    t3 = 3
    t7 = 7
    amount3 = 555
    amount7 = 777
    accord56_gov_row = [accord56_gov_idea, "", "", "", "", "", "", "", "", ""]
    govunit_df = DataFrame([accord56_gov_row], columns=xc.govunit_agg_columns)
    a56_cashbook_t3 = [accord56_gov_idea, sue_str, bob_str, t3, amount3]
    a56_cashbook_t7 = [accord56_gov_idea, sue_str, bob_str, t7, amount7]
    a56_cashbook_rows = [a56_cashbook_t3, a56_cashbook_t7]
    gov_cashbook_df = DataFrame(a56_cashbook_rows, columns=xc.gov_cashbook_agg_columns)
    # print(f"{gov_cashbook_df=}")
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    upsert_sheet(xp.gov_cashbook_path, agg_str, gov_cashbook_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_govunit = govunit_shop(accord56_gov_idea, govs_dir, x_timelineunit)
    expected_govunit.add_cashpurchase(sue_str, bob_str, t3, amount3)
    expected_govunit.add_cashpurchase(sue_str, bob_str, t7, amount7)
    print(f"{expected_govunit.cashbook=}")
    print(f"{accord56_govunit.cashbook=}")
    # print(f"{accord56_govunit=}")
    assert accord56_govunit.cashbook == expected_govunit.cashbook


def test_create_govunit_jsons_from_prime_files_Scenario7_gov_deal_episode(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    govs_dir = create_path(get_test_etl_dir(), "govs")
    create_init_gov_prime_files(govs_dir)
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    agg_str = "agg"
    accord56_gov_idea = "accord56"
    accord56_gov_idea
    sue_str = "Sue"
    t3 = 3
    t7 = 7
    quota3 = 555
    quota7 = 777
    accord56_gov_row = [accord56_gov_idea, "", "", "", "", "", "", "", "", ""]
    govunit_df = DataFrame([accord56_gov_row], columns=xc.govunit_agg_columns)
    a56_deal_t3 = [accord56_gov_idea, sue_str, t3, quota3]
    a56_deal_t7 = [accord56_gov_idea, sue_str, t7, quota7]
    a56_deal_rows = [a56_deal_t3, a56_deal_t7]
    gov_deal_df = DataFrame(a56_deal_rows, columns=xc.gov_deal_agg_columns)
    print(f"{gov_deal_df=}")
    upsert_sheet(xp.govunit_path, agg_str, govunit_df)
    upsert_sheet(xp.gov_deal_path, agg_str, gov_deal_df)
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    accord56_json_path = create_path(gov_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_json_path) is False

    # WHEN
    create_govunit_jsons_from_prime_files(govs_dir=govs_dir)

    # THEN
    assert os_path_exists(accord56_json_path)
    accord56_govunit = gov_get_from_json(open_file(accord56_json_path))
    x_timelineunit = timelineunit_shop(create_timeline_config())
    expected_govunit = govunit_shop(accord56_gov_idea, govs_dir, x_timelineunit)
    expected_govunit.add_dealepisode(sue_str, t3, quota3)
    expected_govunit.add_dealepisode(sue_str, t7, quota7)
    print(f"{expected_govunit.deallogs=}")
    print(f"{expected_govunit=}")
    assert accord56_govunit.deallogs == expected_govunit.deallogs


# def test_create_govunit_jsons_from_prime_files_Scenario4_gov_cashbook(env_dir_setup_cleanup):
# def test_create_govunit_jsons_from_prime_files_Scenario5_gov_timeline_hour(env_dir_setup_cleanup):
# def test_create_govunit_jsons_from_prime_files_Scenario6_gov_timeline_month(env_dir_setup_cleanup):
# def test_create_govunit_jsons_from_prime_files_Scenario7_gov_timeline_weekday(env_dir_setup_cleanup):


# def test_WorldUnit_boat_agg_to_pidgin_staging_CreatesFile(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     ukx = "Unknown"
#     m_str = "accord23"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     br00113_file_path = create_path(fizz_world._boat_dir, "br00113.xlsx")
#     br00113_columns = [
#         face_name_str(),
#         event_int_str(),
#         gov_idea_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_name_str(),
#         inx_name_str(),
#     ]
#     br00043_file_path = create_path(fizz_world._boat_dir, "br00043.xlsx")
#     br00043_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_name_str(),
#         inx_name_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00113_rows = [sue0, sue1]
#     br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
#     upsert_sheet(br00113_file_path, boat_agg_str(), br00113_df)
#     br00043_df = [sue2, sue3, yao1]
#     br00043_df = DataFrame(br00043_df, columns=br00043_columns)
#     upsert_sheet(br00043_file_path, boat_agg_str(), br00043_df)
#     pidgin_path = create_path(fizz_world._boat_dir, "pidgin.xlsx")

#     br00115_file_path = create_path(fizz_world._boat_dir, "br00115.xlsx")
#     br00115_columns = [
#         face_name_str(),
#         event_int_str(),
#         gov_idea_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_label_str(),
#         inx_label_str(),
#     ]
#     br00042_file_path = create_path(fizz_world._boat_dir, "br00042.xlsx")
#     br00042_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_label_str(),
#         inx_label_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00115_rows = [sue0, sue1]
#     br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
#     upsert_sheet(br00115_file_path, boat_agg_str(), br00115_df)
#     b40_rows = [sue2, sue3, yao1]
#     br00042_df = DataFrame(b40_rows, columns=br00042_columns)
#     upsert_sheet(br00042_file_path, boat_agg_str(), br00042_df)

#     br00116_file_path = create_path(fizz_world._boat_dir, "br00116.xlsx")
#     br00116_columns = [
#         face_name_str(),
#         event_int_str(),
#         gov_idea_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_idea_str(),
#         inx_idea_str(),
#     ]
#     br00044_file_path = create_path(fizz_world._boat_dir, "br00044.xlsx")
#     br00044_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_idea_str(),
#         inx_idea_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00116_rows = [sue0, sue1]
#     br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
#     upsert_sheet(br00116_file_path, boat_agg_str(), br00116_df)
#     br00044_rows = [sue2, sue3, yao1]
#     br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
#     upsert_sheet(br00044_file_path, boat_agg_str(), br00044_df)

#     br00117_file_path = create_path(fizz_world._boat_dir, "br00117.xlsx")
#     br00117_columns = [
#         face_name_str(),
#         event_int_str(),
#         gov_idea_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     br00045_file_path = create_path(fizz_world._boat_dir, "br00045.xlsx")
#     br00045_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     b117_rows = [sue0, sue1]
#     br00117_df = DataFrame(b117_rows, columns=br00117_columns)
#     upsert_sheet(br00117_file_path, boat_agg_str(), br00117_df)
#     br00045_rows = [sue2, sue3, yao1]
#     br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
#     upsert_sheet(br00045_file_path, boat_agg_str(), br00045_df)

#     assert fizz_world.events == {}
#     fizz_world.boat_agg_to_boat_events()
#     fizz_world.boat_events_to_events_log()
#     fizz_world.boat_events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg_file()
#     assert fizz_world.events == {event2: sue_str, event5: sue_str}
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.boat_agg_to_pidgin_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     group_staging_str = "group_staging"
#     acct_staging_str = "acct_staging"
#     idea_staging_str = "idea_staging"
#     road_staging_str = "road_staging"
#     assert sheet_exists(pidgin_path, acct_staging_str)
#     assert sheet_exists(pidgin_path, group_staging_str)
#     assert sheet_exists(pidgin_path, idea_staging_str)
#     assert sheet_exists(pidgin_path, road_staging_str)

#     gen_group_df = pandas_read_excel(pidgin_path, sheet_name=group_staging_str)
#     gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
#     gen_idea_df = pandas_read_excel(pidgin_path, sheet_name=idea_staging_str)
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)

#     group_file_columns = [
#         "src_brick",
#         face_name_str(),
#         event_int_str(),
#         otx_label_str(),
#         inx_label_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_group_df.columns) == group_file_columns
#     assert len(gen_group_df) == 2
#     b3 = "br00115"
#     b4 = "br00042"
#     e1_group3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_group4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_group_rows = [e1_group3, e1_group4]
#     e1_group_df = DataFrame(e1_group_rows, columns=group_file_columns)
#     assert len(gen_group_df) == len(e1_group_df)
#     print(f"{gen_group_df.to_csv()=}")
#     print(f" {e1_group_df.to_csv()=}")
#     assert gen_group_df.to_csv(index=False) == e1_group_df.to_csv(index=False)

#     acct_file_columns = [
#         "src_brick",
#         face_name_str(),
#         event_int_str(),
#         otx_name_str(),
#         inx_name_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_acct_df.columns) == acct_file_columns
#     assert len(gen_acct_df) == 2
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_acct3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_acct4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_acct_rows = [e1_acct3, e1_acct4]
#     e1_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
#     assert len(gen_acct_df) == len(e1_acct_df)
#     print(f"{gen_acct_df.to_csv()=}")
#     print(f" {e1_acct_df.to_csv()=}")
#     assert gen_acct_df.to_csv(index=False) == e1_acct_df.to_csv(index=False)

#     idea_file_columns = [
#         "src_brick",
#         face_name_str(),
#         event_int_str(),
#         otx_idea_str(),
#         inx_idea_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_idea_df.columns) == idea_file_columns
#     assert len(gen_idea_df) == 2
#     b3 = "br00116"
#     b4 = "br00044"
#     e1_idea3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_idea4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_idea_rows = [e1_idea3, e1_idea4]
#     e1_idea_df = DataFrame(e1_idea_rows, columns=idea_file_columns)
#     assert len(gen_idea_df) == len(e1_idea_df)
#     print(f"{gen_idea_df.to_csv()=}")
#     print(f" {e1_idea_df.to_csv()=}")
#     assert gen_idea_df.to_csv(index=False) == e1_idea_df.to_csv(index=False)

#     road_file_columns = [
#         "src_brick",
#         face_name_str(),
#         event_int_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_road_df.columns) == road_file_columns
#     assert len(gen_road_df) == 2
#     b3 = "br00117"
#     b4 = "br00045"
#     e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_road_rows = [e1_road3, e1_road4]
#     e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     assert len(gen_road_df) == len(e1_road_df)
#     print(f"{gen_road_df.to_csv()=}")
#     print(f" {e1_road_df.to_csv()=}")
#     assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)


# from src.f00_instrument.file import create_path
# from src.f04_gift.atom_config import face_name_str, gov_idea_str
# from src.f07_gov.gov_config import cumlative_minute_str, hour_idea_str
# from src.f08_pidgin.pidgin_config import event_int_str
# from src.f09_brick.pandas_tool import upsert_sheet, sheet_exists
# from src.f11_world.world import worldunit_shop
# from src.f11_world.examples.world_env import env_dir_setup_cleanup
# from pandas.testing import (
#     assert_frame_equal as pandas_assert_frame_equal,
# )
# from pandas import DataFrame, read_excel as pandas_read_excel


# def test_WorldUnit_aft_face_bricks_to_aft_event_bricks_CreatesFaceBrickSheets_Scenario0_MultpleFaceNames(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     zia_str = "Zia"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     brick_columns = [
#         face_name_str(),
#         event_int_str(),
#         gov_idea_str(),
#         hour_idea_str(),
#         cumlative_minute_str(),
#     ]
#     accord23_str = "accord23"
#     sue0 = [sue_str, event3, accord23_str, hour6am, minute_360]
#     sue1 = [sue_str, event3, accord23_str, hour7am, minute_420]
#     zia0 = [zia_str, event7, accord23_str, hour7am, minute_420]
#     zia1 = [zia_str, event9, accord23_str, hour6am, minute_360]
#     zia2 = [zia_str, event9, accord23_str, hour7am, minute_420]
#     example_sue_df = DataFrame([sue0, sue1], columns=brick_columns)
#     example_zia_df = DataFrame([zia0, zia1, zia2], columns=brick_columns)
#     fizz_world = worldunit_shop("fizz")
#     br00003_filename = "br00003.xlsx"
#     sue_dir = create_path(fizz_world._faces_aft_dir, sue_str)
#     zia_dir = create_path(fizz_world._faces_aft_dir, zia_str)
#     sue_br00003_filepath = create_path(sue_dir, br00003_filename)
#     zia_br00003_filepath = create_path(zia_dir, br00003_filename)
#     upsert_sheet(sue_br00003_filepath, "inx", example_sue_df)
#     upsert_sheet(zia_br00003_filepath, "inx", example_zia_df)

#     event3_dir = create_path(sue_dir, event3)
#     event7_dir = create_path(zia_dir, event7)
#     event9_dir = create_path(zia_dir, event9)
#     event3_br00003_filepath = create_path(event3_dir, br00003_filename)
#     event7_br00003_filepath = create_path(event7_dir, br00003_filename)
#     event9_br00003_filepath = create_path(event9_dir, br00003_filename)
#     assert sheet_exists(event3_br00003_filepath, "inx") is False
#     assert sheet_exists(event7_br00003_filepath, "inx") is False
#     assert sheet_exists(event9_br00003_filepath, "inx") is False

#     # WHEN
#     fizz_world.aft_face_bricks_to_aft_event_bricks()

#     # THEN
#     assert sheet_exists(event3_br00003_filepath, "inx")
#     assert sheet_exists(event7_br00003_filepath, "inx")
#     assert sheet_exists(event9_br00003_filepath, "inx")
#     gen_event3_df = pandas_read_excel(event3_br00003_filepath, "inx")
#     gen_event7_df = pandas_read_excel(event7_br00003_filepath, "inx")
#     gen_event9_df = pandas_read_excel(event9_br00003_filepath, "inx")
#     example_event3_df = DataFrame([sue0, sue1], columns=brick_columns)
#     example_event7_df = DataFrame([zia0], columns=brick_columns)
#     example_event9_df = DataFrame([zia1, zia2], columns=brick_columns)
#     pandas_assert_frame_equal(gen_event3_df, example_event3_df)
#     pandas_assert_frame_equal(gen_event7_df, example_event7_df)
#     pandas_assert_frame_equal(gen_event9_df, example_event9_df)
