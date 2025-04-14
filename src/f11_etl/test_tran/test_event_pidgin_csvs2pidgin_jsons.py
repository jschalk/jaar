from src.a00_data_toolboxs.file_toolbox import (
    create_path,
    open_file,
    save_file,
    set_dir,
    delete_dir,
)
from src.a01_word_logic.road import default_bridge_if_None
from src.f04_pack.atom_config import type_RoadUnit_str
from src.f09_pidgin.pidgin_config import pidgin_filename, default_unknown_word_if_None
from src.f09_pidgin.pidgin import get_pidginunit_from_json
from src.f11_etl.transformers import (
    etl_event_pidgin_csvs_to_pidgin_json,
    etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons,
    get_pidgin_events_by_dirs,
)
from src.f11_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_etl_event_pidgin_csvs_to_pidgin_json_Scenario0_1Event_road(
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
    event3_road_csv = f"""face_name,event_int,otx_road,inx_road,otx_bridge,inx_bridge,unknown_word
"{bob_str}",{event3},"{casa_otx}","{casa_inx}",,,
"{bob_str}",{event3},"{clean_otx}","{clean_inx}",,,
"""
    bob_dir = create_path(get_test_etl_dir(), bob_str)
    event3_dir = create_path(bob_dir, event3)
    save_file(event3_dir, "road.csv", event3_road_csv)
    pidgin_json_file_path = create_path(event3_dir, pidgin_filename())
    assert os_path_exists(pidgin_json_file_path) is False

    # WHEN
    etl_event_pidgin_csvs_to_pidgin_json(event3_dir)

    # THEN
    assert os_path_exists(pidgin_json_file_path)
    json_pidginunit = get_pidginunit_from_json(open_file(event3_dir, pidgin_filename()))
    assert json_pidginunit.face_name == bob_str
    assert json_pidginunit.event_int == event3
    assert json_pidginunit.otx_bridge == default_bridge_if_None()
    assert json_pidginunit.inx_bridge == default_bridge_if_None()
    assert json_pidginunit.unknown_word == default_unknown_word_if_None()
    assert json_pidginunit.otx2inx_exists(type_RoadUnit_str(), casa_otx, casa_inx)
    assert json_pidginunit.otx2inx_exists(type_RoadUnit_str(), clean_otx, clean_inx)


def test_etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons_Scenario0_1Event_road(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # create 3 events, 2 with bob face_name, 1 with zia face_name. Each csv should be different
    # confirm 3 event_pidgin_jsons do not exists
    # WHEN
    # confirm 3 event_pidgin_jsons do exist
    bob_str = "Bob"
    zia_str = "Zia"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event3 = 3
    event7 = 7
    event9 = 9
    event3_road_csv = f"""face_name,event_int,otx_road,inx_road,otx_bridge,inx_bridge,unknown_word
"{bob_str}",{event3},"{casa_otx}","{casa_inx}",,,
"{bob_str}",{event3},"{clean_otx}","{clean_inx}",,,
"""
    event7_road_csv = f"""face_name,event_int,otx_road,inx_road,otx_bridge,inx_bridge,unknown_word
"{bob_str}",{event7},"{casa_otx}","{casa_inx}",,,
"{bob_str}",{event7},"{clean_otx}","{clean_inx}",,,
"""
    event9_road_csv = f"""face_name,event_int,otx_road,inx_road,otx_bridge,inx_bridge,unknown_word
"{zia_str}",{event9},"{casa_otx}","{casa_inx}",,,
"{zia_str}",{event9},"{clean_otx}","{clean_inx}",,,
"""
    x_faces_otz_dir = create_path(get_test_etl_dir(), "faces_otz")
    bob_dir = create_path(x_faces_otz_dir, bob_str)
    zia_dir = create_path(x_faces_otz_dir, bob_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(bob_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    save_file(event3_dir, "road.csv", event3_road_csv)
    save_file(event7_dir, "road.csv", event7_road_csv)
    save_file(event9_dir, "road.csv", event9_road_csv)
    e3_json_file_path = create_path(event3_dir, pidgin_filename())
    e7_json_file_path = create_path(event7_dir, pidgin_filename())
    e9_json_file_path = create_path(event9_dir, pidgin_filename())
    assert os_path_exists(e3_json_file_path) is False
    assert os_path_exists(e7_json_file_path) is False
    assert os_path_exists(e9_json_file_path) is False

    # WHEN
    etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons(x_faces_otz_dir)

    # THEN
    assert os_path_exists(e3_json_file_path)
    assert os_path_exists(e7_json_file_path)
    assert os_path_exists(e9_json_file_path)
    e3_json_pidginunit = get_pidginunit_from_json(
        open_file(event3_dir, pidgin_filename())
    )
    assert e3_json_pidginunit.face_name == bob_str
    assert e3_json_pidginunit.event_int == event3
    assert e3_json_pidginunit.otx_bridge == default_bridge_if_None()
    assert e3_json_pidginunit.inx_bridge == default_bridge_if_None()
    assert e3_json_pidginunit.unknown_word == default_unknown_word_if_None()
    assert e3_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), casa_otx, casa_inx)
    assert e3_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), clean_otx, clean_inx)
    e7_json_pidginunit = get_pidginunit_from_json(
        open_file(event7_dir, pidgin_filename())
    )
    assert e7_json_pidginunit.face_name == bob_str
    assert e7_json_pidginunit.event_int == event7
    assert e7_json_pidginunit.otx_bridge == default_bridge_if_None()
    assert e7_json_pidginunit.inx_bridge == default_bridge_if_None()
    assert e7_json_pidginunit.unknown_word == default_unknown_word_if_None()
    assert e7_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), casa_otx, casa_inx)
    assert e7_json_pidginunit.otx2inx_exists(type_RoadUnit_str(), clean_otx, clean_inx)

    # bob_dir = create_path(fizz_world._faces_otz_dir, bob_str)
    # zia_dir = create_path(fizz_world._faces_otz_dir, zia_str)
    # event3_dir = create_path(bob_dir, event3)
    # event7_dir = create_path(bob_dir, event7)
    # event9_dir = create_path(z
    # event3_pidgin_file_path = create_otx_event_pidgin_path(event3_dir)
    # event7_pidgin_file_path = create_otx_event_pidgin_path(event7_dir)
    # event9_pidgin_file_path = create_otx_event_pidgin_path(event9_dir)
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
    # fizz_world.otz_event_pidgins_to_otz_pidgin_csv_files()

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


def test_get_pidgin_events_by_dirs_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    event3 = 3
    event5 = 3
    event7 = 7
    event9 = 9

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    event3_dir = create_path(zia_dir, event3)
    event5_dir = create_path(sue_dir, event5)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    event3_pidgin_file_path = create_path(event3_dir, pidgin_filename())
    event5_pidgin_file_path = create_path(event5_dir, pidgin_filename())
    event7_pidgin_file_path = create_path(event7_dir, pidgin_filename())
    event9_pidgin_file_path = create_path(event9_dir, pidgin_filename())
    save_file(event3_dir, pidgin_filename(), "")
    set_dir(event5_dir)
    save_file(event7_dir, pidgin_filename(), "")
    save_file(event9_dir, pidgin_filename(), "")
    print(f"{event3_pidgin_file_path=}")
    print(f"{event5_pidgin_file_path=}")
    print(f"{event7_pidgin_file_path=}")
    print(f"{event9_pidgin_file_path=}")
    assert os_path_exists(event3_pidgin_file_path)
    assert os_path_exists(event5_pidgin_file_path) is False
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)

    # WHEN
    pidgin_events = get_pidgin_events_by_dirs(faces_dir)

    # THEN
    assert pidgin_events == {sue_str: {event7, event9}, zia_str: {event3}}

    # WHEN
    delete_dir(event3_pidgin_file_path)
    assert os_path_exists(event3_pidgin_file_path) is False
    assert os_path_exists(event5_pidgin_file_path) is False
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)

    # WHEN
    pidgin_events = get_pidgin_events_by_dirs(faces_dir)

    # THEN
    assert pidgin_events == {sue_str: {event7, event9}}
