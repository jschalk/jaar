from src.a00_data_toolbox.file_toolbox import create_path
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a02_finance_logic._utils.strs_a02 import fisc_word_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_word_str
from src.a17_creed_logic._utils.str_a17 import brick_raw_str, brick_agg_str
from src.a17_creed_logic.creed_db_tool import sheet_exists, create_creed_sorted_table
from src.a18_etl_toolbox.transformers import (
    etl_brick_raw_tables_to_brick_agg_tables,
    etl_brick_agg_tables_to_brick_agg_dfs,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect


def test_etl_brick_raw_tables_to_brick_agg_tables_PopulatesAggTable_Scenario0_GroupByWorks():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    raw_br00003_tablename = f"br00003_{brick_raw_str()}"
    raw_br00003_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        cumlative_minute_str(),
        hour_word_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_creed_sorted_table(cursor, raw_br00003_tablename, raw_br00003_columns)
        insert_into_clause = f"""INSERT INTO {raw_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_word_str()}
, {cumlative_minute_str()}
, {hour_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        agg_br00003_tablename = f"br00003_{brick_agg_str()}"
        assert get_row_count(cursor, raw_br00003_tablename) == 3
        assert not db_table_exists(cursor, agg_br00003_tablename)

        # WHEN
        etl_brick_raw_tables_to_brick_agg_tables(cursor)

        # THEN
        assert db_table_exists(cursor, agg_br00003_tablename)
        assert get_row_count(cursor, agg_br00003_tablename) == 2

        br00003_table_cols = get_table_columns(cursor, agg_br00003_tablename)
        file_dir_str = "file_dir"
        filename_str = "filename"
        sheet_name_str = "sheet_name"
        assert file_dir_str not in set(br00003_table_cols[0])
        assert filename_str not in set(br00003_table_cols[1])
        assert sheet_name_str not in set(br00003_table_cols[2])
        select_agg_sqlstr = f"""
SELECT * 
FROM {agg_br00003_tablename} 
ORDER BY {event_int_str()}, {cumlative_minute_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 2
        e1 = event1
        m_360 = minute_360
        m_420 = minute_420
        row0 = (e1, sue_str, a23_str, m_360, hour6am)
        row1 = (e1, sue_str, a23_str, m_420, hour7am)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0
        assert rows[1] == row1


def test_etl_brick_raw_tables_to_brick_agg_tables_PopulatesAggTable_Scenario1_GroupByOnlyNonConflictingRecords():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"

    raw_br00003_tablename = f"br00003_{brick_raw_str()}"
    raw_br00003_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        cumlative_minute_str(),
        hour_word_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_creed_sorted_table(cursor, raw_br00003_tablename, raw_br00003_columns)
        insert_into_clause = f"""INSERT INTO {raw_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_word_str()}
, {cumlative_minute_str()}
, {hour_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour8am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        agg_br00003_tablename = f"br00003_{brick_agg_str()}"
        assert get_row_count(cursor, raw_br00003_tablename) == 3
        assert not db_table_exists(cursor, agg_br00003_tablename)

        # WHEN
        etl_brick_raw_tables_to_brick_agg_tables(cursor)

        # THEN
        assert db_table_exists(cursor, agg_br00003_tablename)
        assert get_row_count(cursor, agg_br00003_tablename) == 1

        br00003_table_cols = get_table_columns(cursor, agg_br00003_tablename)
        file_dir_str = "file_dir"
        filename_str = "filename"
        sheet_name_str = "sheet_name"
        assert file_dir_str not in set(br00003_table_cols[0])
        assert filename_str not in set(br00003_table_cols[1])
        assert sheet_name_str not in set(br00003_table_cols[2])
        select_agg_sqlstr = f"""SELECT * FROM {agg_br00003_tablename};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 1
        e1 = event1
        m_360 = minute_360
        row0 = (e1, sue_str, a23_str, m_360, hour6am)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0


def test_etl_brick_agg_tables_to_brick_agg_dfs_PopulatesAggTable_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    minute_360 = 360
    minute_420 = 420
    minute_480 = 480
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"
    agg_br00003_tablename = f"br00003_{brick_agg_str()}"
    agg_br00003_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        cumlative_minute_str(),
        hour_word_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_creed_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_word_str()}
, {cumlative_minute_str()}
, {hour_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{event2}', '{sue_str}', '{a23_str}', '{minute_480}', '{hour8am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, agg_br00003_tablename) == 3
        brick_dir = create_path(get_module_temp_dir(), "brick")
        brick_file_path = create_path(brick_dir, "br00003.xlsx")
        assert not sheet_exists(brick_file_path, brick_agg_str())

        # WHEN
        etl_brick_agg_tables_to_brick_agg_dfs(db_conn, brick_dir)

        # THEN
        assert sheet_exists(brick_file_path, brick_agg_str())
        agg_df = pandas_read_excel(brick_file_path, sheet_name=brick_agg_str())
        row0 = [event1, sue_str, a23_str, minute_360, hour6am]
        row1 = [event1, sue_str, a23_str, minute_420, hour7am]
        row2 = [event2, sue_str, a23_str, minute_480, hour8am]
        ex_agg_df = DataFrame([row0, row1, row2], columns=agg_br00003_columns)
        print(f"{agg_df.columns=}")
        assert len(ex_agg_df.columns) == len(agg_df.columns)
        assert list(ex_agg_df.columns) == list(agg_df.columns)
        assert len(agg_df) > 0
        assert len(ex_agg_df) == len(agg_df)
        assert len(agg_df) == 3
        assert ex_agg_df.to_csv() == agg_df.to_csv()
