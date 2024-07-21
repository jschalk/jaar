from src.bud.idea import ideaunit_shop
from src.bud.bud import BudUnit, budunit_shop


def get_budunit_with_4_levels() -> BudUnit:
    sue_bud = budunit_shop(_owner_id="Sue", _weight=10)

    casa = "casa"
    sue_bud.set_l1_idea(ideaunit_shop(casa, _weight=30, pledge=True))

    cat = "cat have dinner"
    sue_bud.set_l1_idea(ideaunit_shop(cat, _weight=30, pledge=True))

    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    idea_kid_weekdays = ideaunit_shop(week_text, _weight=40)
    sue_bud.set_l1_idea(idea_kid_weekdays)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    idea_grandkidU = ideaunit_shop(sun_text, _weight=20)
    idea_grandkidM = ideaunit_shop(mon_text, _weight=20)
    idea_grandkidT = ideaunit_shop(tue_text, _weight=20)
    idea_grandkidW = ideaunit_shop(wed_text, _weight=20)
    idea_grandkidR = ideaunit_shop(thu_text, _weight=30)
    idea_grandkidF = ideaunit_shop(fri_text, _weight=40)
    idea_grandkidA = ideaunit_shop(sat_text, _weight=50)

    sue_bud.set_idea(idea_grandkidU, week_road)
    sue_bud.set_idea(idea_grandkidM, week_road)
    sue_bud.set_idea(idea_grandkidT, week_road)
    sue_bud.set_idea(idea_grandkidW, week_road)
    sue_bud.set_idea(idea_grandkidR, week_road)
    sue_bud.set_idea(idea_grandkidF, week_road)
    sue_bud.set_idea(idea_grandkidA, week_road)

    states_text = "nation-state"
    states_road = sue_bud.make_l1_road(states_text)
    idea_kid_states = ideaunit_shop(states_text, _weight=30)
    sue_bud.set_l1_idea(idea_kid_states)

    usa_text = "USA"
    usa_road = sue_bud.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = ideaunit_shop(usa_text, _weight=50)
    idea_grandkid_france = ideaunit_shop(france_text, _weight=50)
    idea_grandkid_brazil = ideaunit_shop(brazil_text, _weight=50)
    sue_bud.set_idea(idea_grandkid_france, states_road)
    sue_bud.set_idea(idea_grandkid_brazil, states_road)
    sue_bud.set_idea(idea_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = ideaunit_shop(texas_text, _weight=50)
    idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_text, _weight=50)
    sue_bud.set_idea(idea_grandgrandkid_usa_texas, usa_road)
    sue_bud.set_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return sue_bud


def get_fund_explanation_bud() -> BudUnit:
    sue_bud = budunit_shop(_owner_id="Sue")

    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    cat_text = "cat status"
    cat_road = sue_bud.make_road(casa_road, cat_text)
    hun_n_text = "not hungry"
    hun_y_text = "hungry"
    clean_text = "cleaning"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    sweep_text = "sweep floor"
    dish_text = "clean dishes"
    sue_bud.set_l1_idea(ideaunit_shop(casa_text, _weight=30))
    sue_bud.set_idea(ideaunit_shop(cat_text, _weight=30), casa_road)
    sue_bud.set_idea(ideaunit_shop(hun_n_text, _weight=30), cat_road)
    sue_bud.set_idea(ideaunit_shop(hun_y_text, _weight=30), cat_road)
    sue_bud.set_idea(ideaunit_shop(clean_text, _weight=30), casa_road)
    sue_bud.set_idea(ideaunit_shop(sweep_text, _weight=30, pledge=True), clean_road)
    sue_bud.set_idea(ideaunit_shop(dish_text, _weight=30, pledge=True), clean_road)

    cat_text = "cat have dinner"
    sue_bud.set_l1_idea(ideaunit_shop(cat_text, _weight=30, pledge=True))

    # week_text = "weekdays"
    # week_road = sue_bud.make_l1_road(week_text)
    # idea_kid_weekdays = ideaunit_shop(week_text, _weight=25)
    # sue_bud.set_l1_idea(idea_kid_weekdays)

    # sun_text = "Sunday"
    # mon_text = "Monday"
    # tue_text = "Tuesday"
    # wed_text = "Wednesday"
    # thu_text = "Thursday"
    # fri_text = "Friday"
    # sat_text = "Saturday"
    # idea_grandkidU = ideaunit_shop(sun_text, _weight=20)
    # idea_grandkidM = ideaunit_shop(mon_text, _weight=20)
    # idea_grandkidT = ideaunit_shop(tue_text, _weight=20)
    # idea_grandkidW = ideaunit_shop(wed_text, _weight=20)
    # idea_grandkidR = ideaunit_shop(thu_text, _weight=30)
    # idea_grandkidF = ideaunit_shop(fri_text, _weight=40)
    # idea_grandkidA = ideaunit_shop(sat_text, _weight=50)
    # sue_bud.set_idea(idea_grandkidU, week_road)
    # sue_bud.set_idea(idea_grandkidM, week_road)
    # sue_bud.set_idea(idea_grandkidT, week_road)
    # sue_bud.set_idea(idea_grandkidW, week_road)
    # sue_bud.set_idea(idea_grandkidR, week_road)
    # sue_bud.set_idea(idea_grandkidF, week_road)
    # sue_bud.set_idea(idea_grandkidA, week_road)

    # states_text = "nation-state"
    # states_road = sue_bud.make_l1_road(states_text)
    # idea_kid_states = ideaunit_shop(states_text, _weight=30)
    # sue_bud.set_l1_idea(idea_kid_states)

    # usa_text = "USA"
    # usa_road = sue_bud.make_road(states_road, usa_text)
    # france_text = "France"
    # brazil_text = "Brazil"
    # idea_grandkid_usa = ideaunit_shop(usa_text, _weight=50)
    # idea_grandkid_france = ideaunit_shop(france_text, _weight=50)
    # idea_grandkid_brazil = ideaunit_shop(brazil_text, _weight=50)
    # sue_bud.set_idea(idea_grandkid_france, states_road)
    # sue_bud.set_idea(idea_grandkid_brazil, states_road)
    # sue_bud.set_idea(idea_grandkid_usa, states_road)

    # texas_text = "Texas"
    # oregon_text = "Oregon"
    # idea_grandgrandkid_usa_texas = ideaunit_shop(texas_text, _weight=50)
    # idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_text, _weight=50)
    # sue_bud.set_idea(idea_grandgrandkid_usa_texas, usa_road)
    # sue_bud.set_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return sue_bud
