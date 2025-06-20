from src.a00_data_toolbox.file_toolbox import open_file
from src.a01_term_logic.rope import RopeTerm
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import (
    PlanUnit,
    get_from_json as planunit_get_from_json,
    planunit_shop,
)


def planunit_v001() -> PlanUnit:
    plan1_path = "src/a06_plan_logic/test/_util/example_plan1.json"
    plan1_json = open_file(plan1_path)
    return planunit_get_from_json(plan1_json)


def planunit_v001_with_large_agenda() -> PlanUnit:
    yao_plan = planunit_v001()
    day_minute_rope = yao_plan.make_l1_rope("day_minute")
    month_wk_rope = yao_plan.make_l1_rope("month_wk")
    nations_rope = yao_plan.make_l1_rope("Nation-States")
    mood_rope = yao_plan.make_l1_rope("Moods")
    aaron_rope = yao_plan.make_l1_rope("Aaron Donald objects effected by him")
    yr_month_rope = yao_plan.make_l1_rope("yr_month")
    season_rope = yao_plan.make_l1_rope("Seasons")
    ced_wk_rope = yao_plan.make_l1_rope("ced_wk")
    wkdays_rope = yao_plan.make_l1_rope("wkdays")

    yao_plan.add_fact(aaron_rope, aaron_rope)
    yao_plan.add_fact(ced_wk_rope, ced_wk_rope, fopen=0, fnigh=53)
    yao_plan.add_fact(day_minute_rope, day_minute_rope, fopen=0, fnigh=1399)
    # yao_plan.add_fact(interweb, interweb)
    yao_plan.add_fact(month_wk_rope, month_wk_rope, fopen=0, fnigh=5)
    yao_plan.add_fact(mood_rope, mood_rope)
    # yao_plan.add_fact(movie, movie)
    yao_plan.add_fact(nations_rope, nations_rope)
    yao_plan.add_fact(season_rope, season_rope)
    yao_plan.add_fact(yr_month_rope, yr_month_rope, fopen=0, fnigh=12)
    # yao_plan.add_fact(water, water)
    yao_plan.add_fact(wkdays_rope, wkdays_rope)
    return yao_plan


def planunit_v002() -> PlanUnit:
    plan2_path = "src/a06_plan_logic/test/_util/example_plan2.json"
    return planunit_get_from_json(open_file(plan2_path))


def get_planunit_with_4_levels() -> PlanUnit:
    a23_str = "accord23"
    sue_plan = planunit_shop("Sue", a23_str)
    casa_str = "casa"
    sue_plan.set_l1_concept(conceptunit_shop(casa_str, mass=30, task=True))
    cat_str = "cat have dinner"
    sue_plan.set_l1_concept(conceptunit_shop(cat_str, mass=30, task=True))

    wk_str = "wkdays"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    concept_kid_wkdays = conceptunit_shop(wk_str, mass=40)
    sue_plan.set_l1_concept(concept_kid_wkdays)
    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sue_plan.set_concept(conceptunit_shop(sun_str, mass=20), wk_rope)
    sue_plan.set_concept(conceptunit_shop(mon_str, mass=20), wk_rope)
    sue_plan.set_concept(conceptunit_shop(tue_str, mass=20), wk_rope)
    sue_plan.set_concept(conceptunit_shop(wed_str, mass=20), wk_rope)
    sue_plan.set_concept(conceptunit_shop(thu_str, mass=30), wk_rope)
    sue_plan.set_concept(conceptunit_shop(fri_str, mass=40), wk_rope)
    sue_plan.set_concept(conceptunit_shop(sat_str, mass=50), wk_rope)

    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    concept_kid_nation = conceptunit_shop(nation_str, mass=30)
    sue_plan.set_l1_concept(concept_kid_nation)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    concept_grandkid_usa = conceptunit_shop(usa_str, mass=50)
    concept_grandkid_france = conceptunit_shop(france_str, mass=50)
    concept_grandkid_brazil = conceptunit_shop(brazil_str, mass=50)
    sue_plan.set_concept(concept_grandkid_france, nation_rope)
    sue_plan.set_concept(concept_grandkid_brazil, nation_rope)
    sue_plan.set_concept(concept_grandkid_usa, nation_rope)
    texas_str = "Texas"
    oregon_str = "Oregon"
    concept_grandgrandkid_usa_texas = conceptunit_shop(texas_str, mass=50)
    concept_grandgrandkid_usa_oregon = conceptunit_shop(oregon_str, mass=50)
    sue_plan.set_concept(concept_grandgrandkid_usa_texas, usa_rope)
    sue_plan.set_concept(concept_grandgrandkid_usa_oregon, usa_rope)
    return sue_plan


def get_planunit_with_4_levels_and_2reasons() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels()
    wk_str = "wkdays"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wed_str = "Wednesday"
    wed_rope = sue_plan.make_rope(wk_rope, wed_str)
    wk_reason = reasonunit_shop(wk_rope)
    wk_reason.set_premise(wed_rope)

    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    nation_reason = reasonunit_shop(nation_rope)
    nation_reason.set_premise(usa_rope)

    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    sue_plan.edit_concept_attr(casa_rope, reason=wk_reason)
    sue_plan.edit_concept_attr(casa_rope, reason=nation_reason)
    return sue_plan


def get_planunit_with_4_levels_and_2reasons_2facts() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wed_str = "Wednesday"
    wed_rope = sue_plan.make_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    sue_plan.add_fact(fcontext=wk_rope, fstate=wed_rope)
    sue_plan.add_fact(fcontext=nation_rope, fstate=usa_rope)
    return sue_plan


def get_planunit_with7amCleanTableReason() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels_and_2reasons_2facts()

    time_str = "timetech"
    time_rope = sue_plan.make_l1_rope(time_str)
    time_concept = conceptunit_shop(time_str)

    day24hr_str = "24hr day"
    day24hr_rope = sue_plan.make_rope(time_rope, day24hr_str)
    day24hr_concept = conceptunit_shop(day24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_rope = sue_plan.make_rope(day24hr_rope, am_str)
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
    sue_plan.set_concept(day24hr_concept, time_rope)
    sue_plan.set_concept(am_concept, day24hr_rope)
    sue_plan.set_concept(pm_concept, day24hr_rope)
    sue_plan.set_concept(n1_concept, am_rope)  # concept_am
    sue_plan.set_concept(n2_concept, am_rope)  # concept_am
    sue_plan.set_concept(n3_concept, am_rope)  # concept_am

    house_str = "housemanagement"
    house_rope = sue_plan.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_plan.make_rope(house_rope, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_rope = sue_plan.make_rope(clean_rope, soap_str)
    grab_str = "grab soap"
    grab_rope = sue_plan.make_rope(soap_rope, grab_str)
    house_concept = conceptunit_shop(house_str)
    clean_concept = conceptunit_shop(clean_str, task=True)
    dish_concept = conceptunit_shop(dish_str, task=True)
    soap_concept = conceptunit_shop(soap_str, task=True)
    grab_concept = conceptunit_shop(grab_str, task=True)

    sue_plan.set_l1_concept(house_concept)
    sue_plan.set_concept(clean_concept, house_rope)
    sue_plan.set_concept(dish_concept, clean_rope)
    sue_plan.set_concept(soap_concept, clean_rope)
    sue_plan.set_concept(grab_concept, soap_rope)

    clean_table_7am_rcontext = day24hr_rope
    clean_table_7am_premise_rope = day24hr_rope
    clean_table_7am_popen = 7.0
    clean_table_7am_pnigh = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_rcontext)
    clean_table_7am_reason.set_premise(
        premise=clean_table_7am_premise_rope,
        popen=clean_table_7am_popen,
        pnigh=clean_table_7am_pnigh,
    )
    sue_plan.edit_concept_attr(clean_rope, reason=clean_table_7am_reason)
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    sue_plan.edit_concept_attr(casa_rope, reason=clean_table_7am_reason)
    return sue_plan


def get_planunit_1Chore_1CE0MinutesReason_1Fact() -> PlanUnit:
    yao_plan = planunit_shop("Yao")
    hr_min_str = "hr"
    hr_min_concept = conceptunit_shop(hr_min_str)
    hr_rope = yao_plan.make_l1_rope(hr_min_str)
    hr_reasonunit = reasonunit_shop(hr_rope)
    hr_reasonunit.set_premise(hr_rope, popen=80, pnigh=90)
    yao_plan.set_l1_concept(hr_min_concept)
    yao_plan.add_fact(hr_rope, hr_rope, 85, 95)
    mail_str = "obtain mail"
    mail_rope = yao_plan.make_l1_rope(mail_str)
    mail_concept = conceptunit_shop(mail_str, task=True)
    yao_plan.set_l1_concept(mail_concept)
    yao_plan.edit_concept_attr(mail_rope, reason=hr_reasonunit)
    return yao_plan


def get_planunit_x1_3levels_1reason_1facts() -> PlanUnit:
    tiger_str = "tiger"
    zia_plan = planunit_shop("Zia", vow_label=tiger_str)
    shave_str = "shave"
    shave_rope = zia_plan.make_l1_rope(shave_str)
    concept_kid_shave = conceptunit_shop(shave_str, mass=30, task=True)
    zia_plan.set_l1_concept(concept_kid_shave)
    wk_str = "wkdays"
    wk_rope = zia_plan.make_l1_rope(wk_str)
    wk_concept = conceptunit_shop(wk_str, mass=40)
    zia_plan.set_l1_concept(wk_concept)

    sun_str = "Sunday"
    sun_rope = zia_plan.make_rope(wk_rope, sun_str)
    church_str = "Church"
    church_rope = zia_plan.make_rope(sun_rope, church_str)
    mon_str = "Monday"
    mon_rope = zia_plan.make_rope(wk_rope, mon_str)
    concept_grandkidU = conceptunit_shop(sun_str, mass=20)
    concept_grandkidM = conceptunit_shop(mon_str, mass=20)
    zia_plan.set_concept(concept_grandkidU, wk_rope)
    zia_plan.set_concept(concept_grandkidM, wk_rope)

    shave_reason = reasonunit_shop(wk_rope)
    shave_reason.set_premise(mon_rope)

    zia_plan.edit_concept_attr(shave_rope, reason=shave_reason)
    zia_plan.add_fact(fcontext=wk_rope, fstate=sun_rope)
    x_factunit = factunit_shop(fcontext=wk_rope, fstate=church_rope)
    zia_plan.edit_concept_attr(shave_rope, factunit=x_factunit)
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
    egg_rope = hatter_plan.make_l1_rope(egg_str)
    hatter_plan.set_l1_concept(conceptunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_rope = hatter_plan.make_l1_rope(chicken_str)
    hatter_plan.set_l1_concept(conceptunit_shop(chicken_str))

    # set egg task is True when chicken first is False
    hatter_plan.edit_concept_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rconcept_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_plan.edit_concept_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rconcept_active_requisite=False,
    )

    return hatter_plan


def get_mop_with_reason_planunit_example1():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_plan.make_rope(casa_rope, floor_str)
    floor_concept = conceptunit_shop(floor_str, task=True)
    sue_plan.set_concept(floor_concept, casa_rope)
    sue_plan.set_l1_concept(conceptunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_rope = sue_plan.make_rope(casa_rope, status_str)
    sue_plan.set_concept(conceptunit_shop(status_str), casa_rope)

    clean_str = "clean"
    clean_rope = sue_plan.make_rope(status_rope, clean_str)
    sue_plan.set_concept(conceptunit_shop(clean_str), status_rope)
    sue_plan.set_concept(conceptunit_shop("very_much"), clean_rope)
    sue_plan.set_concept(conceptunit_shop("moderately"), clean_rope)
    sue_plan.set_concept(conceptunit_shop("dirty"), status_rope)

    floor_reason = reasonunit_shop(status_rope)
    floor_reason.set_premise(premise=status_rope)
    sue_plan.edit_concept_attr(floor_rope, reason=floor_reason)
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
    casa_rope = amos_plan.make_l1_rope(casa_str)
    basket_rope = amos_plan.make_rope(casa_rope, basket_str)
    b_full_rope = amos_plan.make_rope(basket_rope, b_full_str)
    b_smel_rope = amos_plan.make_rope(basket_rope, b_smel_str)
    laundry_chore_rope = amos_plan.make_rope(casa_rope, do_laundry_str)
    amos_plan.set_l1_concept(conceptunit_shop(casa_str))
    amos_plan.set_concept(conceptunit_shop(basket_str), casa_rope)
    amos_plan.set_concept(conceptunit_shop(b_full_str), basket_rope)
    amos_plan.set_concept(conceptunit_shop(b_smel_str), basket_rope)
    amos_plan.set_concept(conceptunit_shop(b_bare_str), basket_rope)
    amos_plan.set_concept(conceptunit_shop(b_fine_str), basket_rope)
    amos_plan.set_concept(conceptunit_shop(b_half_str), basket_rope)
    amos_plan.set_concept(conceptunit_shop(do_laundry_str, task=True), casa_rope)

    # laundry requirement
    amos_plan.edit_concept_attr(
        laundry_chore_rope, reason_rcontext=basket_rope, reason_premise=b_full_rope
    )
    # laundry requirement
    amos_plan.edit_concept_attr(
        laundry_chore_rope, reason_rcontext=basket_rope, reason_premise=b_smel_rope
    )
    cali_laborunit = laborunit_shop()
    cali_laborunit.set_laborlink(cali_str)
    amos_plan.edit_concept_attr(laundry_chore_rope, laborunit=cali_laborunit)
    amos_plan.add_fact(fcontext=basket_rope, fstate=b_full_rope)

    return amos_plan


# class YR:
def from_list_get_active(
    rope: RopeTerm, concept_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_concept = None

    active_true_count = 0
    active_false_count = 0
    for concept in concept_dict.values():
        if concept.get_concept_rope() == rope:
            temp_concept = concept
            print(
                f"s for ConceptUnit {temp_concept.get_concept_rope()}  {temp_concept._active=}"
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
