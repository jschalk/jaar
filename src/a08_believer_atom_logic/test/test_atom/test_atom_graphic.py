from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a08_believer_atom_logic.atom_graphic import believeratom_periodic_table0

# from src.a06_believer_logic.test._util.example_believers import (
#     believerunit_v001_with_large_agenda,
#     get_believerunit_with_4_levels,
#     get_believerunit_with_4_levels_and_2reasons,
#     get_believerunit_x1_3levels_1reason_1facts,
# )
# from src.a06_believer_logic.believer import believerunit_shop


def test_believeratom_periodic_table0_ShowsGraph0(graphics_bool):
    # ESTABLISH / WHEN
    believeratom_periodic_table0_fig = believeratom_periodic_table0()

    # THEN
    conditional_fig_show(believeratom_periodic_table0_fig, graphics_bool)
