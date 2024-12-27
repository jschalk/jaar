from src.f07_deal.deal_graphic import (
    get_deal_structures0_fig,
    # get_deal_structures5_fig,
)


def test_deal_graphics_ExplainThingsWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_deal_structures0_fig(graphics_bool)
