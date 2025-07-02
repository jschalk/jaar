from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a08_owner_atom_logic.atom_graphic import owneratom_periodic_table0

# from src.a06_owner_logic.test._util.example_owners import (
#     ownerunit_v001_with_large_agenda,
#     get_ownerunit_with_4_levels,
#     get_ownerunit_with_4_levels_and_2reasons,
#     get_ownerunit_x1_3levels_1reason_1facts,
# )
# from src.a06_owner_logic.owner import ownerunit_shop


def test_owneratom_periodic_table0_ShowsGraph0(graphics_bool):
    # ESTABLISH / WHEN
    owneratom_periodic_table0_fig = owneratom_periodic_table0()

    # THEN
    conditional_fig_show(owneratom_periodic_table0_fig, graphics_bool)
