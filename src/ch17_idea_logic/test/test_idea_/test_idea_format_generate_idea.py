from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import beliefunit_v001
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch17_idea_logic._ref.ch17_keywords import Ch17Keywords as wx
from src.ch17_idea_logic.idea_config import (
    idea_format_00013_planunit_v0_0_0,
    idea_format_00021_belief_voiceunit_v0_0_0,
)
from src.ch17_idea_logic.idea_main import (
    create_idea_df,
    get_idearef_obj,
    make_beliefdelta,
)


def test_make_beliefdelta_Arg_idea_format_00021_belief_voiceunit_v0_0_0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_voice_cred_points = 11
    bob_voice_cred_points = 13
    yao_voice_cred_points = 41
    sue_voice_debt_points = 23
    bob_voice_debt_points = 29
    yao_voice_debt_points = 37
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    sue_beliefunit.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)
    sue_beliefunit.add_voiceunit(bob_str, bob_voice_cred_points, bob_voice_debt_points)
    sue_beliefunit.add_voiceunit(yao_str, yao_voice_cred_points, yao_voice_debt_points)
    x_idea_name = idea_format_00021_belief_voiceunit_v0_0_0()
    voice_dataframe = create_idea_df(sue_beliefunit, x_idea_name)
    print(f"{voice_dataframe.columns=}")
    voice_csv = voice_dataframe.to_csv(index=False)

    # WHEN
    sue_voice_beliefdelta = make_beliefdelta(voice_csv)

    # THEN
    assert sue_voice_beliefdelta
    sue_beliefatom = beliefatom_shop(wx.belief_voiceunit, wx.INSERT)
    sue_beliefatom.set_arg(wx.voice_name, sue_str)
    sue_beliefatom.set_arg(wx.voice_cred_points, sue_voice_cred_points)
    sue_beliefatom.set_arg(wx.voice_debt_points, sue_voice_debt_points)
    sue_beliefatom.set_atom_order()
    bob_beliefatom = beliefatom_shop(wx.belief_voiceunit, wx.INSERT)
    bob_beliefatom.set_arg(wx.voice_name, bob_str)
    bob_beliefatom.set_arg(wx.voice_cred_points, bob_voice_cred_points)
    bob_beliefatom.set_arg(wx.voice_debt_points, bob_voice_debt_points)
    bob_beliefatom.set_atom_order()
    # print(f"{sue_voice_beliefdelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_voice_beliefdelta.beliefatoms.get(wx.INSERT).get(wx.belief_voiceunit).get(sue_str)=}"
    # )
    print(f"{sue_beliefatom=}")
    assert sue_voice_beliefdelta.beliefatom_exists(sue_beliefatom)
    assert sue_voice_beliefdelta.beliefatom_exists(bob_beliefatom)
    assert len(sue_voice_beliefdelta.get_ordered_beliefatoms()) == 3


# def test_make_beliefdelta_Arg_idea_format_00020_belief_voice_membership_v0_0_0():
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     amy_moment_label = "amy56"
#     sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
#     sue_beliefunit.add_voiceunit(sue_str)
#     sue_beliefunit.add_voiceunit(bob_str)
#     sue_beliefunit.add_voiceunit(yao_str)
#     iowa_str = ";Iowa"
#     sue_iowa_group_cred_points = 37
#     bob_iowa_group_cred_points = 43
#     yao_iowa_group_cred_points = 51
#     sue_iowa_group_debt_points = 57
#     bob_iowa_group_debt_points = 61
#     yao_iowa_group_debt_points = 67
#     ohio_str = ";Ohio"
#     yao_ohio_group_cred_points = 73
#     yao_ohio_group_debt_points = 67
#     sue_voiceunit = sue_beliefunit.get_voice(sue_str)
#     bob_voiceunit = sue_beliefunit.get_voice(bob_str)
#     yao_voiceunit = sue_beliefunit.get_voice(yao_str)
#     sue_voiceunit.add_membership(iowa_str, sue_iowa_group_cred_points, sue_iowa_group_debt_points)
#     bob_voiceunit.add_membership(iowa_str, bob_iowa_group_cred_points, bob_iowa_group_debt_points)
#     yao_voiceunit.add_membership(iowa_str, yao_iowa_group_cred_points, yao_iowa_group_debt_points)
#     yao_voiceunit.add_membership(ohio_str, yao_ohio_group_cred_points, yao_ohio_group_debt_points)
#     x_idea_name = idea_format_00020_belief_voice_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_beliefunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_beliefdelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_beliefatom = beliefatom_shop(wx.belief_voice_membership, wx.INSERT)
#     bob_iowa_beliefatom = beliefatom_shop(wx.belief_voice_membership, wx.INSERT)
#     yao_iowa_beliefatom = beliefatom_shop(wx.belief_voice_membership, wx.INSERT)
#     yao_ohio_beliefatom = beliefatom_shop(wx.belief_voice_membership, wx.INSERT)
#     sue_iowa_beliefatom.set_arg(wx.group_title, iowa_str)
#     bob_iowa_beliefatom.set_arg(wx.group_title, iowa_str)
#     yao_iowa_beliefatom.set_arg(wx.group_title, iowa_str)
#     yao_ohio_beliefatom.set_arg(wx.group_title, ohio_str)
#     sue_iowa_beliefatom.set_arg(wx.voice_name, sue_str)
#     bob_iowa_beliefatom.set_arg(wx.voice_name, bob_str)
#     yao_iowa_beliefatom.set_arg(wx.voice_name, yao_str)
#     yao_ohio_beliefatom.set_arg(wx.voice_name, yao_str)
#     sue_iowa_beliefatom.set_arg(wx.group_cred_points, sue_iowa_group_cred_points)
#     bob_iowa_beliefatom.set_arg(wx.group_cred_points, bob_iowa_group_cred_points)
#     yao_iowa_beliefatom.set_arg(wx.group_cred_points, yao_iowa_group_cred_points)
#     yao_ohio_beliefatom.set_arg(wx.group_cred_points, yao_ohio_group_cred_points)
#     sue_iowa_beliefatom.set_arg(wx.group_debt_points, sue_iowa_group_debt_points)
#     bob_iowa_beliefatom.set_arg(wx.group_debt_points, bob_iowa_group_debt_points)
#     yao_iowa_beliefatom.set_arg(wx.group_debt_points, yao_iowa_group_debt_points)
#     yao_ohio_beliefatom.set_arg(wx.group_debt_points, yao_ohio_group_debt_points)
#     bob_iowa_beliefatom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_beliefatoms()[2]=}")
#     # print(f"{sue_iowa_beliefatom=}")
#     assert len(membership_changunit.get_ordered_beliefatoms()) == 10
#     assert membership_changunit.get_ordered_beliefatoms()[0] == bob_iowa_beliefatom
#     assert membership_changunit.beliefatom_exists(sue_iowa_beliefatom)
#     assert membership_changunit.beliefatom_exists(bob_iowa_beliefatom)
#     assert membership_changunit.beliefatom_exists(yao_iowa_beliefatom)
#     assert membership_changunit.beliefatom_exists(yao_ohio_beliefatom)
#     assert len(membership_changunit.get_ordered_beliefatoms()) == 10


def test_make_beliefdelta_Arg_idea_format_00013_planunit_v0_0_0():
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
    planunit_dataframe = create_idea_df(sue_beliefunit, x_idea_name)
    planunit_csv = planunit_dataframe.to_csv(index=False)

    # WHEN
    planunit_changunit = make_beliefdelta(planunit_csv)

    # THEN
    casa_beliefatom = beliefatom_shop(wx.belief_planunit, wx.INSERT)
    casa_beliefatom.set_arg(wx.plan_rope, casa_rope)
    casa_beliefatom.set_arg(wx.pledge, False)
    casa_beliefatom.set_arg(wx.star, casa_star)
    print(f"{casa_beliefatom=}")
    assert casa_beliefatom.get_value(wx.star) == casa_star
    clean_beliefatom = beliefatom_shop(wx.belief_planunit, wx.INSERT)
    clean_beliefatom.set_arg(wx.plan_rope, clean_rope)
    clean_beliefatom.set_arg(wx.pledge, True)
    clean_beliefatom.set_arg(wx.star, 1)
    assert planunit_changunit.beliefatom_exists(casa_beliefatom)
    assert planunit_changunit.beliefatom_exists(clean_beliefatom)
    assert len(planunit_changunit.get_ordered_beliefatoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_planunit_v0_0_0_Scenario_beliefunit_v001(
    run_big_tests,
):
    # sourcery skip: no-conditionals-in-tests
    if run_big_tests:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_planunit_v0_0_0()

        # WHEN
        planunit_format = create_idea_df(beliefunit_v001(), x_idea_name)

        # THEN
        array_headers = list(planunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(planunit_format) == 251
