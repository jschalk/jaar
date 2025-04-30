from src.a00_data_toolbox.file_toolbox import save_file, delete_dir, create_path
from src.a02_finance_logic.deal import timeconversion_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from src.a19_world_logic.world import (
    init_fiscunits_from_dirs,
    WorldUnit,
    worldunit_shop,
)
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
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
    assert not x_world._events
    assert not x_world._syntax_otz_dir
    assert not x_world._syntax_inz_dir
    assert not x_world._world_dir
    assert not x_world._mud_dir
    assert not x_world._brick_dir
    assert not x_world._fisc_mstr_dir
    assert not x_world._fiscunits
    assert not x_world._pidgin_events


def test_WorldUnit_set_mud_dir_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = WorldUnit("fizz")
    x_example_dir = create_path(worlds_dir(), "example_dir")
    x_mud_dir = create_path(x_example_dir, "mud")

    assert fizz_world._world_dir is None
    assert fizz_world._syntax_otz_dir is None
    assert fizz_world._mud_dir is None
    assert fizz_world._brick_dir is None
    assert fizz_world._fisc_mstr_dir is None
    assert os_path_exists(x_mud_dir) is False

    # WHEN
    fizz_world.set_mud_dir(x_mud_dir)

    # THEN
    assert fizz_world._world_dir is None
    assert fizz_world._syntax_otz_dir is None
    assert fizz_world._mud_dir == x_mud_dir
    assert fizz_world._brick_dir is None
    assert fizz_world._fisc_mstr_dir is None
    assert os_path_exists(x_mud_dir)


def test_WorldUnit_set_world_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = WorldUnit(world_id=fizz_str, worlds_dir=worlds_dir())
    x_world_dir = create_path(worlds_dir(), fizz_str)
    x_syntax_otz_dir = create_path(x_world_dir, "syntax_otz")
    x_syntax_inz_dir = create_path(x_world_dir, "syntax_inz")
    x_mud_dir = create_path(x_world_dir, "mud")
    x_brick_dir = create_path(x_world_dir, "brick")
    x_fisc_mstr_dir = create_path(x_world_dir, "fisc_mstr")

    assert not fizz_world._world_dir
    assert not fizz_world._syntax_otz_dir
    assert not fizz_world._syntax_inz_dir
    assert not fizz_world._mud_dir
    assert not fizz_world._brick_dir
    assert not fizz_world._fisc_mstr_dir
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_syntax_otz_dir) is False
    assert os_path_exists(x_syntax_inz_dir) is False
    assert os_path_exists(x_mud_dir) is False
    assert os_path_exists(x_brick_dir) is False
    assert os_path_exists(x_fisc_mstr_dir) is False

    # WHEN
    fizz_world._set_world_dirs()

    # THEN
    assert fizz_world._world_dir == x_world_dir
    assert fizz_world._syntax_otz_dir == x_syntax_otz_dir
    assert fizz_world._syntax_inz_dir == x_syntax_inz_dir
    assert not fizz_world._mud_dir
    assert fizz_world._brick_dir == x_brick_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_syntax_otz_dir)
    assert os_path_exists(x_syntax_inz_dir)
    assert os_path_exists(x_mud_dir) is False
    assert os_path_exists(x_brick_dir)
    assert os_path_exists(x_fisc_mstr_dir)


def test_worldunit_shop_ReturnsObj_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    worlds2_dir = create_path(worlds_dir(), "worlds2")
    example_mud_dir = create_path(worlds_dir(), "example_mud")
    five_world_id = "five"
    world2_time_nigh = 55
    accord45_str = "accord45"
    world2timeconversions = {accord45_str: timeconversion_shop(accord45_str)}
    world2_fiscunits = {"accord45"}

    # WHEN
    x_world = worldunit_shop(
        world_id=five_world_id,
        worlds_dir=worlds2_dir,
        mud_dir=example_mud_dir,
        world_time_nigh=world2_time_nigh,
        timeconversions=world2timeconversions,
        _fiscunits=world2_fiscunits,
    )

    # THEN
    world_dir = create_path(worlds2_dir, x_world.world_id)
    assert x_world.world_id == five_world_id
    assert x_world.worlds_dir == worlds2_dir
    assert x_world._mud_dir == example_mud_dir
    assert x_world.world_time_nigh == world2_time_nigh
    assert x_world.timeconversions == world2timeconversions
    assert x_world._events == {}
    assert x_world._syntax_otz_dir == create_path(world_dir, "syntax_otz")
    assert x_world._fiscunits == world2_fiscunits
    assert x_world._pidgin_events == {}


def test_worldunit_shop_ReturnsObj_WithoutParameters(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    x_world = worldunit_shop(a23_str, worlds_dir())

    # THEN
    world_dir = create_path(worlds_dir(), x_world.world_id)
    assert x_world.world_id == a23_str
    assert x_world.worlds_dir == worlds_dir()
    assert x_world.world_time_nigh == 0
    assert x_world.timeconversions == {}
    assert x_world._events == {}
    assert x_world._mud_dir == create_path(x_world._world_dir, "mud")
    assert x_world._syntax_otz_dir == create_path(world_dir, "syntax_otz")
    assert x_world._syntax_inz_dir == create_path(world_dir, "syntax_inz")
    assert x_world._fiscunits == set()


# def test_WorldUnit_open_event_from_files_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     x_world.add_pidginunit(sue_str)
#     x_world.add_pidginunit(bob_str)
#     sue_dir = create_path(x_world._syntax_otz_dir, sue_str)
#     bob_dir = create_path(x_world._syntax_otz_dir, bob_str)
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
#     save_file(x_world._syntax_otz_dir, sue_str, "temp.txt", "")
#     save_file(x_world._syntax_otz_dir, bob_str, "temp.txt", "")
#     save_file(x_world._syntax_otz_dir, zia_str, "temp.txt", "")
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
#     delete_dir(x_world._syntax_otz_dir, zia_str)
#     x_world._set_all_pidginunits_from_dirs()

#     # THEN
#     assert x_world.pidginunit_exists(sue_str)
#     assert x_world.pidginunit_exists(bob_str)
#     assert x_world.pidginunit_exists(zia_str) is False
#     assert x_world.pidgins_empty() is False


def test_init_fiscunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = worlds_dir()

    # WHEN
    x_fiscunits = init_fiscunits_from_dirs([])

    # THEN
    assert x_fiscunits == []


def test_WorldUnit_set_event_SetsAttr_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop("accord23", worlds_dir())
    assert x_world._events == {}

    # WHEN
    e5_event_int = 5
    e5_face_name = "Sue"
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world._events != {}
    assert x_world._events == {e5_event_int: e5_face_name}


def test_WorldUnit_event_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop("accord23", worlds_dir())
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_world.event_exists(e5_event_int) is False

    # WHEN
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world.event_exists(e5_event_int)


def test_WorldUnit_get_event_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop("accord23", worlds_dir())
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_world.get_event(e5_event_int) is None

    # WHEN
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world.get_event(e5_event_int) == e5_face_name
