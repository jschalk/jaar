from src.a05_item_logic.item import itemunit_shop
from src.f02_bud.bud import BudUnit, budunit_shop


def get_budunit_with_4_levels() -> BudUnit:
    a23_str = "accord23"
    sue_bud = budunit_shop(owner_name="Sue", fisc_title=a23_str, tally=10)

    casa = "casa"
    sue_bud.set_l1_item(itemunit_shop(casa, mass=30, pledge=True))

    cat = "cat have dinner"
    sue_bud.set_l1_item(itemunit_shop(cat, mass=30, pledge=True))

    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    item_kid_weekdays = itemunit_shop(week_str, mass=40)
    sue_bud.set_l1_item(item_kid_weekdays)

    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"

    item_grandkidU = itemunit_shop(sun_str, mass=20)
    item_grandkidM = itemunit_shop(mon_str, mass=20)
    item_grandkidT = itemunit_shop(tue_str, mass=20)
    item_grandkidW = itemunit_shop(wed_str, mass=20)
    item_grandkidR = itemunit_shop(thu_str, mass=30)
    item_grandkidF = itemunit_shop(fri_str, mass=40)
    item_grandkidA = itemunit_shop(sat_str, mass=50)

    sue_bud.set_item(item_grandkidU, week_road)
    sue_bud.set_item(item_grandkidM, week_road)
    sue_bud.set_item(item_grandkidT, week_road)
    sue_bud.set_item(item_grandkidW, week_road)
    sue_bud.set_item(item_grandkidR, week_road)
    sue_bud.set_item(item_grandkidF, week_road)
    sue_bud.set_item(item_grandkidA, week_road)

    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    item_kid_states = itemunit_shop(states_str, mass=30)
    sue_bud.set_l1_item(item_kid_states)

    usa_str = "USA"
    usa_road = sue_bud.make_road(states_road, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    item_grandkid_usa = itemunit_shop(usa_str, mass=50)
    item_grandkid_france = itemunit_shop(france_str, mass=50)
    item_grandkid_brazil = itemunit_shop(brazil_str, mass=50)
    sue_bud.set_item(item_grandkid_france, states_road)
    sue_bud.set_item(item_grandkid_brazil, states_road)
    sue_bud.set_item(item_grandkid_usa, states_road)

    texas_str = "Texas"
    oregon_str = "Oregon"
    item_grandgrandkid_usa_texas = itemunit_shop(texas_str, mass=50)
    item_grandgrandkid_usa_oregon = itemunit_shop(oregon_str, mass=50)
    sue_bud.set_item(item_grandgrandkid_usa_texas, usa_road)
    sue_bud.set_item(item_grandgrandkid_usa_oregon, usa_road)
    return sue_bud


def get_fund_breakdown_bud() -> BudUnit:
    sue_bud = budunit_shop(owner_name="Sue")

    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    cat_str = "cat status"
    cat_road = sue_bud.make_road(casa_road, cat_str)
    hun_n_str = "not hungry"
    hun_y_str = "hungry"
    clean_str = "cleaning"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    sweep_str = "sweep floor"
    dish_str = "clean dishes"
    sue_bud.set_l1_item(itemunit_shop(casa_str, mass=30))
    sue_bud.set_item(itemunit_shop(cat_str, mass=30), casa_road)
    sue_bud.set_item(itemunit_shop(hun_n_str, mass=30), cat_road)
    sue_bud.set_item(itemunit_shop(hun_y_str, mass=30), cat_road)
    sue_bud.set_item(itemunit_shop(clean_str, mass=30), casa_road)
    sue_bud.set_item(itemunit_shop(sweep_str, mass=30, pledge=True), clean_road)
    sue_bud.set_item(itemunit_shop(dish_str, mass=30, pledge=True), clean_road)

    cat_str = "cat have dinner"
    sue_bud.set_l1_item(itemunit_shop(cat_str, mass=30, pledge=True))

    # week_str = "weekdays"
    # week_road = sue_bud.make_l1_road(week_str)
    # item_kid_weekdays = itemunit_shop(week_str, mass=25)
    # sue_bud.set_l1_item(item_kid_weekdays)

    # sun_str = "Sunday"
    # mon_str = "Monday"
    # tue_str = "Tuesday"
    # wed_str = "Wednesday"
    # thu_str = "Thursday"
    # fri_str = "Friday"
    # sat_str = "Saturday"
    # item_grandkidU = itemunit_shop(sun_str, mass=20)
    # item_grandkidM = itemunit_shop(mon_str, mass=20)
    # item_grandkidT = itemunit_shop(tue_str, mass=20)
    # item_grandkidW = itemunit_shop(wed_str, mass=20)
    # item_grandkidR = itemunit_shop(thu_str, mass=30)
    # item_grandkidF = itemunit_shop(fri_str, mass=40)
    # item_grandkidA = itemunit_shop(sat_str, mass=50)
    # sue_bud.set_item(item_grandkidU, week_road)
    # sue_bud.set_item(item_grandkidM, week_road)
    # sue_bud.set_item(item_grandkidT, week_road)
    # sue_bud.set_item(item_grandkidW, week_road)
    # sue_bud.set_item(item_grandkidR, week_road)
    # sue_bud.set_item(item_grandkidF, week_road)
    # sue_bud.set_item(item_grandkidA, week_road)

    # states_str = "nation-state"
    # states_road = sue_bud.make_l1_road(states_str)
    # item_kid_states = itemunit_shop(states_str, mass=30)
    # sue_bud.set_l1_item(item_kid_states)

    # usa_str = "USA"
    # usa_road = sue_bud.make_road(states_road, usa_str)
    # france_str = "France"
    # brazil_str = "Brazil"
    # item_grandkid_usa = itemunit_shop(usa_str, mass=50)
    # item_grandkid_france = itemunit_shop(france_str, mass=50)
    # item_grandkid_brazil = itemunit_shop(brazil_str, mass=50)
    # sue_bud.set_item(item_grandkid_france, states_road)
    # sue_bud.set_item(item_grandkid_brazil, states_road)
    # sue_bud.set_item(item_grandkid_usa, states_road)

    # texas_str = "Texas"
    # oregon_str = "Oregon"
    # item_grandgrandkid_usa_texas = itemunit_shop(texas_str, mass=50)
    # item_grandgrandkid_usa_oregon = itemunit_shop(oregon_str, mass=50)
    # sue_bud.set_item(item_grandgrandkid_usa_texas, usa_road)
    # sue_bud.set_item(item_grandgrandkid_usa_oregon, usa_road)
    return sue_bud


def get_budunit_irrational_example() -> BudUnit:
    # this bud has no conclusive agenda because 2 pledge items are in contradiction
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
    egg_road = hatter_bud.make_l1_road(egg_str)
    hatter_bud.add_item(egg_road)

    chicken_str = "chicken first"
    chicken_road = hatter_bud.make_l1_road(chicken_str)
    hatter_bud.add_item(chicken_road)

    # set egg pledge is True when chicken first is False
    hatter_bud.edit_item_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_item_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_bud.edit_item_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_item_active_requisite=False,
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
