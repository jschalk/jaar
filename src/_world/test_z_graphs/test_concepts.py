from src._world.examples.example_worlds import (
    world_v001_with_large_agenda,
    get_world_with_4_levels,
    get_world_assignment_laundry_example1,
    get_world_with_4_levels_and_2reasons,
    get_world_x1_3levels_1reason_1facts,
)
from src._world.world import worldunit_shop
from src._world.graphic import (
    worldunit_explanation0,
    worldunit_explanation1,
    worldunit_explanation2,
    worldunit_explanation3,
    worldunit_explanation4,
    fiscal_explanation0,
)


def test_worldunit_explanation_ShowsExplanation0WorldConceptGraph():
    # GIVEN / WHEN
    worldunit_explanation0_fig = worldunit_explanation0()
    worldunit_explanation1_fig = worldunit_explanation1()
    worldunit_explanation2_fig = worldunit_explanation2()
    worldunit_explanation3_fig = worldunit_explanation3()
    worldunit_explanation4_fig = worldunit_explanation4()
    fiscal_explanation0_fig = fiscal_explanation0()

    # # THEN
    # show_figure = True
    # if show_figure:
    #     # worldunit_explanation0_fig.show()
    #     # worldunit_explanation1_fig.show()
    #     # worldunit_explanation2_fig.show()
    #     # worldunit_explanation3_fig.show()
    #     # worldunit_explanation4_fig.show()
    #     fiscal_explanation0_fig.show()

    # assert 1 == 2

    # # a_world = get_1node_world()
    # # a_world = get_2node_world()
    # # a_world = get_3node_world()
    # # a_world = get_5nodeHG_world()
    # # a_world = get_7nodeJRoot_world()
    # a_world = get_world_with_4_levels()
    # # a_world = world_v001()
    # a_world.calc_world_metrics()
    # print(f"World {a_world._real_id}: Nodes ({len(a_world._idea_dict)})")

    # # WHEN
    # x_fig = concept_world_level0(a_world)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
