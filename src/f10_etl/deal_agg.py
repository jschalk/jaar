from src.f00_instrument.file import create_path
from src.f09_brick.pandas_tool import upsert_sheet
from pandas import DataFrame


def create_init_deal_prime_files(dir: str):
    dealunit_path = create_path(dir, "dealunit.xlsx")
    deal_purview_episode_path = create_path(dir, "deal_purview_episode.xlsx")
    deal_cashbook_path = create_path(dir, "deal_cashbook.xlsx")
    deal_timeline_hour_path = create_path(dir, "deal_timeline_hour.xlsx")
    deal_timeline_month_path = create_path(dir, "deal_timeline_month.xlsx")
    deal_timeline_weekday_path = create_path(dir, "deal_timeline_weekday.xlsx")

    dealunit_columns = [
        "source_br",
        "face_name",
        "event_int",
        "deal_idea",
        "c400_number",
        "current_time",
        "fund_coin",
        "monthday_distortion",
        "penny",
        "respect_bit",
        "bridge",
        "timeline_idea",
        "yr1_jan1_offset",
        "note",
    ]
    deal_purview_episode_columns = [
        "source_br",
        "face_name",
        "event_int",
        "deal_idea",
        "owner_name",
        "acct_name",
        "time_int",
        "quota",
        "note",
    ]
    deal_cashbook_columns = [
        "source_br",
        "face_name",
        "event_int",
        "deal_idea",
        "owner_name",
        "acct_name",
        "time_int",
        "amount",
        "note",
    ]
    deal_timeline_hour_columns = [
        "source_br",
        "face_name",
        "event_int",
        "deal_idea",
        "hour_idea",
        "cumlative_minute",
        "note",
    ]
    deal_timeline_month_columns = [
        "source_br",
        "face_name",
        "event_int",
        "deal_idea",
        "month_idea",
        "cumlative_day",
        "note",
    ]
    deal_timeline_weekday_columns = [
        "source_br",
        "face_name",
        "event_int",
        "deal_idea",
        "weekday_idea",
        "weekday_order",
        "note",
    ]
    dealunit_df = DataFrame([], columns=dealunit_columns)
    deal_purview_episode_df = DataFrame([], columns=deal_purview_episode_columns)
    deal_cashbook_df = DataFrame([], columns=deal_cashbook_columns)
    deal_timeline_hour_df = DataFrame([], columns=deal_timeline_hour_columns)
    deal_timeline_month_df = DataFrame([], columns=deal_timeline_month_columns)
    deal_timeline_weekday_df = DataFrame([], columns=deal_timeline_weekday_columns)

    upsert_sheet(dealunit_path, "staging", dealunit_df)
    upsert_sheet(deal_purview_episode_path, "staging", deal_purview_episode_df)
    upsert_sheet(deal_cashbook_path, "staging", deal_cashbook_df)
    upsert_sheet(deal_timeline_hour_path, "staging", deal_timeline_hour_df)
    upsert_sheet(deal_timeline_month_path, "staging", deal_timeline_month_df)
    upsert_sheet(deal_timeline_weekday_path, "staging", deal_timeline_weekday_df)

    drop_list = ["source_br", "face_name", "event_int", "note"]
    dealunit_df.drop(columns=drop_list, axis=1, inplace=True)
    deal_purview_episode_df.drop(columns=drop_list, axis=1, inplace=True)
    deal_cashbook_df.drop(columns=drop_list, axis=1, inplace=True)
    deal_timeline_hour_df.drop(columns=drop_list, axis=1, inplace=True)
    deal_timeline_month_df.drop(columns=drop_list, axis=1, inplace=True)
    deal_timeline_weekday_df.drop(columns=drop_list, axis=1, inplace=True)

    upsert_sheet(dealunit_path, "agg", dealunit_df)
    upsert_sheet(deal_purview_episode_path, "agg", deal_purview_episode_df)
    upsert_sheet(deal_cashbook_path, "agg", deal_cashbook_df)
    upsert_sheet(deal_timeline_hour_path, "agg", deal_timeline_hour_df)
    upsert_sheet(deal_timeline_month_path, "agg", deal_timeline_month_df)
    upsert_sheet(deal_timeline_weekday_path, "agg", deal_timeline_weekday_df)
