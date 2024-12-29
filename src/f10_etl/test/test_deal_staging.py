from src.f00_instrument.file import create_path, open_file
from src.f01_road.finance_tran import quota_str, time_int_str, bridge_str
from src.f03_chrono.chrono import (
    c400_number_str,
    monthday_distortion_str,
    timeline_idea_str,
    yr1_jan1_offset_str,
)
from src.f04_gift.atom_config import (
    face_name_str,
    deal_idea_str,
    acct_name_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_deal.deal import get_from_json as deal_get_from_json, dealunit_shop
from src.f07_deal.deal_config import (
    current_time_str,
    amount_str,
    month_idea_str,
    hour_idea_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_idea_str,
    weekday_order_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_brick.pandas_tool import sheet_exists, upsert_sheet
from src.f10_etl.deal_agg import (
    create_init_deal_prime_files,
    create_dealunit_jsons_from_prime_files,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from copy import copy as copy_copy

# _get_deal_brick_format_filenames == {
#     "br00000.xlsx",dealunit_str
#     "br00001.xlsx",deal_purviewlog_str
#     "br00002.xlsx",deal_cashbook_str
#     "br00003.xlsx",deal_hour_str
#     "br00004.xlsx",deal_month_str
#     "br00005.xlsx",deal_weekday_str
#     "br00042.xlsx",
# }

# br00000 deal_idea c400_number,current_time,fund_coin,monthday_distortion,penny,respect_bit,bridge,timeline_idea,yr1_jan1_offset
# br00001 deal_idea owner_name,acct_name,time_int,quota
# br00002 deal_idea owner_name,acct_name,time_int,amount
# br00003 deal_idea hour_idea,cumlative_minute
# br00004 deal_idea month_idea,cumlative_day
# br00005 deal_idea weekday_idea,weekday_order


def test_create_init_deal_prime_files_CreatesFiles_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    staging_str = "staging"
    dealunit_path = create_path(x_dir, "dealunit.xlsx")
    deal_purview_path = create_path(x_dir, "deal_purview_episode.xlsx")
    deal_cashbook_path = create_path(x_dir, "deal_cashbook.xlsx")
    deal_hour_path = create_path(x_dir, "deal_timeline_hour.xlsx")
    deal_month_path = create_path(x_dir, "deal_timeline_month.xlsx")
    deal_weekday_path = create_path(x_dir, "deal_timeline_weekday.xlsx")
    assert sheet_exists(dealunit_path, staging_str) is False
    assert sheet_exists(deal_purview_path, staging_str) is False
    assert sheet_exists(deal_cashbook_path, staging_str) is False
    assert sheet_exists(deal_hour_path, staging_str) is False
    assert sheet_exists(deal_month_path, staging_str) is False
    assert sheet_exists(deal_weekday_path, staging_str) is False

    # WHEN
    create_init_deal_prime_files(x_dir)

    # THEN
    assert sheet_exists(dealunit_path, staging_str)
    assert sheet_exists(deal_purview_path, staging_str)
    assert sheet_exists(deal_cashbook_path, staging_str)
    assert sheet_exists(deal_hour_path, staging_str)
    assert sheet_exists(deal_month_path, staging_str)
    assert sheet_exists(deal_weekday_path, staging_str)


def test_create_init_deal_prime_files_HasCorrectColumns_staging(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_deal_prime_files(x_dir)

    # THEN
    staging_str = "staging"
    dealunit_path = create_path(x_dir, "dealunit.xlsx")
    deal_purview_path = create_path(x_dir, "deal_purview_episode.xlsx")
    deal_cashbook_path = create_path(x_dir, "deal_cashbook.xlsx")
    deal_hour_path = create_path(x_dir, "deal_timeline_hour.xlsx")
    deal_month_path = create_path(x_dir, "deal_timeline_month.xlsx")
    deal_weekday_path = create_path(x_dir, "deal_timeline_weekday.xlsx")

    dealunit_df = pandas_read_excel(dealunit_path, sheet_name=staging_str)
    deal_purview_df = pandas_read_excel(deal_purview_path, sheet_name=staging_str)
    deal_cashbook_df = pandas_read_excel(deal_cashbook_path, sheet_name=staging_str)
    deal_hour_df = pandas_read_excel(deal_hour_path, sheet_name=staging_str)
    deal_month_df = pandas_read_excel(deal_month_path, sheet_name=staging_str)
    deal_weekday_df = pandas_read_excel(deal_weekday_path, sheet_name=staging_str)

    common_cols = ["source_br", face_name_str(), event_int_str(), deal_idea_str()]
    expected_dealunit_columns = copy_copy(common_cols)
    expected_deal_purview_columns = copy_copy(common_cols)
    expected_deal_cashbook_columns = copy_copy(common_cols)
    expected_deal_hour_columns = copy_copy(common_cols)
    expected_deal_month_columns = copy_copy(common_cols)
    expected_deal_weekday_columns = copy_copy(common_cols)
    expected_dealunit_columns.extend(
        [
            c400_number_str(),
            current_time_str(),
            fund_coin_str(),
            monthday_distortion_str(),
            penny_str(),
            respect_bit_str(),
            bridge_str(),
            timeline_idea_str(),
            yr1_jan1_offset_str(),
        ]
    )
    expected_deal_purview_columns.extend(
        [owner_name_str(), acct_name_str(), time_int_str(), quota_str()]
    )
    expected_deal_cashbook_columns.extend(
        [owner_name_str(), acct_name_str(), time_int_str(), amount_str()]
    )
    expected_deal_hour_columns.extend([hour_idea_str(), cumlative_minute_str()])
    expected_deal_month_columns.extend([month_idea_str(), cumlative_day_str()])
    expected_deal_weekday_columns.extend([weekday_idea_str(), weekday_order_str()])

    note_column = ["note"]
    expected_dealunit_columns.extend(note_column)
    expected_deal_purview_columns.extend(note_column)
    expected_deal_cashbook_columns.extend(note_column)
    expected_deal_hour_columns.extend(note_column)
    expected_deal_month_columns.extend(note_column)
    expected_deal_weekday_columns.extend(note_column)

    print(f"{list(dealunit_df.columns)=}")
    assert list(dealunit_df.columns) == expected_dealunit_columns
    assert list(deal_purview_df.columns) == expected_deal_purview_columns
    assert list(deal_cashbook_df.columns) == expected_deal_cashbook_columns
    assert list(deal_hour_df.columns) == expected_deal_hour_columns
    assert list(deal_month_df.columns) == expected_deal_month_columns
    assert list(deal_weekday_df.columns) == expected_deal_weekday_columns


def test_create_init_deal_prime_files_CreatesFiles_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()
    agg_str = "agg"
    dealunit_path = create_path(x_dir, "dealunit.xlsx")
    deal_purview_path = create_path(x_dir, "deal_purview_episode.xlsx")
    deal_cashbook_path = create_path(x_dir, "deal_cashbook.xlsx")
    deal_hour_path = create_path(x_dir, "deal_timeline_hour.xlsx")
    deal_month_path = create_path(x_dir, "deal_timeline_month.xlsx")
    deal_weekday_path = create_path(x_dir, "deal_timeline_weekday.xlsx")
    assert sheet_exists(dealunit_path, agg_str) is False
    assert sheet_exists(deal_purview_path, agg_str) is False
    assert sheet_exists(deal_cashbook_path, agg_str) is False
    assert sheet_exists(deal_hour_path, agg_str) is False
    assert sheet_exists(deal_month_path, agg_str) is False
    assert sheet_exists(deal_weekday_path, agg_str) is False

    # WHEN
    create_init_deal_prime_files(x_dir)

    # THEN
    assert sheet_exists(dealunit_path, agg_str)
    assert sheet_exists(deal_purview_path, agg_str)
    assert sheet_exists(deal_cashbook_path, agg_str)
    assert sheet_exists(deal_hour_path, agg_str)
    assert sheet_exists(deal_month_path, agg_str)
    assert sheet_exists(deal_weekday_path, agg_str)


def test_create_init_deal_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_etl_dir()

    # WHEN
    create_init_deal_prime_files(x_dir)

    # THEN
    agg_str = "agg"
    dealunit_path = create_path(x_dir, "dealunit.xlsx")
    deal_purview_path = create_path(x_dir, "deal_purview_episode.xlsx")
    deal_cashbook_path = create_path(x_dir, "deal_cashbook.xlsx")
    deal_hour_path = create_path(x_dir, "deal_timeline_hour.xlsx")
    deal_month_path = create_path(x_dir, "deal_timeline_month.xlsx")
    deal_weekday_path = create_path(x_dir, "deal_timeline_weekday.xlsx")

    dealunit_df = pandas_read_excel(dealunit_path, sheet_name=agg_str)
    deal_purview_df = pandas_read_excel(deal_purview_path, sheet_name=agg_str)
    deal_cashbook_df = pandas_read_excel(deal_cashbook_path, sheet_name=agg_str)
    deal_hour_df = pandas_read_excel(deal_hour_path, sheet_name=agg_str)
    deal_month_df = pandas_read_excel(deal_month_path, sheet_name=agg_str)
    deal_weekday_df = pandas_read_excel(deal_weekday_path, sheet_name=agg_str)

    common_cols = [deal_idea_str()]
    expected_dealunit_columns = copy_copy(common_cols)
    expected_deal_purview_columns = copy_copy(common_cols)
    expected_deal_cashbook_columns = copy_copy(common_cols)
    expected_deal_hour_columns = copy_copy(common_cols)
    expected_deal_month_columns = copy_copy(common_cols)
    expected_deal_weekday_columns = copy_copy(common_cols)
    expected_dealunit_columns.extend(
        [
            c400_number_str(),
            current_time_str(),
            fund_coin_str(),
            monthday_distortion_str(),
            penny_str(),
            respect_bit_str(),
            bridge_str(),
            timeline_idea_str(),
            yr1_jan1_offset_str(),
        ]
    )
    expected_deal_purview_columns.extend(
        [owner_name_str(), acct_name_str(), time_int_str(), quota_str()]
    )
    expected_deal_cashbook_columns.extend(
        [owner_name_str(), acct_name_str(), time_int_str(), amount_str()]
    )
    expected_deal_hour_columns.extend([hour_idea_str(), cumlative_minute_str()])
    expected_deal_month_columns.extend([month_idea_str(), cumlative_day_str()])
    expected_deal_weekday_columns.extend([weekday_idea_str(), weekday_order_str()])

    print(f"{list(dealunit_df.columns)=}")
    assert list(dealunit_df.columns) == expected_dealunit_columns
    assert list(deal_purview_df.columns) == expected_deal_purview_columns
    assert list(deal_cashbook_df.columns) == expected_deal_cashbook_columns
    assert list(deal_hour_df.columns) == expected_deal_hour_columns
    assert list(deal_month_df.columns) == expected_deal_month_columns
    assert list(deal_weekday_df.columns) == expected_deal_weekday_columns


def test_create_init_deal_prime_files_HasCorrectColumns_agg(env_dir_setup_cleanup):
    # ESTABLISH
    deals_dir = create_path(get_test_etl_dir(), "deals")
    create_init_deal_prime_files(deals_dir)
    agg_str = "agg"
    dealunit_path = create_path(deals_dir, "dealunit.xlsx")
    dealunit_columns = [
        deal_idea_str(),
        c400_number_str(),
        current_time_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        timeline_idea_str(),
        yr1_jan1_offset_str(),
    ]
    accord56_deal_idea_str = "accord56"
    accord56 = [
        accord56_deal_idea_str,
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
    dealunit_rows = [accord56]
    dealunit_df = DataFrame(dealunit_rows, columns=dealunit_columns)
    upsert_sheet(dealunit_path, agg_str, dealunit_df)
    deal_jsons_dir = create_path(deals_dir, "deal_jsons")
    accord56_path = create_path(deal_jsons_dir, "accord56.json")
    assert os_path_exists(accord56_path) is False

    # WHEN
    create_dealunit_jsons_from_prime_files(deals_dir=deals_dir)

    # THEN
    assert os_path_exists(accord56_path)
    accord56_dealunit = deal_get_from_json(open_file(accord56_path))
    assert accord56_dealunit
    assert accord56_dealunit.deal_idea == accord56_deal_idea_str
    expected_dealunit = dealunit_shop(accord56_deal_idea_str)
    assert accord56_dealunit.timeline == expected_dealunit.timeline
    assert accord56_dealunit == expected_dealunit


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
#         deal_idea_str(),
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
#         deal_idea_str(),
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
#         deal_idea_str(),
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
#         deal_idea_str(),
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
# from src.f04_gift.atom_config import face_name_str, deal_idea_str
# from src.f07_deal.deal_config import cumlative_minute_str, hour_idea_str
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
#         deal_idea_str(),
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
