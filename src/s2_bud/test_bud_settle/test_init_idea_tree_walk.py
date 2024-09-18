from src.s2_bud.examples.example_buds import get_budunit_with_4_levels
from src.s2_bud.reason_idea import reasonunit_shop
from src.s2_bud.idea import ideaunit_shop
from src.s2_bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_set_idea_dict_Scenario0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    root_idea = yao_bud.get_idea_obj(yao_bud._fiscal_id)
    assert not root_idea.begin
    assert not root_idea.close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert yao_bud._idea_dict == {}
    assert yao_bud._reason_bases == set()

    # WHEN
    yao_bud._set_idea_dict()

    # THEN
    assert not root_idea.begin
    assert not root_idea.close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert yao_bud._idea_dict == {root_idea.get_road(): root_idea}
    assert yao_bud._reason_bases == set()


def test_BudUnit_set_idea_dict_Scenario1():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    yao_bud.edit_idea_attr(yao_bud._fiscal_id, begin=time0_begin, close=time0_close)
    root_idea = yao_bud.get_idea_obj(yao_bud._fiscal_id)
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud._set_idea_dict()

    # THEN
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc


def test_BudUnit_set_idea_dict_Clears_gogo_calc_stop_calc():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_idea = sue_bud.get_idea_obj(sue_bud._fiscal_id)
    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    usa_str = "USA"
    usa_road = sue_bud.make_road(states_road, usa_str)
    texas_str = "Texas"
    texas_road = sue_bud.make_road(usa_road, texas_str)
    texas_idea = sue_bud.get_idea_obj(texas_road)
    texas_idea._gogo_calc = 7
    texas_idea._stop_calc = 11
    texas_idea._range_evaluated = True
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert texas_idea._range_evaluated
    assert texas_idea._gogo_calc
    assert texas_idea._stop_calc

    # WHEN
    sue_bud._set_idea_dict()

    # THEN
    assert not root_idea.begin
    assert not root_idea.close
    assert not texas_idea._range_evaluated
    assert not texas_idea._gogo_calc
    assert not texas_idea._stop_calc


def test_BudUnit_set_idea_dict_Sets_reason_bases():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    polis_str = "polis"
    polis_road = sue_bud.make_l1_road(polis_str)
    sue_bud.add_idea(polis_road)
    sue_bud.add_idea(states_road)
    sue_bud.edit_idea_attr(
        states_road, reason_base=polis_road, reason_premise=polis_road
    )
    states_idea = sue_bud.get_idea_obj(states_road)
    assert states_idea.base_reasonunit_exists(polis_road)
    assert sue_bud._reason_bases == set()

    # WHEN
    sue_bud._set_idea_dict()

    # THEN
    assert sue_bud._reason_bases == {polis_road}


def test_BudUnit_set_idea_CreatesIdeaUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_road = sue_bud.make_l1_road("casa")
    cleaning_road = sue_bud.make_road(casa_road, "cleaning")
    clean_cookery_str = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(clean_cookery_str, mass=40, pledge=True)

    buildings_str = "buildings"
    buildings_road = sue_bud.make_l1_road(buildings_str)
    cookery_room_str = "cookery"
    cookery_room_road = sue_bud.make_road(buildings_road, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_str)
    cookery_reasonunit = reasonunit_shop(base=cookery_room_road)
    cookery_reasonunit.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reasonunit(cookery_reasonunit)

    assert sue_bud.idea_exists(buildings_road) is False

    # WHEN
    sue_bud.set_idea(clean_cookery_idea, cleaning_road, create_missing_ideas=True)

    # THEN
    assert sue_bud.idea_exists(buildings_road)
