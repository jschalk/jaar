from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.dict_toolbox import (
    get_sorted_list_of_dict_keys as get_sorted_list,
)
from src.f03_chrono.chrono import (
    create_timeline_config,
    timelineunit_shop,
    validate_timeline_config,
)
from src.f07_cmty.cmty import cmtyunit_shop
from src.f09_brick.brick import _add_cashpurchases_from_df, _add_dealepisodes_from_df
from src.f09_brick.pandas_tool import (
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
            "cmty_idea",
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
        self.cmty_deal_agg_columns = [
            "cmty_idea",
            "owner_name",
            "time_int",
            "quota",
        ]
        self.cmty_cashbook_agg_columns = [
            "cmty_idea",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
        ]
        self.cmty_hour_agg_columns = ["cmty_idea", "hour_idea", "cumlative_minute"]
        self.cmty_month_agg_columns = ["cmty_idea", "month_idea", "cumlative_day"]
        self.cmty_weekday_agg_columns = ["cmty_idea", "weekday_idea", "weekday_order"]

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
    timeline_config = create_timeline_config(
        timeline_idea=if_nan_return_None(cmty_attrs.get("timeline_idea")),
        c400_count=if_nan_return_None(cmty_attrs.get("c400_number")),
        hour_length=None,
        month_length=None,
        weekday_list=x_weekday_list,
        months_list=None,
        monthday_distortion=None,
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


def create_cmtyunit_jsons_from_prime_files(cmtys_dir: str):
    xp = CmtyPrimeFilePaths(cmtys_dir)
    cmtyunit_df = pandas_read_excel(xp.cmtyunit_path, "agg")
    cmty_deal_df = pandas_read_excel(xp.cmty_deal_path, "agg")
    cmty_cashbook_df = pandas_read_excel(xp.cmty_cashbook_path, "agg")
    cmty_hour_df = pandas_read_excel(xp.cmty_hour_path, "agg")
    cmty_month_df = pandas_read_excel(xp.cmty_month_path, "agg")
    cmty_weekday_df = pandas_read_excel(xp.cmty_weekday_path, "agg")
    cmtyunits_dict = dataframe_to_dict(cmtyunit_df, ["cmty_idea"])
    cmtys_hour_dict = dataframe_to_dict(cmty_hour_df, ["cmty_idea", "hour_idea"])
    cmtys_month_dict = dataframe_to_dict(cmty_month_df, ["cmty_idea", "month_idea"])
    weekday_keys = ["cmty_idea", "weekday_idea"]
    cmtys_weekday_dict = dataframe_to_dict(cmty_weekday_df, weekday_keys)
    cmtyunits = {}
    for cmty_attrs in cmtyunits_dict.values():
        x_cmty_idea = cmty_attrs.get("cmty_idea")
        cmty_timelineunit = create_timelineunit_from_prime_data(
            cmty_attrs=cmty_attrs,
            cmty_weekday_dict=cmtys_weekday_dict.get(x_cmty_idea),
            cmty_month_dict=cmtys_month_dict.get(x_cmty_idea),
            cmty_hour_dict=cmtys_hour_dict.get(x_cmty_idea),
        )

        cmtyunit = cmtyunit_shop(
            cmty_idea=x_cmty_idea,
            cmtys_dir=cmtys_dir,
            timeline=cmty_timelineunit,
            current_time=if_nan_return_None(cmty_attrs.get("current_time")),
            bridge=cmty_attrs.get("bridge"),
            fund_coin=if_nan_return_None(cmty_attrs.get("fund_coin")),
            penny=if_nan_return_None(cmty_attrs.get("penny")),
            respect_bit=if_nan_return_None(cmty_attrs.get("respect_bit")),
        )
        _add_cashpurchases_from_df(cmtyunit, cmty_cashbook_df)
        _add_dealepisodes_from_df(cmtyunit, cmty_deal_df)
        cmtyunits[cmtyunit.cmty_idea] = cmtyunit
    cmty_jsons_dir = create_path(cmtys_dir, "cmty_jsons")
    for cmtyunit in cmtyunits.values():
        cmty_file_name = f"{cmtyunit.cmty_idea}.json"
        save_file(cmty_jsons_dir, cmty_file_name, cmtyunit.get_json())
