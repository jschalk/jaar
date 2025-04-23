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
    get_sheet_names,
    upsert_sheet,
    cochlea_raw_str,
    cochlea_agg_str,
)
from src.a18_etl_toolbox.transformers import (
    etl_sound_df_to_cochlea_raw_df,
    etl_cochlea_raw_df_to_cochlea_agg_df,
    etl_cochlea_agg_df_to_cochlea_agg_events_df,
    etl_cochlea_raw_db_to_cochlea_agg_events_db,
    etl_cochlea_agg_events_db_to_event_dict,
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect


def test_etl_cochlea_agg_df_to_cochlea_agg_events_df_CreatesSheets_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    sound_dir = create_path(get_test_etl_dir(), "sound")
    cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
    sound_file_path = create_path(sound_dir, ex_filename)
    cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        hour_tag_str(),
        cumlative_minute_str(),
    ]
    a23_str = "accord23"
    row1 = [sue_str, event1, a23_str, hour6am, minute_360]
    row2 = [sue_str, event1, a23_str, hour7am, minute_420]
    row3 = [yao_str, event3, a23_str, hour7am, minute_420]
    row4 = [yao_str, event9, a23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4], columns=idea_columns)
    upsert_sheet(sound_file_path, "example1_br00003", df1)
    etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)
    etl_cochlea_raw_df_to_cochlea_agg_df(cochlea_dir)

    # WHEN
    etl_cochlea_agg_df_to_cochlea_agg_events_df(cochlea_dir)

    # THEN
    gen_otx_events_df = pandas_read_excel(
        cochlea_file_path, sheet_name="cochlea_events"
    )
    print(f"{gen_otx_events_df.columns=}")
    events_otx_columns = [face_name_str(), event_int_str(), "error_message"]
    sue_r = [sue_str, event1, ""]
    yao3_r = [yao_str, event3, ""]
    yao9_r = [yao_str, event9, ""]
    ex_otx_events_df = DataFrame([sue_r, yao3_r, yao9_r], columns=events_otx_columns)
    assert len(gen_otx_events_df.columns) == len(ex_otx_events_df.columns)
    assert list(gen_otx_events_df.columns) == list(ex_otx_events_df.columns)
    assert len(gen_otx_events_df) > 0
    assert len(gen_otx_events_df) == 3
    assert len(gen_otx_events_df) == len(ex_otx_events_df)
    assert gen_otx_events_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)
    assert get_sheet_names(cochlea_file_path) == [
        cochlea_raw_str(),
        cochlea_agg_str(),
        "cochlea_events",
    ]


def test_etl_cochlea_agg_df_to_cochlea_agg_events_df_CreatesSheets_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
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
    ex_filename = "fizzbuzz.xlsx"
    sound_dir = create_path(get_test_etl_dir(), "sound")
    cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
    sound_file_path = create_path(sound_dir, ex_filename)
    cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        hour_tag_str(),
        cumlative_minute_str(),
    ]
    a23_str = "accord23"
    row1 = [sue_str, event1, a23_str, hour6am, minute_360]
    row2 = [sue_str, event1, a23_str, hour7am, minute_420]
    row3 = [yao_str, event1, a23_str, hour7am, minute_420]
    row4 = [yao_str, event9, a23_str, hour7am, minute_420]
    row5 = [bob_str, event3, a23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4, row5], columns=idea_columns)
    upsert_sheet(sound_file_path, "example1_br00003", df1)
    etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)
    etl_cochlea_raw_df_to_cochlea_agg_df(cochlea_dir)

    # WHEN
    etl_cochlea_agg_df_to_cochlea_agg_events_df(cochlea_dir)

    # THEN
    gen_otx_events_df = pandas_read_excel(
        cochlea_file_path, sheet_name="cochlea_events"
    )
    print(f"{gen_otx_events_df.columns=}")
    events_otx_columns = [face_name_str(), event_int_str(), "error_message"]
    bob_row = [bob_str, event3, ""]
    sue_row = [sue_str, event1, "invalid because of conflicting event_int"]
    yao1_row = [yao_str, event1, "invalid because of conflicting event_int"]
    yao9_row = [yao_str, event9, ""]
    events_rows = [bob_row, sue_row, yao1_row, yao9_row]
    ex_otx_events_df = DataFrame(events_rows, columns=events_otx_columns)
    assert len(gen_otx_events_df.columns) == len(ex_otx_events_df.columns)
    assert list(gen_otx_events_df.columns) == list(ex_otx_events_df.columns)
    assert len(gen_otx_events_df) > 0
    assert len(gen_otx_events_df) == 4
    assert len(gen_otx_events_df) == len(ex_otx_events_df)
    print(f"{gen_otx_events_df.to_csv(index=False)=}")
    print(f" {ex_otx_events_df.to_csv(index=False)=}")
    assert gen_otx_events_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)


def test_etl_cochlea_agg_db_to_cochlea_agg_events_db_PopulatesTables_Scenario0(
    env_dir_setup_cleanup,
):
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
  ('{sue_str}', '{event1}', '{a23_str}', '{minute_360}', '{hour6am}')
, ('{sue_str}', '{event1}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{yao_str}', '{event3}', '{a23_str}', '{minute_420}', '{hour7am}')
, ('{yao_str}', '{event9}', '{a23_str}', '{minute_420}', '{hour7am}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        cochlea_events_tablename = "cochlea_agg_events"
        assert get_row_count(cursor, agg_br00003_tablename) == 4
        assert not db_table_exists(cursor, cochlea_events_tablename)

        # WHEN
        etl_cochlea_raw_db_to_cochlea_agg_events_db(cursor)

        # THEN
        assert db_table_exists(cursor, cochlea_events_tablename)
        cochlea_events_table_cols = get_table_columns(cursor, cochlea_events_tablename)
        assert face_name_str() in set(cochlea_events_table_cols)
        assert event_int_str() in set(cochlea_events_table_cols)
        assert "error_message" in set(cochlea_events_table_cols)
        assert get_row_count(cursor, cochlea_events_tablename) == 3
        select_agg_sqlstr = f"""
SELECT * 
FROM {cochlea_events_tablename} 
ORDER BY {face_name_str()}, {event_int_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 3
        sue_r = (sue_str, event1, None)
        yao3_r = (yao_str, event3, None)
        yao9_r = (yao_str, event9, None)
        print(f"{rows[0]=}")
        assert rows[0] == sue_r
        assert rows[1] == yao3_r
        assert rows[2] == yao9_r


def test_etl_cochlea_agg_db_to_cochlea_agg_events_db_PopulatesTables_Scenario1(
    env_dir_setup_cleanup,
):
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
  ('{sue_str}', '{event1}', "{a23_str}", '{hour6am}', '{minute_360}')
, ('{sue_str}', '{event1}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{yao_str}', '{event1}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{yao_str}', '{event9}', "{a23_str}", '{hour7am}', '{minute_420}')
, ('{bob_str}', '{event3}', "{a23_str}", '{hour7am}', '{minute_420}')
;
"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
        cochlea_events_tablename = "cochlea_agg_events"
        assert get_row_count(cursor, agg_br00003_tablename) == 5
        assert not db_table_exists(cursor, cochlea_events_tablename)

        # WHEN
        etl_cochlea_raw_db_to_cochlea_agg_events_db(cursor)

        # THEN
        assert db_table_exists(cursor, cochlea_events_tablename)
        assert get_row_count(cursor, cochlea_events_tablename) == 4
        select_agg_sqlstr = f"""
SELECT * 
FROM {cochlea_events_tablename} 
ORDER BY {face_name_str()}, {event_int_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 4
        bob_row = (bob_str, event3, None)
        sue_row = (sue_str, event1, "invalid because of conflicting event_int")
        yao1_row = (yao_str, event1, "invalid because of conflicting event_int")
        yao9_row = (yao_str, event9, None)

        assert rows[0] == bob_row
        assert rows[1] == sue_row
        assert rows[2] == yao1_row
        assert rows[3] == yao9_row


def test_etl_cochlea_agg_events_db_to_event_dict_ReturnsObj_Scenario0(
    env_dir_setup_cleanup,
):
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
        agg_events_tablename = "cochlea_agg_events"
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
        assert get_row_count(cursor, agg_events_tablename) == 6

        # WHEN
        events_dict = etl_cochlea_agg_events_db_to_event_dict(cursor)

        # THEN
        assert events_dict == {event3: bob_str, event9: yao_str}
