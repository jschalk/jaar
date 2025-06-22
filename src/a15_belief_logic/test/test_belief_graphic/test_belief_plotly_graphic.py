from src.a15_belief_logic.belief_graphic import (  # get_belief_structures5_fig,
    get_belief_structures0_fig,
)


def test_belief_graphics_ExplainedWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_belief_structures0_fig(graphics_bool)
