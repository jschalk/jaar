from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import delete_dir, open_file, save_file
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic.plan_graphics import display_concepttree
from src.a12_hub_toolbox._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_toolbox._util.example_hub_atoms import get_texas_rope
from src.a12_hub_toolbox.hub_path import treasury_filename
from src.a12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.a12_hub_toolbox.hubunit import hubunit_shop


def test_HubUnit_get_keep_ropes_RaisesErrorWhen__keeps_justified_IsFalse(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_plan())
    sue_gut_plan = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_plan.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    dallas_str = "dallas"
    dallas_rope = sue_gut_plan.make_rope(texas_rope, dallas_str)
    sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    sue_gut_plan.set_concept(conceptunit_shop(dallas_str), texas_rope)
    sue_gut_plan.edit_concept_attr(texas_rope, healerlink=healerlink_shop({sue_str}))
    sue_gut_plan.edit_concept_attr(dallas_rope, healerlink=healerlink_shop({sue_str}))
    sue_gut_plan.settle_plan()
    assert sue_gut_plan._keeps_justified is False
    save_gut_file(env_dir(), sue_gut_plan)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ropes()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ropes from '{sue_str}' gut plan because 'PlanUnit._keeps_justified' is False."
    )


def test_HubUnit_get_keep_ropes_RaisesErrorWhen__keeps_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_plan())
    sue_gut_plan = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_plan.add_acctunit(sue_str)
    texas_str = "Tex/as"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    sue_gut_plan.edit_concept_attr(texas_rope, healerlink=healerlink_shop({sue_str}))
    sue_gut_plan.settle_plan()
    assert sue_gut_plan._keeps_justified
    assert sue_gut_plan._keeps_buildable is False
    save_gut_file(env_dir(), sue_gut_plan)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ropes()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ropes from '{sue_str}' gut plan because 'PlanUnit._keeps_buildable' is False."
    )


def test_HubUnit_get_keep_ropes_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_plan())
    sue_gut_plan = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_plan.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_rope = sue_gut_plan.make_rope(texas_rope, dallas_str)
    elpaso_rope = sue_gut_plan.make_rope(texas_rope, elpaso_str)
    dallas_concept = conceptunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_concept = conceptunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_plan.set_concept(dallas_concept, texas_rope)
    sue_gut_plan.set_concept(elpaso_concept, texas_rope)
    sue_gut_plan.settle_plan()
    display_concepttree(sue_gut_plan, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_plan)

    # WHEN
    sue_keep_ropes = sue_hubunit.get_keep_ropes()

    # THEN
    assert len(sue_keep_ropes) == 2
    assert dallas_rope in sue_keep_ropes
    assert elpaso_rope in sue_keep_ropes


def test_HubUnit_save_all_gut_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_plan())
    sue_gut_plan = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_plan.add_acctunit(sue_str)
    bob_str = "Bob"
    sue_gut_plan.add_acctunit(bob_str)
    texas_str = "Texas"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_plan.make_rope(texas_rope, dallas_str)
    dallas_concept = conceptunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_plan.set_concept(dallas_concept, texas_rope)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_plan.make_rope(texas_rope, elpaso_str)
    elpaso_concept = conceptunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_plan.set_concept(elpaso_concept, texas_rope)
    display_concepttree(sue_gut_plan, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_plan)
    sue_dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_rope)
    sue_elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_rope)
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str)) is False
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str)) is False
    assert sue_hubunit.keep_rope is None

    # WHEN
    sue_hubunit.save_all_gut_dutys()

    # THEN
    assert os_path_exists(sue_dallas_hubunit.duty_path(sue_str))
    assert os_path_exists(sue_elpaso_hubunit.duty_path(sue_str))
    assert sue_hubunit.keep_rope is None


def test_HubUnit_create_treasury_db_file_CorrectlyCreatesDatabase(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_plan())
    sue_gut_plan = open_gut_file(env_dir(), a23_str, sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    sue_hubunit.keep_rope = texas_rope
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
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, get_texas_rope())
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
    save_gut_file(env_dir(), sue_hubunit.default_gut_plan())
    sue_gut_plan = open_gut_file(env_dir(), a23_str, sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    sue_hubunit.keep_rope = texas_rope
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
#     sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, get_texas_rope())

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         check_connection(sue_hubunit.treasury_db_file_conn())
#     assert str(excinfo.value) == "unable to popen database file"

#     # WHEN
#     sue_hubunit.create_treasury_db_file()

#     # THEN
#     assert check_connection(sue_hubunit.treasury_db_file_conn())


def test_HubUnit_treasury_db_file_conn_RaisesErrorIfMissing_keep_rope(
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
        == f"hubunit cannot connect to treasury_db_file because keep_rope is {sue_hubunit.keep_rope}"
    )


def test_HubUnit_create_gut_treasury_db_files_CreatesDatabases(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_plan())
    sue_gut_plan = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_plan.add_acctunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_rope = sue_gut_plan.make_rope(texas_rope, dallas_str)
    elpaso_rope = sue_gut_plan.make_rope(texas_rope, elpaso_str)
    dallas_concept = conceptunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_concept = conceptunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_plan.set_concept(dallas_concept, texas_rope)
    sue_gut_plan.set_concept(elpaso_concept, texas_rope)
    sue_gut_plan.settle_plan()
    display_concepttree(sue_gut_plan, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_plan)

    dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_rope)
    elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_rope)
    print(f"{dallas_hubunit.treasury_db_path()=}")
    print(f"{elpaso_hubunit.treasury_db_path()=}")
    assert os_path_exists(dallas_hubunit.treasury_db_path()) is False
    assert os_path_exists(elpaso_hubunit.treasury_db_path()) is False
    assert sue_hubunit.keep_rope is None

    # WHEN
    sue_hubunit.create_gut_treasury_db_files()

    # THEN
    assert os_path_exists(dallas_hubunit.treasury_db_path())
    assert os_path_exists(elpaso_hubunit.treasury_db_path())
    assert sue_hubunit.keep_rope is None
