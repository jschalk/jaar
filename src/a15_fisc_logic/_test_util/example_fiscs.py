from src.a01_term_logic.way import create_way
from src.a04_reason_logic.reason_concept import FactUnit, factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_bud_logic.bud import BudUnit, budunit_shop
from src.a12_hub_tools.hub_tool import open_gut_file, save_gut_file
from src.a15_fisc_logic._test_util.a15_env import get_module_temp_dir
from src.a15_fisc_logic.fisc import FiscUnit, fiscunit_shop


def create_example_fisc2() -> FiscUnit:
    # ESTABLISH
    x_fisc_mstr_dir = get_module_temp_dir()
    a45_str = "accord45"
    accord_fisc = fiscunit_shop(a45_str, x_fisc_mstr_dir, in_memory_journal=True)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    accord_fisc.create_init_job_from_guts(yao_str)
    accord_fisc.create_init_job_from_guts(wei_str)
    accord_fisc.create_init_job_from_guts(zia_str)
    yao_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, yao_str)
    wei_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, wei_str)
    zia_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, zia_str)

    yao_gut_bud.set_credor_respect(101)
    wei_gut_bud.set_credor_respect(75)
    zia_gut_bud.set_credor_respect(52)
    yao_gut_bud.set_debtor_respect(1000)
    wei_gut_bud.set_debtor_respect(750)
    zia_gut_bud.set_debtor_respect(500)

    yao_gut_bud.add_acctunit(yao_str, 34, 600)
    yao_gut_bud.add_acctunit(zia_str, 57, 300)
    yao_gut_bud.add_acctunit(wei_str, 10, 100)
    wei_gut_bud.add_acctunit(yao_str, 37, 100)
    wei_gut_bud.add_acctunit(wei_str, 11, 400)
    wei_gut_bud.add_acctunit(zia_str, 27, 250)
    zia_gut_bud.add_acctunit(yao_str, 14, 100)
    zia_gut_bud.add_acctunit(zia_str, 38, 400)
    texas_str = "Texas"
    texas_way = yao_gut_bud.make_l1_way(texas_str)
    yao_gut_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    wei_gut_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    zia_gut_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_way = yao_gut_bud.make_way(texas_way, dallas_str)
    dallas_healerlink = healerlink_shop({yao_str, zia_str})
    dallas_concept = conceptunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_way = yao_gut_bud.make_way(texas_way, elpaso_str)
    elpaso_healerlink = healerlink_shop({yao_str})
    elpaso_concept = conceptunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    yao_gut_bud.set_concept(dallas_concept, texas_way)
    yao_gut_bud.set_concept(elpaso_concept, texas_way)
    wei_gut_bud.set_concept(dallas_concept, texas_way)
    wei_gut_bud.set_concept(elpaso_concept, texas_way)
    zia_gut_bud.set_concept(dallas_concept, texas_way)
    zia_gut_bud.set_concept(elpaso_concept, texas_way)
    save_gut_file(x_fisc_mstr_dir, yao_gut_bud)
    save_gut_file(x_fisc_mstr_dir, wei_gut_bud)
    save_gut_file(x_fisc_mstr_dir, zia_gut_bud)
    accord_fisc._set_all_healer_dutys(yao_str)
    accord_fisc._set_all_healer_dutys(wei_str)
    accord_fisc._set_all_healer_dutys(zia_str)

    return accord_fisc


def create_example_fisc3() -> FiscUnit:
    # ESTABLISH
    a45_str = "accord45"
    x_fisc_mstr_dir = get_module_temp_dir()
    accord_fisc = fiscunit_shop(a45_str, x_fisc_mstr_dir)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    accord_fisc.create_init_job_from_guts(yao_str)
    accord_fisc.create_init_job_from_guts(wei_str)
    accord_fisc.create_init_job_from_guts(zia_str)
    yao_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, yao_str)
    wei_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, wei_str)
    zia_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_way = yao_gut_bud.make_l1_way(casa_str)
    yao_gut_bud.set_l1_concept(conceptunit_shop(casa_str))
    wei_gut_bud.set_l1_concept(conceptunit_shop(casa_str))
    zia_gut_bud.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_way = yao_gut_bud.make_way(casa_way, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_bud.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)
    yao_gut_bud.set_concept(conceptunit_shop(bath_str, pledge=True), clean_way)
    yao_gut_bud.set_concept(conceptunit_shop(hall_str, pledge=True), clean_way)

    wei_gut_bud.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)
    wei_gut_bud.set_concept(conceptunit_shop(bath_str, pledge=True), clean_way)

    zia_gut_bud.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)
    zia_gut_bud.set_concept(conceptunit_shop(bath_str, pledge=True), clean_way)
    zia_gut_bud.set_concept(conceptunit_shop(hall_str, pledge=True), clean_way)

    save_gut_file(x_fisc_mstr_dir, yao_gut_bud)
    save_gut_file(x_fisc_mstr_dir, wei_gut_bud)
    save_gut_file(x_fisc_mstr_dir, zia_gut_bud)

    return accord_fisc


def create_example_fisc4() -> FiscUnit:
    # ESTABLISH
    x_fisc_mstr_dir = get_module_temp_dir()
    a45_str = "accord45"
    accord_fisc = fiscunit_shop(a45_str, x_fisc_mstr_dir, in_memory_journal=True)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    accord_fisc.create_init_job_from_guts(yao_str)
    accord_fisc.create_init_job_from_guts(wei_str)
    accord_fisc.create_init_job_from_guts(zia_str)
    yao_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, yao_str)
    wei_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, wei_str)
    zia_gut_bud = open_gut_file(x_fisc_mstr_dir, a45_str, zia_str)

    casa_str = "casa"
    casa_way = yao_gut_bud.make_l1_way(casa_str)
    yao_gut_bud.set_l1_concept(conceptunit_shop(casa_str))
    wei_gut_bud.set_l1_concept(conceptunit_shop(casa_str))
    zia_gut_bud.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_way = yao_gut_bud.make_way(casa_way, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_bud.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)
    yao_gut_bud.set_concept(conceptunit_shop(bath_str, pledge=True), clean_way)
    yao_gut_bud.set_concept(conceptunit_shop(hall_str, pledge=True), clean_way)

    wei_gut_bud.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)
    wei_gut_bud.set_concept(conceptunit_shop(bath_str, pledge=True), clean_way)

    zia_gut_bud.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)
    zia_gut_bud.set_concept(conceptunit_shop(bath_str, pledge=True), clean_way)
    zia_gut_bud.set_concept(conceptunit_shop(hall_str, pledge=True), clean_way)

    yao_gut_bud.set_credor_respect(101)
    wei_gut_bud.set_credor_respect(75)
    zia_gut_bud.set_credor_respect(52)
    yao_gut_bud.set_debtor_respect(1000)
    wei_gut_bud.set_debtor_respect(750)
    zia_gut_bud.set_debtor_respect(500)

    yao_gut_bud.add_acctunit(yao_str, 34, 600)
    yao_gut_bud.add_acctunit(zia_str, 57, 300)
    yao_gut_bud.add_acctunit(wei_str, 10, 100)
    wei_gut_bud.add_acctunit(yao_str, 37, 100)
    wei_gut_bud.add_acctunit(wei_str, 11, 400)
    wei_gut_bud.add_acctunit(zia_str, 27, 250)
    zia_gut_bud.add_acctunit(yao_str, 14, 100)
    zia_gut_bud.add_acctunit(zia_str, 38, 400)

    texas_str = "Texas"
    yao_gut_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    wei_gut_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    zia_gut_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    save_gut_file(x_fisc_mstr_dir, yao_gut_bud)
    save_gut_file(x_fisc_mstr_dir, wei_gut_bud)
    save_gut_file(x_fisc_mstr_dir, zia_gut_bud)

    return accord_fisc


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    floor_way = create_way(casa_way, "floor status")
    clean_way = create_way(floor_way, "clean")
    return factunit_shop(floor_way, clean_way)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    floor_way = create_way(casa_way, "floor status")
    dirty_way = create_way(floor_way, "dirty")
    return factunit_shop(floor_way, dirty_way)


def _example_empty_bob_budunit() -> BudUnit:
    a23_str = "accord23"
    return budunit_shop("Bob", a23_str)


def get_bob_mop_without_reason_budunit_example() -> BudUnit:
    bob_bud = _example_empty_bob_budunit()
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = bob_bud.make_l1_way(casa_str)
    floor_way = bob_bud.make_way(casa_way, floor_str)
    clean_way = bob_bud.make_way(floor_way, clean_str)
    dirty_way = bob_bud.make_way(floor_way, dirty_str)
    mop_way = bob_bud.make_way(casa_way, mop_str)
    bob_bud.add_concept(casa_way, 1)
    bob_bud.add_concept(floor_way, 1)
    bob_bud.add_concept(clean_way, 1)
    bob_bud.add_concept(dirty_way, 1)
    bob_bud.add_concept(mop_way, 1, pledge=True)
    return bob_bud


def get_bob_mop_with_reason_budunit_example() -> BudUnit:
    """owner_name: bob, fisc_label: accord23"""
    bob_bud = get_bob_mop_without_reason_budunit_example()
    casa_str = "casa"
    floor_str = "floor status"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = bob_bud.make_l1_way(casa_str)
    floor_way = bob_bud.make_way(casa_way, floor_str)
    dirty_way = bob_bud.make_way(floor_way, dirty_str)
    mop_way = bob_bud.make_way(casa_way, mop_str)
    bob_bud.edit_concept_attr(
        mop_way, reason_rcontext=floor_way, reason_premise=dirty_way
    )
    return bob_bud


def get_bob_mop_fact_clean_budunit_example() -> BudUnit:
    bob_bud = get_bob_mop_with_reason_budunit_example()
    bob_bud.add_acctunit("Bob")
    casa_way = bob_bud.make_l1_way("casa")
    floor_way = bob_bud.make_way(casa_way, "floor status")
    clean_way = bob_bud.make_way(floor_way, "clean")
    bob_bud.add_fact(floor_way, clean_way)
    return bob_bud


def get_yao_run_with_reason_budunit_example() -> BudUnit:
    yao_bud = budunit_shop("Yao", "accord23")
    sport_str = "sport"
    participate_str = "participate"
    ski_str = "skiing"
    run_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowng_str = "snowng"
    sport_way = yao_bud.make_l1_way(sport_str)
    participate_way = yao_bud.make_way(sport_way, participate_str)
    ski_way = yao_bud.make_way(participate_way, ski_str)
    run_way = yao_bud.make_way(participate_way, run_str)
    weather_way = yao_bud.make_l1_way(weather_str)
    rain_way = yao_bud.make_way(weather_way, raining_str)
    snow_way = yao_bud.make_way(weather_way, snowng_str)
    yao_bud.add_concept(participate_way)
    yao_bud.add_concept(ski_way, 5, pledge=True)
    yao_bud.add_concept(run_way, 1, pledge=True)
    yao_bud.add_concept(weather_way)
    yao_bud.add_concept(rain_way)
    yao_bud.add_concept(snow_way)
    yao_bud.edit_concept_attr(
        ski_way, reason_rcontext=weather_way, reason_premise=snow_way
    )
    yao_bud.edit_concept_attr(
        run_way, reason_rcontext=weather_way, reason_premise=rain_way
    )
    return yao_bud


def get_yao_run_rain_fact_budunit_example() -> BudUnit:
    yao_bud = get_yao_run_with_reason_budunit_example()
    weather_way = yao_bud.make_l1_way("weather")
    rain_way = yao_bud.make_way(weather_way, "raining")
    yao_bud.add_fact(weather_way, rain_way)
    return yao_bud
