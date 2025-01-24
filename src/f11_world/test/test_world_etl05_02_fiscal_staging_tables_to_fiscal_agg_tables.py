from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import db_table_exists, get_row_count
from src.f04_gift.atom_config import (
    face_name_str,
    fiscal_title_str,
    acct_name_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_db_tool import get_pragma_table_fetchall
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeColumnsRef,
    FiscalPrimeObjsRef,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_idea_staging_to_fiscal_tables_PopulatesFiscalAggTables(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method

    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord45_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.etl_aft_face_csv_files2idea_staging_tables(fiscal_db_conn)
        fis_objs = FiscalPrimeObjsRef(fizz_world._fiscal_mstr_dir)
        assert not db_table_exists(fiscal_db_conn, fis_objs.unit_agg_tablename)

        # WHEN
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)

        # THEN
        assert db_table_exists(fiscal_db_conn, fis_objs.unit_agg_tablename)
        cursor = fiscal_db_conn.cursor()
        # cursor.execute(f"SELECT * FROM {fiscalunit_stage_tablename};")
        # fiscalunit_stage_rows = cursor.fetchall()
        # assert len(fiscalunit_stage_rows) == 4
        cursor.execute(f"SELECT * FROM {fis_objs.unit_agg_tablename};")
        fiscalunit_agg_rows = cursor.fetchall()
        expected_row1 = (
            accord23_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # present_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        expected_row2 = (
            accord45_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # present_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        assert fiscalunit_agg_rows == [expected_row1, expected_row2]
