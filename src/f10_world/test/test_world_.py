from src.f00_instrument.file import save_file, delete_dir, create_file_path
from src.f01_road.finance_tran import timeconversion_shop
from src.f04_gift.atom_config import road_str
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f10_world.world import (
    init_fiscalunits_from_dirs,
    WorldUnit,
    worldunit_shop,
)
from src.f10_world.examples.world_env import (
    get_test_world_id,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_WorldUnit_Exists():
    # ESTABLISH / WHEN
    x_world = WorldUnit()

    # THEN
    assert not x_world.world_id
    assert not x_world.worlds_dir
    assert not x_world.current_time
    assert not x_world.timeconversions
    assert not x_world.events
    assert not x_world.pidgins
    assert not x_world._events_dir
    assert not x_world._pidgins_dir
    assert not x_world._fiscalunits
    assert not x_world._world_dir
    assert not x_world._jungle_dir
    assert not x_world._zoo_dir


def test_worldunit_shop_ReturnsObj_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    worlds2_dir = f"{get_test_worlds_dir()}/worlds2"
    five_world_id = "five"
    world2_current_time = 55
    music_text = "music45"
    sue_str = "Sue"
    bob_str = "Bob"
    world2_pidgins = {
        sue_str: pidginunit_shop(sue_str),
        bob_str: pidginunit_shop(bob_str),
    }
    world2timeconversions = {music_text: timeconversion_shop(music_text)}
    world2_fiscalunits = {"music45"}

    # WHEN
    x_world = worldunit_shop(
        five_world_id,
        worlds2_dir,
        world2_current_time,
        world2timeconversions,
        world2_pidgins,
        world2_fiscalunits,
    )

    # THEN
    assert x_world.world_id == five_world_id
    assert x_world.worlds_dir == worlds2_dir
    assert x_world.current_time == world2_current_time
    assert x_world.timeconversions == world2timeconversions
    assert x_world.events == {}
    assert x_world.pidgins == world2_pidgins
    assert x_world._events_dir == f"{worlds2_dir}/{five_world_id}/events"
    assert x_world._pidgins_dir == f"{worlds2_dir}/{five_world_id}/pidgins"
    assert x_world._fiscalunits == world2_fiscalunits


def test_worldunit_shop_ReturnsObj_WithoutParameters(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    x_world = worldunit_shop()

    # THEN
    assert x_world.world_id == get_test_world_id()
    assert x_world.worlds_dir == get_test_worlds_dir()
    assert x_world.current_time == 0
    assert x_world.timeconversions == {}
    assert x_world.pidgins == {}
    assert x_world.events == {}
    assert x_world._events_dir == f"{get_test_worlds_dir()}/{x_world.world_id}/events"
    assert x_world._pidgins_dir == f"{get_test_worlds_dir()}/{x_world.world_id}/pidgins"
    assert x_world._fiscalunits == set()


def test_WorldUnit_set_pidginunit_SetsAttr_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    assert x_world.pidgins == {}

    # WHEN
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_world.set_pidginunit(sue_pidginunit)

    # THEN
    assert x_world.pidgins != {}
    assert x_world.pidgins == {sue_str: sue_pidginunit}


def test_WorldUnit_add_pidginunit_SetsAttr_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    assert x_world.pidgins == {}

    # WHEN
    sue_str = "Sue"
    x_world.add_pidginunit(sue_str)

    # THEN
    assert x_world.pidgins != {}
    assert x_world.pidgins == {sue_str: pidginunit_shop(sue_str)}


def test_WorldUnit_pidginunit_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    assert x_world.pidginunit_exists(sue_str) is False

    # WHEN
    x_world.add_pidginunit(sue_str)

    # THEN
    assert x_world.pidginunit_exists(sue_str)


def test_WorldUnit_get_pidginunit_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    slash_str = "/"
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str, slash_str)
    assert x_world.get_pidginunit(sue_str) is None

    # WHEN
    x_world.set_pidginunit(sue_pidginunit)

    # THEN
    assert x_world.get_pidginunit(sue_str) == sue_pidginunit


def test_WorldUnit_del_pidginunit_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    sue_pidginunit = pidginunit_shop(sue_str)
    bob_pidginunit = pidginunit_shop(bob_str)
    x_world.set_pidginunit(sue_pidginunit)
    x_world.set_pidginunit(bob_pidginunit)
    assert x_world.get_pidginunit(sue_str) == sue_pidginunit
    assert x_world.get_pidginunit(bob_str) == bob_pidginunit

    # WHEN
    x_world.del_pidginunit(sue_str)

    # THEN
    assert x_world.get_pidginunit(sue_str) is None
    assert x_world.get_pidginunit(bob_str) == bob_pidginunit


def test_WorldUnit_del_all_pidginunits_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    sue_pidginunit = pidginunit_shop(sue_str)
    bob_pidginunit = pidginunit_shop(bob_str)
    x_world.set_pidginunit(sue_pidginunit)
    x_world.set_pidginunit(bob_pidginunit)
    assert x_world.get_pidginunit(sue_str) == sue_pidginunit
    assert x_world.get_pidginunit(bob_str) == bob_pidginunit

    # WHEN
    x_world.del_all_pidginunits()

    # THEN
    assert x_world.get_pidginunit(sue_str) is None
    assert x_world.get_pidginunit(bob_str) is None
    assert x_world.pidgins == {}


def test_WorldUnit_pidgins_empty_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    assert x_world.pidgins_empty()

    # WHEN / THEN
    x_world.add_pidginunit(sue_str)
    assert x_world.pidgins_empty() is False

    # WHEN / THEN
    x_world.add_pidginunit(bob_str)
    assert x_world.pidgins_empty() is False

    # WHEN / THEN
    x_world.del_all_pidginunits()
    assert x_world.pidgins_empty()


def test_WorldUnit_save_pidginunit_files_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    x_world.add_pidginunit(sue_str)
    x_world.add_pidginunit(bob_str)
    sue_dir = create_file_path(x_world._pidgins_dir, sue_str)
    bob_dir = create_file_path(x_world._pidgins_dir, bob_str)
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir) is False

    # WHEN
    x_world.save_pidginunit_files(sue_str)

    # THEN
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir)


def test_WorldUnit_pidgins_dir_exist_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    x_world.add_pidginunit(sue_str)
    x_world.add_pidginunit(bob_str)
    sue_dir = create_file_path(x_world._pidgins_dir, sue_str)
    bob_dir = create_file_path(x_world._pidgins_dir, bob_str)
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir) is False
    assert x_world.pidgin_dir_exists(bob_str) is False
    assert x_world.pidgin_dir_exists(sue_str) is False

    # WHEN
    x_world.save_pidginunit_files(sue_str)

    # THEN
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir)
    assert x_world.pidgin_dir_exists(bob_str) is False
    assert x_world.pidgin_dir_exists(sue_str)


def test_WorldUnit_load_pidginunit_from_files_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_otx = "Bob"
    bob2_inx = "Bob2"
    bob3_inx = "Bob3"
    x_world.add_pidginunit(sue_str)
    sue_pidginunit = x_world.get_pidginunit(sue_str)
    sue_pidginunit.set_otx_to_inx(road_str(), bob_otx, bob2_inx)
    x_world.save_pidginunit_files(sue_str)
    sue_pidginunit.set_otx_to_inx(road_str(), bob_otx, bob3_inx)
    assert x_world.pidgin_dir_exists(sue_str)
    assert sue_pidginunit.otx_to_inx_exists(road_str(), bob_otx, bob2_inx) is False
    assert sue_pidginunit.otx_to_inx_exists(road_str(), bob_otx, bob3_inx)

    # WHEN
    x_world.load_pidginunit_from_files(sue_str)

    # THEN
    after_pidginunit = x_world.get_pidginunit(sue_str)
    assert after_pidginunit.otx_to_inx_exists(road_str(), bob_otx, bob2_inx)
    assert after_pidginunit.otx_to_inx_exists(road_str(), bob_otx, bob3_inx) is False


def test_WorldUnit_delete_pidginunit_dir_SetsAttrDeletesDir(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    x_world.add_pidginunit(sue_str)
    x_world.add_pidginunit(bob_str)
    x_world.save_pidginunit_files(sue_str)
    x_world.save_pidginunit_files(bob_str)
    assert x_world.pidginunit_exists(sue_str)
    assert x_world.pidginunit_exists(bob_str)
    assert x_world.pidgin_dir_exists(sue_str)
    assert x_world.pidgin_dir_exists(bob_str)

    # WHEN
    x_world._delete_pidginunit_dir(sue_str)

    # THEN
    assert x_world.pidginunit_exists(sue_str)
    assert x_world.pidginunit_exists(bob_str)
    assert x_world.pidgin_dir_exists(sue_str) is False
    assert x_world.pidgin_dir_exists(bob_str)


# def test_WorldUnit_open_event_from_files_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     x_world.add_pidginunit(sue_str)
#     x_world.add_pidginunit(bob_str)
#     sue_dir = create_file_path(x_world._pidgins_dir, sue_str)
#     bob_dir = create_file_path(x_world._pidgins_dir, bob_str)
#     assert os_path_exists(sue_dir) is False
#     assert os_path_exists(bob_dir) is False

#     # WHEN
#     x_world.save_pidginunit_files(sue_str)

#     # THEN
#     assert os_path_exists(sue_dir)
#     assert os_path_exists(bob_dir) is False


def test_WorldUnit_set_all_events_from_dirs_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    save_file(f"{x_world._pidgins_dir}/{sue_str}", "temp.txt", "")
    save_file(f"{x_world._pidgins_dir}/{bob_str}", "temp.txt", "")
    save_file(f"{x_world._pidgins_dir}/{zia_str}", "temp.txt", "")
    assert x_world.pidginunit_exists(sue_str) is False
    assert x_world.pidginunit_exists(bob_str) is False
    assert x_world.pidginunit_exists(zia_str) is False
    assert x_world.pidgins_empty()

    # WHEN
    x_world._set_all_pidginunits_from_dirs()

    # THEN
    assert x_world.pidginunit_exists(sue_str)
    assert x_world.pidginunit_exists(bob_str)
    assert x_world.pidginunit_exists(zia_str)
    assert x_world.pidgins_empty() is False

    # WHEN
    delete_dir(f"{x_world._pidgins_dir}/{zia_str}")
    x_world._set_all_pidginunits_from_dirs()

    # THEN
    assert x_world.pidginunit_exists(sue_str)
    assert x_world.pidginunit_exists(bob_str)
    assert x_world.pidginunit_exists(zia_str) is False
    assert x_world.pidgins_empty() is False


# def test_WorldUnit_save_pidginunit_ChangesFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     save_file(f"{x_world._pidgins_dir}/{sue_str}", "temp.txt", "")
#     save_file(f"{x_world._pidgins_dir}/{bob_str}", "temp.txt", "")
#     save_file(f"{x_world._pidgins_dir}/{zia_str}", "temp.txt", "")
#     assert x_world.pidginunit_exists(sue_str) is False
#     assert x_world.pidginunit_exists(bob_str) is False
#     assert x_world.pidginunit_exists(zia_str) is False
#     assert x_world.pidgins_empty()

#     # WHEN
#     x_world._set_all_pidginunits_from_dirs()

#     # THEN
#     assert x_world.pidginunit_exists(sue_str)
#     assert x_world.pidginunit_exists(bob_str)
#     assert x_world.pidginunit_exists(zia_str)
#     assert x_world.pidgins_empty() is False

#     # WHEN
#     delete_dir(f"{x_world._pidgins_dir}/{zia_str}")
#     x_world._set_all_pidginunits_from_dirs()

#     # THEN
#     assert x_world.pidginunit_exists(sue_str)
#     assert x_world.pidginunit_exists(bob_str)
#     assert x_world.pidginunit_exists(zia_str) is False
#     assert x_world.pidgins_empty() is False


def test_init_fiscalunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_worlds_dir()

    # WHEN
    x_fiscalunits = init_fiscalunits_from_dirs([])

    # THEN
    assert x_fiscalunits == []


def test_WorldUnit_set_event_SetsAttr_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    assert x_world.events == {}

    # WHEN
    e5_event_id = 5
    e5_face_id = "Sue"
    x_world.set_event(e5_event_id, e5_face_id)

    # THEN
    assert x_world.events != {}
    assert x_world.events == {e5_event_id: e5_face_id}


def test_WorldUnit_event_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    e5_event_id = 5
    e5_face_id = "Sue"
    assert x_world.event_exists(e5_event_id) is False

    # WHEN
    x_world.set_event(e5_event_id, e5_face_id)

    # THEN
    assert x_world.event_exists(e5_event_id)


def test_WorldUnit_get_event_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    e5_event_id = 5
    e5_face_id = "Sue"
    assert x_world.get_event(e5_event_id) is None

    # WHEN
    x_world.set_event(e5_event_id, e5_face_id)

    # THEN
    assert x_world.get_event(e5_event_id) == e5_face_id
