from src.f00_instrument.file import open_file, create_file_path
from src.f00_instrument.pandas_tool import (
    get_sorting_priority_column_headers,
    save_dataframe_to_csv,
    get_ordered_csv,
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
    get_ex02_atom_dataframe,
    get_ex02_atom_csv,
)
from src.f00_instrument.examples.instrument_env import (
    env_dir_setup_cleanup,
    get_instrument_temp_env_dir,
)
from os.path import exists as os_path_exists


def test_get_sorting_priority_column_headers_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_sorting_priority_column_headers()

    # THEN
    assert table_sorting_priority[0] == "face_id"
    assert table_sorting_priority[1] == "python_type"
    assert table_sorting_priority[2] == "owner_id"
    assert table_sorting_priority[3] == "acct_id"
    assert table_sorting_priority[4] == "group_id"
    assert table_sorting_priority[5] == "parent_road"
    assert table_sorting_priority[6] == "label"
    assert table_sorting_priority[7] == "road"
    assert table_sorting_priority[8] == "base"
    assert table_sorting_priority[9] == "need"
    assert table_sorting_priority[10] == "pick"
    assert table_sorting_priority[11] == "team_id"
    assert table_sorting_priority[12] == "awardee_id"
    assert table_sorting_priority[13] == "healer_id"
    assert table_sorting_priority[14] == "numor"
    assert table_sorting_priority[15] == "denom"
    assert table_sorting_priority[16] == "addin"
    assert table_sorting_priority[17] == "base_item_active_requisite"
    assert table_sorting_priority[18] == "begin"
    assert table_sorting_priority[19] == "close"
    assert table_sorting_priority[20] == "credit_belief"
    assert table_sorting_priority[21] == "debtit_belief"
    assert table_sorting_priority[22] == "credit_vote"
    assert table_sorting_priority[23] == "debtit_vote"
    assert table_sorting_priority[24] == "credor_respect"
    assert table_sorting_priority[25] == "debtor_respect"
    assert table_sorting_priority[26] == "fopen"
    assert table_sorting_priority[27] == "fnigh"
    assert table_sorting_priority[28] == "fund_pool"
    assert table_sorting_priority[29] == "give_force"
    assert table_sorting_priority[30] == "gogo_want"
    assert table_sorting_priority[31] == "mass"
    assert table_sorting_priority[32] == "max_tree_traverse"
    assert table_sorting_priority[33] == "morph"
    assert table_sorting_priority[34] == "nigh"
    assert table_sorting_priority[35] == "open"
    assert table_sorting_priority[36] == "divisor"
    assert table_sorting_priority[37] == "pledge"
    assert table_sorting_priority[38] == "problem_bool"
    assert table_sorting_priority[39] == "purview_timestamp"
    assert table_sorting_priority[40] == "stop_want"
    assert table_sorting_priority[41] == "take_force"
    assert table_sorting_priority[42] == "tally"
    assert table_sorting_priority[43] == "fund_coin"
    assert table_sorting_priority[44] == "penny"
    assert table_sorting_priority[45] == "respect_bit"
    assert table_sorting_priority[46] == "otx_road_delimiter"
    assert table_sorting_priority[47] == "inx_road_delimiter"
    assert table_sorting_priority[48] == "unknown_word"
    assert table_sorting_priority[49] == "otx_word"
    assert table_sorting_priority[50] == "inx_word"
    assert table_sorting_priority[51] == "otx_label"
    assert table_sorting_priority[52] == "inx_label"
    assert len(table_sorting_priority) == 53


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
