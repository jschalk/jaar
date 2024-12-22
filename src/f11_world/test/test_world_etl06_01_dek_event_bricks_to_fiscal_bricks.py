from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import upsert_sheet, sheet_exists
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_dek_event_bricks_to_fiscal_bricks_CreatesFaceBrickSheets_Scenario0_MultpleFaceIDs(
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
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    music55_str = "music55"
    sue0 = [sue_str, event3, music23_str, hour6am, minute_360]
    sue1 = [sue_str, event3, music23_str, hour7am, minute_420]
    zia0 = [zia_str, event7, music23_str, hour7am, minute_420]
    zia1 = [zia_str, event9, music23_str, hour6am, minute_360]
    zia2 = [zia_str, event9, music55_str, hour7am, minute_420]
    example_event3_df = DataFrame([sue0, sue1], columns=brick_columns)
    example_event7_df = DataFrame([zia0], columns=brick_columns)
    example_event9_df = DataFrame([zia1, zia2], columns=brick_columns)
    fizz_world = worldunit_shop("fizz")
    br00003_filename = "br00003.xlsx"
    sue_dir = create_path(fizz_world._faces_dek_dir, sue_str)
    zia_dir = create_path(fizz_world._faces_dek_dir, zia_str)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_br00003_filepath = create_path(event3_dir, br00003_filename)
    event7_br00003_filepath = create_path(event7_dir, br00003_filename)
    event9_br00003_filepath = create_path(event9_dir, br00003_filename)
    upsert_sheet(event3_br00003_filepath, "inx", example_event3_df)
    upsert_sheet(event7_br00003_filepath, "inx", example_event7_df)
    upsert_sheet(event9_br00003_filepath, "inx", example_event9_df)
    e3_m23_dir = create_path(event3_dir, music23_str)
    e7_m23_dir = create_path(event7_dir, music23_str)
    e9_m23_dir = create_path(event9_dir, music23_str)
    e9_m55_dir = create_path(event9_dir, music55_str)
    e3_m23_br00003_filepath = create_path(e3_m23_dir, br00003_filename)
    e7_m23_br00003_filepath = create_path(e7_m23_dir, br00003_filename)
    e9_m23_br00003_filepath = create_path(e9_m23_dir, br00003_filename)
    e9_m55_br00003_filepath = create_path(e9_m55_dir, br00003_filename)
    assert sheet_exists(e3_m23_br00003_filepath, "inx") is False
    assert sheet_exists(e7_m23_br00003_filepath, "inx") is False
    assert sheet_exists(e9_m23_br00003_filepath, "inx") is False
    assert sheet_exists(e9_m55_br00003_filepath, "inx") is False

    # WHEN
    fizz_world.dek_event_bricks_to_fiscal_bricks()

    # THEN
    assert sheet_exists(e3_m23_br00003_filepath, "inx")
    assert sheet_exists(e7_m23_br00003_filepath, "inx")
    assert sheet_exists(e9_m23_br00003_filepath, "inx")
    assert sheet_exists(e9_m55_br00003_filepath, "inx")
    gen_e3_m23_df = pandas_read_excel(e3_m23_br00003_filepath, "inx")
    gen_e7_m23_df = pandas_read_excel(e7_m23_br00003_filepath, "inx")
    gen_e9_m23_df = pandas_read_excel(e9_m23_br00003_filepath, "inx")
    gen_e9_m55_df = pandas_read_excel(e9_m55_br00003_filepath, "inx")
    example_e3_m23_df = DataFrame([sue0, sue1], columns=brick_columns)
    example_e7_m23_df = DataFrame([zia0], columns=brick_columns)
    example_e9_m23_df = DataFrame([zia1], columns=brick_columns)
    example_e9_m55_df = DataFrame([zia2], columns=brick_columns)
    pandas_assert_frame_equal(gen_e3_m23_df, example_e3_m23_df)
    pandas_assert_frame_equal(gen_e7_m23_df, example_e7_m23_df)
    pandas_assert_frame_equal(gen_e9_m23_df, example_e9_m23_df)
    pandas_assert_frame_equal(gen_e9_m55_df, example_e9_m55_df)

    # TODO confirm dek_event_bricks_to_fiscal_bricks
