from src.bud.examples.example_buds import get_budunit_with_4_levels_and_2reasons
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_set_ideaunits_range_SetsInitialIdea_gogo_calc_stop_calc_UnitDoesNotErrorWithEmptyBudUnit():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    assert not root_idea.begin
    assert not root_idea.close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert not root_idea.begin
    assert not root_idea.close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc


def test_BudUnit_set_ideaunits_range_SetsInitialIdea_gogo_calc_stop_calc_DoesNotErrorWhenNoMathNodes():
    # ESTABLISH
    yao_bud = get_budunit_with_4_levels_and_2reasons()
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    assert not root_idea._gogo_calc

    # WHEM
    yao_bud._set_ideaunits_range()

    # THEN
    assert not root_idea._gogo_calc


def test_BudUnit_set_ideaunits_range_SetsInitialIdea_gogo_calc_stop_calc_SimpleNode():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    yao_bud.edit_idea_attr(yao_bud._tribe_id, begin=time0_begin, close=time0_close)
    yao_bud._init_idea_tree_walk()
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea._gogo_calc == time0_begin
    assert root_idea._stop_calc == time0_close


def test_BudUnit_set_ideaunits_range_SetsInitialIdea_gogo_calc_stop_calc_NodeWith_denom():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 21
    time0_denom = 3
    yao_bud.edit_idea_attr(
        yao_bud._tribe_id,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
    )
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea.denom == time0_denom
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea._gogo_calc == time0_begin / time0_denom
    assert root_idea._stop_calc == time0_close / time0_denom
    assert root_idea._gogo_calc == 2
    assert root_idea._stop_calc == 7


def test_BudUnit_set_ideaunits_range_SetsInitialIdea_gogo_calc_stop_calc_NodeWith_denom_numor():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 18
    time0_numor = 7
    time0_denom = 3
    yao_bud.edit_idea_attr(
        yao_bud._tribe_id,
        begin=time0_begin,
        close=time0_close,
        numor=time0_numor,
        denom=time0_denom,
    )
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea.numor == time0_numor
    assert root_idea.denom == time0_denom
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea._gogo_calc == (time0_begin * time0_numor) / time0_denom
    assert root_idea._stop_calc == (time0_close * time0_numor) / time0_denom
    assert root_idea._gogo_calc == 14
    assert root_idea._stop_calc == 42


def test_BudUnit_set_ideaunits_range_SetsInitialIdea_gogo_calc_stop_calc_NodeWith_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 18
    time0_addin = 7
    yao_bud.edit_idea_attr(
        yao_bud._tribe_id,
        begin=time0_begin,
        close=time0_close,
        addin=time0_addin,
    )
    yao_bud._init_idea_tree_walk()
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea.addin == time0_addin
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea._gogo_calc == time0_begin + time0_addin
    assert root_idea._stop_calc == time0_close + time0_addin
    assert root_idea._gogo_calc == 13
    assert root_idea._stop_calc == 25


def test_BudUnit_set_ideaunits_range_SetsInitialIdea_gogo_calc_stop_calc_NodeWith_denom_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 18
    time0_denom = 3
    time0_addin = 60
    yao_bud.edit_idea_attr(
        yao_bud._tribe_id,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
        addin=time0_addin,
    )
    yao_bud._init_idea_tree_walk()
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea.denom == time0_denom
    assert root_idea.addin == time0_addin
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert root_idea.begin == time0_begin
    assert root_idea.close == time0_close
    assert root_idea._gogo_calc == (time0_begin + time0_addin) / time0_denom
    assert root_idea._stop_calc == (time0_close + time0_addin) / time0_denom
    assert root_idea._gogo_calc == 22
    assert root_idea._stop_calc == 26


def test_BudUnit_set_ideaunits_range_SetsDescendentIdea_gogo_calc_stop_calc_Simple0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 7
    time0_close = 31
    time0_idea = ideaunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_idea(time0_idea)

    time1_str = "time1"
    time1_road = yao_bud.make_road(time0_road, time1_str)
    yao_bud.set_idea(ideaunit_shop(time1_str), time0_road)
    time1_idea = yao_bud.get_idea_obj(time1_road)
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert time0_idea.begin == time0_begin
    assert time0_idea.close == time0_close
    assert time1_idea.begin != time0_begin
    assert time1_idea.close != time0_close
    assert not time1_idea._gogo_calc
    assert not time1_idea._stop_calc
    assert yao_bud._range_inheritors == {}

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert time1_idea.begin != time0_begin
    assert time1_idea.close != time0_close
    assert not time1_idea.begin
    assert not time1_idea.close
    assert time1_idea._gogo_calc == time0_begin
    assert time1_idea._stop_calc == time0_close
    assert yao_bud._range_inheritors == {time1_road: time0_road}


def test_BudUnit_set_ideaunits_range_SetsDescendentIdea_gogo_calc_stop_calc_NodeWith_denom():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_idea = ideaunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_idea(time0_idea)

    time1_str = "time1"
    time1_denom = 7
    time1_road = yao_bud.make_road(time0_road, time1_str)
    yao_bud.set_idea(ideaunit_shop(time1_str, denom=time1_denom), time0_road)
    time1_idea = yao_bud.get_idea_obj(time1_road)
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert time0_idea.begin == time0_begin
    assert time0_idea.close == time0_close
    assert time1_idea.begin != time0_begin
    assert time1_idea.close != time0_close
    assert not time1_idea._gogo_calc
    assert not time1_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert not time1_idea.begin
    assert not time1_idea.close
    assert time1_idea._gogo_calc == time0_begin / time1_denom
    assert time1_idea._stop_calc == time0_close / time1_denom
    assert time1_idea._gogo_calc == 2
    assert time1_idea._stop_calc == 5


def test_BudUnit_set_ideaunits_range_SetsDescendentIdea_gogo_calc_stop_calc_NodeWith_denom_numor():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_idea = ideaunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_idea(time0_idea)

    time1_str = "time1"
    time1_denom = 7
    time1_numor = 3
    time1_road = yao_bud.make_road(time0_road, time1_str)
    temp_idea = ideaunit_shop(time1_str, numor=time1_numor, denom=time1_denom)
    yao_bud.set_idea(temp_idea, time0_road)
    time1_idea = yao_bud.get_idea_obj(time1_road)
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert time0_idea.begin == time0_begin
    assert time0_idea.close == time0_close
    assert time1_idea.begin != time0_begin
    assert time1_idea.close != time0_close
    assert not time1_idea._gogo_calc
    assert not time1_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert not time1_idea.begin
    assert not time1_idea.close
    assert time1_idea._gogo_calc == (time0_begin * time1_numor) / time1_denom
    assert time1_idea._stop_calc == (time0_close * time1_numor) / time1_denom
    assert time1_idea._gogo_calc == 6
    assert time1_idea._stop_calc == 15


def test_BudUnit_set_ideaunits_range_SetsDescendentIdea_gogo_calc_stop_calc_NodeWith_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_idea = ideaunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_idea(time0_idea)

    time1_str = "time1"
    time1_addin = 5
    time1_road = yao_bud.make_road(time0_road, time1_str)
    temp_idea = ideaunit_shop(time1_str, addin=time1_addin)
    yao_bud.set_idea(temp_idea, time0_road)
    time1_idea = yao_bud.get_idea_obj(time1_road)
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert time0_idea.begin == time0_begin
    assert time0_idea.close == time0_close
    assert time1_idea.begin != time0_begin
    assert time1_idea.close != time0_close
    assert time1_idea.addin == time1_addin
    assert not time1_idea._gogo_calc
    assert not time1_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert not time1_idea.begin
    assert not time1_idea.close
    assert time1_idea._gogo_calc == time0_idea._gogo_calc + time1_addin
    assert time1_idea._stop_calc == time0_idea._stop_calc + time1_addin
    assert time1_idea._gogo_calc == 8
    assert time1_idea._stop_calc == 12


def test_BudUnit_set_ideaunits_range_Sets2LevelsDescendentIdea_gogo_calc_stop_calc_NodeWith_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_idea = ideaunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_idea(time0_idea)

    time1_str = "time1"
    time1_road = yao_bud.make_road(time0_road, time1_str)
    yao_bud.add_idea(time1_road)
    time2_str = "time2"
    time2_road = yao_bud.make_road(time1_road, time2_str)
    time2_addin = 5
    x_time2_idea = ideaunit_shop(time2_str, addin=time2_addin)
    yao_bud.set_idea(x_time2_idea, time1_road)
    time2_idea = yao_bud.get_idea_obj(time2_road)
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert time0_idea.begin == time0_begin
    assert time0_idea.close == time0_close
    assert time2_idea.begin != time0_begin
    assert time2_idea.close != time0_close
    assert time2_idea.addin == time2_addin
    assert not time2_idea._gogo_calc
    assert not time2_idea._stop_calc
    assert yao_bud._range_inheritors == {}

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert not time2_idea.begin
    assert not time2_idea.close
    assert time2_idea._gogo_calc == time0_idea._gogo_calc + time2_addin
    assert time2_idea._stop_calc == time0_idea._stop_calc + time2_addin
    assert time2_idea._gogo_calc == 8
    assert time2_idea._stop_calc == 12
    assert yao_bud._range_inheritors == {time1_road: time0_road, time2_road: time0_road}


def test_BudUnit_set_ideaunits_range_SetsDescendentIdea_gogo_calc_stop_calc_NodeWith_denom_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 21
    time0_close = 35
    time0_idea = ideaunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_idea(time0_idea)

    time1_str = "time1"
    time1_addin = 70
    time1_denom = 7
    time1_road = yao_bud.make_road(time0_road, time1_str)
    temp_idea = ideaunit_shop(time1_str, denom=time1_denom, addin=time1_addin)
    yao_bud.set_idea(temp_idea, time0_road)
    time1_idea = yao_bud.get_idea_obj(time1_road)
    root_idea = yao_bud.get_idea_obj(yao_bud._tribe_id)
    yao_bud._init_idea_tree_walk()
    assert not root_idea._gogo_calc
    assert not root_idea._stop_calc
    assert time0_idea.begin == time0_begin
    assert time0_idea.close == time0_close
    assert time1_idea.begin != time0_begin
    assert time1_idea.close != time0_close
    assert time1_idea.addin == time1_addin
    assert not time1_idea._gogo_calc
    assert not time1_idea._stop_calc

    # WHEN
    yao_bud._set_ideaunits_range()

    # THEN
    assert not time1_idea.begin
    assert not time1_idea.close
    assert time1_idea._gogo_calc == (time0_idea._gogo_calc + time1_addin) / time1_denom
    assert time1_idea._stop_calc == (time0_idea._stop_calc + time1_addin) / time1_denom
    assert time1_idea._gogo_calc == 13
    assert time1_idea._stop_calc == 15
