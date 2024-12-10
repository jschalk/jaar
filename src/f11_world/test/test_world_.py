from src.f00_instrument.file import save_file, delete_dir, create_path
from src.f01_road.finance_tran import timeconversion_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f11_world.world import init_fiscalunits_from_dirs, WorldUnit, worldunit_shop
from src.f11_world.examples.world_env import (
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
    assert not x_world._faces_dir
    assert not x_world._fiscalunits
    assert not x_world._world_dir
    assert not x_world._jungle_dir
    assert not x_world._zoo_dir


def test_WorldUnit_set_jungle_dir_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = WorldUnit("fizz")
    x_example_dir = create_path(get_test_worlds_dir(), "example_dir")
    x_jungle_dir = create_path(x_example_dir, "jungle")

    assert fizz_world._world_dir is None
    assert fizz_world._faces_dir is None
    assert fizz_world._jungle_dir is None
    assert fizz_world._zoo_dir is None
    assert os_path_exists(x_jungle_dir) is False

    # WHEN
    fizz_world.set_jungle_dir(x_jungle_dir)

    # THEN
    assert fizz_world._world_dir is None
    assert fizz_world._faces_dir is None
    assert fizz_world._jungle_dir == x_jungle_dir
    assert fizz_world._zoo_dir is None
    assert os_path_exists(x_jungle_dir)


def test_WorldUnit_set_world_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = WorldUnit(world_id=fizz_str, worlds_dir=get_test_worlds_dir())
    x_world_dir = create_path(get_test_worlds_dir(), fizz_str)
    x_faces_dir = create_path(x_world_dir, "faces")
    x_jungle_dir = create_path(x_world_dir, "jungle")
    x_zoo_dir = create_path(x_world_dir, "zoo")

    assert fizz_world._world_dir is None
    assert fizz_world._faces_dir is None
    assert fizz_world._jungle_dir is None
    assert fizz_world._zoo_dir is None
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_faces_dir) is False
    assert os_path_exists(x_jungle_dir) is False
    assert os_path_exists(x_zoo_dir) is False

    # WHEN
    fizz_world._set_world_dirs()

    # THEN
    assert fizz_world._world_dir == x_world_dir
    assert fizz_world._faces_dir == x_faces_dir
    assert fizz_world._jungle_dir is None
    assert fizz_world._zoo_dir == x_zoo_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_faces_dir)
    assert os_path_exists(x_jungle_dir) is False
    assert os_path_exists(x_zoo_dir)


def test_worldunit_shop_ReturnsObj_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    worlds2_dir = f"{get_test_worlds_dir()}/worlds2"
    example_jungle_dir = f"{get_test_worlds_dir()}/example_jungle"
    five_world_id = "five"
    world2_current_time = 55
    music_text = "music45"
    sue_str = "Sue"
    bob_str = "Bob"
    world2timeconversions = {music_text: timeconversion_shop(music_text)}
    world2_fiscalunits = {"music45"}

    # WHEN
    x_world = worldunit_shop(
        world_id=five_world_id,
        worlds_dir=worlds2_dir,
        jungle_dir=example_jungle_dir,
        current_time=world2_current_time,
        timeconversions=world2timeconversions,
        _fiscalunits=world2_fiscalunits,
    )

    # THEN
    world_dir = create_path(worlds2_dir, x_world.world_id)
    assert x_world.world_id == five_world_id
    assert x_world.worlds_dir == worlds2_dir
    assert x_world._jungle_dir == example_jungle_dir
    assert x_world.current_time == world2_current_time
    assert x_world.timeconversions == world2timeconversions
    assert x_world.events == {}
    assert x_world._faces_dir == create_path(world_dir, "faces")
    assert x_world._fiscalunits == world2_fiscalunits


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
    assert x_world._jungle_dir == create_path(x_world._world_dir, "jungle")
    assert x_world._faces_dir == create_path(world_dir, "faces")
    assert x_world._fiscalunits == set()


# def test_WorldUnit_open_event_from_files_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     x_world.add_pidginunit(sue_str)
#     x_world.add_pidginunit(bob_str)
#     sue_dir = create_path(x_world._faces_dir, sue_str)
#     bob_dir = create_path(x_world._faces_dir, bob_str)
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
#     save_file(f"{x_world._faces_dir}/{sue_str}", "temp.txt", "")
#     save_file(f"{x_world._faces_dir}/{bob_str}", "temp.txt", "")
#     save_file(f"{x_world._faces_dir}/{zia_str}", "temp.txt", "")
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
#     delete_dir(f"{x_world._faces_dir}/{zia_str}")
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
