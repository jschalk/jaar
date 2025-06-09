from src.a00_data_toolbox.file_toolbox import open_file
from src.a01_term_logic.way import WayTerm
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import (
    PlanUnit,
    get_from_json as planunit_get_from_json,
    planunit_shop,
)


def planunit_v001() -> PlanUnit:
    plan1_path = "src/a06_plan_logic/_test_util/example_plan1.json"
    plan1_json = open_file(plan1_path)
    return planunit_get_from_json(plan1_json)


def planunit_v001_with_large_agenda() -> PlanUnit:
    yao_plan = planunit_v001()
    day_minute_way = yao_plan.make_l1_way("day_minute")
    month_wk_way = yao_plan.make_l1_way("month_wk")
    nations_way = yao_plan.make_l1_way("Nation-States")
    mood_way = yao_plan.make_l1_way("Moods")
    aaron_way = yao_plan.make_l1_way("Aaron Donald objects effected by him")
    yr_month_way = yao_plan.make_l1_way("yr_month")
    season_way = yao_plan.make_l1_way("Seasons")
    ced_wk_way = yao_plan.make_l1_way("ced_wk")
    wkdays_way = yao_plan.make_l1_way("wkdays")

    yao_plan.add_fact(aaron_way, aaron_way)
    yao_plan.add_fact(ced_wk_way, ced_wk_way, fopen=0, fnigh=53)
    yao_plan.add_fact(day_minute_way, day_minute_way, fopen=0, fnigh=1399)
    # yao_plan.add_fact(interweb, interweb)
    yao_plan.add_fact(month_wk_way, month_wk_way, fopen=0, fnigh=5)
    yao_plan.add_fact(mood_way, mood_way)
    # yao_plan.add_fact(movie, movie)
    yao_plan.add_fact(nations_way, nations_way)
    yao_plan.add_fact(season_way, season_way)
    yao_plan.add_fact(yr_month_way, yr_month_way, fopen=0, fnigh=12)
    # yao_plan.add_fact(water, water)
    yao_plan.add_fact(wkdays_way, wkdays_way)
    return yao_plan


def planunit_v002() -> PlanUnit:
    plan2_path = "src/a06_plan_logic/_test_util/example_plan2.json"
    return planunit_get_from_json(open_file(plan2_path))


def get_planunit_with_4_levels() -> PlanUnit:
    a23_str = "accord23"
    sue_plan = planunit_shop("Sue", a23_str)
    casa_str = "casa"
    sue_plan.set_l1_concept(conceptunit_shop(casa_str, mass=30, task=True))
    cat_str = "cat have dinner"
    sue_plan.set_l1_concept(conceptunit_shop(cat_str, mass=30, task=True))

    wk_str = "wkdays"
    wk_way = sue_plan.make_l1_way(wk_str)
    concept_kid_wkdays = conceptunit_shop(wk_str, mass=40)
    sue_plan.set_l1_concept(concept_kid_wkdays)
    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sue_plan.set_concept(conceptunit_shop(sun_str, mass=20), wk_way)
    sue_plan.set_concept(conceptunit_shop(mon_str, mass=20), wk_way)
    sue_plan.set_concept(conceptunit_shop(tue_str, mass=20), wk_way)
    sue_plan.set_concept(conceptunit_shop(wed_str, mass=20), wk_way)
    sue_plan.set_concept(conceptunit_shop(thu_str, mass=30), wk_way)
    sue_plan.set_concept(conceptunit_shop(fri_str, mass=40), wk_way)
    sue_plan.set_concept(conceptunit_shop(sat_str, mass=50), wk_way)

    nation_str = "nation"
    nation_way = sue_plan.make_l1_way(nation_str)
    concept_kid_nation = conceptunit_shop(nation_str, mass=30)
    sue_plan.set_l1_concept(concept_kid_nation)
    usa_str = "USA"
    usa_way = sue_plan.make_way(nation_way, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    concept_grandkid_usa = conceptunit_shop(usa_str, mass=50)
    concept_grandkid_france = conceptunit_shop(france_str, mass=50)
    concept_grandkid_brazil = conceptunit_shop(brazil_str, mass=50)
    sue_plan.set_concept(concept_grandkid_france, nation_way)
    sue_plan.set_concept(concept_grandkid_brazil, nation_way)
    sue_plan.set_concept(concept_grandkid_usa, nation_way)
    texas_str = "Texas"
    oregon_str = "Oregon"
    concept_grandgrandkid_usa_texas = conceptunit_shop(texas_str, mass=50)
    concept_grandgrandkid_usa_oregon = conceptunit_shop(oregon_str, mass=50)
    sue_plan.set_concept(concept_grandgrandkid_usa_texas, usa_way)
    sue_plan.set_concept(concept_grandgrandkid_usa_oregon, usa_way)
    return sue_plan


def get_planunit_with_4_levels_and_2reasons() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels()
    wk_str = "wkdays"
    wk_way = sue_plan.make_l1_way(wk_str)
    wed_str = "Wednesday"
    wed_way = sue_plan.make_way(wk_way, wed_str)
    wk_reason = reasonunit_shop(wk_way)
    wk_reason.set_premise(wed_way)

    nation_str = "nation"
    nation_way = sue_plan.make_l1_way(nation_str)
    usa_str = "USA"
    usa_way = sue_plan.make_way(nation_way, usa_str)
    nation_reason = reasonunit_shop(nation_way)
    nation_reason.set_premise(usa_way)

    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.edit_concept_attr(casa_way, reason=wk_reason)
    sue_plan.edit_concept_attr(casa_way, reason=nation_reason)
    return sue_plan


def get_planunit_with_4_levels_and_2reasons_2facts() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_way = sue_plan.make_l1_way(wk_str)
    wed_str = "Wednesday"
    wed_way = sue_plan.make_way(wk_way, wed_str)
    nation_str = "nation"
    nation_way = sue_plan.make_l1_way(nation_str)
    usa_str = "USA"
    usa_way = sue_plan.make_way(nation_way, usa_str)
    sue_plan.add_fact(fcontext=wk_way, fstate=wed_way)
    sue_plan.add_fact(fcontext=nation_way, fstate=usa_way)
    return sue_plan


def get_planunit_with7amCleanTableReason() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels_and_2reasons_2facts()

    time_str = "timetech"
    time_way = sue_plan.make_l1_way(time_str)
    time_concept = conceptunit_shop(time_str)

    day24hr_str = "24hr day"
    day24hr_way = sue_plan.make_way(time_way, day24hr_str)
    day24hr_concept = conceptunit_shop(day24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_way = sue_plan.make_way(day24hr_way, am_str)
    pm_str = "pm"
    n1_str = "1"
    n2_str = "2"
    n3_str = "3"
    am_concept = conceptunit_shop(am_str, gogo_want=0, stop_want=12)
    pm_concept = conceptunit_shop(pm_str, gogo_want=12, stop_want=24)
    n1_concept = conceptunit_shop(n1_str, gogo_want=1, stop_want=2)
    n2_concept = conceptunit_shop(n2_str, gogo_want=2, stop_want=3)
    n3_concept = conceptunit_shop(n3_str, gogo_want=3, stop_want=4)

    sue_plan.set_l1_concept(time_concept)
    sue_plan.set_concept(day24hr_concept, time_way)
    sue_plan.set_concept(am_concept, day24hr_way)
    sue_plan.set_concept(pm_concept, day24hr_way)
    sue_plan.set_concept(n1_concept, am_way)  # concept_am
    sue_plan.set_concept(n2_concept, am_way)  # concept_am
    sue_plan.set_concept(n3_concept, am_way)  # concept_am

    house_str = "housemanagement"
    house_way = sue_plan.make_l1_way(house_str)
    clean_str = "clean table"
    clean_way = sue_plan.make_way(house_way, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_way = sue_plan.make_way(clean_way, soap_str)
    grab_str = "grab soap"
    grab_way = sue_plan.make_way(soap_way, grab_str)
    house_concept = conceptunit_shop(house_str)
    clean_concept = conceptunit_shop(clean_str, task=True)
    dish_concept = conceptunit_shop(dish_str, task=True)
    soap_concept = conceptunit_shop(soap_str, task=True)
    grab_concept = conceptunit_shop(grab_str, task=True)

    sue_plan.set_l1_concept(house_concept)
    sue_plan.set_concept(clean_concept, house_way)
    sue_plan.set_concept(dish_concept, clean_way)
    sue_plan.set_concept(soap_concept, clean_way)
    sue_plan.set_concept(grab_concept, soap_way)

    clean_table_7am_rcontext = day24hr_way
    clean_table_7am_premise_way = day24hr_way
    clean_table_7am_popen = 7.0
    clean_table_7am_pnigh = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_rcontext)
    clean_table_7am_reason.set_premise(
        premise=clean_table_7am_premise_way,
        popen=clean_table_7am_popen,
        pnigh=clean_table_7am_pnigh,
    )
    sue_plan.edit_concept_attr(clean_way, reason=clean_table_7am_reason)
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.edit_concept_attr(casa_way, reason=clean_table_7am_reason)
    return sue_plan


def get_planunit_1Chore_1CE0MinutesReason_1Fact() -> PlanUnit:
    yao_plan = planunit_shop("Yao")
    hr_min_str = "hr"
    hr_min_concept = conceptunit_shop(hr_min_str)
    hr_way = yao_plan.make_l1_way(hr_min_str)
    hr_reasonunit = reasonunit_shop(hr_way)
    hr_reasonunit.set_premise(hr_way, popen=80, pnigh=90)
    yao_plan.set_l1_concept(hr_min_concept)
    yao_plan.add_fact(hr_way, hr_way, 85, 95)
    mail_str = "obtain mail"
    mail_way = yao_plan.make_l1_way(mail_str)
    mail_concept = conceptunit_shop(mail_str, task=True)
    yao_plan.set_l1_concept(mail_concept)
    yao_plan.edit_concept_attr(mail_way, reason=hr_reasonunit)
    return yao_plan


def get_planunit_x1_3levels_1reason_1facts() -> PlanUnit:
    tiger_str = "tiger"
    zia_plan = planunit_shop("Zia", vow_label=tiger_str)
    shave_str = "shave"
    shave_way = zia_plan.make_l1_way(shave_str)
    concept_kid_shave = conceptunit_shop(shave_str, mass=30, task=True)
    zia_plan.set_l1_concept(concept_kid_shave)
    wk_str = "wkdays"
    wk_way = zia_plan.make_l1_way(wk_str)
    wk_concept = conceptunit_shop(wk_str, mass=40)
    zia_plan.set_l1_concept(wk_concept)

    sun_str = "Sunday"
    sun_way = zia_plan.make_way(wk_way, sun_str)
    church_str = "Church"
    church_way = zia_plan.make_way(sun_way, church_str)
    mon_str = "Monday"
    mon_way = zia_plan.make_way(wk_way, mon_str)
    concept_grandkidU = conceptunit_shop(sun_str, mass=20)
    concept_grandkidM = conceptunit_shop(mon_str, mass=20)
    zia_plan.set_concept(concept_grandkidU, wk_way)
    zia_plan.set_concept(concept_grandkidM, wk_way)

    shave_reason = reasonunit_shop(wk_way)
    shave_reason.set_premise(mon_way)

    zia_plan.edit_concept_attr(shave_way, reason=shave_reason)
    zia_plan.add_fact(fcontext=wk_way, fstate=sun_way)
    x_factunit = factunit_shop(fcontext=wk_way, fstate=church_way)
    zia_plan.edit_concept_attr(shave_way, factunit=x_factunit)
    return zia_plan


def get_planunit_rcontext_time_example() -> PlanUnit:
    sue_plan = planunit_shop("Sue")
    sue_plan.set_l1_concept(conceptunit_shop("casa"))
    return sue_plan


def get_planunit_irrational_example() -> PlanUnit:
    # this plan has no definitive agenda because 2 task concepts are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_plan.settle_plan these should be true:
    # 1. hatter_plan._irrational is True
    # 2. hatter_plan._tree_traverse_count = hatter_plan.max_tree_traverse

    hatter_plan = planunit_shop("Mad Hatter")
    hatter_plan.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_way = hatter_plan.make_l1_way(egg_str)
    hatter_plan.set_l1_concept(conceptunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_way = hatter_plan.make_l1_way(chicken_str)
    hatter_plan.set_l1_concept(conceptunit_shop(chicken_str))

    # set egg task is True when chicken first is False
    hatter_plan.edit_concept_attr(
        egg_way,
        task=True,
        reason_rcontext=chicken_way,
        reason_rconcept_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_plan.edit_concept_attr(
        chicken_way,
        task=True,
        reason_rcontext=egg_way,
        reason_rconcept_active_requisite=False,
    )

    return hatter_plan


def get_mop_with_reason_planunit_example1():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    floor_str = "mop floor"
    floor_way = sue_plan.make_way(casa_way, floor_str)
    floor_concept = conceptunit_shop(floor_str, task=True)
    sue_plan.set_concept(floor_concept, casa_way)
    sue_plan.set_l1_concept(conceptunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_way = sue_plan.make_way(casa_way, status_str)
    sue_plan.set_concept(conceptunit_shop(status_str), casa_way)

    clean_str = "clean"
    clean_way = sue_plan.make_way(status_way, clean_str)
    sue_plan.set_concept(conceptunit_shop(clean_str), status_way)
    sue_plan.set_concept(conceptunit_shop("very_much"), clean_way)
    sue_plan.set_concept(conceptunit_shop("moderately"), clean_way)
    sue_plan.set_concept(conceptunit_shop("dirty"), status_way)

    floor_reason = reasonunit_shop(status_way)
    floor_reason.set_premise(premise=status_way)
    sue_plan.edit_concept_attr(floor_way, reason=floor_reason)
    return sue_plan


def get_planunit_laundry_example1() -> PlanUnit:
    amos_str = "Amos"
    amos_plan = planunit_shop(amos_str)
    cali_str = "Cali"
    amos_plan.add_acctunit(amos_str)
    amos_plan.add_acctunit(cali_str)

    casa_str = "casa"
    basket_str = "laundry basket status"
    b_full_str = "full"
    b_smel_str = "smelly"
    b_bare_str = "bare"
    b_fine_str = "fine"
    b_half_str = "half full"
    do_laundry_str = "do_laundry"
    casa_way = amos_plan.make_l1_way(casa_str)
    basket_way = amos_plan.make_way(casa_way, basket_str)
    b_full_way = amos_plan.make_way(basket_way, b_full_str)
    b_smel_way = amos_plan.make_way(basket_way, b_smel_str)
    laundry_chore_way = amos_plan.make_way(casa_way, do_laundry_str)
    amos_plan.set_l1_concept(conceptunit_shop(casa_str))
    amos_plan.set_concept(conceptunit_shop(basket_str), casa_way)
    amos_plan.set_concept(conceptunit_shop(b_full_str), basket_way)
    amos_plan.set_concept(conceptunit_shop(b_smel_str), basket_way)
    amos_plan.set_concept(conceptunit_shop(b_bare_str), basket_way)
    amos_plan.set_concept(conceptunit_shop(b_fine_str), basket_way)
    amos_plan.set_concept(conceptunit_shop(b_half_str), basket_way)
    amos_plan.set_concept(conceptunit_shop(do_laundry_str, task=True), casa_way)

    # laundry requirement
    amos_plan.edit_concept_attr(
        laundry_chore_way, reason_rcontext=basket_way, reason_premise=b_full_way
    )
    # laundry requirement
    amos_plan.edit_concept_attr(
        laundry_chore_way, reason_rcontext=basket_way, reason_premise=b_smel_way
    )
    cali_laborunit = laborunit_shop()
    cali_laborunit.set_laborlink(cali_str)
    amos_plan.edit_concept_attr(laundry_chore_way, laborunit=cali_laborunit)
    amos_plan.add_fact(fcontext=basket_way, fstate=b_full_way)

    return amos_plan


# class YR:
def from_list_get_active(
    way: WayTerm, concept_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_concept = None

    active_true_count = 0
    active_false_count = 0
    for concept in concept_dict.values():
        if concept.get_concept_way() == way:
            temp_concept = concept
            print(
                f"s for ConceptUnit {temp_concept.get_concept_way()}  {temp_concept._active=}"
            )

        if concept._active:
            active_true_count += 1
        elif concept._active is False:
            active_false_count += 1

    active = temp_concept._active
    print(
        f"Set active: {concept.concept_label=} {active} {active_true_count=} {active_false_count=}"
    )

    return active
