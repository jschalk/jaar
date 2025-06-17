from os.path import exists as os_path_exists
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal
from shutil import copy2 as shutil_copy2
from src.a00_data_toolbox.file_toolbox import create_path, set_dir
from src.a02_finance_logic._util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic._util.a06_str import acct_name_str
from src.a09_pack_logic._util.a09_str import event_int_str, face_name_str
from src.a17_idea_logic.idea_db_tool import get_sheet_names, sheet_exists, upsert_sheet
from src.a19_kpi_toolbox._util.a19_str import vow_kpi001_acct_nets_str
from src.a19_kpi_toolbox.kpi_mstr import get_kpi_dir
from src.a20_world_logic._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.a20_world_logic.world import worldunit_shop


def test_WorldUnit_create_kpi_csvs_Senario0_EmptyWorld_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    fizz_world.mud_to_clarity_mstr()
    kpi_dir = get_kpi_dir(fizz_world._vow_mstr_dir)
    kpi001_csv_path = create_path(kpi_dir, f"{vow_kpi001_acct_nets_str()}.csv")
    assert not os_path_exists(kpi001_csv_path)

    # WHEN
    fizz_world.create_kpi_csvs()

    # THEN
    assert os_path_exists(kpi001_csv_path)


def test_WorldUnit_create_kpi_csvs_Senario1_Add_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    sue_str = "Sue"
    event2 = 2
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    accord23_str = "accord23"
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        vow_label_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    br00011_rows = [[event2, sue_str, accord23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(mud_file_path, "br00011_ex3", br00011_df)
    fizz_world.mud_to_clarity_mstr()
    kpi_dir = get_kpi_dir(fizz_world._vow_mstr_dir)
    kpi001_csv_path = create_path(kpi_dir, f"{vow_kpi001_acct_nets_str()}.csv")
    print(f"         {kpi001_csv_path=}")
    assert not os_path_exists(kpi001_csv_path)

    # WHEN
    fizz_world.create_kpi_csvs()

    # THEN
    assert os_path_exists(kpi001_csv_path)
    expected_csv_str = "vow_label,owner_name,funds,fund_rank,tasks_count\n"
    assert open(kpi001_csv_path).read() == expected_csv_str
