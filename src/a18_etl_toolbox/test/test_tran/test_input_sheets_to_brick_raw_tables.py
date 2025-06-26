from pandas import DataFrame
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a00_data_toolbox.file_toolbox import create_path
from src.a09_pack_logic.test._util.a09_str import (
    belief_label_str,
    event_int_str,
    face_name_str,
)
from src.a15_belief_logic.test._util.a15_str import (
    cumulative_minute_str,
    hour_label_str,
)
from src.a17_idea_logic.idea_db_tool import upsert_sheet
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.test._util.a18_str import brick_raw_str, error_message_str
from src.a18_etl_toolbox.transformers import etl_input_dfs_to_brick_raw_tables


def test_etl_input_dfs_to_brick_raw_tables_PopulatesTables_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event3 = 3
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    input_dir = create_path(get_module_temp_dir(), "input")
    input_file_path = create_path(input_dir, ex_filename)
    br3_columns = [
        event_int_str(),
        face_name_str(),
        cumulative_minute_str(),
        belief_label_str(),
        hour_label_str(),
    ]
    a23_str = "accord23"
    row0 = [event1, sue_str, minute_360, a23_str, hour6am]
    row1 = [event1, sue_str, minute_420, a23_str, hour7am]
    row2 = [event2, sue_str, minute_420, a23_str, hour7am]
    row3 = [event3, sue_str, "num55", a23_str, hour7am]
    row4 = ["event3", sue_str, "num55", a23_str, hour7am]

    df1 = DataFrame([row0, row1, row2, row3, row4], columns=br3_columns)
    br00003_ex1_str = "example1_br00003"
    upsert_sheet(input_file_path, br00003_ex1_str, df1)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        br00003_tablename = f"br00003_{brick_raw_str()}"
        assert not db_table_exists(cursor, br00003_tablename)

        # WHEN
        etl_input_dfs_to_brick_raw_tables(db_conn, input_dir)

        # THEN
        assert db_table_exists(cursor, br00003_tablename)
        br00003_table_cols = get_table_columns(cursor, br00003_tablename)
        file_dir_str = "file_dir"
        filename_str = "filename"
        sheet_name_str = "sheet_name"
        assert file_dir_str == br00003_table_cols[0]
        assert filename_str == br00003_table_cols[1]
        assert sheet_name_str == br00003_table_cols[2]
        assert error_message_str() == br00003_table_cols[-1]
        assert get_row_count(cursor, br00003_tablename) == 5
        select_agg_sqlstr = f"""
SELECT * 
FROM {br00003_tablename} 
ORDER BY sheet_name, {event_int_str()}, {cumulative_minute_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 5
        file = ex_filename
        e1 = event1
        e2 = event2
        e3 = event3
        s_dir = create_path(input_dir, ".")
        m_360 = minute_360
        m_420 = minute_420
        br3_ex1_str = br00003_ex1_str
        err4 = f"Conversion errors: {cumulative_minute_str()}: num55"
        err0 = f"Conversion errors: {event_int_str()}: event3, {cumulative_minute_str()}: num55"
        row0 = (s_dir, file, br3_ex1_str, None, sue_str, a23_str, None, hour7am, err0)
        row1 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_360, hour6am, None)
        row2 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_420, hour7am, None)
        row3 = (s_dir, file, br3_ex1_str, e2, sue_str, a23_str, m_420, hour7am, None)
        row4 = (s_dir, file, br3_ex1_str, e3, sue_str, a23_str, None, hour7am, err4)
        print(f"{rows[2]=}")
        print(f"   {row2=}")
        assert rows[0] == row0
        assert rows[1] == row1
        assert rows[2] == row2
        assert rows[3] == row3
        assert rows[4] == row4


def test_etl_input_dfs_to_brick_raw_tables_PopulatesTables_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    input_dir = create_path(get_module_temp_dir(), "input")
    input_file_path = create_path(input_dir, ex_filename)
    idea_columns = [
        event_int_str(),
        face_name_str(),
        cumulative_minute_str(),
        belief_label_str(),
        hour_label_str(),
    ]
    a23_str = "accord23"
    row1 = [event1, sue_str, minute_360, a23_str, hour6am]
    row2 = [event1, sue_str, minute_420, a23_str, hour7am]
    row3 = [event2, sue_str, minute_420, a23_str, hour7am]
    incomplete_idea_columns = [
        event_int_str(),
        face_name_str(),
        cumulative_minute_str(),
        belief_label_str(),
    ]
    incom_row1 = [event1, sue_str, minute_360, a23_str]
    incom_row2 = [event1, sue_str, minute_420, a23_str]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
    df3 = DataFrame([row2, row1, row3], columns=idea_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(input_file_path, br00003_ex1_str, df1)
    upsert_sheet(input_file_path, br00003_ex2_str, df2)
    upsert_sheet(input_file_path, br00003_ex3_str, df3)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        br00003_tablename = f"br00003_{brick_raw_str()}"
        assert not db_table_exists(cursor, br00003_tablename)

        # WHEN
        etl_input_dfs_to_brick_raw_tables(db_conn, input_dir)

        # THEN
        assert db_table_exists(cursor, br00003_tablename)
        assert get_row_count(cursor, br00003_tablename) == 5
        br00003_table_cols = get_table_columns(cursor, br00003_tablename)
        file_dir_str = "file_dir"
        filename_str = "filename"
        sheet_name_str = "sheet_name"
        assert file_dir_str == br00003_table_cols[0]
        assert filename_str == br00003_table_cols[1]
        assert sheet_name_str == br00003_table_cols[2]
        assert error_message_str() == br00003_table_cols[-1]
        select_agg_sqlstr = f"""
SELECT * 
FROM {br00003_tablename} 
ORDER BY sheet_name, {event_int_str()}, {cumulative_minute_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 5
        file = ex_filename
        e1 = event1
        e2 = event2
        s_dir = create_path(input_dir, ".")
        m_360 = minute_360
        m_420 = minute_420
        br3_ex1_str = br00003_ex1_str
        br3_ex3_str = br00003_ex3_str
        row0 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_360, hour6am, None)
        row1 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_420, hour7am, None)
        row2 = (s_dir, file, br3_ex3_str, e1, sue_str, a23_str, m_360, hour6am, None)
        row3 = (s_dir, file, br3_ex3_str, e1, sue_str, a23_str, m_420, hour7am, None)
        row4 = (s_dir, file, br3_ex3_str, e2, sue_str, a23_str, m_420, hour7am, None)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0
        assert rows[1] == row1
        assert rows[2] == row2
        assert rows[3] == row3
        assert rows[4] == row4


# def test_etl_input_dfs_to_brick_raw_tables_PopulatesTables_Scenario2(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     event1 = 1
#     event2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "fizzbuzz.xlsx"
#     input_dir = create_path(get_module_temp_dir(), "input")
#     input_file_path = create_path(input_dir, ex_filename)
#     idea_columns = [
#         event_int_str(),
#         face_name_str(),
#         cumulative_minute_str(),
#         belief_label_str(),
#         hour_label_str(),
#     ]
#     a23_str = "accord23"
#     df_row0 = [event1, sue_str, minute_360, a23_str, hour6am]
#     df_row1 = [event1, sue_str, minute_420, a23_str, hour7am]
#     df_row2 = [event2, sue_str, minute_420, a23_str, hour7am]

#     df1 = DataFrame([df_row0, df_row1, df_row2], columns=idea_columns)
#     br00003_ex1_str = "example1_br00003"
#     upsert_sheet(input_file_path, br00003_ex1_str, df1)
#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         br00003_tablename = f"br00003_{brick_raw_str()}"
#         assert not db_table_exists(cursor, br00003_tablename)

#         # WHEN
#         etl_input_dfs_to_brick_raw_tables(db_conn, input_dir)

#         # THEN
#         assert db_table_exists(cursor, br00003_tablename)
#         assert get_row_count(cursor, br00003_tablename) == 5
#         br00003_table_cols = get_table_columns(cursor, br00003_tablename)
#         file_dir_str = "file_dir"
#         filename_str = "filename"
#         sheet_name_str = "sheet_name"
#         assert file_dir_str == br00003_table_cols[0]
#         assert filename_str == br00003_table_cols[1]
#         assert sheet_name_str == br00003_table_cols[2]
#         assert error_message_str() != br00003_table_cols[-1]
#         select_agg_sqlstr = f"""
# SELECT *
# FROM {br00003_tablename}
# ORDER BY sheet_name, {event_int_str()}, {cumulative_minute_str()};"""
#         cursor.execute(select_agg_sqlstr)

#         br3rows = cursor.fetchall()
#         assert len(br3rows) == 5
#         file = ex_filename
#         e1 = event1
#         e2 = event2
#         s_dir = create_path(input_dir, ".")
#         m_360 = minute_360
#         m_420 = minute_420
#         br3_ex1_str = br00003_ex1_str
#         br3row0 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_360, hour6am)
#         br3row1 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_420, hour7am)
#         br3row2 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_360, hour6am)
#         print(f"{rows[0]=}")
#         print(f"   {row0=}")
#         assert rows[0] == row0
#         assert rows[1] == row1
#         assert rows[2] == row2
#         assert rows[3] == row3
#         assert rows[4] == row4
