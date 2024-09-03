from src._road.jaar_refer import sue_str, bob_str, yao_str
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.gift.atom_config import (
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    atom_insert,
    acct_id_str,
    group_id_str,
    parent_road_str,
    pledge_str,
    label_str,
    mass_str,
    debtit_score_str,
    credit_score_str,
    debtit_vote_str,
    credit_vote_str,
)
from src.gift.atom import atomunit_shop
from src.stone.stone import create_stone_df, create_changeunit
from src.stone.stone_config import (
    stone_format_00021_bud_acctunit_v0_0_0,
    stone_format_00020_bud_acct_membership_v0_0_0,
    stone_format_00003_ideaunit_v0_0_0,
)


def test_create_changeunit_Arg_stone_format_00021_bud_acctunit_v0_0_0():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    sue_credit_score = 11
    bob_credit_score = 13
    yao_credit_score = 41
    sue_debtit_score = 23
    bob_debtit_score = 29
    yao_debtit_score = 37
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text, sue_credit_score, sue_debtit_score)
    sue_budunit.add_acctunit(bob_text, bob_credit_score, bob_debtit_score)
    sue_budunit.add_acctunit(yao_text, yao_credit_score, yao_debtit_score)
    x_stone_name = stone_format_00021_bud_acctunit_v0_0_0()
    acct_dataframe = create_stone_df(sue_budunit, x_stone_name)
    acct_csv = acct_dataframe.to_csv(index=False)

    # WHEN
    sue_acct_changeunit = create_changeunit(acct_csv, x_stonename=x_stone_name)

    # THEN
    assert sue_acct_changeunit
    sue_atomunit = atomunit_shop(bud_acctunit_text(), atom_insert())
    sue_atomunit.set_arg(acct_id_str(), sue_text)
    sue_atomunit.set_arg(credit_score_str(), sue_credit_score)
    sue_atomunit.set_arg(debtit_score_str(), sue_debtit_score)
    sue_atomunit.set_atom_order()
    bob_atomunit = atomunit_shop(bud_acctunit_text(), atom_insert())
    bob_atomunit.set_arg(acct_id_str(), bob_text)
    bob_atomunit.set_arg(credit_score_str(), bob_credit_score)
    bob_atomunit.set_arg(debtit_score_str(), bob_debtit_score)
    bob_atomunit.set_atom_order()
    # print(f"{sue_acct_changeunit.get_ordered_dict()=}")
    # print(
    #     f"{sue_acct_changeunit.atomunits.get(atom_insert()).get(bud_acctunit_text()).get(sue_text)=}"
    # )
    assert sue_acct_changeunit.atomunit_exists(sue_atomunit)
    assert sue_acct_changeunit.atomunit_exists(bob_atomunit)
    assert len(sue_acct_changeunit.get_ordered_atomunits()) == 3


def test_create_changeunit_Arg_stone_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text)
    sue_budunit.add_acctunit(bob_text)
    sue_budunit.add_acctunit(yao_text)
    iowa_text = ";Iowa"
    sue_iowa_credit_vote = 37
    bob_iowa_credit_vote = 43
    yao_iowa_credit_vote = 51
    sue_iowa_debtit_vote = 57
    bob_iowa_debtit_vote = 61
    yao_iowa_debtit_vote = 67
    ohio_text = ";Ohio"
    yao_ohio_credit_vote = 73
    yao_ohio_debtit_vote = 67
    sue_acctunit = sue_budunit.get_acct(sue_text)
    bob_acctunit = sue_budunit.get_acct(bob_text)
    yao_acctunit = sue_budunit.get_acct(yao_text)
    sue_acctunit.add_membership(iowa_text, sue_iowa_credit_vote, sue_iowa_debtit_vote)
    bob_acctunit.add_membership(iowa_text, bob_iowa_credit_vote, bob_iowa_debtit_vote)
    yao_acctunit.add_membership(iowa_text, yao_iowa_credit_vote, yao_iowa_debtit_vote)
    yao_acctunit.add_membership(ohio_text, yao_ohio_credit_vote, yao_ohio_debtit_vote)
    x_stone_name = stone_format_00020_bud_acct_membership_v0_0_0()
    membership_dataframe = create_stone_df(sue_budunit, x_stone_name)
    assert len(membership_dataframe) == 7
    membership_csv = membership_dataframe.to_csv(index=False)

    # WHEN
    membership_changunit = create_changeunit(membership_csv, x_stone_name)

    # THEN
    assert membership_changunit
    sue_iowa_atomunit = atomunit_shop(bud_acct_membership_text(), atom_insert())
    bob_iowa_atomunit = atomunit_shop(bud_acct_membership_text(), atom_insert())
    yao_iowa_atomunit = atomunit_shop(bud_acct_membership_text(), atom_insert())
    yao_ohio_atomunit = atomunit_shop(bud_acct_membership_text(), atom_insert())
    sue_iowa_atomunit.set_arg(group_id_str(), iowa_text)
    bob_iowa_atomunit.set_arg(group_id_str(), iowa_text)
    yao_iowa_atomunit.set_arg(group_id_str(), iowa_text)
    yao_ohio_atomunit.set_arg(group_id_str(), ohio_text)
    sue_iowa_atomunit.set_arg(acct_id_str(), sue_text)
    bob_iowa_atomunit.set_arg(acct_id_str(), bob_text)
    yao_iowa_atomunit.set_arg(acct_id_str(), yao_text)
    yao_ohio_atomunit.set_arg(acct_id_str(), yao_text)
    sue_iowa_atomunit.set_arg(credit_vote_str(), sue_iowa_credit_vote)
    bob_iowa_atomunit.set_arg(credit_vote_str(), bob_iowa_credit_vote)
    yao_iowa_atomunit.set_arg(credit_vote_str(), yao_iowa_credit_vote)
    yao_ohio_atomunit.set_arg(credit_vote_str(), yao_ohio_credit_vote)
    sue_iowa_atomunit.set_arg(debtit_vote_str(), sue_iowa_debtit_vote)
    bob_iowa_atomunit.set_arg(debtit_vote_str(), bob_iowa_debtit_vote)
    yao_iowa_atomunit.set_arg(debtit_vote_str(), yao_iowa_debtit_vote)
    yao_ohio_atomunit.set_arg(debtit_vote_str(), yao_ohio_debtit_vote)
    bob_iowa_atomunit.set_atom_order()
    print(f"{membership_changunit.get_ordered_atomunits()[2]=}")
    print(f"{sue_iowa_atomunit=}")
    assert membership_changunit.get_ordered_atomunits()[0] == bob_iowa_atomunit
    assert membership_changunit.atomunit_exists(sue_iowa_atomunit)
    assert membership_changunit.atomunit_exists(bob_iowa_atomunit)
    assert membership_changunit.atomunit_exists(yao_iowa_atomunit)
    assert membership_changunit.atomunit_exists(yao_ohio_atomunit)
    assert len(membership_changunit.get_ordered_atomunits()) == 7


def test_create_changeunit_Arg_stone_format_00003_ideaunit_v0_0_0():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    casa_mass = 31
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text, _mass=casa_mass))
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    x_stone_name = stone_format_00003_ideaunit_v0_0_0()
    ideaunit_dataframe = create_stone_df(sue_budunit, x_stone_name)
    ideaunit_csv = ideaunit_dataframe.to_csv(index=False)

    # WHEN
    ideaunit_changunit = create_changeunit(ideaunit_csv, x_stone_name)

    # THEN
    casa_atomunit = atomunit_shop(bud_ideaunit_text(), atom_insert())
    casa_atomunit.set_arg(parent_road_str(), sue_budunit._real_id)
    casa_atomunit.set_arg(label_str(), casa_text)
    casa_atomunit.set_arg(pledge_str(), False)
    casa_atomunit.set_arg(mass_str(), casa_mass)
    assert casa_atomunit.get_value(mass_str()) == casa_mass
    clean_atomunit = atomunit_shop(bud_ideaunit_text(), atom_insert())
    clean_atomunit.set_arg(parent_road_str(), casa_road)
    clean_atomunit.set_arg(label_str(), clean_text)
    clean_atomunit.set_arg(pledge_str(), True)
    clean_atomunit.set_arg(mass_str(), 1)
    assert ideaunit_changunit.atomunit_exists(casa_atomunit)
    assert ideaunit_changunit.atomunit_exists(clean_atomunit)
    assert len(ideaunit_changunit.get_ordered_atomunits()) == 2


# # Commented out to reduce testing time.
# def test_create_stone_df_Arg_stone_format_00003_ideaunit_v0_0_0_Scenario_budunit_v001():
#     # ESTABLISH / WHEN
#     x_stone_name = stone_format_00003_ideaunit_v0_0_0()

#     # WHEN
#     ideaunit_format = create_stone_df(budunit_v001(), x_stone_name)

#     # THEN
#     array_headers = list(ideaunit_format.columns)
#     assert array_headers == get_stoneref(x_stone_name).get_headers_list()
#     assert len(ideaunit_format) == 251
#     assert 1 == 2
