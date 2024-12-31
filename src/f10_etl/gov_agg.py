from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.dict_toolbox import (
    get_sorted_list_of_dict_keys as get_sorted_list,
)
from src.f03_chrono.chrono import (
    create_timeline_config,
    timelineunit_shop,
    validate_timeline_config,
)
from src.f07_gov.gov import govunit_shop
from src.f09_brick.brick import _add_cashpurchases_from_df, _add_dealepisodes_from_df
from src.f09_brick.pandas_tool import (
    upsert_sheet,
    dataframe_to_dict,
    if_nan_return_None,
)
from pandas import DataFrame, read_excel as pandas_read_excel


class GovPrimeFilePaths:
    def __init__(self, govs_dir: str):
        self.govunit_path = create_path(govs_dir, "govunit.xlsx")
        self.gov_deal_path = create_path(govs_dir, "gov_deal_episode.xlsx")
        self.gov_cashbook_path = create_path(govs_dir, "gov_cashbook.xlsx")
        self.gov_hour_path = create_path(govs_dir, "gov_timeline_hour.xlsx")
        self.gov_month_path = create_path(govs_dir, "gov_timeline_month.xlsx")
        self.gov_weekday_path = create_path(govs_dir, "gov_timeline_weekday.xlsx")


class GovPrimeColumns:
    def __init__(self):
        self.govunit_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "gov_idea",
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
        self.gov_deal_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "gov_idea",
            "owner_name",
            "time_int",
            "quota",
            "note",
        ]
        self.gov_cashbook_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "gov_idea",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
            "note",
        ]
        self.gov_hour_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "gov_idea",
            "hour_idea",
            "cumlative_minute",
            "note",
        ]
        self.gov_month_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "gov_idea",
            "month_idea",
            "cumlative_day",
            "note",
        ]
        self.gov_weekday_staging_columns = [
            "source_br",
            "face_name",
            "event_int",
            "gov_idea",
            "weekday_idea",
            "weekday_order",
            "note",
        ]

        self.govunit_agg_columns = [
            "gov_idea",
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
        self.gov_deal_agg_columns = [
            "gov_idea",
            "owner_name",
            "time_int",
            "quota",
        ]
        self.gov_cashbook_agg_columns = [
            "gov_idea",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
        ]
        self.gov_hour_agg_columns = ["gov_idea", "hour_idea", "cumlative_minute"]
        self.gov_month_agg_columns = ["gov_idea", "month_idea", "cumlative_day"]
        self.gov_weekday_agg_columns = ["gov_idea", "weekday_idea", "weekday_order"]


def create_init_gov_prime_files(govs_dir: str):
    xp = GovPrimeFilePaths(govs_dir)
    xc = GovPrimeColumns()
    stage_govunit_df = DataFrame([], columns=xc.govunit_staging_columns)
    stage_gov_deal_df = DataFrame([], columns=xc.gov_deal_staging_columns)
    stage_gov_cashbook_df = DataFrame([], columns=xc.gov_cashbook_staging_columns)
    stage_gov_hour_df = DataFrame([], columns=xc.gov_hour_staging_columns)
    stage_gov_month_df = DataFrame([], columns=xc.gov_month_staging_columns)
    stage_gov_weekday_df = DataFrame([], columns=xc.gov_weekday_staging_columns)
    upsert_sheet(xp.govunit_path, "staging", stage_govunit_df)
    upsert_sheet(xp.gov_deal_path, "staging", stage_gov_deal_df)
    upsert_sheet(xp.gov_cashbook_path, "staging", stage_gov_cashbook_df)
    upsert_sheet(xp.gov_hour_path, "staging", stage_gov_hour_df)
    upsert_sheet(xp.gov_month_path, "staging", stage_gov_month_df)
    upsert_sheet(xp.gov_weekday_path, "staging", stage_gov_weekday_df)

    agg_govunit_df = DataFrame([], columns=xc.govunit_agg_columns)
    agg_gov_deal_df = DataFrame([], columns=xc.gov_deal_agg_columns)
    agg_gov_cashbook_df = DataFrame([], columns=xc.gov_cashbook_agg_columns)
    agg_gov_hour_df = DataFrame([], columns=xc.gov_hour_agg_columns)
    agg_gov_month_df = DataFrame([], columns=xc.gov_month_agg_columns)
    agg_gov_weekday_df = DataFrame([], columns=xc.gov_weekday_agg_columns)
    upsert_sheet(xp.govunit_path, "agg", agg_govunit_df)
    upsert_sheet(xp.gov_deal_path, "agg", agg_gov_deal_df)
    upsert_sheet(xp.gov_cashbook_path, "agg", agg_gov_cashbook_df)
    upsert_sheet(xp.gov_hour_path, "agg", agg_gov_hour_df)
    upsert_sheet(xp.gov_month_path, "agg", agg_gov_month_df)
    upsert_sheet(xp.gov_weekday_path, "agg", agg_gov_weekday_df)


def create_timelineunit_from_prime_data(
    gov_attrs, gov_weekday_dict, gov_month_dict, gov_hour_dict
):
    if gov_weekday_dict:
        x_weekday_list = get_sorted_list(gov_weekday_dict, "weekday_order")
    else:
        x_weekday_list = None
    timeline_config = create_timeline_config(
        timeline_idea=if_nan_return_None(gov_attrs.get("timeline_idea")),
        c400_count=if_nan_return_None(gov_attrs.get("c400_number")),
        hour_length=None,
        month_length=None,
        weekday_list=x_weekday_list,
        months_list=None,
        monthday_distortion=None,
        yr1_jan1_offset=if_nan_return_None(gov_attrs.get("yr1_jan1_offset")),
    )
    if gov_month_dict:
        x_month_list = get_sorted_list(gov_month_dict, "cumlative_day", True)
        timeline_config["months_config"] = x_month_list
    if gov_hour_dict:
        x_hour_list = get_sorted_list(gov_hour_dict, "cumlative_minute", True)
        timeline_config["hours_config"] = x_hour_list
    if validate_timeline_config(timeline_config) is False:
        raise ValueError(f"Invalid timeline_config: {timeline_config=}")

    return timelineunit_shop(timeline_config)


def create_govunit_jsons_from_prime_files(govs_dir: str):
    xp = GovPrimeFilePaths(govs_dir)
    govunit_df = pandas_read_excel(xp.govunit_path, "agg")
    gov_deal_df = pandas_read_excel(xp.gov_deal_path, "agg")
    gov_cashbook_df = pandas_read_excel(xp.gov_cashbook_path, "agg")
    gov_hour_df = pandas_read_excel(xp.gov_hour_path, "agg")
    gov_month_df = pandas_read_excel(xp.gov_month_path, "agg")
    gov_weekday_df = pandas_read_excel(xp.gov_weekday_path, "agg")
    govunits_dict = dataframe_to_dict(govunit_df, ["gov_idea"])
    govs_hour_dict = dataframe_to_dict(gov_hour_df, ["gov_idea", "hour_idea"])
    govs_month_dict = dataframe_to_dict(gov_month_df, ["gov_idea", "month_idea"])
    weekday_keys = ["gov_idea", "weekday_idea"]
    govs_weekday_dict = dataframe_to_dict(gov_weekday_df, weekday_keys)
    govunits = {}
    for gov_attrs in govunits_dict.values():
        x_gov_idea = gov_attrs.get("gov_idea")
        gov_timelineunit = create_timelineunit_from_prime_data(
            gov_attrs=gov_attrs,
            gov_weekday_dict=govs_weekday_dict.get(x_gov_idea),
            gov_month_dict=govs_month_dict.get(x_gov_idea),
            gov_hour_dict=govs_hour_dict.get(x_gov_idea),
        )

        govunit = govunit_shop(
            gov_idea=x_gov_idea,
            govs_dir=govs_dir,
            timeline=gov_timelineunit,
            current_time=if_nan_return_None(gov_attrs.get("current_time")),
            bridge=gov_attrs.get("bridge"),
            fund_coin=if_nan_return_None(gov_attrs.get("fund_coin")),
            penny=if_nan_return_None(gov_attrs.get("penny")),
            respect_bit=if_nan_return_None(gov_attrs.get("respect_bit")),
        )
        _add_cashpurchases_from_df(govunit, gov_cashbook_df)
        _add_dealepisodes_from_df(govunit, gov_deal_df)
        govunits[govunit.gov_idea] = govunit
    gov_jsons_dir = create_path(govs_dir, "gov_jsons")
    for govunit in govunits.values():
        gov_file_name = f"{govunit.gov_idea}.json"
        save_file(gov_jsons_dir, gov_file_name, govunit.get_json())
