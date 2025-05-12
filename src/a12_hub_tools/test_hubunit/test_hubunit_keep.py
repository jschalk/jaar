from src.a00_data_toolbox.file_toolbox import delete_dir, save_file, open_file
from src.a05_idea_logic.healer import healerlink_shop
from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud_graphics import display_ideatree
from src.a12_hub_tools.hub_path import treasury_filename
from src.a12_hub_tools.hub_tool import save_gut_file, open_gut_file
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic._utils.example_listen_hub import get_texas_way
from src.a13_bud_listen_logic._utils.env_a13 import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_get_keep_ways_RaisesErrorWhen__keeps_justified_IsFalse(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_bud.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_way = sue_gut_bud.make_l1_way(texas_str)
    dallas_str = "dallas"
    dallas_way = sue_gut_bud.make_way(texas_way, dallas_str)
    sue_gut_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    sue_gut_bud.set_idea(ideaunit_shop(dallas_str), texas_way)
    sue_gut_bud.edit_idea_attr(texas_way, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.edit_idea_attr(dallas_way, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.settle_bud()
    assert sue_gut_bud._keeps_justified is False
    save_gut_file(env_dir(), sue_gut_bud)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ways()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ways from '{sue_str}' gut bud because 'BudUnit._keeps_justified' is False."
    )


def test_HubUnit_get_keep_ways_RaisesErrorWhen__keeps_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_bud.add_acctunit(sue_str)
    texas_str = "Tex/as"
    texas_way = sue_gut_bud.make_l1_way(texas_str)
    sue_gut_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    sue_gut_bud.edit_idea_attr(texas_way, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.settle_bud()
    assert sue_gut_bud._keeps_justified
    assert sue_gut_bud._keeps_buildable is False
    save_gut_file(env_dir(), sue_gut_bud)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ways()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ways from '{sue_str}' gut bud because 'BudUnit._keeps_buildable' is False."
    )


def test_HubUnit_get_keep_ways_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_bud.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_way = sue_gut_bud.make_l1_way(texas_str)
    sue_gut_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_way = sue_gut_bud.make_way(texas_way, dallas_str)
    elpaso_way = sue_gut_bud.make_way(texas_way, elpaso_str)
    dallas_idea = ideaunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_idea = ideaunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_idea(dallas_idea, texas_way)
    sue_gut_bud.set_idea(elpaso_idea, texas_way)
    sue_gut_bud.settle_bud()
    display_ideatree(sue_gut_bud, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_bud)

    # WHEN
    sue_keep_ways = sue_hubunit.get_keep_ways()

    # THEN
    assert len(sue_keep_ways) == 2
    assert dallas_way in sue_keep_ways
    assert elpaso_way in sue_keep_ways


def test_HubUnit_save_all_gut_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_bud.add_acctunit(sue_str)
    bob_str = "Bob"
    sue_gut_bud.add_acctunit(bob_str)
    texas_str = "Texas"
    texas_way = sue_gut_bud.make_l1_way(texas_str)
    sue_gut_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_way = sue_gut_bud.make_way(texas_way, dallas_str)
    dallas_idea = ideaunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_idea(dallas_idea, texas_way)
    elpaso_str = "el paso"
    elpaso_way = sue_gut_bud.make_way(texas_way, elpaso_str)
    elpaso_idea = ideaunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_idea(elpaso_idea, texas_way)
    display_ideatree(sue_gut_bud, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_bud)
    sue_dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_way)
    sue_elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_way)
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str)) is False
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str)) is False
    assert sue_hubunit.keep_way is None

    # WHEN
    sue_hubunit.save_all_gut_dutys()

    # THEN
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str))
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str))
    assert sue_hubunit.keep_way is None


def test_HubUnit_create_treasury_db_file_CorrectlyCreatesDatabase(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    texas_str = "Texas"
    texas_way = sue_gut_bud.make_l1_way(texas_str)
    sue_hubunit.keep_way = texas_way
    assert os_path_exists(sue_hubunit.treasury_db_path()) is False

    # WHEN
    sue_hubunit.create_treasury_db_file()

    # THEN
    assert os_path_exists(sue_hubunit.treasury_db_path())


def test_HubUnit_create_treasury_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH create keep
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, get_texas_way())
    delete_dir(sue_hubunit.treasury_db_path())  # clear out any treasury.db file
    sue_hubunit.create_treasury_db_file()
    assert os_path_exists(sue_hubunit.treasury_db_path())

    # ESTABLISH
    x_file_str = "Texas Dallas ElPaso"
    db_file = treasury_filename()
    save_file(
        sue_hubunit.keep_dir(),
        filename=db_file,
        file_str=x_file_str,
        replace=True,
    )
    assert os_path_exists(sue_hubunit.treasury_db_path())
    assert open_file(sue_hubunit.keep_dir(), filename=db_file) == x_file_str

    # WHEN
    sue_hubunit.create_treasury_db_file()
    # THEN
    assert open_file(sue_hubunit.keep_dir(), filename=db_file) == x_file_str


def test_HubUnit_treasury_db_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    texas_str = "Texas"
    texas_way = sue_gut_bud.make_l1_way(texas_str)
    sue_hubunit.keep_way = texas_way
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
#     sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, get_texas_way())

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         check_connection(sue_hubunit.treasury_db_file_conn())
#     assert str(excinfo.value) == "unable to open database file"

#     # WHEN
#     sue_hubunit.create_treasury_db_file()

#     # THEN
#     assert check_connection(sue_hubunit.treasury_db_file_conn())


def test_HubUnit_treasury_db_file_conn_RaisesErrorIfMissing_keep_way(
    env_dir_setup_cleanup,
):
    # ESTABLISH create
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.treasury_db_file_conn()
    assert (
        str(excinfo.value)
        == f"hubunit cannot connect to treasury_db_file because keep_way is {sue_hubunit.keep_way}"
    )


def test_HubUnit_create_gut_treasury_db_files_CreatesDatabases(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_bud.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_way = sue_gut_bud.make_l1_way(texas_str)
    sue_gut_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_way = sue_gut_bud.make_way(texas_way, dallas_str)
    elpaso_way = sue_gut_bud.make_way(texas_way, elpaso_str)
    dallas_idea = ideaunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_idea = ideaunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_idea(dallas_idea, texas_way)
    sue_gut_bud.set_idea(elpaso_idea, texas_way)
    sue_gut_bud.settle_bud()
    display_ideatree(sue_gut_bud, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_bud)

    dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_way)
    elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_way)
    print(f"{dallas_hubunit.treasury_db_path()=}")
    print(f"{elpaso_hubunit.treasury_db_path()=}")
    assert os_path_exists(dallas_hubunit.treasury_db_path()) is False
    assert os_path_exists(elpaso_hubunit.treasury_db_path()) is False
    assert sue_hubunit.keep_way is None

    # WHEN
    sue_hubunit.create_gut_treasury_db_files()

    # THEN
    assert os_path_exists(dallas_hubunit.treasury_db_path())
    assert os_path_exists(elpaso_hubunit.treasury_db_path())
    assert sue_hubunit.keep_way is None
