from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
    create_table_from_columns,
)
from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic._utils.str_a17 import idea_number_str, yell_agg_str
from src.a17_idea_logic.idea_db_tool import create_idea_sorted_table
from src.a18_etl_toolbox.transformers import (
    etl_yell_raw_db_to_yell_agg_events_db,
    etl_yell_agg_events_db_to_yell_valid_events_db,
    etl_yell_agg_events_db_to_event_dict,
)
from sqlite3 import connect as sqlite3_connect


def test_etl_yell_agg_db_to_yell_agg_events_db_PopulatesTables_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
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
, ('{sue_str}', '{event1}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{yao_str}', '{event3}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{yao_str}', '{event9}', '{a23_str}', '{minute_420}', '{hour7am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        yell_events_tablename = "yell_agg_events"
        assert get_row_count(cursor, agg_br00003_tablename) == 4
        assert not db_table_exists(cursor, yell_events_tablename)

        # WHEN
        etl_yell_raw_db_to_yell_agg_events_db(cursor)

        # THEN
        assert db_table_exists(cursor, yell_events_tablename)
        yell_events_table_cols = set(get_table_columns(cursor, yell_events_tablename))
        assert len(yell_events_table_cols) == 4
        assert idea_number_str() in yell_events_table_cols
        assert face_name_str() in yell_events_table_cols
        assert event_int_str() in yell_events_table_cols
        assert "error_message" in yell_events_table_cols
        assert get_row_count(cursor, yell_events_tablename) == 3
        select_agg_sqlstr = f"""
SELECT * 
FROM {yell_events_tablename} 
ORDER BY {face_name_str()}, {event_int_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 3
        sue_r = ("br00003", sue_str, event1, None)
        yao3_r = ("br00003", yao_str, event3, None)
        yao9_r = ("br00003", yao_str, event9, None)
        print(f"{rows[0]=}")
        assert rows[0] == sue_r
        assert rows[1] == yao3_r
        assert rows[2] == yao9_r


def test_etl_yell_agg_db_to_yell_agg_events_db_PopulatesTables_Scenario1():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
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
  ('{sue_str}', '{event1}', "{a23_str}", '{hour6am}', '{minute_360}')
, ('{sue_str}', '{event1}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{yao_str}', '{event1}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{yao_str}', '{event9}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{bob_str}', '{event3}', "{a23_str}", '{hour7am}', '{minute_420}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        yell_events_tablename = "yell_agg_events"
        assert get_row_count(cursor, agg_br00003_tablename) == 5
        assert not db_table_exists(cursor, yell_events_tablename)

        # WHEN
        etl_yell_raw_db_to_yell_agg_events_db(cursor)

        # THEN
        assert db_table_exists(cursor, yell_events_tablename)
        assert get_row_count(cursor, yell_events_tablename) == 4
        select_agg_sqlstr = f"""
SELECT * 
FROM {yell_events_tablename} 
ORDER BY {face_name_str()}, {event_int_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 4
        invalid_str = "invalid because of conflicting event_int"
        bob_row = ("br00003", bob_str, event3, None)
        sue_row = ("br00003", sue_str, event1, invalid_str)
        yao1_row = ("br00003", yao_str, event1, invalid_str)
        yao9_row = ("br00003", yao_str, event9, None)

        assert rows[0] == bob_row
        assert rows[1] == sue_row
        assert rows[2] == yao1_row
        assert rows[3] == yao9_row


def test_etl_yell_agg_events_db_to_yell_valid_events_db_PopulatesTables_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        agg_events_tablename = "yell_agg_events"
        agg_events_columns = ["idea_number", "face_name", "event_int", "error_message"]
        create_idea_sorted_table(cursor, agg_events_tablename, agg_events_columns)
        insert_into_clause = f"""INSERT INTO {agg_events_tablename} (
  {idea_number_str()}
, {face_name_str()}
, {event_int_str()}
, error_message
)"""
        invalid_str = "invalid because of conflicting event_int"
        values_clause = f"""
VALUES
  ('br00003', '{bob_str}', '{event3}', NULL)
, ('br00003', '{sue_str}', '{event1}', '{invalid_str}')
, ('br00003', '{yao_str}', '{event1}', '{invalid_str}')
, ('br00003', '{yao_str}', '{event9}', NULL)  
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, agg_events_tablename) == 4
        valid_events_tablename = "yell_valid_events"
        assert not db_table_exists(cursor, valid_events_tablename)

        # WHEN
        etl_yell_agg_events_db_to_yell_valid_events_db(cursor)

        # THEN
        assert db_table_exists(cursor, valid_events_tablename)
        assert get_row_count(cursor, valid_events_tablename) == 2
        select_agg_sqlstr = f"""
SELECT * 
FROM {valid_events_tablename} 
ORDER BY {face_name_str()}, {event_int_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 2
        bob_row = (bob_str, event3)
        yao9_row = (yao_str, event9)

        assert rows[0] == bob_row
        assert rows[1] == yao9_row


def test_etl_yell_agg_events_db_to_event_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    agg_columns = [face_name_str(), event_int_str(), "error_message"]
    agg_types = {
        face_name_str(): "TEXT",
        event_int_str(): "TEXT",
        "error_message": "TEXT",
    }
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        agg_events_tablename = "yell_agg_events"
        create_table_from_columns(cursor, agg_events_tablename, agg_columns, agg_types)
        insert_into_clause = f"""
INSERT INTO {agg_events_tablename} ({face_name_str()}, {event_int_str()}, error_message)
VALUES     
  ('{bob_str}', '{event3}', NULL)
, ('{sue_str}', '{event1}', 'invalid because of conflicting event_int')
, ('{yao_str}', '{event1}', 'invalid because of conflicting event_int')
, ('{yao_str}', '{event9}', NULL)
, ('{yao_str}', '{event9}', NULL)
, ('{yao_str}', '{event9}', NULL)
;
"""
        cursor.execute(insert_into_clause)
        etl_yell_agg_events_db_to_yell_valid_events_db(cursor)
        assert get_row_count(cursor, agg_events_tablename) == 6

        # WHEN
        events_dict = etl_yell_agg_events_db_to_event_dict(cursor)

        # THEN
        assert events_dict == {event3: bob_str, event9: yao_str}
