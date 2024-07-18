# from src.bud.examples.example_buds import (
#     budunit_v001_with_large_agenda,
#     get_bud_with_4_levels,
#     get_bud_with_4_levels_and_2reasons,
#     get_bud_x1_3levels_1reason_1facts,
# )
# from src.bud.bud import budunit_shop
from src.gift.atom_graphic import atomunit_periodic_table0


def test_atomunit_periodic_table0_ShowsExplanation0Graph():
    # ESTABLISH / WHEN
    atomunit_periodic_table0_fig = atomunit_periodic_table0()

    # # THEN
    # show_figure = True
    # if show_figure:
    #     atomunit_periodic_table0_fig.show()
