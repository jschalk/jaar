from src._instrument.file import delete_dir, save_file, open_file
from src._instrument.sqlite import check_connection
from src._world.healer import healerhold_shop
from src._world.idea import ideaunit_shop
from src._world.graphic import display_ideatree
from src.listen.hubunit import hubunit_shop, treasury_file_name
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
    get_texas_road,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_get_econ_roads_RaisesErrorWhen__econs_justified_IsFalse(
    env_dir_setup_cleanup,
):

    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)
    sue_hubunit.save_mind_world(sue_hubunit.default_mind_world())
    sue_mind_world = sue_hubunit.get_mind_world()
    sue_mind_world.add_charunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_mind_world.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_mind_world.make_road(texas_road, dallas_text)
    sue_mind_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_mind_world.add_idea(ideaunit_shop(dallas_text), texas_road)
    sue_mind_world.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_mind_world.edit_idea_attr(dallas_road, healerhold=healerhold_shop({sue_text}))
    sue_mind_world.calc_world_metrics()
    assert sue_mind_world._econs_justified is False
    sue_hubunit.save_mind_world(sue_mind_world)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_econ_roads()
    assert (
        str(excinfo.value)
        == f"Cannot get_econ_roads from '{sue_text}' mind world because 'WorldUnit._econs_justified' is False."
    )


def test_HubUnit_get_econ_roads_RaisesErrorWhen__econs_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)
    sue_hubunit.save_mind_world(sue_hubunit.default_mind_world())
    sue_mind_world = sue_hubunit.get_mind_world()
    sue_mind_world.add_charunit(sue_text)
    texas_text = "Tex/as"
    texas_road = sue_mind_world.make_l1_road(texas_text)
    sue_mind_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_mind_world.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_mind_world.calc_world_metrics()
    assert sue_mind_world._econs_justified
    assert sue_mind_world._econs_buildable is False
    sue_hubunit.save_mind_world(sue_mind_world)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_econ_roads()
    assert (
        str(excinfo.value)
        == f"Cannot get_econ_roads from '{sue_text}' mind world because 'WorldUnit._econs_buildable' is False."
    )


def test_HubUnit_get_econ_roads_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)
    sue_hubunit.save_mind_world(sue_hubunit.default_mind_world())
    sue_mind_world = sue_hubunit.get_mind_world()
    sue_mind_world.add_charunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_mind_world.make_l1_road(texas_text)
    sue_mind_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_mind_world.make_road(texas_road, dallas_text)
    elpaso_road = sue_mind_world.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_mind_world.add_idea(dallas_idea, texas_road)
    sue_mind_world.add_idea(elpaso_idea, texas_road)
    sue_mind_world.calc_world_metrics()
    # display_ideatree(sue_mind_world, mode="Econ").show()
    sue_hubunit.save_mind_world(sue_mind_world)

    # WHEN
    sue_econ_roads = sue_hubunit.get_econ_roads()

    # THEN
    assert len(sue_econ_roads) == 2
    assert dallas_road in sue_econ_roads
    assert elpaso_road in sue_econ_roads


def test_HubUnit_save_all_mind_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)
    sue_hubunit.save_mind_world(sue_hubunit.default_mind_world())
    sue_mind_world = sue_hubunit.get_mind_world()
    sue_mind_world.add_charunit(sue_text)
    bob_text = "Bob"
    sue_mind_world.add_charunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_mind_world.make_l1_road(texas_text)
    sue_mind_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_mind_world.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_mind_world.add_idea(dallas_idea, texas_road)
    elpaso_text = "el paso"
    elpaso_road = sue_mind_world.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_mind_world.add_idea(elpaso_idea, texas_road)
    # sue_mind_world.calc_world_metrics()
    # display_ideatree(sue_mind_world, mode="Econ").show()
    sue_hubunit.save_mind_world(sue_mind_world)
    sue_dallas_hubunit = hubunit_shop(env_dir(), None, sue_text, dallas_road)
    sue_elpaso_hubunit = hubunit_shop(env_dir(), None, sue_text, elpaso_road)
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_text)) is False
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_text)) is False
    assert sue_hubunit.econ_road is None

    # WHEN
    sue_hubunit.save_all_mind_dutys()

    # THEN
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_text))
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_text))
    assert sue_hubunit.econ_road is None


def test_HubUnit_create_treasury_db_file_CorrectlyCreatesDatabase(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)
    sue_hubunit.save_mind_world(sue_hubunit.default_mind_world())
    sue_mind_world = sue_hubunit.get_mind_world()
    texas_text = "Texas"
    texas_road = sue_mind_world.make_l1_road(texas_text)
    sue_hubunit.econ_road = texas_road
    assert os_path_exists(sue_hubunit.treasury_db_path()) is False

    # WHEN
    sue_hubunit.create_treasury_db_file()

    # THEN
    assert os_path_exists(sue_hubunit.treasury_db_path())


def test_HubUnit_create_treasury_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, get_texas_road())
    delete_dir(sue_hubunit.treasury_db_path())  # clear out any treasury.db file
    sue_hubunit.create_treasury_db_file()
    assert os_path_exists(sue_hubunit.treasury_db_path())

    # GIVEN
    x_file_text = "Texas Dallas ElPaso"
    db_file = treasury_file_name()
    save_file(
        sue_hubunit.econ_dir(),
        file_name=db_file,
        file_text=x_file_text,
        replace=True,
    )
    assert os_path_exists(sue_hubunit.treasury_db_path())
    assert open_file(sue_hubunit.econ_dir(), file_name=db_file) == x_file_text

    # WHEN
    sue_hubunit.create_treasury_db_file()
    # THEN
    assert open_file(sue_hubunit.econ_dir(), file_name=db_file) == x_file_text


def test_HubUnit_treasury_db_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)
    sue_hubunit.save_mind_world(sue_hubunit.default_mind_world())
    sue_mind_world = sue_hubunit.get_mind_world()
    texas_text = "Texas"
    texas_road = sue_mind_world.make_l1_road(texas_text)
    sue_hubunit.econ_road = texas_road
    assert sue_hubunit.treasury_db_file_exists() is False

    # WHEN
    sue_hubunit.create_treasury_db_file()

    # THEN
    assert sue_hubunit.treasury_db_file_exists()


# def test_HubUnit_treasury_db_file_conn_CreatesTreasuryDBIfDoesNotExist(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN create
#     sue_text = "Sue"
#     sue_hubunit = hubunit_shop(env_dir(), None, sue_text, get_texas_road())

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         check_connection(sue_hubunit.treasury_db_file_conn())
#     assert str(excinfo.value) == "unable to open database file"

#     # WHEN
#     sue_hubunit.create_treasury_db_file()

#     # THEN
#     assert check_connection(sue_hubunit.treasury_db_file_conn())


def test_HubUnit_treasury_db_file_conn_RaisesErrorIfMissing_econ_road(
    env_dir_setup_cleanup,
):
    # GIVEN create
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.treasury_db_file_conn()
    assert (
        str(excinfo.value)
        == f"hubunit cannot connect to treasury_db_file because econ_road is {sue_hubunit.econ_road}"
    )


def test_HubUnit_create_mind_treasury_db_files_CreatesDatabases(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, None)
    sue_hubunit.save_mind_world(sue_hubunit.default_mind_world())
    sue_mind_world = sue_hubunit.get_mind_world()
    sue_mind_world.add_charunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_mind_world.make_l1_road(texas_text)
    sue_mind_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_mind_world.make_road(texas_road, dallas_text)
    elpaso_road = sue_mind_world.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_mind_world.add_idea(dallas_idea, texas_road)
    sue_mind_world.add_idea(elpaso_idea, texas_road)
    sue_mind_world.calc_world_metrics()
    # display_ideatree(sue_mind_world, mode="Econ").show()
    sue_hubunit.save_mind_world(sue_mind_world)

    dallas_hubunit = hubunit_shop(env_dir(), None, sue_text, dallas_road)
    elpaso_hubunit = hubunit_shop(env_dir(), None, sue_text, elpaso_road)
    print(f"{dallas_hubunit.treasury_db_path()=}")
    print(f"{elpaso_hubunit.treasury_db_path()=}")
    assert os_path_exists(dallas_hubunit.treasury_db_path()) is False
    assert os_path_exists(elpaso_hubunit.treasury_db_path()) is False
    assert sue_hubunit.econ_road is None

    # WHEN
    sue_hubunit.create_mind_treasury_db_files()

    # THEN
    assert os_path_exists(dallas_hubunit.treasury_db_path())
    assert os_path_exists(elpaso_hubunit.treasury_db_path())
    assert sue_hubunit.econ_road is None
