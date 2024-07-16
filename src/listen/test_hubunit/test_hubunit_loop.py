from src._road.jaar_config import get_test_real_id as real_id
from src._road.road import create_road
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_worlds import get_world_with_4_levels
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_HubUnit_get_perspective_world_ReturnsWorldWith_owner_idSetToHubUnit_owner_id():
    # GIVEN
    bob_text = "Bob"
    bob_worldunit = get_world_with_4_levels()
    bob_worldunit.set_owner_id(bob_text)

    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_worldunit = sue_hubunit.get_perspective_world(bob_worldunit)

    # THEN
    assert perspective_worldunit.get_dict() != bob_worldunit.get_dict()
    assert perspective_worldunit._owner_id == sue_text
    perspective_worldunit.set_owner_id(bob_text)
    assert perspective_worldunit.get_dict() == bob_worldunit.get_dict()


def test_HubUnit_get_dw_perspective_world_ReturnsWorldWith_owner_idSetToHubUnit_owner_id(
    env_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    bob_worldunit = get_world_with_4_levels()
    bob_worldunit.set_owner_id(bob_text)
    bob_hubunit = hubunit_shop(env_dir(), real_id(), bob_text)
    bob_hubunit.save_action_world(bob_worldunit)

    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_worldunit = sue_hubunit.get_dw_perspective_world(bob_text)

    # THEN
    assert perspective_worldunit._owner_id == sue_text
    assert perspective_worldunit.get_dict() != bob_worldunit.get_dict()
    perspective_worldunit.set_owner_id(bob_text)
    assert perspective_worldunit.get_dict() == bob_worldunit.get_dict()


def test_HubUnit_rj_perspective_world_ReturnsWorldWith_owner_idSetToHubUnit_owner_id(
    env_dir_setup_cleanup,
):
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")

    bob_text = "Bob"
    yao_text = "Yao"
    yao_worldunit = get_world_with_4_levels()
    yao_worldunit.set_owner_id(yao_text)

    bob_iowa_hubunit = hubunit_shop(env_dir(), real_id(), bob_text, iowa_road)
    bob_iowa_hubunit.save_job_world(yao_worldunit)

    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, iowa_road)

    # WHEN
    perspective_worldunit = sue_hubunit.rj_perspective_world(bob_text, yao_text)

    # THEN
    assert perspective_worldunit._owner_id == sue_text
    assert perspective_worldunit.get_dict() != yao_worldunit.get_dict()
    perspective_worldunit.set_owner_id(yao_text)
    assert perspective_worldunit.get_dict() == yao_worldunit.get_dict()
