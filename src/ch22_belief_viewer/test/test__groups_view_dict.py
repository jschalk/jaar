from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch22_belief_viewer._ref.ch22_keywords import Ch22Keywords as wx
from src.ch22_belief_viewer.belief_viewer__tool import (
    add_small_dot,
    get_groups_view_dict,
)
from src.ch22_belief_viewer.example22_beliefs import (
    best_run_str,
    best_soccer_str,
    best_sport_str,
    best_swim_str,
    get_beliefunit_irrational_example,
    get_sue_belief_with_facts_and_reasons,
    get_sue_beliefunit,
    play_run_str,
    play_soccer_str,
    play_str,
    play_swim_str,
)
from src.ch22_belief_viewer.test.test__voices_view_dict import add_readable


def test_get_groups_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    sue_believer.cashout()

    # WHEN
    groups_view_dict = get_groups_view_dict(sue_believer)

    # THEN
    assert groups_view_dict == {}


# def test_get_groups_view_dict_ReturnsObj_Scenario1_groups():
#     # ESTABLISH
#     sue_str = "Sue"
#     sue_believer = beliefunit_shop(sue_str)
#     yao_str = "Yao"
#     bob_str = "Bob"
#     yao_cred_points = 110
#     yao_debt_points = 130
#     bob_cred_points = 230
#     bob_debt_points = 290
#     sue_believer.add_voiceunit(yao_str, yao_cred_points, yao_debt_points)
#     sue_believer.add_voiceunit(bob_str, bob_cred_points, bob_debt_points)
#     swim_str = ";swimmers"
#     bob_swim_cred_points = 66
#     bob_swim_debt_points = 77
#     yao_swim_cred_points = 88
#     yao_swim_debt_points = 99
#     yao_voice = sue_believer.get_voice(yao_str)
#     bob_voice = sue_believer.get_voice(bob_str)
#     yao_voice.add_membership(swim_str, yao_swim_cred_points, yao_swim_debt_points)
#     bob_voice.add_membership(swim_str, bob_swim_cred_points, bob_swim_debt_points)
#     sue_believer.cashout()

#     # WHEN
#     groups_view_dict = get_groups_view_dict(sue_believer)

#     # THEN
#     assert set(groups_view_dict.keys()) == {yao_str, bob_str, swim_str}

#     swim_group_dict = groups_view_dict.get(swim_str)
#     group_title_readable_key = add_readable(wx.group_title)
#     memberships_readable_key = add_readable(wx.memberships)
#     fund_give_readable_key = add_readable(wx.fund_give)
#     fund_take_readable_key = add_readable(wx.fund_take)
#     fund_agenda_give_readable_key = add_readable(wx.fund_agenda_give)
#     fund_agenda_take_readable_key = add_readable(wx.fund_agenda_take)
#     credor_pool_readable_key = add_readable(wx.credor_pool)
#     debtor_pool_readable_key = add_readable(wx.debtor_pool)
#     assert set(swim_group_dict.keys()) == {
#         wx.group_title,
#         wx.memberships,
#         wx.fund_give,
#         wx.fund_take,
#         wx.fund_agenda_give,
#         wx.fund_agenda_take,
#         wx.credor_pool,
#         wx.debtor_pool,
#         group_title_readable_key,
#         memberships_readable_key,
#         fund_give_readable_key,
#         fund_take_readable_key,
#         fund_agenda_give_readable_key,
#         fund_agenda_take_readable_key,
#         credor_pool_readable_key,
#         debtor_pool_readable_key,
#     }

#     swim_groupunit = sue_believer.get_groupunit(swim_str)
#     swim_group_title_readable = f"group_title_readable: {swim_groupunit.group_title}"
#     swim_memberships_readable = f"memberships_readable: {swim_groupunit.memberships}"
#     swim_fund_give_readable = f"fund_give_readable: {swim_groupunit.fund_give}"
#     swim_fund_take_readable = f"fund_take_readable: {swim_groupunit.fund_take}"
#     swim_fund_agenda_give_readable = (
#         f"fund_agenda_give_readable: {swim_groupunit.fund_agenda_give}"
#     )
#     swim_fund_agenda_take_readable = (
#         f"fund_agenda_take_readable: {swim_groupunit.fund_agenda_take}"
#     )
#     swim_credor_pool_readable = f"credor_pool_readable: {swim_groupunit.credor_pool}"
#     swim_debtor_pool_readable = f"debtor_pool_readable: {swim_groupunit.debtor_pool}"

#     sgu = swim_groupunit
#     sg_dict = swim_group_dict
#     assert sgu.group_title == sg_dict.get(wx.group_title)
#     assert sgu.memberships == sg_dict.get(wx.memberships)
#     assert sgu.fund_give == sg_dict.get(wx.fund_give)
#     assert sgu.fund_take == sg_dict.get(wx.fund_take)
#     assert sgu.fund_agenda_give == sg_dict.get(wx.fund_agenda_give)
#     assert sgu.fund_agenda_take == sg_dict.get(wx.fund_agenda_take)
#     assert sgu.credor_pool == sg_dict.get(wx.credor_pool)
#     assert sgu.debtor_pool == sg_dict.get(wx.debtor_pool)
#     assert swim_group_title_readable == sg_dict.get(group_title_readable_key)
#     assert swim_memberships_readable == sg_dict.get(memberships_readable_key)
#     assert swim_fund_give_readable == sg_dict.get(fund_give_readable_key)
#     assert swim_fund_take_readable == sg_dict.get(fund_take_readable_key)
#     assert swim_fund_agenda_give_readable == sg_dict.get(fund_agenda_give_readable_key)
#     assert swim_fund_agenda_take_readable == sg_dict.get(fund_agenda_take_readable_key)
#     assert swim_credor_pool_readable == sg_dict.get(credor_pool_readable_key)
#     assert swim_debtor_pool_readable == sg_dict.get(debtor_pool_readable_key)

#     assert 1 == 2


# def test_get_groups_view_dict_ReturnsObj_Scenario2_memberships():
#     # ESTABLISH
#     sue_str = "Sue"
#     sue_believer = beliefunit_shop(sue_str)
#     yao_str = "Yao"
#     sue_believer.add_voiceunit(yao_str)
#     swim_str = ";swimmers"
#     yao_swim_cred_points = 311
#     yao_swim_debt_points = 313
#     yao_voiceunit = sue_believer.get_voice(yao_str)
#     yao_voiceunit.add_membership(swim_str, yao_swim_cred_points, yao_swim_debt_points)
#     sue_believer.cashout()

#     # WHEN
#     groups_view_dict = get_groups_view_dict(sue_believer)

#     # THEN
#     assert set(groups_view_dict.keys()) == {yao_str}
#     yao_voice_dict = groups_view_dict.get(yao_str)
#     assert wx.memberships in set(yao_voice_dict.keys())
#     yao_memberships_dict = yao_voice_dict.get(wx.memberships)
#     assert {swim_str, yao_str} == set(yao_memberships_dict.keys())
#     yao_swim_dict = yao_memberships_dict.get(swim_str)

#     group_title_readable_key = add_readable(wx.group_title)
#     group_cred_points_readable_key = add_readable(wx.group_cred_points)
#     group_debt_points_readable_key = add_readable(wx.group_debt_points)
#     credor_pool_readable_key = add_readable(wx.credor_pool)
#     debtor_pool_readable_key = add_readable(wx.debtor_pool)
#     fund_agenda_give_readable_key = add_readable(wx.fund_agenda_give)
#     fund_agenda_ratio_give_readable_key = add_readable(wx.fund_agenda_ratio_give)
#     fund_agenda_ratio_take_readable_key = add_readable(wx.fund_agenda_ratio_take)
#     fund_agenda_take_readable_key = add_readable(wx.fund_agenda_take)
#     fund_give_readable_key = add_readable(wx.fund_give)
#     fund_take_readable_key = add_readable(wx.fund_take)
#     assert set(yao_swim_dict.keys()) == {
#         wx.voice_name,
#        wx.group_title,
#        wx.group_cred_points,
#        wx.group_debt_points,
#         wx.credor_pool,
#         wx.debtor_pool,
#         wx.fund_agenda_give,
#         wx.fund_agenda_ratio_give,
#         wx.fund_agenda_ratio_take,
#         wx.fund_agenda_take,
#         wx.fund_give,
#         wx.fund_take,
#         group_title_readable_key,
#         group_cred_points_readable_key,
#         group_debt_points_readable_key,
#         credor_pool_readable_key,
#         debtor_pool_readable_key,
#         fund_agenda_give_readable_key,
#         fund_agenda_ratio_give_readable_key,
#         fund_agenda_ratio_take_readable_key,
#         fund_agenda_take_readable_key,
#         fund_give_readable_key,
#         fund_take_readable_key,
#     }
#     yao_swim_mu = yao_voiceunit.get_membership(swim_str)
#     expected_group_title_readable = f"{wx.group_title}: {yao_swim_mu.group_title}"
#     expected_group_cred_points_readable = (
#         f"{wx.group_cred_points}: {yao_swim_mu.group_cred_points}"
#     )
#     expected_group_debt_points_readable = (
#         f"{wx.group_debt_points}: {yao_swim_mu.group_debt_points}"
#     )
#     expected_credor_pool_readable = f"{wx.credor_pool}: {yao_swim_mu.credor_pool}"
#     expected_debtor_pool_readable = f"{wx.debtor_pool}: {yao_swim_mu.debtor_pool}"
#     expected_fund_agenda_give_readable = (
#         f"{wx.fund_agenda_give}: {yao_swim_mu.fund_agenda_give}"
#     )
#     expected_fund_agenda_ratio_give_readable = (
#         f"{wx.fund_agenda_ratio_give}: {yao_swim_mu.fund_agenda_ratio_give}"
#     )
#     expected_fund_agenda_ratio_take_readable = (
#         f"{wx.fund_agenda_ratio_take}: {yao_swim_mu.fund_agenda_ratio_take}"
#     )
#     expected_fund_agenda_take_readable = (
#         f"{wx.fund_agenda_take}: {yao_swim_mu.fund_agenda_take}"
#     )
#     expected_fund_give_readable = f"{wx.fund_give}: {yao_swim_mu.fund_give}"
#     expected_fund_take_readable = f"{wx.fund_take}: {yao_swim_mu.fund_take}"

#     assert yao_swim_dict.get(wx.voice_name) == yao_swim_mu.voice_name
#     assert yao_swim_dict.get(wx.group_title) == yao_swim_mu.group_title
#     assert yao_swim_dict.get(wx.group_cred_points) == yao_swim_mu.group_cred_points
#     assert yao_swim_dict.get(wx.group_debt_points) == yao_swim_mu.group_debt_points
#     assert yao_swim_dict.get(wx.credor_pool) == yao_swim_mu.credor_pool
#     assert yao_swim_dict.get(wx.debtor_pool) == yao_swim_mu.debtor_pool
#     assert yao_swim_dict.get(wx.fund_agenda_give) == yao_swim_mu.fund_agenda_give
#     assert (
#         yao_swim_dict.get(wx.fund_agenda_ratio_give)
#         == yao_swim_mu.fund_agenda_ratio_give
#     )
#     assert (
#         yao_swim_dict.get(wx.fund_agenda_ratio_take)
#         == yao_swim_mu.fund_agenda_ratio_take
#     )
#     assert yao_swim_dict.get(wx.fund_agenda_take) == yao_swim_mu.fund_agenda_take
#     assert yao_swim_dict.get(wx.fund_give) == yao_swim_mu.fund_give
#     assert yao_swim_dict.get(wx.fund_take) == yao_swim_mu.fund_take
#     assert yao_swim_dict.get(group_title_readable_key) == expected_group_title_readable
#     assert (
#         yao_swim_dict.get(group_cred_points_readable_key)
#         == expected_group_cred_points_readable
#     )
#     assert (
#         yao_swim_dict.get(group_debt_points_readable_key)
#         == expected_group_debt_points_readable
#     )
#     assert (
#         yao_swim_dict.get(credor_pool_readable_key) == expected_credor_pool_readable
#     )
#     assert (
#         yao_swim_dict.get(debtor_pool_readable_key) == expected_debtor_pool_readable
#     )
#     assert (
#         yao_swim_dict.get(fund_agenda_give_readable_key)
#         == expected_fund_agenda_give_readable
#     )
#     assert (
#         yao_swim_dict.get(fund_agenda_ratio_give_readable_key)
#         == expected_fund_agenda_ratio_give_readable
#     )
#     assert (
#         yao_swim_dict.get(fund_agenda_ratio_take_readable_key)
#         == expected_fund_agenda_ratio_take_readable
#     )
#     assert (
#         yao_swim_dict.get(fund_agenda_take_readable_key)
#         == expected_fund_agenda_take_readable
#     )
#     assert yao_swim_dict.get(fund_give_readable_key) == expected_fund_give_readable
#     assert yao_swim_dict.get(fund_take_readable_key) == expected_fund_take_readable

#     # sue_str = "Sue"
#     # sue_believer = beliefunit_shop(sue_str)
#     # yao_str = "Yao"
#     # bob_str = "Bob"
#     # yao_cred_points = 110
#     # yao_debt_points = 130
#     # bob_cred_points = 230
#     # bob_debt_points = 290
#     # sue_believer.add_voiceunit(yao_str, yao_cred_points, yao_debt_points)
#     # sue_believer.add_voiceunit(bob_str, bob_cred_points, bob_debt_points)
#     # swim_str = ";swimmers"
#     # yao_swim_cred_points = 311
#     # yao_swim_debt_points = 313
#     # bob_swim_cred_points = 411
#     # bob_swim_debt_points = 413
#     # clea_str = ";cleaners"
#     # cleaners_cred_points = 511
#     # cleaners_debt_points = 513
#     # yao_voiceunit = sue_believer.get_voice(yao_str)
#     # bob_voiceunit = sue_believer.get_voice(bob_str)
#     # bob_voiceunit.add_membership(swim_str, bob_swim_cred_points, bob_swim_debt_points)
#     # yao_voiceunit.add_membership(swim_str, yao_swim_cred_points, yao_swim_debt_points)
#     # yao_voiceunit.add_membership(clea_str, cleaners_cred_points, cleaners_debt_points)
#     # sue_believer.get_voice(yao_str).add_membership()
