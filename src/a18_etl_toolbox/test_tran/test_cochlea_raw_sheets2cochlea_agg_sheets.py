from src.a00_data_toolboxs.file_toolbox import create_path
from src.a00_data_toolboxs.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
    create_table_from_columns,
)
from src.a02_finance_toolboxs.deal import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import (
    cochlea_raw_str,
    cochlea_agg_str,
    sheet_exists,
)
from src.a18_etl_toolbox.transformers import (
    etl_cochlea_raw_db_to_cochlea_agg_db,
    etl_cochlea_agg_db_to_cochlea_agg_df,
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect


def test_etl_cochlea_raw_db_to_cochlea_agg_db_PopulatesAggTable_Scenario0_GroupByWorks():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    raw_br00003_tablename = f"{cochlea_raw_str()}_br00003"
    raw_br00003_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        cumlative_minute_str(),
        hour_tag_str(),
    ]
    raw_br00003_types = {
        face_name_str(): "TEXT",
        event_int_str(): "TEXT",
        fisc_tag_str(): "TEXT",
        cumlative_minute_str(): "TEXT",
        hour_tag_str(): "TEXT",
    }
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_table_from_columns(
            cursor, raw_br00003_tablename, raw_br00003_columns, raw_br00003_types
        )
        insert_into_clause = f"""INSERT INTO {raw_br00003_tablename} (
  {face_name_str()}
, {event_int_str()}
, {fisc_tag_str()}
, {cumlative_minute_str()}
, {hour_tag_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event_1}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{sue_str}', '{event_1}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{sue_str}', '{event_1}', '{a23_str}', '{minute_420}', '{hour7am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        agg_br00003_tablename = f"{cochlea_agg_str()}_br00003"
        assert get_row_count(cursor, raw_br00003_tablename) == 3
        assert not db_table_exists(cursor, agg_br00003_tablename)

        # WHEN
        etl_cochlea_raw_db_to_cochlea_agg_db(cursor)

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
        e1 = event_1
        m_360 = minute_360
        m_420 = minute_420
        row0 = (sue_str, e1, a23_str, m_360, hour6am)
        row1 = (sue_str, e1, a23_str, m_420, hour7am)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0
        assert rows[1] == row1


def test_etl_cochlea_raw_db_to_cochlea_agg_db_PopulatesAggTable_Scenario1_GroupByOnlyNonConflictingRecords():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"

    raw_br00003_tablename = f"{cochlea_raw_str()}_br00003"
    raw_br00003_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        cumlative_minute_str(),
        hour_tag_str(),
    ]
    raw_br00003_types = {
        face_name_str(): "TEXT",
        event_int_str(): "TEXT",
        fisc_tag_str(): "TEXT",
        cumlative_minute_str(): "TEXT",
        hour_tag_str(): "TEXT",
    }
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_table_from_columns(
            cursor, raw_br00003_tablename, raw_br00003_columns, raw_br00003_types
        )
        insert_into_clause = f"""INSERT INTO {raw_br00003_tablename} (
  {face_name_str()}
, {event_int_str()}
, {fisc_tag_str()}
, {cumlative_minute_str()}
, {hour_tag_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event_1}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{sue_str}', '{event_1}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{sue_str}', '{event_1}', '{a23_str}', '{minute_420}', '{hour8am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        agg_br00003_tablename = f"{cochlea_agg_str()}_br00003"
        assert get_row_count(cursor, raw_br00003_tablename) == 3
        assert not db_table_exists(cursor, agg_br00003_tablename)

        # WHEN
        etl_cochlea_raw_db_to_cochlea_agg_db(cursor)

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
        e1 = event_1
        m_360 = minute_360
        row0 = (sue_str, e1, a23_str, m_360, hour6am)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0


def test_etl_cochlea_agg_db_to_cochlea_agg_df_PopulatesAggTable_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event_1 = 1
    event_2 = 2
    minute_360 = 360
    minute_420 = 420
    minute_480 = 480
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"
    agg_br00003_tablename = f"{cochlea_agg_str()}_br00003"
    agg_br00003_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        cumlative_minute_str(),
        hour_tag_str(),
    ]
    agg_br00003_types = {
        face_name_str(): "TEXT",
        event_int_str(): "TEXT",
        fisc_tag_str(): "TEXT",
        cumlative_minute_str(): "TEXT",
        hour_tag_str(): "TEXT",
    }
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_table_from_columns(
            cursor, agg_br00003_tablename, agg_br00003_columns, agg_br00003_types
        )
        insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {face_name_str()}
, {event_int_str()}
, {fisc_tag_str()}
, {cumlative_minute_str()}
, {hour_tag_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event_1}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{sue_str}', '{event_1}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{sue_str}', '{event_2}', '{a23_str}', '{minute_480}', '{hour8am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, agg_br00003_tablename) == 3
        cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
        cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
        assert not sheet_exists(cochlea_file_path, cochlea_agg_str())

        # WHEN
        etl_cochlea_agg_db_to_cochlea_agg_df(db_conn, cochlea_dir)

        # THEN
        assert sheet_exists(cochlea_file_path, cochlea_agg_str())
        agg_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_agg_str())
        row0 = [sue_str, event_1, a23_str, minute_360, hour6am]
        row1 = [sue_str, event_1, a23_str, minute_420, hour7am]
        row2 = [sue_str, event_2, a23_str, minute_480, hour8am]
        ex_agg_df = DataFrame([row0, row1, row2], columns=agg_br00003_columns)
        print(f"{agg_df.columns=}")
        assert len(ex_agg_df.columns) == len(agg_df.columns)
        assert list(ex_agg_df.columns) == list(agg_df.columns)
        assert len(agg_df) > 0
        assert len(ex_agg_df) == len(agg_df)
        assert len(agg_df) == 3
        assert ex_agg_df.to_csv() == agg_df.to_csv()
