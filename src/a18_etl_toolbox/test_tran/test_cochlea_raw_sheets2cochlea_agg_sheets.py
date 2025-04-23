from src.a00_data_toolboxs.file_toolbox import create_path
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
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


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
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, minute_360, hour6am]
    row2 = [sue_str, event_1, accord23_str, minute_420, hour7am]
    row3 = [sue_str, event_1, accord23_str, minute_420, hour7am]
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
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, minute_360, hour6am]
    row2 = [sue_str, event_1, accord23_str, minute_420, hour7am]
    row3 = [sue_str, event_1, accord23_str, minute_420, hour8am]
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
