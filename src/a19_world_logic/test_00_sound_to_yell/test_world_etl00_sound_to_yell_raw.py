from src.a00_data_toolbox.file_toolbox import create_path
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a02_finance_logic._utils.str_helpers import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet, yell_raw_str
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_utils import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_sound_df_to_yell_raw_db_CreatesYellFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    sue_str = "Sue"
    event_1 = 1
    event_2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    sound_file_path = create_path(fizz_world._sound_dir, ex_filename)
    yell_file_path = create_path(fizz_world._yell_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
        hour_tag_str(),
    ]
    a23_str = "accord23"
    row1 = [sue_str, event_1, minute_360, a23_str, hour6am]
    row2 = [sue_str, event_1, minute_420, a23_str, hour7am]
    row3 = [sue_str, event_2, minute_420, a23_str, hour7am]
    incomplete_idea_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
    ]
    incom_row1 = [sue_str, event_1, minute_360, a23_str]
    incom_row2 = [sue_str, event_1, minute_420, a23_str]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
    df3 = DataFrame([row2, row1, row3], columns=idea_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(sound_file_path, br00003_ex1_str, df1)
    upsert_sheet(sound_file_path, br00003_ex2_str, df2)
    upsert_sheet(sound_file_path, br00003_ex3_str, df3)
    assert os_path_exists(yell_file_path) is False

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        br00003_tablename = f"{yell_raw_str()}_br00003"
        assert not db_table_exists(cursor, br00003_tablename)

        # WHEN
        fizz_world.sound_df_to_yell_raw_db(db_conn)

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
        select_agg_sqlstr = f"""
SELECT * 
FROM {br00003_tablename} 
ORDER BY sheet_name, {event_int_str()}, {cumlative_minute_str()};"""
        cursor.execute(select_agg_sqlstr)

        rows = cursor.fetchall()
        assert len(rows) == 5
        file = ex_filename
        e1 = event_1
        e2 = event_2
        s_dir = create_path(fizz_world._sound_dir, ".")
        m_360 = minute_360
        m_420 = minute_420
        br3_ex1 = br00003_ex1_str
        br3_ex3 = br00003_ex3_str
        row0 = (s_dir, file, br3_ex1, sue_str, e1, a23_str, m_360, hour6am)
        row1 = (s_dir, file, br3_ex1, sue_str, e1, a23_str, m_420, hour7am)
        row2 = (s_dir, file, br3_ex3, sue_str, e1, a23_str, m_360, hour6am)
        row3 = (s_dir, file, br3_ex3, sue_str, e1, a23_str, m_420, hour7am)
        row4 = (s_dir, file, br3_ex3, sue_str, e2, a23_str, m_420, hour7am)
        print(f"{rows[0]=}")
        print(f"   {row0=}")
        assert rows[0] == row0
        assert rows[1] == row1
        assert rows[2] == row2
        assert rows[3] == row3
        assert rows[4] == row4
