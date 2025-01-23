from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.db_toolbox import db_table_exists
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    fiscal_title_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f10_etl.transformers import etl_etl_aft_face_csv_files2idea_staging_tables
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect


def test_etl_etl_aft_face_csv_files2idea_staging_tables_DBChanges(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    aft_faces_dir = get_test_etl_dir()
    sue_aft_dir = create_path(aft_faces_dir, sue_inx)
    br00011_str = "br00011"
    br00011_staging_tablename = f"{br00011_str}_staging"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        assert db_table_exists(fiscal_db_conn, br00011_staging_tablename) is False

        # ESTABLISH
        etl_etl_aft_face_csv_files2idea_staging_tables(fiscal_db_conn, aft_faces_dir)

        # THEN
        assert db_table_exists(fiscal_db_conn, br00011_staging_tablename)
        print(f"{type(fiscal_db_conn)=}")
        assert fiscal_db_conn != None
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"PRAGMA table_info({br00011_staging_tablename})")
        br00011_db_columns = cursor.fetchall()
        br00011_expected_columns = [
            (0, face_name_str(), "TEXT", 0, None, 0),
            (1, event_int_str(), "INTEGER", 0, None, 0),
            (2, fiscal_title_str(), "TEXT", 0, None, 0),
            (3, owner_name_str(), "TEXT", 0, None, 0),
            (4, acct_name_str(), "TEXT", 0, None, 0),
        ]
        print(f"      {br00011_db_columns=}")
        print(f"{br00011_expected_columns=}")
        assert br00011_db_columns == br00011_expected_columns
        cursor.execute(f"SELECT * FROM {br00011_staging_tablename}")
        br00011_db_rows = cursor.fetchall()
        expected_data = [
            (sue_inx, event3, accord23_str, bob_inx, bob_inx),
            (sue_inx, event3, accord23_str, yao_inx, bob_inx),
            (sue_inx, event3, accord23_str, yao_inx, yao_inx),
            (sue_inx, event7, accord23_str, yao_inx, yao_inx),
        ]
        assert br00011_db_rows == expected_data
