from src._instrument.python_tool import conditional_fig_show
from src.hear.examples.example_hear_buds import get_fund_explanation_bud
from src.hear.hear_graphic import (
    get_hear_structures0_fig,
    get_hear_structures1_fig,
    get_hear_structures2_fig,
    get_hear_structures3_fig,
    fund_explanation0,
)


def test_hear_structures0_ShowsExplanation0Graph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_hear_structures0_fig(graphics_bool)
    get_hear_structures1_fig(graphics_bool)
    get_hear_structures2_fig(graphics_bool)
    get_hear_structures3_fig(graphics_bool)


def test_fund_explanation_Graph(graphics_bool):
    # ESTABLISH / WHEN
    x_budunit = get_fund_explanation_bud()
    fund_explanation0(x_budunit, "Task", graphics_bool)
