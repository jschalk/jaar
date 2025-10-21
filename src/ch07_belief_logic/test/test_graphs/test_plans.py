from src.ch07_belief_logic.belief_graphics import (
    beliefunit_graph0,
    beliefunit_graph1,
    beliefunit_graph2,
    beliefunit_graph3,
    beliefunit_graph4,
    display_plantree,
)
from src.ch07_belief_logic.test._util.ch07_examples import (
    get_beliefunit_with_4_levels,
    get_beliefunit_with_4_levels_and_2reasons,
    get_beliefunit_x1_3levels_1reason_1facts,
)
from src.ref.keywords import Ch07Keywords as kw


def test_beliefunit_graph_Showsgraph0BeliefGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_plantree(get_beliefunit_with_4_levels(), graphics_bool)
    display_plantree(
        get_beliefunit_with_4_levels_and_2reasons(), kw.task, graphics_bool
    )
    display_plantree(get_beliefunit_x1_3levels_1reason_1facts(), graphics_bool)
    beliefunit_graph0(graphics_bool)
    beliefunit_graph1(graphics_bool)
    beliefunit_graph2(graphics_bool)
    beliefunit_graph3(graphics_bool)
    beliefunit_graph4(graphics_bool)
