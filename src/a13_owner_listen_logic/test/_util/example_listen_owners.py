from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_owner_logic.owner import OwnerUnit, ownerunit_shop


def get_ownerunit_with_4_levels() -> OwnerUnit:
    a23_str = "amy23"
    sue_owner = ownerunit_shop(owner_name="Sue", belief_label=a23_str, tally=10)

    casa = "casa"
    sue_owner.set_l1_concept(conceptunit_shop(casa, mass=30, task=True))

    cat = "cat have dinner"
    sue_owner.set_l1_concept(conceptunit_shop(cat, mass=30, task=True))

    week_str = "weekdays"
    week_rope = sue_owner.make_l1_rope(week_str)
    concept_kid_weekdays = conceptunit_shop(week_str, mass=40)
    sue_owner.set_l1_concept(concept_kid_weekdays)

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

    sue_owner.set_concept(concept_grandkidU, week_rope)
    sue_owner.set_concept(concept_grandkidM, week_rope)
    sue_owner.set_concept(concept_grandkidT, week_rope)
    sue_owner.set_concept(concept_grandkidW, week_rope)
    sue_owner.set_concept(concept_grandkidR, week_rope)
    sue_owner.set_concept(concept_grandkidF, week_rope)
    sue_owner.set_concept(concept_grandkidA, week_rope)

    nation_str = "nation"
    nation_rope = sue_owner.make_l1_rope(nation_str)
    concept_kid_nation = conceptunit_shop(nation_str, mass=30)
    sue_owner.set_l1_concept(concept_kid_nation)

    usa_str = "USA"
    usa_rope = sue_owner.make_rope(nation_rope, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    concept_grandkid_usa = conceptunit_shop(usa_str, mass=50)
    concept_grandkid_france = conceptunit_shop(france_str, mass=50)
    concept_grandkid_brazil = conceptunit_shop(brazil_str, mass=50)
    sue_owner.set_concept(concept_grandkid_france, nation_rope)
    sue_owner.set_concept(concept_grandkid_brazil, nation_rope)
    sue_owner.set_concept(concept_grandkid_usa, nation_rope)

    texas_str = "Texas"
    oregon_str = "Oregon"
    concept_grandgrandkid_usa_texas = conceptunit_shop(texas_str, mass=50)
    concept_grandgrandkid_usa_oregon = conceptunit_shop(oregon_str, mass=50)
    sue_owner.set_concept(concept_grandgrandkid_usa_texas, usa_rope)
    sue_owner.set_concept(concept_grandgrandkid_usa_oregon, usa_rope)
    return sue_owner


def get_fund_breakdown_owner() -> OwnerUnit:
    sue_owner = ownerunit_shop(owner_name="Sue")

    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_owner.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_y_str = "hungry"
    clean_str = "cleaning"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    dish_str = "clean dishes"
    sue_owner.set_l1_concept(conceptunit_shop(casa_str, mass=30))
    sue_owner.set_concept(conceptunit_shop(cat_str, mass=30), casa_rope)
    sue_owner.set_concept(conceptunit_shop(hun_n_str, mass=30), cat_rope)
    sue_owner.set_concept(conceptunit_shop(hun_y_str, mass=30), cat_rope)
    sue_owner.set_concept(conceptunit_shop(clean_str, mass=30), casa_rope)
    sue_owner.set_concept(conceptunit_shop(sweep_str, mass=30, task=True), clean_rope)
    sue_owner.set_concept(conceptunit_shop(dish_str, mass=30, task=True), clean_rope)

    cat_str = "cat have dinner"
    sue_owner.set_l1_concept(conceptunit_shop(cat_str, mass=30, task=True))

    # week_str = "weekdays"
    # week_rope = sue_owner.make_l1_rope(week_str)
    # concept_kid_weekdays = conceptunit_shop(week_str, mass=25)
    # sue_owner.set_l1_concept(concept_kid_weekdays)

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
    # sue_owner.set_concept(concept_grandkidU, week_rope)
    # sue_owner.set_concept(concept_grandkidM, week_rope)
    # sue_owner.set_concept(concept_grandkidT, week_rope)
    # sue_owner.set_concept(concept_grandkidW, week_rope)
    # sue_owner.set_concept(concept_grandkidR, week_rope)
    # sue_owner.set_concept(concept_grandkidF, week_rope)
    # sue_owner.set_concept(concept_grandkidA, week_rope)

    # nation_str = "nation"
    # nation_rope = sue_owner.make_l1_rope(nation_str)
    # concept_kid_nation = conceptunit_shop(nation_str, mass=30)
    # sue_owner.set_l1_concept(concept_kid_nation)

    # usa_str = "USA"
    # usa_rope = sue_owner.make_rope(nation_rope, usa_str)
    # france_str = "France"
    # brazil_str = "Brazil"
    # concept_grandkid_usa = conceptunit_shop(usa_str, mass=50)
    # concept_grandkid_france = conceptunit_shop(france_str, mass=50)
    # concept_grandkid_brazil = conceptunit_shop(brazil_str, mass=50)
    # sue_owner.set_concept(concept_grandkid_france, nation_rope)
    # sue_owner.set_concept(concept_grandkid_brazil, nation_rope)
    # sue_owner.set_concept(concept_grandkid_usa, nation_rope)

    # texas_str = "Texas"
    # oregon_str = "Oregon"
    # concept_grandgrandkid_usa_texas = conceptunit_shop(texas_str, mass=50)
    # concept_grandgrandkid_usa_oregon = conceptunit_shop(oregon_str, mass=50)
    # sue_owner.set_concept(concept_grandgrandkid_usa_texas, usa_rope)
    # sue_owner.set_concept(concept_grandgrandkid_usa_oregon, usa_rope)
    return sue_owner


def get_ownerunit_irrational_example() -> OwnerUnit:
    # this owner has no definitive agenda because 2 task concepts are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_owner.settle_owner these should be true:
    # 1. hatter_owner._irrational is True
    # 2. hatter_owner._tree_traverse_count = hatter_owner.max_tree_traverse

    hatter_owner = ownerunit_shop("Mad Hatter")
    hatter_owner.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_owner.make_l1_rope(egg_str)
    hatter_owner.add_concept(egg_rope)

    chicken_str = "chicken first"
    chicken_rope = hatter_owner.make_l1_rope(chicken_str)
    hatter_owner.add_concept(chicken_rope)

    # set egg task is True when chicken first is False
    hatter_owner.edit_concept_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rconcept_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_owner.edit_concept_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rconcept_active_requisite=False,
    )

    return hatter_owner


def get_ownerunit_3_acct() -> OwnerUnit:
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_acct_cred_points = 5
    yao_acct_cred_points = 2
    zia_acct_cred_points = 33
    sue_acct_debt_points = 1
    yao_acct_debt_points = 7
    zia_acct_debt_points = 13
    bob_owner = ownerunit_shop(bob_str)
    bob_owner.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    bob_owner.add_acctunit(yao_str, yao_acct_cred_points, yao_acct_debt_points)
    bob_owner.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)

    return bob_owner
