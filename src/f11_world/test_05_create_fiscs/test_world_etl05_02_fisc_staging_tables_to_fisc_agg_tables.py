from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.db_toolbox import db_table_exists
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f04_gift.atom_config import face_name_str, acct_name_str, event_int_str
from src.f10_etl.fisc_etl_tool import FiscPrimeObjsRef
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_idea_staging_to_fisc_tables_PopulatesFiscAggTables(
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
    sue_inz_dir = create_path(fizz_world._faces_inz_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord45_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.etl_inz_face_csv_files2idea_staging_tables(cursor)
        fisc_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
        assert not db_table_exists(cursor, fisc_objs.unit_agg_tablename)

        # WHEN
        fizz_world.idea_staging_to_fisc_tables(cursor)

        # THEN
        assert db_table_exists(cursor, fisc_objs.unit_agg_tablename)
        # cursor.execute(f"SELECT * FROM {fiscunit_stage_tablename};")
        # fiscunit_stage_rows = cursor.fetchall()
        # assert len(fiscunit_stage_rows) == 4
        cursor.execute(f"SELECT * FROM {fisc_objs.unit_agg_tablename};")
        fiscunit_agg_rows = cursor.fetchall()
        expected_row1 = (
            accord23_str,  # fisc_title
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
            accord45_str,  # fisc_title
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
        assert fiscunit_agg_rows == [expected_row1, expected_row2]


def test_WorldUnit_idea_staging_to_fisc_tables_PopulatesTable_fisc_event_time(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event2 = 2
    event3 = 3
    event7 = 7
    event8 = 8
    accord23_str = "accord23"
    accord45_str = "accord45"
    timepoint22 = 22
    timepoint23 = 23
    timepoint800 = 800
    timepoint900 = 900
    quota_t8 = 8888
    quota_t9 = 9999
    amount_t22 = 2222
    amount_t23 = 2323
    x_ledger_depth = 2
    fizz_world = worldunit_shop("fizz")
    sue_inz_dir = create_path(fizz_world._faces_inz_dir, sue_inx)
    # create deal rows
    # create cash rows
    br00001_str = "br00001"
    br00002_str = "br00002"
    br00001_csv_filename = f"{br00001_str}.csv"
    br00002_csv_filename = f"{br00002_str}.csv"
    br00001_csv_str = f"""{face_name_str()},{event_int_str()},fisc_title,owner_name,time_int,quota,ledger_depth
{sue_inx},{event3},{accord23_str},{bob_inx},{timepoint800},{quota_t8},{x_ledger_depth}
{sue_inx},{event3},{accord23_str},{yao_inx},{timepoint800},{quota_t8},{x_ledger_depth}
{sue_inx},{event3},{accord45_str},{yao_inx},{timepoint800},{quota_t8},{x_ledger_depth}
{sue_inx},{event7},{accord45_str},{yao_inx},{timepoint900},{quota_t9},{x_ledger_depth}
"""
    br00002_csv_str = f"""{face_name_str()},{event_int_str()},fisc_title,owner_name,acct_name,time_int,amount
{sue_inx},{event2},{accord23_str},{bob_inx},{sue_inx},{timepoint22},{amount_t22}
{sue_inx},{event2},{accord23_str},{yao_inx},{sue_inx},{timepoint22},{amount_t22}
{sue_inx},{event2},{accord45_str},{yao_inx},{sue_inx},{timepoint22},{amount_t22}
{sue_inx},{event8},{accord45_str},{yao_inx},{bob_inx},{timepoint23},{amount_t23}
"""
    save_file(sue_inz_dir, br00001_csv_filename, br00001_csv_str)
    save_file(sue_inz_dir, br00002_csv_filename, br00002_csv_str)
    fizz_world = worldunit_shop("fizz")

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.etl_inz_face_csv_files2idea_staging_tables(cursor)
        event_time_tablename = "fisc_event_time_agg"
        assert not db_table_exists(cursor, event_time_tablename)

        # WHEN
        fizz_world.idea_staging_to_fisc_tables(cursor)

        # THEN
        assert db_table_exists(cursor, event_time_tablename)
        # cursor.execute(f"SELECT * FROM {fiscunit_stage_tablename};")
        # fiscunit_stage_rows = cursor.fetchall()
        # assert len(fiscunit_stage_rows) == 4
        event_time_select_sql = f"""SELECT fisc_title, event_int, time_int, error_message 
FROM {event_time_tablename}
;
"""
        cursor.execute(event_time_select_sql)
        fiscunit_agg_rows = cursor.fetchall()
        # fisc_title, owner_name
        expected_row0 = (accord23_str, event2, timepoint22, "sorted")
        expected_row1 = (accord23_str, event3, timepoint800, "sorted")
        expected_row2 = (accord45_str, event2, timepoint22, "sorted")
        expected_row3 = (accord45_str, event3, timepoint800, "sorted")
        expected_row4 = (accord45_str, event7, timepoint900, "sorted")
        expected_row5 = (accord45_str, event8, timepoint23, "not sorted")
        assert fiscunit_agg_rows == [
            expected_row0,
            expected_row1,
            expected_row2,
            expected_row3,
            expected_row4,
            expected_row5,
        ]
