from pandas import DataFrame
from src.ref.ch17_keywords import Ch17Keywords as wx

AMY23_STR = "amy23"
JEFFY45_STR = "jeffy45"


def get_ex1_br00000_df() -> DataFrame:
    """idea_format_00000_momentunit_v0_0_0
    c400_number,moment_label,fund_grain,monthday_index,money_grain,respect_grain,knot,epoch_label,yr1_jan1_offset
    """
    x_df = DataFrame(
        columns=[
            wx.c400_number,
            wx.moment_label,
            wx.fund_grain,
            wx.monthday_index,
            wx.money_grain,
            wx.respect_grain,
            wx.knot,
            wx.epoch_label,
            wx.yr1_jan1_offset,
            wx.job_listen_rotations,
        ]
    )
    x_df.loc[0] = [7, AMY23_STR, 1, 1, 1, 1, "/", "creg", 440640, 7]
    return x_df


def get_ex1_br00001_df() -> DataFrame:
    """idea_format_00001_moment_budunit_v0_0_0
    moment_label,belief_name,quota,bud_time,celldepth"""
    x_df = DataFrame(
        columns=[
            wx.moment_label,
            wx.belief_name,
            wx.quota,
            wx.bud_time,
            wx.celldepth,
        ]
    )
    x_df.loc[0] = [AMY23_STR, "Sue", 445, 777, 5]
    return x_df


def get_ex1_br00002_df() -> DataFrame:
    """idea_format_00002_moment_paybook_v0_0_0
    voice_name,amount,moment_label,belief_name,tran_time"""
    x_df = DataFrame(
        columns=["voice_name", "amount", "moment_label", "belief_name", "tran_time"]
    )
    x_df.loc[0] = ["Bob", 888, AMY23_STR, "Zia", 777]
    return x_df


def get_ex1_br00003_df() -> DataFrame:
    """idea_format_00003_moment_epoch_hour_v0_0_0
    cumulative_minute,moment_label,hour_label"""
    x_df = DataFrame(columns=["moment_label", "hour_label", "cumulative_minute"])
    x_df.loc[0] = [AMY23_STR, "12am", 60]
    x_df.loc[1] = [AMY23_STR, "1am", 120]
    x_df.loc[2] = [AMY23_STR, "2am", 180]
    x_df.loc[3] = [AMY23_STR, "3am", 240]
    x_df.loc[4] = [AMY23_STR, "4am", 300]
    x_df.loc[5] = [AMY23_STR, "5am", 360]
    x_df.loc[6] = [AMY23_STR, "6am", 420]
    x_df.loc[7] = [AMY23_STR, "7am", 480]
    x_df.loc[8] = [AMY23_STR, "8am", 540]
    x_df.loc[9] = [AMY23_STR, "9am", 600]
    x_df.loc[10] = [AMY23_STR, "10am", 660]
    x_df.loc[11] = [AMY23_STR, "11am", 720]
    x_df.loc[12] = [AMY23_STR, "12pm", 780]
    x_df.loc[13] = [AMY23_STR, "1pm", 840]
    x_df.loc[14] = [AMY23_STR, "2pm", 900]
    x_df.loc[15] = [AMY23_STR, "3pm", 960]
    x_df.loc[16] = [AMY23_STR, "4pm", 1020]
    x_df.loc[17] = [AMY23_STR, "5pm", 1080]
    x_df.loc[18] = [AMY23_STR, "6pm", 1140]
    x_df.loc[19] = [AMY23_STR, "7pm", 1200]
    x_df.loc[20] = [AMY23_STR, "8pm", 1260]
    x_df.loc[21] = [AMY23_STR, "9pm", 1320]
    x_df.loc[22] = [AMY23_STR, "10pm", 1380]
    x_df.loc[23] = [AMY23_STR, "11pm", 1440]
    return x_df


def get_ex1_br00004_df() -> DataFrame:
    """idea_format_00004_moment_epoch_month_v0_0_0
    cumulative_day,moment_label,month_label"""
    x_df = DataFrame(columns=["moment_label", "month_label", "cumulative_day"])
    x_df.loc[0] = [AMY23_STR, "March", 31]
    x_df.loc[1] = [AMY23_STR, "April", 61]
    x_df.loc[2] = [AMY23_STR, "May", 92]
    x_df.loc[3] = [AMY23_STR, "June", 122]
    x_df.loc[4] = [AMY23_STR, "July", 153]
    x_df.loc[5] = [AMY23_STR, "August", 184]
    x_df.loc[6] = [AMY23_STR, "September", 214]
    x_df.loc[7] = [AMY23_STR, "October", 245]
    x_df.loc[8] = [AMY23_STR, "November", 275]
    x_df.loc[9] = [AMY23_STR, "December", 306]
    x_df.loc[10] = [AMY23_STR, "January", 337]
    x_df.loc[11] = [AMY23_STR, "February", 365]
    return x_df


def get_ex1_br00005_df() -> DataFrame:
    """idea_format_00005_moment_epoch_weekday_v0_0_0
    moment_label,weekday_label,weekday_order"""
    x_df = DataFrame(columns=[wx.moment_label, wx.weekday_label, wx.weekday_order])
    x_df.loc[0] = [AMY23_STR, "Wednesday", 0]
    x_df.loc[1] = [AMY23_STR, "Thursday", 1]
    x_df.loc[2] = [AMY23_STR, "Friday", 2]
    x_df.loc[3] = [AMY23_STR, "Saturday", 3]
    x_df.loc[4] = [AMY23_STR, "Sunday", 4]
    x_df.loc[5] = [AMY23_STR, "Monday", 5]
    x_df.loc[6] = [AMY23_STR, "Tuesday", 6]
    return x_df


def get_ex2_br00000_df() -> DataFrame:
    """idea_format_00000_momentunit_v0_0_0
    c400_number,moment_label,fund_grain,monthday_index,money_grain,respect_grain,knot,epoch_label,yr1_jan1_offset,job_listen_rotations
    """
    x_df = DataFrame(
        columns=[
            wx.c400_number,
            wx.moment_label,
            wx.fund_grain,
            wx.monthday_index,
            wx.money_grain,
            wx.respect_grain,
            wx.knot,
            wx.epoch_label,
            wx.yr1_jan1_offset,
            wx.job_listen_rotations,
        ]
    )
    x_df.loc[0] = [7, AMY23_STR, 1, 1, 1, 1, "/", "creg", 440640, 4]
    x_df.loc[1] = [25, JEFFY45_STR, 1, 0, 1, 1, ",", "five", 1683478080, 4]
    return x_df


def get_ex2_br00001_df() -> DataFrame:
    """idea_format_00001_moment_budunit_v0_0_0
    moment_label,belief_name,quota,bud_time"""
    x_df = DataFrame(
        columns=[
            wx.moment_label,
            wx.belief_name,
            wx.quota,
            wx.bud_time,
            wx.celldepth,
        ]
    )
    x_df.loc[0] = [AMY23_STR, "Bob", 332, 999, 3]
    x_df.loc[1] = [AMY23_STR, "Sue", 445, 777, 3]
    x_df.loc[2] = [AMY23_STR, "Yao", 700, 222, 3]
    x_df.loc[3] = [JEFFY45_STR, "Xio", 332, 999, 3]
    x_df.loc[4] = [JEFFY45_STR, "Zia", 700, 222, 3]
    return x_df


def get_ex2_br00002_df() -> DataFrame:
    """idea_format_00002_moment_paybook_v0_0_0
    voice_name,amount,moment_label,belief_name,tran_time"""
    x_df = DataFrame(
        columns=[
            wx.voice_name,
            wx.amount,
            wx.moment_label,
            wx.belief_name,
            wx.tran_time,
        ]
    )
    x_df.loc[0] = ["Zia", 888, AMY23_STR, "Bob", 777]
    x_df.loc[1] = ["Zia", 234, AMY23_STR, "Sue", 999]
    x_df.loc[2] = ["Zia", 234, AMY23_STR, "Yao", 999]
    x_df.loc[3] = ["Zia", 234, JEFFY45_STR, "Yao", 999]
    x_df.loc[4] = ["Bob", 888, AMY23_STR, "Zia", 777]
    return x_df


def get_ex2_br00003_df() -> DataFrame:
    """idea_format_00003_moment_epoch_hour_v0_0_0
    cumulative_minute,moment_label,hour_label"""
    x_df = DataFrame(columns=["moment_label", "hour_label", "cumulative_minute"])
    x_df.loc[0] = [AMY23_STR, "12am", 60]
    x_df.loc[1] = [AMY23_STR, "1am", 120]
    x_df.loc[2] = [AMY23_STR, "2am", 180]
    x_df.loc[3] = [AMY23_STR, "3am", 240]
    x_df.loc[4] = [AMY23_STR, "4am", 300]
    x_df.loc[5] = [AMY23_STR, "5am", 360]
    x_df.loc[6] = [AMY23_STR, "6am", 420]
    x_df.loc[7] = [AMY23_STR, "7am", 480]
    x_df.loc[8] = [AMY23_STR, "8am", 540]
    x_df.loc[9] = [AMY23_STR, "9am", 600]
    x_df.loc[10] = [AMY23_STR, "10am", 660]
    x_df.loc[11] = [AMY23_STR, "11am", 720]
    x_df.loc[12] = [AMY23_STR, "12pm", 780]
    x_df.loc[13] = [AMY23_STR, "1pm", 840]
    x_df.loc[14] = [AMY23_STR, "2pm", 900]
    x_df.loc[15] = [AMY23_STR, "3pm", 960]
    x_df.loc[16] = [AMY23_STR, "4pm", 1020]
    x_df.loc[17] = [AMY23_STR, "5pm", 1080]
    x_df.loc[18] = [AMY23_STR, "6pm", 1140]
    x_df.loc[19] = [AMY23_STR, "7pm", 1200]
    x_df.loc[20] = [AMY23_STR, "8pm", 1260]
    x_df.loc[21] = [AMY23_STR, "9pm", 1320]
    x_df.loc[22] = [AMY23_STR, "10pm", 1380]
    x_df.loc[23] = [AMY23_STR, "11pm", 1440]
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
    """idea_format_00004_moment_epoch_month_v0_0_0
    cumulative_day,moment_label,month_label"""
    x_df = DataFrame(columns=["moment_label", "month_label", "cumulative_day"])
    x_df.loc[0] = [AMY23_STR, "March", 31]
    x_df.loc[1] = [AMY23_STR, "April", 61]
    x_df.loc[2] = [AMY23_STR, "May", 92]
    x_df.loc[3] = [AMY23_STR, "June", 122]
    x_df.loc[4] = [AMY23_STR, "July", 153]
    x_df.loc[5] = [AMY23_STR, "August", 184]
    x_df.loc[6] = [AMY23_STR, "September", 214]
    x_df.loc[7] = [AMY23_STR, "October", 245]
    x_df.loc[8] = [AMY23_STR, "November", 275]
    x_df.loc[9] = [AMY23_STR, "December", 306]
    x_df.loc[10] = [AMY23_STR, "January", 337]
    x_df.loc[11] = [AMY23_STR, "February", 365]
    x_df.loc[12] = (JEFFY45_STR, "Fredrick", 25)
    x_df.loc[13] = (JEFFY45_STR, "Geo", 50)
    x_df.loc[14] = (JEFFY45_STR, "Holocene", 75)
    x_df.loc[15] = (JEFFY45_STR, "Iguana", 100)
    x_df.loc[16] = (JEFFY45_STR, "Jesus", 125)
    x_df.loc[17] = (JEFFY45_STR, "Keel", 150)
    x_df.loc[18] = (JEFFY45_STR, "LeBron", 175)
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
    """idea_format_00005_moment_epoch_weekday_v0_0_0
    moment_label,weekday_label,weekday_order"""
    x_df = DataFrame(columns=["moment_label", "weekday_label", "weekday_order"])
    x_df.loc[0] = [AMY23_STR, "Wednesday", 0]
    x_df.loc[1] = [AMY23_STR, "Thursday", 1]
    x_df.loc[2] = [AMY23_STR, "Friday", 2]
    x_df.loc[3] = [AMY23_STR, "Saturday", 3]
    x_df.loc[4] = [AMY23_STR, "Sunday", 4]
    x_df.loc[5] = [AMY23_STR, "Monday", 5]
    x_df.loc[6] = [AMY23_STR, "Tuesday", 6]
    x_df.loc[7] = [JEFFY45_STR, "Anaday", 0]
    x_df.loc[8] = [JEFFY45_STR, "Baileyday", 1]
    x_df.loc[9] = [JEFFY45_STR, "Chiday", 2]
    x_df.loc[10] = [JEFFY45_STR, "Danceday", 3]
    x_df.loc[11] = [JEFFY45_STR, "Eastday", 4]
    return x_df


# def get_ex2_br00006_df() -> DataFrame:
#     """idea_format_00006_moment_timeoffi_v0_0_0
#     moment_label,offi_time,_offi_time_maxt"""
#     x_df = DataFrame(columns=["moment_label", "offi_time", "offi_time_max"])
#     x_df.loc[0] = [AMY23_STR, 100, 300]
#     x_df.loc[1] = [AMY23_STR, 110, 320]
#     x_df.loc[2] = [AMY23_STR, 120, 330]
#     x_df.loc[3] = [AMY23_STR, 130, 340]
#     x_df.loc[4] = [AMY23_STR, 140, 350]
#     return x_df


def get_small_example01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["Fay"])
    x_dt.loc[0, "Fay"] = "Fay_bob0"
    x_dt.loc[1, "Fay"] = "Fay_bob1"
    x_dt.loc[2, "Fay"] = "Fay_bob2"
    x_dt.loc[3, "Fay"] = "Fay_bob3"
    return x_dt


def get_small_example01_csv() -> str:
    return """Fay
fay_bob0
fay_bob1
fay_bob2
fay_bob3
"""


def get_empty_dataframe() -> DataFrame:
    return DataFrame()


def get_ex01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["fay", "bob", "x_boolean", "count"])
    x_dt.loc[0] = ["fay2", "bob1", False, 10]
    x_dt.loc[1] = ["fay1", "bob2", True, 10]
    x_dt.loc[2] = ["fay0", "bob3", True, 20]
    x_dt.loc[3] = ["fay3", "bob0", False, 20]
    return x_dt


def get_ex01_unordered_csv() -> str:
    return """fay,bob,x_boolean,count
fay2,bob1,False,10
fay1,bob2,True,10
fay0,bob3,True,20
fay3,bob0,False,20
"""


def get_ex01_ordered_by_fay_csv() -> str:
    return """fay,bob,x_boolean,count
fay0,bob3,True,20
fay1,bob2,True,10
fay2,bob1,False,10
fay3,bob0,False,20
"""


def get_ex01_ordered_by_count_csv() -> str:
    return """count,fay,bob,x_boolean
10,fay1,bob2,True
10,fay2,bob1,False
20,fay0,bob3,True
20,fay3,bob0,False
"""


def get_ex01_ordered_by_count_bob_csv() -> str:
    return """count,bob,fay,x_boolean
10,bob1,fay2,False
10,bob2,fay1,True
20,bob0,fay3,False
20,bob3,fay0,True
"""


def get_ex01_ordered_by_count_x_boolean_csv() -> str:
    return """count,x_boolean,fay,bob
10,False,fay2,bob1
10,True,fay1,bob2
20,False,fay3,bob0
20,True,fay0,bob3
"""


def get_ex02_atom_dataframe() -> DataFrame:
    ex02_columns = [
        "healer_name",
        "voice_name",
        "group_title",
        "party_title",
        "awardee_title",
        "plan_rope",
    ]
    x_dt = DataFrame(columns=ex02_columns)
    # x_dt.loc[0] = ["Fay2", "Bob1", False, 10]
    # x_dt.loc[1] = ["Fay1", "Bob2", True, 10]
    # x_dt.loc[2] = ["Fay0", "Bob3", True, 20]
    # x_dt.loc[3] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[4] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[5] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[6] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[7] = ["Fay3", "Bob0", False, 20]
    x_dt.loc[0] = [";yao4", "sue2", ";swim2", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[1] = [";yao3", "sue2", ";swim1", ";labor4", "aw1", "amy45;casa;clean"]
    x_dt.loc[2] = [";yao4", "sue2", ";swim1", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[3] = [";yao3", "sue2", ";swim2", ";labor4", "aw1", "amy45;casa;clean"]
    x_dt.loc[4] = [";yao4", "sue1", ";swim1", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[5] = [";yao3", "sue1", ";swim1", ";labor4", "aw1", "amy45;casa;clean"]
    x_dt.loc[6] = [";yao4", "sue1", ";swim2", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[7] = [";yao3", "sue1", ";swim2", ";labor4", "aw1", "amy45;casa;clean"]

    return x_dt


def get_ex02_atom_csv() -> str:
    return """voice_name,group_title,plan_rope,party_title,awardee_title,healer_name
sue1,;swim1,amy45;casa,;labor5,aw1,;yao4
sue1,;swim1,amy45;casa;clean,;labor4,aw1,;yao3
sue1,;swim2,amy45;casa,;labor5,aw1,;yao4
sue1,;swim2,amy45;casa;clean,;labor4,aw1,;yao3
sue2,;swim1,amy45;casa,;labor5,aw1,;yao4
sue2,;swim1,amy45;casa;clean,;labor4,aw1,;yao3
sue2,;swim2,amy45;casa,;labor5,aw1,;yao4
sue2,;swim2,amy45;casa;clean,;labor4,aw1,;yao3
"""
