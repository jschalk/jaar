from src.f01_road.jaar_config import get_test_fisc_title as fisc_title
from src.f01_road.road import create_road
from src.f06_listen.hub_tool import save_forecast_file, open_forecast_file
from src.f06_listen.hubunit import hubunit_shop
from src.f06_listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.f06_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_HubUnit_get_perspective_bud_ReturnsBudWith_owner_nameSetToHubUnit_owner_name():
    # ESTABLISH
    bob_str = "Bob"
    bob_budunit = get_budunit_with_4_levels()
    bob_budunit.set_owner_name(bob_str)
    a23_str = "accord23"

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_budunit = sue_hubunit.get_perspective_bud(bob_budunit)

    # THEN
    assert perspective_budunit.get_dict() != bob_budunit.get_dict()
    assert perspective_budunit.owner_name == sue_str
    perspective_budunit.set_owner_name(bob_str)
    assert perspective_budunit.get_dict() == bob_budunit.get_dict()


def test_HubUnit_get_dw_perspective_bud_ReturnsBudWith_owner_nameSetToHubUnit_owner_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    a23_str = "accord23"
    bob_budunit = get_budunit_with_4_levels()
    bob_budunit.set_owner_name(bob_str)
    bob_hubunit = hubunit_shop(env_dir(), a23_str, bob_str)
    save_forecast_file(bob_hubunit.fisc_mstr_dir, bob_budunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_budunit = sue_hubunit.get_dw_perspective_bud(bob_str)

    # THEN
    assert perspective_budunit.owner_name == sue_str
    assert perspective_budunit.get_dict() != bob_budunit.get_dict()
    perspective_budunit.set_owner_name(bob_str)
    assert perspective_budunit.get_dict() == bob_budunit.get_dict()


def test_HubUnit_rj_perspective_bud_ReturnsBudWith_owner_nameSetToHubUnit_owner_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(fisc_title(), nation_str)
    iowa_road = create_road(nation_road, "Iowa")
    a23_str = "accord23"

    bob_str = "Bob"
    yao_str = "Yao"
    yao_budunit = get_budunit_with_4_levels()
    yao_budunit.set_owner_name(yao_str)

    bob_iowa_hubunit = hubunit_shop(env_dir(), a23_str, bob_str, iowa_road)
    bob_iowa_hubunit.save_job_bud(yao_budunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, iowa_road)

    # WHEN
    perspective_budunit = sue_hubunit.rj_perspective_bud(bob_str, yao_str)

    # THEN
    assert perspective_budunit.owner_name == sue_str
    assert perspective_budunit.get_dict() != yao_budunit.get_dict()
    perspective_budunit.set_owner_name(yao_str)
    assert perspective_budunit.get_dict() == yao_budunit.get_dict()
