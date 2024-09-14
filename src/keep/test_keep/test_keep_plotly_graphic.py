from src.keep.keep_graphic import (
    get_protect_structures0_fig,
    get_protect_structures1_fig,
    get_protect_structures2_fig,
    get_protect_structures3_fig,
    get_protect_structures4_fig,
    get_protect_structures5_fig,
)


def test_money_graphics_ExplainThingsWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_protect_structures0_fig(graphics_bool)
    get_protect_structures1_fig(graphics_bool)
    get_protect_structures2_fig(graphics_bool)
    get_protect_structures3_fig(graphics_bool)
    get_protect_structures4_fig(graphics_bool)
    get_protect_structures5_fig(graphics_bool)
