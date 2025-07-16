from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer import BelieverUnit, believerunit_shop


def get_believerunit_with_4_levels() -> BelieverUnit:
    a23_str = "amy23"
    sue_believer = believerunit_shop(
        believer_name="Sue", belief_label=a23_str, tally=10
    )

    casa = "casa"
    sue_believer.set_l1_plan(planunit_shop(casa, mass=30, task=True))

    cat = "cat have dinner"
    sue_believer.set_l1_plan(planunit_shop(cat, mass=30, task=True))

    week_str = "weekdays"
    week_rope = sue_believer.make_l1_rope(week_str)
    plan_kid_weekdays = planunit_shop(week_str, mass=40)
    sue_believer.set_l1_plan(plan_kid_weekdays)

    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"

    plan_grandkidU = planunit_shop(sun_str, mass=20)
    plan_grandkidM = planunit_shop(mon_str, mass=20)
    plan_grandkidT = planunit_shop(tue_str, mass=20)
    plan_grandkidW = planunit_shop(wed_str, mass=20)
    plan_grandkidR = planunit_shop(thu_str, mass=30)
    plan_grandkidF = planunit_shop(fri_str, mass=40)
    plan_grandkidA = planunit_shop(sat_str, mass=50)

    sue_believer.set_plan(plan_grandkidU, week_rope)
    sue_believer.set_plan(plan_grandkidM, week_rope)
    sue_believer.set_plan(plan_grandkidT, week_rope)
    sue_believer.set_plan(plan_grandkidW, week_rope)
    sue_believer.set_plan(plan_grandkidR, week_rope)
    sue_believer.set_plan(plan_grandkidF, week_rope)
    sue_believer.set_plan(plan_grandkidA, week_rope)

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


def get_fund_breakdown_believer() -> BelieverUnit:
    sue_believer = believerunit_shop(believer_name="Sue")

    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_believer.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_y_str = "hungry"
    clean_str = "cleaning"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    dish_str = "clean dishes"
    sue_believer.set_l1_plan(planunit_shop(casa_str, mass=30))
    sue_believer.set_plan(planunit_shop(cat_str, mass=30), casa_rope)
    sue_believer.set_plan(planunit_shop(hun_n_str, mass=30), cat_rope)
    sue_believer.set_plan(planunit_shop(hun_y_str, mass=30), cat_rope)
    sue_believer.set_plan(planunit_shop(clean_str, mass=30), casa_rope)
    sue_believer.set_plan(planunit_shop(sweep_str, mass=30, task=True), clean_rope)
    sue_believer.set_plan(planunit_shop(dish_str, mass=30, task=True), clean_rope)

    cat_str = "cat have dinner"
    sue_believer.set_l1_plan(planunit_shop(cat_str, mass=30, task=True))

    # week_str = "weekdays"
    # week_rope = sue_believer.make_l1_rope(week_str)
    # plan_kid_weekdays = planunit_shop(week_str, mass=25)
    # sue_believer.set_l1_plan(plan_kid_weekdays)

    # sun_str = "Sunday"
    # mon_str = "Monday"
    # tue_str = "Tuesday"
    # wed_str = "Wednesday"
    # thu_str = "Thursday"
    # fri_str = "Friday"
    # sat_str = "Saturday"
    # plan_grandkidU = planunit_shop(sun_str, mass=20)
    # plan_grandkidM = planunit_shop(mon_str, mass=20)
    # plan_grandkidT = planunit_shop(tue_str, mass=20)
    # plan_grandkidW = planunit_shop(wed_str, mass=20)
    # plan_grandkidR = planunit_shop(thu_str, mass=30)
    # plan_grandkidF = planunit_shop(fri_str, mass=40)
    # plan_grandkidA = planunit_shop(sat_str, mass=50)
    # sue_believer.set_plan(plan_grandkidU, week_rope)
    # sue_believer.set_plan(plan_grandkidM, week_rope)
    # sue_believer.set_plan(plan_grandkidT, week_rope)
    # sue_believer.set_plan(plan_grandkidW, week_rope)
    # sue_believer.set_plan(plan_grandkidR, week_rope)
    # sue_believer.set_plan(plan_grandkidF, week_rope)
    # sue_believer.set_plan(plan_grandkidA, week_rope)

    # nation_str = "nation"
    # nation_rope = sue_believer.make_l1_rope(nation_str)
    # plan_kid_nation = planunit_shop(nation_str, mass=30)
    # sue_believer.set_l1_plan(plan_kid_nation)

    # usa_str = "USA"
    # usa_rope = sue_believer.make_rope(nation_rope, usa_str)
    # france_str = "France"
    # brazil_str = "Brazil"
    # plan_grandkid_usa = planunit_shop(usa_str, mass=50)
    # plan_grandkid_france = planunit_shop(france_str, mass=50)
    # plan_grandkid_brazil = planunit_shop(brazil_str, mass=50)
    # sue_believer.set_plan(plan_grandkid_france, nation_rope)
    # sue_believer.set_plan(plan_grandkid_brazil, nation_rope)
    # sue_believer.set_plan(plan_grandkid_usa, nation_rope)

    # texas_str = "Texas"
    # oregon_str = "Oregon"
    # plan_grandgrandkid_usa_texas = planunit_shop(texas_str, mass=50)
    # plan_grandgrandkid_usa_oregon = planunit_shop(oregon_str, mass=50)
    # sue_believer.set_plan(plan_grandgrandkid_usa_texas, usa_rope)
    # sue_believer.set_plan(plan_grandgrandkid_usa_oregon, usa_rope)
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
    hatter_believer.add_plan(egg_rope)

    chicken_str = "chicken first"
    chicken_rope = hatter_believer.make_l1_rope(chicken_str)
    hatter_believer.add_plan(chicken_rope)

    # set egg task is True when chicken first is False
    hatter_believer.edit_plan_attr(
        egg_rope,
        task=True,
        reason_r_context=chicken_rope,
        reason_r_plan_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_believer.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_r_context=egg_rope,
        reason_r_plan_active_requisite=False,
    )

    return hatter_believer


def get_believerunit_3_partner() -> BelieverUnit:
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_partner_cred_points = 5
    yao_partner_cred_points = 2
    zia_partner_cred_points = 33
    sue_partner_debt_points = 1
    yao_partner_debt_points = 7
    zia_partner_debt_points = 13
    bob_believer = believerunit_shop(bob_str)
    bob_believer.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    bob_believer.add_partnerunit(
        yao_str, yao_partner_cred_points, yao_partner_debt_points
    )
    bob_believer.add_partnerunit(
        zia_str, zia_partner_cred_points, zia_partner_debt_points
    )

    return bob_believer
