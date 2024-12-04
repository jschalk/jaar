from src.f00_instrument.file import create_path
from src.f01_road.finance_tran import timeconversion_shop
from src.f10_world.world import worldunit_shop
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup


def test_WorldUnit_get_dict_ReturnsObj_Scenario0MinimalParameters():
    # ESTABLISH
    worlds2_dir = create_path(get_test_worlds_dir(), "worlds2")
    five_world_id = "five"
    x_world = worldunit_shop(five_world_id, worlds2_dir)

    # WHEN
    x_world_dict = x_world.get_dict()

    # THEN
    assert x_world_dict
    assert set(x_world_dict.keys()) == {
        "world_id",
        "current_time",
        "timeconversions",
        "events",
        "pidgins",
    }
    assert x_world_dict.get("world_id") == five_world_id
    assert x_world_dict.get("current_time") == 0
    assert x_world_dict.get("timeconversions") == {}
    assert x_world_dict.get("events") == {}
    assert x_world_dict.get("pidgins") == {}


def test_WorldUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    worlds2_dir = create_path(get_test_worlds_dir(), "worlds2")
    five_world_id = "five"
    world2_current_time = 55
    music_text = "music45"
    world2_pidgins = {"Sue", "Bob"}
    world2_timeconversions = {music_text: timeconversion_shop(music_text)}
    world2_fiscalunits = {"music45"}
    x_world = worldunit_shop(
        five_world_id,
        worlds2_dir,
        world2_current_time,
        world2_timeconversions,
        world2_pidgins,
        world2_fiscalunits,
    )

    # WHEN
    x_world_dict = x_world.get_dict()

    # THEN
    assert x_world_dict
    assert x_world_dict.get("world_id") == five_world_id
    assert x_world_dict.get("current_time") == world2_current_time
    assert x_world_dict.get("timeconversions") == world2_timeconversions
    assert x_world_dict.get("pidgins") == world2_pidgins
    assert x_world_dict.get("events") == {}
