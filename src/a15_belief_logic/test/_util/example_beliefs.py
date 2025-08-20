from src.a01_term_logic.rope import create_rope
from src.a04_reason_logic.reason_plan import FactUnit, factunit_shop
from src.a05_plan_logic.healer import healerunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import BelieverUnit, believerunit_shop
from src.a12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.a15_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.a15_belief_logic.test._util.a15_env import get_module_temp_dir


def create_example_belief2() -> BeliefUnit:
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a45_str = "amy45"
    amy_belief = beliefunit_shop(a45_str, x_belief_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    amy_belief.create_init_job_from_guts(yao_str)
    amy_belief.create_init_job_from_guts(wei_str)
    amy_belief.create_init_job_from_guts(zia_str)
    yao_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, yao_str)
    wei_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, wei_str)
    zia_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, zia_str)

    yao_gut_believer.set_credor_respect(101)
    wei_gut_believer.set_credor_respect(75)
    zia_gut_believer.set_credor_respect(52)
    yao_gut_believer.set_debtor_respect(1000)
    wei_gut_believer.set_debtor_respect(750)
    zia_gut_believer.set_debtor_respect(500)

    yao_gut_believer.add_partnerunit(yao_str, 34, 600)
    yao_gut_believer.add_partnerunit(zia_str, 57, 300)
    yao_gut_believer.add_partnerunit(wei_str, 10, 100)
    wei_gut_believer.add_partnerunit(yao_str, 37, 100)
    wei_gut_believer.add_partnerunit(wei_str, 11, 400)
    wei_gut_believer.add_partnerunit(zia_str, 27, 250)
    zia_gut_believer.add_partnerunit(yao_str, 14, 100)
    zia_gut_believer.add_partnerunit(zia_str, 38, 400)
    texas_str = "Texas"
    texas_rope = yao_gut_believer.make_l1_rope(texas_str)
    yao_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    wei_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    zia_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = yao_gut_believer.make_rope(texas_rope, dallas_str)
    dallas_healerunit = healerunit_shop({yao_str, zia_str})
    dallas_plan = planunit_shop(dallas_str, healerunit=dallas_healerunit)
    elpaso_str = "el paso"
    elpaso_rope = yao_gut_believer.make_rope(texas_rope, elpaso_str)
    elpaso_healerunit = healerunit_shop({yao_str})
    elpaso_plan = planunit_shop(elpaso_str, healerunit=elpaso_healerunit)

    yao_gut_believer.set_plan(dallas_plan, texas_rope)
    yao_gut_believer.set_plan(elpaso_plan, texas_rope)
    wei_gut_believer.set_plan(dallas_plan, texas_rope)
    wei_gut_believer.set_plan(elpaso_plan, texas_rope)
    zia_gut_believer.set_plan(dallas_plan, texas_rope)
    zia_gut_believer.set_plan(elpaso_plan, texas_rope)
    save_gut_file(x_belief_mstr_dir, yao_gut_believer)
    save_gut_file(x_belief_mstr_dir, wei_gut_believer)
    save_gut_file(x_belief_mstr_dir, zia_gut_believer)
    amy_belief._set_all_healer_dutys(yao_str)
    amy_belief._set_all_healer_dutys(wei_str)
    amy_belief._set_all_healer_dutys(zia_str)

    return amy_belief


def create_example_belief3() -> BeliefUnit:
    # ESTABLISH
    a45_str = "amy45"
    x_belief_mstr_dir = get_module_temp_dir()
    amy_belief = beliefunit_shop(a45_str, x_belief_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    amy_belief.create_init_job_from_guts(yao_str)
    amy_belief.create_init_job_from_guts(wei_str)
    amy_belief.create_init_job_from_guts(zia_str)
    yao_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, yao_str)
    wei_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, wei_str)
    zia_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_rope = yao_gut_believer.make_l1_rope(casa_str)
    yao_gut_believer.set_l1_plan(planunit_shop(casa_str))
    wei_gut_believer.set_l1_plan(planunit_shop(casa_str))
    zia_gut_believer.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = yao_gut_believer.make_rope(casa_rope, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_believer.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    yao_gut_believer.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    yao_gut_believer.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    wei_gut_believer.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    wei_gut_believer.set_plan(planunit_shop(bath_str, task=True), clean_rope)

    zia_gut_believer.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    zia_gut_believer.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    zia_gut_believer.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    save_gut_file(x_belief_mstr_dir, yao_gut_believer)
    save_gut_file(x_belief_mstr_dir, wei_gut_believer)
    save_gut_file(x_belief_mstr_dir, zia_gut_believer)

    return amy_belief


def create_example_belief4() -> BeliefUnit:
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a45_str = "amy45"
    amy_belief = beliefunit_shop(a45_str, x_belief_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    amy_belief.create_init_job_from_guts(yao_str)
    amy_belief.create_init_job_from_guts(wei_str)
    amy_belief.create_init_job_from_guts(zia_str)
    yao_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, yao_str)
    wei_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, wei_str)
    zia_gut_believer = open_gut_file(x_belief_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_rope = yao_gut_believer.make_l1_rope(casa_str)
    yao_gut_believer.set_l1_plan(planunit_shop(casa_str))
    wei_gut_believer.set_l1_plan(planunit_shop(casa_str))
    zia_gut_believer.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = yao_gut_believer.make_rope(casa_rope, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_believer.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    yao_gut_believer.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    yao_gut_believer.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    wei_gut_believer.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    wei_gut_believer.set_plan(planunit_shop(bath_str, task=True), clean_rope)

    zia_gut_believer.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    zia_gut_believer.set_plan(planunit_shop(bath_str, task=True), clean_rope)
    zia_gut_believer.set_plan(planunit_shop(hall_str, task=True), clean_rope)

    yao_gut_believer.set_credor_respect(101)
    wei_gut_believer.set_credor_respect(75)
    zia_gut_believer.set_credor_respect(52)
    yao_gut_believer.set_debtor_respect(1000)
    wei_gut_believer.set_debtor_respect(750)
    zia_gut_believer.set_debtor_respect(500)

    yao_gut_believer.add_partnerunit(yao_str, 34, 600)
    yao_gut_believer.add_partnerunit(zia_str, 57, 300)
    yao_gut_believer.add_partnerunit(wei_str, 10, 100)
    wei_gut_believer.add_partnerunit(yao_str, 37, 100)
    wei_gut_believer.add_partnerunit(wei_str, 11, 400)
    wei_gut_believer.add_partnerunit(zia_str, 27, 250)
    zia_gut_believer.add_partnerunit(yao_str, 14, 100)
    zia_gut_believer.add_partnerunit(zia_str, 38, 400)

    texas_str = "Texas"
    yao_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    wei_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    zia_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    save_gut_file(x_belief_mstr_dir, yao_gut_believer)
    save_gut_file(x_belief_mstr_dir, wei_gut_believer)
    save_gut_file(x_belief_mstr_dir, zia_gut_believer)

    return amy_belief


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


def _example_empty_bob_believerunit() -> BelieverUnit:
    a23_str = "amy23"
    return believerunit_shop("Bob", a23_str)


def get_bob_mop_without_reason_believerunit_example() -> BelieverUnit:
    bob_believer = _example_empty_bob_believerunit()
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    floor_rope = bob_believer.make_rope(casa_rope, floor_str)
    clean_rope = bob_believer.make_rope(floor_rope, clean_str)
    dirty_rope = bob_believer.make_rope(floor_rope, dirty_str)
    mop_rope = bob_believer.make_rope(casa_rope, mop_str)
    bob_believer.add_plan(casa_rope, 1)
    bob_believer.add_plan(floor_rope, 1)
    bob_believer.add_plan(clean_rope, 1)
    bob_believer.add_plan(dirty_rope, 1)
    bob_believer.add_plan(mop_rope, 1, task=True)
    return bob_believer


def get_bob_mop_with_reason_believerunit_example() -> BelieverUnit:
    """believer_name: bob, belief_label: amy23"""
    bob_believer = get_bob_mop_without_reason_believerunit_example()
    casa_str = "casa"
    floor_str = "floor status"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    floor_rope = bob_believer.make_rope(casa_rope, floor_str)
    dirty_rope = bob_believer.make_rope(floor_rope, dirty_str)
    mop_rope = bob_believer.make_rope(casa_rope, mop_str)
    bob_believer.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    return bob_believer


def get_bob_mop_fact_clean_believerunit_example() -> BelieverUnit:
    bob_believer = get_bob_mop_with_reason_believerunit_example()
    bob_believer.add_partnerunit("Bob")
    casa_rope = bob_believer.make_l1_rope("casa")
    floor_rope = bob_believer.make_rope(casa_rope, "floor status")
    clean_rope = bob_believer.make_rope(floor_rope, "clean")
    bob_believer.add_fact(floor_rope, clean_rope)
    return bob_believer


def get_yao_run_with_reason_believerunit_example() -> BelieverUnit:
    yao_believer = believerunit_shop("Yao", "amy23")
    sport_str = "sport"
    participate_str = "participate"
    ski_str = "skiing"
    run_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowng_str = "snowng"
    sport_rope = yao_believer.make_l1_rope(sport_str)
    participate_rope = yao_believer.make_rope(sport_rope, participate_str)
    ski_rope = yao_believer.make_rope(participate_rope, ski_str)
    run_rope = yao_believer.make_rope(participate_rope, run_str)
    weather_rope = yao_believer.make_l1_rope(weather_str)
    rain_rope = yao_believer.make_rope(weather_rope, raining_str)
    snow_rope = yao_believer.make_rope(weather_rope, snowng_str)
    yao_believer.add_plan(participate_rope)
    yao_believer.add_plan(ski_rope, 5, task=True)
    yao_believer.add_plan(run_rope, 1, task=True)
    yao_believer.add_plan(weather_rope)
    yao_believer.add_plan(rain_rope)
    yao_believer.add_plan(snow_rope)
    yao_believer.edit_plan_attr(
        ski_rope, reason_context=weather_rope, reason_case=snow_rope
    )
    yao_believer.edit_plan_attr(
        run_rope, reason_context=weather_rope, reason_case=rain_rope
    )
    return yao_believer


def get_yao_run_rain_fact_believerunit_example() -> BelieverUnit:
    yao_believer = get_yao_run_with_reason_believerunit_example()
    weather_rope = yao_believer.make_l1_rope("weather")
    rain_rope = yao_believer.make_rope(weather_rope, "raining")
    yao_believer.add_fact(weather_rope, rain_rope)
    return yao_believer
