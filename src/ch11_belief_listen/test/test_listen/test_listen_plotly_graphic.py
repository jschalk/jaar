from src.ch11_belief_listen.listen_graphic import (
    fund_graph13,
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
)
from src.ch11_belief_listen.test._util.ch11_examples import get_fund_breakdown_belief
from src.ref.keywords import Ch11Keywords as kw


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
    fund_graph13(x_beliefunit, kw.task, graphics_bool)
