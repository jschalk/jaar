from src.f00_instrument.file import open_file, create_file_path
from src.f00_instrument.pandas_tool import (
    get_sorting_priority_atom_args,
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
    get_ex02_atom_dataframe,
    get_ex02_atom_csv,
)
from src.f00_instrument.examples.instrument_env import (
    env_dir_setup_cleanup,
    get_instrument_temp_env_dir,
)
from os.path import exists as os_path_exists


def test_get_sorting_priority_atom_args_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_sorting_priority_atom_args()

    # THEN
    assert table_sorting_priority[0] == "acct_id"
    assert table_sorting_priority[1] == "group_id"
    assert table_sorting_priority[2] == "parent_road"
    assert table_sorting_priority[3] == "label"
    assert table_sorting_priority[4] == "road"
    assert table_sorting_priority[5] == "base"
    assert table_sorting_priority[6] == "need"
    assert table_sorting_priority[7] == "pick"
    assert table_sorting_priority[8] == "team_id"
    assert table_sorting_priority[9] == "awardee_id"
    assert table_sorting_priority[10] == "healer_id"
    assert table_sorting_priority[11] == "numor"
    assert table_sorting_priority[12] == "denom"
    assert table_sorting_priority[13] == "addin"
    assert table_sorting_priority[14] == "base_item_active_requisite"
    assert table_sorting_priority[15] == "begin"
    assert table_sorting_priority[16] == "close"
    assert table_sorting_priority[17] == "credit_belief"
    assert table_sorting_priority[18] == "debtit_belief"
    assert table_sorting_priority[19] == "credit_vote"
    assert table_sorting_priority[20] == "debtit_vote"
    assert table_sorting_priority[21] == "credor_respect"
    assert table_sorting_priority[22] == "debtor_respect"
    assert table_sorting_priority[23] == "fopen"
    assert table_sorting_priority[24] == "fnigh"
    assert table_sorting_priority[25] == "fund_pool"
    assert table_sorting_priority[26] == "give_force"
    assert table_sorting_priority[27] == "gogo_want"
    assert table_sorting_priority[28] == "mass"
    assert table_sorting_priority[29] == "max_tree_traverse"
    assert table_sorting_priority[30] == "morph"
    assert table_sorting_priority[31] == "nigh"
    assert table_sorting_priority[32] == "open"
    assert table_sorting_priority[33] == "divisor"
    assert table_sorting_priority[34] == "pledge"
    assert table_sorting_priority[35] == "problem_bool"
    assert table_sorting_priority[36] == "purview_timestamp"
    assert table_sorting_priority[37] == "stop_want"
    assert table_sorting_priority[38] == "take_force"
    assert table_sorting_priority[39] == "tally"
    assert table_sorting_priority[40] == "fund_coin"
    assert table_sorting_priority[41] == "penny"
    assert table_sorting_priority[42] == "respect_bit"
    assert len(table_sorting_priority) == 43


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
    # have sorting work even if sorting column does not exist
    assert get_orderd_csv(x1_dt, ["count", "vic", "buzz"]) == count_buzz_csv


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
