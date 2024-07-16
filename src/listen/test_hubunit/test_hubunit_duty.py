from src._road.road import (
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_worlds import get_world_with_4_levels
from src.listen.examples.listen_env import (
    get_texas_hubunit,
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_HubUnit_create_econ_dir_if_missing_CreatesDirectory(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    assert os_path_exists(sue_hubunit.econ_dir()) is False

    # WHEN
    sue_hubunit.create_econ_dir_if_missing()

    # THEN
    assert os_path_exists(sue_hubunit.econ_dir())


def test_HubUnit_save_duty_world_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_world = get_world_with_4_levels()
    bob_world.set_owner_id(bob_text)
    assert sue_hubunit.duty_file_exists(bob_text) is False

    # WHEN
    sue_hubunit.save_duty_world(bob_world)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_text)


def test_HubUnit_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_world = get_world_with_4_levels()
    bob_world.set_owner_id(bob_text)
    assert sue_hubunit.duty_file_exists(bob_text) is False

    # WHEN
    sue_hubunit.save_duty_world(bob_world)

    # THEN
    assert sue_hubunit.duty_file_exists(bob_text)


def test_HubUnit_get_duty_world_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_world = get_world_with_4_levels()
    bob_world.set_owner_id(bob_text)
    sue_hubunit.save_duty_world(bob_world)

    # WHEN / THEN
    assert sue_hubunit.get_duty_world(bob_text).get_dict() == bob_world.get_dict()


def test_HubUnit_delete_duty_file_DeletesWorldFile(env_dir_setup_cleanup):
    # GIVEN
    texas_hubunit = get_texas_hubunit()
    sue_world = get_world_with_4_levels()
    sue_text = sue_world._owner_id
    texas_hubunit.save_duty_world(sue_world)
    print(f"{texas_hubunit.duty_path(sue_text)=}")
    duty_path = texas_hubunit.duty_path(sue_text)
    assert texas_hubunit.duty_file_exists(sue_text)

    # WHEN
    texas_hubunit.delete_duty_file(sue_text)

    # THEN
    assert texas_hubunit.duty_file_exists(sue_text) is False


def test_HubUnit_save_job_world_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_world = get_world_with_4_levels()
    bob_world.set_owner_id(bob_text)
    assert sue_hubunit.job_file_exists(bob_text) is False

    # WHEN
    sue_hubunit.save_job_world(bob_world)

    # THEN
    assert sue_hubunit.job_file_exists(bob_text)


def test_HubUnit_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_world = get_world_with_4_levels()
    bob_world.set_owner_id(bob_text)
    assert sue_hubunit.job_file_exists(bob_text) is False

    # WHEN
    sue_hubunit.save_job_world(bob_world)

    # THEN
    assert sue_hubunit.job_file_exists(bob_text)


def test_HubUnit_get_job_world_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_world = get_world_with_4_levels()
    bob_world.set_owner_id(bob_text)
    sue_hubunit.save_job_world(bob_world)

    # WHEN / THEN
    assert sue_hubunit.get_job_world(bob_text).get_dict() == bob_world.get_dict()


def test_HubUnit_get_job_world_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"

    # WHEN / THEN
    assert sue_hubunit.get_job_world(bob_text) is None


def test_HubUnit_delete_job_file_DeletesWorldFile(env_dir_setup_cleanup):
    # GIVEN
    texas_hubunit = get_texas_hubunit()
    sue_world = get_world_with_4_levels()
    sue_text = sue_world._owner_id
    texas_hubunit.save_job_world(sue_world)
    print(f"{texas_hubunit.job_path(sue_text)=}")
    assert texas_hubunit.job_file_exists(sue_text)

    # WHEN
    texas_hubunit.delete_job_file(sue_text)

    # THEN
    assert texas_hubunit.job_file_exists(sue_text) is False


def test_HubUnit_delete_treasury_db_file_DeletesFile(env_dir_setup_cleanup):
    # GIVEN
    texas_hubunit = get_texas_hubunit()
    texas_hubunit.create_treasury_db_file()
    assert texas_hubunit.treasury_db_file_exists()

    # WHEN
    texas_hubunit.delete_treasury_db_file()

    # THEN
    assert texas_hubunit.treasury_db_file_exists() is False
