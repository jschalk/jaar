from pandas import DataFrame


# brick_format_00000_fiscalunit_v0_0_0
def get_ex1_br00000_df() -> DataFrame:
    # "c400_number,current_time,fiscal_id,fund_coin,monthday_distortion,penny,respect_bit,road_delimiter,timeline_label,yr1_jan1_offset":
    x_df = DataFrame(
        columns=[
            "c400_number",
            "current_time",
            "fiscal_id",
            "fund_coin",
            "monthday_distortion",
            "penny",
            "respect_bit",
            "road_delimiter",
            "timeline_label",
            "yr1_jan1_offset",
        ]
    )
    x_df.loc[0] = [7, 5500, "music23", 1, 1, 1, 1, "/", "creg", 440640]
    return x_df


# brick_format_00001_fiscal_purview_episode_v0_0_0
def get_ex1_br00001_df() -> DataFrame:
    # "acct_id,fiscal_id,owner_id,quota,time_id":
    x_df = DataFrame(columns=["acct_id", "fiscal_id", "owner_id", "quota", "time_id"])
    x_df.loc[0] = ["Bob", "music23", "Sue", 445, 777]
    return x_df


# brick_format_00002_fiscal_cashbook_v0_0_0
def get_ex1_br00002_df() -> DataFrame:
    # "acct_id,amount,fiscal_id,owner_id,time_id":
    x_df = DataFrame(columns=["acct_id", "amount", "fiscal_id", "owner_id", "time_id"])
    x_df.loc[0] = ["Bob", 888, "music23", "Zia", 777]
    return x_df


# brick_format_00003_fiscal_timeline_hour_v0_0_0
def get_ex1_br00003_df() -> DataFrame:
    # "cumlative_minute,fiscal_id,hour_label":
    x_df = DataFrame(columns=["fiscal_id", "hour_label", "cumlative_minute"])
    x_df.loc[0] = ["music23", "0-12am", 60]
    x_df.loc[1] = ["music23", "1-1am", 120]
    x_df.loc[2] = ["music23", "2-2am", 180]
    x_df.loc[3] = ["music23", "3-3am", 240]
    x_df.loc[4] = ["music23", "4-4am", 300]
    x_df.loc[5] = ["music23", "5-5am", 360]
    x_df.loc[6] = ["music23", "6-6am", 420]
    x_df.loc[7] = ["music23", "7-7am", 480]
    x_df.loc[8] = ["music23", "8-8am", 540]
    x_df.loc[9] = ["music23", "9-9am", 600]
    x_df.loc[10] = ["music23", "10-10am", 660]
    x_df.loc[11] = ["music23", "11-11am", 720]
    x_df.loc[12] = ["music23", "12-12pm", 780]
    x_df.loc[13] = ["music23", "13-1pm", 840]
    x_df.loc[14] = ["music23", "14-2pm", 900]
    x_df.loc[15] = ["music23", "15-3pm", 960]
    x_df.loc[16] = ["music23", "16-4pm", 1020]
    x_df.loc[17] = ["music23", "17-5pm", 1080]
    x_df.loc[18] = ["music23", "18-6pm", 1140]
    x_df.loc[19] = ["music23", "19-7pm", 1200]
    x_df.loc[20] = ["music23", "20-8pm", 1260]
    x_df.loc[21] = ["music23", "21-9pm", 1320]
    x_df.loc[22] = ["music23", "22-10pm", 1380]
    x_df.loc[23] = ["music23", "23-11pm", 1440]
    return x_df


# brick_format_00004_fiscal_timeline_month_v0_0_0
def get_ex1_br00004_df() -> DataFrame:
    # "cumlative_day,fiscal_id,month_label":
    x_df = DataFrame(columns=["fiscal_id", "month_label", "cumlative_day"])
    x_df.loc[0] = ["music23", "March", 31]
    x_df.loc[1] = ["music23", "April", 61]
    x_df.loc[2] = ["music23", "May", 92]
    x_df.loc[3] = ["music23", "June", 122]
    x_df.loc[4] = ["music23", "July", 153]
    x_df.loc[5] = ["music23", "August", 184]
    x_df.loc[6] = ["music23", "September", 214]
    x_df.loc[7] = ["music23", "October", 245]
    x_df.loc[8] = ["music23", "November", 275]
    x_df.loc[9] = ["music23", "December", 306]
    x_df.loc[10] = ["music23", "January", 337]
    x_df.loc[11] = ["music23", "February", 365]
    return x_df


# brick_format_00005_fiscal_timeline_weekday_v0_0_0
def get_ex1_br00005_df() -> DataFrame:
    # "fiscal_id,weekday_label,weekday_order":
    x_df = DataFrame(columns=["fiscal_id", "weekday_label", "weekday_order"])
    x_df.loc[0] = ["music23", "Wednesday", 0]
    x_df.loc[1] = ["music23", "Thursday", 1]
    x_df.loc[2] = ["music23", "Friday", 2]
    x_df.loc[3] = ["music23", "Saturday", 3]
    x_df.loc[4] = ["music23", "Sunday", 4]
    x_df.loc[5] = ["music23", "Monday", 5]
    x_df.loc[6] = ["music23", "Tuesday", 6]
    return x_df
