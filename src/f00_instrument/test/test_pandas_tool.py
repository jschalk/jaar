from src.f00_instrument.file import open_file, create_file_path
from src.f00_instrument.pandas_tool import save_dataframe_to_csv
from src.f00_instrument.examples.examples_pandas import (
    get_small_example01_csv,
    get_small_example01_dataframe,
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
    ex_filename = "fizzbuzz"
    ex_file_name = "fizzbuzz.csv"
    ex_file_path = create_file_path(env_dir, ex_file_name)
    assert os_path_exists(ex_file_path) is False

    # WHEN
    save_dataframe_to_csv(small_dt, env_dir, ex_file_name)

    # THEN
    assert os_path_exists(ex_file_path)
    small_example01_csv = get_small_example01_csv()
    assert open_file(env_dir, ex_file_name) == small_example01_csv
