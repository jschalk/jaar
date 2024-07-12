from src._world.examples.example_worlds import (
    get_world_with_4_levels,
    get_world_with_4_levels_and_2reasons,
    get_world_x1_3levels_1reason_1facts,
)
from src._world.graphic import (
    display_ideatree,
    worldunit_explanation0,
    worldunit_explanation1,
    worldunit_explanation2,
    worldunit_explanation3,
    worldunit_explanation4,
)


def test_worldunit_explanation_ShowsExplanation0WorldConceptGraph():
    # GIVEN / WHEN
    ideatree1 = display_ideatree(get_world_with_4_levels())
    ideatree2 = display_ideatree(get_world_with_4_levels_and_2reasons(), "Task")
    ideatree3 = display_ideatree(get_world_x1_3levels_1reason_1facts())
    worldunit_explanation0_fig = worldunit_explanation0()
    worldunit_explanation1_fig = worldunit_explanation1()
    worldunit_explanation2_fig = worldunit_explanation2()
    worldunit_explanation3_fig = worldunit_explanation3()
    worldunit_explanation4_fig = worldunit_explanation4()

    # # THEN
    # ideatree0.show()
    # ideatree1.show()
    # ideatree2.show()
    # ideatree3.show()
    # worldunit_explanation0_fig.show()
    # worldunit_explanation1_fig.show()
    # worldunit_explanation2_fig.show()
    # worldunit_explanation3_fig.show()
    # worldunit_explanation4_fig.show()
