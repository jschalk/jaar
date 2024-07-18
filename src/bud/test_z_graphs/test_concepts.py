from src.bud.examples.example_buds import (
    get_bud_with_4_levels,
    get_bud_with_4_levels_and_2reasons,
    get_bud_x1_3levels_1reason_1facts,
)
from src.bud.graphic import (
    display_ideatree,
    budunit_explanation0,
    budunit_explanation1,
    budunit_explanation2,
    budunit_explanation3,
    budunit_explanation4,
)


def test_budunit_explanation_ShowsExplanation0BudConceptGraph():
    # ESTABLISH / WHEN
    ideatree1 = display_ideatree(get_bud_with_4_levels())
    ideatree2 = display_ideatree(get_bud_with_4_levels_and_2reasons(), "Task")
    ideatree3 = display_ideatree(get_bud_x1_3levels_1reason_1facts())
    budunit_explanation0_fig = budunit_explanation0()
    budunit_explanation1_fig = budunit_explanation1()
    budunit_explanation2_fig = budunit_explanation2()
    budunit_explanation3_fig = budunit_explanation3()
    budunit_explanation4_fig = budunit_explanation4()

    # # THEN
    # ideatree0.show()
    # ideatree1.show()
    # ideatree2.show()
    # ideatree3.show()
    # budunit_explanation0_fig.show()
    # budunit_explanation1_fig.show()
    # budunit_explanation2_fig.show()
    # budunit_explanation3_fig.show()
    # budunit_explanation4_fig.show()
