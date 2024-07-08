# from src._world.examples.example_worlds import (
#     world_v001_with_large_agenda,
#     get_world_with_4_levels,
#     get_world_with_4_levels_and_2reasons,
#     get_world_x1_3levels_1reason_1facts,
# )
# from src._world.world import worldunit_shop
from src.listen.listen_graphic import (
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
)


def test_listen_structures0_ShowsExplanation0Graph():
    # GIVEN / WHEN
    listen_structures0_fig = get_listen_structures0_fig()
    listen_structures1_fig = get_listen_structures1_fig()
    listen_structures2_fig = get_listen_structures2_fig()
    listen_structures3_fig = get_listen_structures3_fig()

    # # THEN
    # show_figure = True
    # if show_figure:
    #     listen_structures0_fig.show()
    #     # listen_structures1_fig.show()
    #     # listen_structures2_fig.show()
    #     # listen_structures3_fig.show()
