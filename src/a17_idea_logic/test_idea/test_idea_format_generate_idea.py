from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_tool import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
)
from src.a06_bud_logic.examples.example_buds import budunit_v001
from src.a08_bud_atom_logic.atom_config import (
    atom_insert,
    acct_name_str,
    group_label_str,
    parent_road_str,
    pledge_str,
    item_title_str,
    mass_str,
    debtit_belief_str,
    credit_belief_str,
    debtit_vote_str,
    credit_vote_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a17_idea_logic.idea import create_idea_df, make_buddelta, get_idearef_obj
from src.a17_idea_logic.idea_config import (
    idea_format_00021_bud_acctunit_v0_0_0,
    idea_format_00020_bud_acct_membership_v0_0_0,
    idea_format_00013_itemunit_v0_0_0,
)


def test_make_buddelta_Arg_idea_format_00021_bud_acctunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_belief = 11
    bob_credit_belief = 13
    yao_credit_belief = 41
    sue_debtit_belief = 23
    bob_debtit_belief = 29
    yao_debtit_belief = 37
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    x_idea_name = idea_format_00021_bud_acctunit_v0_0_0()
    acct_dataframe = create_idea_df(sue_budunit, x_idea_name)
    print(f"{acct_dataframe.columns=}")
    acct_csv = acct_dataframe.to_csv(index=False)

    # WHEN
    sue_acct_buddelta = make_buddelta(acct_csv)

    # THEN
    assert sue_acct_buddelta
    sue_budatom = budatom_shop(bud_acctunit_str(), atom_insert())
    sue_budatom.set_arg(acct_name_str(), sue_str)
    sue_budatom.set_arg(credit_belief_str(), sue_credit_belief)
    sue_budatom.set_arg(debtit_belief_str(), sue_debtit_belief)
    sue_budatom.set_atom_order()
    bob_budatom = budatom_shop(bud_acctunit_str(), atom_insert())
    bob_budatom.set_arg(acct_name_str(), bob_str)
    bob_budatom.set_arg(credit_belief_str(), bob_credit_belief)
    bob_budatom.set_arg(debtit_belief_str(), bob_debtit_belief)
    bob_budatom.set_atom_order()
    # print(f"{sue_acct_buddelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_acct_buddelta.budatoms.get(atom_insert()).get(bud_acctunit_str()).get(sue_str)=}"
    # )
    print(f"{sue_budatom=}")
    assert sue_acct_buddelta.budatom_exists(sue_budatom)
    assert sue_acct_buddelta.budatom_exists(bob_budatom)
    assert len(sue_acct_buddelta.get_ordered_budatoms()) == 3


def test_make_buddelta_Arg_idea_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    sue_budunit.add_acctunit(sue_str)
    sue_budunit.add_acctunit(bob_str)
    sue_budunit.add_acctunit(yao_str)
    iowa_str = ";Iowa"
    sue_iowa_credit_vote = 37
    bob_iowa_credit_vote = 43
    yao_iowa_credit_vote = 51
    sue_iowa_debtit_vote = 57
    bob_iowa_debtit_vote = 61
    yao_iowa_debtit_vote = 67
    ohio_str = ";Ohio"
    yao_ohio_credit_vote = 73
    yao_ohio_debtit_vote = 67
    sue_acctunit = sue_budunit.get_acct(sue_str)
    bob_acctunit = sue_budunit.get_acct(bob_str)
    yao_acctunit = sue_budunit.get_acct(yao_str)
    sue_acctunit.add_membership(iowa_str, sue_iowa_credit_vote, sue_iowa_debtit_vote)
    bob_acctunit.add_membership(iowa_str, bob_iowa_credit_vote, bob_iowa_debtit_vote)
    yao_acctunit.add_membership(iowa_str, yao_iowa_credit_vote, yao_iowa_debtit_vote)
    yao_acctunit.add_membership(ohio_str, yao_ohio_credit_vote, yao_ohio_debtit_vote)
    x_idea_name = idea_format_00020_bud_acct_membership_v0_0_0()
    membership_dataframe = create_idea_df(sue_budunit, x_idea_name)
    assert len(membership_dataframe) == 7
    membership_csv = membership_dataframe.to_csv(index=False)
    print(f"{membership_csv=}")

    # WHEN
    membership_changunit = make_buddelta(membership_csv)

    # THEN
    assert membership_changunit
    sue_iowa_budatom = budatom_shop(bud_acct_membership_str(), atom_insert())
    bob_iowa_budatom = budatom_shop(bud_acct_membership_str(), atom_insert())
    yao_iowa_budatom = budatom_shop(bud_acct_membership_str(), atom_insert())
    yao_ohio_budatom = budatom_shop(bud_acct_membership_str(), atom_insert())
    sue_iowa_budatom.set_arg(group_label_str(), iowa_str)
    bob_iowa_budatom.set_arg(group_label_str(), iowa_str)
    yao_iowa_budatom.set_arg(group_label_str(), iowa_str)
    yao_ohio_budatom.set_arg(group_label_str(), ohio_str)
    sue_iowa_budatom.set_arg(acct_name_str(), sue_str)
    bob_iowa_budatom.set_arg(acct_name_str(), bob_str)
    yao_iowa_budatom.set_arg(acct_name_str(), yao_str)
    yao_ohio_budatom.set_arg(acct_name_str(), yao_str)
    sue_iowa_budatom.set_arg(credit_vote_str(), sue_iowa_credit_vote)
    bob_iowa_budatom.set_arg(credit_vote_str(), bob_iowa_credit_vote)
    yao_iowa_budatom.set_arg(credit_vote_str(), yao_iowa_credit_vote)
    yao_ohio_budatom.set_arg(credit_vote_str(), yao_ohio_credit_vote)
    sue_iowa_budatom.set_arg(debtit_vote_str(), sue_iowa_debtit_vote)
    bob_iowa_budatom.set_arg(debtit_vote_str(), bob_iowa_debtit_vote)
    yao_iowa_budatom.set_arg(debtit_vote_str(), yao_iowa_debtit_vote)
    yao_ohio_budatom.set_arg(debtit_vote_str(), yao_ohio_debtit_vote)
    bob_iowa_budatom.set_atom_order()
    # print(f"{membership_changunit.get_ordered_budatoms()[2]=}")
    # print(f"{sue_iowa_budatom=}")
    assert len(membership_changunit.get_ordered_budatoms()) == 7
    assert membership_changunit.get_ordered_budatoms()[0] == bob_iowa_budatom
    assert membership_changunit.budatom_exists(sue_iowa_budatom)
    assert membership_changunit.budatom_exists(bob_iowa_budatom)
    assert membership_changunit.budatom_exists(yao_iowa_budatom)
    assert membership_changunit.budatom_exists(yao_ohio_budatom)
    assert len(membership_changunit.get_ordered_budatoms()) == 7


def test_make_buddelta_Arg_idea_format_00013_itemunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_item(itemunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    sue_budunit.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    x_idea_name = idea_format_00013_itemunit_v0_0_0()
    itemunit_dataframe = create_idea_df(sue_budunit, x_idea_name)
    itemunit_csv = itemunit_dataframe.to_csv(index=False)

    # WHEN
    itemunit_changunit = make_buddelta(itemunit_csv)

    # THEN
    casa_budatom = budatom_shop(bud_itemunit_str(), atom_insert())
    casa_budatom.set_arg(parent_road_str(), sue_budunit.fisc_title)
    casa_budatom.set_arg(item_title_str(), casa_str)
    casa_budatom.set_arg(pledge_str(), False)
    casa_budatom.set_arg(mass_str(), casa_mass)
    print(f"{casa_budatom=}")
    assert casa_budatom.get_value(mass_str()) == casa_mass
    clean_budatom = budatom_shop(bud_itemunit_str(), atom_insert())
    clean_budatom.set_arg(parent_road_str(), casa_road)
    clean_budatom.set_arg(item_title_str(), clean_str)
    clean_budatom.set_arg(pledge_str(), True)
    clean_budatom.set_arg(mass_str(), 1)
    assert itemunit_changunit.budatom_exists(casa_budatom)
    assert itemunit_changunit.budatom_exists(clean_budatom)
    assert len(itemunit_changunit.get_ordered_budatoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_itemunit_v0_0_0_Scenario_budunit_v001(
    big_volume,
):
    # sourcery skip: no-conditionals-in-tests
    if big_volume:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_itemunit_v0_0_0()

        # WHEN
        itemunit_format = create_idea_df(budunit_v001(), x_idea_name)

        # THEN
        array_headers = list(itemunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(itemunit_format) == 251


def test_make_buddelta_Arg_idea_format_00013_itemunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_item(itemunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    sue_budunit.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    x_idea_name = idea_format_00013_itemunit_v0_0_0()
    itemunit_dataframe = create_idea_df(sue_budunit, x_idea_name)
    itemunit_csv = itemunit_dataframe.to_csv(index=False)

    # WHEN
    itemunit_changunit = make_buddelta(itemunit_csv)

    # THEN
    casa_budatom = budatom_shop(bud_itemunit_str(), atom_insert())
    casa_budatom.set_arg(parent_road_str(), sue_budunit.fisc_title)
    casa_budatom.set_arg(item_title_str(), casa_str)
    casa_budatom.set_arg(pledge_str(), False)
    casa_budatom.set_arg(mass_str(), casa_mass)
    print(f"{casa_budatom=}")
    assert casa_budatom.get_value(mass_str()) == casa_mass
    clean_budatom = budatom_shop(bud_itemunit_str(), atom_insert())
    clean_budatom.set_arg(parent_road_str(), casa_road)
    clean_budatom.set_arg(item_title_str(), clean_str)
    clean_budatom.set_arg(pledge_str(), True)
    clean_budatom.set_arg(mass_str(), 1)
    assert itemunit_changunit.budatom_exists(casa_budatom)
    assert itemunit_changunit.budatom_exists(clean_budatom)
    assert len(itemunit_changunit.get_ordered_budatoms()) == 2
