from src.f00_instrument.file import save_file, delete_dir, create_path
from src.f01_road.finance_tran import timeconversion_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f11_world.world import init_dealunits_from_dirs, WorldUnit, worldunit_shop
from src.f11_world.examples.world_env import (
    get_test_world_id,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize dealunits and output acct metrics such as calendars, financial status, healer status


def test_WorldUnit_Exists():
    # ESTABLISH / WHEN
    x_world = WorldUnit()

    # THEN
    assert not x_world.world_id
    assert not x_world.worlds_dir
    assert not x_world.current_time
    assert not x_world.timeconversions
    assert not x_world.events
    assert not x_world._faces_bow_dir
    assert not x_world._faces_aft_dir
    assert not x_world._world_dir
    assert not x_world._ocean_dir
    assert not x_world._boat_dir
    assert not x_world._dealunits
    assert not x_world._pidgin_events


def test_WorldUnit_set_ocean_dir_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = WorldUnit("fizz")
    x_example_dir = create_path(get_test_worlds_dir(), "example_dir")
    x_ocean_dir = create_path(x_example_dir, "ocean")

    assert fizz_world._world_dir is None
    assert fizz_world._faces_bow_dir is None
    assert fizz_world._ocean_dir is None
    assert fizz_world._boat_dir is None
    assert os_path_exists(x_ocean_dir) is False

    # WHEN
    fizz_world.set_ocean_dir(x_ocean_dir)

    # THEN
    assert fizz_world._world_dir is None
    assert fizz_world._faces_bow_dir is None
    assert fizz_world._ocean_dir == x_ocean_dir
    assert fizz_world._boat_dir is None
    assert os_path_exists(x_ocean_dir)


def test_WorldUnit_set_world_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = WorldUnit(world_id=fizz_str, worlds_dir=get_test_worlds_dir())
    x_world_dir = create_path(get_test_worlds_dir(), fizz_str)
    x_faces_bow_dir = create_path(x_world_dir, "faces_bow")
    x_faces_aft_dir = create_path(x_world_dir, "faces_aft")
    x_ocean_dir = create_path(x_world_dir, "ocean")
    x_boat_dir = create_path(x_world_dir, "boat")

    assert not fizz_world._world_dir
    assert not fizz_world._faces_bow_dir
    assert not fizz_world._faces_aft_dir
    assert not fizz_world._ocean_dir
    assert not fizz_world._boat_dir
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_faces_bow_dir) is False
    assert os_path_exists(x_faces_aft_dir) is False
    assert os_path_exists(x_ocean_dir) is False
    assert os_path_exists(x_boat_dir) is False

    # WHEN
    fizz_world._set_world_dirs()

    # THEN
    assert fizz_world._world_dir == x_world_dir
    assert fizz_world._faces_bow_dir == x_faces_bow_dir
    assert fizz_world._faces_aft_dir == x_faces_aft_dir
    assert not fizz_world._ocean_dir
    assert fizz_world._boat_dir == x_boat_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_faces_bow_dir)
    assert os_path_exists(x_faces_aft_dir)
    assert os_path_exists(x_ocean_dir) is False
    assert os_path_exists(x_boat_dir)


def test_worldunit_shop_ReturnsObj_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    worlds2_dir = f"{get_test_worlds_dir()}/worlds2"
    example_ocean_dir = f"{get_test_worlds_dir()}/example_ocean"
    five_world_id = "five"
    world2_current_time = 55
    accord_str = "accord45"
    world2timeconversions = {accord_str: timeconversion_shop(accord_str)}
    world2_dealunits = {"accord45"}

    # WHEN
    x_world = worldunit_shop(
        world_id=five_world_id,
        worlds_dir=worlds2_dir,
        ocean_dir=example_ocean_dir,
        current_time=world2_current_time,
        timeconversions=world2timeconversions,
        _dealunits=world2_dealunits,
    )

    # THEN
    world_dir = create_path(worlds2_dir, x_world.world_id)
    assert x_world.world_id == five_world_id
    assert x_world.worlds_dir == worlds2_dir
    assert x_world._ocean_dir == example_ocean_dir
    assert x_world.current_time == world2_current_time
    assert x_world.timeconversions == world2timeconversions
    assert x_world.events == {}
    assert x_world._faces_bow_dir == create_path(world_dir, "faces_bow")
    assert x_world._dealunits == world2_dealunits
    assert x_world._pidgin_events == {}


def test_worldunit_shop_ReturnsObj_WithoutParameters(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    x_world = worldunit_shop()

    # THEN
    world_dir = create_path(get_test_worlds_dir(), x_world.world_id)
    assert x_world.world_id == get_test_world_id()
    assert x_world.worlds_dir == get_test_worlds_dir()
    assert x_world.current_time == 0
    assert x_world.timeconversions == {}
    assert x_world.events == {}
    assert x_world._ocean_dir == create_path(x_world._world_dir, "ocean")
    assert x_world._faces_bow_dir == create_path(world_dir, "faces_bow")
    assert x_world._faces_aft_dir == create_path(world_dir, "faces_aft")
    assert x_world._dealunits == set()


# def test_WorldUnit_open_event_from_files_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     x_world.add_pidginunit(sue_str)
#     x_world.add_pidginunit(bob_str)
#     sue_dir = create_path(x_world._faces_bow_dir, sue_str)
#     bob_dir = create_path(x_world._faces_bow_dir, bob_str)
#     assert os_path_exists(sue_dir) is False
#     assert os_path_exists(bob_dir) is False

#     # WHEN
#     x_world.save_pidginunit_files(sue_str)

#     # THEN
#     assert os_path_exists(sue_dir)
#     assert os_path_exists(bob_dir) is False


# def test_WorldUnit_save_pidginunit_ChangesFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     save_file(f"{x_world._faces_bow_dir}/{sue_str}", "temp.txt", "")
#     save_file(f"{x_world._faces_bow_dir}/{bob_str}", "temp.txt", "")
#     save_file(f"{x_world._faces_bow_dir}/{zia_str}", "temp.txt", "")
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
#     delete_dir(f"{x_world._faces_bow_dir}/{zia_str}")
#     x_world._set_all_pidginunits_from_dirs()

#     # THEN
#     assert x_world.pidginunit_exists(sue_str)
#     assert x_world.pidginunit_exists(bob_str)
#     assert x_world.pidginunit_exists(zia_str) is False
#     assert x_world.pidgins_empty() is False


def test_init_dealunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_worlds_dir()

    # WHEN
    x_dealunits = init_dealunits_from_dirs([])

    # THEN
    assert x_dealunits == []


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
