from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop


def get_beliefunit_with_4_levels() -> BeliefUnit:
    a23_str = "amy23"
    sue_belief = beliefunit_shop(belief_name="Sue", moment_label=a23_str, tally=10)

    casa = "casa"
    sue_belief.set_l1_plan(planunit_shop(casa, star=30, task=True))

    cat = "cat have dinner"
    sue_belief.set_l1_plan(planunit_shop(cat, star=30, task=True))

    week_str = "weekdays"
    week_rope = sue_belief.make_l1_rope(week_str)
    plan_kid_weekdays = planunit_shop(week_str, star=40)
    sue_belief.set_l1_plan(plan_kid_weekdays)

    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"

    plan_grandkidU = planunit_shop(sun_str, star=20)
    plan_grandkidM = planunit_shop(mon_str, star=20)
    plan_grandkidT = planunit_shop(tue_str, star=20)
    plan_grandkidW = planunit_shop(wed_str, star=20)
    plan_grandkidR = planunit_shop(thu_str, star=30)
    plan_grandkidF = planunit_shop(fri_str, star=40)
    plan_grandkidA = planunit_shop(sat_str, star=50)

    sue_belief.set_plan(plan_grandkidU, week_rope)
    sue_belief.set_plan(plan_grandkidM, week_rope)
    sue_belief.set_plan(plan_grandkidT, week_rope)
    sue_belief.set_plan(plan_grandkidW, week_rope)
    sue_belief.set_plan(plan_grandkidR, week_rope)
    sue_belief.set_plan(plan_grandkidF, week_rope)
    sue_belief.set_plan(plan_grandkidA, week_rope)

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


def get_fund_breakdown_belief() -> BeliefUnit:
    sue_belief = beliefunit_shop(belief_name="Sue")

    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_belief.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_y_str = "hungry"
    clean_str = "cleaning"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    dish_str = "clean dishes"
    sue_belief.set_l1_plan(planunit_shop(casa_str, star=30))
    sue_belief.set_plan(planunit_shop(cat_str, star=30), casa_rope)
    sue_belief.set_plan(planunit_shop(hun_n_str, star=30), cat_rope)
    sue_belief.set_plan(planunit_shop(hun_y_str, star=30), cat_rope)
    sue_belief.set_plan(planunit_shop(clean_str, star=30), casa_rope)
    sue_belief.set_plan(planunit_shop(sweep_str, star=30, task=True), clean_rope)
    sue_belief.set_plan(planunit_shop(dish_str, star=30, task=True), clean_rope)

    cat_str = "cat have dinner"
    sue_belief.set_l1_plan(planunit_shop(cat_str, star=30, task=True))

    # week_str = "weekdays"
    # week_rope = sue_belief.make_l1_rope(week_str)
    # plan_kid_weekdays = planunit_shop(week_str, star=25)
    # sue_belief.set_l1_plan(plan_kid_weekdays)

    # sun_str = "Sunday"
    # mon_str = "Monday"
    # tue_str = "Tuesday"
    # wed_str = "Wednesday"
    # thu_str = "Thursday"
    # fri_str = "Friday"
    # sat_str = "Saturday"
    # plan_grandkidU = planunit_shop(sun_str, star=20)
    # plan_grandkidM = planunit_shop(mon_str, star=20)
    # plan_grandkidT = planunit_shop(tue_str, star=20)
    # plan_grandkidW = planunit_shop(wed_str, star=20)
    # plan_grandkidR = planunit_shop(thu_str, star=30)
    # plan_grandkidF = planunit_shop(fri_str, star=40)
    # plan_grandkidA = planunit_shop(sat_str, star=50)
    # sue_belief.set_plan(plan_grandkidU, week_rope)
    # sue_belief.set_plan(plan_grandkidM, week_rope)
    # sue_belief.set_plan(plan_grandkidT, week_rope)
    # sue_belief.set_plan(plan_grandkidW, week_rope)
    # sue_belief.set_plan(plan_grandkidR, week_rope)
    # sue_belief.set_plan(plan_grandkidF, week_rope)
    # sue_belief.set_plan(plan_grandkidA, week_rope)

    # nation_str = "nation"
    # nation_rope = sue_belief.make_l1_rope(nation_str)
    # plan_kid_nation = planunit_shop(nation_str, star=30)
    # sue_belief.set_l1_plan(plan_kid_nation)

    # usa_str = "USA"
    # usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    # france_str = "France"
    # brazil_str = "Brazil"
    # plan_grandkid_usa = planunit_shop(usa_str, star=50)
    # plan_grandkid_france = planunit_shop(france_str, star=50)
    # plan_grandkid_brazil = planunit_shop(brazil_str, star=50)
    # sue_belief.set_plan(plan_grandkid_france, nation_rope)
    # sue_belief.set_plan(plan_grandkid_brazil, nation_rope)
    # sue_belief.set_plan(plan_grandkid_usa, nation_rope)

    # texas_str = "Texas"
    # oregon_str = "Oregon"
    # plan_grandgrandkid_usa_texas = planunit_shop(texas_str, star=50)
    # plan_grandgrandkid_usa_oregon = planunit_shop(oregon_str, star=50)
    # sue_belief.set_plan(plan_grandgrandkid_usa_texas, usa_rope)
    # sue_belief.set_plan(plan_grandgrandkid_usa_oregon, usa_rope)
    return sue_belief


def get_beliefunit_irrational_example() -> BeliefUnit:
    # this belief has no definitive agenda because 2 task plans are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_belief.cash_out these should be true:
    # 1. hatter_belief._irrational is True
    # 2. hatter_belief._tree_traverse_count = hatter_belief.max_tree_traverse

    hatter_belief = beliefunit_shop("Mad Hatter")
    hatter_belief.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_belief.make_l1_rope(egg_str)
    hatter_belief.add_plan(egg_rope)

    chicken_str = "chicken first"
    chicken_rope = hatter_belief.make_l1_rope(chicken_str)
    hatter_belief.add_plan(chicken_rope)

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


def get_beliefunit_3_voice() -> BeliefUnit:
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_voice_cred_points = 5
    yao_voice_cred_points = 2
    zia_voice_cred_points = 33
    sue_voice_debt_points = 1
    yao_voice_debt_points = 7
    zia_voice_debt_points = 13
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)
    bob_belief.add_voiceunit(yao_str, yao_voice_cred_points, yao_voice_debt_points)
    bob_belief.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)

    return bob_belief
