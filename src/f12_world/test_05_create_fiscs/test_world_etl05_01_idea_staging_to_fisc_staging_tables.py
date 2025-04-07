from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import db_table_exists, get_row_count
from src.f01_road.deal import deal_time_str, owner_name_str, fisc_title_str
from src.f04_kick.atom_config import face_name_str, acct_name_str, event_int_str
from src.f10_idea.idea_db_tool import get_pragma_table_fetchall
from src.f11_etl.tran_sqlstrs import create_fisc_tables
from src.f11_etl.fisc_etl_tool import FiscPrimeColumnsRef, FiscPrimeObjsRef
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_idea_staging_to_fisc_tables_CreatesFiscStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.idea_staging_to_fisc_tables(cursor)
        fisc_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
        fisc_cols = FiscPrimeColumnsRef()
        assert db_table_exists(cursor, fisc_objs.unit_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.week_agg_tablename)

        assert db_table_exists(cursor, fisc_objs.unit_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.week_stage_tablename)

        fisc_unit_agg_pragma = get_pragma_table_fetchall(fisc_cols.unit_agg_columns)
        fisc_deal_agg_pragma = get_pragma_table_fetchall(fisc_cols.deal_agg_columns)
        fisc_cash_agg_pragma = get_pragma_table_fetchall(fisc_cols.cash_agg_columns)
        fisc_hour_agg_pragma = get_pragma_table_fetchall(fisc_cols.hour_agg_columns)
        fisc_mont_agg_pragma = get_pragma_table_fetchall(fisc_cols.mont_agg_columns)
        fisc_week_agg_pragma = get_pragma_table_fetchall(fisc_cols.week_agg_columns)
        fisc_unit_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.unit_staging_columns
        )
        fisc_deal_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.deal_staging_columns
        )
        fisc_cash_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.cash_staging_columns
        )
        fisc_hour_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.hour_staging_columns
        )
        fisc_mont_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.mont_staging_columns
        )
        fisc_week_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.week_staging_columns
        )
        cursor.execute(f"PRAGMA table_info({fisc_objs.unit_agg_tablename})")
        assert fisc_unit_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.deal_agg_tablename})")
        assert fisc_deal_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.cash_agg_tablename})")
        assert fisc_cash_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.hour_agg_tablename})")
        assert fisc_hour_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.mont_agg_tablename})")
        assert fisc_mont_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.week_agg_tablename})")
        assert fisc_week_agg_pragma == cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({fisc_objs.unit_stage_tablename})")
        assert fisc_unit_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.deal_stage_tablename})")
        assert fisc_deal_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.cash_stage_tablename})")
        assert fisc_cash_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.hour_stage_tablename})")
        assert fisc_hour_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.mont_stage_tablename})")
        assert fisc_mont_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.week_stage_tablename})")
        assert fisc_week_stage_pragma == cursor.fetchall()


def test_WorldUnit_idea_staging_to_fisc_tables_Bud_dimen_idea_PopulatesFiscStagingTables(
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
    sue_inz_dir = create_path(fizz_world._faces_inz_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.inz_face_csv_files2idea_staging_tables(cursor)
        fisc_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
        assert not db_table_exists(cursor, fisc_objs.unit_stage_tablename)

        # WHEN
        fizz_world.idea_staging_to_fisc_tables(cursor)

        # THEN
        assert get_row_count(cursor, fisc_objs.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {fisc_objs.unit_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row1 = (
            br00011_str,
            sue_inx,
            event3,
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
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
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
            None,  # note
        )
        assert fiscunit_db_rows == [expected_row1, expected_row2]


def test_WorldUnit_set_idea_staging_error_message_ChangeAttrs(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_owner_name = bob_inx
    t1_deal_time = 33
    t1_quota_1 = 200
    t1_quota_2 = 300
    t2_deal_time = 55
    t2_quota = 400
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()
    fizz_world = worldunit_shop("fizz")

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.deal_stage_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.deal_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_2},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, {deal_time_str()}, error_message FROM {x_tablename};"
        # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        # print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        # print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, t1_deal_time, None),
            (event7, accord23_str, t1_deal_time, None),
            (event7, accord23_str, t2_deal_time, None),
            (event7, accord45_str, t1_deal_time, None),
            (event7, accord45_str, t2_deal_time, None),
        ]

        # WHEN
        fizz_world.idea_staging_to_fisc_tables(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent fisc data"
        assert rows == [
            (event3, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t2_deal_time, None),
            (event7, accord45_str, t1_deal_time, None),
            (event7, accord45_str, t2_deal_time, None),
        ]
