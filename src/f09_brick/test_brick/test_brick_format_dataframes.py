from src.f00_instrument.file import open_file, create_path
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f03_chrono.examples.chrono_examples import (
    add_time_creg_itemunit,
    add_time_five_itemunit,
)
from src.f04_gift.atom_config import (
    deal_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    lx_str,
    mass_str,
    pledge_str,
    debtit_belief_str,
    credit_belief_str,
    debtit_vote_str,
    credit_vote_str,
)
from src.f09_brick.brick import create_brick_df, get_brickref_obj, save_brick_csv
from src.f09_brick.brick_config import (
    brick_format_00021_bud_acctunit_v0_0_0,
    brick_format_00020_bud_acct_membership_v0_0_0,
    brick_format_00013_itemunit_v0_0_0,
    brick_format_00019_itemunit_v0_0_0,
)
from src.f09_brick.examples.brick_env import (
    brick_examples_dir,
    brick_deals_dir,
    brick_env_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_create_brick_df_Arg_brick_format_00021_bud_acctunit_v0_0_0():
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
    accord_deal_id = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_deal_id)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)

    # WHEN
    x_brick_name = brick_format_00021_bud_acctunit_v0_0_0()
    acct_dataframe = create_brick_df(sue_budunit, x_brick_name)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_brickref = get_brickref_obj(x_brick_name)
    assert array_headers == acct_brickref.get_headers_list()
    assert acct_dataframe.loc[0, deal_id_str()] == accord_deal_id
    assert acct_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[0, acct_id_str()] == bob_str
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief

    assert acct_dataframe.loc[1, deal_id_str()] == accord_deal_id
    assert acct_dataframe.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[1, acct_id_str()] == sue_str
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief

    assert acct_dataframe.loc[2, deal_id_str()] == accord_deal_id
    assert acct_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[2, acct_id_str()] == yao_str
    assert acct_dataframe.loc[2, debtit_belief_str()] == yao_debtit_belief
    assert acct_dataframe.loc[2, credit_belief_str()] == yao_credit_belief

    assert len(acct_dataframe) == 3


def test_create_brick_df_Arg_brick_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    accord_deal_id = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_deal_id)
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
    x_brick_name = brick_format_00020_bud_acct_membership_v0_0_0()
    membership_dataframe = create_brick_df(sue_budunit, x_brick_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    acct_brickref = get_brickref_obj(x_brick_name)
    print(f"{len(membership_dataframe)=}")
    assert array_headers == acct_brickref.get_headers_list()
    assert membership_dataframe.loc[0, deal_id_str()] == accord_deal_id
    assert membership_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[0, acct_id_str()] == bob_str
    assert membership_dataframe.loc[0, group_id_str()] == iowa_str
    assert membership_dataframe.loc[0, credit_vote_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, debtit_vote_str()] == bob_iowa_debtit_w

    assert membership_dataframe.loc[2, deal_id_str()] == accord_deal_id
    assert membership_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[2, acct_id_str()] == sue_str
    assert membership_dataframe.loc[2, group_id_str()] == iowa_str
    assert membership_dataframe.loc[2, credit_vote_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[2, debtit_vote_str()] == sue_iowa_debtit_w

    assert membership_dataframe.loc[4, deal_id_str()] == accord_deal_id
    assert membership_dataframe.loc[4, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[4, acct_id_str()] == yao_str
    assert membership_dataframe.loc[4, group_id_str()] == iowa_str
    assert membership_dataframe.loc[4, credit_vote_str()] == yao_iowa_credit_w
    assert membership_dataframe.loc[4, debtit_vote_str()] == yao_iowa_debtit_w

    assert membership_dataframe.loc[5, deal_id_str()] == accord_deal_id
    assert membership_dataframe.loc[5, owner_id_str()] == sue_budunit._owner_id
    assert membership_dataframe.loc[5, acct_id_str()] == yao_str
    assert membership_dataframe.loc[5, group_id_str()] == ohio_str
    assert membership_dataframe.loc[5, credit_vote_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[5, debtit_vote_str()] == yao_ohio_debtit_w
    assert len(membership_dataframe) == 7


def test_create_brick_df_Arg_brick_format_00013_itemunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    accord_deal_id = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_deal_id)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_item(itemunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    sue_budunit.set_item(itemunit_shop(clean_str, pledge=True), casa_road)

    # WHEN
    x_brick_name = brick_format_00013_itemunit_v0_0_0()
    itemunit_format = create_brick_df(sue_budunit, x_brick_name)

    # THEN
    array_headers = list(itemunit_format.columns)
    assert array_headers == get_brickref_obj(x_brick_name).get_headers_list()

    assert itemunit_format.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert itemunit_format.loc[0, pledge_str()] == ""
    assert itemunit_format.loc[0, deal_id_str()] == accord_deal_id
    assert itemunit_format.loc[0, lx_str()] == casa_str
    assert itemunit_format.loc[0, mass_str()] == casa_mass
    assert itemunit_format.loc[0, parent_road_str()] == accord_deal_id

    assert itemunit_format.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert itemunit_format.loc[1, pledge_str()] == "Yes"
    assert itemunit_format.loc[1, deal_id_str()] == accord_deal_id
    assert itemunit_format.loc[1, parent_road_str()] == casa_road
    assert itemunit_format.loc[1, lx_str()] == clean_str
    assert itemunit_format.loc[1, mass_str()] == 1
    assert len(itemunit_format) == 2


def test_save_brick_csv_Arg_brick_format_00019_itemunit_v0_0_0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue", "accord56")
    sue_budunit = add_time_creg_itemunit(sue_budunit)
    sue_budunit = add_time_five_itemunit(sue_budunit)
    x_brick_name = brick_format_00019_itemunit_v0_0_0()

    # WHEN
    # acct_filename = f"{sue_str}_itemunit_example_00019.csv"
    # csv_example_path = create_path(brick_deals_dir(), acct_filename)
    # save_brick_csv(x_brick_name, sue_budunit, brick_examples_dir(), acct_filename)
    brick_df = create_brick_df(sue_budunit, x_brick_name)

    # THEN
    array_headers = list(brick_df.columns)
    assert array_headers == get_brickref_obj(x_brick_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_brick_csv_Arg_brick_format_00021_bud_acctunit_v0_0_0_SaveToCSV(
    brick_env_setup_cleanup,
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
    accord_deal_id = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_deal_id)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_brickname = brick_format_00021_bud_acctunit_v0_0_0()
    acct_filename = f"{sue_str}_acct_example_00.csv"
    csv_example_path = create_path(brick_deals_dir(), acct_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_brick_csv(j1_brickname, sue_budunit, brick_deals_dir(), acct_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_acct_example_csv = """face_id,event_id,deal_id,owner_id,acct_id,credit_belief,debtit_belief
,,accord56,Sue,Bob,13,29
,,accord56,Sue,Sue,11,23
,,accord56,Sue,Yao,41,37
"""
    brick_file_str = open_file(brick_deals_dir(), acct_filename)
    print(f"      {brick_file_str=}")
    print(f"{sue1_acct_example_csv=}")
    assert brick_file_str == sue1_acct_example_csv

    # WHEN
    zia_str = "Zia"
    sue_budunit.add_acctunit(zia_str)
    save_brick_csv(j1_brickname, sue_budunit, brick_deals_dir(), acct_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_acct_example_csv = """face_id,event_id,deal_id,owner_id,acct_id,credit_belief,debtit_belief
,,accord56,Sue,Bob,13,29
,,accord56,Sue,Sue,11,23
,,accord56,Sue,Yao,41,37
,,accord56,Sue,Zia,1,1
"""
    assert open_file(brick_deals_dir(), acct_filename) == sue2_acct_example_csv


def test_save_brick_csv_Arg_brick_format_00013_itemunit_v0_0_0(brick_env_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    accord_deal_id = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_deal_id)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_mass = 31
    sue_budunit.set_l1_item(itemunit_shop(casa_str, mass=casa_mass))
    clean_str = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    sue_budunit.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    x_brick_name = brick_format_00013_itemunit_v0_0_0()
    itemunit_format = create_brick_df(sue_budunit, x_brick_name)
    acct_filename = f"{sue_str}_itemunit_example_000.csv"
    csv_example_path = create_path(brick_deals_dir(), acct_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_brick_csv(x_brick_name, sue_budunit, brick_deals_dir(), acct_filename)

    # THEN
    assert os_path_exists(csv_example_path)
