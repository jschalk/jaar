from os.path import exists as os_path_exists
from pandas import DataFrame
from src.a00_data_toolbox.file_toolbox import create_path
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    partner_name_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet
from src.a19_kpi_toolbox.test._util.a19_str import belief_kpi001_partner_nets_str
from src.a20_world_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.a20_world_logic.world import worldunit_shop


def test_WorldUnit_create_kpi_csvs_Senario0_EmptyWorld_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(worlds_dir(), "output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), output_dir)
    fay_world.sheets_input_to_clarity_mstr()
    kpi001_csv_path = create_path(output_dir, f"{belief_kpi001_partner_nets_str()}.csv")
    assert not os_path_exists(kpi001_csv_path)

    # WHEN
    fay_world.create_kpi_csvs()

    # THEN
    assert os_path_exists(kpi001_csv_path)


def test_WorldUnit_create_kpi_csvs_Senario1_Add_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(worlds_dir(), "output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), output_dir)
    sue_str = "Sue"
    event2 = 2
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    amy23_str = "amy23"
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        belief_label_str(),
        believer_name_str(),
        partner_name_str(),
    ]
    br00011_rows = [[event2, sue_str, amy23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    fay_world.sheets_input_to_clarity_mstr()
    kpi001_csv_path = create_path(output_dir, f"{belief_kpi001_partner_nets_str()}.csv")
    print(f"         {kpi001_csv_path=}")
    assert not os_path_exists(kpi001_csv_path)

    # WHEN
    fay_world.create_kpi_csvs()

    # THEN
    assert os_path_exists(kpi001_csv_path)
    expected_csv_str = "belief_label,believer_name,funds,fund_rank,tasks_count\n"
    assert open(kpi001_csv_path).read() == expected_csv_str
