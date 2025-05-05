from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.a17_idea_logic.idea_db_tool import create_idea_sorted_table
from src.a17_idea_logic._utils.str_a17 import brick_valid_str
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a18_etl_toolbox.transformers import etl_brick_valid_tables_to_sound_raw_tables
from sqlite3 import connect as sqlite3_connect

# get examples from tests from etl_brick_agg_dfs_to_pidgin_label_raw
# get examples from tests from etl_brick_agg_dfs_to_pidgin_road_raw
# get examples from tests from etl_brick_agg_dfs_to_pidgin__raw
# get examples from tests from etl_brick_agg_dfs_to_pidgin_road_raw


def test_etl_brick_valid_tables_to_sound_raw_tables_PopulatesValidTable_Scenario0_Only_valid_events():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()

        br00117_valid_tablename = f"br00117_{brick_valid_str()}"
        br00117_columns = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_road_str(),
            inx_road_str(),
        ]
        create_idea_sorted_table(cursor, br00117_valid_tablename, br00117_columns)
        insert_into_clause = f"""INSERT INTO {br00117_valid_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_road_str()}
, {inx_road_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ({event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        br00045_valid_tablename = f"br00045_{brick_valid_str()}"
        br00045_columns = [
            event_int_str(),
            face_name_str(),
            otx_road_str(),
            inx_road_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
        create_idea_sorted_table(cursor, br00045_valid_tablename, br00045_columns)
        insert_into_clause = f"""INSERT INTO {br00045_valid_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, br00117_valid_tablename) == 2
        assert get_row_count(cursor, br00045_valid_tablename) == 3
        pidroad_s_raw_tablename = create_prime_tablename("PIDROAD", "s", "raw")
        budacct_s_put_raw_tblname = create_prime_tablename("BUDACCT", "s", "raw", "put")
        assert not db_table_exists(cursor, pidroad_s_raw_tablename)
        assert not db_table_exists(cursor, budacct_s_put_raw_tblname)

        # WHEN
        etl_brick_valid_tables_to_sound_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, pidroad_s_raw_tablename) == 5
        assert get_row_count(cursor, budacct_s_put_raw_tblname) == 2
        b117 = "br00117"
        b045 = "br00045"
        ex_road0 = (b117, event1, sue_str, yao_str, yao_inx, None, None, None, None)
        ex_road1 = (b117, event1, sue_str, bob_str, bob_inx, None, None, None, None)
        ex_road2 = (b045, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx, None)
        ex_road3 = (b045, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx, None)
        ex_road4 = (b045, event7, yao_str, yao_str, yao_inx, rdx, rdx, ukx, None)
        select_agg_sqlstr = f"""SELECT * FROM {pidroad_s_raw_tablename};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 5
        assert rows[0] == ex_road2
        assert rows[1] == ex_road3
        assert rows[2] == ex_road4
        assert rows[3] == ex_road0
        assert rows[4] == ex_road1

        select_agg_sqlstr = f"""SELECT * FROM {budacct_s_put_raw_tblname};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert len(rows) == 2
        assert rows == [
            (b117, 1, sue_str, a23_str, bob_str, yao_str, None, None, None),
            (b117, 1, sue_str, a23_str, bob_str, bob_str, None, None, None),
        ]
