from src.a01_term_logic.rope import to_rope
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    concept_rope_str,
    credit_score_str,
    credit_vote_str,
    debt_score_str,
    debt_vote_str,
    group_title_str,
    mass_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_conceptunit_str,
    task_str,
)
from src.a06_plan_logic._test_util.example_plans import planunit_v001
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._test_util.a08_str import INSERT_str
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a17_idea_logic.idea import create_idea_df, get_idearef_obj, make_plandelta
from src.a17_idea_logic.idea_config import (
    idea_format_00013_conceptunit_v0_0_0,
    idea_format_00020_plan_acct_membership_v0_0_0,
    idea_format_00021_plan_acctunit_v0_0_0,
)


def test_make_plandelta_Arg_idea_format_00021_plan_acctunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_score = 11
    bob_credit_score = 13
    yao_credit_score = 41
    sue_debt_score = 23
    bob_debt_score = 29
    yao_debt_score = 37
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    sue_planunit.add_acctunit(sue_str, sue_credit_score, sue_debt_score)
    sue_planunit.add_acctunit(bob_str, bob_credit_score, bob_debt_score)
    sue_planunit.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    x_idea_name = idea_format_00021_plan_acctunit_v0_0_0()
    acct_dataframe = create_idea_df(sue_planunit, x_idea_name)
    print(f"{acct_dataframe.columns=}")
    acct_csv = acct_dataframe.to_csv(index=False)

    # WHEN
    sue_acct_plandelta = make_plandelta(acct_csv)

    # THEN
    assert sue_acct_plandelta
    sue_planatom = planatom_shop(plan_acctunit_str(), INSERT_str())
    sue_planatom.set_arg(acct_name_str(), sue_str)
    sue_planatom.set_arg(credit_score_str(), sue_credit_score)
    sue_planatom.set_arg(debt_score_str(), sue_debt_score)
    sue_planatom.set_atom_order()
    bob_planatom = planatom_shop(plan_acctunit_str(), INSERT_str())
    bob_planatom.set_arg(acct_name_str(), bob_str)
    bob_planatom.set_arg(credit_score_str(), bob_credit_score)
    bob_planatom.set_arg(debt_score_str(), bob_debt_score)
    bob_planatom.set_atom_order()
    # print(f"{sue_acct_plandelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_acct_plandelta.planatoms.get(INSERT_str()).get(plan_acctunit_str()).get(sue_str)=}"
    # )
    print(f"{sue_planatom=}")
    assert sue_acct_plandelta.planatom_exists(sue_planatom)
    assert sue_acct_plandelta.planatom_exists(bob_planatom)
    assert len(sue_acct_plandelta.get_ordered_planatoms()) == 3


# def test_make_plandelta_Arg_idea_format_00020_plan_acct_membership_v0_0_0():
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     accord_vow_label = "accord56"
#     sue_planunit = planunit_shop(sue_str, accord_vow_label)
#     sue_planunit.add_acctunit(sue_str)
#     sue_planunit.add_acctunit(bob_str)
#     sue_planunit.add_acctunit(yao_str)
#     iowa_str = ";Iowa"
#     sue_iowa_credit_vote = 37
#     bob_iowa_credit_vote = 43
#     yao_iowa_credit_vote = 51
#     sue_iowa_debt_vote = 57
#     bob_iowa_debt_vote = 61
#     yao_iowa_debt_vote = 67
#     ohio_str = ";Ohio"
#     yao_ohio_credit_vote = 73
#     yao_ohio_debt_vote = 67
#     sue_acctunit = sue_planunit.get_acct(sue_str)
#     bob_acctunit = sue_planunit.get_acct(bob_str)
#     yao_acctunit = sue_planunit.get_acct(yao_str)
#     sue_acctunit.add_membership(iowa_str, sue_iowa_credit_vote, sue_iowa_debt_vote)
#     bob_acctunit.add_membership(iowa_str, bob_iowa_credit_vote, bob_iowa_debt_vote)
#     yao_acctunit.add_membership(iowa_str, yao_iowa_credit_vote, yao_iowa_debt_vote)
#     yao_acctunit.add_membership(ohio_str, yao_ohio_credit_vote, yao_ohio_debt_vote)
#     x_idea_name = idea_format_00020_plan_acct_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_planunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_plandelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_planatom = planatom_shop(plan_acct_membership_str(), INSERT_str())
#     bob_iowa_planatom = planatom_shop(plan_acct_membership_str(), INSERT_str())
#     yao_iowa_planatom = planatom_shop(plan_acct_membership_str(), INSERT_str())
#     yao_ohio_planatom = planatom_shop(plan_acct_membership_str(), INSERT_str())
#     sue_iowa_planatom.set_arg(group_title_str(), iowa_str)
#     bob_iowa_planatom.set_arg(group_title_str(), iowa_str)
#     yao_iowa_planatom.set_arg(group_title_str(), iowa_str)
#     yao_ohio_planatom.set_arg(group_title_str(), ohio_str)
#     sue_iowa_planatom.set_arg(acct_name_str(), sue_str)
#     bob_iowa_planatom.set_arg(acct_name_str(), bob_str)
#     yao_iowa_planatom.set_arg(acct_name_str(), yao_str)
#     yao_ohio_planatom.set_arg(acct_name_str(), yao_str)
#     sue_iowa_planatom.set_arg(credit_vote_str(), sue_iowa_credit_vote)
#     bob_iowa_planatom.set_arg(credit_vote_str(), bob_iowa_credit_vote)
#     yao_iowa_planatom.set_arg(credit_vote_str(), yao_iowa_credit_vote)
#     yao_ohio_planatom.set_arg(credit_vote_str(), yao_ohio_credit_vote)
#     sue_iowa_planatom.set_arg(debt_vote_str(), sue_iowa_debt_vote)
#     bob_iowa_planatom.set_arg(debt_vote_str(), bob_iowa_debt_vote)
#     yao_iowa_planatom.set_arg(debt_vote_str(), yao_iowa_debt_vote)
#     yao_ohio_planatom.set_arg(debt_vote_str(), yao_ohio_debt_vote)
#     bob_iowa_planatom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_planatoms()[2]=}")
#     # print(f"{sue_iowa_planatom=}")
#     assert len(membership_changunit.get_ordered_planatoms()) == 10
#     assert membership_changunit.get_ordered_planatoms()[0] == bob_iowa_planatom
#     assert membership_changunit.planatom_exists(sue_iowa_planatom)
#     assert membership_changunit.planatom_exists(bob_iowa_planatom)
#     assert membership_changunit.planatom_exists(yao_iowa_planatom)
#     assert membership_changunit.planatom_exists(yao_ohio_planatom)
#     assert len(membership_changunit.get_ordered_planatoms()) == 10


def test_make_plandelta_Arg_idea_format_00013_conceptunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    casa_mass = 31
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    x_idea_name = idea_format_00013_conceptunit_v0_0_0()
    conceptunit_dataframe = create_idea_df(sue_planunit, x_idea_name)
    conceptunit_csv = conceptunit_dataframe.to_csv(index=False)

    # WHEN
    conceptunit_changunit = make_plandelta(conceptunit_csv)

    # THEN
    casa_planatom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    casa_planatom.set_arg(concept_rope_str(), casa_rope)
    casa_planatom.set_arg(task_str(), False)
    casa_planatom.set_arg(mass_str(), casa_mass)
    print(f"{casa_planatom=}")
    assert casa_planatom.get_value(mass_str()) == casa_mass
    clean_planatom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    clean_planatom.set_arg(concept_rope_str(), clean_rope)
    clean_planatom.set_arg(task_str(), True)
    clean_planatom.set_arg(mass_str(), 1)
    assert conceptunit_changunit.planatom_exists(casa_planatom)
    assert conceptunit_changunit.planatom_exists(clean_planatom)
    assert len(conceptunit_changunit.get_ordered_planatoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_conceptunit_v0_0_0_Scenario_planunit_v001(
    big_volume,
):
    # sourcery skip: no-conditionals-in-tests
    if big_volume:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_conceptunit_v0_0_0()

        # WHEN
        conceptunit_format = create_idea_df(planunit_v001(), x_idea_name)

        # THEN
        array_headers = list(conceptunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(conceptunit_format) == 251


def test_make_plandelta_Arg_idea_format_00013_conceptunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    casa_mass = 31
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    x_idea_name = idea_format_00013_conceptunit_v0_0_0()
    conceptunit_dataframe = create_idea_df(sue_planunit, x_idea_name)
    conceptunit_csv = conceptunit_dataframe.to_csv(index=False)

    # WHEN
    conceptunit_changunit = make_plandelta(conceptunit_csv)

    # THEN
    casa_planatom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    casa_planatom.set_arg(concept_rope_str(), casa_rope)
    casa_planatom.set_arg(task_str(), False)
    casa_planatom.set_arg(mass_str(), casa_mass)
    print(f"{casa_planatom=}")
    assert casa_planatom.get_value(mass_str()) == casa_mass
    clean_planatom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    clean_planatom.set_arg(concept_rope_str(), clean_rope)
    clean_planatom.set_arg(task_str(), True)
    clean_planatom.set_arg(mass_str(), 1)
    assert conceptunit_changunit.planatom_exists(casa_planatom)
    assert conceptunit_changunit.planatom_exists(clean_planatom)
    assert len(conceptunit_changunit.get_ordered_planatoms()) == 2
