from src.a06_plan_logic.plan_graphics import (
    display_concepttree,
    planunit_graph0,
    planunit_graph1,
    planunit_graph2,
    planunit_graph3,
    planunit_graph4,
)
from src.a06_plan_logic.test._util.example_plans import (
    get_planunit_with_4_levels,
    get_planunit_with_4_levels_and_2reasons,
    get_planunit_x1_3levels_1reason_1facts,
)


def test_planunit_graph_Showsgraph0PlanGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_concepttree(get_planunit_with_4_levels(), graphics_bool)
    display_concepttree(
        get_planunit_with_4_levels_and_2reasons(), "Chore", graphics_bool
    )
    display_concepttree(get_planunit_x1_3levels_1reason_1facts(), graphics_bool)
    planunit_graph0(graphics_bool)
    planunit_graph1(graphics_bool)
    planunit_graph2(graphics_bool)
    planunit_graph3(graphics_bool)
    planunit_graph4(graphics_bool)
