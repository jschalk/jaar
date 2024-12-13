from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str
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
from src.f09_brick.pandas_tool import sheet_exists, upsert_sheet, open_csv
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_event_pidgins_to_pidgin_csv_files_Scenario0_3Event_road(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
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
    e3_road0 = [bob_str, event3, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e3_road1 = [bob_str, event3, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e3_road_rows = [e3_road0, e3_road1]
    e3_road_df = DataFrame(e3_road_rows, columns=road_file_columns)

    e7_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e7_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e7_road_rows = [e7_road0, e7_road1]
    e7_road_df = DataFrame(e7_road_rows, columns=road_file_columns)

    e9_road0 = [zia_str, event9, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e9_road1 = [zia_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e9_road_rows = [e9_road0, e9_road1]
    e9_road_df = DataFrame(e9_road_rows, columns=road_file_columns)

    fizz_world = worldunit_shop("Fizz")
    bob_dir = create_path(fizz_world._faces_otx_dir, bob_str)
    sue_dir = create_path(fizz_world._faces_otx_dir, sue_str)
    zia_dir = create_path(fizz_world._faces_otx_dir, zia_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
    event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
    event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
    event3_road_csv_file_path = create_path(event3_dir, "road.csv")
    event7_road_csv_file_path = create_path(event7_dir, "road.csv")
    event9_road_csv_file_path = create_path(event9_dir, "road.csv")
    road_agg_str = "road_agg"
    upsert_sheet(event3_pidgin_file_path, road_agg_str, e3_road_df)
    upsert_sheet(event7_pidgin_file_path, road_agg_str, e7_road_df)
    upsert_sheet(event9_pidgin_file_path, road_agg_str, e9_road_df)
    assert sheet_exists(event3_pidgin_file_path, road_agg_str)
    assert sheet_exists(event7_pidgin_file_path, road_agg_str)
    assert sheet_exists(event9_pidgin_file_path, road_agg_str)
    assert os_path_exists(event3_road_csv_file_path) is False
    assert os_path_exists(event7_road_csv_file_path) is False
    assert os_path_exists(event9_road_csv_file_path) is False

    # WHEN
    fizz_world.event_pidgins_to_pidgin_csv_files()

    # THEN
    assert os_path_exists(event3_road_csv_file_path)
    assert os_path_exists(event7_road_csv_file_path)
    assert os_path_exists(event9_road_csv_file_path)
    gen_csv_event3_df = open_csv(event7_dir, "road.csv")
    print(f"{gen_csv_event3_df=}")
    pandas_testing_assert_frame_equal(gen_csv_event3_df, e7_road_df)
