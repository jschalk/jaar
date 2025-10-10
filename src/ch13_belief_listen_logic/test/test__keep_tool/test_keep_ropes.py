from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.ch06_plan_logic.healer import healerunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_graphics import display_plantree
from src.ch12_belief_file_toolbox.hub_tool import open_gut_file, save_gut_file
from src.ch12_belief_file_toolbox.hubunit import hubunit_shop
from src.ch12_belief_file_toolbox.test._util.ch12_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch13_belief_listen_logic._ref.ch13_path import create_keep_duty_path
from src.ch13_belief_listen_logic.keep_tool import get_keep_ropes, save_all_gut_dutys


def test_get_keep_ropes_RaisesErrorWhen_keeps_justified_IsFalse(
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
        get_keep_ropes(env_dir(), moment_label=a23_str, belief_name=sue_str)
    exception_str = f"Cannot get_keep_ropes from '{sue_str}' gut belief because 'BeliefUnit.keeps_justified' is False."
    assert str(excinfo.value) == exception_str


def test_get_keep_ropes_RaisesErrorWhen_keeps_buildable_IsFalse(
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
        get_keep_ropes(env_dir(), a23_str, belief_name=sue_str)
    exception_str = f"Cannot get_keep_ropes from '{sue_str}' gut belief because 'BeliefUnit.keeps_buildable' is False."
    assert str(excinfo.value) == exception_str


def test_get_keep_ropes_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
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
    sue_keep_ropes = get_keep_ropes(env_dir(), a23_str, belief_name=sue_str)

    # THEN
    assert len(sue_keep_ropes) == 2
    assert dallas_rope in sue_keep_ropes
    assert elpaso_rope in sue_keep_ropes


def test_save_all_gut_dutys_Setsdutys(env_dir_setup_cleanup, graphics_bool):
    # sourcery skip: extract-duplicate-method
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
    sue_keep_ropes = get_keep_ropes(env_dir(), a23_str, belief_name=sue_str)
    assert os_path_exists(sue_dallas_duty_path) is False
    assert os_path_exists(sue_elpaso_duty_path) is False

    # WHEN
    save_all_gut_dutys(
        moment_mstr_dir=mstr_dir,
        moment_label=a23_str,
        belief_name=sue_str,
        keep_ropes=sue_keep_ropes,
        knot=sue_hubunit.knot,
    )

    # THEN
    assert os_path_exists(sue_dallas_duty_path)
    assert os_path_exists(sue_elpaso_duty_path)
