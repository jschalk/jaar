from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import BudUnit, budunit_shop


def get_budunit_with_4_levels() -> BudUnit:
    a23_str = "accord23"
    sue_bud = budunit_shop(owner_name="Sue", vow_label=a23_str, tally=10)

    casa = "casa"
    sue_bud.set_l1_concept(conceptunit_shop(casa, mass=30, pledge=True))

    cat = "cat have dinner"
    sue_bud.set_l1_concept(conceptunit_shop(cat, mass=30, pledge=True))

    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    concept_kid_weekdays = conceptunit_shop(week_str, mass=40)
    sue_bud.set_l1_concept(concept_kid_weekdays)

    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"

    concept_grandkidU = conceptunit_shop(sun_str, mass=20)
    concept_grandkidM = conceptunit_shop(mon_str, mass=20)
    concept_grandkidT = conceptunit_shop(tue_str, mass=20)
    concept_grandkidW = conceptunit_shop(wed_str, mass=20)
    concept_grandkidR = conceptunit_shop(thu_str, mass=30)
    concept_grandkidF = conceptunit_shop(fri_str, mass=40)
    concept_grandkidA = conceptunit_shop(sat_str, mass=50)

    sue_bud.set_concept(concept_grandkidU, week_way)
    sue_bud.set_concept(concept_grandkidM, week_way)
    sue_bud.set_concept(concept_grandkidT, week_way)
    sue_bud.set_concept(concept_grandkidW, week_way)
    sue_bud.set_concept(concept_grandkidR, week_way)
    sue_bud.set_concept(concept_grandkidF, week_way)
    sue_bud.set_concept(concept_grandkidA, week_way)

    nation_str = "nation"
    nation_way = sue_bud.make_l1_way(nation_str)
    concept_kid_nation = conceptunit_shop(nation_str, mass=30)
    sue_bud.set_l1_concept(concept_kid_nation)

    usa_str = "USA"
    usa_way = sue_bud.make_way(nation_way, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    concept_grandkid_usa = conceptunit_shop(usa_str, mass=50)
    concept_grandkid_france = conceptunit_shop(france_str, mass=50)
    concept_grandkid_brazil = conceptunit_shop(brazil_str, mass=50)
    sue_bud.set_concept(concept_grandkid_france, nation_way)
    sue_bud.set_concept(concept_grandkid_brazil, nation_way)
    sue_bud.set_concept(concept_grandkid_usa, nation_way)

    texas_str = "Texas"
    oregon_str = "Oregon"
    concept_grandgrandkid_usa_texas = conceptunit_shop(texas_str, mass=50)
    concept_grandgrandkid_usa_oregon = conceptunit_shop(oregon_str, mass=50)
    sue_bud.set_concept(concept_grandgrandkid_usa_texas, usa_way)
    sue_bud.set_concept(concept_grandgrandkid_usa_oregon, usa_way)
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
    sue_bud.set_l1_concept(conceptunit_shop(casa_str, mass=30))
    sue_bud.set_concept(conceptunit_shop(cat_str, mass=30), casa_way)
    sue_bud.set_concept(conceptunit_shop(hun_n_str, mass=30), cat_way)
    sue_bud.set_concept(conceptunit_shop(hun_y_str, mass=30), cat_way)
    sue_bud.set_concept(conceptunit_shop(clean_str, mass=30), casa_way)
    sue_bud.set_concept(conceptunit_shop(sweep_str, mass=30, pledge=True), clean_way)
    sue_bud.set_concept(conceptunit_shop(dish_str, mass=30, pledge=True), clean_way)

    cat_str = "cat have dinner"
    sue_bud.set_l1_concept(conceptunit_shop(cat_str, mass=30, pledge=True))

    # week_str = "weekdays"
    # week_way = sue_bud.make_l1_way(week_str)
    # concept_kid_weekdays = conceptunit_shop(week_str, mass=25)
    # sue_bud.set_l1_concept(concept_kid_weekdays)

    # sun_str = "Sunday"
    # mon_str = "Monday"
    # tue_str = "Tuesday"
    # wed_str = "Wednesday"
    # thu_str = "Thursday"
    # fri_str = "Friday"
    # sat_str = "Saturday"
    # concept_grandkidU = conceptunit_shop(sun_str, mass=20)
    # concept_grandkidM = conceptunit_shop(mon_str, mass=20)
    # concept_grandkidT = conceptunit_shop(tue_str, mass=20)
    # concept_grandkidW = conceptunit_shop(wed_str, mass=20)
    # concept_grandkidR = conceptunit_shop(thu_str, mass=30)
    # concept_grandkidF = conceptunit_shop(fri_str, mass=40)
    # concept_grandkidA = conceptunit_shop(sat_str, mass=50)
    # sue_bud.set_concept(concept_grandkidU, week_way)
    # sue_bud.set_concept(concept_grandkidM, week_way)
    # sue_bud.set_concept(concept_grandkidT, week_way)
    # sue_bud.set_concept(concept_grandkidW, week_way)
    # sue_bud.set_concept(concept_grandkidR, week_way)
    # sue_bud.set_concept(concept_grandkidF, week_way)
    # sue_bud.set_concept(concept_grandkidA, week_way)

    # nation_str = "nation"
    # nation_way = sue_bud.make_l1_way(nation_str)
    # concept_kid_nation = conceptunit_shop(nation_str, mass=30)
    # sue_bud.set_l1_concept(concept_kid_nation)

    # usa_str = "USA"
    # usa_way = sue_bud.make_way(nation_way, usa_str)
    # france_str = "France"
    # brazil_str = "Brazil"
    # concept_grandkid_usa = conceptunit_shop(usa_str, mass=50)
    # concept_grandkid_france = conceptunit_shop(france_str, mass=50)
    # concept_grandkid_brazil = conceptunit_shop(brazil_str, mass=50)
    # sue_bud.set_concept(concept_grandkid_france, nation_way)
    # sue_bud.set_concept(concept_grandkid_brazil, nation_way)
    # sue_bud.set_concept(concept_grandkid_usa, nation_way)

    # texas_str = "Texas"
    # oregon_str = "Oregon"
    # concept_grandgrandkid_usa_texas = conceptunit_shop(texas_str, mass=50)
    # concept_grandgrandkid_usa_oregon = conceptunit_shop(oregon_str, mass=50)
    # sue_bud.set_concept(concept_grandgrandkid_usa_texas, usa_way)
    # sue_bud.set_concept(concept_grandgrandkid_usa_oregon, usa_way)
    return sue_bud


def get_budunit_irrational_example() -> BudUnit:
    # this bud has no definitive agenda because 2 pledge concepts are in contradiction
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
    hatter_bud.add_concept(egg_way)

    chicken_str = "chicken first"
    chicken_way = hatter_bud.make_l1_way(chicken_str)
    hatter_bud.add_concept(chicken_way)

    # set egg pledge is True when chicken first is False
    hatter_bud.edit_concept_attr(
        egg_way,
        pledge=True,
        reason_rcontext=chicken_way,
        reason_rconcept_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_bud.edit_concept_attr(
        chicken_way,
        pledge=True,
        reason_rcontext=egg_way,
        reason_rconcept_active_requisite=False,
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
