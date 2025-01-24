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


def test_WorldUnit_idea_staging_to_fiscal_tables_CreatesFiscalStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)
        fis_objs = FiscalPrimeObjsRef(fizz_world._fiscal_mstr_dir)
        fis_cols = FiscalPrimeColumnsRef()
        assert db_table_exists(fiscal_db_conn, fis_objs.unit_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.deal_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.cash_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.hour_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.mont_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.week_agg_tablename)

        assert db_table_exists(fiscal_db_conn, fis_objs.unit_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.deal_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.cash_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.hour_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.mont_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.week_stage_tablename)

        fis_unit_agg_pragma = get_pragma_table_fetchall(fis_cols.unit_agg_columns)
        fis_deal_agg_pragma = get_pragma_table_fetchall(fis_cols.deal_agg_columns)
        fis_cash_agg_pragma = get_pragma_table_fetchall(fis_cols.cash_agg_columns)
        fis_hour_agg_pragma = get_pragma_table_fetchall(fis_cols.hour_agg_columns)
        fis_mont_agg_pragma = get_pragma_table_fetchall(fis_cols.mont_agg_columns)
        fis_week_agg_pragma = get_pragma_table_fetchall(fis_cols.week_agg_columns)
        fis_unit_stage_pragma = get_pragma_table_fetchall(fis_cols.unit_staging_columns)
        fis_deal_stage_pragma = get_pragma_table_fetchall(fis_cols.deal_staging_columns)
        fis_cash_stage_pragma = get_pragma_table_fetchall(fis_cols.cash_staging_columns)
        fis_hour_stage_pragma = get_pragma_table_fetchall(fis_cols.hour_staging_columns)
        fis_mont_stage_pragma = get_pragma_table_fetchall(fis_cols.mont_staging_columns)
        fis_week_stage_pragma = get_pragma_table_fetchall(fis_cols.week_staging_columns)
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"PRAGMA table_info({fis_objs.unit_agg_tablename})")
        assert fis_unit_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.deal_agg_tablename})")
        assert fis_deal_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.cash_agg_tablename})")
        assert fis_cash_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.hour_agg_tablename})")
        assert fis_hour_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.mont_agg_tablename})")
        assert fis_mont_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.week_agg_tablename})")
        assert fis_week_agg_pragma == cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({fis_objs.unit_stage_tablename})")
        assert fis_unit_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.deal_stage_tablename})")
        assert fis_deal_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.cash_stage_tablename})")
        assert fis_cash_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.hour_stage_tablename})")
        assert fis_hour_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.mont_stage_tablename})")
        assert fis_mont_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.week_stage_tablename})")
        assert fis_week_stage_pragma == cursor.fetchall()


def test_WorldUnit_idea_staging_to_fiscal_tables_Bud_category_idea_PopulatesFiscalStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.etl_aft_face_csv_files2idea_staging_tables(fiscal_db_conn)
        fis_objs = FiscalPrimeObjsRef(fizz_world._fiscal_mstr_dir)
        assert not db_table_exists(fiscal_db_conn, fis_objs.unit_stage_tablename)

        # WHEN
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, fis_objs.unit_stage_tablename) == 2
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"SELECT * FROM {fis_objs.unit_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row1 = (
            br00011_str,
            sue_inx,
            event3,
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
            None,  # note
        )
        expected_row2 = (
            br00011_str,
            sue_inx,
            event7,
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
            None,  # note
        )
        assert fiscalunit_db_rows == [expected_row1, expected_row2]
