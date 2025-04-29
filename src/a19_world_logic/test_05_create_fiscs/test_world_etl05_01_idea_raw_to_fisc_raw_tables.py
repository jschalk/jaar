from src.a00_data_toolbox.file_toolbox import create_path, save_file, open_file
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a02_finance_logic._utils.strs_a02 import (
    deal_time_str,
    owner_name_str,
    fisc_tag_str,
)
from src.a08_bud_atom_logic.atom_config import (
    face_name_str,
    acct_name_str,
    event_int_str,
)
from src.a17_idea_logic.idea_db_tool import get_pragma_table_fetchall
from src.a18_etl_toolbox.tran_sqlstrs import create_fisc_prime_tables
from src.a18_etl_toolbox.fisc_etl_tool import FiscPrimeColumnsRef, FiscPrimeObjsRef
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_idea_raw_to_fisc_tables_CreatesFiscRawTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.idea_raw_to_fisc_tables(cursor)
        fisc_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
        fisc_cols = FiscPrimeColumnsRef()
        assert db_table_exists(cursor, fisc_objs.unit_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.week_agg_tablename)

        assert db_table_exists(cursor, fisc_objs.unit_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.week_raw_tablename)

        fisc_unit_agg_pragma = get_pragma_table_fetchall(fisc_cols.unit_agg_columns)
        fisc_deal_agg_pragma = get_pragma_table_fetchall(fisc_cols.deal_agg_columns)
        fisc_cash_agg_pragma = get_pragma_table_fetchall(fisc_cols.cash_agg_columns)
        fisc_hour_agg_pragma = get_pragma_table_fetchall(fisc_cols.hour_agg_columns)
        fisc_mont_agg_pragma = get_pragma_table_fetchall(fisc_cols.mont_agg_columns)
        fisc_week_agg_pragma = get_pragma_table_fetchall(fisc_cols.week_agg_columns)
        fisc_unit_raw_pragma = get_pragma_table_fetchall(fisc_cols.unit_raw_columns)
        fisc_deal_raw_pragma = get_pragma_table_fetchall(fisc_cols.deal_raw_columns)
        fisc_cash_raw_pragma = get_pragma_table_fetchall(fisc_cols.cash_raw_columns)
        fisc_hour_raw_pragma = get_pragma_table_fetchall(fisc_cols.hour_raw_columns)
        fisc_mont_raw_pragma = get_pragma_table_fetchall(fisc_cols.mont_raw_columns)
        fisc_week_raw_pragma = get_pragma_table_fetchall(fisc_cols.week_raw_columns)
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

        cursor.execute(f"PRAGMA table_info({fisc_objs.unit_raw_tablename})")
        assert fisc_unit_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.deal_raw_tablename})")
        assert fisc_deal_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.cash_raw_tablename})")
        assert fisc_cash_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.hour_raw_tablename})")
        assert fisc_hour_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.mont_raw_tablename})")
        assert fisc_mont_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.week_raw_tablename})")
        assert fisc_week_raw_pragma == cursor.fetchall()


def test_WorldUnit_idea_raw_to_fisc_tables_Bud_dimen_idea_PopulatesFiscRawTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    sue_inz_dir = create_path(fizz_world._syntax_inz_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_tag_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.inz_face_csv_files2idea_raw_tables(cursor)
        fisc_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
        assert not db_table_exists(cursor, fisc_objs.unit_raw_tablename)

        # WHEN
        fizz_world.idea_raw_to_fisc_tables(cursor)

        # THEN
        assert get_row_count(cursor, fisc_objs.unit_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {fisc_objs.unit_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row1 = (
            br00011_str,
            sue_inx,
            event3,
            accord23_str,  # fisc_tag
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_tag
            None,  # job_listen_rotations
            None,  # note
        )
        expected_row2 = (
            br00011_str,
            sue_inx,
            event7,
            accord23_str,  # fisc_tag
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_tag
            None,  # job_listen_rotations
            None,  # note
        )
        assert fiscunit_db_rows == [expected_row1, expected_row2]


def test_WorldUnit_set_idea_raw_error_message_ChangeAttrs(env_dir_setup_cleanup):
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
    fizz_world = worldunit_shop("fizz", worlds_dir())

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.deal_raw_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.deal_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_2},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_tag_str()}, {deal_time_str()}, error_message FROM {x_tablename};"
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
        fizz_world.idea_raw_to_fisc_tables(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t2_deal_time, None),
            (event7, accord45_str, t1_deal_time, None),
            (event7, accord45_str, t2_deal_time, None),
        ]
