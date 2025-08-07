from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
)
from src.a12_hub_toolbox.hub_tool import save_job_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)


def test_HubUnit_get_perspective_believer_ReturnsBelieverWith_believer_nameSetToHubUnit_believer_name():
    # ESTABLISH
    bob_str = "Bob"
    bob_believerunit = get_believerunit_with_4_levels()
    bob_believerunit.set_believer_name(bob_str)
    a23_str = "amy23"

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_believerunit = sue_hubunit.get_perspective_believer(bob_believerunit)

    # THEN
    assert perspective_believerunit.to_dict() != bob_believerunit.to_dict()
    assert perspective_believerunit.believer_name == sue_str
    perspective_believerunit.set_believer_name(bob_str)
    assert perspective_believerunit.to_dict() == bob_believerunit.to_dict()


def test_HubUnit_get_dw_perspective_believer_ReturnsBelieverWith_believer_nameSetToHubUnit_believer_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    a23_str = "amy23"
    bob_believerunit = get_believerunit_with_4_levels()
    bob_believerunit.set_believer_name(bob_str)
    bob_hubunit = hubunit_shop(env_dir(), a23_str, bob_str)
    save_job_file(bob_hubunit.belief_mstr_dir, bob_believerunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_believerunit = sue_hubunit.get_dw_perspective_believer(bob_str)

    # THEN
    assert perspective_believerunit.believer_name == sue_str
    assert perspective_believerunit.to_dict() != bob_believerunit.to_dict()
    perspective_believerunit.set_believer_name(bob_str)
    assert perspective_believerunit.to_dict() == bob_believerunit.to_dict()


def test_HubUnit_rj_perspective_believer_ReturnsBelieverWith_believer_nameSetToHubUnit_believer_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope("amy23", nation_str)
    iowa_rope = create_rope(nation_rope, "Iowa")
    a23_str = "amy23"

    bob_str = "Bob"
    yao_str = "Yao"
    yao_believerunit = get_believerunit_with_4_levels()
    yao_believerunit.set_believer_name(yao_str)

    bob_iowa_hubunit = hubunit_shop(env_dir(), a23_str, bob_str, iowa_rope)
    bob_iowa_hubunit.save_vision_believer(yao_believerunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, iowa_rope)

    # WHEN
    perspective_believerunit = sue_hubunit.rj_perspective_believer(bob_str, yao_str)

    # THEN
    assert perspective_believerunit.believer_name == sue_str
    assert perspective_believerunit.to_dict() != yao_believerunit.to_dict()
    perspective_believerunit.set_believer_name(yao_str)
    assert perspective_believerunit.to_dict() == yao_believerunit.to_dict()
