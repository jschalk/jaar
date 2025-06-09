from src.a00_data_toolbox.file_toolbox import create_path
from src.a19_world_logic._test_util.a19_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a19_world_logic.world import worldunit_shop


def test_WorldUnit_get_dict_ReturnsObj_Scenario0MinimalParameters():
    # ESTABLISH
    worlds2_dir = create_path(get_module_temp_dir(), "worlds2")
    five_world_id = "five"
    x_world = worldunit_shop(five_world_id, worlds2_dir)

    # WHEN
    x_world_dict = x_world.get_dict()

    # THEN
    assert x_world_dict
    assert set(x_world_dict.keys()) == {
        "world_id",
        "world_time_pnigh",
    }
    assert x_world_dict.get("world_id") == five_world_id
    assert x_world_dict.get("world_time_pnigh") == 0


def test_WorldUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    worlds2_dir = create_path(get_module_temp_dir(), "worlds2")
    five_world_id = "five"
    world2_time_pnigh = 55
    accord45_str = "accord45"
    world2_vowunits = {"accord45"}
    x_world = worldunit_shop(
        world_id=five_world_id,
        worlds_dir=worlds2_dir,
        world_time_pnigh=world2_time_pnigh,
        _vowunits=world2_vowunits,
    )

    # WHEN
    x_world_dict = x_world.get_dict()

    # THEN
    assert x_world_dict
    assert x_world_dict.get("world_id") == five_world_id
    assert x_world_dict.get("world_time_pnigh") == world2_time_pnigh
