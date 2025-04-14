from src.a00_data_toolboxs.file_toolbox import save_file, delete_dir, create_path
from src.f02_finance_toolboxs.deal import timeconversion_shop
from src.f09_pidgin.pidgin import pidginunit_shop
from src.f12_world.world import init_fiscunits_from_dirs, WorldUnit, worldunit_shop
from src.f12_world.examples.world_env import (
    get_test_world_id,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize fiscunits and output acct metrics such as calendars, financial status, healer status


def test_WorldUnit_Exists():
    # ESTABLISH / WHEN
    x_world = WorldUnit()

    # THEN
    assert not x_world.world_id
    assert not x_world.worlds_dir
    assert not x_world.world_time_nigh
    assert not x_world.timeconversions
    assert not x_world.events
    assert not x_world._faces_otz_dir
    assert not x_world._faces_inz_dir
    assert not x_world._world_dir
    assert not x_world._mine_dir
    assert not x_world._cart_dir
    assert not x_world._fisc_mstr_dir
    assert not x_world._fiscunits
    assert not x_world._pidgin_events


def test_WorldUnit_set_mine_dir_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = WorldUnit("fizz")
    x_example_dir = create_path(get_test_worlds_dir(), "example_dir")
    x_mine_dir = create_path(x_example_dir, "mine")

    assert fizz_world._world_dir is None
    assert fizz_world._faces_otz_dir is None
    assert fizz_world._mine_dir is None
    assert fizz_world._cart_dir is None
    assert fizz_world._fisc_mstr_dir is None
    assert os_path_exists(x_mine_dir) is False

    # WHEN
    fizz_world.set_mine_dir(x_mine_dir)

    # THEN
    assert fizz_world._world_dir is None
    assert fizz_world._faces_otz_dir is None
    assert fizz_world._mine_dir == x_mine_dir
    assert fizz_world._cart_dir is None
    assert fizz_world._fisc_mstr_dir is None
    assert os_path_exists(x_mine_dir)


def test_WorldUnit_set_world_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = WorldUnit(world_id=fizz_str, worlds_dir=get_test_worlds_dir())
    x_world_dir = create_path(get_test_worlds_dir(), fizz_str)
    x_faces_otz_dir = create_path(x_world_dir, "faces_otz")
    x_faces_inz_dir = create_path(x_world_dir, "faces_inz")
    x_mine_dir = create_path(x_world_dir, "mine")
    x_cart_dir = create_path(x_world_dir, "cart")
    x_fisc_mstr_dir = create_path(x_world_dir, "fisc_mstr")

    assert not fizz_world._world_dir
    assert not fizz_world._faces_otz_dir
    assert not fizz_world._faces_inz_dir
    assert not fizz_world._mine_dir
    assert not fizz_world._cart_dir
    assert not fizz_world._fisc_mstr_dir
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_faces_otz_dir) is False
    assert os_path_exists(x_faces_inz_dir) is False
    assert os_path_exists(x_mine_dir) is False
    assert os_path_exists(x_cart_dir) is False
    assert os_path_exists(x_fisc_mstr_dir) is False

    # WHEN
    fizz_world._set_world_dirs()

    # THEN
    assert fizz_world._world_dir == x_world_dir
    assert fizz_world._faces_otz_dir == x_faces_otz_dir
    assert fizz_world._faces_inz_dir == x_faces_inz_dir
    assert not fizz_world._mine_dir
    assert fizz_world._cart_dir == x_cart_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_faces_otz_dir)
    assert os_path_exists(x_faces_inz_dir)
    assert os_path_exists(x_mine_dir) is False
    assert os_path_exists(x_cart_dir)
    assert os_path_exists(x_fisc_mstr_dir)


def test_worldunit_shop_ReturnsObj_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    worlds2_dir = create_path(get_test_worlds_dir(), "worlds2")
    example_mine_dir = create_path(get_test_worlds_dir(), "example_mine")
    five_world_id = "five"
    world2_time_nigh = 55
    accord45_str = "accord45"
    world2timeconversions = {accord45_str: timeconversion_shop(accord45_str)}
    world2_fiscunits = {"accord45"}

    # WHEN
    x_world = worldunit_shop(
        world_id=five_world_id,
        worlds_dir=worlds2_dir,
        mine_dir=example_mine_dir,
        world_time_nigh=world2_time_nigh,
        timeconversions=world2timeconversions,
        _fiscunits=world2_fiscunits,
    )

    # THEN
    world_dir = create_path(worlds2_dir, x_world.world_id)
    assert x_world.world_id == five_world_id
    assert x_world.worlds_dir == worlds2_dir
    assert x_world._mine_dir == example_mine_dir
    assert x_world.world_time_nigh == world2_time_nigh
    assert x_world.timeconversions == world2timeconversions
    assert x_world.events == {}
    assert x_world._faces_otz_dir == create_path(world_dir, "faces_otz")
    assert x_world._fiscunits == world2_fiscunits
    assert x_world._pidgin_events == {}


def test_worldunit_shop_ReturnsObj_WithoutParameters(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    x_world = worldunit_shop()

    # THEN
    world_dir = create_path(get_test_worlds_dir(), x_world.world_id)
    assert x_world.world_id == get_test_world_id()
    assert x_world.worlds_dir == get_test_worlds_dir()
    assert x_world.world_time_nigh == 0
    assert x_world.timeconversions == {}
    assert x_world.events == {}
    assert x_world._mine_dir == create_path(x_world._world_dir, "mine")
    assert x_world._faces_otz_dir == create_path(world_dir, "faces_otz")
    assert x_world._faces_inz_dir == create_path(world_dir, "faces_inz")
    assert x_world._fiscunits == set()


# def test_WorldUnit_open_event_from_files_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     x_world.add_pidginunit(sue_str)
#     x_world.add_pidginunit(bob_str)
#     sue_dir = create_path(x_world._faces_otz_dir, sue_str)
#     bob_dir = create_path(x_world._faces_otz_dir, bob_str)
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
#     save_file(x_world._faces_otz_dir, sue_str, "temp.txt", "")
#     save_file(x_world._faces_otz_dir, bob_str, "temp.txt", "")
#     save_file(x_world._faces_otz_dir, zia_str, "temp.txt", "")
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
#     delete_dir(x_world._faces_otz_dir, zia_str)
#     x_world._set_all_pidginunits_from_dirs()

#     # THEN
#     assert x_world.pidginunit_exists(sue_str)
#     assert x_world.pidginunit_exists(bob_str)
#     assert x_world.pidginunit_exists(zia_str) is False
#     assert x_world.pidgins_empty() is False


def test_init_fiscunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_worlds_dir()

    # WHEN
    x_fiscunits = init_fiscunits_from_dirs([])

    # THEN
    assert x_fiscunits == []


def test_WorldUnit_set_event_SetsAttr_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    assert x_world.events == {}

    # WHEN
    e5_event_int = 5
    e5_face_name = "Sue"
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world.events != {}
    assert x_world.events == {e5_event_int: e5_face_name}


def test_WorldUnit_event_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_world.event_exists(e5_event_int) is False

    # WHEN
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world.event_exists(e5_event_int)


def test_WorldUnit_get_event_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_world.get_event(e5_event_int) is None

    # WHEN
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world.get_event(e5_event_int) == e5_face_name
