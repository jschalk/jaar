from src.f00_instrument.file import create_path, open_file, save_file
from src.f01_road.road import default_wall_if_none
from src.f01_road.jaar_config import default_unknown_word
from src.f04_gift.atom_config import face_id_str
from src.f08_pidgin.pidgin import pidginunit_shop, get_pidginunit_from_json
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
from src.f09_brick.pidgin_toolbox import init_pidginunit_from_dir
from src.f09_brick.pandas_tool import sheet_exists, upsert_sheet, open_csv
from src.f10_world.transformers import etl_event_pidgin_csvs_to_pidgin_json
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_event_pidgins_to_pidgin_csv_files_Scenario0_1Event_road(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event3 = 3
    event7 = 7
    event9 = 9
    event3_road_csv = 'face_id,event_id,otx_road,inx_road,otx_wall,inx_wall,unknown_word\nBob,3,"fizz,casa","fizz,casaita",,,\nBob,3,"fizz,casa,clean","fizz,casaita,limpio",,,\n'
    bob_dir = create_path(get_test_worlds_dir(), bob_str)
    event3_dir = create_path(bob_dir, event3)
    save_file(event3_dir, "road.csv", event3_road_csv)
    pidgin_json_file_path = create_path(event3_dir, "pidgin.json")
    assert os_path_exists(pidgin_json_file_path) is False

    # WHEN
    etl_event_pidgin_csvs_to_pidgin_json(event3_dir)

    # THEN
    assert os_path_exists(pidgin_json_file_path)
    json_pidginunit = get_pidginunit_from_json(open_file(event3_dir, "pidgin.json"))
    assert json_pidginunit.face_id == bob_str
    assert json_pidginunit.event_id == event3
    assert json_pidginunit.otx_wall == default_wall_if_none()
    assert json_pidginunit.inx_wall == default_wall_if_none()
    assert json_pidginunit.unknown_word == default_unknown_word()
    assert json_pidginunit.otx2inx_exists("RoadUnit", casa_otx, casa_inx)
    assert json_pidginunit.otx2inx_exists("RoadUnit", clean_otx, clean_inx)

    # bob_dir = create_path(fizz_world._faces_dir, bob_str)
    # zia_dir = create_path(fizz_world._faces_dir, zia_str)
    # event3_dir = create_path(bob_dir, event3)
    # event7_dir = create_path(bob_dir, event7)
    # event9_dir = create_path(zia_dir, event9)
    # event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
    # event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
    # event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
    # event3_road_csv_file_path = create_path(event3_dir, "road.csv")
    # event7_road_csv_file_path = create_path(event7_dir, "road.csv")
    # event9_road_csv_file_path = create_path(event9_dir, "road.csv")
    # road_agg_str = "road_agg"
    # upsert_sheet(event3_pidgin_file_path, road_agg_str, e3_road_df)
    # upsert_sheet(event7_pidgin_file_path, road_agg_str, e7_road_df)
    # upsert_sheet(event9_pidgin_file_path, road_agg_str, e9_road_df)
    # assert sheet_exists(event3_pidgin_file_path, road_agg_str)
    # assert sheet_exists(event7_pidgin_file_path, road_agg_str)
    # assert sheet_exists(event9_pidgin_file_path, road_agg_str)
    # assert os_path_exists(event3_road_csv_file_path) is False
    # assert os_path_exists(event7_road_csv_file_path) is False
    # assert os_path_exists(event9_road_csv_file_path) is False

    # # WHEN
    # fizz_world.event_pidgins_to_pidgin_csv_files()

    # # THEN
    # assert os_path_exists(event3_road_csv_file_path)
    # assert os_path_exists(event7_road_csv_file_path)
    # assert os_path_exists(event9_road_csv_file_path)
    # road_filename = "road.csv"
    # print(f"{open_file(event3_dir, road_filename)=}")
    # print(f"{open_file(event7_dir, road_filename)=}")
    # print(f"{open_file(event9_dir, road_filename)=}")
    # gen_csv_event3_df = open_csv(event7_dir, "road.csv")
    # print(f"{gen_csv_event3_df=}")
    # pandas_testing_assert_frame_equal(gen_csv_event3_df, e7_road_df)
