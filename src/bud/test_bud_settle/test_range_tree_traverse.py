# from src.bud.examples.example_buds import (
#     get_budunit_with_4_levels,
#     get_budunit_with_4_levels_and_2reasons,
# )
# from src.bud.idea import ideaunit_shop
# from src.bud.bud import budunit_shop
# from src.bud.group import awardlink_shop
# from src.bud.graphic import display_ideatree
# from pytest import raises as pytest_raises


# def test_BudUnit_tree_range_push_traverse_check_Scenario0():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
#     assert not root_idea._begin
#     assert not root_idea._close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc

#     # WHEN
#     yao_bud.tree_range_push_traverse_check()

#     # THEN
#     assert not root_idea._begin
#     assert not root_idea._close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc


# def test_BudUnit_tree_range_push_traverse_check_Scenario1():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     time0_begin = 7
#     time0_close = 31
#     yao_bud.edit_idea_attr(yao_bud._real_id, begin=time0_begin, close=time0_close)
#     root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
#     assert root_idea._begin == time0_begin
#     assert root_idea._close == time0_close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc

#     # WHEN
#     yao_bud.tree_range_push_traverse_check()

#     # THEN
#     assert root_idea._begin == time0_begin
#     assert root_idea._close == time0_close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc


# def test_BudUnit_tree_range_push_traverse_check_Scenario2():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     day_text = "day"
#     day_road = yao_bud.make_l1_road(day_text)
#     yao_bud.set_l1_idea(ideaunit_shop(day_text))
#     day_idea = yao_bud.get_idea_obj(day_road)
#     time0_text = "time0"
#     time0_road = yao_bud.make_l1_road(time0_text)
#     yao_bud.set_l1_idea(ideaunit_shop(time0_text))
#     yao_bud.edit_idea_attr(time0_road, range_push=day_road)
#     assert not day_idea._begin
#     assert not day_idea._close
#     assert not day_idea._gogo_calc
#     assert not day_idea._stop_calc

#     # WHEN
#     yao_bud.tree_range_push_traverse_check()

#     # THEN
#     assert not day_idea._begin
#     assert not day_idea._close
#     assert not day_idea._gogo_calc
#     assert not day_idea._stop_calc


# def test_BudUnit_tree_range_push_traverse_check_RaisesError():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     day_text = "day"
#     day_road = yao_bud.make_l1_road(day_text)
#     time0_text = "time0"
#     time0_road = yao_bud.make_l1_road(time0_text)
#     yao_bud.set_l1_idea(ideaunit_shop(time0_text))
#     yao_bud.edit_idea_attr(time0_road, range_push=day_road)
#     yao_bud.tree_range_push_traverse_check()

#     time1_text = "time1"
#     time1_road = yao_bud.make_l1_road(time1_text)
#     yao_bud.set_l1_idea(ideaunit_shop(time1_text))
#     yao_bud.edit_idea_attr(time1_road, range_push=day_road)

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         yao_bud.tree_range_push_traverse_check()
#     assert (
#         str(excinfo.value)
#         == f"Multiple IdeaUnits including ('{time0_road}', '{time1_road}') have range_push '{day_road}'"
#     )


# def test_BudUnit_tree_arithmetic_traverse_calc_Scenario0():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
#     assert not root_idea._begin
#     assert not root_idea._close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc

#     # WHEN
#     yao_bud.tree_arithmetic_traverse_calc()

#     # THEN
#     assert not root_idea._begin
#     assert not root_idea._close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc


# def test_BudUnit_tree_arithmetic_traverse_calc_Scenario1():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     time0_begin = 7
#     time0_close = 31
#     yao_bud.edit_idea_attr(yao_bud._real_id, begin=time0_begin, close=time0_close)
#     root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
#     assert root_idea._begin == time0_begin
#     assert root_idea._close == time0_close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc

#     # WHEN
#     yao_bud.tree_arithmetic_traverse_calc()

#     # THEN
#     assert root_idea._begin == time0_begin
#     assert root_idea._close == time0_close
#     assert root_idea._gogo_calc == time0_begin
#     assert root_idea._stop_calc == time0_close


# def test_BudUnit_tree_arithmetic_traverse_calc_Scenario2():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     time0_text = "time0"
#     time0_road = yao_bud.make_l1_road(time0_text)
#     time0_begin = 7
#     time0_close = 31
#     time0_idea = ideaunit_shop(time0_text, _begin=time0_begin, _close=time0_close)
#     yao_bud.set_l1_idea(time0_idea)

#     time1_text = "time1"
#     time1_road = yao_bud.make_road(time0_road, time1_text)
#     yao_bud.set_idea(ideaunit_shop(time1_text), time0_road)
#     time1_idea = yao_bud.get_idea_obj(time1_road)
#     root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
#     assert root_idea._begin == time0_begin
#     assert root_idea._close == time0_close
#     assert not root_idea._gogo_calc
#     assert not root_idea._stop_calc
#     assert time1_idea._begin != time0_begin
#     assert time1_idea._close != time0_close

#     # WHEN
#     yao_bud.tree_arithmetic_traverse_calc()

#     # THEN
#     assert time1_idea._begin == time0_begin
#     assert time1_idea._close == time0_close


# def test_BudUnit_tree_arithmetic_traverse_calc_Scenario2():
#     # ESTABLISH
#     yao_bud = budunit_shop("Yao")
#     day_text = "day"
#     day_road = yao_bud.make_l1_road(day_text)
#     yao_bud.set_l1_idea(ideaunit_shop(day_text))
#     time0_text = "time0"
#     time0_road = yao_bud.make_l1_road(time0_text)
#     time0_begin = 7
#     time0_close = 31
#     time0_idea = ideaunit_shop(time0_text, _begin=time0_begin, _close=time0_close)
#     yao_bud.set_l1_idea(time0_idea)
#     yao_bud.edit_idea_attr(time0_road, range_push=day_road)
#     day_idea = yao_bud.get_idea_obj(day_road)
#     assert day_idea._begin != time0_begin
#     assert day_idea._close != time0_close

#     # WHEN
#     yao_bud.tree_arithmetic_traverse_calc()

#     # THEN
#     assert day_idea._begin == time0_begin
#     assert day_idea._close == time0_close
