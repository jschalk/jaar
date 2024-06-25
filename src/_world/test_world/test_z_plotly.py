from src._world.examples.example_worlds import (
    world_v001_with_large_agenda,
    get_world_with_4_levels,
    get_world_assignment_laundry_example1,
    get_world_with_4_levels_and_2reasons,
    get_world_x1_3levels_1reason_1facts,
)
from src._world.world import worldunit_shop
from src._world.graphic import (
    display_ideatree,
    get_world_persons_plotly_fig,
    get_world_agenda_plotly_fig,
)


def test_display_ideatree_GivenWorld():
    # a_world = get_1node_world()
    # a_world = get_2node_world()
    # a_world = get_3node_world()
    # a_world = get_5nodeHG_world()
    # a_world = get_7nodeJRoot_world()
    a_world = get_world_with_4_levels()
    # a_world = world_v001()
    a_world.calc_world_metrics()
    print(f"World {a_world._real_id}: Nodes ({len(a_world._idea_dict)})")

    # WHEN
    x_fig = display_ideatree(a_world)

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_display_ideatree_GivenWorld_shows_Tasks():
    # a_world = get_1node_world()
    # a_world = get_2node_world()
    # a_world = get_3node_world()
    # a_world = get_5nodeHG_world()
    # a_world = get_7nodeJRoot_world()
    a_world = get_world_assignment_laundry_example1()
    # a_world = world_v001()
    a_world.calc_world_metrics()
    print(f"World {a_world._real_id}: Nodes ({len(a_world._idea_dict)})")

    # WHEN
    x_fig = display_ideatree(a_world, mode="Task")

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_get_world_persons_plotly_fig_DisplaysCorrectInfo():
    # GIVEN
    luca_world = worldunit_shop()
    luca_world.set_person_credor_pool(500)
    luca_world.set_person_debtor_pool(400)
    todd_text = "Todd"
    todd_credor_weight = 66
    todd_debtor_weight = 77
    luca_world.add_personunit(todd_text, todd_credor_weight, todd_debtor_weight)
    sue_text = "Sue"
    sue_credor_weight = 434
    sue_debtor_weight = 323
    luca_world.add_personunit(sue_text, sue_credor_weight, sue_debtor_weight)

    # WHEN
    x_fig = get_world_persons_plotly_fig(luca_world)

    # THEN
    # show_figure = True
    # if show_figure:
    #   x_fig.show()


def test_get_world_agenda_plotly_fig_DisplaysCorrectInfo():
    # GIVEN
    yao_world = world_v001_with_large_agenda()
    week_text = "weekdays"
    week_road = yao_world.make_l1_road(week_text)
    assert len(yao_world.get_agenda_dict()) == 63

    # WHEN
    x_fig = get_world_agenda_plotly_fig(yao_world)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
