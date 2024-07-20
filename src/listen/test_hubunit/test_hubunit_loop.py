from src._road.jaar_config import get_test_real_id as real_id
from src._road.road import create_road
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_HubUnit_get_perspective_bud_ReturnsBudWith_owner_idSetToHubUnit_owner_id():
    # ESTABLISH
    bob_text = "Bob"
    bob_budunit = get_budunit_with_4_levels()
    bob_budunit.set_owner_id(bob_text)

    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_budunit = sue_hubunit.get_perspective_bud(bob_budunit)

    # THEN
    assert perspective_budunit.get_dict() != bob_budunit.get_dict()
    assert perspective_budunit._owner_id == sue_text
    perspective_budunit.set_owner_id(bob_text)
    assert perspective_budunit.get_dict() == bob_budunit.get_dict()


def test_HubUnit_get_dw_perspective_bud_ReturnsBudWith_owner_idSetToHubUnit_owner_id(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_text = "Bob"
    bob_budunit = get_budunit_with_4_levels()
    bob_budunit.set_owner_id(bob_text)
    bob_hubunit = hubunit_shop(env_dir(), real_id(), bob_text)
    bob_hubunit.save_action_bud(bob_budunit)

    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_budunit = sue_hubunit.get_dw_perspective_bud(bob_text)

    # THEN
    assert perspective_budunit._owner_id == sue_text
    assert perspective_budunit.get_dict() != bob_budunit.get_dict()
    perspective_budunit.set_owner_id(bob_text)
    assert perspective_budunit.get_dict() == bob_budunit.get_dict()


def test_HubUnit_rj_perspective_bud_ReturnsBudWith_owner_idSetToHubUnit_owner_id(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")

    bob_text = "Bob"
    yao_text = "Yao"
    yao_budunit = get_budunit_with_4_levels()
    yao_budunit.set_owner_id(yao_text)

    bob_iowa_hubunit = hubunit_shop(env_dir(), real_id(), bob_text, iowa_road)
    bob_iowa_hubunit.save_job_bud(yao_budunit)

    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, iowa_road)

    # WHEN
    perspective_budunit = sue_hubunit.rj_perspective_bud(bob_text, yao_text)

    # THEN
    assert perspective_budunit._owner_id == sue_text
    assert perspective_budunit.get_dict() != yao_budunit.get_dict()
    perspective_budunit.set_owner_id(yao_text)
    assert perspective_budunit.get_dict() == yao_budunit.get_dict()
