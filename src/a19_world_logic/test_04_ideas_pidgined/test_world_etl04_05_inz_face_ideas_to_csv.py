from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import acct_name_str, face_name_str, event_int_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame
from os.path import exists as os_path_exists


def test_WorldUnit_inz_face_ideas_to_csv_files_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    sue0 = [sue_inx, event3, accord23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, accord23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, accord23_str, yao_inx, yao_inx]
    sue3 = [sue_inx, event7, accord23_str, yao_inx, yao_inx]
    sue_accord23_df = DataFrame([sue0, sue1, sue2, sue3], columns=br00011_columns)
    fizz_world = worldunit_shop("fizz", worlds_dir())
    inx_str = "inx"
    sue_inz_dir = create_path(fizz_world._syntax_inz_dir, sue_inx)
    br00011_excel_filename = "br00011.xlsx"
    br00011_excel_path = create_path(sue_inz_dir, br00011_excel_filename)
    upsert_sheet(br00011_excel_path, inx_str, sue_accord23_df)

    br00011_csv_filename = "br00011.csv"
    br00011_csv_path = create_path(sue_inz_dir, br00011_csv_filename)
    assert os_path_exists(br00011_csv_path) is False

    # WHEN
    fizz_world.inz_face_ideas_to_csv_files()

    # THEN
    assert os_path_exists(br00011_csv_path)
    expected_csv = """face_name,event_int,fisc_tag,owner_name,acct_name
Suzy,3,accord23,Bob,Bob
Suzy,3,accord23,Yao,Bob
Suzy,3,accord23,Yao,Yao
Suzy,7,accord23,Yao,Yao
"""
    print(f"{expected_csv=}")
    assert open_file(br00011_csv_path) == expected_csv
