from src.pecun.pecun_graphic import (
    get_pecun_structures0_fig,
    # get_pecun_structures5_fig,
)


def test_pecun_graphics_ExplainThingsWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_pecun_structures0_fig(graphics_bool)
