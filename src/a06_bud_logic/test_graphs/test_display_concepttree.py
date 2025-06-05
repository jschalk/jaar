from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a06_bud_logic._test_util.example_buds import (
    budunit_v001_with_large_agenda,
    get_budunit_laundry_example1,
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_x1_3levels_1reason_1facts,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_graphics import (
    display_concepttree,
    fund_graph0,
    get_bud_accts_plotly_fig,
    get_bud_agenda_plotly_fig,
)


def test_display_concepttree_Scenario0(graphics_bool):
    # a_bud = get_1label_bud()
    # a_bud = get_2label_bud()
    # a_bud = get_3label_bud()
    # a_bud = get_5labelHG_bud()
    # a_bud = get_7labelJRoot_bud()
    a_bud = get_budunit_with_4_levels()
    # a_bud = budunit_v001()
    a_bud.settle_bud()
    print(f"Bud {a_bud.vow_label}: Labels ({len(a_bud._concept_dict)})")

    # WHEN / THEN
    x_fig = display_concepttree(a_bud, graphics_bool)


def test_display_concepttree_Scenario1_shows_Chores(graphics_bool):
    # a_bud = get_1label_bud()
    # a_bud = get_2label_bud()
    # a_bud = get_3label_bud()
    # a_bud = get_5labelHG_bud()
    # a_bud = get_7labelJRoot_bud()
    a_bud = get_budunit_laundry_example1()
    # a_bud = budunit_v001()
    a_bud.settle_bud()
    print(f"Bud {a_bud.vow_label}: Labels ({len(a_bud._concept_dict)})")

    # WHEN / THEN
    display_concepttree(a_bud, mode="Chore", graphics_bool=graphics_bool)


def test_get_bud_accts_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    luca_bud = budunit_shop()
    luca_bud.set_credor_respect(500)
    luca_bud.set_debtor_respect(400)
    yao_str = "Yao"
    yao_credit_belief = 66
    yao_debtit_belief = 77
    luca_bud.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    sue_str = "Sue"
    sue_credit_belief = 434
    sue_debtit_belief = 323
    luca_bud.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)

    # WHEN
    x_fig = get_bud_accts_plotly_fig(luca_bud)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_bud_agenda_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    yao_bud = budunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_way = yao_bud.make_l1_way(wk_str)
    assert len(yao_bud.get_agenda_dict()) == 63

    # WHEN
    x_fig = get_bud_agenda_plotly_fig(yao_bud)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_BudUnit_fund_flow(graphics_bool):
    # ESTABLISH
    sue_bud = budunit_shop(owner_name="Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    cat_str = "cat status"
    cat_way = sue_bud.make_way(casa_way, cat_str)
    hun_n_str = "not hungry"
    hun_n_way = sue_bud.make_way(cat_way, hun_n_str)
    hun_y_str = "hungry"
    hun_y_way = sue_bud.make_way(cat_way, hun_y_str)
    clean_str = "cleaning"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_str = "sweep floor"
    sweep_way = sue_bud.make_way(clean_way, sweep_str)
    dish_str = "clean dishes"
    dish_way = sue_bud.make_way(clean_way, dish_str)
    sue_bud.add_concept(casa_way, mass=30)
    sue_bud.add_concept(cat_way, mass=30)
    sue_bud.add_concept(hun_n_way, mass=30)
    sue_bud.add_concept(hun_y_way, mass=30)
    sue_bud.add_concept(clean_way, mass=30)
    sue_bud.add_concept(sweep_way, mass=30, pledge=True)
    sue_bud.add_concept(dish_way, mass=30, pledge=True)
    dinner_str = "cat have dinner"
    dinner_way = sue_bud.make_l1_way(dinner_str)
    sue_bud.add_concept(dinner_way, mass=30, pledge=True)

    # WHEN / THEN
    fund_graph0(sue_bud, "Chore", graphics_bool)
