from src.bud.examples.example_buds import get_budunit_with_4_levels
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_init_idea_tree_walk_Scenario0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
    assert not root_idea._begin
    assert not root_idea._close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert yao_bud._idea_dict == {}

    # WHEN
    yao_bud.init_idea_tree_walk()

    # THEN
    assert not root_idea._begin
    assert not root_idea._close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert yao_bud._idea_dict == {root_idea.get_road(): root_idea}


def test_BudUnit_init_idea_tree_walk_Scenario1():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    yao_bud.edit_idea_attr(yao_bud._real_id, begin=time0_begin, close=time0_close)
    root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
    assert root_idea._begin == time0_begin
    assert root_idea._close == time0_close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud.init_idea_tree_walk()

    # THEN
    assert root_idea._begin == time0_begin
    assert root_idea._close == time0_close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc


def test_BudUnit_init_idea_tree_walk_Scenario2():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    day_text = "day"
    day_road = yao_bud.make_l1_road(day_text)
    yao_bud.set_l1_idea(ideaunit_shop(day_text))
    day_idea = yao_bud.get_idea_obj(day_road)
    time0_text = "time0"
    time0_road = yao_bud.make_l1_road(time0_text)
    yao_bud.set_l1_idea(ideaunit_shop(time0_text))
    yao_bud.edit_idea_attr(time0_road, range_push=day_road)
    assert not day_idea._begin
    assert not day_idea._close
    assert not day_idea._gogo_calc
    assert not day_idea._stop_calc

    # WHEN
    yao_bud.init_idea_tree_walk()

    # THEN
    assert not day_idea._begin
    assert not day_idea._close
    assert not day_idea._gogo_calc
    assert not day_idea._stop_calc


def test_BudUnit_init_idea_tree_walk_RaisesError():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    day_text = "day"
    day_road = yao_bud.make_l1_road(day_text)
    time0_text = "time0"
    time0_road = yao_bud.make_l1_road(time0_text)
    yao_bud.set_l1_idea(ideaunit_shop(time0_text))
    yao_bud.edit_idea_attr(time0_road, range_push=day_road)
    yao_bud.init_idea_tree_walk()

    time1_text = "time1"
    time1_road = yao_bud.make_l1_road(time1_text)
    yao_bud.set_l1_idea(ideaunit_shop(time1_text))
    yao_bud.edit_idea_attr(time1_road, range_push=day_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.init_idea_tree_walk()
    exception_text = f"Multiple IdeaUnits including ('{time0_road}', '{time1_road}') have range_push '{day_road}'"
    assert str(excinfo.value) == exception_text


def test_BudUnit_init_idea_tree_walk_Clears_gogo_calc_stop_calc():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_idea = sue_bud.get_idea_obj(sue_bud._real_id)
    states_text = "nation-state"
    states_road = sue_bud.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_bud.make_road(states_road, usa_text)
    texas_text = "Texas"
    texas_road = sue_bud.make_road(usa_road, texas_text)
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
    sue_bud.init_idea_tree_walk()

    # THEN
    assert not root_idea._begin
    assert not root_idea._close
    assert not texas_idea._range_evaluated
    assert not texas_idea._gogo_calc
    assert not texas_idea._stop_calc
