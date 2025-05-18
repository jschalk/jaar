from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import fisc_label_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_label_str
from src.a17_idea_logic._utils.str_a17 import brick_valid_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_otz_face_ideas_to_otz_event_otx_ideas_CreatesFaceIdeaSheets_Scenario0_MultpleFaceNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    event3 = 3
    event7 = 7
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    idea_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    sue0 = [event3, sue_str, accord23_str, hour6am, minute_360]
    sue1 = [event3, sue_str, accord23_str, hour7am, minute_420]
    zia0 = [event7, zia_str, accord23_str, hour7am, minute_420]
    zia1 = [event9, zia_str, accord23_str, hour6am, minute_360]
    zia2 = [event9, zia_str, accord23_str, hour7am, minute_420]
    example_sue_df = DataFrame([sue0, sue1], columns=idea_columns)
    example_zia_df = DataFrame([zia0, zia1, zia2], columns=idea_columns)
    fizz_world = worldunit_shop("fizz", worlds_dir())
    br00003_filename = "br00003.xlsx"
    sue_dir = create_path(fizz_world._syntax_otz_dir, sue_str)
    zia_dir = create_path(fizz_world._syntax_otz_dir, zia_str)
    sue_br00003_filepath = create_path(sue_dir, br00003_filename)
    zia_br00003_filepath = create_path(zia_dir, br00003_filename)
    upsert_sheet(sue_br00003_filepath, brick_valid_str(), example_sue_df)
    upsert_sheet(zia_br00003_filepath, brick_valid_str(), example_zia_df)

    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_br00003_filepath = create_path(event3_dir, br00003_filename)
    event7_br00003_filepath = create_path(event7_dir, br00003_filename)
    event9_br00003_filepath = create_path(event9_dir, br00003_filename)
    assert sheet_exists(event3_br00003_filepath, brick_valid_str()) is False
    assert sheet_exists(event7_br00003_filepath, brick_valid_str()) is False
    assert sheet_exists(event9_br00003_filepath, brick_valid_str()) is False

    # WHEN
    fizz_world.otz_face_ideas_to_otz_event_otx_ideas()

    # THEN
    assert sheet_exists(event3_br00003_filepath, brick_valid_str())
    assert sheet_exists(event7_br00003_filepath, brick_valid_str())
    assert sheet_exists(event9_br00003_filepath, brick_valid_str())
    gen_event3_df = pandas_read_excel(event3_br00003_filepath, brick_valid_str())
    gen_event7_df = pandas_read_excel(event7_br00003_filepath, brick_valid_str())
    gen_event9_df = pandas_read_excel(event9_br00003_filepath, brick_valid_str())
    example_event3_df = DataFrame([sue0, sue1], columns=idea_columns)
    example_event7_df = DataFrame([zia0], columns=idea_columns)
    example_event9_df = DataFrame([zia1, zia2], columns=idea_columns)
    pandas_assert_frame_equal(gen_event3_df, example_event3_df)
    pandas_assert_frame_equal(gen_event7_df, example_event7_df)
    pandas_assert_frame_equal(gen_event9_df, example_event9_df)
