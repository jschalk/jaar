from src.a13_owner_listen_logic.listen_graphic import (
    fund_graph0,
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
)
from src.a13_owner_listen_logic.test._util.example_listen_owners import (
    get_fund_breakdown_owner,
)


def test_listen_structures0_ShowsGraphs(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_listen_structures0_fig(graphics_bool)
    get_listen_structures1_fig(graphics_bool)
    get_listen_structures2_fig(graphics_bool)
    get_listen_structures3_fig(graphics_bool)


def test_fund_graph_ShowsGraph(graphics_bool):
    # ESTABLISH / WHEN
    x_ownerunit = get_fund_breakdown_owner()
    fund_graph0(x_ownerunit, "Chore", graphics_bool)
