from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import BudUnit, budunit_shop


def get_budunit_with_4_levels() -> BudUnit:
    a23_str = "accord23"
    sue_bud = budunit_shop(owner_name="Sue", fisc_label=a23_str, tally=10)

    casa = "casa"
    sue_bud.set_l1_idea(ideaunit_shop(casa, mass=30, pledge=True))

    cat = "cat have dinner"
    sue_bud.set_l1_idea(ideaunit_shop(cat, mass=30, pledge=True))

    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    idea_kid_weekdays = ideaunit_shop(week_str, mass=40)
    sue_bud.set_l1_idea(idea_kid_weekdays)

    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"

    idea_grandkidU = ideaunit_shop(sun_str, mass=20)
    idea_grandkidM = ideaunit_shop(mon_str, mass=20)
    idea_grandkidT = ideaunit_shop(tue_str, mass=20)
    idea_grandkidW = ideaunit_shop(wed_str, mass=20)
    idea_grandkidR = ideaunit_shop(thu_str, mass=30)
    idea_grandkidF = ideaunit_shop(fri_str, mass=40)
    idea_grandkidA = ideaunit_shop(sat_str, mass=50)

    sue_bud.set_idea(idea_grandkidU, week_way)
    sue_bud.set_idea(idea_grandkidM, week_way)
    sue_bud.set_idea(idea_grandkidT, week_way)
    sue_bud.set_idea(idea_grandkidW, week_way)
    sue_bud.set_idea(idea_grandkidR, week_way)
    sue_bud.set_idea(idea_grandkidF, week_way)
    sue_bud.set_idea(idea_grandkidA, week_way)

    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    idea_kid_states = ideaunit_shop(states_str, mass=30)
    sue_bud.set_l1_idea(idea_kid_states)

    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    idea_grandkid_usa = ideaunit_shop(usa_str, mass=50)
    idea_grandkid_france = ideaunit_shop(france_str, mass=50)
    idea_grandkid_brazil = ideaunit_shop(brazil_str, mass=50)
    sue_bud.set_idea(idea_grandkid_france, states_way)
    sue_bud.set_idea(idea_grandkid_brazil, states_way)
    sue_bud.set_idea(idea_grandkid_usa, states_way)

    texas_str = "Texas"
    oregon_str = "Oregon"
    idea_grandgrandkid_usa_texas = ideaunit_shop(texas_str, mass=50)
    idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_str, mass=50)
    sue_bud.set_idea(idea_grandgrandkid_usa_texas, usa_way)
    sue_bud.set_idea(idea_grandgrandkid_usa_oregon, usa_way)
    return sue_bud


def get_fund_breakdown_bud() -> BudUnit:
    sue_bud = budunit_shop(owner_name="Sue")

    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    cat_str = "cat status"
    cat_way = sue_bud.make_way(casa_way, cat_str)
    hun_n_str = "not hungry"
    hun_y_str = "hungry"
    clean_str = "cleaning"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_str = "sweep floor"
    dish_str = "clean dishes"
    sue_bud.set_l1_idea(ideaunit_shop(casa_str, mass=30))
    sue_bud.set_idea(ideaunit_shop(cat_str, mass=30), casa_way)
    sue_bud.set_idea(ideaunit_shop(hun_n_str, mass=30), cat_way)
    sue_bud.set_idea(ideaunit_shop(hun_y_str, mass=30), cat_way)
    sue_bud.set_idea(ideaunit_shop(clean_str, mass=30), casa_way)
    sue_bud.set_idea(ideaunit_shop(sweep_str, mass=30, pledge=True), clean_way)
    sue_bud.set_idea(ideaunit_shop(dish_str, mass=30, pledge=True), clean_way)

    cat_str = "cat have dinner"
    sue_bud.set_l1_idea(ideaunit_shop(cat_str, mass=30, pledge=True))

    # week_str = "weekdays"
    # week_way = sue_bud.make_l1_way(week_str)
    # idea_kid_weekdays = ideaunit_shop(week_str, mass=25)
    # sue_bud.set_l1_idea(idea_kid_weekdays)

    # sun_str = "Sunday"
    # mon_str = "Monday"
    # tue_str = "Tuesday"
    # wed_str = "Wednesday"
    # thu_str = "Thursday"
    # fri_str = "Friday"
    # sat_str = "Saturday"
    # idea_grandkidU = ideaunit_shop(sun_str, mass=20)
    # idea_grandkidM = ideaunit_shop(mon_str, mass=20)
    # idea_grandkidT = ideaunit_shop(tue_str, mass=20)
    # idea_grandkidW = ideaunit_shop(wed_str, mass=20)
    # idea_grandkidR = ideaunit_shop(thu_str, mass=30)
    # idea_grandkidF = ideaunit_shop(fri_str, mass=40)
    # idea_grandkidA = ideaunit_shop(sat_str, mass=50)
    # sue_bud.set_idea(idea_grandkidU, week_way)
    # sue_bud.set_idea(idea_grandkidM, week_way)
    # sue_bud.set_idea(idea_grandkidT, week_way)
    # sue_bud.set_idea(idea_grandkidW, week_way)
    # sue_bud.set_idea(idea_grandkidR, week_way)
    # sue_bud.set_idea(idea_grandkidF, week_way)
    # sue_bud.set_idea(idea_grandkidA, week_way)

    # states_str = "nation-state"
    # states_way = sue_bud.make_l1_way(states_str)
    # idea_kid_states = ideaunit_shop(states_str, mass=30)
    # sue_bud.set_l1_idea(idea_kid_states)

    # usa_str = "USA"
    # usa_way = sue_bud.make_way(states_way, usa_str)
    # france_str = "France"
    # brazil_str = "Brazil"
    # idea_grandkid_usa = ideaunit_shop(usa_str, mass=50)
    # idea_grandkid_france = ideaunit_shop(france_str, mass=50)
    # idea_grandkid_brazil = ideaunit_shop(brazil_str, mass=50)
    # sue_bud.set_idea(idea_grandkid_france, states_way)
    # sue_bud.set_idea(idea_grandkid_brazil, states_way)
    # sue_bud.set_idea(idea_grandkid_usa, states_way)

    # texas_str = "Texas"
    # oregon_str = "Oregon"
    # idea_grandgrandkid_usa_texas = ideaunit_shop(texas_str, mass=50)
    # idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_str, mass=50)
    # sue_bud.set_idea(idea_grandgrandkid_usa_texas, usa_way)
    # sue_bud.set_idea(idea_grandgrandkid_usa_oregon, usa_way)
    return sue_bud


def get_budunit_irrational_example() -> BudUnit:
    # this bud has no definitive agenda because 2 pledge ideas are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_bud.settle_bud these should be true:
    # 1. hatter_bud._irrational is True
    # 2. hatter_bud._tree_traverse_count = hatter_bud.max_tree_traverse

    hatter_bud = budunit_shop("Mad Hatter")
    hatter_bud.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_way = hatter_bud.make_l1_way(egg_str)
    hatter_bud.add_idea(egg_way)

    chicken_str = "chicken first"
    chicken_way = hatter_bud.make_l1_way(chicken_str)
    hatter_bud.add_idea(chicken_way)

    # set egg pledge is True when chicken first is False
    hatter_bud.edit_idea_attr(
        egg_way,
        pledge=True,
        reason_rcontext=chicken_way,
        reason_rcontext_idea_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_bud.edit_idea_attr(
        chicken_way,
        pledge=True,
        reason_rcontext=egg_way,
        reason_rcontext_idea_active_requisite=False,
    )

    return hatter_bud


def get_budunit_3_acct() -> BudUnit:
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_credit_belief = 5
    yao_credit_belief = 2
    zia_credit_belief = 33
    sue_debtit_belief = 1
    yao_debtit_belief = 7
    zia_debtit_belief = 13
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    bob_bud.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    bob_bud.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)

    return bob_bud
