from pandas import DataFrame


ACCORD23_STR = "accord23"
JEFFY45_STR = "jeffy45"


def get_ex1_br00000_df() -> DataFrame:
    """idea_format_00000_fiscunit_v0_0_0
    c400_number,present_time,fisc_title,fund_coin,monthday_distortion,penny,respect_bit,bridge,timeline_title,yr1_jan1_offset
    """
    x_df = DataFrame(
        columns=[
            "c400_number",
            "present_time",
            "fisc_title",
            "fund_coin",
            "monthday_distortion",
            "penny",
            "respect_bit",
            "bridge",
            "timeline_title",
            "yr1_jan1_offset",
        ]
    )
    x_df.loc[0] = [7, 5500, ACCORD23_STR, 1, 1, 1, 1, "/", "creg", 440640]
    return x_df


def get_ex1_br00001_df() -> DataFrame:
    """idea_format_00001_fisc_dealunit_v0_0_0
    acct_name,fisc_title,owner_name,quota,time_int"""
    x_df = DataFrame(
        columns=["acct_name", "fisc_title", "owner_name", "quota", "time_int"]
    )
    x_df.loc[0] = ["Bob", ACCORD23_STR, "Sue", 445, 777]
    return x_df


def get_ex1_br00002_df() -> DataFrame:
    """idea_format_00002_fisc_cashbook_v0_0_0
    acct_name,amount,fisc_title,owner_name,time_int"""
    x_df = DataFrame(
        columns=["acct_name", "amount", "fisc_title", "owner_name", "time_int"]
    )
    x_df.loc[0] = ["Bob", 888, ACCORD23_STR, "Zia", 777]
    return x_df


def get_ex1_br00003_df() -> DataFrame:
    """idea_format_00003_fisc_timeline_hour_v0_0_0
    cumlative_minute,fisc_title,hour_title"""
    x_df = DataFrame(columns=["fisc_title", "hour_title", "cumlative_minute"])
    x_df.loc[0] = [ACCORD23_STR, "0-12am", 60]
    x_df.loc[1] = [ACCORD23_STR, "1-1am", 120]
    x_df.loc[2] = [ACCORD23_STR, "2-2am", 180]
    x_df.loc[3] = [ACCORD23_STR, "3-3am", 240]
    x_df.loc[4] = [ACCORD23_STR, "4-4am", 300]
    x_df.loc[5] = [ACCORD23_STR, "5-5am", 360]
    x_df.loc[6] = [ACCORD23_STR, "6-6am", 420]
    x_df.loc[7] = [ACCORD23_STR, "7-7am", 480]
    x_df.loc[8] = [ACCORD23_STR, "8-8am", 540]
    x_df.loc[9] = [ACCORD23_STR, "9-9am", 600]
    x_df.loc[10] = [ACCORD23_STR, "10-10am", 660]
    x_df.loc[11] = [ACCORD23_STR, "11-11am", 720]
    x_df.loc[12] = [ACCORD23_STR, "12-12pm", 780]
    x_df.loc[13] = [ACCORD23_STR, "13-1pm", 840]
    x_df.loc[14] = [ACCORD23_STR, "14-2pm", 900]
    x_df.loc[15] = [ACCORD23_STR, "15-3pm", 960]
    x_df.loc[16] = [ACCORD23_STR, "16-4pm", 1020]
    x_df.loc[17] = [ACCORD23_STR, "17-5pm", 1080]
    x_df.loc[18] = [ACCORD23_STR, "18-6pm", 1140]
    x_df.loc[19] = [ACCORD23_STR, "19-7pm", 1200]
    x_df.loc[20] = [ACCORD23_STR, "20-8pm", 1260]
    x_df.loc[21] = [ACCORD23_STR, "21-9pm", 1320]
    x_df.loc[22] = [ACCORD23_STR, "22-10pm", 1380]
    x_df.loc[23] = [ACCORD23_STR, "23-11pm", 1440]
    return x_df


def get_ex1_br00004_df() -> DataFrame:
    """idea_format_00004_fisc_timeline_month_v0_0_0
    cumlative_day,fisc_title,month_title"""
    x_df = DataFrame(columns=["fisc_title", "month_title", "cumlative_day"])
    x_df.loc[0] = [ACCORD23_STR, "March", 31]
    x_df.loc[1] = [ACCORD23_STR, "April", 61]
    x_df.loc[2] = [ACCORD23_STR, "May", 92]
    x_df.loc[3] = [ACCORD23_STR, "June", 122]
    x_df.loc[4] = [ACCORD23_STR, "July", 153]
    x_df.loc[5] = [ACCORD23_STR, "August", 184]
    x_df.loc[6] = [ACCORD23_STR, "September", 214]
    x_df.loc[7] = [ACCORD23_STR, "October", 245]
    x_df.loc[8] = [ACCORD23_STR, "November", 275]
    x_df.loc[9] = [ACCORD23_STR, "December", 306]
    x_df.loc[10] = [ACCORD23_STR, "January", 337]
    x_df.loc[11] = [ACCORD23_STR, "February", 365]
    return x_df


def get_ex1_br00005_df() -> DataFrame:
    """idea_format_00005_fisc_timeline_weekday_v0_0_0
    fisc_title,weekday_title,weekday_order"""
    x_df = DataFrame(columns=["fisc_title", "weekday_title", "weekday_order"])
    x_df.loc[0] = [ACCORD23_STR, "Wednesday", 0]
    x_df.loc[1] = [ACCORD23_STR, "Thursday", 1]
    x_df.loc[2] = [ACCORD23_STR, "Friday", 2]
    x_df.loc[3] = [ACCORD23_STR, "Saturday", 3]
    x_df.loc[4] = [ACCORD23_STR, "Sunday", 4]
    x_df.loc[5] = [ACCORD23_STR, "Monday", 5]
    x_df.loc[6] = [ACCORD23_STR, "Tuesday", 6]
    return x_df


def get_ex2_br00000_df() -> DataFrame:
    """idea_format_00000_fiscunit_v0_0_0
    c400_number,present_time,fisc_title,fund_coin,monthday_distortion,penny,respect_bit,bridge,timeline_title,yr1_jan1_offset
    """
    x_df = DataFrame(
        columns=[
            "c400_number",
            "present_time",
            "fisc_title",
            "fund_coin",
            "monthday_distortion",
            "penny",
            "respect_bit",
            "bridge",
            "timeline_title",
            "yr1_jan1_offset",
        ]
    )
    x_df.loc[0] = [7, 5500, ACCORD23_STR, 1, 1, 1, 1, "/", "creg", 440640]
    x_df.loc[1] = [25, 444, JEFFY45_STR, 1, 0, 1, 1, ",", "five", 1683478080]
    return x_df


def get_ex2_br00001_df() -> DataFrame:
    """idea_format_00001_fisc_dealunit_v0_0_0
    acct_name,fisc_title,owner_name,quota,time_int"""
    x_df = DataFrame(
        columns=["acct_name", "fisc_title", "owner_name", "quota", "time_int"]
    )
    x_df.loc[0] = ["Bob", ACCORD23_STR, "Sue", 445, 777]
    x_df.loc[1] = ["Yao", ACCORD23_STR, "Bob", 332, 999]
    x_df.loc[2] = ["Bob", ACCORD23_STR, "Yao", 700, 222]
    x_df.loc[3] = ["Yao", JEFFY45_STR, "Xio", 332, 999]
    x_df.loc[4] = ["Bob", JEFFY45_STR, "Zia", 700, 222]
    return x_df


def get_ex2_br00002_df() -> DataFrame:
    """idea_format_00002_fisc_cashbook_v0_0_0
    acct_name,amount,fisc_title,owner_name,time_int"""
    x_df = DataFrame(
        columns=["acct_name", "amount", "fisc_title", "owner_name", "time_int"]
    )
    x_df.loc[0] = ["Bob", 888, ACCORD23_STR, "Zia", 777]
    x_df.loc[1] = ["Zia", 234, ACCORD23_STR, "Sue", 999]
    x_df.loc[2] = ["Zia", 888, ACCORD23_STR, "Bob", 777]
    x_df.loc[3] = ["Zia", 234, ACCORD23_STR, "Yao", 999]
    x_df.loc[4] = ["Zia", 234, JEFFY45_STR, "Yao", 999]
    return x_df


def get_ex2_br00003_df() -> DataFrame:
    """idea_format_00003_fisc_timeline_hour_v0_0_0
    cumlative_minute,fisc_title,hour_title"""
    x_df = DataFrame(columns=["fisc_title", "hour_title", "cumlative_minute"])
    x_df.loc[0] = [ACCORD23_STR, "0-12am", 60]
    x_df.loc[1] = [ACCORD23_STR, "1-1am", 120]
    x_df.loc[2] = [ACCORD23_STR, "2-2am", 180]
    x_df.loc[3] = [ACCORD23_STR, "3-3am", 240]
    x_df.loc[4] = [ACCORD23_STR, "4-4am", 300]
    x_df.loc[5] = [ACCORD23_STR, "5-5am", 360]
    x_df.loc[6] = [ACCORD23_STR, "6-6am", 420]
    x_df.loc[7] = [ACCORD23_STR, "7-7am", 480]
    x_df.loc[8] = [ACCORD23_STR, "8-8am", 540]
    x_df.loc[9] = [ACCORD23_STR, "9-9am", 600]
    x_df.loc[10] = [ACCORD23_STR, "10-10am", 660]
    x_df.loc[11] = [ACCORD23_STR, "11-11am", 720]
    x_df.loc[12] = [ACCORD23_STR, "12-12pm", 780]
    x_df.loc[13] = [ACCORD23_STR, "13-1pm", 840]
    x_df.loc[14] = [ACCORD23_STR, "14-2pm", 900]
    x_df.loc[15] = [ACCORD23_STR, "15-3pm", 960]
    x_df.loc[16] = [ACCORD23_STR, "16-4pm", 1020]
    x_df.loc[17] = [ACCORD23_STR, "17-5pm", 1080]
    x_df.loc[18] = [ACCORD23_STR, "18-6pm", 1140]
    x_df.loc[19] = [ACCORD23_STR, "19-7pm", 1200]
    x_df.loc[20] = [ACCORD23_STR, "20-8pm", 1260]
    x_df.loc[21] = [ACCORD23_STR, "21-9pm", 1320]
    x_df.loc[22] = [ACCORD23_STR, "22-10pm", 1380]
    x_df.loc[23] = [ACCORD23_STR, "23-11pm", 1440]
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
    """idea_format_00004_fisc_timeline_month_v0_0_0
    cumlative_day,fisc_title,month_title"""
    x_df = DataFrame(columns=["fisc_title", "month_title", "cumlative_day"])
    x_df.loc[0] = [ACCORD23_STR, "March", 31]
    x_df.loc[1] = [ACCORD23_STR, "April", 61]
    x_df.loc[2] = [ACCORD23_STR, "May", 92]
    x_df.loc[3] = [ACCORD23_STR, "June", 122]
    x_df.loc[4] = [ACCORD23_STR, "July", 153]
    x_df.loc[5] = [ACCORD23_STR, "August", 184]
    x_df.loc[6] = [ACCORD23_STR, "September", 214]
    x_df.loc[7] = [ACCORD23_STR, "October", 245]
    x_df.loc[8] = [ACCORD23_STR, "November", 275]
    x_df.loc[9] = [ACCORD23_STR, "December", 306]
    x_df.loc[10] = [ACCORD23_STR, "January", 337]
    x_df.loc[11] = [ACCORD23_STR, "February", 365]
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
    """idea_format_00005_fisc_timeline_weekday_v0_0_0
    fisc_title,weekday_title,weekday_order"""
    x_df = DataFrame(columns=["fisc_title", "weekday_title", "weekday_order"])
    x_df.loc[0] = [ACCORD23_STR, "Wednesday", 0]
    x_df.loc[1] = [ACCORD23_STR, "Thursday", 1]
    x_df.loc[2] = [ACCORD23_STR, "Friday", 2]
    x_df.loc[3] = [ACCORD23_STR, "Saturday", 3]
    x_df.loc[4] = [ACCORD23_STR, "Sunday", 4]
    x_df.loc[5] = [ACCORD23_STR, "Monday", 5]
    x_df.loc[6] = [ACCORD23_STR, "Tuesday", 6]
    x_df.loc[7] = [JEFFY45_STR, "Anaday", 0]
    x_df.loc[8] = [JEFFY45_STR, "Baileyday", 1]
    x_df.loc[9] = [JEFFY45_STR, "Chiday", 2]
    x_df.loc[10] = [JEFFY45_STR, "Danceday", 3]
    x_df.loc[11] = [JEFFY45_STR, "Elonday", 4]
    return x_df
