from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import create_path, save_file
from src.ch20_world_logic.test._util.ch20_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as worlds_dir,
)
from src.ch20_world_logic.world import (
    WorldName,
    WorldUnit,
    init_momentunits_from_dirs,
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
    assert not x_world.world_time_reason_upper
    assert not x_world._events
    assert not x_world._world_dir
    assert not x_world._input_dir
    assert not x_world._brick_dir
    assert not x_world._moment_mstr_dir
    assert not x_world._momentunits
    assert not x_world._translate_events


def test_WorldUnit_set_input_dir_SetsDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fay_world = WorldUnit("Fay")
    x_example_dir = create_path(worlds_dir(), "example_dir")
    x_input_dir = create_path(x_example_dir, "input")

    assert not fay_world._world_dir
    assert not fay_world._input_dir
    assert not fay_world._brick_dir
    assert not fay_world._moment_mstr_dir
    assert os_path_exists(x_input_dir) is False

    # WHEN
    fay_world.set_input_dir(x_input_dir)

    # THEN
    assert not fay_world._world_dir
    assert fay_world._input_dir == x_input_dir
    assert not fay_world._brick_dir
    assert not fay_world._moment_mstr_dir
    assert os_path_exists(x_input_dir)


def test_WorldUnit_set_world_dirs_SetsDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fay_str = "Fay"
    fay_world = WorldUnit(world_name=fay_str, worlds_dir=worlds_dir())
    x_world_dir = create_path(worlds_dir(), fay_str)
    x_input_dir = create_path(x_world_dir, "input")
    x_brick_dir = create_path(x_world_dir, "brick")
    x_moment_mstr_dir = create_path(x_world_dir, "moment_mstr")

    assert not fay_world._world_dir
    assert not fay_world._input_dir
    assert not fay_world._brick_dir
    assert not fay_world._moment_mstr_dir
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_input_dir) is False
    assert os_path_exists(x_brick_dir) is False
    assert os_path_exists(x_moment_mstr_dir) is False

    # WHEN
    fay_world._set_world_dirs()

    # THEN
    assert fay_world._world_dir == x_world_dir
    assert not fay_world._input_dir
    assert fay_world._brick_dir == x_brick_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_input_dir) is False
    assert os_path_exists(x_brick_dir)
    assert os_path_exists(x_moment_mstr_dir)


def test_worldunit_shop_ReturnsObj_Scenario0_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    worlds2_dir = create_path(worlds_dir(), "worlds2")
    example_input_dir = create_path(worlds_dir(), "example_input")
    output_dir = create_path(worlds_dir(), "output")
    five_world_name = "five"
    world2_time_reason_upper = 55
    world2_momentunits = {"amy45"}

    # WHEN
    x_world = worldunit_shop(
        world_name=five_world_name,
        worlds_dir=worlds2_dir,
        output_dir=output_dir,
        input_dir=example_input_dir,
        world_time_reason_upper=world2_time_reason_upper,
        _momentunits=world2_momentunits,
    )

    # THEN
    world_dir = create_path(worlds2_dir, x_world.world_name)
    assert x_world.world_name == five_world_name
    assert x_world.worlds_dir == worlds2_dir
    assert x_world.output_dir == output_dir
    assert x_world._input_dir == example_input_dir
    assert x_world.world_time_reason_upper == world2_time_reason_upper
    assert x_world._events == {}
    assert x_world._momentunits == world2_momentunits
    assert x_world._translate_events == {}


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
    assert x_world.world_time_reason_upper == 0
    assert x_world._events == {}
    assert x_world._input_dir == create_path(x_world._world_dir, "input")
    assert x_world._momentunits == set()


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


def test_init_momentunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = worlds_dir()

    # WHEN
    x_momentunits = init_momentunits_from_dirs([])

    # THEN
    assert x_momentunits == []


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


def test_WorldUnit_get_world_db_path_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    a23_world = worldunit_shop("amy23", worlds_dir())

    # WHEN
    a23_db_path = a23_world.get_world_db_path()

    # THEN
    assert a23_db_path == create_path(a23_world._world_dir, "world.db")


def test_WorldUnit_delete_world_db_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    a23_world = worldunit_shop("amy23", worlds_dir())
    a23_db_path = a23_world.get_world_db_path()
    print(f"{a23_db_path=}")
    save_file(a23_db_path, None, "example_text")
    assert os_path_exists(a23_db_path)

    # WHEN
    a23_world.delete_world_db()

    # THEN
    assert not os_path_exists(a23_db_path)
