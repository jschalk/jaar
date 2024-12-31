from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.dict_toolbox import get_sorted_list_of_dict_keys
from src.f03_chrono.chrono import (
    create_timeline_config,
    timelineunit_shop,
    validate_timeline_config,
)
from src.f07_deal.deal import dealunit_shop
from src.f09_brick.pandas_tool import (
    upsert_sheet,
    dataframe_to_dict,
    if_nan_return_None,
)
from pandas import DataFrame, read_excel as pandas_read_excel


class DealPrimeFilePaths:
    def __init__(self, deals_dir: str):
        self.dealunit_path = create_path(deals_dir, "dealunit.xlsx")
        self.deal_purview_path = create_path(deals_dir, "deal_purview_episode.xlsx")
        self.deal_cashbook_path = create_path(deals_dir, "deal_cashbook.xlsx")
        self.deal_hour_path = create_path(deals_dir, "deal_timeline_hour.xlsx")
        self.deal_month_path = create_path(deals_dir, "deal_timeline_month.xlsx")
        self.deal_weekday_path = create_path(deals_dir, "deal_timeline_weekday.xlsx")


class DealPrimeColumns:
    def __init__(self):
        self.dealunit_staging_columns = [
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
        self.deal_purview_staging_columns = [
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
        self.deal_cashbook_staging_columns = [
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
        self.deal_hour_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "deal_idea",
            "hour_idea",
            "cumlative_minute",
            "note",
        ]
        self.deal_month_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "deal_idea",
            "month_idea",
            "cumlative_day",
            "note",
        ]
        self.deal_weekday_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "deal_idea",
            "weekday_idea",
            "weekday_order",
            "note",
        ]

        self.dealunit_agg_columns = [
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
        ]
        self.deal_purview_agg_columns = [
            "deal_idea",
            "owner_name",
            "acct_name",
            "time_int",
            "quota",
        ]
        self.deal_cashbook_agg_columns = [
            "deal_idea",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
        ]
        self.deal_hour_agg_columns = ["deal_idea", "hour_idea", "cumlative_minute"]
        self.deal_month_agg_columns = ["deal_idea", "month_idea", "cumlative_day"]
        self.deal_weekday_agg_columns = ["deal_idea", "weekday_idea", "weekday_order"]


def create_init_deal_prime_files(deals_dir: str):
    xp = DealPrimeFilePaths(deals_dir)
    xc = DealPrimeColumns()
    stage_dealunit_df = DataFrame([], columns=xc.dealunit_staging_columns)
    stage_deal_purview_df = DataFrame([], columns=xc.deal_purview_staging_columns)
    stage_deal_cashbook_df = DataFrame([], columns=xc.deal_cashbook_staging_columns)
    stage_deal_hour_df = DataFrame([], columns=xc.deal_hour_staging_columns)
    stage_deal_month_df = DataFrame([], columns=xc.deal_month_staging_columns)
    stage_deal_weekday_df = DataFrame([], columns=xc.deal_weekday_staging_columns)

    upsert_sheet(xp.dealunit_path, "staging", stage_dealunit_df)
    upsert_sheet(xp.deal_purview_path, "staging", stage_deal_purview_df)
    upsert_sheet(xp.deal_cashbook_path, "staging", stage_deal_cashbook_df)
    upsert_sheet(xp.deal_hour_path, "staging", stage_deal_hour_df)
    upsert_sheet(xp.deal_month_path, "staging", stage_deal_month_df)
    upsert_sheet(xp.deal_weekday_path, "staging", stage_deal_weekday_df)

    agg_dealunit_df = DataFrame([], columns=xc.dealunit_agg_columns)
    agg_deal_purview_df = DataFrame([], columns=xc.deal_purview_agg_columns)
    agg_deal_cashbook_df = DataFrame([], columns=xc.deal_cashbook_agg_columns)
    agg_deal_hour_df = DataFrame([], columns=xc.deal_hour_agg_columns)
    agg_deal_month_df = DataFrame([], columns=xc.deal_month_agg_columns)
    agg_deal_weekday_df = DataFrame([], columns=xc.deal_weekday_agg_columns)

    upsert_sheet(xp.dealunit_path, "agg", agg_dealunit_df)
    upsert_sheet(xp.deal_purview_path, "agg", agg_deal_purview_df)
    upsert_sheet(xp.deal_cashbook_path, "agg", agg_deal_cashbook_df)
    upsert_sheet(xp.deal_hour_path, "agg", agg_deal_hour_df)
    upsert_sheet(xp.deal_month_path, "agg", agg_deal_month_df)
    upsert_sheet(xp.deal_weekday_path, "agg", agg_deal_weekday_df)


def create_dealunit_jsons_from_prime_files(deals_dir: str):
    xp = DealPrimeFilePaths(deals_dir)
    xc = DealPrimeColumns()
    dealunit_df = pandas_read_excel(xp.dealunit_path, "agg")
    deal_purview_df = pandas_read_excel(xp.deal_purview_path, "agg")
    deal_cashbook_df = pandas_read_excel(xp.deal_cashbook_path, "agg")
    deal_hour_df = pandas_read_excel(xp.deal_hour_path, "agg")
    deal_month_df = pandas_read_excel(xp.deal_month_path, "agg")
    deal_weekday_df = pandas_read_excel(xp.deal_weekday_path, "agg")
    dealunits_dict = dataframe_to_dict(dealunit_df, ["deal_idea"])
    deals_purview_dict = dataframe_to_dict(deal_purview_df, ["deal_idea"])
    deals_cashbook_dict = dataframe_to_dict(deal_cashbook_df, ["deal_idea"])
    deals_hour_dict = dataframe_to_dict(deal_hour_df, ["deal_idea", "hour_idea"])
    deals_month_dict = dataframe_to_dict(deal_month_df, ["deal_idea", "month_idea"])
    weekday_keys = ["deal_idea", "weekday_idea"]
    deals_weekday_dict = dataframe_to_dict(deal_weekday_df, weekday_keys)
    dealunits = {}
    for deal_attrs in dealunits_dict.values():
        x_deal_idea = deal_attrs.get("deal_idea")
        if weekday_dict := deals_weekday_dict.get(x_deal_idea):
            x_weekday_list = get_sorted_list_of_dict_keys(weekday_dict, "weekday_order")
        else:
            x_weekday_list = None
        timeline_config = create_timeline_config(
            timeline_idea=if_nan_return_None(deal_attrs.get("timeline_idea")),
            c400_count=if_nan_return_None(deal_attrs.get("c400_number")),
            hour_length=None,
            month_length=None,
            weekday_list=x_weekday_list,
            months_list=None,
            monthday_distortion=None,
            yr1_jan1_offset=if_nan_return_None(deal_attrs.get("yr1_jan1_offset")),
        )
        if month_dict := deals_month_dict.get(x_deal_idea):
            x_month_list = get_sorted_list_of_dict_keys(
                month_dict, "cumlative_day", True
            )
            timeline_config["months_config"] = x_month_list
        if hour_dict := deals_hour_dict.get(x_deal_idea):
            x_hour_list = get_sorted_list_of_dict_keys(
                hour_dict, "cumlative_minute", True
            )
            timeline_config["hours_config"] = x_hour_list
        if validate_timeline_config(timeline_config) is False:
            raise ValueError(f"Invalid timeline_config: {timeline_config=}")
        dealunit = dealunit_shop(
            deal_idea=x_deal_idea,
            deals_dir=deals_dir,
            timeline=timelineunit_shop(timeline_config),
            current_time=if_nan_return_None(deal_attrs.get("current_time")),
            bridge=deal_attrs.get("bridge"),
            fund_coin=if_nan_return_None(deal_attrs.get("fund_coin")),
            penny=if_nan_return_None(deal_attrs.get("penny")),
            respect_bit=if_nan_return_None(deal_attrs.get("respect_bit")),
        )
        dealunits[dealunit.deal_idea] = dealunit
    deal_jsons_dir = create_path(deals_dir, "deal_jsons")
    for dealunit in dealunits.values():
        deal_file_name = f"{dealunit.deal_idea}.json"
        save_file(deal_jsons_dir, deal_file_name, dealunit.get_json())
