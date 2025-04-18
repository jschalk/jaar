from src.a01_word_logic.road import create_road
from src.a05_item_logic.healer import healerlink_shop
from src.a05_item_logic.item import itemunit_shop
from src.a04_reason_logic.reason_item import factunit_shop, FactUnit
from src.a06_bud_logic.bud import budunit_shop, BudUnit
from src.a12_hub_tools.hub_tool import save_gut_file, open_gut_file
from src.a15_fisc_logic.fisc import FiscUnit, fiscunit_shop
from src.a15_fisc_logic.examples.fisc_env import get_test_fisc_mstr_dir


def create_example_fisc2() -> FiscUnit:
    # ESTABLISH
    x_fisc_mstr_dir = get_test_fisc_mstr_dir()
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
    texas_road = yao_gut_bud.make_l1_road(texas_str)
    yao_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    wei_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    zia_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = yao_gut_bud.make_road(texas_road, dallas_str)
    dallas_healerlink = healerlink_shop({yao_str, zia_str})
    dallas_item = itemunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_road = yao_gut_bud.make_road(texas_road, elpaso_str)
    elpaso_healerlink = healerlink_shop({yao_str})
    elpaso_item = itemunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    yao_gut_bud.set_item(dallas_item, texas_road)
    yao_gut_bud.set_item(elpaso_item, texas_road)
    wei_gut_bud.set_item(dallas_item, texas_road)
    wei_gut_bud.set_item(elpaso_item, texas_road)
    zia_gut_bud.set_item(dallas_item, texas_road)
    zia_gut_bud.set_item(elpaso_item, texas_road)
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
    x_fisc_mstr_dir = get_test_fisc_mstr_dir()
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
    casa_road = yao_gut_bud.make_l1_road(casa_str)
    yao_gut_bud.set_l1_item(itemunit_shop(casa_str))
    wei_gut_bud.set_l1_item(itemunit_shop(casa_str))
    zia_gut_bud.set_l1_item(itemunit_shop(casa_str))
    clean_str = "clean"
    clean_road = yao_gut_bud.make_road(casa_road, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    yao_gut_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    yao_gut_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

    wei_gut_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    wei_gut_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)

    zia_gut_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    zia_gut_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    zia_gut_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

    save_gut_file(x_fisc_mstr_dir, yao_gut_bud)
    save_gut_file(x_fisc_mstr_dir, wei_gut_bud)
    save_gut_file(x_fisc_mstr_dir, zia_gut_bud)

    return accord_fisc


def create_example_fisc4() -> FiscUnit:
    # ESTABLISH
    x_fisc_mstr_dir = get_test_fisc_mstr_dir()
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
    casa_road = yao_gut_bud.make_l1_road(casa_str)
    yao_gut_bud.set_l1_item(itemunit_shop(casa_str))
    wei_gut_bud.set_l1_item(itemunit_shop(casa_str))
    zia_gut_bud.set_l1_item(itemunit_shop(casa_str))
    clean_str = "clean"
    clean_road = yao_gut_bud.make_road(casa_road, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    yao_gut_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    yao_gut_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

    wei_gut_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    wei_gut_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)

    zia_gut_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    zia_gut_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    zia_gut_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

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
    yao_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    wei_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    zia_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    save_gut_file(x_fisc_mstr_dir, yao_gut_bud)
    save_gut_file(x_fisc_mstr_dir, wei_gut_bud)
    save_gut_file(x_fisc_mstr_dir, zia_gut_bud)

    return accord_fisc


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_road = create_road(a23_str, "casa")
    floor_road = create_road(casa_road, "floor status")
    clean_road = create_road(floor_road, "clean")
    return factunit_shop(floor_road, clean_road)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_road = create_road(a23_str, "casa")
    floor_road = create_road(casa_road, "floor status")
    dirty_road = create_road(floor_road, "dirty")
    return factunit_shop(floor_road, dirty_road)


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
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    clean_road = bob_bud.make_road(floor_road, clean_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(casa_road, 1)
    bob_bud.add_item(floor_road, 1)
    bob_bud.add_item(clean_road, 1)
    bob_bud.add_item(dirty_road, 1)
    bob_bud.add_item(mop_road, 1, pledge=True)
    return bob_bud


def get_bob_mop_with_reason_budunit_example() -> BudUnit:
    """owner_name: bob, fisc_title: accord23"""
    bob_bud = get_bob_mop_without_reason_budunit_example()
    casa_str = "casa"
    floor_str = "floor status"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.edit_item_attr(mop_road, reason_base=floor_road, reason_premise=dirty_road)
    return bob_bud


def get_bob_mop_fact_clean_budunit_example() -> BudUnit:
    bob_bud = get_bob_mop_with_reason_budunit_example()
    bob_bud.add_acctunit("Bob")
    casa_road = bob_bud.make_l1_road("casa")
    floor_road = bob_bud.make_road(casa_road, "floor status")
    clean_road = bob_bud.make_road(floor_road, "clean")
    bob_bud.add_fact(floor_road, clean_road)
    return bob_bud


def get_yao_run_with_reason_budunit_example() -> BudUnit:
    yao_bud = budunit_shop("Yao", "accord23")
    sport_str = "sport"
    participate_str = "participate"
    ski_str = "skiing"
    run_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowing_str = "snowing"
    sport_road = yao_bud.make_l1_road(sport_str)
    participate_road = yao_bud.make_road(sport_road, participate_str)
    ski_road = yao_bud.make_road(participate_road, ski_str)
    run_road = yao_bud.make_road(participate_road, run_str)
    weather_road = yao_bud.make_l1_road(weather_str)
    rain_road = yao_bud.make_road(weather_road, raining_str)
    snow_road = yao_bud.make_road(weather_road, snowing_str)
    yao_bud.add_item(participate_road)
    yao_bud.add_item(ski_road, 5, pledge=True)
    yao_bud.add_item(run_road, 1, pledge=True)
    yao_bud.add_item(weather_road)
    yao_bud.add_item(rain_road)
    yao_bud.add_item(snow_road)
    yao_bud.edit_item_attr(ski_road, reason_base=weather_road, reason_premise=snow_road)
    yao_bud.edit_item_attr(run_road, reason_base=weather_road, reason_premise=rain_road)
    return yao_bud


def get_yao_run_rain_fact_budunit_example() -> BudUnit:
    yao_bud = get_yao_run_with_reason_budunit_example()
    weather_road = yao_bud.make_l1_road("weather")
    rain_road = yao_bud.make_road(weather_road, "raining")
    yao_bud.add_fact(weather_road, rain_road)
    return yao_bud
