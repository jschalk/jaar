from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a15_belief_logic.test._util.a15_str import (
    belief_label_str,
    cumulative_minute_str,
    hour_label_str,
)
from src.a17_idea_logic.idea_db_tool import create_idea_sorted_table
from src.a18_etl_toolbox.test._util.a18_str import (
    brick_agg_str,
    brick_raw_str,
    error_message_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_sound_and_voice_tables
from src.a18_etl_toolbox.transformers import (
    etl_brick_raw_tables_to_brick_agg_tables,
    get_max_brick_agg_event_int,
)


def test_etl_brick_raw_tables_to_brick_agg_tables_PopulatesAggTable_Scenario0_GroupByWorks():
    # ESTABLISH
    a23_str = "amy23"
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
        belief_label_str(),
        cumulative_minute_str(),
        hour_label_str(),
        error_message_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, raw_br00003_tablename, raw_br00003_columns)
        insert_into_clause = f"""INSERT INTO {raw_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {cumulative_minute_str()}
, {hour_label_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}', NULL)
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}', NULL)
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}', NULL)
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
ORDER BY {event_int_str()}, {cumulative_minute_str()};"""
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
    a23_str = "amy23"
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
        belief_label_str(),
        cumulative_minute_str(),
        hour_label_str(),
        error_message_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, raw_br00003_tablename, raw_br00003_columns)
        insert_into_clause = f"""INSERT INTO {raw_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {cumulative_minute_str()}
, {hour_label_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}', NULL)
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}', NULL)
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour8am}', NULL)
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


def test_etl_brick_raw_tables_to_brick_agg_tables_PopulatesAggTable_Scenario2_GroupByExcludesRowsWith_error_message():
    # ESTABLISH
    a23_str = "amy23"
    sue_str = "Sue"
    event1 = 1
    minute_360 = 360
    minute_420 = 420
    minute_480 = 480
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"
    raw_br00003_tablename = f"br00003_{brick_raw_str()}"
    raw_br00003_columns = [
        event_int_str(),
        face_name_str(),
        belief_label_str(),
        cumulative_minute_str(),
        hour_label_str(),
        error_message_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, raw_br00003_tablename, raw_br00003_columns)
        insert_into_clause = f"""INSERT INTO {raw_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {cumulative_minute_str()}
, {hour_label_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}', 'some_error')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}', NULL)
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}', 'some_error')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_480}', '{hour8am}', NULL)
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        agg_br00003_tablename = f"br00003_{brick_agg_str()}"
        assert get_row_count(cursor, raw_br00003_tablename) == 4
        assert not db_table_exists(cursor, agg_br00003_tablename)

        # WHEN
        etl_brick_raw_tables_to_brick_agg_tables(cursor)

        # THEN
        select_agg_sqlstr = f"""
SELECT * 
FROM {agg_br00003_tablename} 
ORDER BY {event_int_str()}, {cumulative_minute_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 2
        row0 = (event1, sue_str, a23_str, minute_420, hour7am)
        row1 = (event1, sue_str, a23_str, minute_480, hour8am)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0
        assert rows[1] == row1


def test_get_max_brick_events_event_int_ReturnsObj_Scenario0_NoTables():
    # ESTABLISH
    agg_br00003_tablename = f"br00003_{brick_agg_str()}"
    agg_br00003_columns = [
        event_int_str(),
        face_name_str(),
        belief_label_str(),
        cumulative_minute_str(),
        hour_label_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)

        # WHEN
        assert get_max_brick_agg_event_int(cursor) == 1


def test_get_max_brick_events_event_int_ReturnsObj_Scenario1_OneTable():
    # ESTABLISH
    a23_str = "amy23"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    agg_br00003_tablename = f"br00003_{brick_agg_str()}"
    agg_br00003_columns = [
        event_int_str(),
        face_name_str(),
        belief_label_str(),
        cumulative_minute_str(),
        hour_label_str(),
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {cumulative_minute_str()}
, {hour_label_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{event1}', '{sue_str}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{event3}', '{yao_str}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{event9}', '{yao_str}', '{a23_str}', '{minute_420}', '{hour7am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)

        # WHEN
        max_event_int = get_max_brick_agg_event_int(cursor)

        # THEN
        assert max_event_int
        assert max_event_int == event9


def test_get_max_brick_events_event_int_ReturnsObj_Scenario2_MultipleTable():
    # ESTABLISH
    event1 = 1
    event3 = 3
    event9 = 9
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        agg_br00003_tablename = f"br00003_{brick_agg_str()}"
        agg_br00003_columns = [event_int_str()]
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        agg_br00003_insert_sqlstr = f"""
INSERT INTO {agg_br00003_tablename} ({event_int_str()})
VALUES ('{event1}'), ('{event1}'), ('{event9}');"""
        cursor.execute(agg_br00003_insert_sqlstr)

        agg_br00044_tablename = f"br00044_{brick_agg_str()}"
        agg_br00044_columns = [event_int_str()]
        create_idea_sorted_table(cursor, agg_br00044_tablename, agg_br00044_columns)
        agg_br00044_insert_sqlstr = f"""
INSERT INTO {agg_br00044_tablename} ({event_int_str()})
VALUES ('{event3}');"""
        cursor.execute(agg_br00044_insert_sqlstr)

        # WHEN
        max_event_int = get_max_brick_agg_event_int(cursor)

        # THEN
        assert max_event_int
        assert max_event_int == event9
