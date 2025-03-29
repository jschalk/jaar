from src.f00_instrument.file import open_file, create_path, get_dir_file_strs
from src.f04_stand.atom_config import acct_name_str, group_label_str, credor_respect_str
from src.f09_idea.examples.idea_env import (
    idea_env_setup_cleanup,
    idea_fiscs_dir,
    idea_examples_dir,
)
from src.f09_idea.examples.examples_pandas import (
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
from src.f09_idea.idea_db_tool import (
    save_dataframe_to_csv,
    get_ordered_csv,
    get_relevant_columns_dataframe,
    cart_staging_str,
    cart_agg_str,
    cart_valid_str,
    get_cart_staging_grouping_with_all_values_equal_df,
)
from os.path import exists as os_path_exists
from pandas import DataFrame


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
    # print(f"    {empty_csv=}")
    # print(f"{unordered_csv=}")
    assert get_ordered_csv(empty_dt) == """\n"""
    fizz0_order = ["fizz", "buzz", "x_boolean", "count"]
    count0_order = ["count", "fizz", "buzz", "x_boolean"]
    count0_buzz1_order = ["count", "buzz", "fizz", "x_boolean"]
    count0_xboolean1_order = ["count", "x_boolean", "fizz", "buzz"]
    print(f"                                {count_bool_csv=}")
    print(f"{get_ordered_csv(x1_dt, count0_xboolean1_order)=}")
    assert get_ordered_csv(x1_dt, fizz0_order) != unordered_csv
    assert get_ordered_csv(x1_dt, fizz0_order) == fizz_csv
    assert get_ordered_csv(x1_dt, count0_order) == count_csv
    assert get_ordered_csv(x1_dt, count0_buzz1_order) == count_buzz_csv
    assert get_ordered_csv(x1_dt, count0_xboolean1_order) == count_bool_csv
    # have sorting work even if sorting column does not exist
    count0_vic1_buzz2_order = ["count", "vic", "buzz", "fizz", "x_boolean"]
    assert get_ordered_csv(x1_dt, count0_vic1_buzz2_order) == count_buzz_csv


def test_save_dataframe_to_csv_SavesFile_Scenario0_SmallDataFrame(
    idea_env_setup_cleanup,
):
    # ESTABLISH
    env_dir = idea_examples_dir()
    small_dt = get_small_example01_dataframe()
    ex_filename = "fizzbuzz.csv"
    ex_file_path = create_path(env_dir, ex_filename)
    assert os_path_exists(ex_file_path) is False

    # WHEN
    save_dataframe_to_csv(small_dt, env_dir, ex_filename)

    # THEN
    assert os_path_exists(ex_file_path)
    small_example01_csv = get_small_example01_csv()
    assert open_file(env_dir, ex_filename) != small_example01_csv
    assert open_file(env_dir, ex_filename) != "\n\n\n\n"


def test_save_dataframe_to_csv_SavesFile_Scenario1_OrdersColumns(
    idea_env_setup_cleanup,
):
    # ESTABLISH
    env_dir = idea_examples_dir()
    atom_example_dt = get_ex02_atom_dataframe()
    ex_filename = "atom_example.csv"

    # WHEN
    save_dataframe_to_csv(atom_example_dt, env_dir, ex_filename)

    # THEN
    function_ex02_atom_csv = get_ex02_atom_csv()
    file_ex02_atom_csv = open_file(env_dir, ex_filename)
    print(f"{function_ex02_atom_csv=}")
    print(f"    {file_ex02_atom_csv=}")
    assert file_ex02_atom_csv == function_ex02_atom_csv


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
    relevant_columns = [spam_str, "not_relevant_else"]
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
    df1 = DataFrame([["AAA", "BBB"]], columns=[group_label_str(), acct_name_str()])

    # WHEN
    relevant_dataframe = get_relevant_columns_dataframe(df1)

    # THEN
    assert relevant_dataframe is not None
    print(f"{relevant_dataframe.columns=}")
    assert relevant_dataframe.columns.to_list()[0] == acct_name_str()
    assert relevant_dataframe.columns.to_list() == [acct_name_str(), group_label_str()]


def test_cart_staging_str_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert cart_staging_str() == "cart_staging"
    assert cart_agg_str() == "cart_agg"
    assert cart_valid_str() == "cart_valid"


def test_get_cart_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario0_EmptyDataframe():
    # ESTABLISH
    df1 = DataFrame([[]], columns=[])
    groupby_list = [group_label_str(), acct_name_str()]

    # WHEN
    groupby_dataframe = get_cart_staging_grouping_with_all_values_equal_df(
        df1, groupby_list
    )

    # THEN
    assert groupby_dataframe is not None
    assert len(groupby_dataframe) == len(DataFrame([[]], columns=[]))
    print(f"{groupby_dataframe.columns=}")
    assert groupby_dataframe.columns.to_list() == []


def test_get_cart_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario1_GroupBySingleColumn():
    # ESTABLISH
    df_columns = [group_label_str(), credor_respect_str()]
    before_df_values = [["AA0", "BB0"], ["AA0", "BB0"]]
    df1 = DataFrame(before_df_values, columns=df_columns)
    groupby_list = [group_label_str()]

    # WHEN
    groupby_dataframe = get_cart_staging_grouping_with_all_values_equal_df(
        df1, groupby_list
    )
    print(f"{groupby_dataframe=}")

    # THEN
    assert groupby_dataframe is not None
    after_df_values = [["AA0", "BB0"]]
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert len(groupby_dataframe) == len(after_df)
    print(f"{groupby_dataframe.columns=}")
    assert groupby_dataframe.columns.to_list() == after_df.columns.to_list()
    assert groupby_dataframe.to_csv() == after_df.to_csv()


def test_get_cart_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario2_GroupByExtraColumns():
    # ESTABLISH
    df_columns = [group_label_str(), credor_respect_str()]
    before_df_values = [["AA0", "BB0"], ["AA0", "BB0"]]
    df1 = DataFrame(before_df_values, columns=df_columns)
    groupby_list = [group_label_str(), acct_name_str()]

    # WHEN
    groupby_dataframe = get_cart_staging_grouping_with_all_values_equal_df(
        df1, groupby_list
    )
    print(f"{groupby_dataframe=}")

    # THEN
    assert groupby_dataframe is not None
    after_df_values = [["AA0", "BB0"]]
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert len(groupby_dataframe) == len(after_df)
    print(f"{groupby_dataframe.columns=}")
    assert groupby_dataframe.columns.to_list() == after_df.columns.to_list()
    assert groupby_dataframe.to_csv() == after_df.to_csv()


def test_get_cart_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario3_GroupByExtraColumns():
    # ESTABLISH
    df_columns = [group_label_str(), credor_respect_str(), "column3"]
    before_df_values = [["AA0", "BB0", "CC0"], ["AA0", "BB0", "CC0"]]
    df1 = DataFrame(before_df_values, columns=df_columns)
    groupby_list = [group_label_str(), acct_name_str(), credor_respect_str()]

    # WHEN
    groupby_dataframe = get_cart_staging_grouping_with_all_values_equal_df(
        df1, groupby_list
    )
    print(f"{groupby_dataframe=}")

    # THEN
    assert groupby_dataframe is not None
    after_df_values = [["AA0", "BB0", "CC0"]]
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert len(groupby_dataframe) == len(after_df)
    print(f"{groupby_dataframe.columns=}")
    assert groupby_dataframe.columns.to_list() == after_df.columns.to_list()
    assert groupby_dataframe.to_csv() == after_df.to_csv()


def test_get_cart_staging_grouping_with_all_values_equal_df_ReturnsObj_Scenario4_GroupByExtraColumns():
    # ESTABLISH
    df_columns = [group_label_str(), credor_respect_str(), "column3"]
    before_df_values = [
        ["AA0", "BB0", "CC0"],
        ["AA0", "BB0", "CC1"],
        ["DD0", "EE0", "FF0"],
    ]
    df1 = DataFrame(before_df_values, columns=df_columns)
    groupby_list = [group_label_str(), acct_name_str(), credor_respect_str()]

    # WHEN
    groupby_dataframe = get_cart_staging_grouping_with_all_values_equal_df(
        df1, groupby_list
    )
    print(f"{groupby_dataframe=}")

    # THEN
    after_df_values = [["DD0", "EE0", "FF0"]]
    assert groupby_dataframe is not None
    after_df = DataFrame(after_df_values, columns=df_columns)
    assert groupby_dataframe.columns.to_list() == after_df.columns.to_list()
    assert len(groupby_dataframe) == len(after_df)
    print(f"{groupby_dataframe.columns=}")
    assert groupby_dataframe.to_csv() == after_df.to_csv()
