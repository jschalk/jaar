from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    belief_label_str,
    concept_rope_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    mass_str,
    owner_name_str,
    task_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_conceptunit,
    add_time_five_conceptunit,
)
from src.a17_idea_logic.idea import create_idea_df, get_idearef_obj, save_idea_csv
from src.a17_idea_logic.idea_config import (
    idea_format_00013_conceptunit_v0_0_0,
    idea_format_00019_conceptunit_v0_0_0,
    idea_format_00020_owner_acct_membership_v0_0_0,
    idea_format_00021_owner_acctunit_v0_0_0,
)
from src.a17_idea_logic.test._util.a17_env import (
    env_dir_setup_cleanup,
    idea_beliefs_dir,
)


def test_create_idea_df_Arg_idea_format_00021_owner_acctunit_v0_0_0():
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

    # WHEN
    x_idea_name = idea_format_00021_owner_acctunit_v0_0_0()
    acct_dataframe = create_idea_df(sue_ownerunit, x_idea_name)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_idearef = get_idearef_obj(x_idea_name)
    assert array_headers == acct_idearef.get_headers_list()
    assert acct_dataframe.loc[0, belief_label_str()] == amy_belief_label
    assert acct_dataframe.loc[0, owner_name_str()] == sue_ownerunit.owner_name
    assert acct_dataframe.loc[0, acct_name_str()] == bob_str
    assert acct_dataframe.loc[0, acct_debt_points_str()] == bob_acct_debt_points
    assert acct_dataframe.loc[0, acct_cred_points_str()] == bob_acct_cred_points

    assert acct_dataframe.loc[1, belief_label_str()] == amy_belief_label
    assert acct_dataframe.loc[1, owner_name_str()] == sue_ownerunit.owner_name
    assert acct_dataframe.loc[1, acct_name_str()] == sue_str
    assert acct_dataframe.loc[1, acct_debt_points_str()] == sue_acct_debt_points
    assert acct_dataframe.loc[1, acct_cred_points_str()] == sue_acct_cred_points

    assert acct_dataframe.loc[2, belief_label_str()] == amy_belief_label
    assert acct_dataframe.loc[2, owner_name_str()] == sue_ownerunit.owner_name
    assert acct_dataframe.loc[2, acct_name_str()] == yao_str
    assert acct_dataframe.loc[2, acct_debt_points_str()] == yao_acct_debt_points
    assert acct_dataframe.loc[2, acct_cred_points_str()] == yao_acct_cred_points

    assert len(acct_dataframe) == 3


def test_create_idea_df_Arg_idea_format_00020_owner_acct_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    amy_belief_label = "amy56"
    sue_ownerunit = ownerunit_shop(sue_str, amy_belief_label)
    sue_ownerunit.add_acctunit(sue_str)
    sue_ownerunit.add_acctunit(bob_str)
    sue_ownerunit.add_acctunit(yao_str)
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
    sue_acctunit = sue_ownerunit.get_acct(sue_str)
    bob_acctunit = sue_ownerunit.get_acct(bob_str)
    yao_acctunit = sue_ownerunit.get_acct(yao_str)
    sue_acctunit.add_membership(iowa_str, sue_iowa_credit_w, sue_iowa_debt_w)
    bob_acctunit.add_membership(iowa_str, bob_iowa_credit_w, bob_iowa_debt_w)
    yao_acctunit.add_membership(iowa_str, yao_iowa_credit_w, yao_iowa_debt_w)
    yao_acctunit.add_membership(ohio_str, yao_ohio_credit_w, yao_ohio_debt_w)

    # WHEN
    x_idea_name = idea_format_00020_owner_acct_membership_v0_0_0()
    membership_dataframe = create_idea_df(sue_ownerunit, x_idea_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    acct_idearef = get_idearef_obj(x_idea_name)
    print(f"{len(membership_dataframe)=}")
    assert len(membership_dataframe) == 10
    assert array_headers == acct_idearef.get_headers_list()
    assert membership_dataframe.loc[0, belief_label_str()] == amy_belief_label
    assert membership_dataframe.loc[0, owner_name_str()] == sue_ownerunit.owner_name
    assert membership_dataframe.loc[0, acct_name_str()] == bob_str
    assert membership_dataframe.loc[0, group_title_str()] == iowa_str
    assert membership_dataframe.loc[0, group_cred_points_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, group_debt_points_str()] == bob_iowa_debt_w

    assert membership_dataframe.loc[3, belief_label_str()] == amy_belief_label
    assert membership_dataframe.loc[3, owner_name_str()] == sue_ownerunit.owner_name
    assert membership_dataframe.loc[3, acct_name_str()] == sue_str
    assert membership_dataframe.loc[3, group_title_str()] == iowa_str
    assert membership_dataframe.loc[3, group_cred_points_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[3, group_debt_points_str()] == sue_iowa_debt_w

    assert membership_dataframe.loc[4, belief_label_str()] == amy_belief_label
    assert membership_dataframe.loc[4, owner_name_str()] == sue_ownerunit.owner_name
    assert membership_dataframe.loc[4, acct_name_str()] == sue_str
    assert membership_dataframe.loc[4, group_title_str()] == sue_str
    assert membership_dataframe.loc[4, group_cred_points_str()] == 1
    assert membership_dataframe.loc[4, group_debt_points_str()] == 1

    assert membership_dataframe.loc[7, belief_label_str()] == amy_belief_label
    assert membership_dataframe.loc[7, owner_name_str()] == sue_ownerunit.owner_name
    assert membership_dataframe.loc[7, acct_name_str()] == yao_str
    assert membership_dataframe.loc[7, group_title_str()] == ohio_str
    assert membership_dataframe.loc[7, group_cred_points_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[7, group_debt_points_str()] == yao_ohio_debt_w
    assert len(membership_dataframe) == 10


def test_create_idea_df_Arg_idea_format_00013_conceptunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    amy_belief_label = "amy56"
    sue_ownerunit = ownerunit_shop(sue_str, amy_belief_label)
    casa_str = "casa"
    casa_rope = sue_ownerunit.make_l1_rope(casa_str)
    casa_mass = 31
    sue_ownerunit.set_l1_concept(conceptunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_rope = sue_ownerunit.make_rope(casa_rope, clean_str)
    sue_ownerunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)

    # WHEN
    x_idea_name = idea_format_00013_conceptunit_v0_0_0()
    conceptunit_format = create_idea_df(sue_ownerunit, x_idea_name)

    # THEN
    array_headers = list(conceptunit_format.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()

    assert conceptunit_format.loc[0, owner_name_str()] == sue_ownerunit.owner_name
    assert conceptunit_format.loc[0, task_str()] == ""
    assert conceptunit_format.loc[0, belief_label_str()] == amy_belief_label
    assert conceptunit_format.loc[0, concept_rope_str()] == casa_rope
    assert conceptunit_format.loc[0, mass_str()] == casa_mass

    assert conceptunit_format.loc[1, owner_name_str()] == sue_ownerunit.owner_name
    assert conceptunit_format.loc[1, task_str()] == "Yes"
    assert conceptunit_format.loc[1, belief_label_str()] == amy_belief_label
    assert conceptunit_format.loc[1, concept_rope_str()] == clean_rope
    assert conceptunit_format.loc[1, mass_str()] == 1
    assert len(conceptunit_format) == 2


def test_save_idea_csv_Arg_idea_format_00019_conceptunit_v0_0_0():
    # ESTABLISH
    sue_ownerunit = ownerunit_shop("Sue", "amy56")
    sue_ownerunit = add_time_creg_conceptunit(sue_ownerunit)
    sue_ownerunit = add_time_five_conceptunit(sue_ownerunit)
    x_idea_name = idea_format_00019_conceptunit_v0_0_0()

    # WHEN
    # name_filename = f"{sue_str}_conceptunit_example_00019.csv"
    # csv_example_path = create_path(idea_beliefs_dir(), name_filename)
    # save_idea_csv(x_idea_name, sue_ownerunit, get_module_temp_dir(), name_filename)
    idea_df = create_idea_df(sue_ownerunit, x_idea_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_idea_format_00021_owner_acctunit_v0_0_0_SaveToCSV(
    env_dir_setup_cleanup,
):
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
    j1_ideaname = idea_format_00021_owner_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_00.csv"
    csv_example_path = create_path(idea_beliefs_dir(), name_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(j1_ideaname, sue_ownerunit, idea_beliefs_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_name_example_csv = """event_int,face_name,belief_label,owner_name,acct_name,acct_cred_points,acct_debt_points
,,amy56,Sue,Bob,13,29
,,amy56,Sue,Sue,11,23
,,amy56,Sue,Yao,41,37
"""
    idea_file_str = open_file(idea_beliefs_dir(), name_filename)
    print(f"      {idea_file_str=}")
    print(f"{sue1_name_example_csv=}")
    assert idea_file_str == sue1_name_example_csv

    # WHEN
    zia_str = "Zia"
    sue_ownerunit.add_acctunit(zia_str)
    save_idea_csv(j1_ideaname, sue_ownerunit, idea_beliefs_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_acct_example_csv = """event_int,face_name,belief_label,owner_name,acct_name,acct_cred_points,acct_debt_points
,,amy56,Sue,Bob,13,29
,,amy56,Sue,Sue,11,23
,,amy56,Sue,Yao,41,37
,,amy56,Sue,Zia,1,1
"""
    assert open_file(idea_beliefs_dir(), name_filename) == sue2_acct_example_csv


def test_save_idea_csv_Arg_idea_format_00013_conceptunit_v0_0_0(
    env_dir_setup_cleanup,
):
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
    conceptunit_format = create_idea_df(sue_ownerunit, x_idea_name)
    name_filename = f"{sue_str}_conceptunit_example_000.csv"
    csv_example_path = create_path(idea_beliefs_dir(), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_idea_name, sue_ownerunit, idea_beliefs_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
