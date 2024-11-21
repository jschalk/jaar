from src.f00_instrument.file import open_file, create_path
from src.f00_instrument.examples.instrument_env import (
    env_dir_setup_cleanup,
    get_instrument_temp_env_dir,
)
from src.f04_gift.atom_config import acct_id_str, group_id_str, credor_respect_str
from src.f09_brick.examples.examples_pandas import (
    get_empty_dataframe,
    get_small_example01_csv,
    get_small_example01_dataframe,
    get_ex01_dataframe,
    get_ex01_unordered_csv,
    get_ex01_ordered_by_fizz_csv,
    get_ex01_ordered_by_count_csv,
    get_ex01_ordered_by_count_buzz_csv,
    get_ex01_ordered_by_count_x_boolean_csv,
    get_ex02_atom_dataframe,
    get_ex02_atom_csv,
)
from src.f09_brick.pandas_tool import (
    save_dataframe_to_csv,
    get_ordered_csv,
    get_all_excel_sheet_names,
    get_relevant_columns_dataframe,
    get_zoo_staging_grouping_with_all_values_equal_df,
    upsert_sheet,
)
from os.path import exists as os_path_exists
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from pytest import fixture as pytest_fixture


def test_get_ordered_csv_ReturnsObj():
    # ESTABLISH
    empty_dt = get_empty_dataframe()
    empty_csv = get_ordered_csv(empty_dt).replace("\r", "")
    x1_dt = get_ex01_dataframe()
    unordered_csv = get_ex01_unordered_csv()
    fizz_csv = get_ex01_ordered_by_fizz_csv()
    count_csv = get_ex01_ordered_by_count_csv()
    count_buzz_csv = get_ex01_ordered_by_count_buzz_csv()
    count_bool_csv = get_ex01_ordered_by_count_x_boolean_csv()

    # WHEN / THEN
    print(f"    {empty_csv=}")
    print(f"{unordered_csv=}")
    assert get_ordered_csv(empty_dt) == """\n"""
    assert get_ordered_csv(x1_dt) == unordered_csv
    assert get_ordered_csv(x1_dt, ["fizz"]) == fizz_csv
    assert get_ordered_csv(x1_dt, ["count"]) == count_csv
    assert get_ordered_csv(x1_dt, ["count", "buzz"]) == count_buzz_csv
    assert get_ordered_csv(x1_dt, ["count", "x_boolean"]) == count_bool_csv
    # have sorting work even if sorting column does not exist
    assert get_ordered_csv(x1_dt, ["count", "vic", "buzz"]) == count_buzz_csv


def test_save_dataframe_to_csv_SavesFile_Scenario0_SmallDataFrame(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    small_dt = get_small_example01_dataframe()
    ex_file_name = "fizzbuzz.csv"
    ex_file_path = create_path(env_dir, ex_file_name)
    assert os_path_exists(ex_file_path) is False

    # WHEN
    save_dataframe_to_csv(small_dt, env_dir, ex_file_name)

    # THEN
    assert os_path_exists(ex_file_path)
    small_example01_csv = get_small_example01_csv()
    assert open_file(env_dir, ex_file_name) == small_example01_csv


def test_save_dataframe_to_csv_SavesFile_Scenario1_OrdersColumns(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    atom_example_dt = get_ex02_atom_dataframe()
    ex_file_name = "atom_example.csv"

    # WHEN
    save_dataframe_to_csv(atom_example_dt, env_dir, ex_file_name)

    # THEN
    function_ex02_atom_csv = get_ex02_atom_csv()
    file_ex02_atom_csv = open_file(env_dir, ex_file_name)
    print(f"{function_ex02_atom_csv=}")
    print(f"    {file_ex02_atom_csv=}")
    assert file_ex02_atom_csv == function_ex02_atom_csv


@pytest_fixture
def sample_dataframe():
    """Fixture to provide a sample DataFrame."""
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
    return DataFrame(data)


@pytest_fixture
def temp_excel_file(tmp_path):
    """Fixture to provide a temporary Excel file path."""
    return tmp_path / "test_excel.xlsx"


def test_create_new_file(temp_excel_file, sample_dataframe):
    """Test creating a new Excel file with a specified sheet."""
    upsert_sheet(temp_excel_file, "Sheet1", sample_dataframe)
    assert os_path_exists(temp_excel_file)

    # Verify the content of the sheet
    df_read = pandas_read_excel(temp_excel_file, sheet_name="Sheet1")
    pandas_testing_assert_frame_equal(df_read, sample_dataframe)


def test_replace_existing_sheet(temp_excel_file, sample_dataframe):
    """Test replacing an existing sheet in the Excel file."""
    # Create the file and write initial data
    initial_data = DataFrame({"A": [1, 2, 3]})
    upsert_sheet(temp_excel_file, "Sheet1", initial_data)

    # Replace the sheet with new data
    upsert_sheet(temp_excel_file, "Sheet1", sample_dataframe)

    # Verify the content of the replaced sheet
    df_read = pandas_read_excel(temp_excel_file, sheet_name="Sheet1")
    pandas_testing_assert_frame_equal(df_read, sample_dataframe)


def test_add_new_sheet_to_existing_file(temp_excel_file, sample_dataframe):
    """Test adding a new sheet to an existing Excel file."""
    # Create the file and write initial data to one sheet
    initial_data = DataFrame({"A": [1, 2, 3]})
    upsert_sheet(temp_excel_file, "InitialSheet", initial_data)

    # Add a new sheet with different data
    upsert_sheet(temp_excel_file, "NewSheet", sample_dataframe)

    # Verify both sheets exist and have correct data
    df_initial = pandas_read_excel(temp_excel_file, sheet_name="InitialSheet")
    df_new = pandas_read_excel(temp_excel_file, sheet_name="NewSheet")
    pandas_testing_assert_frame_equal(df_initial, initial_data)
    pandas_testing_assert_frame_equal(df_new, sample_dataframe)


def test_get_all_excel_sheet_names_ReturnsObj_Scenario0_NoPidgin(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x_dir = create_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    sheet_name1 = "Sheet1x"
    sheet_name2 = "Sheet2x"
    upsert_sheet(ex_file_path, sheet_name1, df1)
    upsert_sheet(ex_file_path, sheet_name2, df2)

    # WHEN
    x_sheet_names = get_all_excel_sheet_names(env_dir)

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_file_name, sheet_name1) in x_sheet_names
    assert (x_dir, ex_file_name, sheet_name2) in x_sheet_names
    assert len(x_sheet_names) == 2


def test_get_all_excel_sheet_names_ReturnsObj_Scenario1_PidginSheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x_dir = create_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    sugar_str = "sugar"
    honey_name1 = "honey1x"
    sugar_name1 = f"{sugar_str}2x"
    sugar_name2 = f"honey_{sugar_str}3x"
    upsert_sheet(ex_file_path, honey_name1, df1)
    upsert_sheet(ex_file_path, sugar_name1, df2)
    upsert_sheet(ex_file_path, sugar_name2, df2)

    # WHEN
    x_sheet_names = get_all_excel_sheet_names(env_dir, sub_strs={sugar_str})

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_file_name, honey_name1) not in x_sheet_names
    assert (x_dir, ex_file_name, sugar_name1) in x_sheet_names
    assert (x_dir, ex_file_name, sugar_name2) in x_sheet_names
    assert len(x_sheet_names) == 2


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario0():
    # ESTABLISH
    spam_str = "spam"
    df1 = DataFrame([["AAA", "BBB"]], columns=[spam_str, "egg"])

    # WHEN
    relevant_dataframe = get_relevant_columns_dataframe(df1)

    # THEN
    assert relevant_dataframe is not None
    assert not list(relevant_dataframe.columns)


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario1():
    # ESTABLISH
    spam_str = "spam"
    df1 = DataFrame([["AAA", "BBB"]], columns=[spam_str, "egg"])

    # WHEN
    relevant_dataframe = get_relevant_columns_dataframe(df1, [spam_str])

    # THEN
    assert relevant_dataframe is not None
    print(f"{type(relevant_dataframe.columns)=}")
    print(f"{relevant_dataframe.columns.to_list()=}")
    assert relevant_dataframe.columns.to_list() == [spam_str]


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario2_UnimportantOnesAreignored():
    # ESTABLISH
    spam_str = "spam"
    df1 = DataFrame([["AAA", "BBB"]], columns=[spam_str, "egg"])

    # WHEN
    relevant_columns = [spam_str, "something_else"]
    relevant_dataframe = get_relevant_columns_dataframe(df1, relevant_columns)

    # THEN
    assert relevant_dataframe is not None
    assert relevant_dataframe.columns.to_list() == [spam_str]


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario3_ColumnOrderCorrect():
    # ESTABLISH
    spam_str = "spam"
    egg_str = "egg"
    ham_str = "ham"
    df1 = DataFrame([["AAA", "BBB", "CCC"]], columns=[ham_str, spam_str, egg_str])

    # WHEN
    relevant_columns = [egg_str, spam_str, ham_str]
    relevant_dataframe = get_relevant_columns_dataframe(df1, relevant_columns)

    # THEN
    assert relevant_dataframe is not None
    print(f"{relevant_dataframe.columns=}")
    assert relevant_dataframe.columns.to_list() == relevant_columns
    assert relevant_dataframe.columns.to_list()[0] == egg_str


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario4_ColumnOrderCorrect():
    # ESTABLISH
    df1 = DataFrame([["AAA", "BBB"]], columns=[group_id_str(), acct_id_str()])

    # WHEN
    relevant_dataframe = get_relevant_columns_dataframe(df1)

    # THEN
    assert relevant_dataframe is not None
    print(f"{relevant_dataframe.columns=}")
    assert relevant_dataframe.columns.to_list()[0] == acct_id_str()
    assert relevant_dataframe.columns.to_list() == [acct_id_str(), group_id_str()]


def test_get_zoo_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario0_EmptyDataframe():
    # ESTABLISH
    df1 = DataFrame([[]], columns=[])
    group_by_list = [group_id_str(), acct_id_str()]

    # WHEN
    group_by_dataframe = get_zoo_staging_grouping_with_all_values_equal_df(
        df1, group_by_list
    )

    # THEN
    assert group_by_dataframe is not None
    assert len(group_by_dataframe) == len(DataFrame([[]], columns=[]))
    print(f"{group_by_dataframe.columns=}")
    assert group_by_dataframe.columns.to_list() == []


def test_get_zoo_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario1_GroupBySingleColumn():
    # ESTABLISH
    df_columns = [group_id_str(), credor_respect_str()]
    before_df_values = [["AA0", "BB0"], ["AA0", "BB0"]]
    df1 = DataFrame(before_df_values, columns=df_columns)
    group_by_list = [group_id_str()]

    # WHEN
    group_by_dataframe = get_zoo_staging_grouping_with_all_values_equal_df(
        df1, group_by_list
    )
    print(f"{group_by_dataframe=}")

    # THEN
    assert group_by_dataframe is not None
    after_df_values = [["AA0", "BB0"]]
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert len(group_by_dataframe) == len(after_df)
    print(f"{group_by_dataframe.columns=}")
    assert group_by_dataframe.columns.to_list() == after_df.columns.to_list()
    assert group_by_dataframe.to_csv() == after_df.to_csv()


def test_get_zoo_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario2_GroupByExtraColumns():
    # ESTABLISH
    df_columns = [group_id_str(), credor_respect_str()]
    before_df_values = [["AA0", "BB0"], ["AA0", "BB0"]]
    df1 = DataFrame(before_df_values, columns=df_columns)
    group_by_list = [group_id_str(), acct_id_str()]

    # WHEN
    group_by_dataframe = get_zoo_staging_grouping_with_all_values_equal_df(
        df1, group_by_list
    )
    print(f"{group_by_dataframe=}")

    # THEN
    assert group_by_dataframe is not None
    after_df_values = [["AA0", "BB0"]]
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert len(group_by_dataframe) == len(after_df)
    print(f"{group_by_dataframe.columns=}")
    assert group_by_dataframe.columns.to_list() == after_df.columns.to_list()
    assert group_by_dataframe.to_csv() == after_df.to_csv()


def test_get_zoo_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario3_GroupByExtraColumns():
    # ESTABLISH
    df_columns = [group_id_str(), credor_respect_str(), "column3"]
    before_df_values = [["AA0", "BB0", "CC0"], ["AA0", "BB0", "CC0"]]
    df1 = DataFrame(before_df_values, columns=df_columns)
    group_by_list = [group_id_str(), acct_id_str(), credor_respect_str()]

    # WHEN
    group_by_dataframe = get_zoo_staging_grouping_with_all_values_equal_df(
        df1, group_by_list
    )
    print(f"{group_by_dataframe=}")

    # THEN
    assert group_by_dataframe is not None
    after_df_values = [["AA0", "BB0", "CC0"]]
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert len(group_by_dataframe) == len(after_df)
    print(f"{group_by_dataframe.columns=}")
    assert group_by_dataframe.columns.to_list() == after_df.columns.to_list()
    assert group_by_dataframe.to_csv() == after_df.to_csv()


def test_get_zoo_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario4_GroupByExtraColumns():
    # ESTABLISH
    df_columns = [group_id_str(), credor_respect_str(), "column3"]
    before_df_values = [
        ["AA0", "BB0", "CC0"],
        ["AA0", "BB0", "CC1"],
        ["DD0", "EE0", "FF0"],
    ]
    df1 = DataFrame(before_df_values, columns=df_columns)
    group_by_list = [group_id_str(), acct_id_str(), credor_respect_str()]

    # WHEN
    group_by_dataframe = get_zoo_staging_grouping_with_all_values_equal_df(
        df1, group_by_list
    )
    print(f"{group_by_dataframe=}")

    # THEN
    after_df_values = [["DD0", "EE0", "FF0"]]
    assert group_by_dataframe is not None
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert group_by_dataframe.columns.to_list() == after_df.columns.to_list()
    assert len(group_by_dataframe) == len(after_df)
    print(f"{group_by_dataframe.columns=}")
    assert group_by_dataframe.to_csv() == after_df.to_csv()
