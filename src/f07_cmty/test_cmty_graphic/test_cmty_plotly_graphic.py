from src.f07_cmty.cmty_graphic import (
    get_cmty_structures0_fig,
    # get_cmty_structures5_fig,
)


def test_cmty_graphics_ExplainedWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_cmty_structures0_fig(graphics_bool)
