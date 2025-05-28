from src.a01_way_logic.way import (
    create_way,
    get_default_fisc_label as root_label,
)
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic._test_util.example_listen_buds import (
    get_budunit_with_4_levels,
)
from src.a13_bud_listen_logic._test_util.example_listen_hub import get_texas_hubunit
from src.a13_bud_listen_logic._test_util.a13_env import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_HubUnit_create_keep_dir_if_missing_CreatesDirectory(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    assert os_path_exists(sue_hubunit.keep_dir()) is False

    # WHEN
    sue_hubunit.create_keep_dir_if_missing()

    # THEN
    assert os_path_exists(sue_hubunit.keep_dir())


def test_HubUnit_save_duty_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_name(bob_str)
    assert sue_hubunit.duty_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_duty_bud(bob_bud)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_str)


def test_HubUnit_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_name(bob_str)
    assert sue_hubunit.duty_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_duty_bud(bob_bud)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_str)


def test_HubUnit_get_duty_bud_PopensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_name(bob_str)
    sue_hubunit.save_duty_bud(bob_bud)

    # WHEN / THEN
    assert sue_hubunit.get_duty_bud(bob_str).get_dict() == bob_bud.get_dict()


def test_HubUnit_delete_duty_file_DeletesBudFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    sue_bud = get_budunit_with_4_levels()
    sue_str = sue_bud.owner_name
    texas_hubunit.save_duty_bud(sue_bud)
    print(f"{texas_hubunit.duty_path(sue_str)=}")
    duty_path = texas_hubunit.duty_path(sue_str)
    assert texas_hubunit.duty_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_duty_file(sue_str)

    # THEN
    assert texas_hubunit.duty_file_exists(sue_str) is False


def test_HubUnit_save_plan_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_name(bob_str)
    assert sue_hubunit.plan_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_plan_bud(bob_bud)

    # THEN
    assert sue_hubunit.plan_file_exists(bob_str)


def test_HubUnit_plan_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_name(bob_str)
    assert sue_hubunit.plan_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_plan_bud(bob_bud)

    # THEN
    assert sue_hubunit.plan_file_exists(bob_str)


def test_HubUnit_get_plan_bud_PopensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_name(bob_str)
    sue_hubunit.save_plan_bud(bob_bud)

    # WHEN / THEN
    assert sue_hubunit.get_plan_bud(bob_str).get_dict() == bob_bud.get_dict()


def test_HubUnit_get_plan_bud_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_way)
    bob_str = "Bob"

    # WHEN / THEN
    assert sue_hubunit.get_plan_bud(bob_str) is None


def test_HubUnit_delete_plan_file_DeletesBudFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    sue_bud = get_budunit_with_4_levels()
    sue_str = sue_bud.owner_name
    texas_hubunit.save_plan_bud(sue_bud)
    print(f"{texas_hubunit.plan_path(sue_str)=}")
    assert texas_hubunit.plan_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_plan_file(sue_str)

    # THEN
    assert texas_hubunit.plan_file_exists(sue_str) is False


def test_HubUnit_delete_treasury_db_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    texas_hubunit.create_treasury_db_file()
    assert texas_hubunit.treasury_db_file_exists()

    # WHEN
    texas_hubunit.delete_treasury_db_file()

    # THEN
    assert texas_hubunit.treasury_db_file_exists() is False
