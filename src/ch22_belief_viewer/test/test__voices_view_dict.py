from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch22_belief_viewer._ref.ch22_keywords import Ch04Keywords as wx, readable_str
from src.ch22_belief_viewer.belief_viewer_tool import (
    add_small_dot,
    get_voices_view_dict,
)


def test_get_voices_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    sue_believer.cashout()

    # WHEN
    voices_view_dict = get_voices_view_dict(sue_believer)

    # THEN
    assert voices_view_dict == {}


def add_readable(str: str) -> str:
    return f"{str}_{readable_str()}"


def test_get_voices_view_dict_ReturnsObj_Scenario1_voices():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    yao_str = "Yao"
    bob_str = "Bob"
    yao_cred_points = 110
    yao_debt_points = 130
    bob_cred_points = 230
    bob_debt_points = 290
    sue_believer.add_voiceunit(yao_str, yao_cred_points, yao_debt_points)
    sue_believer.add_voiceunit(bob_str, bob_cred_points, bob_debt_points)
    sue_believer.cashout()

    # WHEN
    voices_view_dict = get_voices_view_dict(sue_believer)

    # THEN
    assert set(voices_view_dict.keys()) == {yao_str, bob_str}
    yao_voice_dict = voices_view_dict.get(yao_str)
    voice_cred_points_readable_key = add_readable(wx.voice_cred_points)
    voice_debt_points_readable_key = add_readable(wx.voice_debt_points)
    memberships_readable_key = add_readable(wx.memberships)
    credor_pool_readable_key = add_readable(wx.credor_pool)
    debtor_pool_readable_key = add_readable(wx.debtor_pool)
    irrational_voice_debt_points_readable_key = add_readable(
        wx.irrational_voice_debt_points
    )
    inallocable_voice_debt_points_readable_key = add_readable(
        wx.inallocable_voice_debt_points
    )
    fund_give_readable_key = add_readable(wx.fund_give)
    fund_take_readable_key = add_readable(wx.fund_take)
    fund_agenda_give_readable_key = add_readable(wx.fund_agenda_give)
    fund_agenda_take_readable_key = add_readable(wx.fund_agenda_take)
    fund_agenda_ratio_give_readable_key = add_readable(wx.fund_agenda_ratio_give)
    fund_agenda_ratio_take_readable_key = add_readable(wx.fund_agenda_ratio_take)

    assert set(yao_voice_dict.keys()) == {
        wx.voice_name,
        wx.voice_cred_points,
        wx.voice_debt_points,
        wx.memberships,
        wx.credor_pool,
        wx.debtor_pool,
        wx.irrational_voice_debt_points,
        wx.inallocable_voice_debt_points,
        wx.fund_give,
        wx.fund_take,
        wx.fund_agenda_give,
        wx.fund_agenda_take,
        wx.fund_agenda_ratio_give,
        wx.fund_agenda_ratio_take,
        voice_cred_points_readable_key,
        voice_debt_points_readable_key,
        memberships_readable_key,
        credor_pool_readable_key,
        debtor_pool_readable_key,
        irrational_voice_debt_points_readable_key,
        inallocable_voice_debt_points_readable_key,
        fund_give_readable_key,
        fund_take_readable_key,
        fund_agenda_give_readable_key,
        fund_agenda_take_readable_key,
        fund_agenda_ratio_give_readable_key,
        fund_agenda_ratio_take_readable_key,
    }
    ypu = sue_believer.get_voice(yao_str)
    yp_dict = yao_voice_dict
    assert ypu.voice_name == yp_dict.get(wx.voice_name)
    assert ypu.voice_cred_points == yp_dict.get(wx.voice_cred_points)
    assert ypu.voice_debt_points == yp_dict.get(wx.voice_debt_points)
    assert ypu.credor_pool == yp_dict.get(wx.credor_pool)
    assert ypu.debtor_pool == yp_dict.get(wx.debtor_pool)
    assert ypu.irrational_voice_debt_points == yp_dict.get(
        wx.irrational_voice_debt_points
    )
    assert ypu.inallocable_voice_debt_points == yp_dict.get(
        wx.inallocable_voice_debt_points
    )
    assert ypu.fund_give == yp_dict.get(wx.fund_give)
    assert ypu.fund_take == yp_dict.get(wx.fund_take)
    assert ypu.fund_agenda_give == yp_dict.get(wx.fund_agenda_give)
    assert ypu.fund_agenda_take == yp_dict.get(wx.fund_agenda_take)
    assert ypu.fund_agenda_ratio_give == yp_dict.get(wx.fund_agenda_ratio_give)
    assert ypu.fund_agenda_ratio_take == yp_dict.get(wx.fund_agenda_ratio_take)

    expected_voice_cred_points_readable = f"voice_cred_points: {ypu.voice_cred_points}"
    expected_voice_debt_points_readable = f"voice_debt_points: {ypu.voice_debt_points}"
    expected_memberships_readable = f"memberships: {ypu.memberships}"
    expected_credor_pool_readable = f"credor_pool: {ypu.credor_pool}"
    expected_debtor_pool_readable = f"debtor_pool: {ypu.debtor_pool}"
    expected_irrational_voice_debt_points_readable = (
        f"irrational_voice_debt_points: {ypu.irrational_voice_debt_points}"
    )
    expected_inallocable_voice_debt_points_readable = (
        f"inallocable_voice_debt_points: {ypu.inallocable_voice_debt_points}"
    )
    expected_fund_give_readable = f"fund_give: {ypu.fund_give}"
    expected_fund_take_readable = f"fund_take: {ypu.fund_take}"
    expected_fund_agenda_give_readable = f"fund_agenda_give: {ypu.fund_agenda_give}"
    expected_fund_agenda_take_readable = f"fund_agenda_take: {ypu.fund_agenda_take}"
    expected_fund_agenda_ratio_give_readable = (
        f"fund_agenda_ratio_give: {ypu.fund_agenda_ratio_give}"
    )
    expected_fund_agenda_ratio_take_readable = (
        f"fund_agenda_ratio_take: {ypu.fund_agenda_ratio_take}"
    )

    assert (
        yp_dict.get(voice_cred_points_readable_key)
        == expected_voice_cred_points_readable
    )
    assert (
        yp_dict.get(voice_debt_points_readable_key)
        == expected_voice_debt_points_readable
    )
    assert yp_dict.get(memberships_readable_key) == expected_memberships_readable
    assert yp_dict.get(credor_pool_readable_key) == expected_credor_pool_readable
    assert yp_dict.get(debtor_pool_readable_key) == expected_debtor_pool_readable
    assert (
        yp_dict.get(irrational_voice_debt_points_readable_key)
        == expected_irrational_voice_debt_points_readable
    )
    assert (
        yp_dict.get(inallocable_voice_debt_points_readable_key)
        == expected_inallocable_voice_debt_points_readable
    )
    assert yp_dict.get(fund_give_readable_key) == expected_fund_give_readable
    assert yp_dict.get(fund_take_readable_key) == expected_fund_take_readable
    assert (
        yp_dict.get(fund_agenda_give_readable_key) == expected_fund_agenda_give_readable
    )
    assert (
        yp_dict.get(fund_agenda_take_readable_key) == expected_fund_agenda_take_readable
    )
    assert (
        yp_dict.get(fund_agenda_ratio_give_readable_key)
        == expected_fund_agenda_ratio_give_readable
    )
    assert (
        yp_dict.get(fund_agenda_ratio_take_readable_key)
        == expected_fund_agenda_ratio_take_readable
    )


def test_get_voices_view_dict_ReturnsObj_Scenario2_memberships():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    yao_str = "Yao"
    sue_believer.add_voiceunit(yao_str)
    swim_str = ";swimmers"
    yao_swim_cred_points = 311
    yao_swim_debt_points = 313
    yao_voiceunit = sue_believer.get_voice(yao_str)
    yao_voiceunit.add_membership(swim_str, yao_swim_cred_points, yao_swim_debt_points)
    sue_believer.cashout()

    # WHEN
    voices_view_dict = get_voices_view_dict(sue_believer)

    # THEN
    assert set(voices_view_dict.keys()) == {yao_str}
    yao_voice_dict = voices_view_dict.get(yao_str)
    assert wx.memberships in set(yao_voice_dict.keys())
    yao_memberships_dict = yao_voice_dict.get(wx.memberships)
    assert {swim_str, yao_str} == set(yao_memberships_dict.keys())
    yao_swim_dict = yao_memberships_dict.get(swim_str)

    group_title_readable_key = add_readable(wx.group_title)
    group_cred_points_readable_key = add_readable(wx.group_cred_points)
    group_debt_points_readable_key = add_readable(wx.group_debt_points)
    credor_pool_readable_key = add_readable(wx.credor_pool)
    debtor_pool_readable_key = add_readable(wx.debtor_pool)
    fund_agenda_give_readable_key = add_readable(wx.fund_agenda_give)
    fund_agenda_ratio_give_readable_key = add_readable(wx.fund_agenda_ratio_give)
    fund_agenda_ratio_take_readable_key = add_readable(wx.fund_agenda_ratio_take)
    fund_agenda_take_readable_key = add_readable(wx.fund_agenda_take)
    fund_give_readable_key = add_readable(wx.fund_give)
    fund_take_readable_key = add_readable(wx.fund_take)
    assert set(yao_swim_dict.keys()) == {
        wx.voice_name,
        wx.group_title,
        wx.group_cred_points,
        wx.group_debt_points,
        wx.credor_pool,
        wx.debtor_pool,
        wx.fund_agenda_give,
        wx.fund_agenda_ratio_give,
        wx.fund_agenda_ratio_take,
        wx.fund_agenda_take,
        wx.fund_give,
        wx.fund_take,
        group_title_readable_key,
        group_cred_points_readable_key,
        group_debt_points_readable_key,
        credor_pool_readable_key,
        debtor_pool_readable_key,
        fund_agenda_give_readable_key,
        fund_agenda_ratio_give_readable_key,
        fund_agenda_ratio_take_readable_key,
        fund_agenda_take_readable_key,
        fund_give_readable_key,
        fund_take_readable_key,
    }
    yao_swim_mu = yao_voiceunit.get_membership(swim_str)

    expected_group_title_readable = f"{wx.group_title}: {yao_swim_mu.group_title}"
    expected_group_cred_points_readable = (
        f"{wx.group_cred_points}: {yao_swim_mu.group_cred_points}"
    )
    expected_group_debt_points_readable = (
        f"{wx.group_debt_points}: {yao_swim_mu.group_debt_points}"
    )
    expected_credor_pool_readable = f"{wx.credor_pool}: {yao_swim_mu.credor_pool}"
    expected_debtor_pool_readable = f"{wx.debtor_pool}: {yao_swim_mu.debtor_pool}"
    expected_fund_agenda_give_readable = (
        f"{wx.fund_agenda_give}: {yao_swim_mu.fund_agenda_give}"
    )
    expected_fund_agenda_ratio_give_readable = (
        f"{wx.fund_agenda_ratio_give}: {yao_swim_mu.fund_agenda_ratio_give}"
    )
    expected_fund_agenda_ratio_take_readable = (
        f"{wx.fund_agenda_ratio_take}: {yao_swim_mu.fund_agenda_ratio_take}"
    )
    expected_fund_agenda_take_readable = (
        f"{wx.fund_agenda_take}: {yao_swim_mu.fund_agenda_take}"
    )
    expected_fund_give_readable = f"{wx.fund_give}: {yao_swim_mu.fund_give}"
    expected_fund_take_readable = f"{wx.fund_take}: {yao_swim_mu.fund_take}"

    expected_group_title_readable = add_small_dot(expected_group_title_readable)
    expected_group_cred_points_readable = add_small_dot(
        expected_group_cred_points_readable
    )
    expected_group_debt_points_readable = add_small_dot(
        expected_group_debt_points_readable
    )
    expected_credor_pool_readable = add_small_dot(expected_credor_pool_readable)
    expected_debtor_pool_readable = add_small_dot(expected_debtor_pool_readable)
    expected_fund_agenda_give_readable = add_small_dot(
        expected_fund_agenda_give_readable
    )
    expected_fund_agenda_ratio_give_readable = add_small_dot(
        expected_fund_agenda_ratio_give_readable
    )
    expected_fund_agenda_ratio_take_readable = add_small_dot(
        expected_fund_agenda_ratio_take_readable
    )
    expected_fund_agenda_take_readable = add_small_dot(
        expected_fund_agenda_take_readable
    )
    expected_fund_give_readable = add_small_dot(expected_fund_give_readable)
    expected_fund_take_readable = add_small_dot(expected_fund_take_readable)

    assert yao_swim_dict.get(wx.voice_name) == yao_swim_mu.voice_name
    assert yao_swim_dict.get(wx.group_title) == yao_swim_mu.group_title
    assert yao_swim_dict.get(wx.group_cred_points) == yao_swim_mu.group_cred_points
    assert yao_swim_dict.get(wx.group_debt_points) == yao_swim_mu.group_debt_points
    assert yao_swim_dict.get(wx.credor_pool) == yao_swim_mu.credor_pool
    assert yao_swim_dict.get(wx.debtor_pool) == yao_swim_mu.debtor_pool
    assert yao_swim_dict.get(wx.fund_agenda_give) == yao_swim_mu.fund_agenda_give
    assert (
        yao_swim_dict.get(wx.fund_agenda_ratio_give)
        == yao_swim_mu.fund_agenda_ratio_give
    )
    assert (
        yao_swim_dict.get(wx.fund_agenda_ratio_take)
        == yao_swim_mu.fund_agenda_ratio_take
    )
    assert yao_swim_dict.get(wx.fund_agenda_take) == yao_swim_mu.fund_agenda_take
    assert yao_swim_dict.get(wx.fund_give) == yao_swim_mu.fund_give
    assert yao_swim_dict.get(wx.fund_take) == yao_swim_mu.fund_take
    assert yao_swim_dict.get(group_title_readable_key) == expected_group_title_readable
    assert (
        yao_swim_dict.get(group_cred_points_readable_key)
        == expected_group_cred_points_readable
    )
    assert (
        yao_swim_dict.get(group_debt_points_readable_key)
        == expected_group_debt_points_readable
    )
    assert yao_swim_dict.get(credor_pool_readable_key) == expected_credor_pool_readable
    assert yao_swim_dict.get(debtor_pool_readable_key) == expected_debtor_pool_readable
    assert (
        yao_swim_dict.get(fund_agenda_give_readable_key)
        == expected_fund_agenda_give_readable
    )
    assert (
        yao_swim_dict.get(fund_agenda_ratio_give_readable_key)
        == expected_fund_agenda_ratio_give_readable
    )
    assert (
        yao_swim_dict.get(fund_agenda_ratio_take_readable_key)
        == expected_fund_agenda_ratio_take_readable
    )
    assert (
        yao_swim_dict.get(fund_agenda_take_readable_key)
        == expected_fund_agenda_take_readable
    )
    assert yao_swim_dict.get(fund_give_readable_key) == expected_fund_give_readable
    assert yao_swim_dict.get(fund_take_readable_key) == expected_fund_take_readable

    # sue_str = "Sue"
    # sue_believer = beliefunit_shop(sue_str)
    # yao_str = "Yao"
    # bob_str = "Bob"
    # yao_cred_points = 110
    # yao_debt_points = 130
    # bob_cred_points = 230
    # bob_debt_points = 290
    # sue_believer.add_voiceunit(yao_str, yao_cred_points, yao_debt_points)
    # sue_believer.add_voiceunit(bob_str, bob_cred_points, bob_debt_points)
    # swim_str = ";swimmers"
    # yao_swim_cred_points = 311
    # yao_swim_debt_points = 313
    # bob_swim_cred_points = 411
    # bob_swim_debt_points = 413
    # clea_str = ";cleaners"
    # cleaners_cred_points = 511
    # cleaners_debt_points = 513
    # yao_voiceunit = sue_believer.get_voice(yao_str)
    # bob_voiceunit = sue_believer.get_voice(bob_str)
    # bob_voiceunit.add_membership(swim_str, bob_swim_cred_points, bob_swim_debt_points)
    # yao_voiceunit.add_membership(swim_str, yao_swim_cred_points, yao_swim_debt_points)
    # yao_voiceunit.add_membership(clea_str, cleaners_cred_points, cleaners_debt_points)
    # sue_believer.get_voice(yao_str).add_membership()
