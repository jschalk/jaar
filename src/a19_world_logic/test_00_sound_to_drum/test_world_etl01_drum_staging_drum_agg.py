from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import (
    get_sheet_names,
    upsert_sheet,
    drum_staging_str,
    drum_agg_str,
    sheet_exists,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic.examples.world_env import (
    get_test_worlds_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_drum_staging_to_drum_agg_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    sound_file_path = create_path(fizz_world._sound_dir, ex_filename)
    drum_file_path = create_path(fizz_world._drum_dir, "br00003.xlsx")
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
    fizz_world.sound_to_drum_staging()
    drum__staging_df = pandas_read_excel(drum_file_path, sheet_name=drum_staging_str())
    assert len(drum__staging_df) == 3

    # WHEN
    fizz_world.drum_staging_to_drum_agg()

    # THEN
    gen_otx_df = pandas_read_excel(drum_file_path, sheet_name=drum_agg_str())
    ex_otx_df = DataFrame([row1, row2], columns=idea_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(drum_file_path) == [drum_staging_str(), drum_agg_str()]


def test_WorldUnit_drum_staging_to_drum_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    sue_str = "Sue"
    event3 = 3
    event7 = 7
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"
    ex_filename = "fizzbuzz.xlsx"
    sound_file_path = create_path(fizz_world._sound_dir, ex_filename)
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        cumlative_minute_str(),
        hour_tag_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event3, accord23_str, minute_360, hour6am]
    row2 = [sue_str, event3, accord23_str, minute_420, hour7am]
    row3 = [sue_str, event3, accord23_str, minute_420, hour8am]
    row4 = [sue_str, event7, accord23_str, minute_420, hour8am]
    df1 = DataFrame([row1, row2, row3, row4], columns=idea_columns)
    upsert_sheet(sound_file_path, "example1_br00003", df1)
    fizz_world.sound_to_drum_staging()
    br00003_agg_file_path = create_path(fizz_world._drum_dir, "br00003.xlsx")
    drum_df = pandas_read_excel(br00003_agg_file_path, sheet_name=drum_staging_str())
    assert len(drum_df) == 4
    assert sheet_exists(br00003_agg_file_path, drum_agg_str()) is False

    # WHEN
    fizz_world.drum_staging_to_drum_agg()

    # THEN
    assert sheet_exists(br00003_agg_file_path, drum_agg_str())
    gen_br00003_agg_df = pandas_read_excel(
        br00003_agg_file_path, sheet_name=drum_agg_str()
    )
    ex_otx_df = DataFrame([row1, row4], columns=idea_columns)
    # print(f"{gen_otx_df.columns=}")
    print("gen_br00003_agg_df")
    print(f"{gen_br00003_agg_df}")
    assert len(gen_br00003_agg_df.columns) == len(ex_otx_df.columns)
    assert list(gen_br00003_agg_df.columns) == list(ex_otx_df.columns)
    assert len(gen_br00003_agg_df) > 0
    assert len(gen_br00003_agg_df) == len(ex_otx_df)
    assert len(gen_br00003_agg_df) == 2
    assert gen_br00003_agg_df.to_csv() == ex_otx_df.to_csv()
    assert get_sheet_names(br00003_agg_file_path) == [
        drum_staging_str(),
        drum_agg_str(),
    ]
