from os.path import exists as os_path_exists
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic.test._util.a02_str import belief_label_str
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a15_belief_logic.test._util.a15_str import (
    cumulative_minute_str,
    hour_label_str,
)
from src.a17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet
from src.a17_idea_logic.test._util.a17_str import brick_raw_str
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import (
    etl_brick_raw_db_to_brick_raw_df,
    etl_mud_dfs_to_brick_raw_tables,
)


def test_etl_mud_dfs_to_brick_raw_tables_PopulatesBrickTables(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    mud_dir = create_path(get_module_temp_dir(), "mud")
    brick_dir = create_path(get_module_temp_dir(), "brick")
    mud_file_path = create_path(mud_dir, ex_filename)
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
    upsert_sheet(mud_file_path, br00003_ex1_str, df1)
    upsert_sheet(mud_file_path, br00003_ex2_str, df2)
    upsert_sheet(mud_file_path, br00003_ex3_str, df3)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        br00003_tablename = f"br00003_{brick_raw_str()}"
        assert not db_table_exists(cursor, br00003_tablename)

        # WHEN
        etl_mud_dfs_to_brick_raw_tables(db_conn, mud_dir)

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
        assert "error_message" != br00003_table_cols[-1]
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
        s_dir = create_path(mud_dir, ".")
        m_360 = minute_360
        m_420 = minute_420
        br3_ex1_str = br00003_ex1_str
        br3_ex3_str = br00003_ex3_str
        row0 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_360, hour6am)
        row1 = (s_dir, file, br3_ex1_str, e1, sue_str, a23_str, m_420, hour7am)
        row2 = (s_dir, file, br3_ex3_str, e1, sue_str, a23_str, m_360, hour6am)
        row3 = (s_dir, file, br3_ex3_str, e1, sue_str, a23_str, m_420, hour7am)
        row4 = (s_dir, file, br3_ex3_str, e2, sue_str, a23_str, m_420, hour7am)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0
        assert rows[1] == row1
        assert rows[2] == row2
        assert rows[3] == row3
        assert rows[4] == row4

        brick_file_path = create_path(brick_dir, "br00003.xlsx")
        assert os_path_exists(brick_file_path) is False

        # WHEN
        etl_brick_raw_db_to_brick_raw_df(db_conn, brick_dir)

        # THEN
        print(f"{brick_file_path=}")
        assert os_path_exists(brick_file_path)
        x_df = pandas_read_excel(brick_file_path, sheet_name=brick_raw_str())
        assert set(idea_columns).issubset(set(x_df.columns))
        assert file_dir_str in set(x_df.columns)
        assert filename_str in set(x_df.columns)
        assert sheet_name_str in set(x_df.columns)
        assert len(x_df) == 5
        assert get_sheet_names(brick_file_path) == [brick_raw_str()]
