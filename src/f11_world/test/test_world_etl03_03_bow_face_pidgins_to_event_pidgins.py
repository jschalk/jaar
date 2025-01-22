from src.f00_instrument.file import create_path, get_dir_filenames
from src.f04_gift.atom_config import face_name_str
from src.f08_pidgin.pidgin_config import (
    event_int_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    inx_title_str,
    otx_title_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.f09_idea.idea_db_tool import sheet_exists, upsert_sheet
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_bow_face_pidgins_to_bow_event_pidgins_Scenario0_road_Two_face_names(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event3 = 3
    event7 = 7
    event9 = 9
    road_file_columns = [
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    x_nan = float("nan")
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road2 = [sue_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1, e1_road2]
    sue_road_agg_df = DataFrame(e1_road_rows, columns=road_file_columns)
    z1_road3 = [zia_str, event3, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    zia_road_agg_df = DataFrame([z1_road3], columns=road_file_columns)

    fizz_world = worldunit_shop("fizz")
    sue_dir = create_path(fizz_world._faces_bow_dir, sue_str)
    zia_dir = create_path(fizz_world._faces_bow_dir, zia_str)
    event3_dir = create_path(zia_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
    zia_pidgin_file_path = create_path(zia_dir, "pidgin.xlsx")
    event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
    event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
    event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
    road_agg_str = "road_agg"
    upsert_sheet(sue_pidgin_file_path, road_agg_str, sue_road_agg_df)
    upsert_sheet(zia_pidgin_file_path, road_agg_str, zia_road_agg_df)
    assert sheet_exists(sue_pidgin_file_path, road_agg_str)
    assert sheet_exists(zia_pidgin_file_path, road_agg_str)

    assert os_path_exists(event3_dir) is False
    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, road_agg_str) is False
    assert sheet_exists(event7_pidgin_file_path, road_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, road_agg_str) is False

    # WHEN
    fizz_world.bow_face_pidgins_to_bow_event_pidgins()

    # THEN
    assert os_path_exists(event3_dir)
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event3_pidgin_file_path)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event3_pidgin_file_path, road_agg_str)
    assert sheet_exists(event7_pidgin_file_path, road_agg_str)
    assert sheet_exists(event9_pidgin_file_path, road_agg_str)
    e3_pidgin_road_df = pandas_read_excel(event3_pidgin_file_path, road_agg_str)
    e7_pidgin_road_df = pandas_read_excel(event7_pidgin_file_path, road_agg_str)
    e9_pidgin_road_df = pandas_read_excel(event9_pidgin_file_path, road_agg_str)

    expected7_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    expected7_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    expected7_road_rows = [expected7_road0, expected7_road1]
    expected7_agg_df = DataFrame(expected7_road_rows, columns=road_file_columns)

    expected9_road0 = [sue_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    expected9_road_rows = [expected9_road0]
    expected9_agg_df = DataFrame(expected9_road_rows, columns=road_file_columns)

    pandas_testing_assert_frame_equal(e3_pidgin_road_df, zia_road_agg_df)
    pandas_testing_assert_frame_equal(e7_pidgin_road_df, expected7_agg_df)
    pandas_testing_assert_frame_equal(e9_pidgin_road_df, expected9_agg_df)
