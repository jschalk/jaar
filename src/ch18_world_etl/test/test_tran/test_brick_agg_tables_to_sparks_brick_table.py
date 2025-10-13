from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from src.ch17_idea.idea_db_tool import create_idea_sorted_table
from src.ch18_world_etl.transformers import (
    etl_brick_agg_tables_to_sparks_brick_agg_table,
    etl_sparks_brick_agg_db_to_spark_dict,
    etl_sparks_brick_agg_table_to_sparks_brick_valid_table,
)
from src.ref.keywords import Ch18Keywords as wx


def test_etl_brick_agg_tables_to_sparks_brick_agg_table_PopulatesTables_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    sue_str = "Sue"
    yao_str = "Yao"
    spark1 = 1
    spark3 = 3
    spark9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    agg_br00003_tablename = f"br00003_{wx.brick_agg}"
    agg_br00003_columns = [
        wx.spark_num,
        wx.face_name,
        wx.moment_label,
        wx.cumulative_minute,
        wx.hour_label,
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.moment_label}
, {wx.cumulative_minute}
, {wx.hour_label}
)"""
        values_clause = f"""
VALUES     
  ('{spark1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{spark1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{spark3}', '{yao_str}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{spark9}', '{yao_str}', '{a23_str}', '{minute_420}', '{hour7am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        brick_sparks_tablename = wx.sparks_brick_agg
        assert get_row_count(cursor, agg_br00003_tablename) == 4
        assert not db_table_exists(cursor, brick_sparks_tablename)

        # WHEN
        etl_brick_agg_tables_to_sparks_brick_agg_table(cursor)

        # THEN
        assert db_table_exists(cursor, brick_sparks_tablename)
        brick_sparks_table_cols = set(get_table_columns(cursor, brick_sparks_tablename))
        assert len(brick_sparks_table_cols) == 4
        assert wx.idea_number in brick_sparks_table_cols
        assert wx.face_name in brick_sparks_table_cols
        assert wx.spark_num in brick_sparks_table_cols
        assert wx.error_message in brick_sparks_table_cols
        assert get_row_count(cursor, brick_sparks_tablename) == 3
        select_agg_sqlstr = f"""
SELECT * 
FROM {brick_sparks_tablename} 
ORDER BY {wx.spark_num}, {wx.face_name};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 3
        sue_r = ("br00003", spark1, sue_str, None)
        yao3_r = ("br00003", spark3, yao_str, None)
        yao9_r = ("br00003", spark9, yao_str, None)
        print(f"{rows[0]=}")
        assert rows[0] == sue_r
        assert rows[1] == yao3_r
        assert rows[2] == yao9_r


def test_etl_brick_agg_tables_to_sparks_brick_agg_table_PopulatesTables_Scenario1():
    # ESTABLISH
    a23_str = "amy23"
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    spark1 = 1
    spark3 = 3
    spark9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    agg_br00003_tablename = f"br00003_{wx.brick_agg}"
    agg_br00003_columns = [
        wx.spark_num,
        wx.face_name,
        wx.moment_label,
        wx.cumulative_minute,
        wx.hour_label,
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.moment_label}
, {wx.cumulative_minute}
, {wx.hour_label}
)"""
        values_clause = f"""
VALUES     
  ('{spark1}', '{sue_str}', "{a23_str}", '{hour6am}', '{minute_360}')
, ('{spark1}', '{sue_str}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{spark1}', '{yao_str}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{spark9}', '{yao_str}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{spark3}', '{bob_str}', "{a23_str}", '{hour7am}', '{minute_420}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        brick_sparks_tablename = wx.sparks_brick_agg
        assert get_row_count(cursor, agg_br00003_tablename) == 5
        assert not db_table_exists(cursor, brick_sparks_tablename)

        # WHEN
        etl_brick_agg_tables_to_sparks_brick_agg_table(cursor)

        # THEN
        assert db_table_exists(cursor, brick_sparks_tablename)
        assert get_row_count(cursor, brick_sparks_tablename) == 4
        select_agg_sqlstr = f"""
SELECT * 
FROM {brick_sparks_tablename} 
ORDER BY {wx.spark_num}, {wx.face_name};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 4
        invalid_str = "invalid because of conflicting spark_num"
        bob_row = ("br00003", spark3, bob_str, None)
        sue_row = ("br00003", spark1, sue_str, invalid_str)
        yao1_row = ("br00003", spark1, yao_str, invalid_str)
        yao9_row = ("br00003", spark9, yao_str, None)

        assert rows[0] == sue_row
        assert rows[1] == yao1_row
        assert rows[2] == bob_row
        assert rows[3] == yao9_row


def test_etl_sparks_brick_agg_table_to_sparks_brick_valid_table_PopulatesTables_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    spark1 = 1
    spark3 = 3
    spark9 = 9
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        agg_sparks_tablename = wx.sparks_brick_agg
        agg_sparks_columns = [
            wx.idea_number,
            wx.spark_num,
            wx.face_name,
            wx.error_message,
        ]
        create_idea_sorted_table(cursor, agg_sparks_tablename, agg_sparks_columns)
        insert_into_clause = f"""INSERT INTO {agg_sparks_tablename} (
  {wx.idea_number}
, {wx.spark_num}
, {wx.face_name}
, {wx.error_message}
)"""
        invalid_str = "invalid because of conflicting spark_num"
        values_clause = f"""
VALUES
  ('br00003', {spark3}, '{bob_str}', NULL)
, ('br00003', {spark1}, '{sue_str}', '{invalid_str}')
, ('br00003', {spark1}, '{yao_str}', '{invalid_str}')
, ('br00003', {spark9}, '{yao_str}', NULL)  
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, agg_sparks_tablename) == 4
        valid_sparks_tablename = wx.sparks_brick_valid
        assert not db_table_exists(cursor, valid_sparks_tablename)

        # WHEN
        etl_sparks_brick_agg_table_to_sparks_brick_valid_table(cursor)

        # THEN
        assert db_table_exists(cursor, valid_sparks_tablename)
        assert get_row_count(cursor, valid_sparks_tablename) == 2
        select_agg_sqlstr = f"""
SELECT * 
FROM {valid_sparks_tablename} 
ORDER BY {wx.spark_num}, {wx.face_name};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 2
        bob_row = (spark3, bob_str)
        yao9_row = (spark9, yao_str)

        assert rows[0] == bob_row
        assert rows[1] == yao9_row


def test_etl_sparks_brick_agg_db_to_spark_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    spark1 = 1
    spark3 = 3
    spark9 = 9
    agg_columns = [wx.face_name, wx.spark_num, wx.error_message]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        agg_sparks_tablename = wx.sparks_brick_agg
        create_idea_sorted_table(cursor, agg_sparks_tablename, agg_columns)
        insert_into_clause = f"""
INSERT INTO {agg_sparks_tablename} ({wx.spark_num}, {wx.face_name}, {wx.error_message})
VALUES     
  ('{spark3}', '{bob_str}', NULL)
, ('{spark1}', '{sue_str}', 'invalid because of conflicting spark_num')
, ('{spark1}', '{yao_str}', 'invalid because of conflicting spark_num')
, ('{spark9}', '{yao_str}', NULL)
, ('{spark9}', '{yao_str}', NULL)
, ('{spark9}', '{yao_str}', NULL)
;
"""
        cursor.execute(insert_into_clause)
        etl_sparks_brick_agg_table_to_sparks_brick_valid_table(cursor)
        assert get_row_count(cursor, agg_sparks_tablename) == 6

        # WHEN
        sparks_dict = etl_sparks_brick_agg_db_to_spark_dict(cursor)

        # THEN
        assert sparks_dict == {spark3: bob_str, spark9: yao_str}
