from src.a13_bud_listen_logic._utils.example_listen_buds import (
    get_fund_breakdown_bud,
)
from src.a13_bud_listen_logic.listen_graphic import (
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
    fund_graph0,
)


def test_listen_structures0_ShowsGraphs(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_listen_structures0_fig(graphics_bool)
    get_listen_structures1_fig(graphics_bool)
    get_listen_structures2_fig(graphics_bool)
    get_listen_structures3_fig(graphics_bool)


def test_fund_graph_ShowsGraph(graphics_bool):
    # ESTABLISH / WHEN
    x_budunit = get_fund_breakdown_bud()
    fund_graph0(x_budunit, "Task", graphics_bool)
