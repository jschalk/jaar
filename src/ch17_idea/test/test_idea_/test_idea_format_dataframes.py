from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, open_file
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_epoch.test._util.ch08_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
)
from src.ch17_idea.idea_config import (
    idea_format_00013_planunit_v0_0_0,
    idea_format_00019_planunit_v0_0_0,
    idea_format_00020_belief_voice_membership_v0_0_0,
    idea_format_00021_belief_voiceunit_v0_0_0,
)
from src.ch17_idea.idea_main import create_idea_df, get_idearef_obj, save_idea_csv
from src.ch17_idea.test._util.ch17_env import env_dir_setup_cleanup, idea_moments_dir
from src.ref.keywords import Ch17Keywords as wx


def test_create_idea_df_Arg_idea_format_00021_belief_voiceunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_voice_cred_lumen = 11
    bob_voice_cred_lumen = 13
    yao_voice_cred_lumen = 41
    sue_voice_debt_lumen = 23
    bob_voice_debt_lumen = 29
    yao_voice_debt_lumen = 37
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    sue_beliefunit.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    sue_beliefunit.add_voiceunit(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    sue_beliefunit.add_voiceunit(yao_str, yao_voice_cred_lumen, yao_voice_debt_lumen)

    # WHEN
    x_idea_name = idea_format_00021_belief_voiceunit_v0_0_0()
    voice_dataframe = create_idea_df(sue_beliefunit, x_idea_name)

    # THEN
    array_headers = list(voice_dataframe.columns)
    voice_idearef = get_idearef_obj(x_idea_name)
    assert array_headers == voice_idearef.get_headers_list()
    assert voice_dataframe.loc[0, wx.moment_label] == amy_moment_label
    assert voice_dataframe.loc[0, wx.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[0, wx.voice_name] == bob_str
    assert voice_dataframe.loc[0, wx.voice_debt_lumen] == bob_voice_debt_lumen
    assert voice_dataframe.loc[0, wx.voice_cred_lumen] == bob_voice_cred_lumen

    assert voice_dataframe.loc[1, wx.moment_label] == amy_moment_label
    assert voice_dataframe.loc[1, wx.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[1, wx.voice_name] == sue_str
    assert voice_dataframe.loc[1, wx.voice_debt_lumen] == sue_voice_debt_lumen
    assert voice_dataframe.loc[1, wx.voice_cred_lumen] == sue_voice_cred_lumen

    assert voice_dataframe.loc[2, wx.moment_label] == amy_moment_label
    assert voice_dataframe.loc[2, wx.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[2, wx.voice_name] == yao_str
    assert voice_dataframe.loc[2, wx.voice_debt_lumen] == yao_voice_debt_lumen
    assert voice_dataframe.loc[2, wx.voice_cred_lumen] == yao_voice_cred_lumen

    assert len(voice_dataframe) == 3


def test_create_idea_df_Arg_idea_format_00020_belief_voice_membership_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    sue_beliefunit.add_voiceunit(sue_str)
    sue_beliefunit.add_voiceunit(bob_str)
    sue_beliefunit.add_voiceunit(yao_str)
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
    sue_voiceunit = sue_beliefunit.get_voice(sue_str)
    bob_voiceunit = sue_beliefunit.get_voice(bob_str)
    yao_voiceunit = sue_beliefunit.get_voice(yao_str)
    sue_voiceunit.add_membership(iowa_str, sue_iowa_credit_w, sue_iowa_debt_w)
    bob_voiceunit.add_membership(iowa_str, bob_iowa_credit_w, bob_iowa_debt_w)
    yao_voiceunit.add_membership(iowa_str, yao_iowa_credit_w, yao_iowa_debt_w)
    yao_voiceunit.add_membership(ohio_str, yao_ohio_credit_w, yao_ohio_debt_w)

    # WHEN
    x_idea_name = idea_format_00020_belief_voice_membership_v0_0_0()
    membership_dataframe = create_idea_df(sue_beliefunit, x_idea_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    voice_idearef = get_idearef_obj(x_idea_name)
    print(f"{len(membership_dataframe)=}")
    assert len(membership_dataframe) == 10
    assert array_headers == voice_idearef.get_headers_list()
    assert membership_dataframe.loc[0, wx.moment_label] == amy_moment_label
    assert membership_dataframe.loc[0, wx.belief_name] == sue_beliefunit.belief_name
    assert membership_dataframe.loc[0, wx.voice_name] == bob_str
    assert membership_dataframe.loc[0, wx.group_title] == iowa_str
    assert membership_dataframe.loc[0, wx.group_cred_lumen] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, wx.group_debt_lumen] == bob_iowa_debt_w

    assert membership_dataframe.loc[3, wx.moment_label] == amy_moment_label
    assert membership_dataframe.loc[3, wx.belief_name] == sue_beliefunit.belief_name
    assert membership_dataframe.loc[3, wx.voice_name] == sue_str
    assert membership_dataframe.loc[3, wx.group_title] == iowa_str
    assert membership_dataframe.loc[3, wx.group_cred_lumen] == sue_iowa_credit_w
    assert membership_dataframe.loc[3, wx.group_debt_lumen] == sue_iowa_debt_w

    assert membership_dataframe.loc[4, wx.moment_label] == amy_moment_label
    assert membership_dataframe.loc[4, wx.belief_name] == sue_beliefunit.belief_name
    assert membership_dataframe.loc[4, wx.voice_name] == sue_str
    assert membership_dataframe.loc[4, wx.group_title] == sue_str
    assert membership_dataframe.loc[4, wx.group_cred_lumen] == 1
    assert membership_dataframe.loc[4, wx.group_debt_lumen] == 1

    assert membership_dataframe.loc[7, wx.moment_label] == amy_moment_label
    assert membership_dataframe.loc[7, wx.belief_name] == sue_beliefunit.belief_name
    assert membership_dataframe.loc[7, wx.voice_name] == yao_str
    assert membership_dataframe.loc[7, wx.group_title] == ohio_str
    assert membership_dataframe.loc[7, wx.group_cred_lumen] == yao_ohio_credit_w
    assert membership_dataframe.loc[7, wx.group_debt_lumen] == yao_ohio_debt_w
    assert len(membership_dataframe) == 10


def test_create_idea_df_Arg_idea_format_00013_planunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    casa_star = 31
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str, star=casa_star))
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_plan(planunit_shop(clean_str, pledge=True), casa_rope)

    # WHEN
    x_idea_name = idea_format_00013_planunit_v0_0_0()
    planunit_format = create_idea_df(sue_beliefunit, x_idea_name)

    # THEN
    array_headers = list(planunit_format.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()

    assert planunit_format.loc[0, wx.belief_name] == sue_beliefunit.belief_name
    assert planunit_format.loc[0, wx.pledge] == ""
    assert planunit_format.loc[0, wx.moment_label] == amy_moment_label
    assert planunit_format.loc[0, wx.plan_rope] == casa_rope
    assert planunit_format.loc[0, wx.star] == casa_star

    assert planunit_format.loc[1, wx.belief_name] == sue_beliefunit.belief_name
    assert planunit_format.loc[1, wx.pledge] == "Yes"
    assert planunit_format.loc[1, wx.moment_label] == amy_moment_label
    assert planunit_format.loc[1, wx.plan_rope] == clean_rope
    assert planunit_format.loc[1, wx.star] == 1
    assert len(planunit_format) == 2


def test_save_idea_csv_Arg_idea_format_00019_planunit_v0_0_0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue", "amy56")
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    sue_beliefunit = add_time_five_planunit(sue_beliefunit)
    x_idea_name = idea_format_00019_planunit_v0_0_0()

    # WHEN
    # name_filename = f"{sue_str}_planunit_example_00019.csv"
    # csv_example_path = create_path(idea_moments_dir(), name_filename)
    # save_idea_csv(x_idea_name, sue_beliefunit, get_chapter_temp_dir(), name_filename)
    idea_df = create_idea_df(sue_beliefunit, x_idea_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_idea_format_00021_belief_voiceunit_v0_0_0_SaveToCSV(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_voice_cred_lumen = 11
    bob_voice_cred_lumen = 13
    yao_voice_cred_lumen = 41
    sue_voice_debt_lumen = 23
    bob_voice_debt_lumen = 29
    yao_voice_debt_lumen = 37
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    sue_beliefunit.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    sue_beliefunit.add_voiceunit(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    sue_beliefunit.add_voiceunit(yao_str, yao_voice_cred_lumen, yao_voice_debt_lumen)
    j1_ideaname = idea_format_00021_belief_voiceunit_v0_0_0()
    name_filename = f"{sue_str}_voice_example_00.csv"
    csv_example_path = create_path(idea_moments_dir(), name_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(j1_ideaname, sue_beliefunit, idea_moments_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_name_example_csv = """event_int,face_name,moment_label,belief_name,voice_name,voice_cred_lumen,voice_debt_lumen
,,amy56,Sue,Bob,13,29
,,amy56,Sue,Sue,11,23
,,amy56,Sue,Yao,41,37
"""
    idea_file_str = open_file(idea_moments_dir(), name_filename)
    print(f"      {idea_file_str=}")
    print(f"{sue1_name_example_csv=}")
    assert idea_file_str == sue1_name_example_csv

    # WHEN
    zia_str = "Zia"
    sue_beliefunit.add_voiceunit(zia_str)
    save_idea_csv(j1_ideaname, sue_beliefunit, idea_moments_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_voice_example_csv = """event_int,face_name,moment_label,belief_name,voice_name,voice_cred_lumen,voice_debt_lumen
,,amy56,Sue,Bob,13,29
,,amy56,Sue,Sue,11,23
,,amy56,Sue,Yao,41,37
,,amy56,Sue,Zia,1,1
"""
    assert open_file(idea_moments_dir(), name_filename) == sue2_voice_example_csv


def test_save_idea_csv_Arg_idea_format_00013_planunit_v0_0_0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    casa_star = 31
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str, star=casa_star))
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_plan(planunit_shop(clean_str, pledge=True), casa_rope)
    x_idea_name = idea_format_00013_planunit_v0_0_0()
    planunit_format = create_idea_df(sue_beliefunit, x_idea_name)
    name_filename = f"{sue_str}_planunit_example_000.csv"
    csv_example_path = create_path(idea_moments_dir(), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_idea_name, sue_beliefunit, idea_moments_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
