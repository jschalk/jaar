from src.f10_world.world import init_fiscalunits_from_dirs
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_init_fiscalunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_worlds_dir()

    # WHEN
    x_fiscalunits = init_fiscalunits_from_dirs([])

    # THEN
    assert x_fiscalunits == []
