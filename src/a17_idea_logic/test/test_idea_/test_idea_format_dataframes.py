from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_name_str,
    coin_label_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    plan_rope_str,
    star_str,
    task_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
)
from src.a17_idea_logic.idea_config import (
    idea_format_00013_planunit_v0_0_0,
    idea_format_00019_planunit_v0_0_0,
    idea_format_00020_believer_partner_membership_v0_0_0,
    idea_format_00021_believer_partnerunit_v0_0_0,
)
from src.a17_idea_logic.idea_main import create_idea_df, get_idearef_obj, save_idea_csv
from src.a17_idea_logic.test._util.a17_env import env_dir_setup_cleanup, idea_coins_dir


def test_create_idea_df_Arg_idea_format_00021_believer_partnerunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_partner_cred_points = 11
    bob_partner_cred_points = 13
    yao_partner_cred_points = 41
    sue_partner_debt_points = 23
    bob_partner_debt_points = 29
    yao_partner_debt_points = 37
    amy_coin_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_coin_label)
    sue_believerunit.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        yao_str, yao_partner_cred_points, yao_partner_debt_points
    )

    # WHEN
    x_idea_name = idea_format_00021_believer_partnerunit_v0_0_0()
    partner_dataframe = create_idea_df(sue_believerunit, x_idea_name)

    # THEN
    array_headers = list(partner_dataframe.columns)
    partner_idearef = get_idearef_obj(x_idea_name)
    assert array_headers == partner_idearef.get_headers_list()
    assert partner_dataframe.loc[0, coin_label_str()] == amy_coin_label
    assert (
        partner_dataframe.loc[0, believer_name_str()] == sue_believerunit.believer_name
    )
    assert partner_dataframe.loc[0, partner_name_str()] == bob_str
    assert (
        partner_dataframe.loc[0, partner_debt_points_str()] == bob_partner_debt_points
    )
    assert (
        partner_dataframe.loc[0, partner_cred_points_str()] == bob_partner_cred_points
    )

    assert partner_dataframe.loc[1, coin_label_str()] == amy_coin_label
    assert (
        partner_dataframe.loc[1, believer_name_str()] == sue_believerunit.believer_name
    )
    assert partner_dataframe.loc[1, partner_name_str()] == sue_str
    assert (
        partner_dataframe.loc[1, partner_debt_points_str()] == sue_partner_debt_points
    )
    assert (
        partner_dataframe.loc[1, partner_cred_points_str()] == sue_partner_cred_points
    )

    assert partner_dataframe.loc[2, coin_label_str()] == amy_coin_label
    assert (
        partner_dataframe.loc[2, believer_name_str()] == sue_believerunit.believer_name
    )
    assert partner_dataframe.loc[2, partner_name_str()] == yao_str
    assert (
        partner_dataframe.loc[2, partner_debt_points_str()] == yao_partner_debt_points
    )
    assert (
        partner_dataframe.loc[2, partner_cred_points_str()] == yao_partner_cred_points
    )

    assert len(partner_dataframe) == 3


def test_create_idea_df_Arg_idea_format_00020_believer_partner_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    amy_coin_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_coin_label)
    sue_believerunit.add_partnerunit(sue_str)
    sue_believerunit.add_partnerunit(bob_str)
    sue_believerunit.add_partnerunit(yao_str)
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
    sue_partnerunit = sue_believerunit.get_partner(sue_str)
    bob_partnerunit = sue_believerunit.get_partner(bob_str)
    yao_partnerunit = sue_believerunit.get_partner(yao_str)
    sue_partnerunit.add_membership(iowa_str, sue_iowa_credit_w, sue_iowa_debt_w)
    bob_partnerunit.add_membership(iowa_str, bob_iowa_credit_w, bob_iowa_debt_w)
    yao_partnerunit.add_membership(iowa_str, yao_iowa_credit_w, yao_iowa_debt_w)
    yao_partnerunit.add_membership(ohio_str, yao_ohio_credit_w, yao_ohio_debt_w)

    # WHEN
    x_idea_name = idea_format_00020_believer_partner_membership_v0_0_0()
    membership_dataframe = create_idea_df(sue_believerunit, x_idea_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    partner_idearef = get_idearef_obj(x_idea_name)
    print(f"{len(membership_dataframe)=}")
    assert len(membership_dataframe) == 10
    assert array_headers == partner_idearef.get_headers_list()
    assert membership_dataframe.loc[0, coin_label_str()] == amy_coin_label
    assert (
        membership_dataframe.loc[0, believer_name_str()]
        == sue_believerunit.believer_name
    )
    assert membership_dataframe.loc[0, partner_name_str()] == bob_str
    assert membership_dataframe.loc[0, group_title_str()] == iowa_str
    assert membership_dataframe.loc[0, group_cred_points_str()] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, group_debt_points_str()] == bob_iowa_debt_w

    assert membership_dataframe.loc[3, coin_label_str()] == amy_coin_label
    assert (
        membership_dataframe.loc[3, believer_name_str()]
        == sue_believerunit.believer_name
    )
    assert membership_dataframe.loc[3, partner_name_str()] == sue_str
    assert membership_dataframe.loc[3, group_title_str()] == iowa_str
    assert membership_dataframe.loc[3, group_cred_points_str()] == sue_iowa_credit_w
    assert membership_dataframe.loc[3, group_debt_points_str()] == sue_iowa_debt_w

    assert membership_dataframe.loc[4, coin_label_str()] == amy_coin_label
    assert (
        membership_dataframe.loc[4, believer_name_str()]
        == sue_believerunit.believer_name
    )
    assert membership_dataframe.loc[4, partner_name_str()] == sue_str
    assert membership_dataframe.loc[4, group_title_str()] == sue_str
    assert membership_dataframe.loc[4, group_cred_points_str()] == 1
    assert membership_dataframe.loc[4, group_debt_points_str()] == 1

    assert membership_dataframe.loc[7, coin_label_str()] == amy_coin_label
    assert (
        membership_dataframe.loc[7, believer_name_str()]
        == sue_believerunit.believer_name
    )
    assert membership_dataframe.loc[7, partner_name_str()] == yao_str
    assert membership_dataframe.loc[7, group_title_str()] == ohio_str
    assert membership_dataframe.loc[7, group_cred_points_str()] == yao_ohio_credit_w
    assert membership_dataframe.loc[7, group_debt_points_str()] == yao_ohio_debt_w
    assert len(membership_dataframe) == 10


def test_create_idea_df_Arg_idea_format_00013_planunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    amy_coin_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_coin_label)
    casa_str = "casa"
    casa_rope = sue_believerunit.make_l1_rope(casa_str)
    casa_star = 31
    sue_believerunit.set_l1_plan(planunit_shop(casa_str, star=casa_star))
    clean_str = "clean"
    clean_rope = sue_believerunit.make_rope(casa_rope, clean_str)
    sue_believerunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)

    # WHEN
    x_idea_name = idea_format_00013_planunit_v0_0_0()
    planunit_format = create_idea_df(sue_believerunit, x_idea_name)

    # THEN
    array_headers = list(planunit_format.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()

    assert planunit_format.loc[0, believer_name_str()] == sue_believerunit.believer_name
    assert planunit_format.loc[0, task_str()] == ""
    assert planunit_format.loc[0, coin_label_str()] == amy_coin_label
    assert planunit_format.loc[0, plan_rope_str()] == casa_rope
    assert planunit_format.loc[0, star_str()] == casa_star

    assert planunit_format.loc[1, believer_name_str()] == sue_believerunit.believer_name
    assert planunit_format.loc[1, task_str()] == "Yes"
    assert planunit_format.loc[1, coin_label_str()] == amy_coin_label
    assert planunit_format.loc[1, plan_rope_str()] == clean_rope
    assert planunit_format.loc[1, star_str()] == 1
    assert len(planunit_format) == 2


def test_save_idea_csv_Arg_idea_format_00019_planunit_v0_0_0():
    # ESTABLISH
    sue_believerunit = believerunit_shop("Sue", "amy56")
    sue_believerunit = add_time_creg_planunit(sue_believerunit)
    sue_believerunit = add_time_five_planunit(sue_believerunit)
    x_idea_name = idea_format_00019_planunit_v0_0_0()

    # WHEN
    # name_filename = f"{sue_str}_planunit_example_00019.csv"
    # csv_example_path = create_path(idea_coins_dir(), name_filename)
    # save_idea_csv(x_idea_name, sue_believerunit, get_module_temp_dir(), name_filename)
    idea_df = create_idea_df(sue_believerunit, x_idea_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_idea_format_00021_believer_partnerunit_v0_0_0_SaveToCSV(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_partner_cred_points = 11
    bob_partner_cred_points = 13
    yao_partner_cred_points = 41
    sue_partner_debt_points = 23
    bob_partner_debt_points = 29
    yao_partner_debt_points = 37
    amy_coin_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_coin_label)
    sue_believerunit.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        yao_str, yao_partner_cred_points, yao_partner_debt_points
    )
    j1_ideaname = idea_format_00021_believer_partnerunit_v0_0_0()
    name_filename = f"{sue_str}_partner_example_00.csv"
    csv_example_path = create_path(idea_coins_dir(), name_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(j1_ideaname, sue_believerunit, idea_coins_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_name_example_csv = """event_int,face_name,coin_label,believer_name,partner_name,partner_cred_points,partner_debt_points
,,amy56,Sue,Bob,13,29
,,amy56,Sue,Sue,11,23
,,amy56,Sue,Yao,41,37
"""
    idea_file_str = open_file(idea_coins_dir(), name_filename)
    print(f"      {idea_file_str=}")
    print(f"{sue1_name_example_csv=}")
    assert idea_file_str == sue1_name_example_csv

    # WHEN
    zia_str = "Zia"
    sue_believerunit.add_partnerunit(zia_str)
    save_idea_csv(j1_ideaname, sue_believerunit, idea_coins_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_partner_example_csv = """event_int,face_name,coin_label,believer_name,partner_name,partner_cred_points,partner_debt_points
,,amy56,Sue,Bob,13,29
,,amy56,Sue,Sue,11,23
,,amy56,Sue,Yao,41,37
,,amy56,Sue,Zia,1,1
"""
    assert open_file(idea_coins_dir(), name_filename) == sue2_partner_example_csv


def test_save_idea_csv_Arg_idea_format_00013_planunit_v0_0_0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    amy_coin_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_coin_label)
    casa_str = "casa"
    casa_rope = sue_believerunit.make_l1_rope(casa_str)
    casa_star = 31
    sue_believerunit.set_l1_plan(planunit_shop(casa_str, star=casa_star))
    clean_str = "clean"
    clean_rope = sue_believerunit.make_rope(casa_rope, clean_str)
    sue_believerunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    x_idea_name = idea_format_00013_planunit_v0_0_0()
    planunit_format = create_idea_df(sue_believerunit, x_idea_name)
    name_filename = f"{sue_str}_planunit_example_000.csv"
    csv_example_path = create_path(idea_coins_dir(), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_idea_name, sue_believerunit, idea_coins_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
