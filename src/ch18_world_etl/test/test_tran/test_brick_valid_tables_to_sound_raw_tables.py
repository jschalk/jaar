from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count
from src.ch17_idea.idea_db_tool import create_idea_sorted_table
from src.ch18_world_etl.tran_sqlstrs import create_prime_tablename
from src.ch18_world_etl.transformers import etl_brick_valid_tables_to_sound_raw_tables
from src.ref.keywords import Ch18Keywords as kw

# get examples from tests from etl_brick_agg_dfs_to_translate_title_raw
# get examples from tests from etl_brick_agg_dfs_to_translate_rope_raw
# get examples from tests from etl_brick_agg_dfs_to_translate__raw
# get examples from tests from etl_brick_agg_dfs_to_translate_rope_raw


def test_etl_brick_valid_tables_to_sound_raw_tables_PopulatesValidTable_Scenario0_Only_valid_sparks():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()

        br00117_valid_tablename = f"br00117_{kw.brick_valid}"
        br00117_columns = [
            kw.spark_num,
            kw.face_name,
            kw.moment_label,
            kw.belief_name,
            kw.voice_name,
            kw.otx_rope,
            kw.inx_rope,
        ]
        create_idea_sorted_table(cursor, br00117_valid_tablename, set(br00117_columns))
        insert_into_clause = f"""INSERT INTO {br00117_valid_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.belief_name}
, {kw.voice_name}
, {kw.otx_rope}
, {kw.inx_rope}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ({spark1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        br00045_valid_tablename = f"br00045_{kw.brick_valid}"
        br00045_columns = [
            kw.spark_num,
            kw.face_name,
            kw.otx_rope,
            kw.inx_rope,
            kw.otx_knot,
            kw.inx_knot,
            kw.unknown_str,
        ]
        create_idea_sorted_table(cursor, br00045_valid_tablename, br00045_columns)
        insert_into_clause = f"""INSERT INTO {br00045_valid_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.otx_rope}
, {kw.inx_rope}
, {kw.otx_knot}
, {kw.inx_knot}
, {kw.unknown_str}
)"""
        values_clause = f"""
VALUES
  ({spark2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({spark5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, br00117_valid_tablename) == 2
        assert get_row_count(cursor, br00045_valid_tablename) == 3
        trlrope_s_raw_tablename = create_prime_tablename("TRLROPE", "s", "raw")
        blfvoce_s_put_raw_tblname = create_prime_tablename("BLFVOCE", "s", "raw", "put")
        assert not db_table_exists(cursor, trlrope_s_raw_tablename)
        assert not db_table_exists(cursor, blfvoce_s_put_raw_tblname)

        # WHEN
        etl_brick_valid_tables_to_sound_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, trlrope_s_raw_tablename) == 5
        assert get_row_count(cursor, blfvoce_s_put_raw_tblname) == 2
        b117 = "br00117"
        b045 = "br00045"
        ex_rope0 = (b117, spark1, sue_str, yao_str, yao_inx, None, None, None, None)
        ex_rope1 = (b117, spark1, sue_str, bob_str, bob_inx, None, None, None, None)
        ex_rope2 = (b045, spark2, sue_str, sue_str, sue_str, rdx, rdx, ukx, None)
        ex_rope3 = (b045, spark5, sue_str, bob_str, bob_inx, rdx, rdx, ukx, None)
        ex_rope4 = (b045, spark7, yao_str, yao_str, yao_inx, rdx, rdx, ukx, None)
        select_agg_sqlstr = f"""SELECT * FROM {trlrope_s_raw_tablename};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 5
        assert rows[0] == ex_rope2
        assert rows[1] == ex_rope3
        assert rows[2] == ex_rope4
        assert rows[3] == ex_rope0
        assert rows[4] == ex_rope1

        select_agg_sqlstr = f"""SELECT * FROM {blfvoce_s_put_raw_tblname};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert len(rows) == 2
        assert rows == [
            (b117, 1, sue_str, a23_str, bob_str, yao_str, None, None, None),
            (b117, 1, sue_str, a23_str, bob_str, bob_str, None, None, None),
        ]
