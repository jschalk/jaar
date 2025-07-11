from os.path import exists as os_path_exists
from src.a01_term_logic.rope import create_rope
from src.a05_plan_logic.plan import get_default_belief_label as root_label
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
)
from src.a12_hub_toolbox.a12_path import create_keep_duty_path, create_treasury_db_path
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.keep_tool import (
    create_treasury_db_file,
    save_duty_believer,
    treasury_db_file_exists,
)
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_toolbox.test._util.example_hub_atoms import (
    get_texas_hubunit,
    get_texas_rope,
)


def test_HubUnit_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    belief_mstr_dir = env_dir()
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_believer = get_believerunit_with_4_levels()
    bob_believer.set_believer_name(bob_str)
    assert sue_hubunit.duty_file_exists(bob_str) is False

    # WHEN
    save_duty_believer(
        belief_mstr_dir, sue_str, a23_str, texas_rope, None, bob_believer
    )

    # THEN
    assert sue_hubunit.duty_file_exists(bob_str)


def test_HubUnit_get_duty_believer_PopensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    mstr_dir = env_dir()
    sue_hubunit = hubunit_shop(mstr_dir, a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_believer = get_believerunit_with_4_levels()
    bob_believer.set_believer_name(bob_str)
    save_duty_believer(
        belief_mstr_dir=mstr_dir,
        believer_name=sue_str,
        belief_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_believer=bob_believer,
    )

    # WHEN / THEN
    assert sue_hubunit.get_duty_believer(bob_str).get_dict() == bob_believer.get_dict()


def test_HubUnit_delete_duty_file_DeletesBelieverFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_rope = get_texas_rope()
    texas_hubunit = get_texas_hubunit()
    sue_believer = get_believerunit_with_4_levels()
    sue_str = sue_believer.believer_name
    save_duty_believer(
        belief_mstr_dir=texas_hubunit.belief_mstr_dir,
        believer_name=texas_hubunit.believer_name,
        belief_label=texas_hubunit.belief_label,
        keep_rope=texas_rope,
        knot=None,
        duty_believer=sue_believer,
    )
    sue_keep_duty_path = create_keep_duty_path(
        belief_mstr_dir=texas_hubunit.belief_mstr_dir,
        believer_name=texas_hubunit.believer_name,
        belief_label=texas_hubunit.belief_label,
        keep_rope=texas_rope,
        knot=None,
        duty_believer=sue_believer,
    )
    print(f"{sue_keep_duty_path=}")
    assert texas_hubunit.duty_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_duty_file(sue_str)

    # THEN
    assert texas_hubunit.duty_file_exists(sue_str) is False


def test_HubUnit_save_vision_believer_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_believer = get_believerunit_with_4_levels()
    bob_believer.set_believer_name(bob_str)
    assert sue_hubunit.vision_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_vision_believer(bob_believer)

    # THEN
    assert sue_hubunit.vision_file_exists(bob_str)


def test_HubUnit_vision_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_believer = get_believerunit_with_4_levels()
    bob_believer.set_believer_name(bob_str)
    assert sue_hubunit.vision_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_vision_believer(bob_believer)

    # THEN
    assert sue_hubunit.vision_file_exists(bob_str)


def test_HubUnit_get_vision_believer_PopensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_believer = get_believerunit_with_4_levels()
    bob_believer.set_believer_name(bob_str)
    sue_hubunit.save_vision_believer(bob_believer)

    # WHEN / THEN
    assert (
        sue_hubunit.get_vision_believer(bob_str).get_dict() == bob_believer.get_dict()
    )


def test_HubUnit_get_vision_believer_ReturnsNoneIfFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"

    # WHEN / THEN
    assert sue_hubunit.get_vision_believer(bob_str) is None


def test_HubUnit_delete_vision_file_DeletesBelieverFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    sue_believer = get_believerunit_with_4_levels()
    sue_str = sue_believer.believer_name
    texas_hubunit.save_vision_believer(sue_believer)
    print(f"{texas_hubunit.vision_path(sue_str)=}")
    assert texas_hubunit.vision_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_vision_file(sue_str)

    # THEN
    assert texas_hubunit.vision_file_exists(sue_str) is False


def test_HubUnit_delete_treasury_db_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    create_treasury_db_file(
        belief_mstr_dir=texas_hubunit.belief_mstr_dir,
        believer_name=texas_hubunit.believer_name,
        belief_label=texas_hubunit.belief_label,
        keep_rope=texas_hubunit.keep_rope,
        knot=texas_hubunit.knot,
    )
    treasury_db_path = create_treasury_db_path(
        belief_mstr_dir=texas_hubunit.belief_mstr_dir,
        believer_name=texas_hubunit.believer_name,
        belief_label=texas_hubunit.belief_label,
        keep_rope=texas_hubunit.keep_rope,
        knot=texas_hubunit.knot,
    )
    print(f"before  {os_path_exists(treasury_db_path)=}")
    t0_exists = treasury_db_file_exists(
        belief_mstr_dir=texas_hubunit.belief_mstr_dir,
        believer_name=texas_hubunit.believer_name,
        belief_label=texas_hubunit.belief_label,
        keep_rope=texas_hubunit.keep_rope,
        knot=texas_hubunit.knot,
    )
    assert t0_exists

    # WHEN
    texas_hubunit.delete_treasury_db_file()

    # THEN
    t1_exists = treasury_db_file_exists(
        belief_mstr_dir=texas_hubunit.belief_mstr_dir,
        believer_name=texas_hubunit.believer_name,
        belief_label=texas_hubunit.belief_label,
        keep_rope=texas_hubunit.keep_rope,
        knot=texas_hubunit.knot,
    )
    assert t1_exists is False
