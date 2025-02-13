from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.dict_toolbox import (
    get_sorted_list_of_dict_keys as get_sorted_list,
)
from src.f03_chrono.chrono import (
    timeline_config_shop,
    timelineunit_shop,
    validate_timeline_config,
)
from src.f07_fisc.fisc import fiscunit_shop
from src.f09_idea.idea import _add_cashpurchases_from_df, _add_dealepisodes_from_df
from src.f09_idea.idea_db_tool import (
    upsert_sheet,
    dataframe_to_dict,
    if_nan_return_None,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def get_fiscunit_sorted_args() -> list[str]:
    return [
        "fisc_title",
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


def get_fisccash_sorted_args() -> list[str]:
    return ["fisc_title", "owner_name", "acct_name", "time_int", "amount"]


def get_fiscdeal_sorted_args() -> list[str]:
    return ["fisc_title", "owner_name", "time_int", "quota", "ledger_depth"]


def get_fischour_sorted_args() -> list[str]:
    return ["fisc_title", "hour_title", "cumlative_minute"]


def get_fiscmont_sorted_args() -> list[str]:
    return ["fisc_title", "month_title", "cumlative_day"]


def get_fiscweek_sorted_args() -> list[str]:
    return ["fisc_title", "weekday_title", "weekday_order"]


class FiscPrimeObjsRef:
    def __init__(self, x_dir: str = ""):
        self.unit_agg_tablename = "fiscunit_agg"
        self.deal_agg_tablename = "fisc_deal_episode_agg"
        self.cash_agg_tablename = "fisc_cashbook_agg"
        self.hour_agg_tablename = "fisc_timeline_hour_agg"
        self.mont_agg_tablename = "fisc_timeline_month_agg"
        self.week_agg_tablename = "fisc_timeline_weekday_agg"
        self.unit_stage_tablename = "fiscunit_staging"
        self.deal_stage_tablename = "fisc_deal_episode_staging"
        self.cash_stage_tablename = "fisc_cashbook_staging"
        self.hour_stage_tablename = "fisc_timeline_hour_staging"
        self.mont_stage_tablename = "fisc_timeline_month_staging"
        self.week_stage_tablename = "fisc_timeline_weekday_staging"
        self.unit_agg_csv_filename = "fiscunit_agg.csv"
        self.deal_agg_csv_filename = "fisc_deal_episode_agg.csv"
        self.cash_agg_csv_filename = "fisc_cashbook_agg.csv"
        self.hour_agg_csv_filename = "fisc_timeline_hour_agg.csv"
        self.mont_agg_csv_filename = "fisc_timeline_month_agg.csv"
        self.week_agg_csv_filename = "fisc_timeline_weekday_agg.csv"
        self.unit_agg_csv_path = create_path(x_dir, self.unit_agg_csv_filename)
        self.deal_agg_csv_path = create_path(x_dir, self.deal_agg_csv_filename)
        self.cash_agg_csv_path = create_path(x_dir, self.cash_agg_csv_filename)
        self.hour_agg_csv_path = create_path(x_dir, self.hour_agg_csv_filename)
        self.mont_agg_csv_path = create_path(x_dir, self.mont_agg_csv_filename)
        self.week_agg_csv_path = create_path(x_dir, self.week_agg_csv_filename)
        self.unit_stage_csv_filename = "fiscunit_staging.csv"
        self.deal_stage_csv_filename = "fisc_deal_episode_staging.csv"
        self.cash_stage_csv_filename = "fisc_cashbook_staging.csv"
        self.hour_stage_csv_filename = "fisc_timeline_hour_staging.csv"
        self.mont_stage_csv_filename = "fisc_timeline_month_staging.csv"
        self.week_stage_csv_filename = "fisc_timeline_weekday_staging.csv"
        self.unit_stage_csv_path = create_path(x_dir, self.unit_stage_csv_filename)
        self.deal_stage_csv_path = create_path(x_dir, self.deal_stage_csv_filename)
        self.cash_stage_csv_path = create_path(x_dir, self.cash_stage_csv_filename)
        self.hour_stage_csv_path = create_path(x_dir, self.hour_stage_csv_filename)
        self.mont_stage_csv_path = create_path(x_dir, self.mont_stage_csv_filename)
        self.week_stage_csv_path = create_path(x_dir, self.week_stage_csv_filename)

        self.unit_excel_filename = "fiscunit.xlsx"
        self.deal_excel_filename = "fisc_deal_episode.xlsx"
        self.cash_excel_filename = "fisc_cashbook.xlsx"
        self.hour_excel_filename = "fisc_timeline_hour.xlsx"
        self.mont_excel_filename = "fisc_timeline_month.xlsx"
        self.week_excel_filename = "fisc_timeline_weekday.xlsx"
        self.unit_excel_path = create_path(x_dir, "fiscunit.xlsx")
        self.deal_excel_path = create_path(x_dir, "fisc_deal_episode.xlsx")
        self.cash_excel_path = create_path(x_dir, "fisc_cashbook.xlsx")
        self.hour_excel_path = create_path(x_dir, "fisc_timeline_hour.xlsx")
        self.mont_excel_path = create_path(x_dir, "fisc_timeline_month.xlsx")
        self.week_excel_path = create_path(x_dir, "fisc_timeline_weekday.xlsx")


class FiscPrimeColumnsRef:
    def __init__(self):
        self.unit_agg_columns = [
            "fisc_title",
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
        self.deal_agg_columns = [
            "fisc_title",
            "owner_name",
            "time_int",
            "quota",
            "ledger_depth",
        ]
        self.cash_agg_columns = [
            "fisc_title",
            "owner_name",
            "acct_name",
            "time_int",
            "amount",
        ]
        self.hour_agg_columns = ["fisc_title", "hour_title", "cumlative_minute"]
        self.mont_agg_columns = ["fisc_title", "month_title", "cumlative_day"]
        self.week_agg_columns = ["fisc_title", "weekday_title", "weekday_order"]

        _front_cols = ["idea_number", "face_name", "event_int"]
        _back_cols = ["error_message"]
        self.unit_agg_csv_header = "fisc_title,fund_coin,penny,respect_bit,present_time,bridge,c400_number,yr1_jan1_offset,monthday_distortion,timeline_title"
        self.deal_agg_csv_header = "fisc_title,owner_name,time_int,quota,ledger_depth"
        self.cash_agg_csv_header = "fisc_title,owner_name,acct_name,time_int,amount"
        self.hour_agg_csv_header = "fisc_title,hour_title,cumlative_minute"
        self.mont_agg_csv_header = "fisc_title,month_title,cumlative_day"
        self.week_agg_csv_header = "fisc_title,weekday_title,weekday_order"
        self.unit_staging_columns = [*_front_cols, *self.unit_agg_columns, *_back_cols]
        self.deal_staging_columns = [*_front_cols, *self.deal_agg_columns, *_back_cols]
        self.cash_staging_columns = [*_front_cols, *self.cash_agg_columns, *_back_cols]
        self.hour_staging_columns = [*_front_cols, *self.hour_agg_columns, *_back_cols]
        self.mont_staging_columns = [*_front_cols, *self.mont_agg_columns, *_back_cols]
        self.week_staging_columns = [*_front_cols, *self.week_agg_columns, *_back_cols]
        self.unit_staging_csv_header = """idea_number,face_name,event_int,fisc_title,fund_coin,penny,respect_bit,present_time,bridge,c400_number,yr1_jan1_offset,monthday_distortion,timeline_title,error_message"""
        self.deal_staging_csv_header = """idea_number,face_name,event_int,fisc_title,owner_name,time_int,quota,ledger_depth,error_message"""
        self.cash_staging_csv_header = """idea_number,face_name,event_int,fisc_title,owner_name,acct_name,time_int,amount,error_message"""
        self.hour_staging_csv_header = """idea_number,face_name,event_int,fisc_title,hour_title,cumlative_minute,error_message"""
        self.mont_staging_csv_header = """idea_number,face_name,event_int,fisc_title,month_title,cumlative_day,error_message"""
        self.week_staging_csv_header = """idea_number,face_name,event_int,fisc_title,weekday_title,weekday_order,error_message"""
        self.unit_agg_empty_csv = f"{self.unit_agg_csv_header}\n"
        self.deal_agg_empty_csv = f"{self.deal_agg_csv_header}\n"
        self.cash_agg_empty_csv = f"{self.cash_agg_csv_header}\n"
        self.hour_agg_empty_csv = f"{self.hour_agg_csv_header}\n"
        self.mont_agg_empty_csv = f"{self.mont_agg_csv_header}\n"
        self.week_agg_empty_csv = f"{self.week_agg_csv_header}\n"


def create_init_fisc_prime_files(fiscs_dir: str):
    fiscref = FiscPrimeObjsRef(fiscs_dir)
    xc = FiscPrimeColumnsRef()
    unit_staging_df = DataFrame([], columns=xc.unit_staging_columns)
    deal_staging_df = DataFrame([], columns=xc.deal_staging_columns)
    cash_staging_df = DataFrame([], columns=xc.cash_staging_columns)
    hour_staging_df = DataFrame([], columns=xc.hour_staging_columns)
    mont_staging_df = DataFrame([], columns=xc.mont_staging_columns)
    week_staging_df = DataFrame([], columns=xc.week_staging_columns)
    upsert_sheet(fiscref.unit_excel_path, "staging", unit_staging_df)
    upsert_sheet(fiscref.deal_excel_path, "staging", deal_staging_df)
    upsert_sheet(fiscref.cash_excel_path, "staging", cash_staging_df)
    upsert_sheet(fiscref.hour_excel_path, "staging", hour_staging_df)
    upsert_sheet(fiscref.mont_excel_path, "staging", mont_staging_df)
    upsert_sheet(fiscref.week_excel_path, "staging", week_staging_df)

    unit_agg_df = DataFrame([], columns=xc.unit_agg_columns)
    deal_agg_df = DataFrame([], columns=xc.deal_agg_columns)
    cash_agg_df = DataFrame([], columns=xc.cash_agg_columns)
    hour_agg_df = DataFrame([], columns=xc.hour_agg_columns)
    mont_agg_df = DataFrame([], columns=xc.mont_agg_columns)
    week_agg_df = DataFrame([], columns=xc.week_agg_columns)
    upsert_sheet(fiscref.unit_excel_path, "agg", unit_agg_df)
    upsert_sheet(fiscref.deal_excel_path, "agg", deal_agg_df)
    upsert_sheet(fiscref.cash_excel_path, "agg", cash_agg_df)
    upsert_sheet(fiscref.hour_excel_path, "agg", hour_agg_df)
    upsert_sheet(fiscref.mont_excel_path, "agg", mont_agg_df)
    upsert_sheet(fiscref.week_excel_path, "agg", week_agg_df)


def create_timelineunit_from_prime_data(
    fisc_attrs, fisc_weekday_dict, fisc_month_dict, fisc_hour_dict
):
    if fisc_weekday_dict:
        x_weekday_list = get_sorted_list(fisc_weekday_dict, "weekday_order")
    else:
        x_weekday_list = None
    timeline_config = timeline_config_shop(
        timeline_title=if_nan_return_None(fisc_attrs.get("timeline_title")),
        c400_number=if_nan_return_None(fisc_attrs.get("c400_number")),
        hour_length=None,
        month_length=None,
        weekday_list=x_weekday_list,
        months_list=None,
        monthday_distortion=if_nan_return_None(fisc_attrs.get("monthday_distortion")),
        yr1_jan1_offset=if_nan_return_None(fisc_attrs.get("yr1_jan1_offset")),
    )
    if fisc_month_dict:
        x_month_list = get_sorted_list(fisc_month_dict, "cumlative_day", True)
        timeline_config["months_config"] = x_month_list
    if fisc_hour_dict:
        x_hour_list = get_sorted_list(fisc_hour_dict, "cumlative_minute", True)
        timeline_config["hours_config"] = x_hour_list
    if validate_timeline_config(timeline_config) is False:
        raise ValueError(f"Invalid timeline_config: {timeline_config=}")

    return timelineunit_shop(timeline_config)


def create_fiscunit_jsons_from_prime_files(fisc_mstr_dir: str):
    xp = FiscPrimeObjsRef(fisc_mstr_dir)
    fiscunit_df = pandas_read_excel(xp.unit_excel_path, "agg")
    fiscdeal_df = pandas_read_excel(xp.deal_excel_path, "agg")
    fisccash_df = pandas_read_excel(xp.cash_excel_path, "agg")
    fischour_df = pandas_read_excel(xp.hour_excel_path, "agg")
    fiscmont_df = pandas_read_excel(xp.mont_excel_path, "agg")
    fiscweek_df = pandas_read_excel(xp.week_excel_path, "agg")

    fiscunits_dict = dataframe_to_dict(fiscunit_df, ["fisc_title"])
    fischours_dict = dataframe_to_dict(fischour_df, ["fisc_title", "hour_title"])
    fiscmonts_dict = dataframe_to_dict(fiscmont_df, ["fisc_title", "month_title"])
    fiscweeks_dict = dataframe_to_dict(fiscweek_df, ["fisc_title", "weekday_title"])
    fiscunits = {}
    for fisc_attrs in fiscunits_dict.values():
        x_fisc_title = fisc_attrs.get("fisc_title")
        fisc_timelineunit = create_timelineunit_from_prime_data(
            fisc_attrs=fisc_attrs,
            fisc_weekday_dict=fiscweeks_dict.get(x_fisc_title),
            fisc_month_dict=fiscmonts_dict.get(x_fisc_title),
            fisc_hour_dict=fischours_dict.get(x_fisc_title),
        )

        fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
        fiscunit = fiscunit_shop(
            fisc_title=x_fisc_title,
            fisc_mstr_dir=fisc_mstr_dir,
            timeline=fisc_timelineunit,
            present_time=if_nan_return_None(fisc_attrs.get("present_time")),
            bridge=fisc_attrs.get("bridge"),
            fund_coin=if_nan_return_None(fisc_attrs.get("fund_coin")),
            penny=if_nan_return_None(fisc_attrs.get("penny")),
            respect_bit=if_nan_return_None(fisc_attrs.get("respect_bit")),
            in_memory_journal=True,
        )
        _add_cashpurchases_from_df(fiscunit, fisccash_df)
        _add_dealepisodes_from_df(fiscunit, fiscdeal_df)
        fiscunits[fiscunit.fisc_title] = fiscunit
    for fiscunit in fiscunits.values():
        fisc_filename = "fisc.json"
        fiscunit_dir = create_path(fiscs_dir, fiscunit.fisc_title)
        save_file(fiscunit_dir, fisc_filename, fiscunit.get_json())
