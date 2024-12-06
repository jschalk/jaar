from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_id_str,
    fiscal_id_str,
    acct_id_str,
    owner_id_str,
)
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    inx_wall_str,
    otx_wall_str,
    inx_acct_id_str,
    otx_acct_id_str,
    inx_group_id_str,
    otx_group_id_str,
    inx_idea_str,
    otx_idea_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import sheet_exists, upsert_sheet
from src.f10_world.world import worldunit_shop

from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_face_pidgins_to_event_pidgins_Scenario0_road_Two_face_ids(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("Fizz")
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
        face_id_str(),
        event_id_str(),
        otx_road_str(),
        inx_road_str(),
        otx_wall_str(),
        inx_wall_str(),
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

    sue_dir = create_path(fizz_world._faces_dir, sue_str)
    zia_dir = create_path(fizz_world._faces_dir, zia_str)
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
    fizz_world.face_pidgins_to_event_pidgins()

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
