from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.believer_graphics import (
    display_plantree,
    fund_graph0,
    get_believer_agenda_plotly_fig,
    get_believer_persons_plotly_fig,
)
from src.a06_believer_logic.test._util.example_believers import (
    believerunit_v001_with_large_agenda,
    get_believerunit_laundry_example1,
    get_believerunit_with_4_levels,
    get_believerunit_with_4_levels_and_2reasons,
    get_believerunit_x1_3levels_1reason_1facts,
)


def test_display_plantree_Scenario0(graphics_bool):
    # a_believer = get_1label_believer()
    # a_believer = get_2label_believer()
    # a_believer = get_3label_believer()
    # a_believer = get_5labelHG_believer()
    # a_believer = get_7labelJRoot_believer()
    a_believer = get_believerunit_with_4_levels()
    # a_believer = believerunit_v001()
    a_believer.settle_believer()
    print(f"Believer {a_believer.belief_label}: Labels ({len(a_believer._plan_dict)})")

    # WHEN / THEN
    x_fig = display_plantree(a_believer, graphics_bool)


def test_display_plantree_Scenario1_shows_Chores(graphics_bool):
    # a_believer = get_1label_believer()
    # a_believer = get_2label_believer()
    # a_believer = get_3label_believer()
    # a_believer = get_5labelHG_believer()
    # a_believer = get_7labelJRoot_believer()
    a_believer = get_believerunit_laundry_example1()
    # a_believer = believerunit_v001()
    a_believer.settle_believer()
    print(f"Believer {a_believer.belief_label}: Labels ({len(a_believer._plan_dict)})")

    # WHEN / THEN
    display_plantree(a_believer, mode="Chore", graphics_bool=graphics_bool)


def test_get_believer_persons_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    luca_believer = believerunit_shop()
    luca_believer.set_credor_respect(500)
    luca_believer.set_debtor_respect(400)
    yao_str = "Yao"
    yao_person_cred_points = 66
    yao_person_debt_points = 77
    luca_believer.add_personunit(
        yao_str, yao_person_cred_points, yao_person_debt_points
    )
    sue_str = "Sue"
    sue_person_cred_points = 434
    sue_person_debt_points = 323
    luca_believer.add_personunit(
        sue_str, sue_person_cred_points, sue_person_debt_points
    )

    # WHEN
    x_fig = get_believer_persons_plotly_fig(luca_believer)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_believer_agenda_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    yao_believer = believerunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_believer.make_l1_rope(wk_str)
    assert len(yao_believer.get_agenda_dict()) == 63

    # WHEN
    x_fig = get_believer_agenda_plotly_fig(yao_believer)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_BelieverUnit_fund_flow(graphics_bool):
    # ESTABLISH
    sue_believer = believerunit_shop(believer_name="Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_believer.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_n_rope = sue_believer.make_rope(cat_rope, hun_n_str)
    hun_y_str = "hungry"
    hun_y_rope = sue_believer.make_rope(cat_rope, hun_y_str)
    clean_str = "cleaning"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    sweep_rope = sue_believer.make_rope(clean_rope, sweep_str)
    dish_str = "clean dishes"
    dish_rope = sue_believer.make_rope(clean_rope, dish_str)
    sue_believer.add_plan(casa_rope, mass=30)
    sue_believer.add_plan(cat_rope, mass=30)
    sue_believer.add_plan(hun_n_rope, mass=30)
    sue_believer.add_plan(hun_y_rope, mass=30)
    sue_believer.add_plan(clean_rope, mass=30)
    sue_believer.add_plan(sweep_rope, mass=30, task=True)
    sue_believer.add_plan(dish_rope, mass=30, task=True)
    dinner_str = "cat have dinner"
    dinner_rope = sue_believer.make_l1_rope(dinner_str)
    sue_believer.add_plan(dinner_rope, mass=30, task=True)

    # WHEN / THEN
    fund_graph0(sue_believer, "Chore", graphics_bool)
