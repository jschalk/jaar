from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.a01_term_logic.rope import to_rope
from src.a02_finance_logic.test._util.a02_str import owner_name_str, vow_label_str
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    concept_rope_str,
    credit_score_str,
    credit_vote_str,
    debt_score_str,
    debt_vote_str,
    group_title_str,
    mass_str,
    task_str,
)
from src.a07_calendar_logic.test._util.calendar_examples import (
    add_time_creg_conceptunit,
    add_time_five_conceptunit,
)
from src.a17_idea_logic.idea import create_idea_df, get_idearef_obj, save_idea_csv
from src.a17_idea_logic.idea_config import (
    idea_format_00013_conceptunit_v0_0_0,
    idea_format_00019_conceptunit_v0_0_0,
    idea_format_00020_plan_acct_membership_v0_0_0,
    idea_format_00021_plan_acctunit_v0_0_0,
)
from src.a17_idea_logic.test._util.a17_env import env_dir_setup_cleanup, idea_vows_dir


def test_create_idea_df_Arg_idea_format_00021_plan_acctunit_v0_0_0():
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

    # WHEN
    x_idea_name = idea_format_00021_plan_acctunit_v0_0_0()
    acct_dataframe = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_idearef = get_idearef_obj(x_idea_name)
    assert array_headers == acct_idearef.get_headers_list()
    assert acct_dataframe.loc[0, vow_label_str()] == accord_vow_label
    assert acct_dataframe.loc[0, owner_name_str()] == sue_planunit.owner_name
    assert acct_dataframe.loc[0, acct_name_str()] == bob_str
    assert acct_dataframe.loc[0, debt_score_str()] == bob_debt_score
    assert acct_dataframe.loc[0, credit_score_str()] == bob_credit_score

    assert acct_dataframe.loc[1, vow_label_str()] == accord_vow_label
    assert acct_dataframe.loc[1, owner_name_str()] == sue_planunit.owner_name
    assert acct_dataframe.loc[1, acct_name_str()] == sue_str
    assert acct_dataframe.loc[1, debt_score_str()] == sue_debt_score
    assert acct_dataframe.loc[1, credit_score_str()] == sue_credit_score

    assert acct_dataframe.loc[2, vow_label_str()] == accord_vow_label
    assert acct_dataframe.loc[2, owner_name_str()] == sue_planunit.owner_name
    assert acct_dataframe.loc[2, acct_name_str()] == yao_str
    assert acct_dataframe.loc[2, debt_score_str()] == yao_debt_score
    assert acct_dataframe.loc[2, credit_score_str()] == yao_credit_score

    assert len(acct_dataframe) == 3


def test_create_idea_df_Arg_idea_format_00020_plan_acct_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    sue_planunit.add_acctunit(sue_str)
    sue_planunit.add_acctunit(bob_str)
    sue_planunit.add_acctunit(yao_str)
    iowa_str = ";Iowa"
    sue_iowa_credit_w = 37
    bob_iowa_credit_w = 43
    yao_iowa_credit_w = 51
    sue_iowa_debt_w = 57
    bob_iowa_debt_w = 61
    yao_iowa_debt_w = 67
    ohio_str = ";Ohio"
    yao_ohio_credit_w = 73
    yao_ohio_debt_w = 67
    sue_acctunit = sue_planunit.get_acct(sue_str)
    bob_acctunit = sue_planunit.get_acct(bob_str)
    yao_acctunit = sue_planunit.get_acct(yao_str)
    sue_acctunit.add_membership(iowa_str, sue_iowa_credit_w, sue_iowa_debt_w)
    bob_acctunit.add_membership(iowa_str, bob_iowa_credit_w, bob_iowa_debt_w)
    yao_acctunit.add_membership(iowa_str, yao_iowa_credit_w, yao_iowa_debt_w)
    yao_acctunit.add_membership(ohio_str, yao_ohio_credit_w, yao_ohio_debt_w)

    # WHEN
    x_idea_name = idea_format_00020_plan_acct_membership_v0_0_0()
    membership_dataframe = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    acct_idearef = get_idearef_obj(x_idea_name)
    print(f"{len(membership_dataframe)=}")
    assert len(membership_dataframe) == 10
    assert array_headers == acct_idearef.get_headers_list()
    assert membership_dataframe.loc[0, vow_label_str()] == accord_vow_label
    assert membership_dataframe.loc[0, owner_name_str()] == sue_planunit.owner_name
    assert membership_dataframe.loc[0, acct_name_str()] == bob_str
    assert membership_dataframe.loc[0, group_title_str()] == iowa_str
    assert membership_dataframe.loc[0, credit_vote_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, debt_vote_str()] == bob_iowa_debt_w

    assert membership_dataframe.loc[3, vow_label_str()] == accord_vow_label
    assert membership_dataframe.loc[3, owner_name_str()] == sue_planunit.owner_name
    assert membership_dataframe.loc[3, acct_name_str()] == sue_str
    assert membership_dataframe.loc[3, group_title_str()] == iowa_str
    assert membership_dataframe.loc[3, credit_vote_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[3, debt_vote_str()] == sue_iowa_debt_w

    assert membership_dataframe.loc[4, vow_label_str()] == accord_vow_label
    assert membership_dataframe.loc[4, owner_name_str()] == sue_planunit.owner_name
    assert membership_dataframe.loc[4, acct_name_str()] == sue_str
    assert membership_dataframe.loc[4, group_title_str()] == sue_str
    assert membership_dataframe.loc[4, credit_vote_str()] == 1
    assert membership_dataframe.loc[4, debt_vote_str()] == 1

    assert membership_dataframe.loc[7, vow_label_str()] == accord_vow_label
    assert membership_dataframe.loc[7, owner_name_str()] == sue_planunit.owner_name
    assert membership_dataframe.loc[7, acct_name_str()] == yao_str
    assert membership_dataframe.loc[7, group_title_str()] == ohio_str
    assert membership_dataframe.loc[7, credit_vote_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[7, debt_vote_str()] == yao_ohio_debt_w
    assert len(membership_dataframe) == 10


def test_create_idea_df_Arg_idea_format_00013_conceptunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    casa_mass = 31
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)

    # WHEN
    x_idea_name = idea_format_00013_conceptunit_v0_0_0()
    conceptunit_format = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(conceptunit_format.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()

    assert conceptunit_format.loc[0, owner_name_str()] == sue_planunit.owner_name
    assert conceptunit_format.loc[0, task_str()] == ""
    assert conceptunit_format.loc[0, vow_label_str()] == accord_vow_label
    assert conceptunit_format.loc[0, concept_rope_str()] == casa_rope
    assert conceptunit_format.loc[0, mass_str()] == casa_mass

    assert conceptunit_format.loc[1, owner_name_str()] == sue_planunit.owner_name
    assert conceptunit_format.loc[1, task_str()] == "Yes"
    assert conceptunit_format.loc[1, vow_label_str()] == accord_vow_label
    assert conceptunit_format.loc[1, concept_rope_str()] == clean_rope
    assert conceptunit_format.loc[1, mass_str()] == 1
    assert len(conceptunit_format) == 2


def test_save_idea_csv_Arg_idea_format_00019_conceptunit_v0_0_0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue", "accord56")
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    sue_planunit = add_time_five_conceptunit(sue_planunit)
    x_idea_name = idea_format_00019_conceptunit_v0_0_0()

    # WHEN
    # name_filename = f"{sue_str}_conceptunit_example_00019.csv"
    # csv_example_path = create_path(idea_vows_dir(), name_filename)
    # save_idea_csv(x_idea_name, sue_planunit, idea_examples_dir(), name_filename)
    idea_df = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_idea_format_00021_plan_acctunit_v0_0_0_SaveToCSV(
    env_dir_setup_cleanup,
):
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
    j1_ideaname = idea_format_00021_plan_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_00.csv"
    csv_example_path = create_path(idea_vows_dir(), name_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(j1_ideaname, sue_planunit, idea_vows_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_name_example_csv = """event_int,face_name,vow_label,owner_name,acct_name,credit_score,debt_score
,,accord56,Sue,Bob,13,29
,,accord56,Sue,Sue,11,23
,,accord56,Sue,Yao,41,37
"""
    idea_file_str = open_file(idea_vows_dir(), name_filename)
    print(f"      {idea_file_str=}")
    print(f"{sue1_name_example_csv=}")
    assert idea_file_str == sue1_name_example_csv

    # WHEN
    zia_str = "Zia"
    sue_planunit.add_acctunit(zia_str)
    save_idea_csv(j1_ideaname, sue_planunit, idea_vows_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_acct_example_csv = """event_int,face_name,vow_label,owner_name,acct_name,credit_score,debt_score
,,accord56,Sue,Bob,13,29
,,accord56,Sue,Sue,11,23
,,accord56,Sue,Yao,41,37
,,accord56,Sue,Zia,1,1
"""
    assert open_file(idea_vows_dir(), name_filename) == sue2_acct_example_csv


def test_save_idea_csv_Arg_idea_format_00013_conceptunit_v0_0_0(
    env_dir_setup_cleanup,
):
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
    conceptunit_format = create_idea_df(sue_planunit, x_idea_name)
    name_filename = f"{sue_str}_conceptunit_example_000.csv"
    csv_example_path = create_path(idea_vows_dir(), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_idea_name, sue_planunit, idea_vows_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
