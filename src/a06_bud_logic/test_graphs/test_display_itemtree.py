from src.a00_data_toolboxs.plotly_toolbox import conditional_fig_show
from src.a06_bud_logic.examples.example_buds import (
    budunit_v001_with_large_agenda,
    get_budunit_with_4_levels,
    get_budunit_laundry_example1,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_x1_3levels_1reason_1facts,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_graphics import (
    display_itemtree,
    get_bud_accts_plotly_fig,
    get_bud_agenda_plotly_fig,
    fund_graph0,
)


def test_display_itemtree_Scenario0(graphics_bool):
    # a_bud = get_1title_bud()
    # a_bud = get_2title_bud()
    # a_bud = get_3title_bud()
    # a_bud = get_5titleHG_bud()
    # a_bud = get_7titleJRoot_bud()
    a_bud = get_budunit_with_4_levels()
    # a_bud = budunit_v001()
    a_bud.settle_bud()
    print(f"Bud {a_bud.fisc_title}: Titles ({len(a_bud._item_dict)})")

    # WHEN / THEN
    x_fig = display_itemtree(a_bud, graphics_bool)


def test_display_itemtree_Scenario1_shows_Tasks(graphics_bool):
    # a_bud = get_1title_bud()
    # a_bud = get_2title_bud()
    # a_bud = get_3title_bud()
    # a_bud = get_5titleHG_bud()
    # a_bud = get_7titleJRoot_bud()
    a_bud = get_budunit_laundry_example1()
    # a_bud = budunit_v001()
    a_bud.settle_bud()
    print(f"Bud {a_bud.fisc_title}: Titles ({len(a_bud._item_dict)})")

    # WHEN / THEN
    display_itemtree(a_bud, mode="Task", graphics_bool=graphics_bool)


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
    week_str = "weekdays"
    week_road = yao_bud.make_l1_road(week_str)
    assert len(yao_bud.get_agenda_dict()) == 63

    # WHEN
    x_fig = get_bud_agenda_plotly_fig(yao_bud)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_BudUnit_fund_flow(graphics_bool):
    # ESTABLISH
    sue_bud = budunit_shop(owner_name="Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    cat_str = "cat status"
    cat_road = sue_bud.make_road(casa_road, cat_str)
    hun_n_str = "not hungry"
    hun_n_road = sue_bud.make_road(cat_road, hun_n_str)
    hun_y_str = "hungry"
    hun_y_road = sue_bud.make_road(cat_road, hun_y_str)
    clean_str = "cleaning"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    sweep_str = "sweep floor"
    sweep_road = sue_bud.make_road(clean_road, sweep_str)
    dish_str = "clean dishes"
    dish_road = sue_bud.make_road(clean_road, dish_str)
    sue_bud.add_item(casa_road, mass=30)
    sue_bud.add_item(cat_road, mass=30)
    sue_bud.add_item(hun_n_road, mass=30)
    sue_bud.add_item(hun_y_road, mass=30)
    sue_bud.add_item(clean_road, mass=30)
    sue_bud.add_item(sweep_road, mass=30, pledge=True)
    sue_bud.add_item(dish_road, mass=30, pledge=True)
    dinner_str = "cat have dinner"
    dinner_road = sue_bud.make_l1_road(dinner_str)
    sue_bud.add_item(dinner_road, mass=30, pledge=True)

    # WHEN / THEN
    fund_graph0(sue_bud, "Task", graphics_bool)
