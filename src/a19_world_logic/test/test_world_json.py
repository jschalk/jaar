from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic.deal import timeconversion_shop
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)


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
        "timeconversions",
    }
    assert x_world_dict.get("world_id") == five_world_id
    assert x_world_dict.get("world_time_pnigh") == 0
    assert x_world_dict.get("timeconversions") == {}


def test_WorldUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    worlds2_dir = create_path(get_module_temp_dir(), "worlds2")
    five_world_id = "five"
    world2_time_pnigh = 55
    accord45_str = "accord45"
    world2_timeconversions = {accord45_str: timeconversion_shop(accord45_str)}
    world2_fiscunits = {"accord45"}
    x_world = worldunit_shop(
        world_id=five_world_id,
        worlds_dir=worlds2_dir,
        world_time_pnigh=world2_time_pnigh,
        timeconversions=world2_timeconversions,
        _fiscunits=world2_fiscunits,
    )

    # WHEN
    x_world_dict = x_world.get_dict()

    # THEN
    assert x_world_dict
    assert x_world_dict.get("world_id") == five_world_id
    assert x_world_dict.get("world_time_pnigh") == world2_time_pnigh
    assert x_world_dict.get("timeconversions") == world2_timeconversions
