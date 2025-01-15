from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.dict_toolbox import (
    get_sorted_list_of_dict_keys as get_sorted_list,
)
from src.f03_chrono.chrono import (
    timeline_config_shop,
    timelineunit_shop,
    validate_timeline_config,
)
from src.f07_fiscal.fiscal import fiscalunit_shop
from src.f09_idea.idea import _add_cashpurchases_from_df, _add_dealepisodes_from_df
from src.f09_idea.pandas_tool import (
    upsert_sheet,
    dataframe_to_dict,
    if_nan_return_None,
)
from pandas import DataFrame, read_excel as pandas_read_excel


class FiscalPrimeFilePaths:
    def __init__(self, fiscals_dir: str):
        self.fiscalunit_path = create_path(fiscals_dir, "fiscalunit.xlsx")
        self.fiscal_deal_path = create_path(fiscals_dir, "fiscal_deal_episode.xlsx")
        self.fiscal_cashbook_path = create_path(fiscals_dir, "fiscal_cashbook.xlsx")
        self.fiscal_hour_path = create_path(fiscals_dir, "fiscal_timeline_hour.xlsx")
        self.fiscal_month_path = create_path(fiscals_dir, "fiscal_timeline_month.xlsx")
        self.fiscal_weekday_path = create_path(
            fiscals_dir, "fiscal_timeline_weekday.xlsx"
        )


class FiscalPrimeColumns:
    def __init__(self):
        self.fiscalunit_agg_columns = [
            "fiscal_title",
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
        self.fiscal_deal_agg_columns = [
            "fiscal_title",
            "owner_name",
            "time_int",
            "quota",
        ]
        self.fiscal_cashbook_agg_columns = [
            "fiscal_title",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
        ]
        self.fiscal_hour_agg_columns = [
            "fiscal_title",
            "hour_title",
            "cumlative_minute",
        ]
        self.fiscal_month_agg_columns = ["fiscal_title", "month_title", "cumlative_day"]
        self.fiscal_weekday_agg_columns = [
            "fiscal_title",
            "weekday_title",
            "weekday_order",
        ]

        _front_columns = ["source_br", "face_name", "event_int"]
        _back_columns = ["note"]
        self.fiscalunit_staging_columns = [
            *_front_columns,
            *self.fiscalunit_agg_columns,
            *_back_columns,
        ]
        self.fiscal_deal_staging_columns = [
            *_front_columns,
            *self.fiscal_deal_agg_columns,
            *_back_columns,
        ]
        self.fiscal_cashbook_staging_columns = [
            *_front_columns,
            *self.fiscal_cashbook_agg_columns,
            *_back_columns,
        ]
        self.fiscal_hour_staging_columns = [
            *_front_columns,
            *self.fiscal_hour_agg_columns,
            *_back_columns,
        ]
        self.fiscal_month_staging_columns = [
            *_front_columns,
            *self.fiscal_month_agg_columns,
            *_back_columns,
        ]
        self.fiscal_weekday_staging_columns = [
            *_front_columns,
            *self.fiscal_weekday_agg_columns,
            *_back_columns,
        ]


def create_init_fiscal_prime_files(fiscals_dir: str):
    xp = FiscalPrimeFilePaths(fiscals_dir)
    xc = FiscalPrimeColumns()
    stage_fiscalunit_df = DataFrame([], columns=xc.fiscalunit_staging_columns)
    stage_fiscal_deal_df = DataFrame([], columns=xc.fiscal_deal_staging_columns)
    stage_fiscal_cashbook_df = DataFrame([], columns=xc.fiscal_cashbook_staging_columns)
    stage_fiscal_hour_df = DataFrame([], columns=xc.fiscal_hour_staging_columns)
    stage_fiscal_month_df = DataFrame([], columns=xc.fiscal_month_staging_columns)
    stage_fiscal_weekday_df = DataFrame([], columns=xc.fiscal_weekday_staging_columns)
    upsert_sheet(xp.fiscalunit_path, "staging", stage_fiscalunit_df)
    upsert_sheet(xp.fiscal_deal_path, "staging", stage_fiscal_deal_df)
    upsert_sheet(xp.fiscal_cashbook_path, "staging", stage_fiscal_cashbook_df)
    upsert_sheet(xp.fiscal_hour_path, "staging", stage_fiscal_hour_df)
    upsert_sheet(xp.fiscal_month_path, "staging", stage_fiscal_month_df)
    upsert_sheet(xp.fiscal_weekday_path, "staging", stage_fiscal_weekday_df)

    agg_fiscalunit_df = DataFrame([], columns=xc.fiscalunit_agg_columns)
    agg_fiscal_deal_df = DataFrame([], columns=xc.fiscal_deal_agg_columns)
    agg_fiscal_cashbook_df = DataFrame([], columns=xc.fiscal_cashbook_agg_columns)
    agg_fiscal_hour_df = DataFrame([], columns=xc.fiscal_hour_agg_columns)
    agg_fiscal_month_df = DataFrame([], columns=xc.fiscal_month_agg_columns)
    agg_fiscal_weekday_df = DataFrame([], columns=xc.fiscal_weekday_agg_columns)
    upsert_sheet(xp.fiscalunit_path, "agg", agg_fiscalunit_df)
    upsert_sheet(xp.fiscal_deal_path, "agg", agg_fiscal_deal_df)
    upsert_sheet(xp.fiscal_cashbook_path, "agg", agg_fiscal_cashbook_df)
    upsert_sheet(xp.fiscal_hour_path, "agg", agg_fiscal_hour_df)
    upsert_sheet(xp.fiscal_month_path, "agg", agg_fiscal_month_df)
    upsert_sheet(xp.fiscal_weekday_path, "agg", agg_fiscal_weekday_df)


def create_timelineunit_from_prime_data(
    fiscal_attrs, fiscal_weekday_dict, fiscal_month_dict, fiscal_hour_dict
):
    if fiscal_weekday_dict:
        x_weekday_list = get_sorted_list(fiscal_weekday_dict, "weekday_order")
    else:
        x_weekday_list = None
    timeline_config = timeline_config_shop(
        timeline_title=if_nan_return_None(fiscal_attrs.get("timeline_title")),
        c400_number=if_nan_return_None(fiscal_attrs.get("c400_number")),
        hour_length=None,
        month_length=None,
        weekday_list=x_weekday_list,
        months_list=None,
        monthday_distortion=if_nan_return_None(fiscal_attrs.get("monthday_distortion")),
        yr1_jan1_offset=if_nan_return_None(fiscal_attrs.get("yr1_jan1_offset")),
    )
    if fiscal_month_dict:
        x_month_list = get_sorted_list(fiscal_month_dict, "cumlative_day", True)
        timeline_config["months_config"] = x_month_list
    if fiscal_hour_dict:
        x_hour_list = get_sorted_list(fiscal_hour_dict, "cumlative_minute", True)
        timeline_config["hours_config"] = x_hour_list
    if validate_timeline_config(timeline_config) is False:
        raise ValueError(f"Invalid timeline_config: {timeline_config=}")

    return timelineunit_shop(timeline_config)


def create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir: str):
    xp = FiscalPrimeFilePaths(fiscal_mstr_dir)
    fiscalunit_df = pandas_read_excel(xp.fiscalunit_path, "agg")
    fiscaldeal_df = pandas_read_excel(xp.fiscal_deal_path, "agg")
    fiscalcash_df = pandas_read_excel(xp.fiscal_cashbook_path, "agg")
    fiscalhour_df = pandas_read_excel(xp.fiscal_hour_path, "agg")
    fiscalmont_df = pandas_read_excel(xp.fiscal_month_path, "agg")
    fiscalweek_df = pandas_read_excel(xp.fiscal_weekday_path, "agg")

    fiscalunits_dict = dataframe_to_dict(fiscalunit_df, ["fiscal_title"])
    fiscalhours_dict = dataframe_to_dict(fiscalhour_df, ["fiscal_title", "hour_title"])
    fiscalmonts_dict = dataframe_to_dict(fiscalmont_df, ["fiscal_title", "month_title"])
    fiscalweeks_dict = dataframe_to_dict(
        fiscalweek_df, ["fiscal_title", "weekday_title"]
    )
    fiscalunits = {}
    for fiscal_attrs in fiscalunits_dict.values():
        x_fiscal_title = fiscal_attrs.get("fiscal_title")
        fiscal_timelineunit = create_timelineunit_from_prime_data(
            fiscal_attrs=fiscal_attrs,
            fiscal_weekday_dict=fiscalweeks_dict.get(x_fiscal_title),
            fiscal_month_dict=fiscalmonts_dict.get(x_fiscal_title),
            fiscal_hour_dict=fiscalhours_dict.get(x_fiscal_title),
        )

        fiscalunit = fiscalunit_shop(
            fiscal_title=x_fiscal_title,
            fiscals_dir=fiscal_mstr_dir,
            timeline=fiscal_timelineunit,
            current_time=if_nan_return_None(fiscal_attrs.get("current_time")),
            bridge=fiscal_attrs.get("bridge"),
            fund_coin=if_nan_return_None(fiscal_attrs.get("fund_coin")),
            penny=if_nan_return_None(fiscal_attrs.get("penny")),
            respect_bit=if_nan_return_None(fiscal_attrs.get("respect_bit")),
            in_memory_journal=True,
        )
        _add_cashpurchases_from_df(fiscalunit, fiscalcash_df)
        _add_dealepisodes_from_df(fiscalunit, fiscaldeal_df)
        fiscalunits[fiscalunit.fiscal_title] = fiscalunit
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    for fiscalunit in fiscalunits.values():
        fiscal_file_name = f"{fiscalunit.fiscal_title}.json"
        fiscalunit_dir = create_path(fiscals_dir, fiscalunit.fiscal_title)
        save_file(fiscalunit_dir, fiscal_file_name, fiscalunit.get_json())
