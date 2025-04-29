from src.a00_data_toolbox.file_toolbox import delete_dir, save_file, open_file
from src.a05_item_logic.healer import healerlink_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud_graphics import display_itemtree
from src.a12_hub_tools.hub_path import treasury_filename
from src.a12_hub_tools.hub_tool import save_gut_file, open_gut_file
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic._utils.example_listen_hub import get_texas_road
from src.a13_bud_listen_logic._utils.env_a13 import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_get_keep_roads_RaisesErrorWhen__keeps_justified_IsFalse(
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
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    dallas_str = "dallas"
    dallas_road = sue_gut_bud.make_road(texas_road, dallas_str)
    sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    sue_gut_bud.set_item(itemunit_shop(dallas_str), texas_road)
    sue_gut_bud.edit_item_attr(texas_road, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.edit_item_attr(dallas_road, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.settle_bud()
    assert sue_gut_bud._keeps_justified is False
    save_gut_file(env_dir(), sue_gut_bud)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_roads()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_roads from '{sue_str}' gut bud because 'BudUnit._keeps_justified' is False."
    )


def test_HubUnit_get_keep_roads_RaisesErrorWhen__keeps_buildable_IsFalse(
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
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    sue_gut_bud.edit_item_attr(texas_road, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.settle_bud()
    assert sue_gut_bud._keeps_justified
    assert sue_gut_bud._keeps_buildable is False
    save_gut_file(env_dir(), sue_gut_bud)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_roads()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_roads from '{sue_str}' gut bud because 'BudUnit._keeps_buildable' is False."
    )


def test_HubUnit_get_keep_roads_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    sue_gut_bud = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_bud.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_road = sue_gut_bud.make_road(texas_road, dallas_str)
    elpaso_road = sue_gut_bud.make_road(texas_road, elpaso_str)
    dallas_item = itemunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_item(dallas_item, texas_road)
    sue_gut_bud.set_item(elpaso_item, texas_road)
    sue_gut_bud.settle_bud()
    display_itemtree(sue_gut_bud, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_bud)

    # WHEN
    sue_keep_roads = sue_hubunit.get_keep_roads()

    # THEN
    assert len(sue_keep_roads) == 2
    assert dallas_road in sue_keep_roads
    assert elpaso_road in sue_keep_roads


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
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = sue_gut_bud.make_road(texas_road, dallas_str)
    dallas_item = itemunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_item(dallas_item, texas_road)
    elpaso_str = "el paso"
    elpaso_road = sue_gut_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_item(elpaso_item, texas_road)
    display_itemtree(sue_gut_bud, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_bud)
    sue_dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_road)
    sue_elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_road)
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str)) is False
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str)) is False
    assert sue_hubunit.keep_road is None

    # WHEN
    sue_hubunit.save_all_gut_dutys()

    # THEN
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str))
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str))
    assert sue_hubunit.keep_road is None


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
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    sue_hubunit.keep_road = texas_road
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
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, get_texas_road())
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
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    sue_hubunit.keep_road = texas_road
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
#     sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, get_texas_road())

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         check_connection(sue_hubunit.treasury_db_file_conn())
#     assert str(excinfo.value) == "unable to open database file"

#     # WHEN
#     sue_hubunit.create_treasury_db_file()

#     # THEN
#     assert check_connection(sue_hubunit.treasury_db_file_conn())


def test_HubUnit_treasury_db_file_conn_RaisesErrorIfMissing_keep_road(
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
        == f"hubunit cannot connect to treasury_db_file because keep_road is {sue_hubunit.keep_road}"
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
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_road = sue_gut_bud.make_road(texas_road, dallas_str)
    elpaso_road = sue_gut_bud.make_road(texas_road, elpaso_str)
    dallas_item = itemunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_bud.set_item(dallas_item, texas_road)
    sue_gut_bud.set_item(elpaso_item, texas_road)
    sue_gut_bud.settle_bud()
    display_itemtree(sue_gut_bud, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_bud)

    dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_road)
    elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_road)
    print(f"{dallas_hubunit.treasury_db_path()=}")
    print(f"{elpaso_hubunit.treasury_db_path()=}")
    assert os_path_exists(dallas_hubunit.treasury_db_path()) is False
    assert os_path_exists(elpaso_hubunit.treasury_db_path()) is False
    assert sue_hubunit.keep_road is None

    # WHEN
    sue_hubunit.create_gut_treasury_db_files()

    # THEN
    assert os_path_exists(dallas_hubunit.treasury_db_path())
    assert os_path_exists(elpaso_hubunit.treasury_db_path())
    assert sue_hubunit.keep_road is None
