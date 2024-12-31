from src.f07_gov.gov_graphic import (
    get_gov_structures0_fig,
    # get_gov_structures5_fig,
)


def test_gov_graphics_ExplainThingsWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_gov_structures0_fig(graphics_bool)
