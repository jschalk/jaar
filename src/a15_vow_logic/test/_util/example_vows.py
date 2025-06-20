from src.a01_term_logic.rope import create_rope
from src.a04_reason_logic.reason_concept import FactUnit, factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.a15_vow_logic.test._util.a15_env import get_module_temp_dir
from src.a15_vow_logic.vow import VowUnit, vowunit_shop


def create_example_vow2() -> VowUnit:
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a45_str = "accord45"
    accord_vow = vowunit_shop(a45_str, x_vow_mstr_dir, in_memory_journal=True)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    accord_vow.create_init_job_from_guts(yao_str)
    accord_vow.create_init_job_from_guts(wei_str)
    accord_vow.create_init_job_from_guts(zia_str)
    yao_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, yao_str)
    wei_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, wei_str)
    zia_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, zia_str)

    yao_gut_plan.set_credor_respect(101)
    wei_gut_plan.set_credor_respect(75)
    zia_gut_plan.set_credor_respect(52)
    yao_gut_plan.set_debtor_respect(1000)
    wei_gut_plan.set_debtor_respect(750)
    zia_gut_plan.set_debtor_respect(500)

    yao_gut_plan.add_acctunit(yao_str, 34, 600)
    yao_gut_plan.add_acctunit(zia_str, 57, 300)
    yao_gut_plan.add_acctunit(wei_str, 10, 100)
    wei_gut_plan.add_acctunit(yao_str, 37, 100)
    wei_gut_plan.add_acctunit(wei_str, 11, 400)
    wei_gut_plan.add_acctunit(zia_str, 27, 250)
    zia_gut_plan.add_acctunit(yao_str, 14, 100)
    zia_gut_plan.add_acctunit(zia_str, 38, 400)
    texas_str = "Texas"
    texas_rope = yao_gut_plan.make_l1_rope(texas_str)
    yao_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    wei_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    zia_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = yao_gut_plan.make_rope(texas_rope, dallas_str)
    dallas_healerlink = healerlink_shop({yao_str, zia_str})
    dallas_concept = conceptunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_rope = yao_gut_plan.make_rope(texas_rope, elpaso_str)
    elpaso_healerlink = healerlink_shop({yao_str})
    elpaso_concept = conceptunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    yao_gut_plan.set_concept(dallas_concept, texas_rope)
    yao_gut_plan.set_concept(elpaso_concept, texas_rope)
    wei_gut_plan.set_concept(dallas_concept, texas_rope)
    wei_gut_plan.set_concept(elpaso_concept, texas_rope)
    zia_gut_plan.set_concept(dallas_concept, texas_rope)
    zia_gut_plan.set_concept(elpaso_concept, texas_rope)
    save_gut_file(x_vow_mstr_dir, yao_gut_plan)
    save_gut_file(x_vow_mstr_dir, wei_gut_plan)
    save_gut_file(x_vow_mstr_dir, zia_gut_plan)
    accord_vow._set_all_healer_dutys(yao_str)
    accord_vow._set_all_healer_dutys(wei_str)
    accord_vow._set_all_healer_dutys(zia_str)

    return accord_vow


def create_example_vow3() -> VowUnit:
    # ESTABLISH
    a45_str = "accord45"
    x_vow_mstr_dir = get_module_temp_dir()
    accord_vow = vowunit_shop(a45_str, x_vow_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    accord_vow.create_init_job_from_guts(yao_str)
    accord_vow.create_init_job_from_guts(wei_str)
    accord_vow.create_init_job_from_guts(zia_str)
    yao_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, yao_str)
    wei_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, wei_str)
    zia_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_rope = yao_gut_plan.make_l1_rope(casa_str)
    yao_gut_plan.set_l1_concept(conceptunit_shop(casa_str))
    wei_gut_plan.set_l1_concept(conceptunit_shop(casa_str))
    zia_gut_plan.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = yao_gut_plan.make_rope(casa_rope, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_plan.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    yao_gut_plan.set_concept(conceptunit_shop(bath_str, task=True), clean_rope)
    yao_gut_plan.set_concept(conceptunit_shop(hall_str, task=True), clean_rope)

    wei_gut_plan.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    wei_gut_plan.set_concept(conceptunit_shop(bath_str, task=True), clean_rope)

    zia_gut_plan.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    zia_gut_plan.set_concept(conceptunit_shop(bath_str, task=True), clean_rope)
    zia_gut_plan.set_concept(conceptunit_shop(hall_str, task=True), clean_rope)

    save_gut_file(x_vow_mstr_dir, yao_gut_plan)
    save_gut_file(x_vow_mstr_dir, wei_gut_plan)
    save_gut_file(x_vow_mstr_dir, zia_gut_plan)

    return accord_vow


def create_example_vow4() -> VowUnit:
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a45_str = "accord45"
    accord_vow = vowunit_shop(a45_str, x_vow_mstr_dir, in_memory_journal=True)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    accord_vow.create_init_job_from_guts(yao_str)
    accord_vow.create_init_job_from_guts(wei_str)
    accord_vow.create_init_job_from_guts(zia_str)
    yao_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, yao_str)
    wei_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, wei_str)
    zia_gut_plan = open_gut_file(x_vow_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_rope = yao_gut_plan.make_l1_rope(casa_str)
    yao_gut_plan.set_l1_concept(conceptunit_shop(casa_str))
    wei_gut_plan.set_l1_concept(conceptunit_shop(casa_str))
    zia_gut_plan.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = yao_gut_plan.make_rope(casa_rope, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_plan.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    yao_gut_plan.set_concept(conceptunit_shop(bath_str, task=True), clean_rope)
    yao_gut_plan.set_concept(conceptunit_shop(hall_str, task=True), clean_rope)

    wei_gut_plan.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    wei_gut_plan.set_concept(conceptunit_shop(bath_str, task=True), clean_rope)

    zia_gut_plan.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    zia_gut_plan.set_concept(conceptunit_shop(bath_str, task=True), clean_rope)
    zia_gut_plan.set_concept(conceptunit_shop(hall_str, task=True), clean_rope)

    yao_gut_plan.set_credor_respect(101)
    wei_gut_plan.set_credor_respect(75)
    zia_gut_plan.set_credor_respect(52)
    yao_gut_plan.set_debtor_respect(1000)
    wei_gut_plan.set_debtor_respect(750)
    zia_gut_plan.set_debtor_respect(500)

    yao_gut_plan.add_acctunit(yao_str, 34, 600)
    yao_gut_plan.add_acctunit(zia_str, 57, 300)
    yao_gut_plan.add_acctunit(wei_str, 10, 100)
    wei_gut_plan.add_acctunit(yao_str, 37, 100)
    wei_gut_plan.add_acctunit(wei_str, 11, 400)
    wei_gut_plan.add_acctunit(zia_str, 27, 250)
    zia_gut_plan.add_acctunit(yao_str, 14, 100)
    zia_gut_plan.add_acctunit(zia_str, 38, 400)

    texas_str = "Texas"
    yao_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    wei_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    zia_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    save_gut_file(x_vow_mstr_dir, yao_gut_plan)
    save_gut_file(x_vow_mstr_dir, wei_gut_plan)
    save_gut_file(x_vow_mstr_dir, zia_gut_plan)

    return accord_vow


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    clean_rope = create_rope(floor_rope, "clean")
    return factunit_shop(floor_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    dirty_rope = create_rope(floor_rope, "dirty")
    return factunit_shop(floor_rope, dirty_rope)


def _example_empty_bob_planunit() -> PlanUnit:
    a23_str = "accord23"
    return planunit_shop("Bob", a23_str)


def get_bob_mop_without_reason_planunit_example() -> PlanUnit:
    bob_plan = _example_empty_bob_planunit()
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_plan.make_l1_rope(casa_str)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, clean_str)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, mop_str)
    bob_plan.add_concept(casa_rope, 1)
    bob_plan.add_concept(floor_rope, 1)
    bob_plan.add_concept(clean_rope, 1)
    bob_plan.add_concept(dirty_rope, 1)
    bob_plan.add_concept(mop_rope, 1, task=True)
    return bob_plan


def get_bob_mop_with_reason_planunit_example() -> PlanUnit:
    """owner_name: bob, vow_label: accord23"""
    bob_plan = get_bob_mop_without_reason_planunit_example()
    casa_str = "casa"
    floor_str = "floor status"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_plan.make_l1_rope(casa_str)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, mop_str)
    bob_plan.edit_concept_attr(
        mop_rope, reason_rcontext=floor_rope, reason_premise=dirty_rope
    )
    return bob_plan


def get_bob_mop_fact_clean_planunit_example() -> PlanUnit:
    bob_plan = get_bob_mop_with_reason_planunit_example()
    bob_plan.add_acctunit("Bob")
    casa_rope = bob_plan.make_l1_rope("casa")
    floor_rope = bob_plan.make_rope(casa_rope, "floor status")
    clean_rope = bob_plan.make_rope(floor_rope, "clean")
    bob_plan.add_fact(floor_rope, clean_rope)
    return bob_plan


def get_yao_run_with_reason_planunit_example() -> PlanUnit:
    yao_plan = planunit_shop("Yao", "accord23")
    sport_str = "sport"
    participate_str = "participate"
    ski_str = "skiing"
    run_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowng_str = "snowng"
    sport_rope = yao_plan.make_l1_rope(sport_str)
    participate_rope = yao_plan.make_rope(sport_rope, participate_str)
    ski_rope = yao_plan.make_rope(participate_rope, ski_str)
    run_rope = yao_plan.make_rope(participate_rope, run_str)
    weather_rope = yao_plan.make_l1_rope(weather_str)
    rain_rope = yao_plan.make_rope(weather_rope, raining_str)
    snow_rope = yao_plan.make_rope(weather_rope, snowng_str)
    yao_plan.add_concept(participate_rope)
    yao_plan.add_concept(ski_rope, 5, task=True)
    yao_plan.add_concept(run_rope, 1, task=True)
    yao_plan.add_concept(weather_rope)
    yao_plan.add_concept(rain_rope)
    yao_plan.add_concept(snow_rope)
    yao_plan.edit_concept_attr(
        ski_rope, reason_rcontext=weather_rope, reason_premise=snow_rope
    )
    yao_plan.edit_concept_attr(
        run_rope, reason_rcontext=weather_rope, reason_premise=rain_rope
    )
    return yao_plan


def get_yao_run_rain_fact_planunit_example() -> PlanUnit:
    yao_plan = get_yao_run_with_reason_planunit_example()
    weather_rope = yao_plan.make_l1_rope("weather")
    rain_rope = yao_plan.make_rope(weather_rope, "raining")
    yao_plan.add_fact(weather_rope, rain_rope)
    return yao_plan
