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
from src.f01_road.finance_tran import quota_str, time_id_str, road_delimiter_str
from src.f03_chrono.chrono import (
    c400_number_str,
    timeline_label_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import (
    get_atom_args_category_mapping,
    face_id_str,
    obj_class_str,
    fiscal_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    road_str,
    base_str,
    team_id_str,
    awardee_id_str,
    healer_id_str,
    numor_str,
    denom_str,
    addin_str,
    base_item_active_requisite_str,
    begin_str,
    close_str,
    credit_belief_str,
    debtit_belief_str,
    credit_vote_str,
    debtit_vote_str,
    credor_respect_str,
    debtor_respect_str,
    fopen_str,
    fnigh_str,
    gogo_want_str,
    mass_str,
    morph_str,
    pledge_str,
    stop_want_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    give_force_str,
    take_force_str,
)
from src.f07_fiscal.fiscal_config import (
    get_fiscal_args_category_mapping,
    current_time_str,
    amount_str,
    month_label_str,
    hour_label_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_label_str,
    weekday_order_str,
)
from src.f08_filter.filter_config import (
    eon_id_str,
    otx_road_delimiter_str,
    inx_road_delimiter_str,
    unknown_word_str,
    otx_word_str,
    inx_word_str,
    otx_label_str,
    inx_label_str,
    get_filter_args_category_mapping,
)
from src.f09_brick.pandas_tool import (
    get_brick_elements_sort_order,
    get_brick_sqlite_type,
    save_dataframe_to_csv,
    get_ordered_csv,
    get_all_excel_sheet_names,
    get_relevant_columns_dataframe,
)
from os.path import exists as os_path_exists
from pandas import DataFrame, ExcelWriter


def test_get_brick_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_brick_elements_sort_order()

    # THEN
    assert table_sorting_priority[0] == face_id_str()
    assert table_sorting_priority[1] == eon_id_str()
    assert table_sorting_priority[2] == fiscal_id_str()
    assert table_sorting_priority[3] == obj_class_str()
    assert table_sorting_priority[4] == owner_id_str()
    assert table_sorting_priority[5] == acct_id_str()
    assert table_sorting_priority[6] == group_id_str()
    assert table_sorting_priority[7] == parent_road_str()
    assert table_sorting_priority[8] == label_str()
    assert table_sorting_priority[9] == road_str()
    assert table_sorting_priority[10] == base_str()
    assert table_sorting_priority[11] == "need"
    assert table_sorting_priority[12] == "pick"
    assert table_sorting_priority[13] == team_id_str()
    assert table_sorting_priority[14] == awardee_id_str()
    assert table_sorting_priority[15] == healer_id_str()
    assert table_sorting_priority[16] == time_id_str()
    assert table_sorting_priority[17] == begin_str()
    assert table_sorting_priority[18] == close_str()
    assert table_sorting_priority[19] == addin_str()
    assert table_sorting_priority[20] == numor_str()
    assert table_sorting_priority[21] == denom_str()
    assert table_sorting_priority[22] == morph_str()
    assert table_sorting_priority[23] == gogo_want_str()
    assert table_sorting_priority[24] == stop_want_str()
    assert table_sorting_priority[25] == base_item_active_requisite_str()
    assert table_sorting_priority[26] == credit_belief_str()
    assert table_sorting_priority[27] == debtit_belief_str()
    assert table_sorting_priority[28] == credit_vote_str()
    assert table_sorting_priority[29] == debtit_vote_str()
    assert table_sorting_priority[30] == credor_respect_str()
    assert table_sorting_priority[31] == debtor_respect_str()
    assert table_sorting_priority[32] == fopen_str()
    assert table_sorting_priority[33] == fnigh_str()
    assert table_sorting_priority[34] == "fund_pool"
    assert table_sorting_priority[35] == give_force_str()
    assert table_sorting_priority[36] == mass_str()
    assert table_sorting_priority[37] == "max_tree_traverse"
    assert table_sorting_priority[38] == "nigh"
    assert table_sorting_priority[39] == "open"
    assert table_sorting_priority[40] == "divisor"
    assert table_sorting_priority[41] == pledge_str()
    assert table_sorting_priority[42] == "problem_bool"
    assert table_sorting_priority[43] == "purview_time_id"
    assert table_sorting_priority[44] == take_force_str()
    assert table_sorting_priority[45] == "tally"
    assert table_sorting_priority[46] == fund_coin_str()
    assert table_sorting_priority[47] == penny_str()
    assert table_sorting_priority[48] == respect_bit_str()
    assert table_sorting_priority[49] == current_time_str()
    assert table_sorting_priority[50] == amount_str()
    assert table_sorting_priority[51] == month_label_str()
    assert table_sorting_priority[52] == hour_label_str()
    assert table_sorting_priority[53] == cumlative_minute_str()
    assert table_sorting_priority[54] == cumlative_day_str()
    assert table_sorting_priority[55] == weekday_label_str()
    assert table_sorting_priority[56] == weekday_order_str()
    assert table_sorting_priority[57] == otx_road_delimiter_str()
    assert table_sorting_priority[58] == inx_road_delimiter_str()
    assert table_sorting_priority[59] == unknown_word_str()
    assert table_sorting_priority[60] == otx_word_str()
    assert table_sorting_priority[61] == inx_word_str()
    assert table_sorting_priority[62] == otx_label_str()
    assert table_sorting_priority[63] == inx_label_str()
    assert table_sorting_priority[64] == road_delimiter_str()
    assert table_sorting_priority[65] == c400_number_str()
    assert table_sorting_priority[66] == yr1_jan1_offset_str()
    assert table_sorting_priority[67] == quota_str()
    assert table_sorting_priority[68] == monthday_distortion_str()
    assert table_sorting_priority[69] == timeline_label_str()
    assert len(table_sorting_priority) == 70
    atom_args = set(get_atom_args_category_mapping().keys())
    assert atom_args.issubset(set(table_sorting_priority))
    fiscal_args = set(get_fiscal_args_category_mapping().keys())
    print(f"{fiscal_args=}")
    print(f"{fiscal_args.difference(set(table_sorting_priority))=}")
    assert fiscal_args.issubset(set(table_sorting_priority))
    filter_args = set(get_filter_args_category_mapping().keys())
    assert filter_args.issubset(set(table_sorting_priority))
    atom_fiscal_filter_args = atom_args
    atom_fiscal_filter_args.update(fiscal_args)
    atom_fiscal_filter_args.update(filter_args)
    table_sorting_priority.remove(eon_id_str())
    table_sorting_priority.remove(face_id_str())
    table_sorting_priority.remove(obj_class_str())
    assert atom_fiscal_filter_args == set(table_sorting_priority)


def test_get_brick_sqlite_type_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_brick_sqlite_type()

    # THEN
    assert set(sqlite_types.keys()) == set(get_brick_elements_sort_order())
    assert sqlite_types.get(face_id_str()) == "TEXT" == "TEXT"
    assert sqlite_types.get(eon_id_str()) == "INTEGER"
    assert sqlite_types.get(fiscal_id_str()) == "TEXT"
    assert sqlite_types.get(obj_class_str()) == "TEXT"
    assert sqlite_types.get(owner_id_str()) == "TEXT"
    assert sqlite_types.get(acct_id_str()) == "TEXT"
    assert sqlite_types.get(group_id_str()) == "TEXT"
    assert sqlite_types.get(parent_road_str()) == "TEXT"
    assert sqlite_types.get(label_str()) == "TEXT"
    assert sqlite_types.get(road_str()) == "TEXT"
    assert sqlite_types.get(base_str()) == "TEXT"
    assert sqlite_types.get("need") == "TEXT"
    assert sqlite_types.get("pick") == "TEXT"
    assert sqlite_types.get(team_id_str()) == "TEXT"
    assert sqlite_types.get(awardee_id_str()) == "TEXT"
    assert sqlite_types.get(healer_id_str()) == "TEXT"
    assert sqlite_types.get(time_id_str()) == "INTEGER"
    assert sqlite_types.get(begin_str()) == "REAL"
    assert sqlite_types.get(close_str()) == "REAL"
    assert sqlite_types.get(addin_str()) == "REAL"
    assert sqlite_types.get(numor_str()) == "REAL"
    assert sqlite_types.get(denom_str()) == "REAL"
    assert sqlite_types.get(morph_str()) == "INTEGER"
    assert sqlite_types.get(gogo_want_str()) == "REAL"
    assert sqlite_types.get(stop_want_str()) == "REAL"
    assert sqlite_types.get(base_item_active_requisite_str()) == "TEXT"
    assert sqlite_types.get(credit_belief_str()) == "REAL"
    assert sqlite_types.get(debtit_belief_str()) == "REAL"
    assert sqlite_types.get(credit_vote_str()) == "REAL"
    assert sqlite_types.get(debtit_vote_str()) == "REAL"
    assert sqlite_types.get(credor_respect_str()) == "REAL"
    assert sqlite_types.get(debtor_respect_str()) == "REAL"
    assert sqlite_types.get(fopen_str()) == "REAL"
    assert sqlite_types.get(fnigh_str()) == "REAL"
    assert sqlite_types.get("fund_pool") == "REAL"
    assert sqlite_types.get(give_force_str()) == "REAL"
    assert sqlite_types.get(mass_str()) == "REAL"
    assert sqlite_types.get("max_tree_traverse") == "INT"
    assert sqlite_types.get("nigh") == "REAL"
    assert sqlite_types.get("open") == "REAL"
    assert sqlite_types.get("divisor") == "REAL"
    assert sqlite_types.get(pledge_str()) == "INTEGER"
    assert sqlite_types.get("problem_bool") == "INTEGER"
    assert sqlite_types.get("purview_time_id") == "INTEGER"
    assert sqlite_types.get(take_force_str()) == "REAL"
    assert sqlite_types.get("tally") == "REAL"
    assert sqlite_types.get(fund_coin_str()) == "REAL"
    assert sqlite_types.get(penny_str()) == "REAL"
    assert sqlite_types.get(respect_bit_str()) == "REAL"
    assert sqlite_types.get(current_time_str()) == "INTEGER"
    assert sqlite_types.get(amount_str()) == "REAL"
    assert sqlite_types.get(month_label_str()) == "TEXT"
    assert sqlite_types.get(hour_label_str()) == "TEXT"
    assert sqlite_types.get(cumlative_minute_str()) == "INTEGER"
    assert sqlite_types.get(cumlative_day_str()) == "INTEGER"
    assert sqlite_types.get(weekday_label_str()) == "TEXT"
    assert sqlite_types.get(weekday_order_str()) == "INTEGER"
    assert sqlite_types.get(otx_road_delimiter_str()) == "TEXT"
    assert sqlite_types.get(inx_road_delimiter_str()) == "TEXT"
    assert sqlite_types.get(unknown_word_str()) == "TEXT"
    assert sqlite_types.get(otx_word_str()) == "TEXT"
    assert sqlite_types.get(inx_word_str()) == "TEXT"
    assert sqlite_types.get(otx_label_str()) == "TEXT"
    assert sqlite_types.get(inx_label_str()) == "TEXT"
    assert sqlite_types.get(road_delimiter_str()) == "TEXT"
    assert sqlite_types.get(c400_number_str()) == "INTEGER"
    assert sqlite_types.get(yr1_jan1_offset_str()) == "INTEGER"
    assert sqlite_types.get(quota_str()) == "REAL"
    assert sqlite_types.get(monthday_distortion_str()) == "INTEGER"
    assert sqlite_types.get(timeline_label_str()) == "TEXT"


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
