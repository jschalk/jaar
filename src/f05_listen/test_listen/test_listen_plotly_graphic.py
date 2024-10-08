from src.f05_listen.examples.example_listen_buds import get_fund_explanation_bud
from src.f05_listen.listen_graphic import (
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
    fund_explanation0,
)


def test_listen_structures0_ShowsExplanation0Graph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_listen_structures0_fig(graphics_bool)
    get_listen_structures1_fig(graphics_bool)
    get_listen_structures2_fig(graphics_bool)
    get_listen_structures3_fig(graphics_bool)


def test_fund_explanation_Graph(graphics_bool):
    # ESTABLISH / WHEN
    x_budunit = get_fund_explanation_bud()
    fund_explanation0(x_budunit, "Task", graphics_bool)
