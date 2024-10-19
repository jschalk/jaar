from src.f00_instrument.file import open_file, create_file_path
from src.f00_instrument.pandas_tool import (
    save_dataframe_to_csv,
    get_orderd_csv,
)
from src.f00_instrument.examples.examples_pandas import (
    get_empty_dataframe,
    get_small_example01_csv,
    get_small_example01_dataframe,
    get_ex01_dataframe,
    get_ex01_unordered_csv,
    get_ex01_ordered_by_fizz_csv,
    get_ex01_ordered_by_count_csv,
    get_ex01_ordered_by_count_buzz_csv,
    get_ex01_ordered_by_count_x_boolean_csv,
)
from src.f00_instrument.examples.instrument_env import (
    env_dir_setup_cleanup,
    get_instrument_temp_env_dir,
)
from os.path import exists as os_path_exists


def test_save_dataframe_to_csv_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    small_dt = get_small_example01_dataframe()
    ex_file_name = "fizzbuzz.csv"
    ex_file_path = create_file_path(env_dir, ex_file_name)
    assert os_path_exists(ex_file_path) is False

    # WHEN
    save_dataframe_to_csv(small_dt, env_dir, ex_file_name)

    # THEN
    assert os_path_exists(ex_file_path)
    small_example01_csv = get_small_example01_csv()
    assert open_file(env_dir, ex_file_name) == small_example01_csv


def test_get_orderd_csv_ReturnsObj():
    # ESTABLISH
    empty_dt = get_empty_dataframe()
    empty_csv = get_orderd_csv(empty_dt).replace("\r", "")
    x1_dt = get_ex01_dataframe()
    unordered_csv = get_ex01_unordered_csv()
    fizz_csv = get_ex01_ordered_by_fizz_csv()
    count_csv = get_ex01_ordered_by_count_csv()
    count_buzz_csv = get_ex01_ordered_by_count_buzz_csv()
    count_bool_csv = get_ex01_ordered_by_count_x_boolean_csv()

    # WHEN / THEN
    print(f"    {empty_csv=}")
    print(f"{unordered_csv=}")
    assert get_orderd_csv(empty_dt) == """\n"""
    assert get_orderd_csv(x1_dt) == unordered_csv
    assert get_orderd_csv(x1_dt, ["fizz"]) == fizz_csv
    assert get_orderd_csv(x1_dt, ["count"]) == count_csv
    assert get_orderd_csv(x1_dt, ["count", "buzz"]) == count_buzz_csv
    assert get_orderd_csv(x1_dt, ["count", "x_boolean"]) == count_bool_csv
