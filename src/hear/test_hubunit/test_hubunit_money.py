from src._instrument.file import delete_dir, save_file, open_file
from src._instrument.db_tool import check_connection
from src.bud.healer import healerlink_shop
from src.bud.idea import ideaunit_shop
from src.bud.graphic import display_ideatree
from src.hear.hubunit import hubunit_shop, treasury_file_name
from src.hear.examples.hear_env import (
    env_dir_setup_cleanup,
    get_hear_temp_env_dir as env_dir,
    get_texas_road,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_get_econ_roads_RaisesErrorWhen__econs_justified_IsFalse(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    sue_voice_bud = sue_hubunit.get_voice_bud()
    sue_voice_bud.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    dallas_str = "dallas"
    dallas_road = sue_voice_bud.make_road(texas_road, dallas_str)
    sue_voice_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    sue_voice_bud.set_idea(ideaunit_shop(dallas_str), texas_road)
    sue_voice_bud.edit_idea_attr(texas_road, healerlink=healerlink_shop({sue_str}))
    sue_voice_bud.edit_idea_attr(dallas_road, healerlink=healerlink_shop({sue_str}))
    sue_voice_bud.settle_bud()
    assert sue_voice_bud._econs_justified is False
    sue_hubunit.save_voice_bud(sue_voice_bud)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_econ_roads()
    assert (
        str(excinfo.value)
        == f"Cannot get_econ_roads from '{sue_str}' voice bud because 'BudUnit._econs_justified' is False."
    )


def test_HubUnit_get_econ_roads_RaisesErrorWhen__econs_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    sue_voice_bud = sue_hubunit.get_voice_bud()
    sue_voice_bud.add_acctunit(sue_str)
    texas_str = "Tex/as"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    sue_voice_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    sue_voice_bud.edit_idea_attr(texas_road, healerlink=healerlink_shop({sue_str}))
    sue_voice_bud.settle_bud()
    assert sue_voice_bud._econs_justified
    assert sue_voice_bud._econs_buildable is False
    sue_hubunit.save_voice_bud(sue_voice_bud)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_econ_roads()
    assert (
        str(excinfo.value)
        == f"Cannot get_econ_roads from '{sue_str}' voice bud because 'BudUnit._econs_buildable' is False."
    )


def test_HubUnit_get_econ_roads_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    sue_voice_bud = sue_hubunit.get_voice_bud()
    sue_voice_bud.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    sue_voice_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_road = sue_voice_bud.make_road(texas_road, dallas_str)
    elpaso_road = sue_voice_bud.make_road(texas_road, elpaso_str)
    dallas_idea = ideaunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_idea = ideaunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_voice_bud.set_idea(dallas_idea, texas_road)
    sue_voice_bud.set_idea(elpaso_idea, texas_road)
    sue_voice_bud.settle_bud()
    display_ideatree(sue_voice_bud, mode="Econ", graphics_bool=graphics_bool)
    sue_hubunit.save_voice_bud(sue_voice_bud)

    # WHEN
    sue_econ_roads = sue_hubunit.get_econ_roads()

    # THEN
    assert len(sue_econ_roads) == 2
    assert dallas_road in sue_econ_roads
    assert elpaso_road in sue_econ_roads


def test_HubUnit_save_all_voice_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    sue_voice_bud = sue_hubunit.get_voice_bud()
    sue_voice_bud.add_acctunit(sue_str)
    bob_str = "Bob"
    sue_voice_bud.add_acctunit(bob_str)
    texas_str = "Texas"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    sue_voice_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = sue_voice_bud.make_road(texas_road, dallas_str)
    dallas_idea = ideaunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    sue_voice_bud.set_idea(dallas_idea, texas_road)
    elpaso_str = "el paso"
    elpaso_road = sue_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_idea = ideaunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_voice_bud.set_idea(elpaso_idea, texas_road)
    display_ideatree(sue_voice_bud, mode="Econ", graphics_bool=graphics_bool)
    sue_hubunit.save_voice_bud(sue_voice_bud)
    sue_dallas_hubunit = hubunit_shop(env_dir(), None, sue_str, dallas_road)
    sue_elpaso_hubunit = hubunit_shop(env_dir(), None, sue_str, elpaso_road)
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str)) is False
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str)) is False
    assert sue_hubunit.econ_road is None

    # WHEN
    sue_hubunit.save_all_voice_dutys()

    # THEN
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str))
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str))
    assert sue_hubunit.econ_road is None


def test_HubUnit_create_treasury_db_file_CorrectlyCreatesDatabase(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    sue_voice_bud = sue_hubunit.get_voice_bud()
    texas_str = "Texas"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    sue_hubunit.econ_road = texas_road
    assert os_path_exists(sue_hubunit.treasury_db_path()) is False

    # WHEN
    sue_hubunit.create_treasury_db_file()

    # THEN
    assert os_path_exists(sue_hubunit.treasury_db_path())


def test_HubUnit_create_treasury_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH create econ
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, get_texas_road())
    delete_dir(sue_hubunit.treasury_db_path())  # clear out any treasury.db file
    sue_hubunit.create_treasury_db_file()
    assert os_path_exists(sue_hubunit.treasury_db_path())

    # ESTABLISH
    x_file_str = "Texas Dallas ElPaso"
    db_file = treasury_file_name()
    save_file(
        sue_hubunit.econ_dir(),
        file_name=db_file,
        file_str=x_file_str,
        replace=True,
    )
    assert os_path_exists(sue_hubunit.treasury_db_path())
    assert open_file(sue_hubunit.econ_dir(), file_name=db_file) == x_file_str

    # WHEN
    sue_hubunit.create_treasury_db_file()
    # THEN
    assert open_file(sue_hubunit.econ_dir(), file_name=db_file) == x_file_str


def test_HubUnit_treasury_db_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    sue_voice_bud = sue_hubunit.get_voice_bud()
    texas_str = "Texas"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    sue_hubunit.econ_road = texas_road
    assert sue_hubunit.treasury_db_file_exists() is False

    # WHEN
    sue_hubunit.create_treasury_db_file()

    # THEN
    assert sue_hubunit.treasury_db_file_exists()


# def test_HubUnit_treasury_db_file_conn_CreatesTreasuryDBIfDoesNotExist(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH create
#     sue_str = "Sue"
#     sue_hubunit = hubunit_shop(env_dir(), None, sue_str, get_texas_road())

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
    # ESTABLISH create
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.treasury_db_file_conn()
    assert (
        str(excinfo.value)
        == f"hubunit cannot connect to treasury_db_file because econ_road is {sue_hubunit.econ_road}"
    )


def test_HubUnit_create_voice_treasury_db_files_CreatesDatabases(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, None)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    sue_voice_bud = sue_hubunit.get_voice_bud()
    sue_voice_bud.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    sue_voice_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_road = sue_voice_bud.make_road(texas_road, dallas_str)
    elpaso_road = sue_voice_bud.make_road(texas_road, elpaso_str)
    dallas_idea = ideaunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_idea = ideaunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_voice_bud.set_idea(dallas_idea, texas_road)
    sue_voice_bud.set_idea(elpaso_idea, texas_road)
    sue_voice_bud.settle_bud()
    display_ideatree(sue_voice_bud, mode="Econ", graphics_bool=graphics_bool)
    sue_hubunit.save_voice_bud(sue_voice_bud)

    dallas_hubunit = hubunit_shop(env_dir(), None, sue_str, dallas_road)
    elpaso_hubunit = hubunit_shop(env_dir(), None, sue_str, elpaso_road)
    print(f"{dallas_hubunit.treasury_db_path()=}")
    print(f"{elpaso_hubunit.treasury_db_path()=}")
    assert os_path_exists(dallas_hubunit.treasury_db_path()) is False
    assert os_path_exists(elpaso_hubunit.treasury_db_path()) is False
    assert sue_hubunit.econ_road is None

    # WHEN
    sue_hubunit.create_voice_treasury_db_files()

    # THEN
    assert os_path_exists(dallas_hubunit.treasury_db_path())
    assert os_path_exists(elpaso_hubunit.treasury_db_path())
    assert sue_hubunit.econ_road is None
