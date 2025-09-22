from src.ch00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.ch09_belief_atom_logic.atom_graphic import beliefatom_periodic_table0

# from src.ch06_belief_logic.test._util.example_beliefs import (
#     beliefunit_v001_with_large_agenda,
#     get_beliefunit_with_4_levels,
#     get_beliefunit_with_4_levels_and_2reasons,
#     get_beliefunit_x1_3levels_1reason_1facts,
# )
# from src.ch06_belief_logic.belief import beliefunit_shop


def test_beliefatom_periodic_table0_ShowsGraph0(graphics_bool):
    # ESTABLISH / WHEN
    beliefatom_periodic_table0_fig = beliefatom_periodic_table0()

    # THEN
    conditional_fig_show(beliefatom_periodic_table0_fig, graphics_bool)
