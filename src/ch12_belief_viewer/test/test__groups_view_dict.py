from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch12_belief_viewer.belief_viewer_examples import (
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
from src.ch12_belief_viewer.belief_viewer_tool import (
    add_small_dot,
    get_groups_view_dict,
)
from src.ch12_belief_viewer.test.test__voices_view_dict import add_readable
from src.ref.keywords import Ch12Keywords as kw


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
#     yao_cred_lumen = 110
#     yao_debt_lumen = 130
#     bob_cred_lumen = 230
#     bob_debt_lumen = 290
#     sue_believer.add_voiceunit(yao_str, yao_cred_lumen, yao_debt_lumen)
#     sue_believer.add_voiceunit(bob_str, bob_cred_lumen, bob_debt_lumen)
#     swim_str = ";swimmers"
#     bob_swim_cred_lumen = 66
#     bob_swim_debt_lumen = 77
#     yao_swim_cred_lumen = 88
#     yao_swim_debt_lumen = 99
#     yao_voice = sue_believer.get_voice(yao_str)
#     bob_voice = sue_believer.get_voice(bob_str)
#     yao_voice.add_membership(swim_str, yao_swim_cred_lumen, yao_swim_debt_lumen)
#     bob_voice.add_membership(swim_str, bob_swim_cred_lumen, bob_swim_debt_lumen)
#     sue_believer.cashout()

#     # WHEN
#     groups_view_dict = get_groups_view_dict(sue_believer)

#     # THEN
#     assert set(groups_view_dict.keys()) == {yao_str, bob_str, swim_str}

#     swim_group_dict = groups_view_dict.get(swim_str)
#     group_title_readable_key = add_readable(kw.group_title)
#     memberships_readable_key = add_readable(kw.memberships)
#     fund_give_readable_key = add_readable(kw.fund_give)
#     fund_take_readable_key = add_readable(kw.fund_take)
#     fund_agenda_give_readable_key = add_readable(kw.fund_agenda_give)
#     fund_agenda_take_readable_key = add_readable(kw.fund_agenda_take)
#     credor_pool_readable_key = add_readable(kw.credor_pool)
#     debtor_pool_readable_key = add_readable(kw.debtor_pool)
#     assert set(swim_group_dict.keys()) == {
#         kw.group_title,
#         kw.memberships,
#         kw.fund_give,
#         kw.fund_take,
#         kw.fund_agenda_give,
#         kw.fund_agenda_take,
#         kw.credor_pool,
#         kw.debtor_pool,
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
#     assert sgu.group_title == sg_dict.get(kw.group_title)
#     assert sgu.memberships == sg_dict.get(kw.memberships)
#     assert sgu.fund_give == sg_dict.get(kw.fund_give)
#     assert sgu.fund_take == sg_dict.get(kw.fund_take)
#     assert sgu.fund_agenda_give == sg_dict.get(kw.fund_agenda_give)
#     assert sgu.fund_agenda_take == sg_dict.get(kw.fund_agenda_take)
#     assert sgu.credor_pool == sg_dict.get(kw.credor_pool)
#     assert sgu.debtor_pool == sg_dict.get(kw.debtor_pool)
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
#     yao_swim_cred_lumen = 311
#     yao_swim_debt_lumen = 313
#     yao_voiceunit = sue_believer.get_voice(yao_str)
#     yao_voiceunit.add_membership(swim_str, yao_swim_cred_lumen, yao_swim_debt_lumen)
#     sue_believer.cashout()

#     # WHEN
#     groups_view_dict = get_groups_view_dict(sue_believer)

#     # THEN
#     assert set(groups_view_dict.keys()) == {yao_str}
#     yao_voice_dict = groups_view_dict.get(yao_str)
#     assert kw.memberships in set(yao_voice_dict.keys())
#     yao_memberships_dict = yao_voice_dict.get(kw.memberships)
#     assert {swim_str, yao_str} == set(yao_memberships_dict.keys())
#     yao_swim_dict = yao_memberships_dict.get(swim_str)

#     group_title_readable_key = add_readable(kw.group_title)
#     group_cred_lumen_readable_key = add_readable(kw.group_cred_lumen)
#     group_debt_lumen_readable_key = add_readable(kw.group_debt_lumen)
#     credor_pool_readable_key = add_readable(kw.credor_pool)
#     debtor_pool_readable_key = add_readable(kw.debtor_pool)
#     fund_agenda_give_readable_key = add_readable(kw.fund_agenda_give)
#     fund_agenda_ratio_give_readable_key = add_readable(kw.fund_agenda_ratio_give)
#     fund_agenda_ratio_take_readable_key = add_readable(kw.fund_agenda_ratio_take)
#     fund_agenda_take_readable_key = add_readable(kw.fund_agenda_take)
#     fund_give_readable_key = add_readable(kw.fund_give)
#     fund_take_readable_key = add_readable(kw.fund_take)
#     assert set(yao_swim_dict.keys()) == {
#         kw.voice_name,
#        kw.group_title,
#        kw.group_cred_lumen,
#        kw.group_debt_lumen,
#         kw.credor_pool,
#         kw.debtor_pool,
#         kw.fund_agenda_give,
#         kw.fund_agenda_ratio_give,
#         kw.fund_agenda_ratio_take,
#         kw.fund_agenda_take,
#         kw.fund_give,
#         kw.fund_take,
#         group_title_readable_key,
#         group_cred_lumen_readable_key,
#         group_debt_lumen_readable_key,
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
#     expected_group_title_readable = f"{kw.group_title}: {yao_swim_mu.group_title}"
#     expected_group_cred_lumen_readable = (
#         f"{kw.group_cred_lumen}: {yao_swim_mu.group_cred_lumen}"
#     )
#     expected_group_debt_lumen_readable = (
#         f"{kw.group_debt_lumen}: {yao_swim_mu.group_debt_lumen}"
#     )
#     expected_credor_pool_readable = f"{kw.credor_pool}: {yao_swim_mu.credor_pool}"
#     expected_debtor_pool_readable = f"{kw.debtor_pool}: {yao_swim_mu.debtor_pool}"
#     expected_fund_agenda_give_readable = (
#         f"{kw.fund_agenda_give}: {yao_swim_mu.fund_agenda_give}"
#     )
#     expected_fund_agenda_ratio_give_readable = (
#         f"{kw.fund_agenda_ratio_give}: {yao_swim_mu.fund_agenda_ratio_give}"
#     )
#     expected_fund_agenda_ratio_take_readable = (
#         f"{kw.fund_agenda_ratio_take}: {yao_swim_mu.fund_agenda_ratio_take}"
#     )
#     expected_fund_agenda_take_readable = (
#         f"{kw.fund_agenda_take}: {yao_swim_mu.fund_agenda_take}"
#     )
#     expected_fund_give_readable = f"{kw.fund_give}: {yao_swim_mu.fund_give}"
#     expected_fund_take_readable = f"{kw.fund_take}: {yao_swim_mu.fund_take}"

#     assert yao_swim_dict.get(kw.voice_name) == yao_swim_mu.voice_name
#     assert yao_swim_dict.get(kw.group_title) == yao_swim_mu.group_title
#     assert yao_swim_dict.get(kw.group_cred_lumen) == yao_swim_mu.group_cred_lumen
#     assert yao_swim_dict.get(kw.group_debt_lumen) == yao_swim_mu.group_debt_lumen
#     assert yao_swim_dict.get(kw.credor_pool) == yao_swim_mu.credor_pool
#     assert yao_swim_dict.get(kw.debtor_pool) == yao_swim_mu.debtor_pool
#     assert yao_swim_dict.get(kw.fund_agenda_give) == yao_swim_mu.fund_agenda_give
#     assert (
#         yao_swim_dict.get(kw.fund_agenda_ratio_give)
#         == yao_swim_mu.fund_agenda_ratio_give
#     )
#     assert (
#         yao_swim_dict.get(kw.fund_agenda_ratio_take)
#         == yao_swim_mu.fund_agenda_ratio_take
#     )
#     assert yao_swim_dict.get(kw.fund_agenda_take) == yao_swim_mu.fund_agenda_take
#     assert yao_swim_dict.get(kw.fund_give) == yao_swim_mu.fund_give
#     assert yao_swim_dict.get(kw.fund_take) == yao_swim_mu.fund_take
#     assert yao_swim_dict.get(group_title_readable_key) == expected_group_title_readable
#     assert (
#         yao_swim_dict.get(group_cred_lumen_readable_key)
#         == expected_group_cred_lumen_readable
#     )
#     assert (
#         yao_swim_dict.get(group_debt_lumen_readable_key)
#         == expected_group_debt_lumen_readable
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
#     # yao_cred_lumen = 110
#     # yao_debt_lumen = 130
#     # bob_cred_lumen = 230
#     # bob_debt_lumen = 290
#     # sue_believer.add_voiceunit(yao_str, yao_cred_lumen, yao_debt_lumen)
#     # sue_believer.add_voiceunit(bob_str, bob_cred_lumen, bob_debt_lumen)
#     # swim_str = ";swimmers"
#     # yao_swim_cred_lumen = 311
#     # yao_swim_debt_lumen = 313
#     # bob_swim_cred_lumen = 411
#     # bob_swim_debt_lumen = 413
#     # clea_str = ";cleaners"
#     # cleaners_cred_lumen = 511
#     # cleaners_debt_lumen = 513
#     # yao_voiceunit = sue_believer.get_voice(yao_str)
#     # bob_voiceunit = sue_believer.get_voice(bob_str)
#     # bob_voiceunit.add_membership(swim_str, bob_swim_cred_lumen, bob_swim_debt_lumen)
#     # yao_voiceunit.add_membership(swim_str, yao_swim_cred_lumen, yao_swim_debt_lumen)
#     # yao_voiceunit.add_membership(clea_str, cleaners_cred_lumen, cleaners_debt_lumen)
#     # sue_believer.get_voice(yao_str).add_membership()
