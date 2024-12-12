from src.f00_instrument.file import create_path, open_file, save_file, set_dir
from src.f01_road.road import default_wall_if_None
from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f04_gift.atom_config import face_id_str, type_AcctID_str
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
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_pidgin_jsons_inherit_younger_pidgins_Scenario0_NoPidginUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    assert fizz_world._pidgin_events == {}

    # WHEN
    fizz_world.pidgin_jsons_inherit_younger_pidgins()

    # THEN nothing changes, no errors raised
    assert fizz_world._pidgin_events == {}


def test_WorldUnit_pidgin_jsons_inherit_younger_pidgins_Scenario1_OnePidginUnitFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    event3 = 3
    e3_pidginunit = pidginunit_shop(bob_str, event3)
    sue_otx = "Sue"
    sue_inx = "Suzy"
    e3_pidginunit.set_otx2inx(type_AcctID_str(), sue_otx, sue_inx)
    bob_dir = create_path(fizz_world._faces_dir, bob_str)
    event3_dir = create_path(bob_dir, event3)
    pidgin_filename = "pidgin.json"
    save_file(event3_dir, pidgin_filename, e3_pidginunit.get_json())
    e3_json_file_path = create_path(event3_dir, pidgin_filename)
    assert os_path_exists(e3_json_file_path)
    fizz_world._pidgin_events = {bob_str: {event3}}
    file_e3_pidgin_json = open_file(event3_dir, pidgin_filename)
    assert get_pidginunit_from_json(file_e3_pidgin_json) == e3_pidginunit

    # WHEN
    fizz_world.pidgin_jsons_inherit_younger_pidgins()

    # THEN
    assert get_pidginunit_from_json(file_e3_pidgin_json) == e3_pidginunit


def test_WorldUnit_pidgin_jsons_inherit_younger_pidgins_Scenario2_TwoPidginUnitFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    event3 = 3
    event7 = 7
    e3_pidginunit = pidginunit_shop(bob_str, event3)
    e7_pidginunit = pidginunit_shop(bob_str, event7)
    sue_otx = "Sue"
    sue_inx = "Suzy"
    e3_pidginunit.set_otx2inx(type_AcctID_str(), sue_otx, sue_inx)
    bob_dir = create_path(fizz_world._faces_dir, bob_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(bob_dir, event7)
    pidgin_filename = "pidgin.json"
    save_file(event3_dir, pidgin_filename, e3_pidginunit.get_json())
    save_file(event7_dir, pidgin_filename, e7_pidginunit.get_json())
    e3_json_file_path = create_path(event3_dir, pidgin_filename)
    e7_json_file_path = create_path(event7_dir, pidgin_filename)
    assert os_path_exists(e3_json_file_path)
    assert os_path_exists(e7_json_file_path)
    fizz_world._pidgin_events = {bob_str: {event3, event7}}
    file_e3_pidgin_json = open_file(event3_dir, pidgin_filename)
    file_e7_pidgin_json = open_file(event7_dir, pidgin_filename)
    before_e3_pidgin = get_pidginunit_from_json(file_e3_pidgin_json)
    before_e7_pidgin = get_pidginunit_from_json(file_e7_pidgin_json)
    assert before_e3_pidgin == e3_pidginunit
    assert before_e7_pidgin == e7_pidginunit
    assert before_e7_pidgin.otx2inx_exists(type_AcctID_str(), sue_otx, sue_inx) is False

    # WHEN
    fizz_world.pidgin_jsons_inherit_younger_pidgins()

    # THEN
    after_e3_pidgin = get_pidginunit_from_json(open_file(e3_json_file_path))
    after_e7_pidgin = get_pidginunit_from_json(open_file(e7_json_file_path))
    assert after_e3_pidgin == before_e3_pidgin
    assert after_e7_pidgin != before_e7_pidgin
    assert after_e7_pidgin.otx2inx_exists(type_AcctID_str(), sue_otx, sue_inx)


#     bob_str = "Bob"
#     casa_otx = "fizz,casa"
#     casa_inx = "fizz,casaita"
#     clean_otx = "fizz,casa,clean"
#     clean_inx = "fizz,casaita,limpio"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     pidginunit_shop()
#     fizz_world = worldunit_shop("fizz")
#     bob_dir = create_path(fizz_world._faces_dir, bob_str)
#     zia_dir = create_path(fizz_world._faces_dir, bob_str)
#     event3_dir = create_path(bob_dir, event3)
#     event7_dir = create_path(bob_dir, event7)
#     event9_dir = create_path(zia_dir, event9)
#     e3_json_file_path = create_path(event3_dir, "pidgin.json")
#     e7_json_file_path = create_path(event7_dir, "pidgin.json")
#     e9_json_file_path = create_path(event9_dir, "pidgin.json")
#     assert os_path_exists(e3_json_file_path) is False
#     assert os_path_exists(e7_json_file_path) is False
#     assert os_path_exists(e9_json_file_path) is False

#     # WHEN
#     fizz_world.event_pidgins_csvs_to_pidgin_jsons()

#     # THEN
#     assert os_path_exists(e3_json_file_path)
#     assert os_path_exists(e7_json_file_path)
#     assert os_path_exists(e9_json_file_path)
#     e3_json_pidginunit = get_pidginunit_from_json(open_file(event3_dir, "pidgin.json"))
#     assert e3_json_pidginunit.face_id == bob_str
#     assert e3_json_pidginunit.event_id == event3
#     assert e3_json_pidginunit.otx_wall == default_wall_if_None()
#     assert e3_json_pidginunit.inx_wall == default_wall_if_None()
#     assert e3_json_pidginunit.unknown_word == default_unknown_word_if_None()
#     assert e3_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), casa_otx, casa_inx)
#     assert e3_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), clean_otx, clean_inx)
#     e7_json_pidginunit = get_pidginunit_from_json(open_file(event7_dir, "pidgin.json"))
#     assert e7_json_pidginunit.face_id == bob_str
#     assert e7_json_pidginunit.event_id == event7
#     assert e7_json_pidginunit.otx_wall == default_wall_if_None()
#     assert e7_json_pidginunit.inx_wall == default_wall_if_None()
#     assert e7_json_pidginunit.unknown_word == default_unknown_word_if_None()
#     assert e7_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), casa_otx, casa_inx)
#     assert e7_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), clean_otx, clean_inx)


# # def test_WorldUnit_event_pidgins_to_pidgin_csv_files_Scenario0_1Event_road(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     bob_str = "Bob"
# #     zia_str = "Zia"
# #     casa_otx = "fizz,casa"
# #     casa_inx = "fizz,casaita"
# #     clean_otx = "fizz,casa,clean"
# #     clean_inx = "fizz,casaita,limpio"
# #     event3 = 3
# #     event7 = 7
# #     event9 = 9
# #     event3_road_csv = 'face_id,event_id,otx_road,inx_road,otx_wall,inx_wall,unknown_word\nBob,3,"fizz,casa","fizz,casaita",,,\nBob,3,"fizz,casa,clean","fizz,casaita,limpio",,,\n'
# #     bob_dir = create_path(get_test_worlds_dir(), bob_str)
# #     event3_dir = create_path(bob_dir, event3)
# #     save_file(event3_dir, "road.csv", event3_road_csv)
# #     pidgin_json_file_path = create_path(event3_dir, "pidgin.json")
# #     assert os_path_exists(pidgin_json_file_path) is False

# #     # WHEN
# #     etl_event_pidgin_csvs_to_pidgin_json(event3_dir)

# #     # THEN
# #     assert os_path_exists(pidgin_json_file_path)
# #     json_pidginunit = get_pidginunit_from_json(open_file(event3_dir, "pidgin.json"))
# #     assert json_pidginunit.face_id == bob_str
# #     assert json_pidginunit.event_id == event3
# #     assert json_pidginunit.otx_wall == default_wall_if_None()
# #     assert json_pidginunit.inx_wall == default_wall_if_None()
# #     assert json_pidginunit.unknown_word == default_unknown_word_if_None()
# #     assert json_pidginunit.otx2inx_exists(type_RoadUnit_str(), casa_otx, casa_inx)
# #     assert json_pidginunit.otx2inx_exists(type_RoadUnit_str(), clean_otx, clean_inx)

# #     # bob_dir = create_path(fizz_world._faces_dir, bob_str)
# #     # zia_dir = create_path(fizz_world._faces_dir, zia_str)
# #     # event3_dir = create_path(bob_dir, event3)
# #     # event7_dir = create_path(bob_dir, event7)
# #     # event9_dir = create_path(zia_dir, event9)
# #     # event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
# #     # event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
# #     # event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
# #     # event3_road_csv_file_path = create_path(event3_dir, "road.csv")
# #     # event7_road_csv_file_path = create_path(event7_dir, "road.csv")
# #     # event9_road_csv_file_path = create_path(event9_dir, "road.csv")
# #     # road_agg_str = "road_agg"
# #     # upsert_sheet(event3_pidgin_file_path, road_agg_str, e3_road_df)
# #     # upsert_sheet(event7_pidgin_file_path, road_agg_str, e7_road_df)
# #     # upsert_sheet(event9_pidgin_file_path, road_agg_str, e9_road_df)
# #     # assert sheet_exists(event3_pidgin_file_path, road_agg_str)
# #     # assert sheet_exists(event7_pidgin_file_path, road_agg_str)
# #     # assert sheet_exists(event9_pidgin_file_path, road_agg_str)
# #     # assert os_path_exists(event3_road_csv_file_path) is False
# #     # assert os_path_exists(event7_road_csv_file_path) is False
# #     # assert os_path_exists(event9_road_csv_file_path) is False

# #     # # WHEN
# #     # fizz_world.event_pidgins_to_pidgin_csv_files()

# #     # # THEN
# #     # assert os_path_exists(event3_road_csv_file_path)
# #     # assert os_path_exists(event7_road_csv_file_path)
# #     # assert os_path_exists(event9_road_csv_file_path)
# #     # road_filename = "road.csv"
# #     # print(f"{open_file(event3_dir, road_filename)=}")
# #     # print(f"{open_file(event7_dir, road_filename)=}")
# #     # print(f"{open_file(event9_dir, road_filename)=}")
# #     # gen_csv_event3_df = open_csv(event7_dir, "road.csv")
# #     # print(f"{gen_csv_event3_df=}")
# #     # pandas_testing_assert_frame_equal(gen_csv_event3_df, e7_road_df)


# def test_WorldUnit_set_pidgin_events_SetsAttr(env_dir_setup_cleanup):
#     # ESTABLISH
#     sue_str = "Sue"
#     zia_str = "Zia"
#     event3 = 3
#     event5 = 3
#     event7 = 7
#     event9 = 9
#     fizz_world = worldunit_shop("fizz")
#     sue_dir = create_path(fizz_world._faces_dir, sue_str)
#     zia_dir = create_path(fizz_world._faces_dir, zia_str)
#     event3_dir = create_path(zia_dir, event3)
#     event5_dir = create_path(sue_dir, event5)
#     event7_dir = create_path(sue_dir, event7)
#     event9_dir = create_path(sue_dir, event9)
#     pidgin_filename = "pidgin.json"
#     event3_pidgin_file_path = create_path(event3_dir, pidgin_filename)
#     event5_pidgin_file_path = create_path(event5_dir, pidgin_filename)
#     event7_pidgin_file_path = create_path(event7_dir, pidgin_filename)
#     event9_pidgin_file_path = create_path(event9_dir, pidgin_filename)
#     save_file(event3_dir, pidgin_filename, "")
#     set_dir(event5_dir)
#     save_file(event7_dir, pidgin_filename, "")
#     save_file(event9_dir, pidgin_filename, "")
#     print(f"{event3_pidgin_file_path=}")
#     print(f"{event5_pidgin_file_path=}")
#     print(f"{event7_pidgin_file_path=}")
#     print(f"{event9_pidgin_file_path=}")
#     assert os_path_exists(event3_pidgin_file_path)
#     assert os_path_exists(event5_pidgin_file_path) is False
#     assert os_path_exists(event7_pidgin_file_path)
#     assert os_path_exists(event9_pidgin_file_path)
#     assert fizz_world._pidgin_events == {}

#     # WHEN
#     fizz_world._set_pidgin_events()

#     # THEN
#     assert fizz_world._pidgin_events == {
#         sue_str: {event7, event9},
#         zia_str: {event3},
#     }


# def test_WorldUnit_face_pidgins_to_event_pidgins_SetsAttr_pidgin_events(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     bob_str = "Bob"
#     zia_str = "Zia"
#     casa_otx = "fizz,casa"
#     casa_inx = "fizz,casaita"
#     clean_otx = "fizz,casa,clean"
#     clean_inx = "fizz,casaita,limpio"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     event3_road_csv = f"""face_id,event_id,otx_road,inx_road,otx_wall,inx_wall,unknown_word
# "{bob_str}",{event3},"{casa_otx}","{casa_inx}",,,
# "{bob_str}",{event3},"{clean_otx}","{clean_inx}",,,
# """
#     event7_road_csv = f"""face_id,event_id,otx_road,inx_road,otx_wall,inx_wall,unknown_word
# "{bob_str}",{event7},"{casa_otx}","{casa_inx}",,,
# "{bob_str}",{event7},"{clean_otx}","{clean_inx}",,,
# """
#     event9_road_csv = f"""face_id,event_id,otx_road,inx_road,otx_wall,inx_wall,unknown_word
# "{zia_str}",{event9},"{casa_otx}","{casa_inx}",,,
# "{zia_str}",{event9},"{clean_otx}","{clean_inx}",,,
# """
#     fizz_world = worldunit_shop("fizz")
#     bob_dir = create_path(fizz_world._faces_dir, bob_str)
#     zia_dir = create_path(fizz_world._faces_dir, zia_str)
#     event3_dir = create_path(bob_dir, event3)
#     event7_dir = create_path(bob_dir, event7)
#     event9_dir = create_path(zia_dir, event9)
#     save_file(event3_dir, "road.csv", event3_road_csv)
#     save_file(event7_dir, "road.csv", event7_road_csv)
#     save_file(event9_dir, "road.csv", event9_road_csv)
#     e3_json_file_path = create_path(event3_dir, "pidgin.json")
#     e7_json_file_path = create_path(event7_dir, "pidgin.json")
#     e9_json_file_path = create_path(event9_dir, "pidgin.json")
#     assert os_path_exists(e3_json_file_path) is False
#     assert os_path_exists(e7_json_file_path) is False
#     assert os_path_exists(e9_json_file_path) is False
#     assert fizz_world._pidgin_events == {}

#     # WHEN
#     fizz_world.event_pidgins_csvs_to_pidgin_jsons()

#     # THEN
#     assert os_path_exists(e3_json_file_path)
#     assert os_path_exists(e7_json_file_path)
#     assert os_path_exists(e9_json_file_path)
#     assert fizz_world._pidgin_events == {bob_str: {event3, event7}, zia_str: {event9}}
