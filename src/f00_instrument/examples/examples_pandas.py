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
