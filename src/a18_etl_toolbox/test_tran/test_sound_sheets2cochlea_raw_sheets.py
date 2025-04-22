from src.a00_data_toolboxs.file_toolbox import create_path
from src.a00_data_toolboxs.db_toolbox import db_table_exists, get_row_count
from src.a02_finance_toolboxs.deal import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import (
    get_sheet_names,
    upsert_sheet,
    cochlea_raw_str,
)
from src.a18_etl_toolbox.transformers import (
    etl_sound_df_to_cochlea_raw_df,
    etl_sound_df_to_cochlea_raw_db,
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_etl_sound_df_to_cochlea_raw_df_CreatesCochleaFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    event_2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    sound_dir = create_path(get_test_etl_dir(), "sound")
    cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
    sound_file_path = create_path(sound_dir, ex_filename)
    idea_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
        hour_tag_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, minute_360, accord23_str, hour6am]
    row2 = [sue_str, event_1, minute_420, accord23_str, hour7am]
    row3 = [sue_str, event_2, minute_420, accord23_str, hour7am]
    incomplete_idea_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
    ]
    incom_row1 = [sue_str, event_1, minute_360, accord23_str]
    incom_row2 = [sue_str, event_1, minute_420, accord23_str]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
    df3 = DataFrame([row2, row1, row3], columns=idea_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(sound_file_path, br00003_ex1_str, df1)
    upsert_sheet(sound_file_path, br00003_ex2_str, df2)
    upsert_sheet(sound_file_path, br00003_ex3_str, df3)
    cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
    assert os_path_exists(cochlea_file_path) is False

    # WHEN
    etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)

    # THEN
    print(f"{cochlea_file_path=}")
    assert os_path_exists(cochlea_file_path)
    x_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_raw_str())
    assert set(idea_columns).issubset(set(x_df.columns))
    file_dir_str = "file_dir"
    filename_str = "filename"
    sheet_name_str = "sheet_name"
    assert file_dir_str in set(x_df.columns)
    assert filename_str in set(x_df.columns)
    assert sheet_name_str in set(x_df.columns)
    assert len(x_df) == 5
    assert get_sheet_names(cochlea_file_path) == [cochlea_raw_str()]


# def test_etl_sound_df_to_cochlea_raw_db_CreatesCochleaFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     sue_str = "Sue"
#     event_1 = 1
#     event_2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "fizzbuzz.xlsx"
#     sound_dir = create_path(get_test_etl_dir(), "sound")
#     cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
#     sound_file_path = create_path(sound_dir, ex_filename)
#     idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         cumlative_minute_str(),
#         fisc_tag_str(),
#         hour_tag_str(),
#     ]
#     a23_str = "accord23"
#     row1 = [sue_str, event_1, minute_360, a23_str, hour6am]
#     row2 = [sue_str, event_1, minute_420, a23_str, hour7am]
#     row3 = [sue_str, event_2, minute_420, a23_str, hour7am]
#     incomplete_idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         cumlative_minute_str(),
#         fisc_tag_str(),
#     ]
#     incom_row1 = [sue_str, event_1, minute_360, a23_str]
#     incom_row2 = [sue_str, event_1, minute_420, a23_str]

#     df1 = DataFrame([row1, row2], columns=idea_columns)
#     df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
#     df3 = DataFrame([row2, row1, row3], columns=idea_columns)
#     br00003_ex1_str = "example1_br00003"
#     br00003_ex2_str = "example2_br00003"
#     br00003_ex3_str = "example3_br00003"
#     upsert_sheet(sound_file_path, br00003_ex1_str, df1)
#     upsert_sheet(sound_file_path, br00003_ex2_str, df2)
#     upsert_sheet(sound_file_path, br00003_ex3_str, df3)
#     cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         br00003_tablename = f"{cochlea_raw_str()}_br00003"
#         assert not db_table_exists(cursor, br00003_tablename)

#         # WHEN
#         etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)

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
#         select_agg_sqlstr = f"SELECT * FROM {br00003_tablename};"
#         cursor.execute(select_agg_sqlstr)

#         rows = cursor.fetchall()
#         file = ex_filename
#         ex_agg_row0 = (sound_dir, file, br00003_ex1_str, a23_str, minute_360, hour6am)
#         ex_agg_row1 = (sound_dir, file, br00003_ex2_str, a23_str, minute_420, hour7am)
#         ex_agg_row2 = (sound_dir, file, br00003_ex3_str, a23_str, minute_420, hour7am)
#         assert rows == [ex_agg_row0, ex_agg_row1, ex_agg_row2]
