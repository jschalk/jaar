from src.a01_term_logic.rope import to_rope
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    belief_partner_membership_str,
    belief_partnerunit_str,
    belief_planunit_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    plan_rope_str,
    star_str,
    task_str,
)
from src.a06_belief_logic.test._util.example_beliefs import beliefunit_v001
from src.a08_belief_atom_logic.atom_main import beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import INSERT_str
from src.a17_idea_logic.idea_config import (
    idea_format_00013_planunit_v0_0_0,
    idea_format_00020_belief_partner_membership_v0_0_0,
    idea_format_00021_belief_partnerunit_v0_0_0,
)
from src.a17_idea_logic.idea_main import (
    create_idea_df,
    get_idearef_obj,
    make_beliefdelta,
)


def test_make_beliefdelta_Arg_idea_format_00021_belief_partnerunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_partner_cred_points = 11
    bob_partner_cred_points = 13
    yao_partner_cred_points = 41
    sue_partner_debt_points = 23
    bob_partner_debt_points = 29
    yao_partner_debt_points = 37
    amy_coin_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_coin_label)
    sue_beliefunit.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    sue_beliefunit.add_partnerunit(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    sue_beliefunit.add_partnerunit(
        yao_str, yao_partner_cred_points, yao_partner_debt_points
    )
    x_idea_name = idea_format_00021_belief_partnerunit_v0_0_0()
    partner_dataframe = create_idea_df(sue_beliefunit, x_idea_name)
    print(f"{partner_dataframe.columns=}")
    partner_csv = partner_dataframe.to_csv(index=False)

    # WHEN
    sue_partner_beliefdelta = make_beliefdelta(partner_csv)

    # THEN
    assert sue_partner_beliefdelta
    sue_beliefatom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    sue_beliefatom.set_arg(partner_name_str(), sue_str)
    sue_beliefatom.set_arg(partner_cred_points_str(), sue_partner_cred_points)
    sue_beliefatom.set_arg(partner_debt_points_str(), sue_partner_debt_points)
    sue_beliefatom.set_atom_order()
    bob_beliefatom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    bob_beliefatom.set_arg(partner_name_str(), bob_str)
    bob_beliefatom.set_arg(partner_cred_points_str(), bob_partner_cred_points)
    bob_beliefatom.set_arg(partner_debt_points_str(), bob_partner_debt_points)
    bob_beliefatom.set_atom_order()
    # print(f"{sue_partner_beliefdelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_partner_beliefdelta.beliefatoms.get(INSERT_str()).get(belief_partnerunit_str()).get(sue_str)=}"
    # )
    print(f"{sue_beliefatom=}")
    assert sue_partner_beliefdelta.beliefatom_exists(sue_beliefatom)
    assert sue_partner_beliefdelta.beliefatom_exists(bob_beliefatom)
    assert len(sue_partner_beliefdelta.get_ordered_beliefatoms()) == 3


# def test_make_beliefdelta_Arg_idea_format_00020_belief_partner_membership_v0_0_0():
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     amy_coin_label = "amy56"
#     sue_beliefunit = beliefunit_shop(sue_str, amy_coin_label)
#     sue_beliefunit.add_partnerunit(sue_str)
#     sue_beliefunit.add_partnerunit(bob_str)
#     sue_beliefunit.add_partnerunit(yao_str)
#     iowa_str = ";Iowa"
#     sue_iowa_group_cred_points = 37
#     bob_iowa_group_cred_points = 43
#     yao_iowa_group_cred_points = 51
#     sue_iowa_group_debt_points = 57
#     bob_iowa_group_debt_points = 61
#     yao_iowa_group_debt_points = 67
#     ohio_str = ";Ohio"
#     yao_ohio_group_cred_points = 73
#     yao_ohio_group_debt_points = 67
#     sue_partnerunit = sue_beliefunit.get_partner(sue_str)
#     bob_partnerunit = sue_beliefunit.get_partner(bob_str)
#     yao_partnerunit = sue_beliefunit.get_partner(yao_str)
#     sue_partnerunit.add_membership(iowa_str, sue_iowa_group_cred_points, sue_iowa_group_debt_points)
#     bob_partnerunit.add_membership(iowa_str, bob_iowa_group_cred_points, bob_iowa_group_debt_points)
#     yao_partnerunit.add_membership(iowa_str, yao_iowa_group_cred_points, yao_iowa_group_debt_points)
#     yao_partnerunit.add_membership(ohio_str, yao_ohio_group_cred_points, yao_ohio_group_debt_points)
#     x_idea_name = idea_format_00020_belief_partner_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_beliefunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_beliefdelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_beliefatom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
#     bob_iowa_beliefatom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
#     yao_iowa_beliefatom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
#     yao_ohio_beliefatom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
#     sue_iowa_beliefatom.set_arg(group_title_str(), iowa_str)
#     bob_iowa_beliefatom.set_arg(group_title_str(), iowa_str)
#     yao_iowa_beliefatom.set_arg(group_title_str(), iowa_str)
#     yao_ohio_beliefatom.set_arg(group_title_str(), ohio_str)
#     sue_iowa_beliefatom.set_arg(partner_name_str(), sue_str)
#     bob_iowa_beliefatom.set_arg(partner_name_str(), bob_str)
#     yao_iowa_beliefatom.set_arg(partner_name_str(), yao_str)
#     yao_ohio_beliefatom.set_arg(partner_name_str(), yao_str)
#     sue_iowa_beliefatom.set_arg(group_cred_points_str(), sue_iowa_group_cred_points)
#     bob_iowa_beliefatom.set_arg(group_cred_points_str(), bob_iowa_group_cred_points)
#     yao_iowa_beliefatom.set_arg(group_cred_points_str(), yao_iowa_group_cred_points)
#     yao_ohio_beliefatom.set_arg(group_cred_points_str(), yao_ohio_group_cred_points)
#     sue_iowa_beliefatom.set_arg(group_debt_points_str(), sue_iowa_group_debt_points)
#     bob_iowa_beliefatom.set_arg(group_debt_points_str(), bob_iowa_group_debt_points)
#     yao_iowa_beliefatom.set_arg(group_debt_points_str(), yao_iowa_group_debt_points)
#     yao_ohio_beliefatom.set_arg(group_debt_points_str(), yao_ohio_group_debt_points)
#     bob_iowa_beliefatom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_beliefatoms()[2]=}")
#     # print(f"{sue_iowa_beliefatom=}")
#     assert len(membership_changunit.get_ordered_beliefatoms()) == 10
#     assert membership_changunit.get_ordered_beliefatoms()[0] == bob_iowa_beliefatom
#     assert membership_changunit.beliefatom_exists(sue_iowa_beliefatom)
#     assert membership_changunit.beliefatom_exists(bob_iowa_beliefatom)
#     assert membership_changunit.beliefatom_exists(yao_iowa_beliefatom)
#     assert membership_changunit.beliefatom_exists(yao_ohio_beliefatom)
#     assert len(membership_changunit.get_ordered_beliefatoms()) == 10


def test_make_beliefdelta_Arg_idea_format_00013_planunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    amy_coin_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_coin_label)
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    casa_star = 31
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str, star=casa_star))
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    x_idea_name = idea_format_00013_planunit_v0_0_0()
    planunit_dataframe = create_idea_df(sue_beliefunit, x_idea_name)
    planunit_csv = planunit_dataframe.to_csv(index=False)

    # WHEN
    planunit_changunit = make_beliefdelta(planunit_csv)

    # THEN
    casa_beliefatom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    casa_beliefatom.set_arg(plan_rope_str(), casa_rope)
    casa_beliefatom.set_arg(task_str(), False)
    casa_beliefatom.set_arg(star_str(), casa_star)
    print(f"{casa_beliefatom=}")
    assert casa_beliefatom.get_value(star_str()) == casa_star
    clean_beliefatom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    clean_beliefatom.set_arg(plan_rope_str(), clean_rope)
    clean_beliefatom.set_arg(task_str(), True)
    clean_beliefatom.set_arg(star_str(), 1)
    assert planunit_changunit.beliefatom_exists(casa_beliefatom)
    assert planunit_changunit.beliefatom_exists(clean_beliefatom)
    assert len(planunit_changunit.get_ordered_beliefatoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_planunit_v0_0_0_Scenario_beliefunit_v001(
    run_big_tests,
):
    # sourcery skip: no-conditionals-in-tests
    if run_big_tests:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_planunit_v0_0_0()

        # WHEN
        planunit_format = create_idea_df(beliefunit_v001(), x_idea_name)

        # THEN
        array_headers = list(planunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(planunit_format) == 251
