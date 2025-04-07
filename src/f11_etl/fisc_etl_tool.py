from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.dict_toolbox import (
    get_sorted_list_of_dict_keys as get_sorted_list,
)
from src.f03_chrono.chrono import (
    timeline_config_shop,
    timelineunit_shop,
    validate_timeline_config,
)
from src.f08_fisc.fisc import fiscunit_shop
from src.f10_idea.idea import (
    _add_cashpurchases_from_df,
    _add_dealunits_from_df,
    _add_time_offis_from_df,
)
from src.f10_idea.idea_db_tool import (
    upsert_sheet,
    dataframe_to_dict,
    if_nan_return_None,
)
from pandas import DataFrame, read_excel as pandas_read_excel


class FiscPrimeObjsRef:
    def __init__(self, x_dir: str = ""):
        self.unit_agg_tablename = "fiscunit_agg"
        self.deal_agg_tablename = "fisc_dealunit_agg"
        self.cash_agg_tablename = "fisc_cashbook_agg"
        self.hour_agg_tablename = "fisc_timeline_hour_agg"
        self.mont_agg_tablename = "fisc_timeline_month_agg"
        self.week_agg_tablename = "fisc_timeline_weekday_agg"
        self.offi_agg_tablename = "fisc_timeoffi_agg"
        self.unit_stage_tablename = "fiscunit_staging"
        self.deal_stage_tablename = "fisc_dealunit_staging"
        self.cash_stage_tablename = "fisc_cashbook_staging"
        self.hour_stage_tablename = "fisc_timeline_hour_staging"
        self.mont_stage_tablename = "fisc_timeline_month_staging"
        self.week_stage_tablename = "fisc_timeline_weekday_staging"
        self.offi_stage_tablename = "fisc_timeoffi_staging"
        self.unit_agg_csv_filename = "fiscunit_agg.csv"
        self.deal_agg_csv_filename = "fisc_dealunit_agg.csv"
        self.cash_agg_csv_filename = "fisc_cashbook_agg.csv"
        self.hour_agg_csv_filename = "fisc_timeline_hour_agg.csv"
        self.mont_agg_csv_filename = "fisc_timeline_month_agg.csv"
        self.week_agg_csv_filename = "fisc_timeline_weekday_agg.csv"
        self.offi_agg_csv_filename = "fisc_timeoffi_agg.csv"
        self.unit_agg_csv_path = create_path(x_dir, self.unit_agg_csv_filename)
        self.deal_agg_csv_path = create_path(x_dir, self.deal_agg_csv_filename)
        self.cash_agg_csv_path = create_path(x_dir, self.cash_agg_csv_filename)
        self.hour_agg_csv_path = create_path(x_dir, self.hour_agg_csv_filename)
        self.mont_agg_csv_path = create_path(x_dir, self.mont_agg_csv_filename)
        self.week_agg_csv_path = create_path(x_dir, self.week_agg_csv_filename)
        self.offi_agg_csv_path = create_path(x_dir, self.offi_agg_csv_filename)
        self.unit_stage_csv_filename = "fiscunit_staging.csv"
        self.deal_stage_csv_filename = "fisc_dealunit_staging.csv"
        self.cash_stage_csv_filename = "fisc_cashbook_staging.csv"
        self.hour_stage_csv_filename = "fisc_timeline_hour_staging.csv"
        self.mont_stage_csv_filename = "fisc_timeline_month_staging.csv"
        self.week_stage_csv_filename = "fisc_timeline_weekday_staging.csv"
        self.offi_stage_csv_filename = "fisc_timeoffi_staging.csv"
        self.unit_stage_csv_path = create_path(x_dir, self.unit_stage_csv_filename)
        self.deal_stage_csv_path = create_path(x_dir, self.deal_stage_csv_filename)
        self.cash_stage_csv_path = create_path(x_dir, self.cash_stage_csv_filename)
        self.hour_stage_csv_path = create_path(x_dir, self.hour_stage_csv_filename)
        self.mont_stage_csv_path = create_path(x_dir, self.mont_stage_csv_filename)
        self.week_stage_csv_path = create_path(x_dir, self.week_stage_csv_filename)
        self.offi_stage_csv_path = create_path(x_dir, self.offi_stage_csv_filename)

        self.unit_excel_filename = "fiscunit.xlsx"
        self.deal_excel_filename = "fisc_dealunit.xlsx"
        self.cash_excel_filename = "fisc_cashbook.xlsx"
        self.hour_excel_filename = "fisc_timeline_hour.xlsx"
        self.mont_excel_filename = "fisc_timeline_month.xlsx"
        self.week_excel_filename = "fisc_timeline_weekday.xlsx"
        self.offi_excel_filename = "fisc_timeoffi.xlsx"
        self.unit_excel_path = create_path(x_dir, "fiscunit.xlsx")
        self.deal_excel_path = create_path(x_dir, "fisc_dealunit.xlsx")
        self.cash_excel_path = create_path(x_dir, "fisc_cashbook.xlsx")
        self.hour_excel_path = create_path(x_dir, "fisc_timeline_hour.xlsx")
        self.mont_excel_path = create_path(x_dir, "fisc_timeline_month.xlsx")
        self.week_excel_path = create_path(x_dir, "fisc_timeline_weekday.xlsx")
        self.offi_excel_path = create_path(x_dir, "fisc_timeoffi.xlsx")


class FiscPrimeColumnsRef:
    def __init__(self):
        self.unit_agg_columns = [
            "fisc_title",
            "timeline_title",
            "c400_number",
            "yr1_jan1_offset",
            "monthday_distortion",
            "fund_coin",
            "penny",
            "respect_bit",
            "bridge",
        ]
        self.deal_agg_columns = [
            "fisc_title",
            "owner_name",
            "deal_time",
            "quota",
            "celldepth",
        ]
        self.cash_agg_columns = [
            "fisc_title",
            "owner_name",
            "acct_name",
            "tran_time",
            "amount",
        ]
        self.hour_agg_columns = ["fisc_title", "cumlative_minute", "hour_title"]
        self.mont_agg_columns = ["fisc_title", "cumlative_day", "month_title"]
        self.week_agg_columns = ["fisc_title", "weekday_order", "weekday_title"]
        self.offi_agg_columns = ["fisc_title", "offi_time"]

        _front_cols = ["idea_number", "face_name", "event_int"]
        _back_cols = ["error_message"]
        self.unit_agg_csv_header = "fisc_title,timeline_title,c400_number,yr1_jan1_offset,monthday_distortion,fund_coin,penny,respect_bit,bridge"
        self.deal_agg_csv_header = "fisc_title,owner_name,deal_time,quota,celldepth"
        self.cash_agg_csv_header = "fisc_title,owner_name,acct_name,tran_time,amount"
        self.hour_agg_csv_header = "fisc_title,cumlative_minute,hour_title"
        self.mont_agg_csv_header = "fisc_title,cumlative_day,month_title"
        self.week_agg_csv_header = "fisc_title,weekday_order,weekday_title"
        self.offi_agg_csv_header = "fisc_title,offi_time"
        self.unit_staging_columns = [*_front_cols, *self.unit_agg_columns, *_back_cols]
        self.deal_staging_columns = [*_front_cols, *self.deal_agg_columns, *_back_cols]
        self.cash_staging_columns = [*_front_cols, *self.cash_agg_columns, *_back_cols]
        self.hour_staging_columns = [*_front_cols, *self.hour_agg_columns, *_back_cols]
        self.mont_staging_columns = [*_front_cols, *self.mont_agg_columns, *_back_cols]
        self.week_staging_columns = [*_front_cols, *self.week_agg_columns, *_back_cols]
        self.offi_staging_columns = [*_front_cols, *self.offi_agg_columns, *_back_cols]
        self.unit_staging_csv_header = """idea_number,face_name,event_int,fisc_title,timeline_title,c400_number,yr1_jan1_offset,monthday_distortion,fund_coin,penny,respect_bit,bridge,error_message"""
        self.deal_staging_csv_header = """idea_number,face_name,event_int,fisc_title,owner_name,deal_time,quota,celldepth,error_message"""
        self.cash_staging_csv_header = """idea_number,face_name,event_int,fisc_title,owner_name,acct_name,tran_time,amount,error_message"""
        self.hour_staging_csv_header = """idea_number,face_name,event_int,fisc_title,cumlative_minute,hour_title,error_message"""
        self.mont_staging_csv_header = """idea_number,face_name,event_int,fisc_title,cumlative_day,month_title,error_message"""
        self.week_staging_csv_header = """idea_number,face_name,event_int,fisc_title,weekday_order,weekday_title,error_message"""
        self.offi_staging_csv_header = (
            """idea_number,face_name,event_int,fisc_title,offi_time,error_message"""
        )
        self.unit_agg_empty_csv = f"{self.unit_agg_csv_header}\n"
        self.deal_agg_empty_csv = f"{self.deal_agg_csv_header}\n"
        self.cash_agg_empty_csv = f"{self.cash_agg_csv_header}\n"
        self.hour_agg_empty_csv = f"{self.hour_agg_csv_header}\n"
        self.mont_agg_empty_csv = f"{self.mont_agg_csv_header}\n"
        self.week_agg_empty_csv = f"{self.week_agg_csv_header}\n"
        self.offi_agg_empty_csv = f"{self.offi_agg_csv_header}\n"


def create_init_fisc_prime_files(fiscs_dir: str):
    fiscref = FiscPrimeObjsRef(fiscs_dir)
    xc = FiscPrimeColumnsRef()
    unit_staging_df = DataFrame([], columns=xc.unit_staging_columns)
    deal_staging_df = DataFrame([], columns=xc.deal_staging_columns)
    cash_staging_df = DataFrame([], columns=xc.cash_staging_columns)
    hour_staging_df = DataFrame([], columns=xc.hour_staging_columns)
    mont_staging_df = DataFrame([], columns=xc.mont_staging_columns)
    week_staging_df = DataFrame([], columns=xc.week_staging_columns)
    offi_staging_df = DataFrame([], columns=xc.offi_staging_columns)
    upsert_sheet(fiscref.unit_excel_path, "staging", unit_staging_df)
    upsert_sheet(fiscref.deal_excel_path, "staging", deal_staging_df)
    upsert_sheet(fiscref.cash_excel_path, "staging", cash_staging_df)
    upsert_sheet(fiscref.hour_excel_path, "staging", hour_staging_df)
    upsert_sheet(fiscref.mont_excel_path, "staging", mont_staging_df)
    upsert_sheet(fiscref.week_excel_path, "staging", week_staging_df)
    upsert_sheet(fiscref.offi_excel_path, "staging", offi_staging_df)

    unit_agg_df = DataFrame([], columns=xc.unit_agg_columns)
    deal_agg_df = DataFrame([], columns=xc.deal_agg_columns)
    cash_agg_df = DataFrame([], columns=xc.cash_agg_columns)
    hour_agg_df = DataFrame([], columns=xc.hour_agg_columns)
    mont_agg_df = DataFrame([], columns=xc.mont_agg_columns)
    week_agg_df = DataFrame([], columns=xc.week_agg_columns)
    offi_agg_df = DataFrame([], columns=xc.offi_agg_columns)
    upsert_sheet(fiscref.unit_excel_path, "agg", unit_agg_df)
    upsert_sheet(fiscref.deal_excel_path, "agg", deal_agg_df)
    upsert_sheet(fiscref.cash_excel_path, "agg", cash_agg_df)
    upsert_sheet(fiscref.hour_excel_path, "agg", hour_agg_df)
    upsert_sheet(fiscref.mont_excel_path, "agg", mont_agg_df)
    upsert_sheet(fiscref.week_excel_path, "agg", week_agg_df)
    upsert_sheet(fiscref.offi_excel_path, "agg", offi_agg_df)


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
