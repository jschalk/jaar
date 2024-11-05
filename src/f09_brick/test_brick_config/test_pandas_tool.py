from src.f00_instrument.file import open_file, create_file_path, create_dir
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
    get_ex02_atom_dataframe,
    get_ex02_atom_csv,
)
from src.f00_instrument.examples.instrument_env import (
    env_dir_setup_cleanup,
    get_instrument_temp_env_dir,
)
from src.f04_gift.atom_config import acct_id_str, group_id_str
from src.f09_brick.pandas_tool import (
    save_dataframe_to_csv,
    get_ordered_csv,
    get_all_excel_sheet_names,
    get_relevant_columns_dataframe,
)
from os.path import exists as os_path_exists
from pandas import DataFrame, ExcelWriter


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
    ex_file_path = create_file_path(env_dir, ex_file_name)
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


def test_get_all_excel_sheet_names_ReturnsObj_Scenario0_NoFilter(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    sheet_name1 = "Sheet1x"
    sheet_name2 = "Sheet2x"
    create_dir(x_dir)
    with ExcelWriter(ex_file_path) as writer:
        df1.to_excel(writer, sheet_name=sheet_name1)
        df2.to_excel(writer, sheet_name=sheet_name2)

    # WHEN
    x_sheet_names = get_all_excel_sheet_names(env_dir)

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_file_name, sheet_name1) in x_sheet_names
    assert (x_dir, ex_file_name, sheet_name2) in x_sheet_names
    assert len(x_sheet_names) == 2


def test_get_all_excel_sheet_names_ReturnsObj_Scenario1_FilterSheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    sugar_str = "sugar"
    honey_name1 = "honey1x"
    sugar_name1 = f"{sugar_str}2x"
    sugar_name2 = f"honey_{sugar_str}3x"
    create_dir(x_dir)
    with ExcelWriter(ex_file_path) as writer:
        df1.to_excel(writer, sheet_name=honey_name1)
        df2.to_excel(writer, sheet_name=sugar_name1)
        df2.to_excel(writer, sheet_name=sugar_name2)

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
