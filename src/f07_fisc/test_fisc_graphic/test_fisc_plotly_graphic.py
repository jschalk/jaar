from src.f07_fisc.fisc_graphic import (
    get_fisc_structures0_fig,
    # get_fisc_structures5_fig,
)


def test_fisc_graphics_ExplainedWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_fisc_structures0_fig(graphics_bool)
