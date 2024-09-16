from src.s7_fiscal.fiscal_graphic import (
    get_fiscal_structures0_fig,
    # get_fiscal_structures5_fig,
)


def test_fiscal_graphics_ExplainThingsWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_fiscal_structures0_fig(graphics_bool)
