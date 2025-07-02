from src.a01_term_logic.rope import to_rope
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    concept_rope_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    mass_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_conceptunit_str,
    task_str,
)
from src.a06_owner_logic.test._util.example_owners import ownerunit_v001
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import INSERT_str
from src.a17_idea_logic.idea import create_idea_df, get_idearef_obj, make_ownerdelta
from src.a17_idea_logic.idea_config import (
    idea_format_00013_conceptunit_v0_0_0,
    idea_format_00020_owner_acct_membership_v0_0_0,
    idea_format_00021_owner_acctunit_v0_0_0,
)


def test_make_ownerdelta_Arg_idea_format_00021_owner_acctunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_acct_cred_points = 11
    bob_acct_cred_points = 13
    yao_acct_cred_points = 41
    sue_acct_debt_points = 23
    bob_acct_debt_points = 29
    yao_acct_debt_points = 37
    amy_belief_label = "amy56"
    sue_ownerunit = ownerunit_shop(sue_str, amy_belief_label)
    sue_ownerunit.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    sue_ownerunit.add_acctunit(bob_str, bob_acct_cred_points, bob_acct_debt_points)
    sue_ownerunit.add_acctunit(yao_str, yao_acct_cred_points, yao_acct_debt_points)
    x_idea_name = idea_format_00021_owner_acctunit_v0_0_0()
    acct_dataframe = create_idea_df(sue_ownerunit, x_idea_name)
    print(f"{acct_dataframe.columns=}")
    acct_csv = acct_dataframe.to_csv(index=False)

    # WHEN
    sue_acct_ownerdelta = make_ownerdelta(acct_csv)

    # THEN
    assert sue_acct_ownerdelta
    sue_owneratom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    sue_owneratom.set_arg(acct_name_str(), sue_str)
    sue_owneratom.set_arg(acct_cred_points_str(), sue_acct_cred_points)
    sue_owneratom.set_arg(acct_debt_points_str(), sue_acct_debt_points)
    sue_owneratom.set_atom_order()
    bob_owneratom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    bob_owneratom.set_arg(acct_name_str(), bob_str)
    bob_owneratom.set_arg(acct_cred_points_str(), bob_acct_cred_points)
    bob_owneratom.set_arg(acct_debt_points_str(), bob_acct_debt_points)
    bob_owneratom.set_atom_order()
    # print(f"{sue_acct_ownerdelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_acct_ownerdelta.owneratoms.get(INSERT_str()).get(owner_acctunit_str()).get(sue_str)=}"
    # )
    print(f"{sue_owneratom=}")
    assert sue_acct_ownerdelta.owneratom_exists(sue_owneratom)
    assert sue_acct_ownerdelta.owneratom_exists(bob_owneratom)
    assert len(sue_acct_ownerdelta.get_ordered_owneratoms()) == 3


# def test_make_ownerdelta_Arg_idea_format_00020_owner_acct_membership_v0_0_0():
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     amy_belief_label = "amy56"
#     sue_ownerunit = ownerunit_shop(sue_str, amy_belief_label)
#     sue_ownerunit.add_acctunit(sue_str)
#     sue_ownerunit.add_acctunit(bob_str)
#     sue_ownerunit.add_acctunit(yao_str)
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
#     sue_acctunit = sue_ownerunit.get_acct(sue_str)
#     bob_acctunit = sue_ownerunit.get_acct(bob_str)
#     yao_acctunit = sue_ownerunit.get_acct(yao_str)
#     sue_acctunit.add_membership(iowa_str, sue_iowa_group_cred_points, sue_iowa_group_debt_points)
#     bob_acctunit.add_membership(iowa_str, bob_iowa_group_cred_points, bob_iowa_group_debt_points)
#     yao_acctunit.add_membership(iowa_str, yao_iowa_group_cred_points, yao_iowa_group_debt_points)
#     yao_acctunit.add_membership(ohio_str, yao_ohio_group_cred_points, yao_ohio_group_debt_points)
#     x_idea_name = idea_format_00020_owner_acct_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_ownerunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_ownerdelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_owneratom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
#     bob_iowa_owneratom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
#     yao_iowa_owneratom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
#     yao_ohio_owneratom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
#     sue_iowa_owneratom.set_arg(group_title_str(), iowa_str)
#     bob_iowa_owneratom.set_arg(group_title_str(), iowa_str)
#     yao_iowa_owneratom.set_arg(group_title_str(), iowa_str)
#     yao_ohio_owneratom.set_arg(group_title_str(), ohio_str)
#     sue_iowa_owneratom.set_arg(acct_name_str(), sue_str)
#     bob_iowa_owneratom.set_arg(acct_name_str(), bob_str)
#     yao_iowa_owneratom.set_arg(acct_name_str(), yao_str)
#     yao_ohio_owneratom.set_arg(acct_name_str(), yao_str)
#     sue_iowa_owneratom.set_arg(group_cred_points_str(), sue_iowa_group_cred_points)
#     bob_iowa_owneratom.set_arg(group_cred_points_str(), bob_iowa_group_cred_points)
#     yao_iowa_owneratom.set_arg(group_cred_points_str(), yao_iowa_group_cred_points)
#     yao_ohio_owneratom.set_arg(group_cred_points_str(), yao_ohio_group_cred_points)
#     sue_iowa_owneratom.set_arg(group_debt_points_str(), sue_iowa_group_debt_points)
#     bob_iowa_owneratom.set_arg(group_debt_points_str(), bob_iowa_group_debt_points)
#     yao_iowa_owneratom.set_arg(group_debt_points_str(), yao_iowa_group_debt_points)
#     yao_ohio_owneratom.set_arg(group_debt_points_str(), yao_ohio_group_debt_points)
#     bob_iowa_owneratom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_owneratoms()[2]=}")
#     # print(f"{sue_iowa_owneratom=}")
#     assert len(membership_changunit.get_ordered_owneratoms()) == 10
#     assert membership_changunit.get_ordered_owneratoms()[0] == bob_iowa_owneratom
#     assert membership_changunit.owneratom_exists(sue_iowa_owneratom)
#     assert membership_changunit.owneratom_exists(bob_iowa_owneratom)
#     assert membership_changunit.owneratom_exists(yao_iowa_owneratom)
#     assert membership_changunit.owneratom_exists(yao_ohio_owneratom)
#     assert len(membership_changunit.get_ordered_owneratoms()) == 10


def test_make_ownerdelta_Arg_idea_format_00013_conceptunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    amy_belief_label = "amy56"
    sue_ownerunit = ownerunit_shop(sue_str, amy_belief_label)
    casa_str = "casa"
    casa_rope = sue_ownerunit.make_l1_rope(casa_str)
    casa_mass = 31
    sue_ownerunit.set_l1_concept(conceptunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_rope = sue_ownerunit.make_rope(casa_rope, clean_str)
    sue_ownerunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    x_idea_name = idea_format_00013_conceptunit_v0_0_0()
    conceptunit_dataframe = create_idea_df(sue_ownerunit, x_idea_name)
    conceptunit_csv = conceptunit_dataframe.to_csv(index=False)

    # WHEN
    conceptunit_changunit = make_ownerdelta(conceptunit_csv)

    # THEN
    casa_owneratom = owneratom_shop(owner_conceptunit_str(), INSERT_str())
    casa_owneratom.set_arg(concept_rope_str(), casa_rope)
    casa_owneratom.set_arg(task_str(), False)
    casa_owneratom.set_arg(mass_str(), casa_mass)
    print(f"{casa_owneratom=}")
    assert casa_owneratom.get_value(mass_str()) == casa_mass
    clean_owneratom = owneratom_shop(owner_conceptunit_str(), INSERT_str())
    clean_owneratom.set_arg(concept_rope_str(), clean_rope)
    clean_owneratom.set_arg(task_str(), True)
    clean_owneratom.set_arg(mass_str(), 1)
    assert conceptunit_changunit.owneratom_exists(casa_owneratom)
    assert conceptunit_changunit.owneratom_exists(clean_owneratom)
    assert len(conceptunit_changunit.get_ordered_owneratoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_conceptunit_v0_0_0_Scenario_ownerunit_v001(
    big_volume,
):
    # sourcery skip: no-conditionals-in-tests
    if big_volume:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_conceptunit_v0_0_0()

        # WHEN
        conceptunit_format = create_idea_df(ownerunit_v001(), x_idea_name)

        # THEN
        array_headers = list(conceptunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(conceptunit_format) == 251
