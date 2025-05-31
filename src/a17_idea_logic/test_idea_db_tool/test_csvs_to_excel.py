from os.path import exists as os_path_exists
from pandas import DataFrame
from pandas import read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from src.a17_idea_logic._test_util.a17_env import (
    env_dir_setup_cleanup,
    idea_examples_dir,
)
from src.a17_idea_logic.idea_db_tool import csv_dict_to_excel


def test_csv_dict_to_excel_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    test_data = {"TestSheet": "A,B\n5,6\n7,8"}
    x_file_dir = idea_examples_dir()
    x_filename = "test_output.xlsx"
    file_path = f"{x_file_dir}/{x_filename}"
    assert os_path_exists(file_path) is False

    # WHEN
    csv_dict_to_excel(test_data, x_file_dir, x_filename)

    # THEN
    assert os_path_exists(file_path)
    # Load the created Excel file to verify its contents
    df = pandas_read_excel(file_path, sheet_name="TestSheet")
    expected_df = DataFrame({"A": [5, 7], "B": [6, 8]})

    pandas_testing_assert_frame_equal(df, expected_df)
    print("Test passed successfully.")
