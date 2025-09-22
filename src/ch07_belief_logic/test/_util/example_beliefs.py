from src.ch00_data_toolbox.file_toolbox import open_file
from src.ch01_rope_logic.rope import RopePointer
from src.ch04_group_logic.labor import laborunit_shop
from src.ch05_reason_logic.reason import factunit_shop, reasonunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import (
    BeliefUnit,
    beliefunit_shop,
    get_from_json as beliefunit_get_from_json,
)

# from src.ch00_data_toolbox.file_toolbox import save_file
# from src.ch07_belief_logic.test._util.ch07_env import get_belief_examples_dir as env_dir
# from src.ch07_belief_logic.test._util.example_beliefs import beliefunit_v001, beliefunit_v002

# save_file(env_dir(), "example_belief3.json", beliefunit_v001().get_json())
# save_file(env_dir(), "example_belief4.json", beliefunit_v002().get_json())


def beliefunit_v001() -> BeliefUnit:
    belief1_path = "src/ch07_belief_logic/test/_util/example_belief1.json"
    belief1_json = open_file(belief1_path)
    return beliefunit_get_from_json(belief1_json)


def beliefunit_v001_with_large_agenda() -> BeliefUnit:
    yao_belief = beliefunit_v001()
    jour_minute_rope = yao_belief.make_l1_rope("jour_minute")
    month_wk_rope = yao_belief.make_l1_rope("month_wk")
    nations_rope = yao_belief.make_l1_rope("Nation-States")
    mood_rope = yao_belief.make_l1_rope("Moods")
    aaron_rope = yao_belief.make_l1_rope("Aaron Donald objects effected by him")
    yr_month_rope = yao_belief.make_l1_rope("yr_month")
    season_rope = yao_belief.make_l1_rope("Seasons")
    ced_wk_rope = yao_belief.make_l1_rope("ced_wk")
    sem_jours_rope = yao_belief.make_l1_rope("sem_jours")

    yao_belief.add_fact(aaron_rope, aaron_rope)
    yao_belief.add_fact(ced_wk_rope, ced_wk_rope, fact_lower=0, fact_upper=53)
    yao_belief.add_fact(
        jour_minute_rope, jour_minute_rope, fact_lower=0, fact_upper=1399
    )
    # yao_belief.add_fact(interweb, interweb)
    yao_belief.add_fact(month_wk_rope, month_wk_rope, fact_lower=0, fact_upper=5)
    yao_belief.add_fact(mood_rope, mood_rope)
    # yao_belief.add_fact(movie, movie)
    yao_belief.add_fact(nations_rope, nations_rope)
    yao_belief.add_fact(season_rope, season_rope)
    yao_belief.add_fact(yr_month_rope, yr_month_rope, fact_lower=0, fact_upper=12)
    # yao_belief.add_fact(water, water)
    yao_belief.add_fact(sem_jours_rope, sem_jours_rope)
    return yao_belief


def beliefunit_v002() -> BeliefUnit:
    belief2_path = "src/ch07_belief_logic/test/_util/example_belief2.json"
    return beliefunit_get_from_json(open_file(belief2_path))


def get_beliefunit_with_4_levels() -> BeliefUnit:
    # sourcery skip: extract-duplicate-method
    a23_str = "amy23"
    sue_belief = beliefunit_shop("Sue", a23_str)
    casa_str = "casa"
    sue_belief.set_l1_plan(planunit_shop(casa_str, star=30, task=True))
    cat_str = "cat have dinner"
    sue_belief.set_l1_plan(planunit_shop(cat_str, star=30, task=True))

    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    plan_kid_sem_jours = planunit_shop(wk_str, star=40)
    sue_belief.set_l1_plan(plan_kid_sem_jours)
    sun_str = "Sun"
    mon_str = "Mon"
    tue_str = "Tue"
    wed_str = "Wed"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sue_belief.set_plan(planunit_shop(sun_str, star=20), wk_rope)
    sue_belief.set_plan(planunit_shop(mon_str, star=20), wk_rope)
    sue_belief.set_plan(planunit_shop(tue_str, star=20), wk_rope)
    sue_belief.set_plan(planunit_shop(wed_str, star=20), wk_rope)
    sue_belief.set_plan(planunit_shop(thu_str, star=30), wk_rope)
    sue_belief.set_plan(planunit_shop(fri_str, star=40), wk_rope)
    sue_belief.set_plan(planunit_shop(sat_str, star=50), wk_rope)

    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    plan_kid_nation = planunit_shop(nation_str, star=30)
    sue_belief.set_l1_plan(plan_kid_nation)
    usa_str = "USA"
    usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    plan_grandkid_usa = planunit_shop(usa_str, star=50)
    plan_grandkid_france = planunit_shop(france_str, star=50)
    plan_grandkid_brazil = planunit_shop(brazil_str, star=50)
    sue_belief.set_plan(plan_grandkid_france, nation_rope)
    sue_belief.set_plan(plan_grandkid_brazil, nation_rope)
    sue_belief.set_plan(plan_grandkid_usa, nation_rope)
    texas_str = "Texas"
    oregon_str = "Oregon"
    plan_grandgrandkid_usa_texas = planunit_shop(texas_str, star=50)
    plan_grandgrandkid_usa_oregon = planunit_shop(oregon_str, star=50)
    sue_belief.set_plan(plan_grandgrandkid_usa_texas, usa_rope)
    sue_belief.set_plan(plan_grandgrandkid_usa_oregon, usa_rope)
    return sue_belief


def get_beliefunit_with_4_levels_and_2reasons() -> BeliefUnit:
    # sourcery skip: extract-duplicate-method
    sue_belief = get_beliefunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    wed_str = "Wed"
    wed_rope = sue_belief.make_rope(wk_rope, wed_str)
    wk_reason = reasonunit_shop(wk_rope)
    wk_reason.set_case(wed_rope)

    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    nation_reason = reasonunit_shop(nation_rope)
    nation_reason.set_case(usa_rope)

    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.edit_plan_attr(casa_rope, reason=wk_reason)
    sue_belief.edit_plan_attr(casa_rope, reason=nation_reason)
    return sue_belief


def get_beliefunit_with_4_levels_and_2reasons_2facts() -> BeliefUnit:
    sue_belief = get_beliefunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    wed_str = "Wed"
    wed_rope = sue_belief.make_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    sue_belief.add_fact(fact_context=wk_rope, fact_state=wed_rope)
    sue_belief.add_fact(fact_context=nation_rope, fact_state=usa_rope)
    return sue_belief


def get_beliefunit_with7amCleanTableReason() -> BeliefUnit:
    sue_belief = get_beliefunit_with_4_levels_and_2reasons_2facts()

    ziet_str = "ziettech"
    ziet_rope = sue_belief.make_l1_rope(ziet_str)
    ziet_plan = planunit_shop(ziet_str)

    x24hr_str = "24hr"
    x24hr_rope = sue_belief.make_rope(ziet_rope, x24hr_str)
    x24hr_plan = planunit_shop(x24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_rope = sue_belief.make_rope(x24hr_rope, am_str)
    pm_str = "pm"
    n1_str = "1"
    n2_str = "2"
    n3_str = "3"
    am_plan = planunit_shop(am_str, gogo_want=0, stop_want=12)
    pm_plan = planunit_shop(pm_str, gogo_want=12, stop_want=24)
    n1_plan = planunit_shop(n1_str, gogo_want=1, stop_want=2)
    n2_plan = planunit_shop(n2_str, gogo_want=2, stop_want=3)
    n3_plan = planunit_shop(n3_str, gogo_want=3, stop_want=4)

    sue_belief.set_l1_plan(ziet_plan)
    sue_belief.set_plan(x24hr_plan, ziet_rope)
    sue_belief.set_plan(am_plan, x24hr_rope)
    sue_belief.set_plan(pm_plan, x24hr_rope)
    sue_belief.set_plan(n1_plan, am_rope)  # plan_am
    sue_belief.set_plan(n2_plan, am_rope)  # plan_am
    sue_belief.set_plan(n3_plan, am_rope)  # plan_am

    house_str = "housemanagement"
    house_rope = sue_belief.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_belief.make_rope(house_rope, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_rope = sue_belief.make_rope(clean_rope, soap_str)
    grab_str = "grab soap"
    grab_rope = sue_belief.make_rope(soap_rope, grab_str)
    house_plan = planunit_shop(house_str)
    clean_plan = planunit_shop(clean_str, task=True)
    dish_plan = planunit_shop(dish_str, task=True)
    soap_plan = planunit_shop(soap_str, task=True)
    grab_plan = planunit_shop(grab_str, task=True)

    sue_belief.set_l1_plan(house_plan)
    sue_belief.set_plan(clean_plan, house_rope)
    sue_belief.set_plan(dish_plan, clean_rope)
    sue_belief.set_plan(soap_plan, clean_rope)
    sue_belief.set_plan(grab_plan, soap_rope)

    clean_table_7am_reason_context = x24hr_rope
    clean_table_7am_case_rope = x24hr_rope
    clean_table_7am_reason_lower = 7.0
    clean_table_7am_reason_upper = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_reason_context)
    clean_table_7am_reason.set_case(
        case=clean_table_7am_case_rope,
        reason_lower=clean_table_7am_reason_lower,
        reason_upper=clean_table_7am_reason_upper,
    )
    sue_belief.edit_plan_attr(clean_rope, reason=clean_table_7am_reason)
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.edit_plan_attr(casa_rope, reason=clean_table_7am_reason)
    return sue_belief


def get_beliefunit_1Chore_1CE0MinutesReason_1Fact() -> BeliefUnit:
    yao_belief = beliefunit_shop("Yao")
    hr_min_str = "hr"
    hr_min_plan = planunit_shop(hr_min_str)
    hr_rope = yao_belief.make_l1_rope(hr_min_str)
    hr_reasonunit = reasonunit_shop(hr_rope)
    hr_reasonunit.set_case(hr_rope, reason_lower=80, reason_upper=90)
    yao_belief.set_l1_plan(hr_min_plan)
    yao_belief.add_fact(hr_rope, hr_rope, 85, 95)
    mail_str = "obtain mail"
    mail_rope = yao_belief.make_l1_rope(mail_str)
    mail_plan = planunit_shop(mail_str, task=True)
    yao_belief.set_l1_plan(mail_plan)
    yao_belief.edit_plan_attr(mail_rope, reason=hr_reasonunit)
    return yao_belief


def get_beliefunit_x1_3levels_1reason_1facts() -> BeliefUnit:
    tiger_str = "tiger"
    zia_belief = beliefunit_shop("Zia", moment_label=tiger_str)
    shave_str = "shave"
    shave_rope = zia_belief.make_l1_rope(shave_str)
    plan_kid_shave = planunit_shop(shave_str, star=30, task=True)
    zia_belief.set_l1_plan(plan_kid_shave)
    wk_str = "sem_jours"
    wk_rope = zia_belief.make_l1_rope(wk_str)
    wk_plan = planunit_shop(wk_str, star=40)
    zia_belief.set_l1_plan(wk_plan)

    sun_str = "Sun"
    sun_rope = zia_belief.make_rope(wk_rope, sun_str)
    church_str = "Church"
    church_rope = zia_belief.make_rope(sun_rope, church_str)
    mon_str = "Mon"
    mon_rope = zia_belief.make_rope(wk_rope, mon_str)
    plan_grandkidU = planunit_shop(sun_str, star=20)
    plan_grandkidM = planunit_shop(mon_str, star=20)
    zia_belief.set_plan(plan_grandkidU, wk_rope)
    zia_belief.set_plan(plan_grandkidM, wk_rope)

    shave_reason = reasonunit_shop(wk_rope)
    shave_reason.set_case(mon_rope)

    zia_belief.edit_plan_attr(shave_rope, reason=shave_reason)
    zia_belief.add_fact(fact_context=wk_rope, fact_state=sun_rope)
    x_factunit = factunit_shop(fact_context=wk_rope, fact_state=church_rope)
    zia_belief.edit_plan_attr(shave_rope, factunit=x_factunit)
    return zia_belief


def get_beliefunit_reason_context_ziet_example() -> BeliefUnit:
    sue_belief = beliefunit_shop("Sue")
    sue_belief.set_l1_plan(planunit_shop("casa"))
    return sue_belief


def get_beliefunit_irrational_example() -> BeliefUnit:
    # sourcery skip: extract-duplicate-method
    # this belief has no definitive agenda because 2 task plans are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken.active is True, egg.active is set to False
    # Step 1: if egg.active is False, chicken.active is set to False
    # Step 2: if chicken.active is False, egg.active is set to True
    # Step 3: if egg.active is True, chicken.active is set to True
    # Step 4: back to step 0.
    # after hatter_belief.cashout these should be true:
    # 1. hatter_belief._irrational is True
    # 2. hatter_belief.tree_traverse_count = hatter_belief.max_tree_traverse

    hatter_belief = beliefunit_shop("Mad Hatter")
    hatter_belief.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_belief.make_l1_rope(egg_str)
    hatter_belief.set_l1_plan(planunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_rope = hatter_belief.make_l1_rope(chicken_str)
    hatter_belief.set_l1_plan(planunit_shop(chicken_str))

    # set egg task is True when chicken first is False
    hatter_belief.edit_plan_attr(
        egg_rope,
        task=True,
        reason_context=chicken_rope,
        reason_plan_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_belief.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_context=egg_rope,
        reason_plan_active_requisite=False,
    )

    return hatter_belief


def get_mop_with_reason_beliefunit_example1():
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_belief.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, task=True)
    sue_belief.set_plan(floor_plan, casa_rope)
    sue_belief.set_l1_plan(planunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_rope = sue_belief.make_rope(casa_rope, status_str)
    sue_belief.set_plan(planunit_shop(status_str), casa_rope)

    clean_str = "clean"
    clean_rope = sue_belief.make_rope(status_rope, clean_str)
    sue_belief.set_plan(planunit_shop(clean_str), status_rope)
    sue_belief.set_plan(planunit_shop("very_much"), clean_rope)
    sue_belief.set_plan(planunit_shop("moderately"), clean_rope)
    sue_belief.set_plan(planunit_shop("dirty"), status_rope)

    floor_reason = reasonunit_shop(status_rope)
    floor_reason.set_case(case=status_rope)
    sue_belief.edit_plan_attr(floor_rope, reason=floor_reason)
    return sue_belief


def get_beliefunit_laundry_example1() -> BeliefUnit:
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    cali_str = "Cali"
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(cali_str)

    casa_str = "casa"
    basket_str = "laundry basket status"
    b_full_str = "full"
    b_smel_str = "smelly"
    b_bare_str = "bare"
    b_fine_str = "fine"
    b_half_str = "half full"
    do_laundry_str = "do_laundry"
    casa_rope = yao_belief.make_l1_rope(casa_str)
    basket_rope = yao_belief.make_rope(casa_rope, basket_str)
    b_full_rope = yao_belief.make_rope(basket_rope, b_full_str)
    b_smel_rope = yao_belief.make_rope(basket_rope, b_smel_str)
    laundry_chore_rope = yao_belief.make_rope(casa_rope, do_laundry_str)
    yao_belief.set_l1_plan(planunit_shop(casa_str))
    yao_belief.set_plan(planunit_shop(basket_str), casa_rope)
    yao_belief.set_plan(planunit_shop(b_full_str), basket_rope)
    yao_belief.set_plan(planunit_shop(b_smel_str), basket_rope)
    yao_belief.set_plan(planunit_shop(b_bare_str), basket_rope)
    yao_belief.set_plan(planunit_shop(b_fine_str), basket_rope)
    yao_belief.set_plan(planunit_shop(b_half_str), basket_rope)
    yao_belief.set_plan(planunit_shop(do_laundry_str, task=True), casa_rope)

    # laundry requirement
    yao_belief.edit_plan_attr(
        laundry_chore_rope, reason_context=basket_rope, reason_case=b_full_rope
    )
    # laundry requirement
    yao_belief.edit_plan_attr(
        laundry_chore_rope, reason_context=basket_rope, reason_case=b_smel_rope
    )
    cali_laborunit = laborunit_shop()
    cali_laborunit.add_party(cali_str)
    yao_belief.edit_plan_attr(laundry_chore_rope, laborunit=cali_laborunit)
    yao_belief.add_fact(fact_context=basket_rope, fact_state=b_full_rope)

    return yao_belief


def from_list_get_active(
    rope: RopePointer, plan_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_plan = None

    active_true_count = 0
    active_false_count = 0
    for plan in plan_dict.values():
        if plan.get_plan_rope() == rope:
            temp_plan = plan
            print(f"s for PlanUnit {temp_plan.get_plan_rope()}  {temp_plan.active=}")

        if plan.active:
            active_true_count += 1
        elif plan.active is False:
            active_false_count += 1

    active = temp_plan.active
    print(
        f"Set active: {plan.plan_label=} {active} {active_true_count=} {active_false_count=}"
    )

    return active
