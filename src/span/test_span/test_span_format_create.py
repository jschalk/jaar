from src._instrument.file import delete_dir, open_file
from src._road.jaar_refer import sue_str, bob_str, yao_str
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.span.span import (
    jaar_format_00001_acct_v0_0_0,
    jaar_format_00002_membership_v0_0_0,
    jaar_format_00003_ideaunit_v0_0_0,
    create_span_df,
    real_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    mass_str,
    pledge_str,
    debtit_score_str,
    credit_score_str,
    debtit_vote_str,
    credit_vote_str,
    get_spanref,
    save_span_csv,
)
from src.span.examples.span_env import span_examples_dir
from os.path import exists as os_path_exists


def test_create_span_df_Arg_jaar_format_00001_acct_v0_0_0():
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

    # WHEN
    x_span_name = jaar_format_00001_acct_v0_0_0()
    acct_dataframe = create_span_df(sue_budunit, x_span_name)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_spanref = get_spanref(x_span_name)
    assert array_headers == acct_spanref.get_headers_list()
    assert acct_dataframe.loc[0, real_id_str()] == music_real_id
    assert acct_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[0, acct_id_str()] == bob_text
    assert acct_dataframe.loc[0, credit_score_str()] == bob_credit_score
    assert acct_dataframe.loc[0, debtit_score_str()] == bob_debtit_score

    assert acct_dataframe.loc[1, real_id_str()] == music_real_id
    assert acct_dataframe.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[1, acct_id_str()] == sue_text
    assert acct_dataframe.loc[1, credit_score_str()] == sue_credit_score
    assert acct_dataframe.loc[1, debtit_score_str()] == sue_debtit_score

    assert acct_dataframe.loc[2, real_id_str()] == music_real_id
    assert acct_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[2, acct_id_str()] == yao_text
    assert acct_dataframe.loc[2, credit_score_str()] == yao_credit_score
    assert acct_dataframe.loc[2, debtit_score_str()] == yao_debtit_score

    assert len(acct_dataframe) == 3


def test_create_span_df_Arg_jaar_format_00002_membership_v0_0_0():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text)
    sue_budunit.add_acctunit(bob_text)
    sue_budunit.add_acctunit(yao_text)
    iowa_text = ",Iowa"
    sue_iowa_credit_w = 37
    bob_iowa_credit_w = 43
    yao_iowa_credit_w = 51
    sue_iowa_debtit_w = 57
    bob_iowa_debtit_w = 61
    yao_iowa_debtit_w = 67
    ohio_text = ",Ohio"
    yao_ohio_credit_w = 73
    yao_ohio_debtit_w = 67
    sue_acctunit = sue_budunit.get_acct(sue_text)
    bob_acctunit = sue_budunit.get_acct(bob_text)
    yao_acctunit = sue_budunit.get_acct(yao_text)
    sue_acctunit.add_membership(iowa_text, sue_iowa_credit_w, sue_iowa_debtit_w)
    bob_acctunit.add_membership(iowa_text, bob_iowa_credit_w, bob_iowa_debtit_w)
    yao_acctunit.add_membership(iowa_text, yao_iowa_credit_w, yao_iowa_debtit_w)
    yao_acctunit.add_membership(ohio_text, yao_ohio_credit_w, yao_ohio_debtit_w)

    # WHEN
    x_span_name = jaar_format_00002_membership_v0_0_0()
    membership_dataframe = create_span_df(sue_budunit, x_span_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    acct_spanref = get_spanref(x_span_name)
    print(f"{len(membership_dataframe)=}")
    assert array_headers == acct_spanref.get_headers_list()
    assert membership_dataframe.loc[0, real_id_str()] == music_real_id
    assert membership_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[0, acct_id_str()] == bob_text
    assert membership_dataframe.loc[0, group_id_str()] == iowa_text
    assert membership_dataframe.loc[0, credit_vote_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, debtit_vote_str()] == bob_iowa_debtit_w

    assert membership_dataframe.loc[2, real_id_str()] == music_real_id
    assert membership_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[2, acct_id_str()] == sue_text
    assert membership_dataframe.loc[2, group_id_str()] == iowa_text
    assert membership_dataframe.loc[2, credit_vote_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[2, debtit_vote_str()] == sue_iowa_debtit_w

    assert membership_dataframe.loc[4, real_id_str()] == music_real_id
    assert membership_dataframe.loc[4, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[4, acct_id_str()] == yao_text
    assert membership_dataframe.loc[4, group_id_str()] == iowa_text
    assert membership_dataframe.loc[4, credit_vote_str()] == yao_iowa_credit_w
    assert membership_dataframe.loc[4, debtit_vote_str()] == yao_iowa_debtit_w

    assert membership_dataframe.loc[5, real_id_str()] == music_real_id
    assert membership_dataframe.loc[5, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[5, acct_id_str()] == yao_text
    assert membership_dataframe.loc[5, group_id_str()] == ohio_text
    assert membership_dataframe.loc[5, credit_vote_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[5, debtit_vote_str()] == yao_ohio_debtit_w
    assert len(membership_dataframe) == 7


def test_create_span_df_Arg_jaar_format_00003_ideaunit_v0_0_0():
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

    # WHEN
    x_span_name = jaar_format_00003_ideaunit_v0_0_0()
    ideaunit_format = create_span_df(sue_budunit, x_span_name)

    # THEN
    array_headers = list(ideaunit_format.columns)
    assert array_headers == get_spanref(x_span_name).get_headers_list()

    assert ideaunit_format.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert ideaunit_format.loc[0, pledge_str()] == ""
    assert ideaunit_format.loc[0, real_id_str()] == music_real_id
    assert ideaunit_format.loc[0, label_str()] == casa_text
    assert ideaunit_format.loc[0, mass_str()] == casa_mass
    assert ideaunit_format.loc[0, parent_road_str()] == music_real_id

    assert ideaunit_format.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert ideaunit_format.loc[1, pledge_str()] == "Yes"
    assert ideaunit_format.loc[1, real_id_str()] == music_real_id
    assert ideaunit_format.loc[1, parent_road_str()] == casa_road
    assert ideaunit_format.loc[1, label_str()] == clean_text
    assert ideaunit_format.loc[1, mass_str()] == 1
    assert len(ideaunit_format) == 2


# Commented out to reduce testing time.
# def test_create_span_df_Arg_jaar_format_00003_ideaunit_v0_0_0_Scenario_budunit_v001():
#     # ESTABLISH / WHEN
#     x_span_name = jaar_format_00003_ideaunit_v0_0_0()

#     # WHEN
#     ideaunit_format = create_span_df(budunit_v001(), x_span_name)

#     # THEN
#     array_headers = list(ideaunit_format.columns)
#     assert array_headers == get_spanref(x_span_name).get_headers_list()
#     assert len(ideaunit_format) == 252


def test_save_span_csv_Arg_jaar_format_00001_acct_v0_0_0_SaveToCSV():
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
    j1_spanname = jaar_format_00001_acct_v0_0_0()
    acct_filename = f"{sue_text}_acct_example_00.csv"
    csv_example_path = f"{span_examples_dir()}/{acct_filename}"
    print(f"{csv_example_path}")
    delete_dir(csv_example_path)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_span_csv(j1_spanname, sue_budunit, span_examples_dir(), acct_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue_acct_example_csv = """real_id,owner_id,acct_id,credit_score,debtit_score
music56,Sue,Bob,13,29
music56,Sue,Sue,11,23
music56,Sue,Yao,41,37
"""
    assert open_file(span_examples_dir(), acct_filename) == sue_acct_example_csv
