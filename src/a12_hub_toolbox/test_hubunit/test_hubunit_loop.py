from src.a01_term_logic.way import create_way
from src.a06_plan_logic._test_util.example_plans import get_planunit_with_4_levels
from src.a12_hub_toolbox._test_util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_toolbox.hub_tool import save_job_file
from src.a12_hub_toolbox.hubunit import hubunit_shop


def test_HubUnit_get_perspective_plan_ReturnsPlanWith_owner_nameSetToHubUnit_owner_name():
    # ESTABLISH
    bob_str = "Bob"
    bob_planunit = get_planunit_with_4_levels()
    bob_planunit.set_owner_name(bob_str)
    a23_str = "accord23"

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_planunit = sue_hubunit.get_perspective_plan(bob_planunit)

    # THEN
    assert perspective_planunit.get_dict() != bob_planunit.get_dict()
    assert perspective_planunit.owner_name == sue_str
    perspective_planunit.set_owner_name(bob_str)
    assert perspective_planunit.get_dict() == bob_planunit.get_dict()


def test_HubUnit_get_dw_perspective_plan_ReturnsPlanWith_owner_nameSetToHubUnit_owner_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    a23_str = "accord23"
    bob_planunit = get_planunit_with_4_levels()
    bob_planunit.set_owner_name(bob_str)
    bob_hubunit = hubunit_shop(env_dir(), a23_str, bob_str)
    save_job_file(bob_hubunit.vow_mstr_dir, bob_planunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_planunit = sue_hubunit.get_dw_perspective_plan(bob_str)

    # THEN
    assert perspective_planunit.owner_name == sue_str
    assert perspective_planunit.get_dict() != bob_planunit.get_dict()
    perspective_planunit.set_owner_name(bob_str)
    assert perspective_planunit.get_dict() == bob_planunit.get_dict()


def test_HubUnit_rj_perspective_plan_ReturnsPlanWith_owner_nameSetToHubUnit_owner_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way("accord23", nation_str)
    iowa_way = create_way(nation_way, "Iowa")
    a23_str = "accord23"

    bob_str = "Bob"
    yao_str = "Yao"
    yao_planunit = get_planunit_with_4_levels()
    yao_planunit.set_owner_name(yao_str)

    bob_iowa_hubunit = hubunit_shop(env_dir(), a23_str, bob_str, iowa_way)
    bob_iowa_hubunit.save_vision_plan(yao_planunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, iowa_way)

    # WHEN
    perspective_planunit = sue_hubunit.rj_perspective_plan(bob_str, yao_str)

    # THEN
    assert perspective_planunit.owner_name == sue_str
    assert perspective_planunit.get_dict() != yao_planunit.get_dict()
    perspective_planunit.set_owner_name(yao_str)
    assert perspective_planunit.get_dict() == yao_planunit.get_dict()
