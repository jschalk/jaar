from src.a00_data_toolbox.file_toolbox import create_path


class FiscPrimeObjsRef:
    def __init__(self, x_dir: str = ""):
        self.unit_agg_tablename = "fiscunit_agg"
        self.deal_agg_tablename = "fisc_dealunit_agg"
        self.cash_agg_tablename = "fisc_cashbook_agg"
        self.hour_agg_tablename = "fisc_timeline_hour_agg"
        self.mont_agg_tablename = "fisc_timeline_month_agg"
        self.week_agg_tablename = "fisc_timeline_weekday_agg"
        self.offi_agg_tablename = "fisc_timeoffi_agg"
        self.unit_raw_tablename = "fiscunit_raw"
        self.deal_raw_tablename = "fisc_dealunit_raw"
        self.cash_raw_tablename = "fisc_cashbook_raw"
        self.hour_raw_tablename = "fisc_timeline_hour_raw"
        self.mont_raw_tablename = "fisc_timeline_month_raw"
        self.week_raw_tablename = "fisc_timeline_weekday_raw"
        self.offi_raw_tablename = "fisc_timeoffi_raw"
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
        self.unit_raw_csv_filename = "fiscunit_raw.csv"
        self.deal_raw_csv_filename = "fisc_dealunit_raw.csv"
        self.cash_raw_csv_filename = "fisc_cashbook_raw.csv"
        self.hour_raw_csv_filename = "fisc_timeline_hour_raw.csv"
        self.mont_raw_csv_filename = "fisc_timeline_month_raw.csv"
        self.week_raw_csv_filename = "fisc_timeline_weekday_raw.csv"
        self.offi_raw_csv_filename = "fisc_timeoffi_raw.csv"
        self.unit_raw_csv_path = create_path(x_dir, self.unit_raw_csv_filename)
        self.deal_raw_csv_path = create_path(x_dir, self.deal_raw_csv_filename)
        self.cash_raw_csv_path = create_path(x_dir, self.cash_raw_csv_filename)
        self.hour_raw_csv_path = create_path(x_dir, self.hour_raw_csv_filename)
        self.mont_raw_csv_path = create_path(x_dir, self.mont_raw_csv_filename)
        self.week_raw_csv_path = create_path(x_dir, self.week_raw_csv_filename)
        self.offi_raw_csv_path = create_path(x_dir, self.offi_raw_csv_filename)

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
            "fisc_label",
            "timeline_label",
            "c400_number",
            "yr1_jan1_offset",
            "monthday_distortion",
            "fund_coin",
            "penny",
            "respect_bit",
            "bridge",
            "job_listen_rotations",
        ]
        self.deal_agg_columns = [
            "fisc_label",
            "owner_name",
            "deal_time",
            "quota",
            "celldepth",
        ]
        self.cash_agg_columns = [
            "fisc_label",
            "owner_name",
            "acct_name",
            "tran_time",
            "amount",
        ]
        self.hour_agg_columns = ["fisc_label", "cumlative_minute", "hour_label"]
        self.mont_agg_columns = ["fisc_label", "cumlative_day", "month_label"]
        self.week_agg_columns = ["fisc_label", "weekday_order", "weekday_label"]
        self.offi_agg_columns = ["fisc_label", "offi_time"]

        _front_cols = ["creed_number", "event_int", "face_name"]
        _back_cols = ["error_message"]
        self.unit_agg_csv_header = "fisc_label,timeline_label,c400_number,yr1_jan1_offset,monthday_distortion,fund_coin,penny,respect_bit,bridge,job_listen_rotations"
        self.deal_agg_csv_header = "fisc_label,owner_name,deal_time,quota,celldepth"
        self.cash_agg_csv_header = "fisc_label,owner_name,acct_name,tran_time,amount"
        self.hour_agg_csv_header = "fisc_label,cumlative_minute,hour_label"
        self.mont_agg_csv_header = "fisc_label,cumlative_day,month_label"
        self.week_agg_csv_header = "fisc_label,weekday_order,weekday_label"
        self.offi_agg_csv_header = "fisc_label,offi_time"
        self.unit_raw_columns = [*_front_cols, *self.unit_agg_columns, *_back_cols]
        self.deal_raw_columns = [*_front_cols, *self.deal_agg_columns, *_back_cols]
        self.cash_raw_columns = [*_front_cols, *self.cash_agg_columns, *_back_cols]
        self.hour_raw_columns = [*_front_cols, *self.hour_agg_columns, *_back_cols]
        self.mont_raw_columns = [*_front_cols, *self.mont_agg_columns, *_back_cols]
        self.week_raw_columns = [*_front_cols, *self.week_agg_columns, *_back_cols]
        self.offi_raw_columns = [*_front_cols, *self.offi_agg_columns, *_back_cols]
        self.unit_raw_csv_header = """creed_number,event_int,face_name,fisc_label,timeline_label,c400_number,yr1_jan1_offset,monthday_distortion,fund_coin,penny,respect_bit,bridge,job_listen_rotations,error_message"""
        self.deal_raw_csv_header = """creed_number,event_int,face_name,fisc_label,owner_name,deal_time,quota,celldepth,error_message"""
        self.cash_raw_csv_header = """creed_number,event_int,face_name,fisc_label,owner_name,acct_name,tran_time,amount,error_message"""
        self.hour_raw_csv_header = """creed_number,event_int,face_name,fisc_label,cumlative_minute,hour_label,error_message"""
        self.mont_raw_csv_header = """creed_number,event_int,face_name,fisc_label,cumlative_day,month_label,error_message"""
        self.week_raw_csv_header = """creed_number,event_int,face_name,fisc_label,weekday_order,weekday_label,error_message"""
        self.offi_raw_csv_header = (
            """creed_number,event_int,face_name,fisc_label,offi_time,error_message"""
        )
        self.unit_agg_empty_csv = f"{self.unit_agg_csv_header}\n"
        self.deal_agg_empty_csv = f"{self.deal_agg_csv_header}\n"
        self.cash_agg_empty_csv = f"{self.cash_agg_csv_header}\n"
        self.hour_agg_empty_csv = f"{self.hour_agg_csv_header}\n"
        self.mont_agg_empty_csv = f"{self.mont_agg_csv_header}\n"
        self.week_agg_empty_csv = f"{self.week_agg_csv_header}\n"
        self.offi_agg_empty_csv = f"{self.offi_agg_csv_header}\n"


# def create_init_fisc_prime_files(fiscs_dir: str):
#     fiscref = FiscPrimeObjsRef(fiscs_dir)
#     xc = FiscPrimeColumnsRef()
#     unit_raw_df = DataFrame([], columns=xc.unit_raw_columns)
#     deal_raw_df = DataFrame([], columns=xc.deal_raw_columns)
#     cash_raw_df = DataFrame([], columns=xc.cash_raw_columns)
#     hour_raw_df = DataFrame([], columns=xc.hour_raw_columns)
#     mont_raw_df = DataFrame([], columns=xc.mont_raw_columns)
#     week_raw_df = DataFrame([], columns=xc.week_raw_columns)
#     offi_raw_df = DataFrame([], columns=xc.offi_raw_columns)
#     upsert_sheet(fiscref.unit_excel_path, "raw", unit_raw_df)
#     upsert_sheet(fiscref.deal_excel_path, "raw", deal_raw_df)
#     upsert_sheet(fiscref.cash_excel_path, "raw", cash_raw_df)
#     upsert_sheet(fiscref.hour_excel_path, "raw", hour_raw_df)
#     upsert_sheet(fiscref.mont_excel_path, "raw", mont_raw_df)
#     upsert_sheet(fiscref.week_excel_path, "raw", week_raw_df)
#     upsert_sheet(fiscref.offi_excel_path, "raw", offi_raw_df)

#     unit_agg_df = DataFrame([], columns=xc.unit_agg_columns)
#     deal_agg_df = DataFrame([], columns=xc.deal_agg_columns)
#     cash_agg_df = DataFrame([], columns=xc.cash_agg_columns)
#     hour_agg_df = DataFrame([], columns=xc.hour_agg_columns)
#     mont_agg_df = DataFrame([], columns=xc.mont_agg_columns)
#     week_agg_df = DataFrame([], columns=xc.week_agg_columns)
#     offi_agg_df = DataFrame([], columns=xc.offi_agg_columns)
#     upsert_sheet(fiscref.unit_excel_path, "agg", unit_agg_df)
#     upsert_sheet(fiscref.deal_excel_path, "agg", deal_agg_df)
#     upsert_sheet(fiscref.cash_excel_path, "agg", cash_agg_df)
#     upsert_sheet(fiscref.hour_excel_path, "agg", hour_agg_df)
#     upsert_sheet(fiscref.mont_excel_path, "agg", mont_agg_df)
#     upsert_sheet(fiscref.week_excel_path, "agg", week_agg_df)
#     upsert_sheet(fiscref.offi_excel_path, "agg", offi_agg_df)


# def create_timelineunit_from_prime_data(
#     fisc_attrs, fisc_weekday_dict, fisc_month_dict, fisc_hour_dict
# ):
#     if fisc_weekday_dict:
#         x_weekday_list = get_sorted_list(fisc_weekday_dict, "weekday_order")
#     else:
#         x_weekday_list = None
#     timeline_config = timeline_config_shop(
#         timeline_label=if_nan_return_None(fisc_attrs.get("timeline_label")),
#         c400_number=if_nan_return_None(fisc_attrs.get("c400_number")),
#         hour_length=None,
#         month_length=None,
#         weekday_list=x_weekday_list,
#         months_list=None,
#         monthday_distortion=if_nan_return_None(fisc_attrs.get("monthday_distortion")),
#         yr1_jan1_offset=if_nan_return_None(fisc_attrs.get("yr1_jan1_offset")),
#     )
#     if fisc_month_dict:
#         x_month_list = get_sorted_list(fisc_month_dict, "cumlative_day", True)
#         timeline_config["months_config"] = x_month_list
#     if fisc_hour_dict:
#         x_hour_list = get_sorted_list(fisc_hour_dict, "cumlative_minute", True)
#         timeline_config["hours_config"] = x_hour_list
#     if validate_timeline_config(timeline_config) is False:
#         raise ValueError(f"Invalid timeline_config: {timeline_config=}")
#     return timelineunit_shop(timeline_config)
