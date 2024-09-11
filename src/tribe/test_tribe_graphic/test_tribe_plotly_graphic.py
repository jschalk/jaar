from src.tribe.tribe_graphic import (
    get_tribe_structures0_fig,
    # get_tribe_structures5_fig,
)


def test_tribe_graphics_ExplainThingsWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_tribe_structures0_fig(graphics_bool)
