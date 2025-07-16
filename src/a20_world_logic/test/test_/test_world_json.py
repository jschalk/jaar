from src.a00_data_toolbox.file_toolbox import create_path
from src.a20_world_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a20_world_logic.world import worldunit_shop


def test_WorldUnit_get_dict_ReturnsObj_Scenario0MinimalParameters():
    # ESTABLISH
    worlds2_dir = create_path(get_module_temp_dir(), "worlds2")
    five_world_name = "five"
    x_world = worldunit_shop(five_world_name, worlds2_dir)

    # WHEN
    x_world_dict = x_world.get_dict()

    # THEN
    assert x_world_dict
    assert set(x_world_dict.keys()) == {
        "world_name",
        "world_time_p_upper",
    }
    assert x_world_dict.get("world_name") == five_world_name
    assert x_world_dict.get("world_time_p_upper") == 0


def test_WorldUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    worlds2_dir = create_path(get_module_temp_dir(), "worlds2")
    five_world_name = "five"
    world2_time_p_upper = 55
    amy45_str = "amy45"
    world2_beliefunits = {"amy45"}
    x_world = worldunit_shop(
        world_name=five_world_name,
        worlds_dir=worlds2_dir,
        world_time_p_upper=world2_time_p_upper,
        _beliefunits=world2_beliefunits,
    )

    # WHEN
    x_world_dict = x_world.get_dict()

    # THEN
    assert x_world_dict
    assert x_world_dict.get("world_name") == five_world_name
    assert x_world_dict.get("world_time_p_upper") == world2_time_p_upper
