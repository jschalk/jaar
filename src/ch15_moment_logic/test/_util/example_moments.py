from src.a01_rope_logic.rope import create_rope
from src.a04_reason_logic.reason import FactUnit, factunit_shop
from src.a05_plan_logic.healer import healerunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.ch15_moment_logic.moment_main import MomentUnit, momentunit_shop
from src.ch15_moment_logic.test._util.ch15_env import get_module_temp_dir


def create_example_moment2() -> MomentUnit:
    # ESTABLISH
    x_moment_mstr_dir = get_module_temp_dir()
    a45_str = "amy45"
    amy_moment = momentunit_shop(a45_str, x_moment_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    amy_moment.create_init_job_from_guts(yao_str)
    amy_moment.create_init_job_from_guts(wei_str)
    amy_moment.create_init_job_from_guts(zia_str)
    yao_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, yao_str)
    wei_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, wei_str)
    zia_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, zia_str)

    yao_gut_belief.set_credor_respect(101)
    wei_gut_belief.set_credor_respect(75)
    zia_gut_belief.set_credor_respect(52)
    yao_gut_belief.set_debtor_respect(1000)
    wei_gut_belief.set_debtor_respect(750)
    zia_gut_belief.set_debtor_respect(500)

    yao_gut_belief.add_voiceunit(yao_str, 34, 600)
    yao_gut_belief.add_voiceunit(zia_str, 57, 300)
    yao_gut_belief.add_voiceunit(wei_str, 10, 100)
    wei_gut_belief.add_voiceunit(yao_str, 37, 100)
    wei_gut_belief.add_voiceunit(wei_str, 11, 400)
    wei_gut_belief.add_voiceunit(zia_str, 27, 250)
    zia_gut_belief.add_voiceunit(yao_str, 14, 100)
    zia_gut_belief.add_voiceunit(zia_str, 38, 400)
    texas_str = "Texas"
    texas_rope = yao_gut_belief.make_l1_rope(texas_str)
    yao_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    wei_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    zia_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = yao_gut_belief.make_rope(texas_rope, dallas_str)
    dallas_healerunit = healerunit_shop({yao_str, zia_str})
    dallas_plan = planunit_shop(dallas_str, healerunit=dallas_healerunit)
    elpaso_str = "el paso"
    elpaso_rope = yao_gut_belief.make_rope(texas_rope, elpaso_str)
    elpaso_healerunit = healerunit_shop({yao_str})
    elpaso_plan = planunit_shop(elpaso_str, healerunit=elpaso_healerunit)

    yao_gut_belief.set_plan(dallas_plan, texas_rope)
    yao_gut_belief.set_plan(elpaso_plan, texas_rope)
    wei_gut_belief.set_plan(dallas_plan, texas_rope)
    wei_gut_belief.set_plan(elpaso_plan, texas_rope)
    zia_gut_belief.set_plan(dallas_plan, texas_rope)
    zia_gut_belief.set_plan(elpaso_plan, texas_rope)
    save_gut_file(x_moment_mstr_dir, yao_gut_belief)
    save_gut_file(x_moment_mstr_dir, wei_gut_belief)
    save_gut_file(x_moment_mstr_dir, zia_gut_belief)
    amy_moment._set_all_healer_dutys(yao_str)
    amy_moment._set_all_healer_dutys(wei_str)
    amy_moment._set_all_healer_dutys(zia_str)

    return amy_moment


def create_example_moment3() -> MomentUnit:
    # ESTABLISH
    a45_str = "amy45"
    x_moment_mstr_dir = get_module_temp_dir()
    amy_moment = momentunit_shop(a45_str, x_moment_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    amy_moment.create_init_job_from_guts(yao_str)
    amy_moment.create_init_job_from_guts(wei_str)
    amy_moment.create_init_job_from_guts(zia_str)
    yao_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, yao_str)
    wei_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, wei_str)
    zia_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_rope = yao_gut_belief.make_l1_rope(casa_str)
    yao_gut_belief.set_l1_plan(planunit_shop(casa_str))
    wei_gut_belief.set_l1_plan(planunit_shop(casa_str))
    zia_gut_belief.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = yao_gut_belief.make_rope(casa_rope, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_belief.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    yao_gut_belief.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    yao_gut_belief.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    wei_gut_belief.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    wei_gut_belief.set_plan(planunit_shop(bath_str, task=True), clean_rope)

    zia_gut_belief.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    zia_gut_belief.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    zia_gut_belief.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    save_gut_file(x_moment_mstr_dir, yao_gut_belief)
    save_gut_file(x_moment_mstr_dir, wei_gut_belief)
    save_gut_file(x_moment_mstr_dir, zia_gut_belief)

    return amy_moment


def create_example_moment4() -> MomentUnit:
    # ESTABLISH
    x_moment_mstr_dir = get_module_temp_dir()
    a45_str = "amy45"
    amy_moment = momentunit_shop(a45_str, x_moment_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    amy_moment.create_init_job_from_guts(yao_str)
    amy_moment.create_init_job_from_guts(wei_str)
    amy_moment.create_init_job_from_guts(zia_str)
    yao_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, yao_str)
    wei_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, wei_str)
    zia_gut_belief = open_gut_file(x_moment_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_rope = yao_gut_belief.make_l1_rope(casa_str)
    yao_gut_belief.set_l1_plan(planunit_shop(casa_str))
    wei_gut_belief.set_l1_plan(planunit_shop(casa_str))
    zia_gut_belief.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = yao_gut_belief.make_rope(casa_rope, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_belief.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    yao_gut_belief.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    yao_gut_belief.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    wei_gut_belief.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    wei_gut_belief.set_plan(planunit_shop(bath_str, task=True), clean_rope)

    zia_gut_belief.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    zia_gut_belief.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    zia_gut_belief.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    yao_gut_belief.set_credor_respect(101)
    wei_gut_belief.set_credor_respect(75)
    zia_gut_belief.set_credor_respect(52)
    yao_gut_belief.set_debtor_respect(1000)
    wei_gut_belief.set_debtor_respect(750)
    zia_gut_belief.set_debtor_respect(500)

    yao_gut_belief.add_voiceunit(yao_str, 34, 600)
    yao_gut_belief.add_voiceunit(zia_str, 57, 300)
    yao_gut_belief.add_voiceunit(wei_str, 10, 100)
    wei_gut_belief.add_voiceunit(yao_str, 37, 100)
    wei_gut_belief.add_voiceunit(wei_str, 11, 400)
    wei_gut_belief.add_voiceunit(zia_str, 27, 250)
    zia_gut_belief.add_voiceunit(yao_str, 14, 100)
    zia_gut_belief.add_voiceunit(zia_str, 38, 400)

    texas_str = "Texas"
    yao_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    wei_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    zia_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    save_gut_file(x_moment_mstr_dir, yao_gut_belief)
    save_gut_file(x_moment_mstr_dir, wei_gut_belief)
    save_gut_file(x_moment_mstr_dir, zia_gut_belief)

    return amy_moment


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    clean_rope = create_rope(floor_rope, "clean")
    return factunit_shop(floor_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    dirty_rope = create_rope(floor_rope, "dirty")
    return factunit_shop(floor_rope, dirty_rope)


def _example_empty_bob_beliefunit() -> BeliefUnit:
    a23_str = "amy23"
    return beliefunit_shop("Bob", a23_str)


def get_bob_mop_without_reason_beliefunit_example() -> BeliefUnit:
    bob_belief = _example_empty_bob_beliefunit()
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    floor_rope = bob_belief.make_rope(casa_rope, floor_str)
    clean_rope = bob_belief.make_rope(floor_rope, clean_str)
    dirty_rope = bob_belief.make_rope(floor_rope, dirty_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.add_plan(casa_rope, 1)
    bob_belief.add_plan(floor_rope, 1)
    bob_belief.add_plan(clean_rope, 1)
    bob_belief.add_plan(dirty_rope, 1)
    bob_belief.add_plan(mop_rope, 1, task=True)
    return bob_belief


def get_bob_mop_with_reason_beliefunit_example() -> BeliefUnit:
    """belief_name: bob, moment_label: amy23"""
    bob_belief = get_bob_mop_without_reason_beliefunit_example()
    casa_str = "casa"
    floor_str = "floor status"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    floor_rope = bob_belief.make_rope(casa_rope, floor_str)
    dirty_rope = bob_belief.make_rope(floor_rope, dirty_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    return bob_belief


def get_bob_mop_fact_clean_beliefunit_example() -> BeliefUnit:
    bob_belief = get_bob_mop_with_reason_beliefunit_example()
    bob_belief.add_voiceunit("Bob")
    casa_rope = bob_belief.make_l1_rope("casa")
    floor_rope = bob_belief.make_rope(casa_rope, "floor status")
    clean_rope = bob_belief.make_rope(floor_rope, "clean")
    bob_belief.add_fact(floor_rope, clean_rope)
    return bob_belief


def get_yao_run_with_reason_beliefunit_example() -> BeliefUnit:
    yao_belief = beliefunit_shop("Yao", "amy23")
    sport_str = "sport"
    participate_str = "participate"
    ski_str = "skiing"
    run_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowng_str = "snowng"
    sport_rope = yao_belief.make_l1_rope(sport_str)
    participate_rope = yao_belief.make_rope(sport_rope, participate_str)
    ski_rope = yao_belief.make_rope(participate_rope, ski_str)
    run_rope = yao_belief.make_rope(participate_rope, run_str)
    weather_rope = yao_belief.make_l1_rope(weather_str)
    rain_rope = yao_belief.make_rope(weather_rope, raining_str)
    snow_rope = yao_belief.make_rope(weather_rope, snowng_str)
    yao_belief.add_plan(participate_rope)
    yao_belief.add_plan(ski_rope, 5, task=True)
    yao_belief.add_plan(run_rope, 1, task=True)
    yao_belief.add_plan(weather_rope)
    yao_belief.add_plan(rain_rope)
    yao_belief.add_plan(snow_rope)
    yao_belief.edit_plan_attr(
        ski_rope, reason_context=weather_rope, reason_case=snow_rope
    )
    yao_belief.edit_plan_attr(
        run_rope, reason_context=weather_rope, reason_case=rain_rope
    )
    return yao_belief


def get_yao_run_rain_fact_beliefunit_example() -> BeliefUnit:
    yao_belief = get_yao_run_with_reason_beliefunit_example()
    weather_rope = yao_belief.make_l1_rope("weather")
    rain_rope = yao_belief.make_rope(weather_rope, "raining")
    yao_belief.add_fact(weather_rope, rain_rope)
    return yao_belief
