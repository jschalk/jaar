from src.a00_data_toolboxs.file_toolbox import create_path
from src.a00_data_toolboxs.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
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
    etl_sound_df_to_cochlea_raw_db,
    etl_cochlea_raw_df_to_cochlea_agg_df,
    etl_cochlea_raw_db_to_cochlea_agg_db,
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect


def test_etl_cochlea_raw_df_to_cochlea_agg_df_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
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
        cumlative_minute_str(),
        hour_tag_str(),
    ]
    a23_str = "accord23"
    row1 = [sue_str, event_1, a23_str, minute_360, hour6am]
    row2 = [sue_str, event_1, a23_str, minute_420, hour7am]
    row3 = [sue_str, event_1, a23_str, minute_420, hour7am]
    df1 = DataFrame([row1, row2, row3], columns=idea_columns)
    upsert_sheet(sound_file_path, "example1_br00003", df1)
    etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)
    cochlea__raw_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_raw_str())
    assert len(cochlea__raw_df) == 3

    # WHEN
    etl_cochlea_raw_df_to_cochlea_agg_df(cochlea_dir)

    # THEN
    gen_otx_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_agg_str())
    ex_otx_df = DataFrame([row1, row2], columns=idea_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(cochlea_file_path) == [cochlea_raw_str(), cochlea_agg_str()]


def test_etl_cochlea_raw_df_to_cochlea_agg_df_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"
    ex_filename = "fizzbuzz.xlsx"
    sound_dir = create_path(get_test_etl_dir(), "sound")
    cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
    sound_file_path = create_path(sound_dir, ex_filename)
    cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        cumlative_minute_str(),
        hour_tag_str(),
    ]
    a23_str = "accord23"
    row1 = [sue_str, event_1, a23_str, minute_360, hour6am]
    row2 = [sue_str, event_1, a23_str, minute_420, hour7am]
    row3 = [sue_str, event_1, a23_str, minute_420, hour8am]
    df1 = DataFrame([row1, row2, row3], columns=idea_columns)
    upsert_sheet(sound_file_path, "example1_br00003", df1)
    etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)
    cochlea_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_raw_str())
    assert len(cochlea_df) == 3

    # WHEN
    etl_cochlea_raw_df_to_cochlea_agg_df(cochlea_dir)

    # THEN
    gen_otx_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_agg_str())
    ex_otx_df = DataFrame([row1], columns=idea_columns)
    # print(f"{gen_otx_df.columns=}")
    print(f"{gen_otx_df=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 1
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(cochlea_file_path) == [cochlea_raw_str(), cochlea_agg_str()]


def test_etl_cochlea_raw_db_to_cochlea_agg_db_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    sound_dir = create_path(get_test_etl_dir(), "sound")
    sound_file_path = create_path(sound_dir, ex_filename)
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        cumlative_minute_str(),
        hour_tag_str(),
    ]
    a23_str = "accord23"
    row1 = [sue_str, event_1, a23_str, minute_360, hour6am]
    row2 = [sue_str, event_1, a23_str, minute_420, hour7am]
    row3 = [sue_str, event_1, a23_str, minute_420, hour7am]
    df1 = DataFrame([row1, row2, row3], columns=idea_columns)
    upsert_sheet(sound_file_path, "example1_br00003", df1)
    with sqlite3_connect(":memory:") as db_conn:
        etl_sound_df_to_cochlea_raw_db(db_conn, sound_dir)
        raw_br00003_tablename = f"{cochlea_raw_str()}_br00003"
        agg_br00003_tablename = f"{cochlea_agg_str()}_br00003"
        cursor = db_conn.cursor()
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


# def test_etl_cochlea_raw_db_to_cochlea_agg_db_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     event_1 = 1
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     hour8am = "8am"
#     ex_filename = "fizzbuzz.xlsx"
#     sound_dir = create_path(get_test_etl_dir(), "sound")
#     cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
#     sound_file_path = create_path(sound_dir, ex_filename)
#     cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
#     idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_tag_str(),
#         cumlative_minute_str(),
#         hour_tag_str(),
#     ]
#     a23_str = "accord23"
#     row1 = [sue_str, event_1, a23_str, minute_360, hour6am]
#     row2 = [sue_str, event_1, a23_str, minute_420, hour7am]
#     row3 = [sue_str, event_1, a23_str, minute_420, hour8am]
#     df1 = DataFrame([row1, row2, row3], columns=idea_columns)
#     upsert_sheet(sound_file_path, "example1_br00003", df1)
#     etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)
#     cochlea_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_raw_str())
#     assert len(cochlea_df) == 3

#     # WHEN
#     etl_cochlea_raw_db_to_cochlea_agg_db(cochlea_dir)

#     # THEN
#     gen_otx_df = pandas_read_excel(cochlea_file_path, sheet_name=cochlea_agg_str())
#     ex_otx_df = DataFrame([row1], columns=idea_columns)
#     # print(f"{gen_otx_df.columns=}")
#     print(f"{gen_otx_df=}")
#     assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
#     assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
#     assert len(gen_otx_df) > 0
#     assert len(ex_otx_df) == len(gen_otx_df)
#     assert len(gen_otx_df) == 1
#     assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
#     assert get_sheet_names(cochlea_file_path) == [cochlea_raw_str(), cochlea_agg_str()]
