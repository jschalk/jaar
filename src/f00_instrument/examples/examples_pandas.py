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
    return """fizz,buzz,x_boolean,count
fizz1,buzz2,True,10
fizz2,buzz1,False,10
fizz0,buzz3,True,20
fizz3,buzz0,False,20
"""


def get_ex01_ordered_by_count_buzz_csv() -> str:
    return """fizz,buzz,x_boolean,count
fizz2,buzz1,False,10
fizz1,buzz2,True,10
fizz3,buzz0,False,20
fizz0,buzz3,True,20
"""


def get_ex01_ordered_by_count_x_boolean_csv() -> str:
    return """fizz,buzz,x_boolean,count
fizz2,buzz1,False,10
fizz1,buzz2,True,10
fizz3,buzz0,False,20
fizz0,buzz3,True,20
"""
