from src.f01_road.finance_tran import timeconversion_shop
from src.f10_world.world import (
    init_fiscalunits_from_dirs,
    WorldUnit,
    worldunit_shop,
)
from src.f10_world.examples.world_env import (
    get_test_world_id,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_WorldUnit_Exists():
    # ESTABLISH / WHEN
    x_world = WorldUnit()

    # THEN
    assert x_world.world_id is None
    assert x_world.worlds_dir is None
    assert x_world.current_time is None
    assert x_world.timeconversions is None


def test_worldunit_shop_ReturnsObj_WithParameters():
    # ESTABLISH
    worlds2_dir = f"{get_test_worlds_dir()}/worlds2"
    five_world_id = "five"
    world2_current_time = 55
    music_text = "music45"
    world2_timeconversions = {music_text: timeconversion_shop(music_text)}

    # WHEN
    x_world = worldunit_shop(
        five_world_id, worlds2_dir, world2_current_time, world2_timeconversions
    )

    # THEN
    assert x_world.world_id == five_world_id
    assert x_world.worlds_dir == worlds2_dir
    assert x_world.current_time == world2_current_time
    assert x_world.timeconversions == world2_timeconversions


def test_worldunit_shop_ReturnsObj_WithoutParameters():
    # ESTABLISH / WHEN
    x_world = worldunit_shop()

    # THEN
    assert x_world.world_id == get_test_world_id()
    assert x_world.worlds_dir == get_test_worlds_dir()
    assert x_world.current_time == 0
    assert x_world.timeconversions == {}


def test_init_fiscalunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_worlds_dir()

    # WHEN
    x_fiscalunits = init_fiscalunits_from_dirs([])

    # THEN
    assert x_fiscalunits == []
