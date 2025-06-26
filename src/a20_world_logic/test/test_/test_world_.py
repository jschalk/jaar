from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a20_world_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.a20_world_logic.world import (
    WorldName,
    WorldUnit,
    init_beliefunits_from_dirs,
    worldunit_shop,
)


def test_WorldName_Exists():
    # ESTABLISH / WHEN / THEN
    assert WorldName() == ""
    assert WorldName("cookie") == "cookie"


def test_WorldUnit_Exists():
    # ESTABLISH / WHEN
    x_world = WorldUnit()

    # THEN
    assert not x_world.world_name
    assert not x_world.worlds_dir
    assert not x_world.output_dir
    assert not x_world.world_time_pnigh
    assert not x_world._events
    assert not x_world._syntax_otz_dir
    assert not x_world._world_dir
    assert not x_world._input_dir
    assert not x_world._brick_dir
    assert not x_world._belief_mstr_dir
    assert not x_world._beliefunits
    assert not x_world._pidgin_events


def test_WorldUnit_set_input_dir_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = WorldUnit("fizz")
    x_example_dir = create_path(worlds_dir(), "example_dir")
    x_input_dir = create_path(x_example_dir, "input")

    assert not fizz_world._world_dir
    assert not fizz_world._syntax_otz_dir
    assert not fizz_world._input_dir
    assert not fizz_world._brick_dir
    assert not fizz_world._belief_mstr_dir
    assert os_path_exists(x_input_dir) is False

    # WHEN
    fizz_world.set_input_dir(x_input_dir)

    # THEN
    assert not fizz_world._world_dir
    assert not fizz_world._syntax_otz_dir
    assert fizz_world._input_dir == x_input_dir
    assert not fizz_world._brick_dir
    assert not fizz_world._belief_mstr_dir
    assert os_path_exists(x_input_dir)


def test_WorldUnit_set_world_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = WorldUnit(world_name=fizz_str, worlds_dir=worlds_dir())
    x_world_dir = create_path(worlds_dir(), fizz_str)
    x_syntax_otz_dir = create_path(x_world_dir, "syntax_otz")
    x_input_dir = create_path(x_world_dir, "input")
    x_brick_dir = create_path(x_world_dir, "brick")
    x_belief_mstr_dir = create_path(x_world_dir, "belief_mstr")

    assert not fizz_world._world_dir
    assert not fizz_world._syntax_otz_dir
    assert not fizz_world._input_dir
    assert not fizz_world._brick_dir
    assert not fizz_world._belief_mstr_dir
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_syntax_otz_dir) is False
    assert os_path_exists(x_input_dir) is False
    assert os_path_exists(x_brick_dir) is False
    assert os_path_exists(x_belief_mstr_dir) is False

    # WHEN
    fizz_world._set_world_dirs()

    # THEN
    assert fizz_world._world_dir == x_world_dir
    assert fizz_world._syntax_otz_dir == x_syntax_otz_dir
    assert not fizz_world._input_dir
    assert fizz_world._brick_dir == x_brick_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_syntax_otz_dir)
    assert os_path_exists(x_input_dir) is False
    assert os_path_exists(x_brick_dir)
    assert os_path_exists(x_belief_mstr_dir)


def test_worldunit_shop_ReturnsObj_Scenario0_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    worlds2_dir = create_path(worlds_dir(), "worlds2")
    example_input_dir = create_path(worlds_dir(), "example_input")
    output_dir = create_path(worlds_dir(), "output")
    five_world_name = "five"
    world2_time_pnigh = 55
    world2_beliefunits = {"amy45"}

    # WHEN
    x_world = worldunit_shop(
        world_name=five_world_name,
        worlds_dir=worlds2_dir,
        output_dir=output_dir,
        input_dir=example_input_dir,
        world_time_pnigh=world2_time_pnigh,
        _beliefunits=world2_beliefunits,
    )

    # THEN
    world_dir = create_path(worlds2_dir, x_world.world_name)
    assert x_world.world_name == five_world_name
    assert x_world.worlds_dir == worlds2_dir
    assert x_world.output_dir == output_dir
    assert x_world._input_dir == example_input_dir
    assert x_world.world_time_pnigh == world2_time_pnigh
    assert x_world._events == {}
    assert x_world._syntax_otz_dir == create_path(world_dir, "syntax_otz")
    assert x_world._beliefunits == world2_beliefunits
    assert x_world._pidgin_events == {}


def test_worldunit_shop_ReturnsObj_Scenario1_WithoutParameters(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    x_world = worldunit_shop(a23_str, worlds_dir())

    # THEN
    world_dir = create_path(worlds_dir(), x_world.world_name)
    assert x_world.world_name == a23_str
    assert x_world.worlds_dir == worlds_dir()
    assert not x_world.output_dir
    assert x_world.world_time_pnigh == 0
    assert x_world._events == {}
    assert x_world._input_dir == create_path(x_world._world_dir, "input")
    assert x_world._syntax_otz_dir == create_path(world_dir, "syntax_otz")
    assert x_world._beliefunits == set()


def test_worldunit_shop_ReturnsObj_Scenario2_ThirdParameterIs_output_dir(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    output_dir = create_path(worlds_dir(), "output")

    # WHEN
    x_world = worldunit_shop(a23_str, worlds_dir(), output_dir)

    # THEN
    assert x_world.world_name == a23_str
    assert x_world.worlds_dir == worlds_dir()
    assert x_world.output_dir == output_dir


def test_init_beliefunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = worlds_dir()

    # WHEN
    x_beliefunits = init_beliefunits_from_dirs([])

    # THEN
    assert x_beliefunits == []


def test_WorldUnit_set_event_SetsAttr_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop("amy23", worlds_dir())
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
    x_world = worldunit_shop("amy23", worlds_dir())
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_world.event_exists(e5_event_int) is False

    # WHEN
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world.event_exists(e5_event_int)


def test_WorldUnit_get_event_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop("amy23", worlds_dir())
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_world.get_event(e5_event_int) is None

    # WHEN
    x_world.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_world.get_event(e5_event_int) == e5_face_name


def test_WorldUnit_get_db_path_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    a23_world = worldunit_shop("amy23", worlds_dir())

    # WHEN
    a23_db_path = a23_world.get_db_path()

    assert a23_db_path == create_path(a23_world._world_dir, "world.db")
