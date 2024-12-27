from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, deal_id_str
from src.f07_deal.deal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import upsert_sheet, boat_valid_str, sheet_exists
from src.f10_etl.transformers import etl_bow_face_bricks_to_bow_event_otx_bricks
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_bow_face_bricks_to_bow_event_otx_bricks_CreatesFaceBrickSheets_Scenario0_MultpleFaceIDs(
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
        deal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    sue0 = [sue_str, event3, music23_str, hour6am, minute_360]
    sue1 = [sue_str, event3, music23_str, hour7am, minute_420]
    zia0 = [zia_str, event7, music23_str, hour7am, minute_420]
    zia1 = [zia_str, event9, music23_str, hour6am, minute_360]
    zia2 = [zia_str, event9, music23_str, hour7am, minute_420]
    example_sue_df = DataFrame([sue0, sue1], columns=brick_columns)
    example_zia_df = DataFrame([zia0, zia1, zia2], columns=brick_columns)
    x_etl_dir = get_test_etl_dir()
    x_faces_bow_dir = create_path(x_etl_dir, "faces_bow")
    br00003_filename = "br00003.xlsx"
    sue_dir = create_path(x_faces_bow_dir, sue_str)
    zia_dir = create_path(x_faces_bow_dir, zia_str)
    sue_br00003_filepath = create_path(sue_dir, br00003_filename)
    zia_br00003_filepath = create_path(zia_dir, br00003_filename)
    upsert_sheet(sue_br00003_filepath, boat_valid_str(), example_sue_df)
    upsert_sheet(zia_br00003_filepath, boat_valid_str(), example_zia_df)

    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_br00003_filepath = create_path(event3_dir, br00003_filename)
    event7_br00003_filepath = create_path(event7_dir, br00003_filename)
    event9_br00003_filepath = create_path(event9_dir, br00003_filename)
    assert sheet_exists(event3_br00003_filepath, boat_valid_str()) is False
    assert sheet_exists(event7_br00003_filepath, boat_valid_str()) is False
    assert sheet_exists(event9_br00003_filepath, boat_valid_str()) is False

    # WHEN
    etl_bow_face_bricks_to_bow_event_otx_bricks(x_faces_bow_dir)

    # THEN
    assert sheet_exists(event3_br00003_filepath, boat_valid_str())
    assert sheet_exists(event7_br00003_filepath, boat_valid_str())
    assert sheet_exists(event9_br00003_filepath, boat_valid_str())

    gen_event3_df = pandas_read_excel(event3_br00003_filepath, boat_valid_str())
    gen_event7_df = pandas_read_excel(event7_br00003_filepath, boat_valid_str())
    gen_event9_df = pandas_read_excel(event9_br00003_filepath, boat_valid_str())
    example_event3_df = DataFrame([sue0, sue1], columns=brick_columns)
    example_event7_df = DataFrame([zia0], columns=brick_columns)
    example_event9_df = DataFrame([zia1, zia2], columns=brick_columns)
    pandas_assert_frame_equal(gen_event3_df, example_event3_df)
    pandas_assert_frame_equal(gen_event7_df, example_event7_df)
    pandas_assert_frame_equal(gen_event9_df, example_event9_df)
