from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.a01_term_logic.way import to_way
from src.a02_finance_logic._test_util.a02_str import fisc_label_str, owner_name_str
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    concept_way_str,
    credit_belief_str,
    credit_vote_str,
    debtit_belief_str,
    debtit_vote_str,
    group_title_str,
    mass_str,
    pledge_str,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a07_calendar_logic._test_util.calendar_examples import (
    add_time_creg_conceptunit,
    add_time_five_conceptunit,
)
from src.a17_idea_logic._test_util.a17_env import env_dir_setup_cleanup, idea_fiscs_dir
from src.a17_idea_logic.idea import create_idea_df, get_idearef_obj, save_idea_csv
from src.a17_idea_logic.idea_config import (
    idea_format_00013_conceptunit_v0_0_0,
    idea_format_00019_conceptunit_v0_0_0,
    idea_format_00020_bud_acct_membership_v0_0_0,
    idea_format_00021_bud_acctunit_v0_0_0,
)


def test_create_idea_df_Arg_idea_format_00021_bud_acctunit_v0_0_0():
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
    accord_fisc_label = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_label)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)

    # WHEN
    x_idea_name = idea_format_00021_bud_acctunit_v0_0_0()
    acct_dataframe = create_idea_df(sue_budunit, x_idea_name)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_idearef = get_idearef_obj(x_idea_name)
    assert array_headers == acct_idearef.get_headers_list()
    assert acct_dataframe.loc[0, fisc_label_str()] == accord_fisc_label
    assert acct_dataframe.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[0, acct_name_str()] == bob_str
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief

    assert acct_dataframe.loc[1, fisc_label_str()] == accord_fisc_label
    assert acct_dataframe.loc[1, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[1, acct_name_str()] == sue_str
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief

    assert acct_dataframe.loc[2, fisc_label_str()] == accord_fisc_label
    assert acct_dataframe.loc[2, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[2, acct_name_str()] == yao_str
    assert acct_dataframe.loc[2, debtit_belief_str()] == yao_debtit_belief
    assert acct_dataframe.loc[2, credit_belief_str()] == yao_credit_belief

    assert len(acct_dataframe) == 3


def test_create_idea_df_Arg_idea_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    accord_fisc_label = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_label)
    sue_budunit.add_acctunit(sue_str)
    sue_budunit.add_acctunit(bob_str)
    sue_budunit.add_acctunit(yao_str)
    iowa_str = ";Iowa"
    sue_iowa_credit_w = 37
    bob_iowa_credit_w = 43
    yao_iowa_credit_w = 51
    sue_iowa_debtit_w = 57
    bob_iowa_debtit_w = 61
    yao_iowa_debtit_w = 67
    ohio_str = ";Ohio"
    yao_ohio_credit_w = 73
    yao_ohio_debtit_w = 67
    sue_acctunit = sue_budunit.get_acct(sue_str)
    bob_acctunit = sue_budunit.get_acct(bob_str)
    yao_acctunit = sue_budunit.get_acct(yao_str)
    sue_acctunit.add_membership(iowa_str, sue_iowa_credit_w, sue_iowa_debtit_w)
    bob_acctunit.add_membership(iowa_str, bob_iowa_credit_w, bob_iowa_debtit_w)
    yao_acctunit.add_membership(iowa_str, yao_iowa_credit_w, yao_iowa_debtit_w)
    yao_acctunit.add_membership(ohio_str, yao_ohio_credit_w, yao_ohio_debtit_w)

    # WHEN
    x_idea_name = idea_format_00020_bud_acct_membership_v0_0_0()
    membership_dataframe = create_idea_df(sue_budunit, x_idea_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    acct_idearef = get_idearef_obj(x_idea_name)
    print(f"{len(membership_dataframe)=}")
    assert len(membership_dataframe) == 10
    assert array_headers == acct_idearef.get_headers_list()
    assert membership_dataframe.loc[0, fisc_label_str()] == accord_fisc_label
    assert membership_dataframe.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[0, acct_name_str()] == bob_str
    assert membership_dataframe.loc[0, group_title_str()] == iowa_str
    assert membership_dataframe.loc[0, credit_vote_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, debtit_vote_str()] == bob_iowa_debtit_w

    assert membership_dataframe.loc[3, fisc_label_str()] == accord_fisc_label
    assert membership_dataframe.loc[3, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[3, acct_name_str()] == sue_str
    assert membership_dataframe.loc[3, group_title_str()] == iowa_str
    assert membership_dataframe.loc[3, credit_vote_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[3, debtit_vote_str()] == sue_iowa_debtit_w

    assert membership_dataframe.loc[4, fisc_label_str()] == accord_fisc_label
    assert membership_dataframe.loc[4, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[4, acct_name_str()] == sue_str
    assert membership_dataframe.loc[4, group_title_str()] == sue_str
    assert membership_dataframe.loc[4, credit_vote_str()] == 1
    assert membership_dataframe.loc[4, debtit_vote_str()] == 1

    assert membership_dataframe.loc[7, fisc_label_str()] == accord_fisc_label
    assert membership_dataframe.loc[7, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[7, acct_name_str()] == yao_str
    assert membership_dataframe.loc[7, group_title_str()] == ohio_str
    assert membership_dataframe.loc[7, credit_vote_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[7, debtit_vote_str()] == yao_ohio_debtit_w
    assert len(membership_dataframe) == 10


def test_create_idea_df_Arg_idea_format_00013_conceptunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    accord_fisc_label = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_label)
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_concept(conceptunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_way = sue_budunit.make_way(casa_way, clean_str)
    sue_budunit.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)

    # WHEN
    x_idea_name = idea_format_00013_conceptunit_v0_0_0()
    conceptunit_format = create_idea_df(sue_budunit, x_idea_name)

    # THEN
    array_headers = list(conceptunit_format.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()

    assert conceptunit_format.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert conceptunit_format.loc[0, pledge_str()] == ""
    assert conceptunit_format.loc[0, fisc_label_str()] == accord_fisc_label
    assert conceptunit_format.loc[0, concept_way_str()] == casa_way
    assert conceptunit_format.loc[0, mass_str()] == casa_mass

    assert conceptunit_format.loc[1, owner_name_str()] == sue_budunit.owner_name
    assert conceptunit_format.loc[1, pledge_str()] == "Yes"
    assert conceptunit_format.loc[1, fisc_label_str()] == accord_fisc_label
    assert conceptunit_format.loc[1, concept_way_str()] == clean_way
    assert conceptunit_format.loc[1, mass_str()] == 1
    assert len(conceptunit_format) == 2


def test_save_idea_csv_Arg_idea_format_00019_conceptunit_v0_0_0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue", "accord56")
    sue_budunit = add_time_creg_conceptunit(sue_budunit)
    sue_budunit = add_time_five_conceptunit(sue_budunit)
    x_idea_name = idea_format_00019_conceptunit_v0_0_0()

    # WHEN
    # name_filename = f"{sue_str}_conceptunit_example_00019.csv"
    # csv_example_path = create_path(idea_fiscs_dir(), name_filename)
    # save_idea_csv(x_idea_name, sue_budunit, idea_examples_dir(), name_filename)
    idea_df = create_idea_df(sue_budunit, x_idea_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_idea_format_00021_bud_acctunit_v0_0_0_SaveToCSV(
    env_dir_setup_cleanup,
):
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
    accord_fisc_label = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_label)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_ideaname = idea_format_00021_bud_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_00.csv"
    csv_example_path = create_path(idea_fiscs_dir(), name_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(j1_ideaname, sue_budunit, idea_fiscs_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_name_example_csv = """event_int,face_name,fisc_label,owner_name,acct_name,credit_belief,debtit_belief
,,accord56,Sue,Bob,13,29
,,accord56,Sue,Sue,11,23
,,accord56,Sue,Yao,41,37
"""
    idea_file_str = open_file(idea_fiscs_dir(), name_filename)
    print(f"      {idea_file_str=}")
    print(f"{sue1_name_example_csv=}")
    assert idea_file_str == sue1_name_example_csv

    # WHEN
    zia_str = "Zia"
    sue_budunit.add_acctunit(zia_str)
    save_idea_csv(j1_ideaname, sue_budunit, idea_fiscs_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_acct_example_csv = """event_int,face_name,fisc_label,owner_name,acct_name,credit_belief,debtit_belief
,,accord56,Sue,Bob,13,29
,,accord56,Sue,Sue,11,23
,,accord56,Sue,Yao,41,37
,,accord56,Sue,Zia,1,1
"""
    assert open_file(idea_fiscs_dir(), name_filename) == sue2_acct_example_csv


def test_save_idea_csv_Arg_idea_format_00013_conceptunit_v0_0_0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    accord_fisc_label = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_label)
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_concept(conceptunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_way = sue_budunit.make_way(casa_way, clean_str)
    sue_budunit.set_concept(conceptunit_shop(clean_str, pledge=True), casa_way)
    x_idea_name = idea_format_00013_conceptunit_v0_0_0()
    conceptunit_format = create_idea_df(sue_budunit, x_idea_name)
    name_filename = f"{sue_str}_conceptunit_example_000.csv"
    csv_example_path = create_path(idea_fiscs_dir(), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_idea_name, sue_budunit, idea_fiscs_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
