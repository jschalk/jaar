from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.plan_graphics import (
    display_concepttree,
    fund_graph0,
    get_plan_accts_plotly_fig,
    get_plan_agenda_plotly_fig,
)
from src.a06_plan_logic.test._util.example_plans import (
    get_planunit_laundry_example1,
    get_planunit_with_4_levels,
    get_planunit_with_4_levels_and_2reasons,
    get_planunit_x1_3levels_1reason_1facts,
    planunit_v001_with_large_agenda,
)


def test_display_concepttree_Scenario0(graphics_bool):
    # a_plan = get_1label_plan()
    # a_plan = get_2label_plan()
    # a_plan = get_3label_plan()
    # a_plan = get_5labelHG_plan()
    # a_plan = get_7labelJRoot_plan()
    a_plan = get_planunit_with_4_levels()
    # a_plan = planunit_v001()
    a_plan.settle_plan()
    print(f"Plan {a_plan.bank_label}: Labels ({len(a_plan._concept_dict)})")

    # WHEN / THEN
    x_fig = display_concepttree(a_plan, graphics_bool)


def test_display_concepttree_Scenario1_shows_Chores(graphics_bool):
    # a_plan = get_1label_plan()
    # a_plan = get_2label_plan()
    # a_plan = get_3label_plan()
    # a_plan = get_5labelHG_plan()
    # a_plan = get_7labelJRoot_plan()
    a_plan = get_planunit_laundry_example1()
    # a_plan = planunit_v001()
    a_plan.settle_plan()
    print(f"Plan {a_plan.bank_label}: Labels ({len(a_plan._concept_dict)})")

    # WHEN / THEN
    display_concepttree(a_plan, mode="Chore", graphics_bool=graphics_bool)


def test_get_plan_accts_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    luca_plan = planunit_shop()
    luca_plan.set_credor_respect(500)
    luca_plan.set_debtor_respect(400)
    yao_str = "Yao"
    yao_credit_score = 66
    yao_debt_score = 77
    luca_plan.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    sue_str = "Sue"
    sue_credit_score = 434
    sue_debt_score = 323
    luca_plan.add_acctunit(sue_str, sue_credit_score, sue_debt_score)

    # WHEN
    x_fig = get_plan_accts_plotly_fig(luca_plan)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_plan_agenda_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    yao_plan = planunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_plan.make_l1_rope(wk_str)
    assert len(yao_plan.get_agenda_dict()) == 63

    # WHEN
    x_fig = get_plan_agenda_plotly_fig(yao_plan)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_PlanUnit_fund_flow(graphics_bool):
    # ESTABLISH
    sue_plan = planunit_shop(owner_name="Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_plan.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_n_rope = sue_plan.make_rope(cat_rope, hun_n_str)
    hun_y_str = "hungry"
    hun_y_rope = sue_plan.make_rope(cat_rope, hun_y_str)
    clean_str = "cleaning"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    sweep_rope = sue_plan.make_rope(clean_rope, sweep_str)
    dish_str = "clean dishes"
    dish_rope = sue_plan.make_rope(clean_rope, dish_str)
    sue_plan.add_concept(casa_rope, mass=30)
    sue_plan.add_concept(cat_rope, mass=30)
    sue_plan.add_concept(hun_n_rope, mass=30)
    sue_plan.add_concept(hun_y_rope, mass=30)
    sue_plan.add_concept(clean_rope, mass=30)
    sue_plan.add_concept(sweep_rope, mass=30, task=True)
    sue_plan.add_concept(dish_rope, mass=30, task=True)
    dinner_str = "cat have dinner"
    dinner_rope = sue_plan.make_l1_rope(dinner_str)
    sue_plan.add_concept(dinner_rope, mass=30, task=True)

    # WHEN / THEN
    fund_graph0(sue_plan, "Chore", graphics_bool)
