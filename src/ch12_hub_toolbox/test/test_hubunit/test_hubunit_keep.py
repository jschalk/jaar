from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.ch00_data_toolbox.file_toolbox import delete_dir, open_file, save_file
from src.ch05_plan_logic.healer import healerunit_shop
from src.ch05_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_graphics import display_plantree
from src.ch12_hub_toolbox.ch12_path import (
    create_keep_duty_path,
    create_keep_rope_path,
    create_treasury_db_path,
    treasury_filename,
)
from src.ch12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.ch12_hub_toolbox.hubunit import hubunit_shop
from src.ch12_hub_toolbox.test._util.ch12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.ch12_hub_toolbox.test._util.example_hub_atoms import get_texas_rope


def test_HubUnit_get_keep_ropes_RaisesErrorWhen_keeps_justified_IsFalse(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_belief())
    sue_gut_belief = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_belief.add_voiceunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_belief.make_l1_rope(texas_str)
    dallas_str = "dallas"
    dallas_rope = sue_gut_belief.make_rope(texas_rope, dallas_str)
    sue_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    sue_gut_belief.set_plan(planunit_shop(dallas_str), texas_rope)
    sue_gut_belief.edit_plan_attr(texas_rope, healerunit=healerunit_shop({sue_str}))
    sue_gut_belief.edit_plan_attr(dallas_rope, healerunit=healerunit_shop({sue_str}))
    sue_gut_belief.cashout()
    assert sue_gut_belief.keeps_justified is False
    save_gut_file(env_dir(), sue_gut_belief)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ropes()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ropes from '{sue_str}' gut belief because 'BeliefUnit.keeps_justified' is False."
    )


def test_HubUnit_get_keep_ropes_RaisesErrorWhen_keeps_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_belief())
    sue_gut_belief = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_belief.add_voiceunit(sue_str)
    texas_str = "Tex/as"
    texas_rope = sue_gut_belief.make_l1_rope(texas_str)
    sue_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    sue_gut_belief.edit_plan_attr(texas_rope, healerunit=healerunit_shop({sue_str}))
    sue_gut_belief.cashout()
    assert sue_gut_belief.keeps_justified
    assert sue_gut_belief.keeps_buildable is False
    save_gut_file(env_dir(), sue_gut_belief)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_keep_ropes()
    assert (
        str(excinfo.value)
        == f"Cannot get_keep_ropes from '{sue_str}' gut belief because 'BeliefUnit.keeps_buildable' is False."
    )


def test_HubUnit_get_keep_ropes_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_belief())
    sue_gut_belief = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_belief.add_voiceunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_belief.make_l1_rope(texas_str)
    sue_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_rope = sue_gut_belief.make_rope(texas_rope, dallas_str)
    elpaso_rope = sue_gut_belief.make_rope(texas_rope, elpaso_str)
    dallas_plan = planunit_shop(dallas_str, healerunit=healerunit_shop({sue_str}))
    elpaso_plan = planunit_shop(elpaso_str, healerunit=healerunit_shop({sue_str}))
    sue_gut_belief.set_plan(dallas_plan, texas_rope)
    sue_gut_belief.set_plan(elpaso_plan, texas_rope)
    sue_gut_belief.cashout()
    display_plantree(sue_gut_belief, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_belief)

    # WHEN
    sue_keep_ropes = sue_hubunit.get_keep_ropes()

    # THEN
    assert len(sue_keep_ropes) == 2
    assert dallas_rope in sue_keep_ropes
    assert elpaso_rope in sue_keep_ropes


def test_HubUnit_save_all_gut_dutys_Setsdutys(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    mstr_dir = env_dir()
    sue_hubunit = hubunit_shop(mstr_dir, a23_str, sue_str, None)
    save_gut_file(mstr_dir, sue_hubunit.default_gut_belief())
    sue_gut_belief = open_gut_file(mstr_dir, a23_str, sue_str)
    sue_gut_belief.add_voiceunit(sue_str)
    bob_str = "Bob"
    sue_gut_belief.add_voiceunit(bob_str)
    texas_str = "Texas"
    texas_rope = sue_gut_belief.make_l1_rope(texas_str)
    sue_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_belief.make_rope(texas_rope, dallas_str)
    dallas_plan = planunit_shop(dallas_str, healerunit=healerunit_shop({sue_str}))
    sue_gut_belief.set_plan(dallas_plan, texas_rope)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_belief.make_rope(texas_rope, elpaso_str)
    elpaso_plan = planunit_shop(elpaso_str, healerunit=healerunit_shop({sue_str}))
    sue_gut_belief.set_plan(elpaso_plan, texas_rope)
    display_plantree(sue_gut_belief, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_belief)
    sue_dallas_duty_path = create_keep_duty_path(
        moment_mstr_dir=mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=dallas_rope,
        knot=None,
        duty_belief=sue_str,
    )
    sue_elpaso_duty_path = create_keep_duty_path(
        moment_mstr_dir=mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=elpaso_rope,
        knot=None,
        duty_belief=sue_str,
    )
    assert os_path_exists(sue_dallas_duty_path) is False
    assert os_path_exists(sue_elpaso_duty_path) is False
    assert not sue_hubunit.keep_rope

    # WHEN
    sue_hubunit.save_all_gut_dutys()

    # THEN
    assert os_path_exists(sue_dallas_duty_path)
    assert os_path_exists(sue_elpaso_duty_path)
    assert not sue_hubunit.keep_rope


def test_HubUnit_create_gut_treasury_db_files_CreatesDatabases(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, None)
    save_gut_file(env_dir(), sue_hubunit.default_gut_belief())
    sue_gut_belief = open_gut_file(env_dir(), a23_str, sue_str)
    sue_gut_belief.add_voiceunit(sue_str)
    texas_str = "Texas"
    texas_rope = sue_gut_belief.make_l1_rope(texas_str)
    sue_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_rope = sue_gut_belief.make_rope(texas_rope, dallas_str)
    elpaso_rope = sue_gut_belief.make_rope(texas_rope, elpaso_str)
    dallas_plan = planunit_shop(dallas_str, healerunit=healerunit_shop({sue_str}))
    elpaso_plan = planunit_shop(elpaso_str, healerunit=healerunit_shop({sue_str}))
    sue_gut_belief.set_plan(dallas_plan, texas_rope)
    sue_gut_belief.set_plan(elpaso_plan, texas_rope)
    sue_gut_belief.cashout()
    display_plantree(sue_gut_belief, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_belief)

    dallas_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, dallas_rope)
    elpaso_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, elpaso_rope)
    dallas_treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=dallas_hubunit.moment_mstr_dir,
        belief_name=dallas_hubunit.belief_name,
        moment_label=dallas_hubunit.moment_label,
        keep_rope=dallas_hubunit.keep_rope,
        knot=dallas_hubunit.knot,
    )
    elpaso_treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=elpaso_hubunit.moment_mstr_dir,
        belief_name=elpaso_hubunit.belief_name,
        moment_label=elpaso_hubunit.moment_label,
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
