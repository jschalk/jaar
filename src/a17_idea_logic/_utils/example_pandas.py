from pandas import DataFrame


def get_small_example01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["fizz"])
    x_dt.loc[0, "fizz"] = "fizz_buzz0"
    x_dt.loc[1, "fizz"] = "fizz_buzz1"
    x_dt.loc[2, "fizz"] = "fizz_buzz2"
    x_dt.loc[3, "fizz"] = "fizz_buzz3"
    return x_dt


def get_small_example01_csv() -> str:
    return """fizz
fizz_buzz0
fizz_buzz1
fizz_buzz2
fizz_buzz3
"""


def get_empty_dataframe() -> DataFrame:
    return DataFrame()


def get_ex01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["fizz", "buzz", "x_boolean", "count"])
    x_dt.loc[0] = ["fizz2", "buzz1", False, 10]
    x_dt.loc[1] = ["fizz1", "buzz2", True, 10]
    x_dt.loc[2] = ["fizz0", "buzz3", True, 20]
    x_dt.loc[3] = ["fizz3", "buzz0", False, 20]
    return x_dt


def get_ex01_unordered_csv() -> str:
    return """fizz,buzz,x_boolean,count
fizz2,buzz1,False,10
fizz1,buzz2,True,10
fizz0,buzz3,True,20
fizz3,buzz0,False,20
"""


def get_ex01_ordered_by_fizz_csv() -> str:
    return """fizz,buzz,x_boolean,count
fizz0,buzz3,True,20
fizz1,buzz2,True,10
fizz2,buzz1,False,10
fizz3,buzz0,False,20
"""


def get_ex01_ordered_by_count_csv() -> str:
    return """count,fizz,buzz,x_boolean
10,fizz1,buzz2,True
10,fizz2,buzz1,False
20,fizz0,buzz3,True
20,fizz3,buzz0,False
"""


def get_ex01_ordered_by_count_buzz_csv() -> str:
    return """count,buzz,fizz,x_boolean
10,buzz1,fizz2,False
10,buzz2,fizz1,True
20,buzz0,fizz3,False
20,buzz3,fizz0,True
"""


def get_ex01_ordered_by_count_x_boolean_csv() -> str:
    return """count,x_boolean,fizz,buzz
10,False,fizz2,buzz1
10,True,fizz1,buzz2
20,False,fizz3,buzz0
20,True,fizz0,buzz3
"""


def get_ex02_atom_dataframe() -> DataFrame:
    ex02_columns = [
        "healer_name",
        "acct_name",
        "group_label",
        "team_title",
        "awardee_title",
        "road",
    ]
    x_dt = DataFrame(columns=ex02_columns)
    # x_dt.loc[0] = ["fizz2", "buzz1", False, 10]
    # x_dt.loc[1] = ["fizz1", "buzz2", True, 10]
    # x_dt.loc[2] = ["fizz0", "buzz3", True, 20]
    # x_dt.loc[3] = ["fizz3", "buzz0", False, 20]
    # x_dt.loc[4] = ["fizz3", "buzz0", False, 20]
    # x_dt.loc[5] = ["fizz3", "buzz0", False, 20]
    # x_dt.loc[6] = ["fizz3", "buzz0", False, 20]
    # x_dt.loc[7] = ["fizz3", "buzz0", False, 20]
    x_dt.loc[0] = [";yao4", "sue2", ";swim2", ";team5", "aw1", "accord45;casa"]
    x_dt.loc[1] = [";yao3", "sue2", ";swim1", ";team4", "aw1", "accord45;casa;clean"]
    x_dt.loc[2] = [";yao4", "sue2", ";swim1", ";team5", "aw1", "accord45;casa"]
    x_dt.loc[3] = [";yao3", "sue2", ";swim2", ";team4", "aw1", "accord45;casa;clean"]
    x_dt.loc[4] = [";yao4", "sue1", ";swim1", ";team5", "aw1", "accord45;casa"]
    x_dt.loc[5] = [";yao3", "sue1", ";swim1", ";team4", "aw1", "accord45;casa;clean"]
    x_dt.loc[6] = [";yao4", "sue1", ";swim2", ";team5", "aw1", "accord45;casa"]
    x_dt.loc[7] = [";yao3", "sue1", ";swim2", ";team4", "aw1", "accord45;casa;clean"]

    return x_dt


def get_ex02_atom_csv() -> str:
    return """acct_name,group_label,road,team_title,awardee_title,healer_name
sue1,;swim1,accord45;casa,;team5,aw1,;yao4
sue1,;swim1,accord45;casa;clean,;team4,aw1,;yao3
sue1,;swim2,accord45;casa,;team5,aw1,;yao4
sue1,;swim2,accord45;casa;clean,;team4,aw1,;yao3
sue2,;swim1,accord45;casa,;team5,aw1,;yao4
sue2,;swim1,accord45;casa;clean,;team4,aw1,;yao3
sue2,;swim2,accord45;casa,;team5,aw1,;yao4
sue2,;swim2,accord45;casa;clean,;team4,aw1,;yao3
"""
