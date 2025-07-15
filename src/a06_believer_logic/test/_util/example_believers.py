from src.a00_data_toolbox.file_toolbox import open_file
from src.a01_term_logic.rope import RopeTerm
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer import (
    BelieverUnit,
    believerunit_shop,
    get_from_json as believerunit_get_from_json,
)

# from src.a00_data_toolbox.file_toolbox import save_file
# from src.a06_believer_logic.test._util.a06_env import get_believer_examples_dir as env_dir
# from src.a06_believer_logic.test._util.example_believers import believerunit_v001, believerunit_v002

# save_file(env_dir(), "example_believer3.json", believerunit_v001().get_json())
# save_file(env_dir(), "example_believer4.json", believerunit_v002().get_json())


def believerunit_v001() -> BelieverUnit:
    believer1_path = "src/a06_believer_logic/test/_util/example_believer1.json"
    believer1_json = open_file(believer1_path)
    return believerunit_get_from_json(believer1_json)


def believerunit_v001_with_large_agenda() -> BelieverUnit:
    yao_believer = believerunit_v001()
    day_minute_rope = yao_believer.make_l1_rope("day_minute")
    month_wk_rope = yao_believer.make_l1_rope("month_wk")
    nations_rope = yao_believer.make_l1_rope("Nation-States")
    mood_rope = yao_believer.make_l1_rope("Moods")
    aaron_rope = yao_believer.make_l1_rope("Aaron Donald objects effected by him")
    yr_month_rope = yao_believer.make_l1_rope("yr_month")
    season_rope = yao_believer.make_l1_rope("Seasons")
    ced_wk_rope = yao_believer.make_l1_rope("ced_wk")
    wkdays_rope = yao_believer.make_l1_rope("wkdays")

    yao_believer.add_fact(aaron_rope, aaron_rope)
    yao_believer.add_fact(ced_wk_rope, ced_wk_rope, fopen=0, fnigh=53)
    yao_believer.add_fact(day_minute_rope, day_minute_rope, fopen=0, fnigh=1399)
    # yao_believer.add_fact(interweb, interweb)
    yao_believer.add_fact(month_wk_rope, month_wk_rope, fopen=0, fnigh=5)
    yao_believer.add_fact(mood_rope, mood_rope)
    # yao_believer.add_fact(movie, movie)
    yao_believer.add_fact(nations_rope, nations_rope)
    yao_believer.add_fact(season_rope, season_rope)
    yao_believer.add_fact(yr_month_rope, yr_month_rope, fopen=0, fnigh=12)
    # yao_believer.add_fact(water, water)
    yao_believer.add_fact(wkdays_rope, wkdays_rope)
    return yao_believer


def believerunit_v002() -> BelieverUnit:
    believer2_path = "src/a06_believer_logic/test/_util/example_believer2.json"
    return believerunit_get_from_json(open_file(believer2_path))


def get_believerunit_with_4_levels() -> BelieverUnit:
    a23_str = "amy23"
    sue_believer = believerunit_shop("Sue", a23_str)
    casa_str = "casa"
    sue_believer.set_l1_plan(planunit_shop(casa_str, mass=30, task=True))
    cat_str = "cat have dinner"
    sue_believer.set_l1_plan(planunit_shop(cat_str, mass=30, task=True))

    wk_str = "wkdays"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    plan_kid_wkdays = planunit_shop(wk_str, mass=40)
    sue_believer.set_l1_plan(plan_kid_wkdays)
    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sue_believer.set_plan(planunit_shop(sun_str, mass=20), wk_rope)
    sue_believer.set_plan(planunit_shop(mon_str, mass=20), wk_rope)
    sue_believer.set_plan(planunit_shop(tue_str, mass=20), wk_rope)
    sue_believer.set_plan(planunit_shop(wed_str, mass=20), wk_rope)
    sue_believer.set_plan(planunit_shop(thu_str, mass=30), wk_rope)
    sue_believer.set_plan(planunit_shop(fri_str, mass=40), wk_rope)
    sue_believer.set_plan(planunit_shop(sat_str, mass=50), wk_rope)

    nation_str = "nation"
    nation_rope = sue_believer.make_l1_rope(nation_str)
    plan_kid_nation = planunit_shop(nation_str, mass=30)
    sue_believer.set_l1_plan(plan_kid_nation)
    usa_str = "USA"
    usa_rope = sue_believer.make_rope(nation_rope, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    plan_grandkid_usa = planunit_shop(usa_str, mass=50)
    plan_grandkid_france = planunit_shop(france_str, mass=50)
    plan_grandkid_brazil = planunit_shop(brazil_str, mass=50)
    sue_believer.set_plan(plan_grandkid_france, nation_rope)
    sue_believer.set_plan(plan_grandkid_brazil, nation_rope)
    sue_believer.set_plan(plan_grandkid_usa, nation_rope)
    texas_str = "Texas"
    oregon_str = "Oregon"
    plan_grandgrandkid_usa_texas = planunit_shop(texas_str, mass=50)
    plan_grandgrandkid_usa_oregon = planunit_shop(oregon_str, mass=50)
    sue_believer.set_plan(plan_grandgrandkid_usa_texas, usa_rope)
    sue_believer.set_plan(plan_grandgrandkid_usa_oregon, usa_rope)
    return sue_believer


def get_believerunit_with_4_levels_and_2reasons() -> BelieverUnit:
    sue_believer = get_believerunit_with_4_levels()
    wk_str = "wkdays"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    wed_str = "Wednesday"
    wed_rope = sue_believer.make_rope(wk_rope, wed_str)
    wk_reason = reasonunit_shop(wk_rope)
    wk_reason.set_premise(wed_rope)

    nation_str = "nation"
    nation_rope = sue_believer.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_believer.make_rope(nation_rope, usa_str)
    nation_reason = reasonunit_shop(nation_rope)
    nation_reason.set_premise(usa_rope)

    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sue_believer.edit_plan_attr(casa_rope, reason=wk_reason)
    sue_believer.edit_plan_attr(casa_rope, reason=nation_reason)
    return sue_believer


def get_believerunit_with_4_levels_and_2reasons_2facts() -> BelieverUnit:
    sue_believer = get_believerunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    wed_str = "Wednesday"
    wed_rope = sue_believer.make_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = sue_believer.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_believer.make_rope(nation_rope, usa_str)
    sue_believer.add_fact(fcontext=wk_rope, fstate=wed_rope)
    sue_believer.add_fact(fcontext=nation_rope, fstate=usa_rope)
    return sue_believer


def get_believerunit_with7amCleanTableReason() -> BelieverUnit:
    sue_believer = get_believerunit_with_4_levels_and_2reasons_2facts()

    time_str = "timetech"
    time_rope = sue_believer.make_l1_rope(time_str)
    time_plan = planunit_shop(time_str)

    day24hr_str = "24hr day"
    day24hr_rope = sue_believer.make_rope(time_rope, day24hr_str)
    day24hr_plan = planunit_shop(day24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_rope = sue_believer.make_rope(day24hr_rope, am_str)
    pm_str = "pm"
    n1_str = "1"
    n2_str = "2"
    n3_str = "3"
    am_plan = planunit_shop(am_str, gogo_want=0, stop_want=12)
    pm_plan = planunit_shop(pm_str, gogo_want=12, stop_want=24)
    n1_plan = planunit_shop(n1_str, gogo_want=1, stop_want=2)
    n2_plan = planunit_shop(n2_str, gogo_want=2, stop_want=3)
    n3_plan = planunit_shop(n3_str, gogo_want=3, stop_want=4)

    sue_believer.set_l1_plan(time_plan)
    sue_believer.set_plan(day24hr_plan, time_rope)
    sue_believer.set_plan(am_plan, day24hr_rope)
    sue_believer.set_plan(pm_plan, day24hr_rope)
    sue_believer.set_plan(n1_plan, am_rope)  # plan_am
    sue_believer.set_plan(n2_plan, am_rope)  # plan_am
    sue_believer.set_plan(n3_plan, am_rope)  # plan_am

    house_str = "housemanagement"
    house_rope = sue_believer.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_believer.make_rope(house_rope, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_rope = sue_believer.make_rope(clean_rope, soap_str)
    grab_str = "grab soap"
    grab_rope = sue_believer.make_rope(soap_rope, grab_str)
    house_plan = planunit_shop(house_str)
    clean_plan = planunit_shop(clean_str, task=True)
    dish_plan = planunit_shop(dish_str, task=True)
    soap_plan = planunit_shop(soap_str, task=True)
    grab_plan = planunit_shop(grab_str, task=True)

    sue_believer.set_l1_plan(house_plan)
    sue_believer.set_plan(clean_plan, house_rope)
    sue_believer.set_plan(dish_plan, clean_rope)
    sue_believer.set_plan(soap_plan, clean_rope)
    sue_believer.set_plan(grab_plan, soap_rope)

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
    sue_believer.edit_plan_attr(clean_rope, reason=clean_table_7am_reason)
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sue_believer.edit_plan_attr(casa_rope, reason=clean_table_7am_reason)
    return sue_believer


def get_believerunit_1Chore_1CE0MinutesReason_1Fact() -> BelieverUnit:
    yao_believer = believerunit_shop("Yao")
    hr_min_str = "hr"
    hr_min_plan = planunit_shop(hr_min_str)
    hr_rope = yao_believer.make_l1_rope(hr_min_str)
    hr_reasonunit = reasonunit_shop(hr_rope)
    hr_reasonunit.set_premise(hr_rope, popen=80, pnigh=90)
    yao_believer.set_l1_plan(hr_min_plan)
    yao_believer.add_fact(hr_rope, hr_rope, 85, 95)
    mail_str = "obtain mail"
    mail_rope = yao_believer.make_l1_rope(mail_str)
    mail_plan = planunit_shop(mail_str, task=True)
    yao_believer.set_l1_plan(mail_plan)
    yao_believer.edit_plan_attr(mail_rope, reason=hr_reasonunit)
    return yao_believer


def get_believerunit_x1_3levels_1reason_1facts() -> BelieverUnit:
    tiger_str = "tiger"
    zia_believer = believerunit_shop("Zia", belief_label=tiger_str)
    shave_str = "shave"
    shave_rope = zia_believer.make_l1_rope(shave_str)
    plan_kid_shave = planunit_shop(shave_str, mass=30, task=True)
    zia_believer.set_l1_plan(plan_kid_shave)
    wk_str = "wkdays"
    wk_rope = zia_believer.make_l1_rope(wk_str)
    wk_plan = planunit_shop(wk_str, mass=40)
    zia_believer.set_l1_plan(wk_plan)

    sun_str = "Sunday"
    sun_rope = zia_believer.make_rope(wk_rope, sun_str)
    church_str = "Church"
    church_rope = zia_believer.make_rope(sun_rope, church_str)
    mon_str = "Monday"
    mon_rope = zia_believer.make_rope(wk_rope, mon_str)
    plan_grandkidU = planunit_shop(sun_str, mass=20)
    plan_grandkidM = planunit_shop(mon_str, mass=20)
    zia_believer.set_plan(plan_grandkidU, wk_rope)
    zia_believer.set_plan(plan_grandkidM, wk_rope)

    shave_reason = reasonunit_shop(wk_rope)
    shave_reason.set_premise(mon_rope)

    zia_believer.edit_plan_attr(shave_rope, reason=shave_reason)
    zia_believer.add_fact(fcontext=wk_rope, fstate=sun_rope)
    x_factunit = factunit_shop(fcontext=wk_rope, fstate=church_rope)
    zia_believer.edit_plan_attr(shave_rope, factunit=x_factunit)
    return zia_believer


def get_believerunit_rcontext_time_example() -> BelieverUnit:
    sue_believer = believerunit_shop("Sue")
    sue_believer.set_l1_plan(planunit_shop("casa"))
    return sue_believer


def get_believerunit_irrational_example() -> BelieverUnit:
    # this believer has no definitive agenda because 2 task plans are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_believer.settle_believer these should be true:
    # 1. hatter_believer._irrational is True
    # 2. hatter_believer._tree_traverse_count = hatter_believer.max_tree_traverse

    hatter_believer = believerunit_shop("Mad Hatter")
    hatter_believer.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_believer.make_l1_rope(egg_str)
    hatter_believer.set_l1_plan(planunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_rope = hatter_believer.make_l1_rope(chicken_str)
    hatter_believer.set_l1_plan(planunit_shop(chicken_str))

    # set egg task is True when chicken first is False
    hatter_believer.edit_plan_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rplan_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_believer.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rplan_active_requisite=False,
    )

    return hatter_believer


def get_mop_with_reason_believerunit_example1():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_believer.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, task=True)
    sue_believer.set_plan(floor_plan, casa_rope)
    sue_believer.set_l1_plan(planunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_rope = sue_believer.make_rope(casa_rope, status_str)
    sue_believer.set_plan(planunit_shop(status_str), casa_rope)

    clean_str = "clean"
    clean_rope = sue_believer.make_rope(status_rope, clean_str)
    sue_believer.set_plan(planunit_shop(clean_str), status_rope)
    sue_believer.set_plan(planunit_shop("very_much"), clean_rope)
    sue_believer.set_plan(planunit_shop("moderately"), clean_rope)
    sue_believer.set_plan(planunit_shop("dirty"), status_rope)

    floor_reason = reasonunit_shop(status_rope)
    floor_reason.set_premise(premise=status_rope)
    sue_believer.edit_plan_attr(floor_rope, reason=floor_reason)
    return sue_believer


def get_believerunit_laundry_example1() -> BelieverUnit:
    amos_str = "Amos"
    amos_believer = believerunit_shop(amos_str)
    cali_str = "Cali"
    amos_believer.add_partnerunit(amos_str)
    amos_believer.add_partnerunit(cali_str)

    casa_str = "casa"
    basket_str = "laundry basket status"
    b_full_str = "full"
    b_smel_str = "smelly"
    b_bare_str = "bare"
    b_fine_str = "fine"
    b_half_str = "half full"
    do_laundry_str = "do_laundry"
    casa_rope = amos_believer.make_l1_rope(casa_str)
    basket_rope = amos_believer.make_rope(casa_rope, basket_str)
    b_full_rope = amos_believer.make_rope(basket_rope, b_full_str)
    b_smel_rope = amos_believer.make_rope(basket_rope, b_smel_str)
    laundry_chore_rope = amos_believer.make_rope(casa_rope, do_laundry_str)
    amos_believer.set_l1_plan(planunit_shop(casa_str))
    amos_believer.set_plan(planunit_shop(basket_str), casa_rope)
    amos_believer.set_plan(planunit_shop(b_full_str), basket_rope)
    amos_believer.set_plan(planunit_shop(b_smel_str), basket_rope)
    amos_believer.set_plan(planunit_shop(b_bare_str), basket_rope)
    amos_believer.set_plan(planunit_shop(b_fine_str), basket_rope)
    amos_believer.set_plan(planunit_shop(b_half_str), basket_rope)
    amos_believer.set_plan(planunit_shop(do_laundry_str, task=True), casa_rope)

    # laundry requirement
    amos_believer.edit_plan_attr(
        laundry_chore_rope, reason_rcontext=basket_rope, reason_premise=b_full_rope
    )
    # laundry requirement
    amos_believer.edit_plan_attr(
        laundry_chore_rope, reason_rcontext=basket_rope, reason_premise=b_smel_rope
    )
    cali_laborunit = laborunit_shop()
    cali_laborunit.set_laborlink(cali_str)
    amos_believer.edit_plan_attr(laundry_chore_rope, laborunit=cali_laborunit)
    amos_believer.add_fact(fcontext=basket_rope, fstate=b_full_rope)

    return amos_believer


# class YR:
def from_list_get_active(
    rope: RopeTerm, plan_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_plan = None

    active_true_count = 0
    active_false_count = 0
    for plan in plan_dict.values():
        if plan.get_plan_rope() == rope:
            temp_plan = plan
            print(f"s for PlanUnit {temp_plan.get_plan_rope()}  {temp_plan._active=}")

        if plan._active:
            active_true_count += 1
        elif plan._active is False:
            active_false_count += 1

    active = temp_plan._active
    print(
        f"Set active: {plan.plan_label=} {active} {active_true_count=} {active_false_count=}"
    )

    return active
