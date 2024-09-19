from src.s0_instrument.plotly_tool import conditional_fig_show
from src.s4_gift.atom_graphic import atomunit_periodic_table0

# from src.s2_bud.examples.example_buds import (
#     budunit_v001_with_large_agenda,
#     get_budunit_with_4_levels,
#     get_budunit_with_4_levels_and_2reasons,
#     get_budunit_x1_3levels_1reason_1facts,
# )
# from src.s2_bud.bud import budunit_shop


def test_atomunit_periodic_table0_ShowsExplanation0Graph(graphics_bool):
    # ESTABLISH / WHEN
    atomunit_periodic_table0_fig = atomunit_periodic_table0()

    # THEN
    conditional_fig_show(atomunit_periodic_table0_fig, graphics_bool)
