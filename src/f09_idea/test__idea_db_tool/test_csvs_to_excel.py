from src.f09_idea.idea_db_tool import csv_dict_to_excel
from src.f09_idea.examples.idea_env import idea_examples_dir, idea_env_setup_cleanup
from pandas import read_excel as pandas_read_excel, DataFrame
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_csv_dict_to_excel_SavesFile(idea_env_setup_cleanup):
    # ESTABLISH
    test_data = {"TestSheet": "A,B\n5,6\n7,8"}
    file_path = f"{idea_examples_dir()}/test_output.xlsx"
    assert os_path_exists(file_path) is False

    # WHEN
    excel_file = csv_dict_to_excel(test_data, file_path)

    # THEN
    assert os_path_exists(file_path)
    # Load the created Excel file to verify its contents
    df = pandas_read_excel(file_path, sheet_name="TestSheet")
    expected_df = DataFrame({"A": [5, 7], "B": [6, 8]})

    pandas_testing_assert_frame_equal(df, expected_df)
    print("Test passed successfully.")
