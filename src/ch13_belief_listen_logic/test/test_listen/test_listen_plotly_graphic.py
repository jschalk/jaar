from src.ch13_belief_listen_logic.listen_graphic import (
    fund_graph13,
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
)
from src.ch13_belief_listen_logic.test._util.ch13_examples import (
    get_fund_breakdown_belief,
)


def test_listen_structures0_ShowsGraphs(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_listen_structures0_fig(graphics_bool)
    get_listen_structures1_fig(graphics_bool)
    get_listen_structures2_fig(graphics_bool)
    get_listen_structures3_fig(graphics_bool)


def test_fund_graph_ShowsGraph(graphics_bool):
    # ESTABLISH / WHEN
    x_beliefunit = get_fund_breakdown_belief()

    # THEN
    fund_graph13(x_beliefunit, "task", graphics_bool)
