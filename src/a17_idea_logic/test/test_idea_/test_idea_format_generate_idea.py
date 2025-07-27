from src.a01_term_logic.rope import to_rope
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_planunit_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    mass_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    plan_rope_str,
    task_str,
)
from src.a06_believer_logic.test._util.example_believers import believerunit_v001
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import INSERT_str
from src.a17_idea_logic.idea_config import (
    idea_format_00013_planunit_v0_0_0,
    idea_format_00020_believer_partner_membership_v0_0_0,
    idea_format_00021_believer_partnerunit_v0_0_0,
)
from src.a17_idea_logic.idea_main import (
    create_idea_df,
    get_idearef_obj,
    make_believerdelta,
)


def test_make_believerdelta_Arg_idea_format_00021_believer_partnerunit_v0_0_0():
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
    amy_belief_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_belief_label)
    sue_believerunit.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        yao_str, yao_partner_cred_points, yao_partner_debt_points
    )
    x_idea_name = idea_format_00021_believer_partnerunit_v0_0_0()
    partner_dataframe = create_idea_df(sue_believerunit, x_idea_name)
    print(f"{partner_dataframe.columns=}")
    partner_csv = partner_dataframe.to_csv(index=False)

    # WHEN
    sue_partner_believerdelta = make_believerdelta(partner_csv)

    # THEN
    assert sue_partner_believerdelta
    sue_believeratom = believeratom_shop(believer_partnerunit_str(), INSERT_str())
    sue_believeratom.set_arg(partner_name_str(), sue_str)
    sue_believeratom.set_arg(partner_cred_points_str(), sue_partner_cred_points)
    sue_believeratom.set_arg(partner_debt_points_str(), sue_partner_debt_points)
    sue_believeratom.set_atom_order()
    bob_believeratom = believeratom_shop(believer_partnerunit_str(), INSERT_str())
    bob_believeratom.set_arg(partner_name_str(), bob_str)
    bob_believeratom.set_arg(partner_cred_points_str(), bob_partner_cred_points)
    bob_believeratom.set_arg(partner_debt_points_str(), bob_partner_debt_points)
    bob_believeratom.set_atom_order()
    # print(f"{sue_partner_believerdelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_partner_believerdelta.believeratoms.get(INSERT_str()).get(believer_partnerunit_str()).get(sue_str)=}"
    # )
    print(f"{sue_believeratom=}")
    assert sue_partner_believerdelta.believeratom_exists(sue_believeratom)
    assert sue_partner_believerdelta.believeratom_exists(bob_believeratom)
    assert len(sue_partner_believerdelta.get_ordered_believeratoms()) == 3


# def test_make_believerdelta_Arg_idea_format_00020_believer_partner_membership_v0_0_0():
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     amy_belief_label = "amy56"
#     sue_believerunit = believerunit_shop(sue_str, amy_belief_label)
#     sue_believerunit.add_partnerunit(sue_str)
#     sue_believerunit.add_partnerunit(bob_str)
#     sue_believerunit.add_partnerunit(yao_str)
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
#     sue_partnerunit = sue_believerunit.get_partner(sue_str)
#     bob_partnerunit = sue_believerunit.get_partner(bob_str)
#     yao_partnerunit = sue_believerunit.get_partner(yao_str)
#     sue_partnerunit.add_membership(iowa_str, sue_iowa_group_cred_points, sue_iowa_group_debt_points)
#     bob_partnerunit.add_membership(iowa_str, bob_iowa_group_cred_points, bob_iowa_group_debt_points)
#     yao_partnerunit.add_membership(iowa_str, yao_iowa_group_cred_points, yao_iowa_group_debt_points)
#     yao_partnerunit.add_membership(ohio_str, yao_ohio_group_cred_points, yao_ohio_group_debt_points)
#     x_idea_name = idea_format_00020_believer_partner_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_believerunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_believerdelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_believeratom = believeratom_shop(believer_partner_membership_str(), INSERT_str())
#     bob_iowa_believeratom = believeratom_shop(believer_partner_membership_str(), INSERT_str())
#     yao_iowa_believeratom = believeratom_shop(believer_partner_membership_str(), INSERT_str())
#     yao_ohio_believeratom = believeratom_shop(believer_partner_membership_str(), INSERT_str())
#     sue_iowa_believeratom.set_arg(group_title_str(), iowa_str)
#     bob_iowa_believeratom.set_arg(group_title_str(), iowa_str)
#     yao_iowa_believeratom.set_arg(group_title_str(), iowa_str)
#     yao_ohio_believeratom.set_arg(group_title_str(), ohio_str)
#     sue_iowa_believeratom.set_arg(partner_name_str(), sue_str)
#     bob_iowa_believeratom.set_arg(partner_name_str(), bob_str)
#     yao_iowa_believeratom.set_arg(partner_name_str(), yao_str)
#     yao_ohio_believeratom.set_arg(partner_name_str(), yao_str)
#     sue_iowa_believeratom.set_arg(group_cred_points_str(), sue_iowa_group_cred_points)
#     bob_iowa_believeratom.set_arg(group_cred_points_str(), bob_iowa_group_cred_points)
#     yao_iowa_believeratom.set_arg(group_cred_points_str(), yao_iowa_group_cred_points)
#     yao_ohio_believeratom.set_arg(group_cred_points_str(), yao_ohio_group_cred_points)
#     sue_iowa_believeratom.set_arg(group_debt_points_str(), sue_iowa_group_debt_points)
#     bob_iowa_believeratom.set_arg(group_debt_points_str(), bob_iowa_group_debt_points)
#     yao_iowa_believeratom.set_arg(group_debt_points_str(), yao_iowa_group_debt_points)
#     yao_ohio_believeratom.set_arg(group_debt_points_str(), yao_ohio_group_debt_points)
#     bob_iowa_believeratom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_believeratoms()[2]=}")
#     # print(f"{sue_iowa_believeratom=}")
#     assert len(membership_changunit.get_ordered_believeratoms()) == 10
#     assert membership_changunit.get_ordered_believeratoms()[0] == bob_iowa_believeratom
#     assert membership_changunit.believeratom_exists(sue_iowa_believeratom)
#     assert membership_changunit.believeratom_exists(bob_iowa_believeratom)
#     assert membership_changunit.believeratom_exists(yao_iowa_believeratom)
#     assert membership_changunit.believeratom_exists(yao_ohio_believeratom)
#     assert len(membership_changunit.get_ordered_believeratoms()) == 10


def test_make_believerdelta_Arg_idea_format_00013_planunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    amy_belief_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_belief_label)
    casa_str = "casa"
    casa_rope = sue_believerunit.make_l1_rope(casa_str)
    casa_mass = 31
    sue_believerunit.set_l1_plan(planunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_rope = sue_believerunit.make_rope(casa_rope, clean_str)
    sue_believerunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    x_idea_name = idea_format_00013_planunit_v0_0_0()
    planunit_dataframe = create_idea_df(sue_believerunit, x_idea_name)
    planunit_csv = planunit_dataframe.to_csv(index=False)

    # WHEN
    planunit_changunit = make_believerdelta(planunit_csv)

    # THEN
    casa_believeratom = believeratom_shop(believer_planunit_str(), INSERT_str())
    casa_believeratom.set_arg(plan_rope_str(), casa_rope)
    casa_believeratom.set_arg(task_str(), False)
    casa_believeratom.set_arg(mass_str(), casa_mass)
    print(f"{casa_believeratom=}")
    assert casa_believeratom.get_value(mass_str()) == casa_mass
    clean_believeratom = believeratom_shop(believer_planunit_str(), INSERT_str())
    clean_believeratom.set_arg(plan_rope_str(), clean_rope)
    clean_believeratom.set_arg(task_str(), True)
    clean_believeratom.set_arg(mass_str(), 1)
    assert planunit_changunit.believeratom_exists(casa_believeratom)
    assert planunit_changunit.believeratom_exists(clean_believeratom)
    assert len(planunit_changunit.get_ordered_believeratoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_planunit_v0_0_0_Scenario_believerunit_v001(
    run_big_tests,
):
    # sourcery skip: no-conditionals-in-tests
    if run_big_tests:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_planunit_v0_0_0()

        # WHEN
        planunit_format = create_idea_df(believerunit_v001(), x_idea_name)

        # THEN
        array_headers = list(planunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(planunit_format) == 251
