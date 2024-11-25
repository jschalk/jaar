from src.f00_instrument.file import create_path
from src.f09_brick.examples.brick_env import brick_env_setup_cleanup, brick_fiscals_dir
from src.f09_brick.pandas_tool import (
    does_sheet_exist,
    upsert_sheet,
    get_all_excel_sheet_names,
    split_excel_into_dirs,
)
from pytest import fixture as pytest_fixture, raises as pytest_raises
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


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


def test_upsert_sheet_CreatesNewFile(temp_excel_file, sample_dataframe):
    """Test creating a new Excel file with a specified sheet."""
    upsert_sheet(temp_excel_file, "Sheet1", sample_dataframe)
    assert os_path_exists(temp_excel_file)

    # Verify the content of the sheet
    df_read = pandas_read_excel(temp_excel_file, sheet_name="Sheet1")
    assert list(df_read.columns) != []
    pandas_testing_assert_frame_equal(df_read, sample_dataframe)


def test_upsert_sheet_ReplacesExistingSheet(temp_excel_file, sample_dataframe):
    """Test replacing an existing sheet in the Excel file."""
    # ESTABLISH Create the file and write initial data
    initial_data = DataFrame({"A": [1, 2, 3]})
    upsert_sheet(temp_excel_file, "Sheet1", initial_data)

    # WHEN Replace the sheet with new data
    upsert_sheet(temp_excel_file, "Sheet1", sample_dataframe)

    # THEN Verify the content of the replaced sheet
    df_read = pandas_read_excel(temp_excel_file, sheet_name="Sheet1")
    pandas_testing_assert_frame_equal(df_read, sample_dataframe)


def test_upsert_sheet_AddNewSheetToExistingFile(temp_excel_file, sample_dataframe):
    """Test adding a new sheet to an existing Excel file."""
    # ESTABLISH Create the file and write initial data to one sheet
    initial_data = DataFrame({"A": [1, 2, 3]})
    upsert_sheet(temp_excel_file, "InitialSheet", initial_data)

    # WHEN Add a new sheet with different data
    upsert_sheet(temp_excel_file, "NewSheet", sample_dataframe)

    # THEN Verify both sheets exist and have correct data
    df_initial = pandas_read_excel(temp_excel_file, sheet_name="InitialSheet")
    df_new = pandas_read_excel(temp_excel_file, sheet_name="NewSheet")
    pandas_testing_assert_frame_equal(df_initial, initial_data)
    pandas_testing_assert_frame_equal(df_new, sample_dataframe)


def test_get_all_excel_sheet_names_ReturnsObj_Scenario0_NoPidgin(
    brick_env_setup_cleanup,
):
    # ESTABLISH
    env_dir = brick_fiscals_dir()
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
    brick_env_setup_cleanup,
):
    # ESTABLISH
    env_dir = brick_fiscals_dir()
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


@pytest_fixture
def sample_excel_file(tmp_path):
    """Fixture to create a sample Excel file for testing."""
    data = {
        "ID": [1, 2, 3, 4, 5],
        "Category": ["A", "B", "A", "C", "B"],
        "Value": [100, 200, 150, 300, 250],
    }
    df = DataFrame(data)
    file_path = tmp_path / "sample.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


@pytest_fixture
def output_dir(tmp_path):
    """Fixture to provide a temporary output directory."""
    output_dir = tmp_path / "output"
    return output_dir


def test_split_excel_into_dirs_RaisesErrorWhenColumnIsInvalid(
    sample_excel_file, output_dir
):
    """Test handling of an invalid column."""
    # ESTABLISH / WHEN / THEN
    with pytest_raises(ValueError, match="Column 'InvalidColumn' does not exist"):
        split_excel_into_dirs(
            sample_excel_file, output_dir, "InvalidColumn", "filename", "sheet5"
        )


def test_split_excel_into_dirs_CreatesFilesWhenColumnIsValid(
    sample_excel_file, output_dir
):
    """Test splitting an Excel file by a valid column."""
    # ESTABLISH
    x_filename = "fizz"
    a_file_path = create_path(output_dir, f"A/{x_filename}.xlsx")
    b_file_path = create_path(output_dir, f"B/{x_filename}.xlsx")
    c_file_path = create_path(output_dir, f"C/{x_filename}.xlsx")
    assert os_path_exists(a_file_path) is False
    assert os_path_exists(b_file_path) is False
    assert os_path_exists(c_file_path) is False

    # WHEN
    split_excel_into_dirs(
        sample_excel_file, output_dir, "Category", x_filename, "sheet5"
    )

    # Verify files are created for each unique value in "Category"
    assert os_path_exists(a_file_path)
    assert os_path_exists(b_file_path)
    assert os_path_exists(c_file_path)

    # Verify contents of one of the created files
    a_df = pandas_read_excel(a_file_path)
    expected_a = DataFrame({"ID": [1, 3], "Category": ["A", "A"], "Value": [100, 150]})
    pandas_testing_assert_frame_equal(a_df, expected_a)

    b_df = pandas_read_excel(b_file_path)
    b_expected = DataFrame({"ID": [2, 5], "Category": ["B", "B"], "Value": [200, 250]})
    pandas_testing_assert_frame_equal(b_df, b_expected)

    c_df = pandas_read_excel(c_file_path)
    c_expected = DataFrame({"ID": [4], "Category": ["C"], "Value": [300]})
    pandas_testing_assert_frame_equal(c_df, c_expected)


def test_split_excel_into_dirs_DoesNothingIfColumnIsEmpty(tmp_path, output_dir):
    """Test handling of an empty column."""
    # ESTABLISH Create an Excel file with an empty column
    data = {
        "ID": [1, 2, 3],
        "Category": [None, None, None],
        "Value": [100, 200, 300],
    }
    df = DataFrame(data)
    file_path = tmp_path / "empty_column.xlsx"
    df.to_excel(file_path, index=False)

    # WHEN
    x_filename = "fizz"
    split_excel_into_dirs(file_path, output_dir, "Category", x_filename, "sheet5")

    # THEN Verify that no files are created
    created_files = list(output_dir.iterdir())
    print(f"{created_files=}")
    assert len(created_files) == 0


def test_split_excel_into_dirs_DoesCreateDirectoryIfColumnEmpty(
    sample_excel_file, tmp_path
):
    """Test if the output directory is created automatically."""
    # ESTABLISH
    output_dir = tmp_path / "nonexistent_output"
    x_filename = "fizz"

    # WHEN
    split_excel_into_dirs(
        sample_excel_file, output_dir, "Category", x_filename, "sheet5"
    )

    # THEN
    assert output_dir.exists()
    print(f"{list(output_dir.iterdir())=}")
    assert len(list(output_dir.iterdir())) > 0


def test_split_excel_into_dirs_SavesToCorrectFileNames(tmp_path, output_dir):
    """Test handling of invalid characters in unique values for filenames."""
    # ESTABLISH Create a DataFrame with special characters in the splitting column
    data = {
        "ID": [1, 2],
        "Category": ["A/B", "C\\D"],
        "Value": [100, 200],
    }
    df = DataFrame(data)
    file_path = tmp_path / "special_chars.xlsx"
    df.to_excel(file_path, index=False)
    x_filename = "fizz"
    b_file_path = create_path(output_dir, f"A_B/{x_filename}.xlsx")
    c_file_path = create_path(output_dir, f"C_D/{x_filename}.xlsx")
    assert os_path_exists(b_file_path) is False
    assert os_path_exists(c_file_path) is False

    # WHEN
    split_excel_into_dirs(file_path, output_dir, "Category", x_filename, "sheet5")

    # THEN
    assert os_path_exists(b_file_path)
    assert os_path_exists(c_file_path)
