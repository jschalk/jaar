from src.ch01_data_toolbox.plotly_toolbox import conditional_fig_show
from src.ch07_belief_logic.belief_graphics import (
    display_plantree,
    fund_graph0,
    get_belief_agenda_plotly_fig,
    get_belief_voices_plotly_fig,
)
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import (
    beliefunit_v001_with_large_agenda,
    get_beliefunit_laundry_example1,
    get_beliefunit_with_4_levels,
    get_beliefunit_with_4_levels_and_2reasons,
    get_beliefunit_x1_3levels_1reason_1facts,
)


def test_display_plantree_Scenario0(graphics_bool):
    # ESTABLISH
    # a_belief = get_1label_belief()
    # a_belief = get_2label_belief()
    # a_belief = get_3label_belief()
    # a_belief = get_5labelHG_belief()
    # a_belief = get_7labelJroot_belief()
    a_belief = get_beliefunit_with_4_levels()
    # a_belief = beliefunit_v001()
    a_belief.cashout()
    print(f"Belief {a_belief.moment_label}: Labels ({len(a_belief._plan_dict)})")

    # WHEN / THEN
    x_fig = display_plantree(a_belief, graphics_bool)


def test_display_plantree_Scenario1_shows_Chores(graphics_bool):
    # ESTABLISH
    # a_belief = get_1label_belief()
    # a_belief = get_2label_belief()
    # a_belief = get_3label_belief()
    # a_belief = get_5labelHG_belief()
    # a_belief = get_7labelJroot_belief()
    a_belief = get_beliefunit_laundry_example1()
    # a_belief = beliefunit_v001()
    a_belief.cashout()
    print(f"Belief {a_belief.moment_label}: Labels ({len(a_belief._plan_dict)})")

    # WHEN / THEN
    display_plantree(a_belief, mode="Chore", graphics_bool=graphics_bool)


def test_get_belief_voices_plotly_fig_DisplaysInfo(graphics_bool):
    # ESTABLISH
    luca_belief = beliefunit_shop()
    luca_belief.set_credor_respect(500)
    luca_belief.set_debtor_respect(400)
    yao_str = "Yao"
    yao_voice_cred_points = 66
    yao_voice_debt_points = 77
    luca_belief.add_voiceunit(yao_str, yao_voice_cred_points, yao_voice_debt_points)
    sue_str = "Sue"
    sue_voice_cred_points = 434
    sue_voice_debt_points = 323
    luca_belief.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)

    # WHEN
    x_fig = get_belief_voices_plotly_fig(luca_belief)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_belief_agenda_plotly_fig_DisplaysInfo(graphics_bool):
    # ESTABLISH
    yao_belief = beliefunit_v001_with_large_agenda()
    assert len(yao_belief.get_agenda_dict()) == 63

    # WHEN
    x_fig = get_belief_agenda_plotly_fig(yao_belief)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_BeliefUnit_fund_flow(graphics_bool):
    # ESTABLISH
    sue_belief = beliefunit_shop(belief_name="Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_belief.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_n_rope = sue_belief.make_rope(cat_rope, hun_n_str)
    hun_y_str = "hungry"
    hun_y_rope = sue_belief.make_rope(cat_rope, hun_y_str)
    clean_str = "cleaning"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    sweep_rope = sue_belief.make_rope(clean_rope, sweep_str)
    dish_str = "clean dishes"
    dish_rope = sue_belief.make_rope(clean_rope, dish_str)
    sue_belief.add_plan(casa_rope, star=30)
    sue_belief.add_plan(cat_rope, star=30)
    sue_belief.add_plan(hun_n_rope, star=30)
    sue_belief.add_plan(hun_y_rope, star=30)
    sue_belief.add_plan(clean_rope, star=30)
    sue_belief.add_plan(sweep_rope, star=30, pledge=True)
    sue_belief.add_plan(dish_rope, star=30, pledge=True)
    dinner_str = "cat have dinner"
    dinner_rope = sue_belief.make_l1_rope(dinner_str)
    sue_belief.add_plan(dinner_rope, star=30, pledge=True)

    # WHEN / THEN
    fund_graph0(sue_belief, "Chore", graphics_bool)
