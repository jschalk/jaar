from src.bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
)
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.bud.group import awardlink_shop
from src.bud.graphic import display_ideatree
from pytest import raises as pytest_raises


def test_BudUnit_tree_range_push_traverse_check_Scenario0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    # WHEN / THEN
    yao_bud.tree_range_push_traverse_check()


def test_BudUnit_tree_range_push_traverse_check_Scenario1():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    day_text = "day"
    day_road = yao_bud.make_l1_road(day_text)
    time0_text = "time0"
    time0_road = yao_bud.make_l1_road(time0_text)
    yao_bud.set_l1_idea(ideaunit_shop(time0_text))
    yao_bud.edit_idea_attr(time0_road, range_push=day_road)
    yao_bud.tree_range_push_traverse_check()


def test_BudUnit_tree_range_push_traverse_check_RaisesError():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    day_text = "day"
    day_road = yao_bud.make_l1_road(day_text)
    time0_text = "time0"
    time0_road = yao_bud.make_l1_road(time0_text)
    yao_bud.set_l1_idea(ideaunit_shop(time0_text))
    yao_bud.edit_idea_attr(time0_road, range_push=day_road)
    yao_bud.tree_range_push_traverse_check()

    time1_text = "time1"
    time1_road = yao_bud.make_l1_road(time1_text)
    yao_bud.set_l1_idea(ideaunit_shop(time1_text))
    yao_bud.edit_idea_attr(time1_road, range_push=day_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.tree_range_push_traverse_check()
    assert (
        str(excinfo.value)
        == f"Multiple IdeaUnits including ('{time0_road}', '{time1_road}') have range_push '{day_road}'"
    )


def test_BudUnit_tree_range_push_traverse_calc_Scenario0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    yao_bud.tree_range_push_traverse_calc()


# def test_BudUnit_tree_range_push_traverse_calc_Scenario1():
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
