from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.owner_graphics import (
    display_concepttree,
    fund_graph0,
    get_owner_accts_plotly_fig,
    get_owner_agenda_plotly_fig,
)
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_laundry_example1,
    get_ownerunit_with_4_levels,
    get_ownerunit_with_4_levels_and_2reasons,
    get_ownerunit_x1_3levels_1reason_1facts,
    ownerunit_v001_with_large_agenda,
)


def test_display_concepttree_Scenario0(graphics_bool):
    # a_owner = get_1label_owner()
    # a_owner = get_2label_owner()
    # a_owner = get_3label_owner()
    # a_owner = get_5labelHG_owner()
    # a_owner = get_7labelJRoot_owner()
    a_owner = get_ownerunit_with_4_levels()
    # a_owner = ownerunit_v001()
    a_owner.settle_owner()
    print(f"Owner {a_owner.belief_label}: Labels ({len(a_owner._concept_dict)})")

    # WHEN / THEN
    x_fig = display_concepttree(a_owner, graphics_bool)


def test_display_concepttree_Scenario1_shows_Chores(graphics_bool):
    # a_owner = get_1label_owner()
    # a_owner = get_2label_owner()
    # a_owner = get_3label_owner()
    # a_owner = get_5labelHG_owner()
    # a_owner = get_7labelJRoot_owner()
    a_owner = get_ownerunit_laundry_example1()
    # a_owner = ownerunit_v001()
    a_owner.settle_owner()
    print(f"Owner {a_owner.belief_label}: Labels ({len(a_owner._concept_dict)})")

    # WHEN / THEN
    display_concepttree(a_owner, mode="Chore", graphics_bool=graphics_bool)


def test_get_owner_accts_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    luca_owner = ownerunit_shop()
    luca_owner.set_credor_respect(500)
    luca_owner.set_debtor_respect(400)
    yao_str = "Yao"
    yao_acct_cred_points = 66
    yao_acct_debt_points = 77
    luca_owner.add_acctunit(yao_str, yao_acct_cred_points, yao_acct_debt_points)
    sue_str = "Sue"
    sue_acct_cred_points = 434
    sue_acct_debt_points = 323
    luca_owner.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)

    # WHEN
    x_fig = get_owner_accts_plotly_fig(luca_owner)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_owner_agenda_plotly_fig_DisplaysCorrectInfo(graphics_bool):
    # ESTABLISH
    yao_owner = ownerunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_owner.make_l1_rope(wk_str)
    assert len(yao_owner.get_agenda_dict()) == 63

    # WHEN
    x_fig = get_owner_agenda_plotly_fig(yao_owner)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_OwnerUnit_fund_flow(graphics_bool):
    # ESTABLISH
    sue_owner = ownerunit_shop(owner_name="Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_owner.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_n_rope = sue_owner.make_rope(cat_rope, hun_n_str)
    hun_y_str = "hungry"
    hun_y_rope = sue_owner.make_rope(cat_rope, hun_y_str)
    clean_str = "cleaning"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    sweep_rope = sue_owner.make_rope(clean_rope, sweep_str)
    dish_str = "clean dishes"
    dish_rope = sue_owner.make_rope(clean_rope, dish_str)
    sue_owner.add_concept(casa_rope, mass=30)
    sue_owner.add_concept(cat_rope, mass=30)
    sue_owner.add_concept(hun_n_rope, mass=30)
    sue_owner.add_concept(hun_y_rope, mass=30)
    sue_owner.add_concept(clean_rope, mass=30)
    sue_owner.add_concept(sweep_rope, mass=30, task=True)
    sue_owner.add_concept(dish_rope, mass=30, task=True)
    dinner_str = "cat have dinner"
    dinner_rope = sue_owner.make_l1_rope(dinner_str)
    sue_owner.add_concept(dinner_rope, mass=30, task=True)

    # WHEN / THEN
    fund_graph0(sue_owner, "Chore", graphics_bool)
