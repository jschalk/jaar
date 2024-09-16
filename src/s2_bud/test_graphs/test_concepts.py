from src.s2_bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_x1_3levels_1reason_1facts,
)
from src.s2_bud.graphic import (
    display_ideatree,
    budunit_explanation0,
    budunit_explanation1,
    budunit_explanation2,
    budunit_explanation3,
    budunit_explanation4,
)


def test_budunit_explanation_ShowsExplanation0BudGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_ideatree(get_budunit_with_4_levels(), graphics_bool)
    display_ideatree(get_budunit_with_4_levels_and_2reasons(), "Task", graphics_bool)
    display_ideatree(get_budunit_x1_3levels_1reason_1facts(), graphics_bool)
    budunit_explanation0(graphics_bool)
    budunit_explanation1(graphics_bool)
    budunit_explanation2(graphics_bool)
    budunit_explanation3(graphics_bool)
    budunit_explanation4(graphics_bool)
