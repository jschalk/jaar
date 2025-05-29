from src.a06_bud_logic.bud_graphics import (
    display_concepttree,
    budunit_graph0,
    budunit_graph1,
    budunit_graph2,
    budunit_graph3,
    budunit_graph4,
)
from src.a06_bud_logic._test_util.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_x1_3levels_1reason_1facts,
)


def test_budunit_graph_Showsgraph0BudGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_concepttree(get_budunit_with_4_levels(), graphics_bool)
    display_concepttree(get_budunit_with_4_levels_and_2reasons(), "Task", graphics_bool)
    display_concepttree(get_budunit_x1_3levels_1reason_1facts(), graphics_bool)
    budunit_graph0(graphics_bool)
    budunit_graph1(graphics_bool)
    budunit_graph2(graphics_bool)
    budunit_graph3(graphics_bool)
    budunit_graph4(graphics_bool)
