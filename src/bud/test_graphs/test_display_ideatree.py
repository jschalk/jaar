from src._instrument.python_tool import conditional_fig_show
from src.bud.examples.example_buds import (
    budunit_v001_with_large_agenda,
    get_budunit_with_4_levels,
    get_budunit_laundry_example1,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_x1_3levels_1reason_1facts,
)
from src.bud.bud import budunit_shop
from src.bud.graphic import (
    display_ideatree,
    get_bud_accts_plotly_fig,
    get_bud_agenda_plotly_fig,
)


def test_display_ideatree_Scenario0(graphics_bool):
    # a_bud = get_1node_bud()
    # a_bud = get_2node_bud()
    # a_bud = get_3node_bud()
    # a_bud = get_5nodeHG_bud()
    # a_bud = get_7nodeJRoot_bud()
    a_bud = get_budunit_with_4_levels()
    # a_bud = budunit_v001()
    a_bud.settle_bud()
    print(f"Bud {a_bud._pecun_id}: Nodes ({len(a_bud._idea_dict)})")

    # WHEN / THEN
    x_fig = display_ideatree(a_bud, graphics_bool)


def test_display_ideatree_Scenario1_shows_Tasks(graphics_bool):
    # a_bud = get_1node_bud()
    # a_bud = get_2node_bud()
    # a_bud = get_3node_bud()
    # a_bud = get_5nodeHG_bud()
    # a_bud = get_7nodeJRoot_bud()
    a_bud = get_budunit_laundry_example1()
    # a_bud = budunit_v001()
    a_bud.settle_bud()
    print(f"Bud {a_bud._pecun_id}: Nodes ({len(a_bud._idea_dict)})")

    # WHEN / THEN
    display_ideatree(a_bud, mode="Task", graphics_bool=graphics_bool)


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
