from os.path import exists as os_path_exists
from src.a01_term_logic.rope import create_rope
from src.a05_concept_logic.concept import get_default_vow_label as root_label
from src.a06_plan_logic._util.example_plans import get_planunit_with_4_levels
from src.a12_hub_toolbox._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_toolbox._util.example_hub_atoms import get_texas_hubunit
from src.a12_hub_toolbox.hubunit import hubunit_shop


def test_HubUnit_create_keep_dir_if_missing_CreatesDirectory(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    assert os_path_exists(sue_hubunit.keep_dir()) is False

    # WHEN
    sue_hubunit.create_keep_dir_if_missing()

    # THEN
    assert os_path_exists(sue_hubunit.keep_dir())


def test_HubUnit_save_duty_plan_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_owner_name(bob_str)
    assert sue_hubunit.duty_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_duty_plan(bob_plan)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_str)


def test_HubUnit_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_owner_name(bob_str)
    assert sue_hubunit.duty_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_duty_plan(bob_plan)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_str)


def test_HubUnit_get_duty_plan_PopensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_owner_name(bob_str)
    sue_hubunit.save_duty_plan(bob_plan)

    # WHEN / THEN
    assert sue_hubunit.get_duty_plan(bob_str).get_dict() == bob_plan.get_dict()


def test_HubUnit_delete_duty_file_DeletesPlanFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    sue_plan = get_planunit_with_4_levels()
    sue_str = sue_plan.owner_name
    texas_hubunit.save_duty_plan(sue_plan)
    print(f"{texas_hubunit.duty_path(sue_str)=}")
    duty_path = texas_hubunit.duty_path(sue_str)
    assert texas_hubunit.duty_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_duty_file(sue_str)

    # THEN
    assert texas_hubunit.duty_file_exists(sue_str) is False


def test_HubUnit_save_vision_plan_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_owner_name(bob_str)
    assert sue_hubunit.vision_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_vision_plan(bob_plan)

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
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_owner_name(bob_str)
    assert sue_hubunit.vision_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_vision_plan(bob_plan)

    # THEN
    assert sue_hubunit.vision_file_exists(bob_str)


def test_HubUnit_get_vision_plan_PopensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_owner_name(bob_str)
    sue_hubunit.save_vision_plan(bob_plan)

    # WHEN / THEN
    assert sue_hubunit.get_vision_plan(bob_str).get_dict() == bob_plan.get_dict()


def test_HubUnit_get_vision_plan_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"

    # WHEN / THEN
    assert sue_hubunit.get_vision_plan(bob_str) is None


def test_HubUnit_delete_vision_file_DeletesPlanFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    sue_plan = get_planunit_with_4_levels()
    sue_str = sue_plan.owner_name
    texas_hubunit.save_vision_plan(sue_plan)
    print(f"{texas_hubunit.vision_path(sue_str)=}")
    assert texas_hubunit.vision_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_vision_file(sue_str)

    # THEN
    assert texas_hubunit.vision_file_exists(sue_str) is False


def test_HubUnit_delete_treasury_db_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    texas_hubunit.create_treasury_db_file()
    treasury_db_path = texas_hubunit.treasury_db_path()
    print(f"before  {os_path_exists(treasury_db_path)=}")
    assert texas_hubunit.treasury_db_file_exists()

    # WHEN
    texas_hubunit.delete_treasury_db_file()

    # THEN
    assert texas_hubunit.treasury_db_file_exists() is False
