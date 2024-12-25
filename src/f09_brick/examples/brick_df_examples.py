from pandas import DataFrame


MUSIC23_STR = "music23"
JEFFY45_STR = "jeffy45"


def get_ex1_br00000_df() -> DataFrame:
    """brick_format_00000_fiscalunit_v0_0_0
    c400_number,current_time,fiscal_id,fund_coin,monthday_distortion,penny,respect_bit,wall,timeline_label,yr1_jan1_offset
    """
    x_df = DataFrame(
        columns=[
            "c400_number",
            "current_time",
            "fiscal_id",
            "fund_coin",
            "monthday_distortion",
            "penny",
            "respect_bit",
            "wall",
            "timeline_label",
            "yr1_jan1_offset",
        ]
    )
    x_df.loc[0] = [7, 5500, MUSIC23_STR, 1, 1, 1, 1, "/", "creg", 440640]
    return x_df


def get_ex1_br00001_df() -> DataFrame:
    """brick_format_00001_fiscal_purview_episode_v0_0_0
    acct_id,fiscal_id,owner_id,quota,time_id"""
    x_df = DataFrame(columns=["acct_id", "fiscal_id", "owner_id", "quota", "time_id"])
    x_df.loc[0] = ["Bob", MUSIC23_STR, "Sue", 445, 777]
    return x_df


def get_ex1_br00002_df() -> DataFrame:
    """brick_format_00002_fiscal_cashbook_v0_0_0
    acct_id,amount,fiscal_id,owner_id,time_id"""
    x_df = DataFrame(columns=["acct_id", "amount", "fiscal_id", "owner_id", "time_id"])
    x_df.loc[0] = ["Bob", 888, MUSIC23_STR, "Zia", 777]
    return x_df


def get_ex1_br00003_df() -> DataFrame:
    """brick_format_00003_fiscal_timeline_hour_v0_0_0
    cumlative_minute,fiscal_id,hour_label"""
    x_df = DataFrame(columns=["fiscal_id", "hour_label", "cumlative_minute"])
    x_df.loc[0] = [MUSIC23_STR, "0-12am", 60]
    x_df.loc[1] = [MUSIC23_STR, "1-1am", 120]
    x_df.loc[2] = [MUSIC23_STR, "2-2am", 180]
    x_df.loc[3] = [MUSIC23_STR, "3-3am", 240]
    x_df.loc[4] = [MUSIC23_STR, "4-4am", 300]
    x_df.loc[5] = [MUSIC23_STR, "5-5am", 360]
    x_df.loc[6] = [MUSIC23_STR, "6-6am", 420]
    x_df.loc[7] = [MUSIC23_STR, "7-7am", 480]
    x_df.loc[8] = [MUSIC23_STR, "8-8am", 540]
    x_df.loc[9] = [MUSIC23_STR, "9-9am", 600]
    x_df.loc[10] = [MUSIC23_STR, "10-10am", 660]
    x_df.loc[11] = [MUSIC23_STR, "11-11am", 720]
    x_df.loc[12] = [MUSIC23_STR, "12-12pm", 780]
    x_df.loc[13] = [MUSIC23_STR, "13-1pm", 840]
    x_df.loc[14] = [MUSIC23_STR, "14-2pm", 900]
    x_df.loc[15] = [MUSIC23_STR, "15-3pm", 960]
    x_df.loc[16] = [MUSIC23_STR, "16-4pm", 1020]
    x_df.loc[17] = [MUSIC23_STR, "17-5pm", 1080]
    x_df.loc[18] = [MUSIC23_STR, "18-6pm", 1140]
    x_df.loc[19] = [MUSIC23_STR, "19-7pm", 1200]
    x_df.loc[20] = [MUSIC23_STR, "20-8pm", 1260]
    x_df.loc[21] = [MUSIC23_STR, "21-9pm", 1320]
    x_df.loc[22] = [MUSIC23_STR, "22-10pm", 1380]
    x_df.loc[23] = [MUSIC23_STR, "23-11pm", 1440]
    return x_df


def get_ex1_br00004_df() -> DataFrame:
    """brick_format_00004_fiscal_timeline_month_v0_0_0
    cumlative_day,fiscal_id,month_label"""
    x_df = DataFrame(columns=["fiscal_id", "month_label", "cumlative_day"])
    x_df.loc[0] = [MUSIC23_STR, "March", 31]
    x_df.loc[1] = [MUSIC23_STR, "April", 61]
    x_df.loc[2] = [MUSIC23_STR, "May", 92]
    x_df.loc[3] = [MUSIC23_STR, "June", 122]
    x_df.loc[4] = [MUSIC23_STR, "July", 153]
    x_df.loc[5] = [MUSIC23_STR, "August", 184]
    x_df.loc[6] = [MUSIC23_STR, "September", 214]
    x_df.loc[7] = [MUSIC23_STR, "October", 245]
    x_df.loc[8] = [MUSIC23_STR, "November", 275]
    x_df.loc[9] = [MUSIC23_STR, "December", 306]
    x_df.loc[10] = [MUSIC23_STR, "January", 337]
    x_df.loc[11] = [MUSIC23_STR, "February", 365]
    return x_df


def get_ex1_br00005_df() -> DataFrame:
    """brick_format_00005_fiscal_timeline_weekday_v0_0_0
    fiscal_id,weekday_label,weekday_order"""
    x_df = DataFrame(columns=["fiscal_id", "weekday_label", "weekday_order"])
    x_df.loc[0] = [MUSIC23_STR, "Wednesday", 0]
    x_df.loc[1] = [MUSIC23_STR, "Thursday", 1]
    x_df.loc[2] = [MUSIC23_STR, "Friday", 2]
    x_df.loc[3] = [MUSIC23_STR, "Saturday", 3]
    x_df.loc[4] = [MUSIC23_STR, "Sunday", 4]
    x_df.loc[5] = [MUSIC23_STR, "Monday", 5]
    x_df.loc[6] = [MUSIC23_STR, "Tuesday", 6]
    return x_df


def get_ex2_br00000_df() -> DataFrame:
    """brick_format_00000_fiscalunit_v0_0_0
    c400_number,current_time,fiscal_id,fund_coin,monthday_distortion,penny,respect_bit,wall,timeline_label,yr1_jan1_offset
    """
    x_df = DataFrame(
        columns=[
            "c400_number",
            "current_time",
            "fiscal_id",
            "fund_coin",
            "monthday_distortion",
            "penny",
            "respect_bit",
            "wall",
            "timeline_label",
            "yr1_jan1_offset",
        ]
    )
    x_df.loc[0] = [7, 5500, MUSIC23_STR, 1, 1, 1, 1, "/", "creg", 440640]
    x_df.loc[1] = [25, 444, JEFFY45_STR, 1, 0, 1, 1, ",", "five", 1683478080]
    return x_df


def get_ex2_br00001_df() -> DataFrame:
    """brick_format_00001_fiscal_purview_episode_v0_0_0
    acct_id,fiscal_id,owner_id,quota,time_id"""
    x_df = DataFrame(columns=["acct_id", "fiscal_id", "owner_id", "quota", "time_id"])
    x_df.loc[0] = ["Bob", MUSIC23_STR, "Sue", 445, 777]
    x_df.loc[1] = ["Yao", MUSIC23_STR, "Bob", 332, 999]
    x_df.loc[2] = ["Bob", MUSIC23_STR, "Yao", 700, 222]
    x_df.loc[3] = ["Yao", JEFFY45_STR, "Xio", 332, 999]
    x_df.loc[4] = ["Bob", JEFFY45_STR, "Zia", 700, 222]
    return x_df


def get_ex2_br00002_df() -> DataFrame:
    """brick_format_00002_fiscal_cashbook_v0_0_0
    acct_id,amount,fiscal_id,owner_id,time_id"""
    x_df = DataFrame(columns=["acct_id", "amount", "fiscal_id", "owner_id", "time_id"])
    x_df.loc[0] = ["Bob", 888, MUSIC23_STR, "Zia", 777]
    x_df.loc[1] = ["Zia", 234, MUSIC23_STR, "Sue", 999]
    x_df.loc[2] = ["Zia", 888, MUSIC23_STR, "Bob", 777]
    x_df.loc[3] = ["Zia", 234, MUSIC23_STR, "Yao", 999]
    x_df.loc[4] = ["Zia", 234, JEFFY45_STR, "Yao", 999]
    return x_df


def get_ex2_br00003_df() -> DataFrame:
    """brick_format_00003_fiscal_timeline_hour_v0_0_0
    cumlative_minute,fiscal_id,hour_label"""
    x_df = DataFrame(columns=["fiscal_id", "hour_label", "cumlative_minute"])
    x_df.loc[0] = [MUSIC23_STR, "0-12am", 60]
    x_df.loc[1] = [MUSIC23_STR, "1-1am", 120]
    x_df.loc[2] = [MUSIC23_STR, "2-2am", 180]
    x_df.loc[3] = [MUSIC23_STR, "3-3am", 240]
    x_df.loc[4] = [MUSIC23_STR, "4-4am", 300]
    x_df.loc[5] = [MUSIC23_STR, "5-5am", 360]
    x_df.loc[6] = [MUSIC23_STR, "6-6am", 420]
    x_df.loc[7] = [MUSIC23_STR, "7-7am", 480]
    x_df.loc[8] = [MUSIC23_STR, "8-8am", 540]
    x_df.loc[9] = [MUSIC23_STR, "9-9am", 600]
    x_df.loc[10] = [MUSIC23_STR, "10-10am", 660]
    x_df.loc[11] = [MUSIC23_STR, "11-11am", 720]
    x_df.loc[12] = [MUSIC23_STR, "12-12pm", 780]
    x_df.loc[13] = [MUSIC23_STR, "13-1pm", 840]
    x_df.loc[14] = [MUSIC23_STR, "14-2pm", 900]
    x_df.loc[15] = [MUSIC23_STR, "15-3pm", 960]
    x_df.loc[16] = [MUSIC23_STR, "16-4pm", 1020]
    x_df.loc[17] = [MUSIC23_STR, "17-5pm", 1080]
    x_df.loc[18] = [MUSIC23_STR, "18-6pm", 1140]
    x_df.loc[19] = [MUSIC23_STR, "19-7pm", 1200]
    x_df.loc[20] = [MUSIC23_STR, "20-8pm", 1260]
    x_df.loc[21] = [MUSIC23_STR, "21-9pm", 1320]
    x_df.loc[22] = [MUSIC23_STR, "22-10pm", 1380]
    x_df.loc[23] = [MUSIC23_STR, "23-11pm", 1440]
    x_df.loc[24] = [JEFFY45_STR, "0hr", 72]
    x_df.loc[25] = [JEFFY45_STR, "1hr", 144]
    x_df.loc[26] = [JEFFY45_STR, "2hr", 216]
    x_df.loc[27] = [JEFFY45_STR, "3hr", 288]
    x_df.loc[28] = [JEFFY45_STR, "4hr", 360]
    x_df.loc[29] = [JEFFY45_STR, "5hr", 432]
    x_df.loc[30] = [JEFFY45_STR, "6hr", 504]
    x_df.loc[31] = [JEFFY45_STR, "7hr", 576]
    x_df.loc[32] = [JEFFY45_STR, "8hr", 648]
    x_df.loc[33] = [JEFFY45_STR, "9hr", 720]
    x_df.loc[34] = [JEFFY45_STR, "10hr", 792]
    x_df.loc[35] = [JEFFY45_STR, "11hr", 864]
    x_df.loc[36] = [JEFFY45_STR, "12hr", 936]
    x_df.loc[37] = [JEFFY45_STR, "13hr", 1008]
    x_df.loc[38] = [JEFFY45_STR, "14hr", 1080]
    x_df.loc[39] = [JEFFY45_STR, "15hr", 1152]
    x_df.loc[40] = [JEFFY45_STR, "16hr", 1224]
    x_df.loc[41] = [JEFFY45_STR, "17hr", 1296]
    x_df.loc[42] = [JEFFY45_STR, "18hr", 1368]
    x_df.loc[43] = [JEFFY45_STR, "19hr", 1440]
    return x_df


def get_ex2_br00004_df() -> DataFrame:
    """brick_format_00004_fiscal_timeline_month_v0_0_0
    cumlative_day,fiscal_id,month_label"""
    x_df = DataFrame(columns=["fiscal_id", "month_label", "cumlative_day"])
    x_df.loc[0] = [MUSIC23_STR, "March", 31]
    x_df.loc[1] = [MUSIC23_STR, "April", 61]
    x_df.loc[2] = [MUSIC23_STR, "May", 92]
    x_df.loc[3] = [MUSIC23_STR, "June", 122]
    x_df.loc[4] = [MUSIC23_STR, "July", 153]
    x_df.loc[5] = [MUSIC23_STR, "August", 184]
    x_df.loc[6] = [MUSIC23_STR, "September", 214]
    x_df.loc[7] = [MUSIC23_STR, "October", 245]
    x_df.loc[8] = [MUSIC23_STR, "November", 275]
    x_df.loc[9] = [MUSIC23_STR, "December", 306]
    x_df.loc[10] = [MUSIC23_STR, "January", 337]
    x_df.loc[11] = [MUSIC23_STR, "February", 365]
    x_df.loc[12] = (JEFFY45_STR, "Fresh", 25)
    x_df.loc[13] = (JEFFY45_STR, "Geo", 50)
    x_df.loc[14] = (JEFFY45_STR, "Holocene", 75)
    x_df.loc[15] = (JEFFY45_STR, "Iguana", 100)
    x_df.loc[16] = (JEFFY45_STR, "Jinping", 125)
    x_df.loc[17] = (JEFFY45_STR, "Keel", 150)
    x_df.loc[18] = (JEFFY45_STR, "Lebron", 175)
    x_df.loc[19] = (JEFFY45_STR, "Mikayla", 200)
    x_df.loc[20] = (JEFFY45_STR, "Ninon", 225)
    x_df.loc[21] = (JEFFY45_STR, "Obama", 250)
    x_df.loc[22] = (JEFFY45_STR, "Preston", 275)
    x_df.loc[23] = (JEFFY45_STR, "Quorum", 300)
    x_df.loc[24] = (JEFFY45_STR, "RioGrande", 325)
    x_df.loc[25] = (JEFFY45_STR, "Simon", 350)
    x_df.loc[26] = [JEFFY45_STR, "Trump", 365]
    return x_df


def get_ex2_br00005_df() -> DataFrame:
    """brick_format_00005_fiscal_timeline_weekday_v0_0_0
    fiscal_id,weekday_label,weekday_order"""
    x_df = DataFrame(columns=["fiscal_id", "weekday_label", "weekday_order"])
    x_df.loc[0] = [MUSIC23_STR, "Wednesday", 0]
    x_df.loc[1] = [MUSIC23_STR, "Thursday", 1]
    x_df.loc[2] = [MUSIC23_STR, "Friday", 2]
    x_df.loc[3] = [MUSIC23_STR, "Saturday", 3]
    x_df.loc[4] = [MUSIC23_STR, "Sunday", 4]
    x_df.loc[5] = [MUSIC23_STR, "Monday", 5]
    x_df.loc[6] = [MUSIC23_STR, "Tuesday", 6]
    x_df.loc[7] = [JEFFY45_STR, "Anaday", 0]
    x_df.loc[8] = [JEFFY45_STR, "Baileyday", 1]
    x_df.loc[9] = [JEFFY45_STR, "Chiday", 2]
    x_df.loc[10] = [JEFFY45_STR, "Danceday", 3]
    x_df.loc[11] = [JEFFY45_STR, "Elonday", 4]
    return x_df
