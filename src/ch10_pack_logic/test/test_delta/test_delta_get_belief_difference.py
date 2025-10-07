from copy import deepcopy as copy_deepcopy
from src.ch01_data_toolbox.dict_toolbox import (
    get_empty_list_if_None,
    get_from_nested_dict,
)
from src.ch04_voice_logic.group import awardunit_shop
from src.ch04_voice_logic.voice import voiceunit_shop
from src.ch05_reason_logic.reason import factunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ch10_pack_logic.delta import BeliefDelta, beliefdelta_shop
from src.ref.ch10_keywords import Ch10Keywords as wx


def print_beliefatom_keys(x_beliefdelta: BeliefDelta):
    for x_beliefatom in get_delete_beliefatom_list(x_beliefdelta):
        print(f"DELETE {x_beliefatom.dimen} {list(x_beliefatom.jkeys.values())}")
    for x_beliefatom in get_update_beliefatom_list(x_beliefdelta):
        print(f"UPDATE {x_beliefatom.dimen} {list(x_beliefatom.jkeys.values())}")
    for x_beliefatom in get_insert_beliefatom_list(x_beliefdelta):
        print(f"INSERT {x_beliefatom.dimen} {list(x_beliefatom.jkeys.values())}")


def get_delete_beliefatom_list(x_beliefdelta: BeliefDelta) -> list:
    return get_empty_list_if_None(
        x_beliefdelta._get_crud_beliefatoms_list().get(wx.DELETE)
    )


def get_insert_beliefatom_list(x_beliefdelta: BeliefDelta):
    return get_empty_list_if_None(
        x_beliefdelta._get_crud_beliefatoms_list().get(wx.INSERT)
    )


def get_update_beliefatom_list(x_beliefdelta: BeliefDelta):
    return get_empty_list_if_None(
        x_beliefdelta._get_crud_beliefatoms_list().get(wx.UPDATE)
    )


def get_beliefatom_total_count(x_beliefdelta: BeliefDelta) -> int:
    return (
        len(get_delete_beliefatom_list(x_beliefdelta))
        + len(get_insert_beliefatom_list(x_beliefdelta))
        + len(get_update_beliefatom_list(x_beliefdelta))
    )


def test_BeliefDelta_create_beliefatoms_EmptyBeliefs():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sue_beliefdelta = beliefdelta_shop()
    assert sue_beliefdelta.beliefatoms == {}

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(sue_belief, sue_belief)

    # THEN
    assert sue_beliefdelta.beliefatoms == {}


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_voiceunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    after_sue_belief = copy_deepcopy(before_sue_belief)
    xio_str = "Xio"
    xio_voice_cred_lumen = 33
    xio_voice_debt_lumen = 44
    xio_voiceunit = voiceunit_shop(xio_str, xio_voice_cred_lumen, xio_voice_debt_lumen)
    after_sue_belief.set_voiceunit(xio_voiceunit, auto_set_membership=False)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    assert len(sue_beliefdelta.beliefatoms.get(wx.INSERT).get(wx.belief_voiceunit)) == 1
    sue_insert_dict = sue_beliefdelta.beliefatoms.get(wx.INSERT)
    sue_voiceunit_dict = sue_insert_dict.get(wx.belief_voiceunit)
    xio_beliefatom = sue_voiceunit_dict.get(xio_str)
    assert xio_beliefatom.get_value(wx.voice_name) == xio_str
    assert xio_beliefatom.get_value("voice_cred_lumen") == xio_voice_cred_lumen
    assert xio_beliefatom.get_value("voice_debt_lumen") == xio_voice_debt_lumen

    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_voiceunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    before_sue_belief.add_voiceunit("Yao")
    before_sue_belief.add_voiceunit("Zia")

    after_sue_belief = copy_deepcopy(before_sue_belief)

    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    xio_beliefatom = get_from_nested_dict(
        sue_beliefdelta.beliefatoms,
        [wx.DELETE, wx.belief_voiceunit, xio_str],
    )
    assert xio_beliefatom.get_value(wx.voice_name) == xio_str

    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    print_beliefatom_keys(sue_beliefdelta)
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_voiceunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    after_sue_belief = copy_deepcopy(before_sue_belief)
    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)
    xio_voice_cred_lumen = 33
    xio_voice_debt_lumen = 44
    after_sue_belief.add_voiceunit(xio_str, xio_voice_cred_lumen, xio_voice_debt_lumen)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    x_keylist = [wx.UPDATE, wx.belief_voiceunit, xio_str]
    xio_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert xio_beliefatom.get_value(wx.voice_name) == xio_str
    assert xio_beliefatom.get_value("voice_cred_lumen") == xio_voice_cred_lumen
    assert xio_beliefatom.get_value("voice_debt_lumen") == xio_voice_debt_lumen

    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_BeliefUnit_simple_attrs_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    after_sue_belief = copy_deepcopy(before_sue_belief)
    x_beliefunit_tally = 55
    x_fund_pool = 8000000
    x_fund_grain = 8
    x_respect_grain = 5
    x_max_tree_traverse = 66
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_belief.tally = x_beliefunit_tally
    after_sue_belief.fund_pool = x_fund_pool
    after_sue_belief.fund_grain = x_fund_grain
    after_sue_belief.respect_grain = x_respect_grain
    after_sue_belief.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_belief.set_credor_respect(x_credor_respect)
    after_sue_belief.set_debtor_respect(x_debtor_respect)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    x_keylist = [wx.UPDATE, wx.beliefunit]
    xio_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert xio_beliefatom.get_value("max_tree_traverse") == x_max_tree_traverse
    assert xio_beliefatom.get_value("credor_respect") == x_credor_respect
    assert xio_beliefatom.get_value("debtor_respect") == x_debtor_respect
    assert xio_beliefatom.get_value("tally") == x_beliefunit_tally
    assert xio_beliefatom.get_value("fund_pool") == x_fund_pool
    assert xio_beliefatom.get_value("fund_grain") == x_fund_grain
    assert xio_beliefatom.get_value("respect_grain") == x_respect_grain

    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_voice_membership_insert():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    after_sue_belief = copy_deepcopy(before_sue_belief)
    yao_str = "Yao"
    zia_str = "Zia"
    temp_yao_voiceunit = voiceunit_shop(yao_str)
    temp_zia_voiceunit = voiceunit_shop(zia_str)
    after_sue_belief.set_voiceunit(temp_yao_voiceunit, auto_set_membership=False)
    after_sue_belief.set_voiceunit(temp_zia_voiceunit, auto_set_membership=False)
    after_yao_voiceunit = after_sue_belief.get_voice(yao_str)
    after_zia_voiceunit = after_sue_belief.get_voice(zia_str)
    run_str = ";runners"
    zia_run_credit_w = 77
    zia_run_debt_w = 88
    after_zia_voiceunit.add_membership(run_str, zia_run_credit_w, zia_run_debt_w)
    print(f"{after_sue_belief.get_voiceunit_group_titles_dict()=}")

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    print(f"{after_sue_belief.get_voice(zia_str).memberships=}")
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)
    # print(f"{sue_beliefdelta.beliefatoms.get(wx.INSERT).keys()=}")
    # print(
    #     sue_beliefdelta.beliefatoms.get(wx.INSERT).get(wx.belief_voice_membership).keys()
    # )

    # THEN
    x_keylist = [wx.INSERT, wx.belief_voiceunit, yao_str]
    yao_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert yao_beliefatom.get_value(wx.voice_name) == yao_str

    x_keylist = [wx.INSERT, wx.belief_voiceunit, zia_str]
    zia_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert zia_beliefatom.get_value(wx.voice_name) == zia_str
    print(f"\n{sue_beliefdelta.beliefatoms=}")
    # print(f"\n{zia_beliefatom=}")

    x_keylist = [wx.INSERT, wx.belief_voice_membership, zia_str, run_str]
    run_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert run_beliefatom.get_value(wx.voice_name) == zia_str
    assert run_beliefatom.get_value(wx.group_title) == run_str
    assert run_beliefatom.get_value("group_cred_lumen") == zia_run_credit_w
    assert run_beliefatom.get_value("group_debt_lumen") == zia_run_debt_w

    print_beliefatom_keys(sue_beliefdelta)
    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    assert len(get_delete_beliefatom_list(sue_beliefdelta)) == 0
    assert len(get_insert_beliefatom_list(sue_beliefdelta)) == 3
    assert len(get_delete_beliefatom_list(sue_beliefdelta)) == 0
    assert get_beliefatom_total_count(sue_beliefdelta) == 3


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_voice_membership_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_belief.add_voiceunit(xio_str)
    before_sue_belief.add_voiceunit(zia_str)
    run_str = ";runners"
    before_xio_credit_w = 77
    before_xio_debt_w = 88
    before_xio_voice = before_sue_belief.get_voice(xio_str)
    before_xio_voice.add_membership(run_str, before_xio_credit_w, before_xio_debt_w)
    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_xio_voiceunit = after_sue_belief.get_voice(xio_str)
    after_xio_credit_w = 55
    after_xio_debt_w = 66
    after_xio_voiceunit.add_membership(run_str, after_xio_credit_w, after_xio_debt_w)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    # x_keylist = [wx.UPDATE, wx.belief_voiceunit, xio_str]
    # xio_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    # assert xio_beliefatom.get_value(wx.voice_name) == xio_str
    # print(f"\n{sue_beliefdelta.beliefatoms=}")
    # print(f"\n{xio_beliefatom=}")

    x_keylist = [wx.UPDATE, wx.belief_voice_membership, xio_str, run_str]
    xio_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert xio_beliefatom.get_value(wx.voice_name) == xio_str
    assert xio_beliefatom.get_value(wx.group_title) == run_str
    assert xio_beliefatom.get_value("group_cred_lumen") == after_xio_credit_w
    assert xio_beliefatom.get_value("group_debt_lumen") == after_xio_debt_w

    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_voice_membership_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_belief.add_voiceunit(xio_str)
    before_sue_belief.add_voiceunit(zia_str)
    before_sue_belief.add_voiceunit(bob_str)
    before_xio_voiceunit = before_sue_belief.get_voice(xio_str)
    before_zia_voiceunit = before_sue_belief.get_voice(zia_str)
    before_bob_voiceunit = before_sue_belief.get_voice(bob_str)
    run_str = ";runners"
    before_xio_voiceunit.add_membership(run_str)
    before_zia_voiceunit.add_membership(run_str)
    fly_str = ";flyers"
    before_xio_voiceunit.add_membership(fly_str)
    before_zia_voiceunit.add_membership(fly_str)
    before_bob_voiceunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_belief.get_voiceunit_group_titles_dict()

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_xio_voiceunit = after_sue_belief.get_voice(xio_str)
    after_zia_voiceunit = after_sue_belief.get_voice(zia_str)
    after_bob_voiceunit = after_sue_belief.get_voice(bob_str)
    after_xio_voiceunit.delete_membership(run_str)
    after_zia_voiceunit.delete_membership(run_str)
    after_bob_voiceunit.delete_membership(fly_str)
    after_group_titles_dict = after_sue_belief.get_voiceunit_group_titles_dict()
    assert len(before_group_titles_dict.get(fly_str)) == 3
    assert len(before_group_titles_dict.get(run_str)) == 2
    assert len(after_group_titles_dict.get(fly_str)) == 2
    assert after_group_titles_dict.get(run_str) is None

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    x_keylist = [wx.DELETE, wx.belief_voice_membership, bob_str, fly_str]
    xio_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert xio_beliefatom.get_value(wx.voice_name) == bob_str
    assert xio_beliefatom.get_value(wx.group_title) == fly_str

    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    print_beliefatom_keys(sue_beliefdelta)
    assert len(get_delete_beliefatom_list(sue_beliefdelta)) == 3
    assert len(get_insert_beliefatom_list(sue_beliefdelta)) == 0
    assert len(get_update_beliefatom_list(sue_beliefdelta)) == 0
    assert get_beliefatom_total_count(sue_beliefdelta) == 3


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_belief.make_rope(ball_rope, street_str)
    before_sue_belief.set_plan(planunit_shop(street_str), ball_rope)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_belief.make_rope(sports_rope, disc_str)
    amy45_str = "amy45"
    before_sue_belief.set_l1_plan(planunit_shop(amy45_str))
    before_sue_belief.set_plan(planunit_shop(disc_str), sports_rope)
    # create after without ball_plan and street_plan
    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_sue_belief.del_plan_obj(ball_rope)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    x_dimen = wx.belief_planunit
    print(f"{sue_beliefdelta.beliefatoms.get(wx.DELETE).get(x_dimen).keys()=}")

    x_keylist = [wx.DELETE, wx.belief_planunit, street_rope]
    street_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert street_beliefatom.get_value(wx.plan_rope) == street_rope

    x_keylist = [wx.DELETE, wx.belief_planunit, ball_rope]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope

    print(f"{get_beliefatom_total_count(sue_beliefdelta)=}")
    assert get_beliefatom_total_count(sue_beliefdelta) == 2


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_belief.make_rope(ball_rope, street_str)
    before_sue_belief.set_plan(planunit_shop(street_str), ball_rope)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    disc_str = "Ultimate Disc"
    disc_rope = after_sue_belief.make_rope(sports_rope, disc_str)
    after_sue_belief.set_plan(planunit_shop(disc_str), sports_rope)
    amy45_str = "amy45"
    amy_begin = 34
    amy_close = 78
    amy_star = 55
    amy_pledge = True
    amy_rope = after_sue_belief.make_l1_rope(amy45_str)
    after_sue_belief.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=amy_begin,
            close=amy_close,
            star=amy_star,
            pledge=amy_pledge,
        )
    )

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print_beliefatom_keys(sue_beliefdelta)

    x_keylist = [wx.INSERT, wx.belief_planunit, disc_rope]
    street_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert street_beliefatom.get_value(wx.plan_rope) == disc_rope

    a45_rope = after_sue_belief.make_l1_rope(amy45_str)
    x_keylist = [wx.INSERT, wx.belief_planunit, a45_rope]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == a45_rope
    assert ball_beliefatom.get_value(wx.begin) == amy_begin
    assert ball_beliefatom.get_value(wx.close) == amy_close
    assert ball_beliefatom.get_value(wx.star) == amy_star
    assert ball_beliefatom.get_value(wx.pledge) == amy_pledge

    assert get_beliefatom_total_count(sue_beliefdelta) == 2


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    amy45_str = "amy45"
    amy45_rope = before_sue_belief.make_l1_rope(amy45_str)
    before_amy_begin = 34
    before_amy_close = 78
    before_amy_star = 55
    before_amy_pledge = True
    amy_rope = before_sue_belief.make_l1_rope(amy45_str)
    before_sue_belief.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=before_amy_begin,
            close=before_amy_close,
            star=before_amy_star,
            pledge=before_amy_pledge,
        )
    )

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_amy_begin = 99
    after_amy_close = 111
    after_amy_star = 22
    after_amy_pledge = False
    after_sue_belief.edit_plan_attr(
        amy_rope,
        begin=after_amy_begin,
        close=after_amy_close,
        star=after_amy_star,
        pledge=after_amy_pledge,
    )

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print_beliefatom_keys(sue_beliefdelta)

    x_keylist = [wx.UPDATE, wx.belief_planunit, amy45_rope]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == amy45_rope
    assert ball_beliefatom.get_value(wx.begin) == after_amy_begin
    assert ball_beliefatom.get_value(wx.close) == after_amy_close
    assert ball_beliefatom.get_value(wx.star) == after_amy_star
    assert ball_beliefatom.get_value(wx.pledge) == after_amy_pledge

    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_awardunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_voiceunit(xio_str)
    before_sue_au.add_voiceunit(zia_str)
    before_sue_au.add_voiceunit(bob_str)
    xio_voiceunit = before_sue_au.get_voice(xio_str)
    zia_voiceunit = before_sue_au.get_voice(zia_str)
    bob_voiceunit = before_sue_au.get_voice(bob_str)
    run_str = ";runners"
    xio_voiceunit.add_membership(run_str)
    zia_voiceunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_voiceunit.add_membership(fly_str)
    zia_voiceunit.add_membership(fly_str)
    bob_voiceunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_au.set_plan(planunit_shop(disc_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(run_str))
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    before_sue_au.edit_plan_attr(disc_rope, awardunit=awardunit_shop(run_str))
    before_sue_au.edit_plan_attr(disc_rope, awardunit=awardunit_shop(fly_str))

    after_sue_belief = copy_deepcopy(before_sue_au)
    after_sue_belief.edit_plan_attr(disc_rope, awardunit_del=run_str)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_au, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")

    x_keylist = [wx.DELETE, wx.belief_plan_awardunit, disc_rope, run_str]
    run_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert run_beliefatom.get_value(wx.plan_rope) == disc_rope
    assert run_beliefatom.get_value(wx.awardee_title) == run_str

    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_awardunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_voiceunit(xio_str)
    before_sue_au.add_voiceunit(zia_str)
    before_sue_au.add_voiceunit(bob_str)
    xio_voiceunit = before_sue_au.get_voice(xio_str)
    zia_voiceunit = before_sue_au.get_voice(zia_str)
    bob_voiceunit = before_sue_au.get_voice(bob_str)
    run_str = ";runners"
    xio_voiceunit.add_membership(run_str)
    zia_voiceunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_voiceunit.add_membership(fly_str)
    zia_voiceunit.add_membership(fly_str)
    bob_voiceunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_au.set_plan(planunit_shop(disc_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(run_str))
    before_sue_au.edit_plan_attr(disc_rope, awardunit=awardunit_shop(fly_str))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    after_run_give_force = 44
    after_run_take_force = 66
    x_awardunit = awardunit_shop(run_str, after_run_give_force, after_run_take_force)
    after_sue_au.edit_plan_attr(disc_rope, awardunit=x_awardunit)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")

    x_keylist = [wx.INSERT, wx.belief_plan_awardunit, disc_rope, run_str]
    run_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert run_beliefatom.get_value(wx.plan_rope) == disc_rope
    assert run_beliefatom.get_value(wx.awardee_title) == run_str
    assert run_beliefatom.get_value(wx.plan_rope) == disc_rope
    assert run_beliefatom.get_value(wx.awardee_title) == run_str
    assert run_beliefatom.get_value(wx.give_force) == after_run_give_force
    assert run_beliefatom.get_value(wx.take_force) == after_run_take_force

    assert get_beliefatom_total_count(sue_beliefdelta) == 2


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_awardunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_au.add_voiceunit(xio_str)
    before_sue_au.add_voiceunit(zia_str)
    xio_voiceunit = before_sue_au.get_voice(xio_str)
    run_str = ";runners"
    xio_voiceunit.add_membership(run_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(run_str))
    run_awardunit = before_sue_au.get_plan_obj(ball_rope).awardunits.get(run_str)

    after_sue_belief = copy_deepcopy(before_sue_au)
    after_give_force = 55
    after_take_force = 66
    after_sue_belief.edit_plan_attr(
        ball_rope,
        awardunit=awardunit_shop(
            awardee_title=run_str,
            give_force=after_give_force,
            take_force=after_take_force,
        ),
    )
    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_au, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")

    x_keylist = [wx.UPDATE, wx.belief_plan_awardunit, ball_rope, run_str]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.awardee_title) == run_str
    assert ball_beliefatom.get_value(wx.give_force) == after_give_force
    assert ball_beliefatom.get_value(wx.take_force) == after_take_force
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_factunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    bend_str = "bendable"
    bend_rope = before_sue_belief.make_rope(knee_rope, bend_str)
    before_sue_belief.set_plan(planunit_shop(bend_str), knee_rope)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_belief.make_rope(knee_rope, damaged_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    before_sue_belief.set_plan(planunit_shop(damaged_str), knee_rope)
    before_fact_lower = 11
    before_fact_upper = 22
    before_fact = factunit_shop(
        knee_rope, bend_rope, before_fact_lower, before_fact_upper
    )
    before_sue_belief.edit_plan_attr(ball_rope, factunit=before_fact)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_fact_lower = 55
    after_fact_upper = 66
    knee_fact = factunit_shop(
        knee_rope, damaged_rope, after_fact_lower, after_fact_upper
    )
    after_sue_belief.edit_plan_attr(ball_rope, factunit=knee_fact)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")

    x_keylist = [wx.UPDATE, wx.belief_plan_factunit, ball_rope, knee_rope]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.fact_context) == knee_rope
    assert ball_beliefatom.get_value(wx.fact_state) == damaged_rope
    assert ball_beliefatom.get_value(wx.fact_lower) == after_fact_lower
    assert ball_beliefatom.get_value(wx.fact_upper) == after_fact_upper
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_factunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_belief.make_rope(knee_rope, damaged_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    before_sue_belief.set_plan(planunit_shop(damaged_str), knee_rope)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_fact_lower = 55
    after_fact_upper = 66
    after_fact = factunit_shop(
        knee_rope, damaged_rope, after_fact_lower, after_fact_upper
    )
    after_sue_belief.edit_plan_attr(ball_rope, factunit=after_fact)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [wx.INSERT, wx.belief_plan_factunit, ball_rope, knee_rope]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    print(f"{ball_beliefatom=}")
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.fact_context) == knee_rope
    assert ball_beliefatom.get_value(wx.fact_state) == damaged_rope
    assert ball_beliefatom.get_value(wx.fact_lower) == after_fact_lower
    assert ball_beliefatom.get_value(wx.fact_upper) == after_fact_upper
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_factunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_belief.make_rope(knee_rope, damaged_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    before_sue_belief.set_plan(planunit_shop(damaged_str), knee_rope)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    before_damaged_reason_lower = 55
    before_damaged_reason_upper = 66
    before_fact = factunit_shop(
        fact_context=knee_rope,
        fact_state=damaged_rope,
        fact_lower=before_damaged_reason_lower,
        fact_upper=before_damaged_reason_upper,
    )
    before_sue_belief.edit_plan_attr(ball_rope, factunit=before_fact)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [wx.DELETE, wx.belief_plan_factunit, ball_rope, knee_rope]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.fact_context) == knee_rope
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_reason_caseunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_belief.make_rope(knee_rope, damaged_str)
    before_sue_belief.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_belief.make_rope(knee_rope, bend_str)
    before_sue_belief.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_belief.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )

    after_sue_belief = copy_deepcopy(before_sue_belief)
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    after_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=damaged_reason_lower,
        reason_upper=damaged_reason_upper,
        reason_divisor=damaged_reason_divisor,
    )

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.INSERT,
        wx.belief_plan_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.reason_context) == knee_rope
    assert ball_beliefatom.get_value(wx.reason_state) == damaged_rope
    assert ball_beliefatom.get_value(wx.reason_lower) == damaged_reason_lower
    assert ball_beliefatom.get_value(wx.reason_upper) == damaged_reason_upper
    assert ball_beliefatom.get_value(wx.reason_divisor) == damaged_reason_divisor
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_reason_caseunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_belief.make_rope(knee_rope, damaged_str)
    before_sue_belief.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_belief.make_rope(knee_rope, bend_str)
    before_sue_belief.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_belief.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    before_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=damaged_reason_lower,
        reason_upper=damaged_reason_upper,
        reason_divisor=damaged_reason_divisor,
    )
    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_sue_belief.edit_plan_attr(
        ball_rope,
        reason_del_case_reason_context=knee_rope,
        reason_del_case_reason_state=damaged_rope,
    )

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.DELETE,
        wx.belief_plan_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.reason_context) == knee_rope
    assert ball_beliefatom.get_value(wx.reason_state) == damaged_rope
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_reason_caseunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_belief.make_rope(knee_rope, damaged_str)
    before_sue_belief.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_belief.make_rope(knee_rope, bend_str)
    before_sue_belief.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_belief.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )
    before_damaged_reason_lower = 111
    before_damaged_reason_upper = 777
    before_damaged_reason_divisor = 13
    before_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=before_damaged_reason_lower,
        reason_upper=before_damaged_reason_upper,
        reason_divisor=before_damaged_reason_divisor,
    )

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_damaged_reason_lower = 333
    after_damaged_reason_upper = 555
    after_damaged_reason_divisor = 78
    after_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=after_damaged_reason_lower,
        reason_upper=after_damaged_reason_upper,
        reason_divisor=after_damaged_reason_divisor,
    )

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.UPDATE,
        wx.belief_plan_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.reason_context) == knee_rope
    assert ball_beliefatom.get_value(wx.reason_state) == damaged_rope
    assert ball_beliefatom.get_value(wx.reason_lower) == after_damaged_reason_lower
    assert ball_beliefatom.get_value(wx.reason_upper) == after_damaged_reason_upper
    assert ball_beliefatom.get_value(wx.reason_divisor) == after_damaged_reason_divisor
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_reasonunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_belief.make_rope(knee_rope, medical_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    before_sue_belief.set_plan(planunit_shop(medical_str), knee_rope)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_medical_reason_active_requisite = False
    after_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_plan_active_requisite=after_medical_reason_active_requisite,
    )

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.INSERT,
        wx.belief_plan_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)

    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value("reason_context") == medical_rope
    assert (
        ball_beliefatom.get_value(wx.reason_active_requisite)
        == after_medical_reason_active_requisite
    )
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_reasonunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_belief.make_rope(knee_rope, medical_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    before_sue_belief.set_plan(planunit_shop(medical_str), knee_rope)
    before_medical_reason_active_requisite = True
    before_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_plan_active_requisite=before_medical_reason_active_requisite,
    )

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_medical_reason_active_requisite = False
    after_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_plan_active_requisite=after_medical_reason_active_requisite,
    )

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.UPDATE,
        wx.belief_plan_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value("reason_context") == medical_rope
    assert (
        ball_beliefatom.get_value(wx.reason_active_requisite)
        == after_medical_reason_active_requisite
    )
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_reasonunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_belief.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_belief.make_rope(knee_rope, medical_str)
    before_sue_belief.set_l1_plan(planunit_shop(knee_str))
    before_sue_belief.set_plan(planunit_shop(medical_str), knee_rope)
    before_medical_reason_active_requisite = True
    before_sue_belief.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_plan_active_requisite=before_medical_reason_active_requisite,
    )

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_ball_plan = after_sue_belief.get_plan_obj(ball_rope)
    after_ball_plan.del_reasonunit_reason_context(medical_rope)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.DELETE,
        wx.belief_plan_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value("reason_context") == medical_rope
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_partyunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_ball_planunit = after_sue_belief.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.add_party(xio_str)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.INSERT,
        wx.belief_plan_partyunit,
        ball_rope,
        xio_str,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.party_title) == xio_str
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_partyunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_belief.get_plan_obj(ball_rope)
    before_ball_planunit.laborunit.add_party(xio_str)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_ball_planunit = after_sue_belief.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.del_partyunit(xio_str)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.DELETE,
        wx.belief_plan_partyunit,
        ball_rope,
        xio_str,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.party_title) == xio_str
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_healerunit_insert_PlanUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_ball_planunit = after_sue_belief.get_plan_obj(ball_rope)
    after_ball_planunit.healerunit.set_healer_name(xio_str)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.INSERT,
        wx.belief_plan_healerunit,
        ball_rope,
        xio_str,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist)
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.healer_name) == xio_str
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_healerunit_insert_PlanUnitInsert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    after_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_belief.get_plan_obj(ball_rope)
    after_ball_planunit.healerunit.set_healer_name(xio_str)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.INSERT,
        wx.belief_plan_healerunit,
        ball_rope,
        xio_str,
    ]
    ball_beliefatom = get_from_nested_dict(sue_beliefdelta.beliefatoms, x_keylist, True)
    assert ball_beliefatom
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.healer_name) == xio_str
    assert get_beliefatom_total_count(sue_beliefdelta) == 3


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_healerunit_delete_PlanUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_belief.get_plan_obj(ball_rope)
    before_ball_planunit.healerunit.set_healer_name(xio_str)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_ball_planunit = after_sue_belief.get_plan_obj(ball_rope)
    after_ball_planunit.healerunit.del_healer_name(xio_str)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.DELETE,
        wx.belief_plan_healerunit,
        ball_rope,
        xio_str,
    ]
    ball_beliefatom = get_from_nested_dict(
        sue_beliefdelta.beliefatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_beliefatom
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.healer_name) == xio_str
    assert get_beliefatom_total_count(sue_beliefdelta) == 1


def test_BeliefDelta_add_all_different_beliefatoms_Creates_BeliefAtom_plan_healerunit_delete_PlanUnitDelete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_belief.add_voiceunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_belief.make_rope(sports_rope, ball_str)
    before_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_belief.get_plan_obj(ball_rope)
    before_ball_planunit.healerunit.set_healer_name(xio_str)

    after_sue_belief = copy_deepcopy(before_sue_belief)
    after_sue_belief.del_plan_obj(ball_rope)

    # WHEN
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    # THEN
    print(f"{print_beliefatom_keys(sue_beliefdelta)=}")
    x_keylist = [
        wx.DELETE,
        wx.belief_plan_healerunit,
        ball_rope,
        xio_str,
    ]
    ball_beliefatom = get_from_nested_dict(
        sue_beliefdelta.beliefatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_beliefatom
    assert ball_beliefatom.get_value(wx.plan_rope) == ball_rope
    assert ball_beliefatom.get_value(wx.healer_name) == xio_str
    assert get_beliefatom_total_count(sue_beliefdelta) == 2


def test_BeliefDelta_add_all_beliefatoms_Creates_BeliefAtoms():
    # ESTABLISH
    sue_str = "Sue"

    after_sue_belief = beliefunit_shop(sue_str)
    xio_str = "Xio"
    temp_xio_voiceunit = voiceunit_shop(xio_str)
    after_sue_belief.set_voiceunit(temp_xio_voiceunit, auto_set_membership=False)
    sports_str = "sports"
    sports_rope = after_sue_belief.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = after_sue_belief.make_rope(sports_rope, ball_str)
    after_sue_belief.set_plan(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_belief.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.add_party(xio_str)

    before_sue_belief = beliefunit_shop(sue_str)
    sue1_beliefdelta = beliefdelta_shop()
    sue1_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)
    print(f"{sue1_beliefdelta.get_ordered_beliefatoms()}")
    assert len(sue1_beliefdelta.get_ordered_beliefatoms()) == 4

    # WHEN
    sue2_beliefdelta = beliefdelta_shop()
    sue2_beliefdelta.add_all_beliefatoms(after_sue_belief)

    # THEN
    assert len(sue2_beliefdelta.get_ordered_beliefatoms()) == 4
    assert sue2_beliefdelta == sue1_beliefdelta
