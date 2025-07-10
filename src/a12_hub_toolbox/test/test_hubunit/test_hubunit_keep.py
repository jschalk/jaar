from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import delete_dir, open_file, save_file
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_graphics import display_plantree
from src.a12_hub_toolbox.a12_path import (
    create_keep_rope_path,
    create_treasury_db_path,
    treasury_filename,
)
from src.a12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_toolbox.test._util.example_hub_atoms import get_texas_rope


def test_HubUnit_get_keep_ropes_RaisesErrorWhen__keeps_justified_IsFalse(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_believer())
    sue_gut_believer = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_believer.add_personunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_believer.make_l1_rope(texas_str)
    dallas_str = "dallas"
    dallas_rope = sue_gut_believer.make_rope(texas_rope, dallas_str)
    sue_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    sue_gut_believer.set_plan(planunit_shop(dallas_str), texas_rope)
    sue_gut_believer.edit_plan_attr(texas_rope, healerlink=healerlink_shop({sue_str}))
    sue_gut_believer.edit_plan_attr(dallas_rope, healerlink=healerlink_shop({sue_str}))
    sue_gut_believer.settle_believer()
    assert sue_gut_believer._keeps_justified is False
    save_gut_file(env_dir(), sue_gut_believer)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ropes()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ropes from '{sue_str}' gut believer because 'BelieverUnit._keeps_justified' is False."
    )


def test_HubUnit_get_keep_ropes_RaisesErrorWhen__keeps_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_believer())
    sue_gut_believer = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_believer.add_personunit(sue_str)
    texas_str = "Tex/as"
    texas_rope = sue_gut_believer.make_l1_rope(texas_str)
    sue_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    sue_gut_believer.edit_plan_attr(texas_rope, healerlink=healerlink_shop({sue_str}))
    sue_gut_believer.settle_believer()
    assert sue_gut_believer._keeps_justified
    assert sue_gut_believer._keeps_buildable is False
    save_gut_file(env_dir(), sue_gut_believer)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ropes()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ropes from '{sue_str}' gut believer because 'BelieverUnit._keeps_buildable' is False."
    )


def test_HubUnit_get_keep_ropes_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_believer())
    sue_gut_believer = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_believer.add_personunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_believer.make_l1_rope(texas_str)
    sue_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_rope = sue_gut_believer.make_rope(texas_rope, dallas_str)
    elpaso_rope = sue_gut_believer.make_rope(texas_rope, elpaso_str)
    dallas_plan = planunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_plan = planunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_believer.set_plan(dallas_plan, texas_rope)
    sue_gut_believer.set_plan(elpaso_plan, texas_rope)
    sue_gut_believer.settle_believer()
    display_plantree(sue_gut_believer, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_believer)

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
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_believer())
    sue_gut_believer = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_believer.add_personunit(sue_str)
    bob_str = "Bob"
    sue_gut_believer.add_personunit(bob_str)
    texas_str = "Texas"
    texas_rope = sue_gut_believer.make_l1_rope(texas_str)
    sue_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_believer.make_rope(texas_rope, dallas_str)
    dallas_plan = planunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_believer.set_plan(dallas_plan, texas_rope)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_believer.make_rope(texas_rope, elpaso_str)
    elpaso_plan = planunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_believer.set_plan(elpaso_plan, texas_rope)
    display_plantree(sue_gut_believer, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_believer)
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


def test_HubUnit_create_gut_treasury_db_files_CreatesDatabases(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_believer())
    sue_gut_believer = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_believer.add_personunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_believer.make_l1_rope(texas_str)
    sue_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_rope = sue_gut_believer.make_rope(texas_rope, dallas_str)
    elpaso_rope = sue_gut_believer.make_rope(texas_rope, elpaso_str)
    dallas_plan = planunit_shop(dallas_str, healerlink=healerlink_shop({sue_str}))
    elpaso_plan = planunit_shop(elpaso_str, healerlink=healerlink_shop({sue_str}))
    sue_gut_believer.set_plan(dallas_plan, texas_rope)
    sue_gut_believer.set_plan(elpaso_plan, texas_rope)
    sue_gut_believer.settle_believer()
    display_plantree(sue_gut_believer, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_believer)

    dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_rope)
    elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_rope)
    dallas_treasury_db_path = create_treasury_db_path(
        belief_mstr_dir=dallas_hubunit.belief_mstr_dir,
        believer_name=dallas_hubunit.believer_name,
        belief_label=dallas_hubunit.belief_label,
        keep_rope=dallas_hubunit.keep_rope,
        knot=dallas_hubunit.knot,
    )
    elpaso_treasury_db_path = create_treasury_db_path(
        belief_mstr_dir=elpaso_hubunit.belief_mstr_dir,
        believer_name=elpaso_hubunit.believer_name,
        belief_label=elpaso_hubunit.belief_label,
        keep_rope=elpaso_hubunit.keep_rope,
        knot=elpaso_hubunit.knot,
    )
    print(f"{dallas_treasury_db_path=}")
    print(f"{elpaso_treasury_db_path=}")
    assert os_path_exists(dallas_treasury_db_path) is False
    assert os_path_exists(elpaso_treasury_db_path) is False
    assert sue_hubunit.keep_rope is None

    # WHEN
    sue_hubunit.create_gut_treasury_db_files()

    # THEN
    assert os_path_exists(dallas_treasury_db_path)
    assert os_path_exists(elpaso_treasury_db_path)
    assert sue_hubunit.keep_rope is None
