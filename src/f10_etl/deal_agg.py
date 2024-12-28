from src.f00_instrument.file import create_path
from src.f09_brick.pandas_tool import upsert_sheet
from pandas import DataFrame


def create_init_deal_staging_files(dir: str):
    br00000_path = create_path(dir, "br00000.xlsx")
    br00001_path = create_path(dir, "br00001.xlsx")
    br00002_path = create_path(dir, "br00002.xlsx")
    br00003_path = create_path(dir, "br00003.xlsx")
    br00004_path = create_path(dir, "br00004.xlsx")
    br00005_path = create_path(dir, "br00005.xlsx")

    br00000_columns = [
        "face_id",
        "event_int",
        "deal_id",
        "c400_number",
        "current_time",
        "fund_coin",
        "monthday_distortion",
        "penny",
        "respect_bit",
        "bridge",
        "timeline_idea",
        "yr1_jan1_offset",
    ]
    br00001_columns = [
        "face_id",
        "event_int",
        "deal_id",
        "owner_id",
        "acct_id",
        "time_int",
        "quota",
    ]
    br00002_columns = [
        "face_id",
        "event_int",
        "deal_id",
        "owner_id",
        "acct_id",
        "time_int",
        "amount",
    ]
    br00003_columns = [
        "face_id",
        "event_int",
        "deal_id",
        "hour_idea",
        "cumlative_minute",
    ]
    br00004_columns = [
        "face_id",
        "event_int",
        "deal_id",
        "month_idea",
        "cumlative_day",
    ]
    br00005_columns = [
        "face_id",
        "event_int",
        "deal_id",
        "weekday_idea",
        "weekday_order",
    ]
    br00000_df = DataFrame([], columns=br00000_columns)
    br00001_df = DataFrame([], columns=br00001_columns)
    br00002_df = DataFrame([], columns=br00002_columns)
    br00003_df = DataFrame([], columns=br00003_columns)
    br00004_df = DataFrame([], columns=br00004_columns)
    br00005_df = DataFrame([], columns=br00005_columns)

    upsert_sheet(br00000_path, "staging", br00000_df)
    upsert_sheet(br00001_path, "staging", br00001_df)
    upsert_sheet(br00002_path, "staging", br00002_df)
    upsert_sheet(br00003_path, "staging", br00003_df)
    upsert_sheet(br00004_path, "staging", br00004_df)
    upsert_sheet(br00005_path, "staging", br00005_df)
