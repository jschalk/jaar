from src._road.jaar_config import get_test_pecun_id as pecun_id
from src._road.road import create_road
from src.hear.hubunit import hubunit_shop
from src.hear.examples.example_hear_buds import get_budunit_with_4_levels
from src.hear.examples.hear_env import (
    env_dir_setup_cleanup,
    get_hear_temp_env_dir as env_dir,
)


def test_HubUnit_get_perspective_bud_ReturnsBudWith_owner_idSetToHubUnit_owner_id():
    # ESTABLISH
    bob_str = "Bob"
    bob_budunit = get_budunit_with_4_levels()
    bob_budunit.set_owner_id(bob_str)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), pecun_id(), sue_str)

    # WHEN
    perspective_budunit = sue_hubunit.get_perspective_bud(bob_budunit)

    # THEN
    assert perspective_budunit.get_dict() != bob_budunit.get_dict()
    assert perspective_budunit._owner_id == sue_str
    perspective_budunit.set_owner_id(bob_str)
    assert perspective_budunit.get_dict() == bob_budunit.get_dict()


def test_HubUnit_get_dw_perspective_bud_ReturnsBudWith_owner_idSetToHubUnit_owner_id(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    bob_budunit = get_budunit_with_4_levels()
    bob_budunit.set_owner_id(bob_str)
    bob_hubunit = hubunit_shop(env_dir(), pecun_id(), bob_str)
    bob_hubunit.save_action_bud(bob_budunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), pecun_id(), sue_str)

    # WHEN
    perspective_budunit = sue_hubunit.get_dw_perspective_bud(bob_str)

    # THEN
    assert perspective_budunit._owner_id == sue_str
    assert perspective_budunit.get_dict() != bob_budunit.get_dict()
    perspective_budunit.set_owner_id(bob_str)
    assert perspective_budunit.get_dict() == bob_budunit.get_dict()


def test_HubUnit_rj_perspective_bud_ReturnsBudWith_owner_idSetToHubUnit_owner_id(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(pecun_id(), nation_str)
    iowa_road = create_road(nation_road, "Iowa")

    bob_str = "Bob"
    yao_str = "Yao"
    yao_budunit = get_budunit_with_4_levels()
    yao_budunit.set_owner_id(yao_str)

    bob_iowa_hubunit = hubunit_shop(env_dir(), pecun_id(), bob_str, iowa_road)
    bob_iowa_hubunit.save_job_bud(yao_budunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), pecun_id(), sue_str, iowa_road)

    # WHEN
    perspective_budunit = sue_hubunit.rj_perspective_bud(bob_str, yao_str)

    # THEN
    assert perspective_budunit._owner_id == sue_str
    assert perspective_budunit.get_dict() != yao_budunit.get_dict()
    perspective_budunit.set_owner_id(yao_str)
    assert perspective_budunit.get_dict() == yao_budunit.get_dict()
