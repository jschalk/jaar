from src._road.road import (
    create_road,
    get_default_pecun_id_roadnode as root_label,
)
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.listen.examples.listen_env import (
    get_texas_hubunit,
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_HubUnit_create_econ_dir_if_missing_CreatesDirectory(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    assert os_path_exists(sue_hubunit.econ_dir()) is False

    # WHEN
    sue_hubunit.create_econ_dir_if_missing()

    # THEN
    assert os_path_exists(sue_hubunit.econ_dir())


def test_HubUnit_save_duty_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_id(bob_str)
    assert sue_hubunit.duty_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_duty_bud(bob_bud)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_str)


def test_HubUnit_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_id(bob_str)
    assert sue_hubunit.duty_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_duty_bud(bob_bud)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_str)


def test_HubUnit_get_duty_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_id(bob_str)
    sue_hubunit.save_duty_bud(bob_bud)

    # WHEN / THEN
    assert sue_hubunit.get_duty_bud(bob_str).get_dict() == bob_bud.get_dict()


def test_HubUnit_delete_duty_file_DeletesBudFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    sue_bud = get_budunit_with_4_levels()
    sue_str = sue_bud._owner_id
    texas_hubunit.save_duty_bud(sue_bud)
    print(f"{texas_hubunit.duty_path(sue_str)=}")
    duty_path = texas_hubunit.duty_path(sue_str)
    assert texas_hubunit.duty_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_duty_file(sue_str)

    # THEN
    assert texas_hubunit.duty_file_exists(sue_str) is False


def test_HubUnit_save_job_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_id(bob_str)
    assert sue_hubunit.job_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_job_bud(bob_bud)

    # THEN
    assert sue_hubunit.job_file_exists(bob_str)


def test_HubUnit_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_id(bob_str)
    assert sue_hubunit.job_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_job_bud(bob_bud)

    # THEN
    assert sue_hubunit.job_file_exists(bob_str)


def test_HubUnit_get_job_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    bob_str = "Bob"
    bob_bud = get_budunit_with_4_levels()
    bob_bud.set_owner_id(bob_str)
    sue_hubunit.save_job_bud(bob_bud)

    # WHEN / THEN
    assert sue_hubunit.get_job_bud(bob_str).get_dict() == bob_bud.get_dict()


def test_HubUnit_get_job_bud_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    bob_str = "Bob"

    # WHEN / THEN
    assert sue_hubunit.get_job_bud(bob_str) is None


def test_HubUnit_delete_job_file_DeletesBudFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    sue_bud = get_budunit_with_4_levels()
    sue_str = sue_bud._owner_id
    texas_hubunit.save_job_bud(sue_bud)
    print(f"{texas_hubunit.job_path(sue_str)=}")
    assert texas_hubunit.job_file_exists(sue_str)

    # WHEN
    texas_hubunit.delete_job_file(sue_str)

    # THEN
    assert texas_hubunit.job_file_exists(sue_str) is False


def test_HubUnit_delete_treasury_db_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    texas_hubunit = get_texas_hubunit()
    texas_hubunit.create_treasury_db_file()
    assert texas_hubunit.treasury_db_file_exists()

    # WHEN
    texas_hubunit.delete_treasury_db_file()

    # THEN
    assert texas_hubunit.treasury_db_file_exists() is False
