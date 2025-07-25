from src.a06_believer_logic.believer_graphics import (
    believerunit_graph0,
    believerunit_graph1,
    believerunit_graph2,
    believerunit_graph3,
    believerunit_graph4,
    display_plantree,
)
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
    get_believerunit_with_4_levels_and_2reasons,
    get_believerunit_x1_3levels_1reason_1facts,
)


def test_believerunit_graph_Showsgraph0BelieverGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_plantree(get_believerunit_with_4_levels(), graphics_bool)
    display_plantree(
        get_believerunit_with_4_levels_and_2reasons(), "Chore", graphics_bool
    )
    display_plantree(get_believerunit_x1_3levels_1reason_1facts(), graphics_bool)
    believerunit_graph0(graphics_bool)
    believerunit_graph1(graphics_bool)
    believerunit_graph2(graphics_bool)
    believerunit_graph3(graphics_bool)
    believerunit_graph4(graphics_bool)
