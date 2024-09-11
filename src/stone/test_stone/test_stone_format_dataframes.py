from src._instrument.file import open_file, create_file_path
from src._road.jaar_refer import sue_str, bob_str, yao_str
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.chrono.examples.chrono_examples import (
    add_time_creg_ideaunit,
    add_time_five_ideaunit,
)
from src.change.atom_config import (
    tribe_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    mass_str,
    pledge_str,
    debtit_belief_str,
    credit_belief_str,
    debtit_vote_str,
    credit_vote_str,
)
from src.stone.stone import create_stone_df, get_stoneref, save_stone_csv
from src.stone.stone_config import (
    stone_format_00021_bud_acctunit_v0_0_0,
    stone_format_00020_bud_acct_membership_v0_0_0,
    stone_format_00003_ideaunit_v0_0_0,
    stone_format_00019_ideaunit_v0_0_0,
)
from src.stone.examples.stone_env import (
    stone_examples_dir,
    stone_tribes_dir,
    stone_env_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_create_stone_df_Arg_stone_format_00021_bud_acctunit_v0_0_0():
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
    music_tribe_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_tribe_id)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)

    # WHEN
    x_stone_name = stone_format_00021_bud_acctunit_v0_0_0()
    acct_dataframe = create_stone_df(sue_budunit, x_stone_name)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_stoneref = get_stoneref(x_stone_name)
    assert array_headers == acct_stoneref.get_headers_list()
    assert acct_dataframe.loc[0, tribe_id_str()] == music_tribe_id
    assert acct_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[0, acct_id_str()] == bob_str
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief

    assert acct_dataframe.loc[1, tribe_id_str()] == music_tribe_id
    assert acct_dataframe.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[1, acct_id_str()] == sue_str
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief

    assert acct_dataframe.loc[2, tribe_id_str()] == music_tribe_id
    assert acct_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[2, acct_id_str()] == yao_str
    assert acct_dataframe.loc[2, debtit_belief_str()] == yao_debtit_belief
    assert acct_dataframe.loc[2, credit_belief_str()] == yao_credit_belief

    assert len(acct_dataframe) == 3


def test_create_stone_df_Arg_stone_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    music_tribe_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_tribe_id)
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
    x_stone_name = stone_format_00020_bud_acct_membership_v0_0_0()
    membership_dataframe = create_stone_df(sue_budunit, x_stone_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    acct_stoneref = get_stoneref(x_stone_name)
    print(f"{len(membership_dataframe)=}")
    assert array_headers == acct_stoneref.get_headers_list()
    assert membership_dataframe.loc[0, tribe_id_str()] == music_tribe_id
    assert membership_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[0, acct_id_str()] == bob_str
    assert membership_dataframe.loc[0, group_id_str()] == iowa_str
    assert membership_dataframe.loc[0, credit_vote_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, debtit_vote_str()] == bob_iowa_debtit_w

    assert membership_dataframe.loc[2, tribe_id_str()] == music_tribe_id
    assert membership_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[2, acct_id_str()] == sue_str
    assert membership_dataframe.loc[2, group_id_str()] == iowa_str
    assert membership_dataframe.loc[2, credit_vote_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[2, debtit_vote_str()] == sue_iowa_debtit_w

    assert membership_dataframe.loc[4, tribe_id_str()] == music_tribe_id
    assert membership_dataframe.loc[4, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[4, acct_id_str()] == yao_str
    assert membership_dataframe.loc[4, group_id_str()] == iowa_str
    assert membership_dataframe.loc[4, credit_vote_str()] == yao_iowa_credit_w
    assert membership_dataframe.loc[4, debtit_vote_str()] == yao_iowa_debtit_w

    assert membership_dataframe.loc[5, tribe_id_str()] == music_tribe_id
    assert membership_dataframe.loc[5, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[5, acct_id_str()] == yao_str
    assert membership_dataframe.loc[5, group_id_str()] == ohio_str
    assert membership_dataframe.loc[5, credit_vote_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[5, debtit_vote_str()] == yao_ohio_debtit_w
    assert len(membership_dataframe) == 7


def test_create_stone_df_Arg_stone_format_00003_ideaunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    music_tribe_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_tribe_id)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_idea(ideaunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    sue_budunit.set_idea(ideaunit_shop(clean_str, pledge=True), casa_road)

    # WHEN
    x_stone_name = stone_format_00003_ideaunit_v0_0_0()
    ideaunit_format = create_stone_df(sue_budunit, x_stone_name)

    # THEN
    array_headers = list(ideaunit_format.columns)
    assert array_headers == get_stoneref(x_stone_name).get_headers_list()

    assert ideaunit_format.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert ideaunit_format.loc[0, pledge_str()] == ""
    assert ideaunit_format.loc[0, tribe_id_str()] == music_tribe_id
    assert ideaunit_format.loc[0, label_str()] == casa_str
    assert ideaunit_format.loc[0, mass_str()] == casa_mass
    assert ideaunit_format.loc[0, parent_road_str()] == music_tribe_id

    assert ideaunit_format.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert ideaunit_format.loc[1, pledge_str()] == "Yes"
    assert ideaunit_format.loc[1, tribe_id_str()] == music_tribe_id
    assert ideaunit_format.loc[1, parent_road_str()] == casa_road
    assert ideaunit_format.loc[1, label_str()] == clean_str
    assert ideaunit_format.loc[1, mass_str()] == 1
    assert len(ideaunit_format) == 2


# Commented out to reduce testing time.
# def test_create_stone_df_Arg_stone_format_00003_ideaunit_v0_0_0_Scenario_budunit_v001():
#     # ESTABLISH / WHEN
#     x_stone_name = stone_format_00003_ideaunit_v0_0_0()

#     # WHEN
#     ideaunit_format = create_stone_df(budunit_v001(), x_stone_name)

#     # THEN
#     array_headers = list(ideaunit_format.columns)
#     assert array_headers == get_stoneref(x_stone_name).get_headers_list()
#     assert len(ideaunit_format) == 252


def test_save_stone_csv_Arg_stone_format_00019_ideaunit_v0_0_0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue", "music56")
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    sue_budunit = add_time_five_ideaunit(sue_budunit)
    x_stone_name = stone_format_00019_ideaunit_v0_0_0()

    # WHEN
    # acct_filename = f"{sue_str}_ideaunit_example_00019.csv"
    # csv_example_path = create_file_path(stone_tribes_dir(), acct_filename)
    # save_stone_csv(x_stone_name, sue_budunit, stone_examples_dir(), acct_filename)
    stone_df = create_stone_df(sue_budunit, x_stone_name)

    # THEN
    array_headers = list(stone_df.columns)
    assert array_headers == get_stoneref(x_stone_name).get_headers_list()
    for x_array_header in array_headers:
        print(f"{x_array_header=}")


def test_save_stone_csv_Arg_stone_format_00021_bud_acctunit_v0_0_0_SaveToCSV(
    stone_env_setup_cleanup,
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
    music_tribe_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_tribe_id)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_stonename = stone_format_00021_bud_acctunit_v0_0_0()
    acct_filename = f"{sue_str}_acct_example_00.csv"
    csv_example_path = create_file_path(stone_tribes_dir(), acct_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_stone_csv(j1_stonename, sue_budunit, stone_tribes_dir(), acct_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_acct_example_csv = """tribe_id,owner_id,acct_id,debtit_belief,credit_belief
music56,Sue,Bob,29,13
music56,Sue,Sue,23,11
music56,Sue,Yao,37,41
"""
    stone_file_str = open_file(stone_tribes_dir(), acct_filename)
    print(f"      {stone_file_str=}")
    print(f"{sue1_acct_example_csv=}")
    assert stone_file_str == sue1_acct_example_csv

    # WHEN
    zia_str = "Zia"
    sue_budunit.add_acctunit(zia_str)
    save_stone_csv(j1_stonename, sue_budunit, stone_tribes_dir(), acct_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_acct_example_csv = """tribe_id,owner_id,acct_id,debtit_belief,credit_belief
music56,Sue,Bob,29,13
music56,Sue,Sue,23,11
music56,Sue,Yao,37,41
music56,Sue,Zia,1,1
"""
    assert open_file(stone_tribes_dir(), acct_filename) == sue2_acct_example_csv


def test_save_stone_csv_Arg_stone_format_00003_ideaunit_v0_0_0(stone_env_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    music_tribe_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_tribe_id)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_idea(ideaunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    sue_budunit.set_idea(ideaunit_shop(clean_str, pledge=True), casa_road)
    x_stone_name = stone_format_00003_ideaunit_v0_0_0()
    ideaunit_format = create_stone_df(sue_budunit, x_stone_name)
    acct_filename = f"{sue_str}_ideaunit_example_000.csv"
    csv_example_path = create_file_path(stone_tribes_dir(), acct_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_stone_csv(x_stone_name, sue_budunit, stone_tribes_dir(), acct_filename)

    # THEN
    assert os_path_exists(csv_example_path)
