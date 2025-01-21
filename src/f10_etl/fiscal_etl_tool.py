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
from src.f09_idea.idea_db_tool import (
    upsert_sheet,
    dataframe_to_dict,
    if_nan_return_None,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def get_fiscalunit_sorted_args() -> list[str]:
    return [
        "fiscal_title",
        "fund_coin",
        "penny",
        "respect_bit",
        "present_time",
        "bridge",
        "c400_number",
        "yr1_jan1_offset",
        "monthday_distortion",
        "timeline_title",
    ]


def get_fiscalcash_sorted_args() -> list[str]:
    return ["fiscal_title", "owner_name", "acct_name", "time_int", "amount"]


def get_fiscaldeal_sorted_args() -> list[str]:
    return ["fiscal_title", "owner_name", "time_int", "quota"]


def get_fiscalhour_sorted_args() -> list[str]:
    return ["fiscal_title", "hour_title", "cumlative_minute"]


def get_fiscalmont_sorted_args() -> list[str]:
    return ["fiscal_title", "month_title", "cumlative_day"]


def get_fiscalweek_sorted_args() -> list[str]:
    return ["fiscal_title", "weekday_title", "weekday_order"]


class FiscalPrimeObjsRef:
    def __init__(self, x_dir: str = ""):
        self.unit_agg_tablename = "fiscalunit_agg"
        self.deal_agg_tablename = "fiscal_deal_episode_agg"
        self.cash_agg_tablename = "fiscal_cashbook_agg"
        self.hour_agg_tablename = "fiscal_timeline_hour_agg"
        self.mont_agg_tablename = "fiscal_timeline_month_agg"
        self.week_agg_tablename = "fiscal_timeline_weekday_agg"
        self.unit_stage_tablename = "fiscalunit_staging"
        self.deal_stage_tablename = "fiscal_deal_episode_staging"
        self.cash_stage_tablename = "fiscal_cashbook_staging"
        self.hour_stage_tablename = "fiscal_timeline_hour_staging"
        self.mont_stage_tablename = "fiscal_timeline_month_staging"
        self.week_stage_tablename = "fiscal_timeline_weekday_staging"
        self.unit_agg_csv_filename = "fiscalunit_agg.csv"
        self.deal_agg_csv_filename = "fiscal_deal_episode_agg.csv"
        self.cash_agg_csv_filename = "fiscal_cashbook_agg.csv"
        self.hour_agg_csv_filename = "fiscal_timeline_hour_agg.csv"
        self.mont_agg_csv_filename = "fiscal_timeline_month_agg.csv"
        self.week_agg_csv_filename = "fiscal_timeline_weekday_agg.csv"
        self.unit_agg_csv_path = create_path(x_dir, self.unit_agg_csv_filename)
        self.deal_agg_csv_path = create_path(x_dir, self.deal_agg_csv_filename)
        self.cash_agg_csv_path = create_path(x_dir, self.cash_agg_csv_filename)
        self.hour_agg_csv_path = create_path(x_dir, self.hour_agg_csv_filename)
        self.mont_agg_csv_path = create_path(x_dir, self.mont_agg_csv_filename)
        self.week_agg_csv_path = create_path(x_dir, self.week_agg_csv_filename)
        self.unit_stage_csv_filename = "fiscalunit_staging.csv"
        self.deal_stage_csv_filename = "fiscal_deal_episode_staging.csv"
        self.cash_stage_csv_filename = "fiscal_cashbook_staging.csv"
        self.hour_stage_csv_filename = "fiscal_timeline_hour_staging.csv"
        self.mont_stage_csv_filename = "fiscal_timeline_month_staging.csv"
        self.week_stage_csv_filename = "fiscal_timeline_weekday_staging.csv"
        self.unit_stage_csv_path = create_path(x_dir, self.unit_stage_csv_filename)
        self.deal_stage_csv_path = create_path(x_dir, self.deal_stage_csv_filename)
        self.cash_stage_csv_path = create_path(x_dir, self.cash_stage_csv_filename)
        self.hour_stage_csv_path = create_path(x_dir, self.hour_stage_csv_filename)
        self.mont_stage_csv_path = create_path(x_dir, self.mont_stage_csv_filename)
        self.week_stage_csv_path = create_path(x_dir, self.week_stage_csv_filename)

        self.unit_excel_filename = "fiscalunit.xlsx"
        self.deal_excel_filename = "fiscal_deal_episode.xlsx"
        self.cash_excel_filename = "fiscal_cashbook.xlsx"
        self.hour_excel_filename = "fiscal_timeline_hour.xlsx"
        self.mont_excel_filename = "fiscal_timeline_month.xlsx"
        self.week_excel_filename = "fiscal_timeline_weekday.xlsx"
        self.unit_excel_path = create_path(x_dir, "fiscalunit.xlsx")
        self.deal_excel_path = create_path(x_dir, "fiscal_deal_episode.xlsx")
        self.cash_excel_path = create_path(x_dir, "fiscal_cashbook.xlsx")
        self.hour_excel_path = create_path(x_dir, "fiscal_timeline_hour.xlsx")
        self.mont_excel_path = create_path(x_dir, "fiscal_timeline_month.xlsx")
        self.week_excel_path = create_path(x_dir, "fiscal_timeline_weekday.xlsx")


class FiscalPrimeColumnsRef:
    def __init__(self):
        self.unit_agg_columns = [
            "fiscal_title",
            "fund_coin",
            "penny",
            "respect_bit",
            "present_time",
            "bridge",
            "c400_number",
            "yr1_jan1_offset",
            "monthday_distortion",
            "timeline_title",
        ]
        self.deal_agg_columns = ["fiscal_title", "owner_name", "time_int", "quota"]
        self.cash_agg_columns = [
            "fiscal_title",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
        ]
        self.hour_agg_columns = ["fiscal_title", "hour_title", "cumlative_minute"]
        self.mont_agg_columns = ["fiscal_title", "month_title", "cumlative_day"]
        self.week_agg_columns = ["fiscal_title", "weekday_title", "weekday_order"]

        _front_cols = ["idea_number", "face_name", "event_int"]
        _back_cols = ["error_message"]
        self.unit_agg_csv_header = "fiscal_title,fund_coin,penny,respect_bit,present_time,bridge,c400_number,yr1_jan1_offset,monthday_distortion,timeline_title"
        self.deal_agg_csv_header = "fiscal_title,owner_name,time_int,quota"
        self.cash_agg_csv_header = "fiscal_title,owner_name,acct_name,time_int,amount"
        self.hour_agg_csv_header = "fiscal_title,hour_title,cumlative_minute"
        self.mont_agg_csv_header = "fiscal_title,month_title,cumlative_day"
        self.week_agg_csv_header = "fiscal_title,weekday_title,weekday_order"
        self.unit_staging_columns = [*_front_cols, *self.unit_agg_columns, *_back_cols]
        self.deal_staging_columns = [*_front_cols, *self.deal_agg_columns, *_back_cols]
        self.cash_staging_columns = [*_front_cols, *self.cash_agg_columns, *_back_cols]
        self.hour_staging_columns = [*_front_cols, *self.hour_agg_columns, *_back_cols]
        self.mont_staging_columns = [*_front_cols, *self.mont_agg_columns, *_back_cols]
        self.week_staging_columns = [*_front_cols, *self.week_agg_columns, *_back_cols]
        self.unit_staging_csv_header = """idea_number,face_name,event_int,fiscal_title,fund_coin,penny,respect_bit,present_time,bridge,c400_number,yr1_jan1_offset,monthday_distortion,timeline_title,error_message"""
        self.deal_staging_csv_header = """idea_number,face_name,event_int,fiscal_title,owner_name,time_int,quota,error_message"""
        self.cash_staging_csv_header = """idea_number,face_name,event_int,fiscal_title,owner_name,acct_name,time_int,amount,error_message"""
        self.hour_staging_csv_header = """idea_number,face_name,event_int,fiscal_title,hour_title,cumlative_minute,error_message"""
        self.mont_staging_csv_header = """idea_number,face_name,event_int,fiscal_title,month_title,cumlative_day,error_message"""
        self.week_staging_csv_header = """idea_number,face_name,event_int,fiscal_title,weekday_title,weekday_order,error_message"""
        self.unit_agg_empty_csv = f"{self.unit_agg_csv_header}\n"
        self.deal_agg_empty_csv = f"{self.deal_agg_csv_header}\n"
        self.cash_agg_empty_csv = f"{self.cash_agg_csv_header}\n"
        self.hour_agg_empty_csv = f"{self.hour_agg_csv_header}\n"
        self.mont_agg_empty_csv = f"{self.mont_agg_csv_header}\n"
        self.week_agg_empty_csv = f"{self.week_agg_csv_header}\n"


def create_init_fiscal_prime_files(fiscals_dir: str):
    fiscalref = FiscalPrimeObjsRef(fiscals_dir)
    xc = FiscalPrimeColumnsRef()
    unit_staging_df = DataFrame([], columns=xc.unit_staging_columns)
    deal_staging_df = DataFrame([], columns=xc.deal_staging_columns)
    cash_staging_df = DataFrame([], columns=xc.cash_staging_columns)
    hour_staging_df = DataFrame([], columns=xc.hour_staging_columns)
    mont_staging_df = DataFrame([], columns=xc.mont_staging_columns)
    week_staging_df = DataFrame([], columns=xc.week_staging_columns)
    upsert_sheet(fiscalref.unit_excel_path, "staging", unit_staging_df)
    upsert_sheet(fiscalref.deal_excel_path, "staging", deal_staging_df)
    upsert_sheet(fiscalref.cash_excel_path, "staging", cash_staging_df)
    upsert_sheet(fiscalref.hour_excel_path, "staging", hour_staging_df)
    upsert_sheet(fiscalref.mont_excel_path, "staging", mont_staging_df)
    upsert_sheet(fiscalref.week_excel_path, "staging", week_staging_df)

    unit_agg_df = DataFrame([], columns=xc.unit_agg_columns)
    deal_agg_df = DataFrame([], columns=xc.deal_agg_columns)
    cash_agg_df = DataFrame([], columns=xc.cash_agg_columns)
    hour_agg_df = DataFrame([], columns=xc.hour_agg_columns)
    mont_agg_df = DataFrame([], columns=xc.mont_agg_columns)
    week_agg_df = DataFrame([], columns=xc.week_agg_columns)
    upsert_sheet(fiscalref.unit_excel_path, "agg", unit_agg_df)
    upsert_sheet(fiscalref.deal_excel_path, "agg", deal_agg_df)
    upsert_sheet(fiscalref.cash_excel_path, "agg", cash_agg_df)
    upsert_sheet(fiscalref.hour_excel_path, "agg", hour_agg_df)
    upsert_sheet(fiscalref.mont_excel_path, "agg", mont_agg_df)
    upsert_sheet(fiscalref.week_excel_path, "agg", week_agg_df)


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
    xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    fiscalunit_df = pandas_read_excel(xp.unit_excel_path, "agg")
    fiscaldeal_df = pandas_read_excel(xp.deal_excel_path, "agg")
    fiscalcash_df = pandas_read_excel(xp.cash_excel_path, "agg")
    fiscalhour_df = pandas_read_excel(xp.hour_excel_path, "agg")
    fiscalmont_df = pandas_read_excel(xp.mont_excel_path, "agg")
    fiscalweek_df = pandas_read_excel(xp.week_excel_path, "agg")

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
            present_time=if_nan_return_None(fiscal_attrs.get("present_time")),
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
