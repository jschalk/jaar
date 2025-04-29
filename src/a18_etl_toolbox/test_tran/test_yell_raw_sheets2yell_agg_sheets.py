from src.a00_data_toolbox.file_toolbox import create_path
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
    create_table_from_columns,
)
from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import (
    yell_raw_str,
    yell_agg_str,
    yell_valid_str,
    sheet_exists,
)
from src.a18_etl_toolbox.transformers import (
    etl_yell_raw_db_to_yell_agg_db,
    etl_yell_agg_db_to_yell_valid_db,
    etl_yell_agg_db_to_yell_agg_df,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect


def test_etl_yell_raw_db_to_yell_agg_db_PopulatesAggTable_Scenario0_GroupByWorks():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    raw_br00003_tablename = f"{yell_raw_str()}_br00003"
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
        agg_br00003_tablename = f"{yell_agg_str()}_br00003"
        assert get_row_count(cursor, raw_br00003_tablename) == 3
        assert not db_table_exists(cursor, agg_br00003_tablename)

        # WHEN
        etl_yell_raw_db_to_yell_agg_db(cursor)

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


def test_etl_yell_raw_db_to_yell_agg_db_PopulatesAggTable_Scenario1_GroupByOnlyNonConflictingRecords():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"

    raw_br00003_tablename = f"{yell_raw_str()}_br00003"
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
        agg_br00003_tablename = f"{yell_agg_str()}_br00003"
        assert get_row_count(cursor, raw_br00003_tablename) == 3
        assert not db_table_exists(cursor, agg_br00003_tablename)

        # WHEN
        etl_yell_raw_db_to_yell_agg_db(cursor)

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


def test_etl_yell_agg_db_to_yell_agg_df_PopulatesAggTable_Scenario0_GroupByWorks(
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
    agg_br00003_tablename = f"{yell_agg_str()}_br00003"
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
        yell_dir = create_path(get_module_temp_dir(), "yell")
        yell_file_path = create_path(yell_dir, "br00003.xlsx")
        assert not sheet_exists(yell_file_path, yell_agg_str())

        # WHEN
        etl_yell_agg_db_to_yell_agg_df(db_conn, yell_dir)

        # THEN
        assert sheet_exists(yell_file_path, yell_agg_str())
        agg_df = pandas_read_excel(yell_file_path, sheet_name=yell_agg_str())
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


def test_etl_yell_agg_db_to_yell_valid_db_PopulatesValidTable_Scenario0_Only_valid_events():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    event1 = 1
    event3 = 3
    event6 = 6
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"

    agg_br00003_tablename = f"{yell_agg_str()}_br00003"
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
  ('{sue_str}', '{event1}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{sue_str}', '{event3}', '{a23_str}', '{minute_420}', '{hour8am}')
, ('{sue_str}', '{event6}', '{a23_str}', '{minute_420}', '{hour8am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, agg_br00003_tablename) == 3

        valid_events_columns = [face_name_str(), event_int_str()]
        valid_events_types = {face_name_str(): "TEXT", event_int_str(): "TEXT"}
        valid_events_tablename = "yell_valid_events"
        create_table_from_columns(
            cursor, valid_events_tablename, valid_events_columns, valid_events_types
        )
        insert_into_valid_events = f"""
INSERT INTO {valid_events_tablename} ({face_name_str()}, {event_int_str()})
VALUES     
  ('{sue_str}', '{event1}')
, ('{sue_str}', '{event6}')
;
"""
        cursor.execute(insert_into_valid_events)
        assert get_row_count(cursor, valid_events_tablename) == 2

        valid_br00003_tablename = f"{yell_valid_str()}_br00003"
        assert not db_table_exists(cursor, valid_br00003_tablename)

        # WHEN
        etl_yell_agg_db_to_yell_valid_db(cursor)

        # THEN
        assert db_table_exists(cursor, valid_br00003_tablename)
        assert get_table_columns(cursor, valid_br00003_tablename) == agg_br00003_columns
        assert get_row_count(cursor, valid_br00003_tablename) == 2
        select_agg_sqlstr = f"""SELECT * FROM {valid_br00003_tablename};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 2
        row0 = (sue_str, str(event1), a23_str, str(minute_360), hour6am)
        row1 = (sue_str, str(event6), a23_str, str(minute_420), hour8am)
        assert rows[0] == row0
        assert rows[1] == row1
