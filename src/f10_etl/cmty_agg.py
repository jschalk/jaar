from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.dict_toolbox import (
    get_sorted_list_of_dict_keys as get_sorted_list,
)
from src.f03_chrono.chrono import (
    timeline_config_shop,
    timelineunit_shop,
    validate_timeline_config,
)
from src.f07_cmty.cmty import cmtyunit_shop
from src.f09_idea.idea import _add_cashpurchases_from_df, _add_dealepisodes_from_df
from src.f09_idea.pandas_tool import (
    upsert_sheet,
    dataframe_to_dict,
    if_nan_return_None,
)
from pandas import DataFrame, read_excel as pandas_read_excel


class CmtyPrimeFilePaths:
    def __init__(self, cmtys_dir: str):
        self.cmtyunit_path = create_path(cmtys_dir, "cmtyunit.xlsx")
        self.cmty_deal_path = create_path(cmtys_dir, "cmty_deal_episode.xlsx")
        self.cmty_cashbook_path = create_path(cmtys_dir, "cmty_cashbook.xlsx")
        self.cmty_hour_path = create_path(cmtys_dir, "cmty_timeline_hour.xlsx")
        self.cmty_month_path = create_path(cmtys_dir, "cmty_timeline_month.xlsx")
        self.cmty_weekday_path = create_path(cmtys_dir, "cmty_timeline_weekday.xlsx")


class CmtyPrimeColumns:
    def __init__(self):
        self.cmtyunit_agg_columns = [
            "cmty_title",
            "c400_number",
            "current_time",
            "fund_coin",
            "monthday_distortion",
            "penny",
            "respect_bit",
            "bridge",
            "timeline_title",
            "yr1_jan1_offset",
        ]
        self.cmty_deal_agg_columns = [
            "cmty_title",
            "owner_name",
            "time_int",
            "quota",
        ]
        self.cmty_cashbook_agg_columns = [
            "cmty_title",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
        ]
        self.cmty_hour_agg_columns = ["cmty_title", "hour_title", "cumlative_minute"]
        self.cmty_month_agg_columns = ["cmty_title", "month_title", "cumlative_day"]
        self.cmty_weekday_agg_columns = ["cmty_title", "weekday_title", "weekday_order"]

        _front_columns = ["source_br", "face_name", "event_int"]
        _back_columns = ["note"]
        self.cmtyunit_staging_columns = [
            *_front_columns,
            *self.cmtyunit_agg_columns,
            *_back_columns,
        ]
        self.cmty_deal_staging_columns = [
            *_front_columns,
            *self.cmty_deal_agg_columns,
            *_back_columns,
        ]
        self.cmty_cashbook_staging_columns = [
            *_front_columns,
            *self.cmty_cashbook_agg_columns,
            *_back_columns,
        ]
        self.cmty_hour_staging_columns = [
            *_front_columns,
            *self.cmty_hour_agg_columns,
            *_back_columns,
        ]
        self.cmty_month_staging_columns = [
            *_front_columns,
            *self.cmty_month_agg_columns,
            *_back_columns,
        ]
        self.cmty_weekday_staging_columns = [
            *_front_columns,
            *self.cmty_weekday_agg_columns,
            *_back_columns,
        ]


def create_init_cmty_prime_files(cmtys_dir: str):
    xp = CmtyPrimeFilePaths(cmtys_dir)
    xc = CmtyPrimeColumns()
    stage_cmtyunit_df = DataFrame([], columns=xc.cmtyunit_staging_columns)
    stage_cmty_deal_df = DataFrame([], columns=xc.cmty_deal_staging_columns)
    stage_cmty_cashbook_df = DataFrame([], columns=xc.cmty_cashbook_staging_columns)
    stage_cmty_hour_df = DataFrame([], columns=xc.cmty_hour_staging_columns)
    stage_cmty_month_df = DataFrame([], columns=xc.cmty_month_staging_columns)
    stage_cmty_weekday_df = DataFrame([], columns=xc.cmty_weekday_staging_columns)
    upsert_sheet(xp.cmtyunit_path, "staging", stage_cmtyunit_df)
    upsert_sheet(xp.cmty_deal_path, "staging", stage_cmty_deal_df)
    upsert_sheet(xp.cmty_cashbook_path, "staging", stage_cmty_cashbook_df)
    upsert_sheet(xp.cmty_hour_path, "staging", stage_cmty_hour_df)
    upsert_sheet(xp.cmty_month_path, "staging", stage_cmty_month_df)
    upsert_sheet(xp.cmty_weekday_path, "staging", stage_cmty_weekday_df)

    agg_cmtyunit_df = DataFrame([], columns=xc.cmtyunit_agg_columns)
    agg_cmty_deal_df = DataFrame([], columns=xc.cmty_deal_agg_columns)
    agg_cmty_cashbook_df = DataFrame([], columns=xc.cmty_cashbook_agg_columns)
    agg_cmty_hour_df = DataFrame([], columns=xc.cmty_hour_agg_columns)
    agg_cmty_month_df = DataFrame([], columns=xc.cmty_month_agg_columns)
    agg_cmty_weekday_df = DataFrame([], columns=xc.cmty_weekday_agg_columns)
    upsert_sheet(xp.cmtyunit_path, "agg", agg_cmtyunit_df)
    upsert_sheet(xp.cmty_deal_path, "agg", agg_cmty_deal_df)
    upsert_sheet(xp.cmty_cashbook_path, "agg", agg_cmty_cashbook_df)
    upsert_sheet(xp.cmty_hour_path, "agg", agg_cmty_hour_df)
    upsert_sheet(xp.cmty_month_path, "agg", agg_cmty_month_df)
    upsert_sheet(xp.cmty_weekday_path, "agg", agg_cmty_weekday_df)


def create_timelineunit_from_prime_data(
    cmty_attrs, cmty_weekday_dict, cmty_month_dict, cmty_hour_dict
):
    if cmty_weekday_dict:
        x_weekday_list = get_sorted_list(cmty_weekday_dict, "weekday_order")
    else:
        x_weekday_list = None
    timeline_config = timeline_config_shop(
        timeline_title=if_nan_return_None(cmty_attrs.get("timeline_title")),
        c400_number=if_nan_return_None(cmty_attrs.get("c400_number")),
        hour_length=None,
        month_length=None,
        weekday_list=x_weekday_list,
        months_list=None,
        monthday_distortion=if_nan_return_None(cmty_attrs.get("monthday_distortion")),
        yr1_jan1_offset=if_nan_return_None(cmty_attrs.get("yr1_jan1_offset")),
    )
    if cmty_month_dict:
        x_month_list = get_sorted_list(cmty_month_dict, "cumlative_day", True)
        timeline_config["months_config"] = x_month_list
    if cmty_hour_dict:
        x_hour_list = get_sorted_list(cmty_hour_dict, "cumlative_minute", True)
        timeline_config["hours_config"] = x_hour_list
    if validate_timeline_config(timeline_config) is False:
        raise ValueError(f"Invalid timeline_config: {timeline_config=}")

    return timelineunit_shop(timeline_config)


def create_cmtyunit_jsons_from_prime_files(cmty_mstr_dir: str):
    xp = CmtyPrimeFilePaths(cmty_mstr_dir)
    cmtyunit_df = pandas_read_excel(xp.cmtyunit_path, "agg")
    cmtydeal_df = pandas_read_excel(xp.cmty_deal_path, "agg")
    cmtycash_df = pandas_read_excel(xp.cmty_cashbook_path, "agg")
    cmtyhour_df = pandas_read_excel(xp.cmty_hour_path, "agg")
    cmtymont_df = pandas_read_excel(xp.cmty_month_path, "agg")
    cmtyweek_df = pandas_read_excel(xp.cmty_weekday_path, "agg")

    cmtyunits_dict = dataframe_to_dict(cmtyunit_df, ["cmty_title"])
    cmtyhours_dict = dataframe_to_dict(cmtyhour_df, ["cmty_title", "hour_title"])
    cmtymonts_dict = dataframe_to_dict(cmtymont_df, ["cmty_title", "month_title"])
    cmtyweeks_dict = dataframe_to_dict(cmtyweek_df, ["cmty_title", "weekday_title"])
    cmtyunits = {}
    for cmty_attrs in cmtyunits_dict.values():
        x_cmty_title = cmty_attrs.get("cmty_title")
        cmty_timelineunit = create_timelineunit_from_prime_data(
            cmty_attrs=cmty_attrs,
            cmty_weekday_dict=cmtyweeks_dict.get(x_cmty_title),
            cmty_month_dict=cmtymonts_dict.get(x_cmty_title),
            cmty_hour_dict=cmtyhours_dict.get(x_cmty_title),
        )

        cmtyunit = cmtyunit_shop(
            cmty_title=x_cmty_title,
            cmtys_dir=cmty_mstr_dir,
            timeline=cmty_timelineunit,
            current_time=if_nan_return_None(cmty_attrs.get("current_time")),
            bridge=cmty_attrs.get("bridge"),
            fund_coin=if_nan_return_None(cmty_attrs.get("fund_coin")),
            penny=if_nan_return_None(cmty_attrs.get("penny")),
            respect_bit=if_nan_return_None(cmty_attrs.get("respect_bit")),
            in_memory_journal=True,
        )
        _add_cashpurchases_from_df(cmtyunit, cmtycash_df)
        _add_dealepisodes_from_df(cmtyunit, cmtydeal_df)
        cmtyunits[cmtyunit.cmty_title] = cmtyunit
    cmtys_dir = create_path(cmty_mstr_dir, "cmtys")
    for cmtyunit in cmtyunits.values():
        cmty_file_name = f"{cmtyunit.cmty_title}.json"
        cmtyunit_dir = create_path(cmtys_dir, cmtyunit.cmty_title)
        save_file(cmtyunit_dir, cmty_file_name, cmtyunit.get_json())
