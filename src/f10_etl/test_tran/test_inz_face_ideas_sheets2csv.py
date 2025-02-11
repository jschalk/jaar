from src.f00_instrument.file import create_path, open_file
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    fisc_title_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_db_tool import upsert_sheet
from src.f10_etl.transformers import etl_inz_face_ideas_to_csv_files
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame
from os.path import exists as os_path_exists


def test_etl_inz_face_ideas_to_csv_files_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    sue0 = [sue_inx, event3, accord23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, accord23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, accord23_str, yao_inx, yao_inx]
    sue3 = [sue_inx, event7, accord23_str, yao_inx, yao_inx]
    sue_accord23_df = DataFrame([sue0, sue1, sue2, sue3], columns=br00011_columns)
    inx_str = "inx"
    x_faces_inz_dir = create_path(get_test_etl_dir(), "inz")
    sue_inz_dir = create_path(x_faces_inz_dir, sue_inx)
    br00011_excel_filename = "br00011.xlsx"
    br00011_excel_path = create_path(sue_inz_dir, br00011_excel_filename)
    upsert_sheet(br00011_excel_path, inx_str, sue_accord23_df)

    br00011_csv_filename = "br00011.csv"
    br00011_csv_path = create_path(sue_inz_dir, br00011_csv_filename)
    assert os_path_exists(br00011_csv_path) is False

    # WHEN
    etl_inz_face_ideas_to_csv_files(x_faces_inz_dir)

    # THEN
    assert os_path_exists(br00011_csv_path)
    expected_csv = """face_name,event_int,fisc_title,owner_name,acct_name\nSuzy,3,accord23,Bob,Bob\nSuzy,3,accord23,Yao,Bob\nSuzy,3,accord23,Yao,Yao\nSuzy,7,accord23,Yao,Yao\n"""
    print(f"{expected_csv=}")
    assert open_file(br00011_csv_path) == expected_csv
