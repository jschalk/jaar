from src.a01_term_logic.rope import create_rope
from src.a06_owner_logic.test._util.example_owners import get_ownerunit_with_4_levels
from src.a12_hub_toolbox.hub_tool import save_job_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)


def test_HubUnit_get_perspective_owner_ReturnsOwnerWith_owner_nameSetToHubUnit_owner_name():
    # ESTABLISH
    bob_str = "Bob"
    bob_ownerunit = get_ownerunit_with_4_levels()
    bob_ownerunit.set_owner_name(bob_str)
    a23_str = "amy23"

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_ownerunit = sue_hubunit.get_perspective_owner(bob_ownerunit)

    # THEN
    assert perspective_ownerunit.get_dict() != bob_ownerunit.get_dict()
    assert perspective_ownerunit.owner_name == sue_str
    perspective_ownerunit.set_owner_name(bob_str)
    assert perspective_ownerunit.get_dict() == bob_ownerunit.get_dict()


def test_HubUnit_get_dw_perspective_owner_ReturnsOwnerWith_owner_nameSetToHubUnit_owner_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    a23_str = "amy23"
    bob_ownerunit = get_ownerunit_with_4_levels()
    bob_ownerunit.set_owner_name(bob_str)
    bob_hubunit = hubunit_shop(env_dir(), a23_str, bob_str)
    save_job_file(bob_hubunit.belief_mstr_dir, bob_ownerunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN
    perspective_ownerunit = sue_hubunit.get_dw_perspective_owner(bob_str)

    # THEN
    assert perspective_ownerunit.owner_name == sue_str
    assert perspective_ownerunit.get_dict() != bob_ownerunit.get_dict()
    perspective_ownerunit.set_owner_name(bob_str)
    assert perspective_ownerunit.get_dict() == bob_ownerunit.get_dict()


def test_HubUnit_rj_perspective_owner_ReturnsOwnerWith_owner_nameSetToHubUnit_owner_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope("amy23", nation_str)
    iowa_rope = create_rope(nation_rope, "Iowa")
    a23_str = "amy23"

    bob_str = "Bob"
    yao_str = "Yao"
    yao_ownerunit = get_ownerunit_with_4_levels()
    yao_ownerunit.set_owner_name(yao_str)

    bob_iowa_hubunit = hubunit_shop(env_dir(), a23_str, bob_str, iowa_rope)
    bob_iowa_hubunit.save_vision_owner(yao_ownerunit)

    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, iowa_rope)

    # WHEN
    perspective_ownerunit = sue_hubunit.rj_perspective_owner(bob_str, yao_str)

    # THEN
    assert perspective_ownerunit.owner_name == sue_str
    assert perspective_ownerunit.get_dict() != yao_ownerunit.get_dict()
    perspective_ownerunit.set_owner_name(yao_str)
    assert perspective_ownerunit.get_dict() == yao_ownerunit.get_dict()
