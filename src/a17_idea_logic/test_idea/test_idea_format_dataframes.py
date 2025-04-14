from src.a00_data_toolboxs.file_toolbox import open_file, create_path
from src.a02_finance_toolboxs.deal import owner_name_str, fisc_title_str
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a07_calendar_logic.examples.chrono_examples import (
    add_time_creg_itemunit,
    add_time_five_itemunit,
)
from src.a08_bud_atom_logic.atom_config import (
    acct_name_str,
    group_label_str,
    parent_road_str,
    item_title_str,
    mass_str,
    pledge_str,
    debtit_belief_str,
    credit_belief_str,
    debtit_vote_str,
    credit_vote_str,
)
from src.a17_idea_logic.idea import create_idea_df, get_idearef_obj, save_idea_csv
from src.a17_idea_logic.idea_config import (
    idea_format_00021_bud_acctunit_v0_0_0,
    idea_format_00020_bud_acct_membership_v0_0_0,
    idea_format_00013_itemunit_v0_0_0,
    idea_format_00019_itemunit_v0_0_0,
)
from src.a17_idea_logic.examples.idea_env import (
    idea_examples_dir,
    idea_fiscs_dir,
    idea_env_setup_cleanup,
)
from os.path import exists as os_path_exists


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
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
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
    assert acct_dataframe.loc[0, fisc_title_str()] == accord_fisc_title
    assert acct_dataframe.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[0, acct_name_str()] == bob_str
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief

    assert acct_dataframe.loc[1, fisc_title_str()] == accord_fisc_title
    assert acct_dataframe.loc[1, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[1, acct_name_str()] == sue_str
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief

    assert acct_dataframe.loc[2, fisc_title_str()] == accord_fisc_title
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
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
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
    assert array_headers == acct_idearef.get_headers_list()
    assert membership_dataframe.loc[0, fisc_title_str()] == accord_fisc_title
    assert membership_dataframe.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[0, acct_name_str()] == bob_str
    assert membership_dataframe.loc[0, group_label_str()] == iowa_str
    assert membership_dataframe.loc[0, credit_vote_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, debtit_vote_str()] == bob_iowa_debtit_w

    assert membership_dataframe.loc[2, fisc_title_str()] == accord_fisc_title
    assert membership_dataframe.loc[2, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[2, acct_name_str()] == sue_str
    assert membership_dataframe.loc[2, group_label_str()] == iowa_str
    assert membership_dataframe.loc[2, credit_vote_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[2, debtit_vote_str()] == sue_iowa_debtit_w

    assert membership_dataframe.loc[4, fisc_title_str()] == accord_fisc_title
    assert membership_dataframe.loc[4, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[4, acct_name_str()] == yao_str
    assert membership_dataframe.loc[4, group_label_str()] == iowa_str
    assert membership_dataframe.loc[4, credit_vote_str()] == yao_iowa_credit_w
    assert membership_dataframe.loc[4, debtit_vote_str()] == yao_iowa_debtit_w

    assert membership_dataframe.loc[5, fisc_title_str()] == accord_fisc_title
    assert membership_dataframe.loc[5, owner_name_str()] == sue_budunit.owner_name
    assert membership_dataframe.loc[5, acct_name_str()] == yao_str
    assert membership_dataframe.loc[5, group_label_str()] == ohio_str
    assert membership_dataframe.loc[5, credit_vote_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[5, debtit_vote_str()] == yao_ohio_debtit_w
    assert len(membership_dataframe) == 7


def test_create_idea_df_Arg_idea_format_00013_itemunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_item(itemunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    sue_budunit.set_item(itemunit_shop(clean_str, pledge=True), casa_road)

    # WHEN
    x_idea_name = idea_format_00013_itemunit_v0_0_0()
    itemunit_format = create_idea_df(sue_budunit, x_idea_name)

    # THEN
    array_headers = list(itemunit_format.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()

    assert itemunit_format.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert itemunit_format.loc[0, pledge_str()] == ""
    assert itemunit_format.loc[0, fisc_title_str()] == accord_fisc_title
    assert itemunit_format.loc[0, item_title_str()] == casa_str
    assert itemunit_format.loc[0, mass_str()] == casa_mass
    assert itemunit_format.loc[0, parent_road_str()] == accord_fisc_title

    assert itemunit_format.loc[1, owner_name_str()] == sue_budunit.owner_name
    assert itemunit_format.loc[1, pledge_str()] == "Yes"
    assert itemunit_format.loc[1, fisc_title_str()] == accord_fisc_title
    assert itemunit_format.loc[1, parent_road_str()] == casa_road
    assert itemunit_format.loc[1, item_title_str()] == clean_str
    assert itemunit_format.loc[1, mass_str()] == 1
    assert len(itemunit_format) == 2


def test_save_idea_csv_Arg_idea_format_00019_itemunit_v0_0_0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue", "accord56")
    sue_budunit = add_time_creg_itemunit(sue_budunit)
    sue_budunit = add_time_five_itemunit(sue_budunit)
    x_idea_name = idea_format_00019_itemunit_v0_0_0()

    # WHEN
    # name_filename = f"{sue_str}_itemunit_example_00019.csv"
    # csv_example_path = create_path(idea_fiscs_dir(), name_filename)
    # save_idea_csv(x_idea_name, sue_budunit, idea_examples_dir(), name_filename)
    idea_df = create_idea_df(sue_budunit, x_idea_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_idea_format_00021_bud_acctunit_v0_0_0_SaveToCSV(
    idea_env_setup_cleanup,
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
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
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
    sue1_name_example_csv = """face_name,event_int,fisc_title,owner_name,acct_name,credit_belief,debtit_belief
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
    sue2_acct_example_csv = """face_name,event_int,fisc_title,owner_name,acct_name,credit_belief,debtit_belief
,,accord56,Sue,Bob,13,29
,,accord56,Sue,Sue,11,23
,,accord56,Sue,Yao,41,37
,,accord56,Sue,Zia,1,1
"""
    assert open_file(idea_fiscs_dir(), name_filename) == sue2_acct_example_csv


def test_save_idea_csv_Arg_idea_format_00013_itemunit_v0_0_0(idea_env_setup_cleanup):
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
    itemunit_format = create_idea_df(sue_budunit, x_idea_name)
    name_filename = f"{sue_str}_itemunit_example_000.csv"
    csv_example_path = create_path(idea_fiscs_dir(), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_idea_name, sue_budunit, idea_fiscs_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
