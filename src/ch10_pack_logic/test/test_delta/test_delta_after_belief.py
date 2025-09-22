from src.ch04_group_logic.group import awardunit_shop
from src.ch05_reason_logic.reason import factunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_terms import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    awardee_title_str,
    begin_str,
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    belief_voice_membership_str,
    belief_voiceunit_str,
    beliefunit_str,
    close_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    give_force_str,
    gogo_want_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    healer_name_str,
    party_title_str,
    plan_rope_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
    stop_want_str,
    take_force_str,
    task_str,
    voice_name_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.test._util.example_deltas import get_beliefdelta_example1


def test_BeliefDelta_get_edited_belief_ReturnsObj_SimplestScenario():
    # ESTABLISH
    ex1_beliefdelta = beliefdelta_shop()

    # WHEN
    sue_str = "Sue"
    sue_tally = 55
    before_sue_beliefunit = beliefunit_shop(sue_str, tally=sue_tally)
    after_sue_beliefunit = ex1_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    assert after_sue_beliefunit.tally == sue_tally
    assert after_sue_beliefunit == before_sue_beliefunit


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnitSimpleAttrs():
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    sue_str = "Sue"

    sue_tally = 44
    before_sue_beliefunit = beliefunit_shop(sue_str, tally=sue_tally)

    dimen = beliefunit_str()
    x_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    new1_value = 55
    new1_arg = "tally"
    x_beliefatom.set_jvalue(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "max_tree_traverse"
    x_beliefatom.set_jvalue(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "credor_respect"
    x_beliefatom.set_jvalue(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "debtor_respect"
    x_beliefatom.set_jvalue(new4_arg, new4_value)
    new9_value = 55550000
    new9_arg = "fund_pool"
    x_beliefatom.set_jvalue(new9_arg, new9_value)
    new8_value = 0.5555
    new8_arg = "fund_iota"
    x_beliefatom.set_jvalue(new8_arg, new8_value)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    new6_value = 0.5
    new6_arg = "respect_bit"
    x_beliefatom.set_jvalue(new6_arg, new6_value)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    new7_value = 0.025
    new7_arg = "penny"
    x_beliefatom.set_jvalue(new7_arg, new7_value)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    # WHEN
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    print(f"{sue_beliefdelta.beliefatoms.keys()=}")
    assert after_sue_beliefunit.max_tree_traverse == new2_value
    assert after_sue_beliefunit.credor_respect == new3_value
    assert after_sue_beliefunit.debtor_respect == new4_value
    assert after_sue_beliefunit.tally == new1_value
    assert after_sue_beliefunit.tally != before_sue_beliefunit.tally
    assert after_sue_beliefunit.fund_pool == new9_value
    assert after_sue_beliefunit.fund_pool != before_sue_beliefunit.fund_pool
    assert after_sue_beliefunit.fund_iota == new8_value
    assert after_sue_beliefunit.fund_iota != before_sue_beliefunit.fund_iota
    assert after_sue_beliefunit.respect_bit == new6_value
    assert after_sue_beliefunit.respect_bit != before_sue_beliefunit.respect_bit
    assert after_sue_beliefunit.penny == new7_value
    assert after_sue_beliefunit.penny != before_sue_beliefunit.penny


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_voice():
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    sue_str = "Sue"

    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_sue_beliefunit.add_voiceunit(zia_str)

    dimen = belief_voiceunit_str()
    x_beliefatom = beliefatom_shop(dimen, DELETE_str())
    x_beliefatom.set_jkey(voice_name_str(), zia_str)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    # WHEN
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    print(f"{sue_beliefdelta.beliefatoms=}")
    assert after_sue_beliefunit != before_sue_beliefunit
    assert after_sue_beliefunit.voice_exists(yao_str)
    assert after_sue_beliefunit.voice_exists(zia_str) is False


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_voice():
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    sue_str = "Sue"

    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_beliefunit.add_voiceunit(yao_str)
    assert before_sue_beliefunit.voice_exists(yao_str)
    assert before_sue_beliefunit.voice_exists(zia_str) is False

    # WHEN
    dimen = belief_voiceunit_str()
    x_beliefatom = beliefatom_shop(dimen, INSERT_str())
    x_beliefatom.set_jkey(voice_name_str(), zia_str)
    x_voice_cred_points = 55
    x_voice_debt_points = 66
    x_beliefatom.set_jvalue("voice_cred_points", x_voice_cred_points)
    x_beliefatom.set_jvalue("voice_debt_points", x_voice_debt_points)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    print(f"{sue_beliefdelta.beliefatoms.keys()=}")
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    yao_voiceunit = after_sue_beliefunit.get_voice(yao_str)
    zia_voiceunit = after_sue_beliefunit.get_voice(zia_str)
    assert yao_voiceunit is not None
    assert zia_voiceunit is not None
    assert zia_voiceunit.voice_cred_points == x_voice_cred_points
    assert zia_voiceunit.voice_debt_points == x_voice_debt_points


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_update_voice():
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    sue_str = "Sue"

    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_beliefunit.add_voiceunit(yao_str)
    assert before_sue_beliefunit.get_voice(yao_str).voice_cred_points == 1

    # WHEN
    dimen = belief_voiceunit_str()
    x_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    x_beliefatom.set_jkey(voice_name_str(), yao_str)
    yao_voice_cred_points = 55
    x_beliefatom.set_jvalue("voice_cred_points", yao_voice_cred_points)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    print(f"{sue_beliefdelta.beliefatoms.keys()=}")
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    yao_voice = after_sue_beliefunit.get_voice(yao_str)
    assert yao_voice.voice_cred_points == yao_voice_cred_points


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_sue_beliefunit.add_voiceunit(zia_str)
    before_sue_beliefunit.add_voiceunit(bob_str)
    yao_voiceunit = before_sue_beliefunit.get_voice(yao_str)
    zia_voiceunit = before_sue_beliefunit.get_voice(zia_str)
    bob_voiceunit = before_sue_beliefunit.get_voice(bob_str)
    run_str = ";runners"
    yao_voiceunit.add_membership(run_str)
    zia_voiceunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_voiceunit.add_membership(fly_str)
    zia_voiceunit.add_membership(fly_str)
    bob_voiceunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_beliefunit.get_voiceunit_group_titles_dict()
    assert len(before_group_titles_dict.get(run_str)) == 2
    assert len(before_group_titles_dict.get(fly_str)) == 3

    # WHEN
    yao_beliefatom = beliefatom_shop(belief_voice_membership_str(), DELETE_str())
    yao_beliefatom.set_jkey(group_title_str(), run_str)
    yao_beliefatom.set_jkey(voice_name_str(), yao_str)
    # print(f"{yao_beliefatom=}")
    zia_beliefatom = beliefatom_shop(belief_voice_membership_str(), DELETE_str())
    zia_beliefatom.set_jkey(group_title_str(), fly_str)
    zia_beliefatom.set_jkey(voice_name_str(), zia_str)
    # print(f"{zia_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_beliefdelta.set_beliefatom(zia_beliefatom)
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    after_group_titles_dict = after_sue_beliefunit.get_voiceunit_group_titles_dict()
    assert len(after_group_titles_dict.get(run_str)) == 1
    assert len(after_group_titles_dict.get(fly_str)) == 2


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_membership():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_sue_beliefunit.add_voiceunit(zia_str)
    before_sue_beliefunit.add_voiceunit(bob_str)
    run_str = ";runners"
    zia_voiceunit = before_sue_beliefunit.get_voice(zia_str)
    zia_voiceunit.add_membership(run_str)
    before_group_titles = before_sue_beliefunit.get_voiceunit_group_titles_dict()
    assert len(before_group_titles.get(run_str)) == 1

    # WHEN
    yao_beliefatom = beliefatom_shop(belief_voice_membership_str(), INSERT_str())
    yao_beliefatom.set_jkey(group_title_str(), run_str)
    yao_beliefatom.set_jkey(voice_name_str(), yao_str)
    yao_run_group_cred_points = 17
    yao_beliefatom.set_jvalue("group_cred_points", yao_run_group_cred_points)
    print(f"{yao_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(yao_beliefatom)
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    after_group_titles = after_sue_beliefunit.get_voiceunit_group_titles_dict()
    assert len(after_group_titles.get(run_str)) == 2
    after_yao_voiceunit = after_sue_beliefunit.get_voice(yao_str)
    after_yao_run_membership = after_yao_voiceunit.get_membership(run_str)
    assert after_yao_run_membership is not None
    assert after_yao_run_membership.group_cred_points == yao_run_group_cred_points


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_update_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_yao_voiceunit = before_sue_beliefunit.get_voice(yao_str)
    run_str = ";runners"
    old_yao_run_group_cred_points = 3
    before_yao_voiceunit.add_membership(run_str, old_yao_run_group_cred_points)
    yao_run_membership = before_yao_voiceunit.get_membership(run_str)
    assert yao_run_membership.group_cred_points == old_yao_run_group_cred_points
    assert yao_run_membership.group_debt_points == 1

    # WHEN
    yao_beliefatom = beliefatom_shop(belief_voice_membership_str(), UPDATE_str())
    yao_beliefatom.set_jkey(group_title_str(), run_str)
    yao_beliefatom.set_jkey(voice_name_str(), yao_str)
    new_yao_run_group_cred_points = 7
    new_yao_run_group_debt_points = 11
    yao_beliefatom.set_jvalue(group_cred_points_str(), new_yao_run_group_cred_points)
    yao_beliefatom.set_jvalue(group_debt_points_str(), new_yao_run_group_debt_points)
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(yao_beliefatom)
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    after_yao_voiceunit = after_sue_beliefunit.get_voice(yao_str)
    after_yao_run_membership = after_yao_voiceunit.get_membership(run_str)
    assert after_yao_run_membership.group_cred_points == new_yao_run_group_cred_points
    assert after_yao_run_membership.group_debt_points == new_yao_run_group_debt_points


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_planunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_beliefunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_beliefunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_beliefunit.make_rope(sports_rope, disc_str)
    before_sue_beliefunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_beliefunit.set_plan(planunit_shop(disc_str), sports_rope)
    delete_disc_beliefatom = beliefatom_shop(belief_planunit_str(), DELETE_str())
    delete_disc_beliefatom.set_jkey(plan_rope_str(), disc_rope)
    print(f"{disc_rope=}")
    delete_disc_beliefatom.set_jkey(plan_rope_str(), disc_rope)
    print(f"{delete_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(delete_disc_beliefatom)
    assert before_sue_beliefunit.plan_exists(ball_rope)
    assert before_sue_beliefunit.plan_exists(disc_rope)

    # WHEN
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    assert after_sue_beliefunit.plan_exists(ball_rope)
    assert after_sue_beliefunit.plan_exists(disc_rope) is False


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_planunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_beliefunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_beliefunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_beliefunit.make_rope(sports_rope, disc_str)
    before_sue_beliefunit.set_plan(planunit_shop(ball_str), sports_rope)
    assert before_sue_beliefunit.plan_exists(ball_rope)
    assert before_sue_beliefunit.plan_exists(disc_rope) is False

    # WHEN
    # x_addin = 140
    x_gogo_want = 1000
    x_stop_want = 1700
    # x_denom = 17
    # x_numor = 10
    x_task = True
    insert_disc_beliefatom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    insert_disc_beliefatom.set_jkey(plan_rope_str(), disc_rope)
    # insert_disc_beliefatom.set_jvalue(addin_str(), x_addin)
    # insert_disc_beliefatom.set_jvalue(begin_str(), x_begin)
    # insert_disc_beliefatom.set_jvalue(close_str(), x_close)
    # insert_disc_beliefatom.set_jvalue(denom_str(), x_denom)
    # insert_disc_beliefatom.set_jvalue(numor_str(), x_numor)
    insert_disc_beliefatom.set_jvalue(task_str(), x_task)
    insert_disc_beliefatom.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_beliefatom.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(insert_disc_beliefatom)
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    assert after_sue_beliefunit.plan_exists(ball_rope)
    assert after_sue_beliefunit.plan_exists(disc_rope)
    disc_plan = after_sue_beliefunit.get_plan_obj(disc_rope)
    assert disc_plan.gogo_want == x_gogo_want
    assert disc_plan.stop_want == x_stop_want


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_update_planunit_SimpleAttributes():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_beliefunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_beliefunit.make_rope(sports_rope, ball_str)
    before_sue_beliefunit.set_plan(planunit_shop(ball_str), sports_rope)

    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    # x_numor = 10
    x_gogo_want = 1222
    x_stop_want = 1333
    x_task = True
    insert_disc_beliefatom = beliefatom_shop(belief_planunit_str(), UPDATE_str())
    insert_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    # insert_disc_beliefatom.set_jvalue(addin_str(), x_addin)
    insert_disc_beliefatom.set_jvalue(begin_str(), x_begin)
    insert_disc_beliefatom.set_jvalue(close_str(), x_close)
    # insert_disc_beliefatom.set_jvalue(denom_str(), x_denom)
    # insert_disc_beliefatom.set_jvalue(numor_str(), x_numor)
    insert_disc_beliefatom.set_jvalue(task_str(), x_task)
    insert_disc_beliefatom.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_beliefatom.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(insert_disc_beliefatom)
    assert before_sue_beliefunit.get_plan_obj(ball_rope).begin is None
    assert before_sue_beliefunit.get_plan_obj(ball_rope).close is None
    assert before_sue_beliefunit.get_plan_obj(ball_rope).task is False
    assert before_sue_beliefunit.get_plan_obj(ball_rope).gogo_want is None
    assert before_sue_beliefunit.get_plan_obj(ball_rope).stop_want is None

    # WHEN
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    assert after_sue_beliefunit.get_plan_obj(ball_rope).begin == x_begin
    assert after_sue_beliefunit.get_plan_obj(ball_rope).close == x_close
    assert after_sue_beliefunit.get_plan_obj(ball_rope).gogo_want == x_gogo_want
    assert after_sue_beliefunit.get_plan_obj(ball_rope).stop_want == x_stop_want
    assert after_sue_beliefunit.get_plan_obj(ball_rope).task


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_plan_awardunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_sue_beliefunit.add_voiceunit(zia_str)
    before_sue_beliefunit.add_voiceunit(bob_str)
    yao_voiceunit = before_sue_beliefunit.get_voice(yao_str)
    zia_voiceunit = before_sue_beliefunit.get_voice(zia_str)
    bob_voiceunit = before_sue_beliefunit.get_voice(bob_str)
    run_str = ";runners"
    yao_voiceunit.add_membership(run_str)
    zia_voiceunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_voiceunit.add_membership(fly_str)
    zia_voiceunit.add_membership(fly_str)
    bob_voiceunit.add_membership(fly_str)

    sports_str = "sports"
    sports_rope = before_sue_beliefunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_beliefunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_beliefunit.make_rope(sports_rope, disc_str)
    before_sue_beliefunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_beliefunit.set_plan(planunit_shop(disc_str), sports_rope)
    before_sue_beliefunit.edit_plan_attr(ball_rope, awardunit=awardunit_shop(run_str))
    before_sue_beliefunit.edit_plan_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    before_sue_beliefunit.edit_plan_attr(disc_rope, awardunit=awardunit_shop(run_str))
    before_sue_beliefunit.edit_plan_attr(disc_rope, awardunit=awardunit_shop(fly_str))
    assert len(before_sue_beliefunit.get_plan_obj(ball_rope).awardunits) == 2
    assert len(before_sue_beliefunit.get_plan_obj(disc_rope).awardunits) == 2

    # WHEN
    delete_disc_beliefatom = beliefatom_shop(belief_plan_awardunit_str(), DELETE_str())
    delete_disc_beliefatom.set_jkey(plan_rope_str(), disc_rope)
    delete_disc_beliefatom.set_jkey(awardee_title_str(), fly_str)
    print(f"{delete_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(delete_disc_beliefatom)
    after_sue_beliefunit = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    assert len(after_sue_beliefunit.get_plan_obj(ball_rope).awardunits) == 2
    assert len(after_sue_beliefunit.get_plan_obj(disc_rope).awardunits) == 1


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_update_plan_awardunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_sue_beliefunit.add_voiceunit(zia_str)
    yao_voiceunit = before_sue_beliefunit.get_voice(yao_str)
    run_str = ";runners"
    yao_voiceunit.add_membership(run_str)

    sports_str = "sports"
    sports_rope = before_sue_beliefunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_beliefunit.make_rope(sports_rope, ball_str)
    before_sue_beliefunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_beliefunit.edit_plan_attr(ball_rope, awardunit=awardunit_shop(run_str))
    run_awardunit = before_sue_beliefunit.get_plan_obj(ball_rope).awardunits.get(
        run_str
    )
    assert run_awardunit.give_force == 1
    assert run_awardunit.take_force == 1

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_beliefatom = beliefatom_shop(belief_plan_awardunit_str(), UPDATE_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(awardee_title_str(), run_str)
    update_disc_beliefatom.set_jvalue(give_force_str(), x_give_force)
    update_disc_beliefatom.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    run_awardunit = after_sue_au.get_plan_obj(ball_rope).awardunits.get(run_str)
    print(f"{run_awardunit.give_force=}")
    assert run_awardunit.give_force == x_give_force
    assert run_awardunit.take_force == x_take_force


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_plan_awardunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_sue_beliefunit.add_voiceunit(zia_str)
    run_str = ";runners"
    yao_voiceunit = before_sue_beliefunit.get_voice(yao_str)
    yao_voiceunit.add_membership(run_str)
    sports_str = "sports"
    sports_rope = before_sue_beliefunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_beliefunit.make_rope(sports_rope, ball_str)
    before_sue_beliefunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_plan = before_sue_beliefunit.get_plan_obj(ball_rope)
    assert before_ball_plan.awardunits.get(run_str) is None

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_beliefatom = beliefatom_shop(belief_plan_awardunit_str(), INSERT_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(awardee_title_str(), run_str)
    update_disc_beliefatom.set_jvalue(give_force_str(), x_give_force)
    update_disc_beliefatom.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.awardunits.get(run_str) is not None


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_plan_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(damaged_str), knee_rope)
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.factunits == {}

    # WHEN
    damaged_fact_lower = 55
    damaged_fact_upper = 66
    update_disc_beliefatom = beliefatom_shop(belief_plan_factunit_str(), INSERT_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(fact_context_str(), knee_rope)
    update_disc_beliefatom.set_jvalue(fact_state_str(), damaged_rope)
    update_disc_beliefatom.set_jvalue(fact_lower_str(), damaged_fact_lower)
    update_disc_beliefatom.set_jvalue(fact_upper_str(), damaged_fact_upper)
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits != {}
    assert after_ball_plan.factunits.get(knee_rope) is not None
    assert after_ball_plan.factunits.get(knee_rope).fact_context == knee_rope
    assert after_ball_plan.factunits.get(knee_rope).fact_state == damaged_rope
    assert after_ball_plan.factunits.get(knee_rope).fact_lower == damaged_fact_lower
    assert after_ball_plan.factunits.get(knee_rope).fact_upper == damaged_fact_upper


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_plan_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(damaged_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope,
        factunit=factunit_shop(fact_context=knee_rope, fact_state=damaged_rope),
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.factunits != {}
    assert before_ball_plan.factunits.get(knee_rope) is not None

    # WHEN
    update_disc_beliefatom = beliefatom_shop(belief_plan_factunit_str(), DELETE_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(fact_context_str(), knee_rope)
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits == {}


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_update_plan_factunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(damaged_str), knee_rope)
    before_sue_au.set_plan(planunit_shop(medical_str), knee_rope)
    before_knee_factunit = factunit_shop(knee_rope, damaged_rope)
    before_sue_au.edit_plan_attr(ball_rope, factunit=before_knee_factunit)
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.factunits != {}
    assert before_ball_plan.factunits.get(knee_rope) is not None
    assert before_ball_plan.factunits.get(knee_rope).fact_state == damaged_rope
    assert before_ball_plan.factunits.get(knee_rope).fact_lower is None
    assert before_ball_plan.factunits.get(knee_rope).fact_upper is None

    # WHEN
    medical_fact_lower = 45
    medical_fact_upper = 77
    update_disc_beliefatom = beliefatom_shop(belief_plan_factunit_str(), UPDATE_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(fact_context_str(), knee_rope)
    update_disc_beliefatom.set_jvalue(fact_state_str(), medical_rope)
    update_disc_beliefatom.set_jvalue(fact_lower_str(), medical_fact_lower)
    update_disc_beliefatom.set_jvalue(fact_upper_str(), medical_fact_upper)
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits != {}
    assert after_ball_plan.factunits.get(knee_rope) is not None
    assert after_ball_plan.factunits.get(knee_rope).fact_state == medical_rope
    assert after_ball_plan.factunits.get(knee_rope).fact_lower == medical_fact_lower
    assert after_ball_plan.factunits.get(knee_rope).fact_upper == medical_fact_upper


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_update_plan_reason_caseunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(damaged_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.reasonunits != {}
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit is not None
    damaged_caseunit = before_knee_reasonunit.get_case(damaged_rope)
    assert damaged_caseunit.reason_state == damaged_rope
    assert damaged_caseunit.reason_lower is None
    assert damaged_caseunit.reason_upper is None
    assert damaged_caseunit.reason_divisor is None

    # WHEN
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    update_disc_beliefatom = beliefatom_shop(
        belief_plan_reason_caseunit_str(), UPDATE_str()
    )
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(reason_context_str(), knee_rope)
    update_disc_beliefatom.set_jkey(reason_state_str(), damaged_rope)
    update_disc_beliefatom.set_jvalue(reason_lower_str(), damaged_reason_lower)
    update_disc_beliefatom.set_jvalue(reason_upper_str(), damaged_reason_upper)
    update_disc_beliefatom.set_jvalue(reason_divisor_str(), damaged_reason_divisor)
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    after_damaged_caseunit = after_knee_reasonunit.get_case(damaged_rope)
    assert after_damaged_caseunit.reason_state == damaged_rope
    assert after_damaged_caseunit.reason_lower == damaged_reason_lower
    assert after_damaged_caseunit.reason_upper == damaged_reason_upper
    assert after_damaged_caseunit.reason_divisor == damaged_reason_divisor


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_plan_reason_caseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(damaged_str), knee_rope)
    before_sue_au.set_plan(planunit_shop(medical_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_case(damaged_rope) is not None
    assert before_knee_reasonunit.get_case(medical_rope) is None

    # WHEN
    medical_reason_lower = 45
    medical_reason_upper = 77
    medical_reason_divisor = 3
    update_disc_beliefatom = beliefatom_shop(
        belief_plan_reason_caseunit_str(), INSERT_str()
    )
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(reason_context_str(), knee_rope)
    update_disc_beliefatom.set_jkey(reason_state_str(), medical_rope)
    update_disc_beliefatom.set_jvalue(reason_lower_str(), medical_reason_lower)
    update_disc_beliefatom.set_jvalue(reason_upper_str(), medical_reason_upper)
    update_disc_beliefatom.set_jvalue(reason_divisor_str(), medical_reason_divisor)
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    after_medical_caseunit = after_knee_reasonunit.get_case(medical_rope)
    assert after_medical_caseunit is not None
    assert after_medical_caseunit.reason_state == medical_rope
    assert after_medical_caseunit.reason_lower == medical_reason_lower
    assert after_medical_caseunit.reason_upper == medical_reason_upper
    assert after_medical_caseunit.reason_divisor == medical_reason_divisor


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_plan_reason_caseunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(damaged_str), knee_rope)
    before_sue_au.set_plan(planunit_shop(medical_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=medical_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_case(damaged_rope) is not None
    assert before_knee_reasonunit.get_case(medical_rope) is not None

    # WHEN
    update_disc_beliefatom = beliefatom_shop(
        belief_plan_reason_caseunit_str(), DELETE_str()
    )
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(reason_context_str(), knee_rope)
    update_disc_beliefatom.set_jkey(reason_state_str(), medical_rope)
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit.get_case(damaged_rope) is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_plan_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(medical_str), knee_rope)
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.get_reasonunit(knee_rope) is None

    # WHEN
    medical_reason_active_requisite = True
    update_disc_beliefatom = beliefatom_shop(belief_plan_reasonunit_str(), INSERT_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey("reason_context", knee_rope)
    update_disc_beliefatom.set_jvalue(
        reason_active_requisite_str(),
        medical_reason_active_requisite,
    )
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None
    assert (
        after_knee_reasonunit.reason_active_requisite == medical_reason_active_requisite
    )


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_update_plan_reasonunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_medical_reason_active_requisite = False
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(medical_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_plan_active_requisite=before_medical_reason_active_requisite,
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_ball_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_ball_reasonunit is not None
    assert (
        before_ball_reasonunit.reason_active_requisite
        == before_medical_reason_active_requisite
    )

    # WHEN
    after_medical_reason_active_requisite = True
    update_disc_beliefatom = beliefatom_shop(belief_plan_reasonunit_str(), UPDATE_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey("reason_context", knee_rope)
    update_disc_beliefatom.set_jvalue(
        reason_active_requisite_str(),
        after_medical_reason_active_requisite,
    )
    # print(f"{update_disc_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None
    assert (
        after_knee_reasonunit.reason_active_requisite
        == after_medical_reason_active_requisite
    )


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_plan_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_reason_active_requisite = False
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_plan_active_requisite=medical_reason_active_requisite,
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.get_reasonunit(knee_rope) is not None

    # WHEN
    update_disc_beliefatom = beliefatom_shop(belief_plan_reasonunit_str(), DELETE_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey("reason_context", knee_rope)
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.get_reasonunit(knee_rope) is None


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_plan_partyunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_voiceunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_planunit.laborunit._partys == {}

    # WHEN
    update_disc_beliefatom = beliefatom_shop(belief_plan_partyunit_str(), INSERT_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(party_title_str(), yao_str)
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.laborunit._partys != set()
    assert after_ball_planunit.laborunit.get_partyunit(yao_str) is not None


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_plan_partyunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_voiceunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    before_ball_planunit.laborunit.add_party(yao_str)
    assert before_ball_planunit.laborunit._partys != set()
    assert before_ball_planunit.laborunit.get_partyunit(yao_str) is not None

    # WHEN
    update_disc_beliefatom = beliefatom_shop(belief_plan_partyunit_str(), DELETE_str())
    update_disc_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_beliefatom.set_jkey(party_title_str(), yao_str)
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(update_disc_beliefatom)
    print(f"{before_sue_au.get_plan_obj(ball_rope).laborunit=}")
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.laborunit._partys == {}


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_insert_plan_healerunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_voiceunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_planunit.healerunit._healer_names == set()
    assert not before_ball_planunit.healerunit.healer_name_exists(yao_str)

    # WHEN
    x_beliefatom = beliefatom_shop(belief_plan_healerunit_str(), INSERT_str())
    x_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    x_beliefatom.set_jkey(healer_name_str(), yao_str)
    print(f"{x_beliefatom=}")
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.healerunit._healer_names != set()
    assert after_ball_planunit.healerunit.healer_name_exists(yao_str)


def test_BeliefDelta_get_edited_belief_ReturnsObj_BeliefUnit_delete_plan_healerunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = beliefunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_voiceunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    before_ball_planunit.healerunit.set_healer_name(yao_str)
    assert before_ball_planunit.healerunit._healer_names != set()
    assert before_ball_planunit.healerunit.healer_name_exists(yao_str)

    # WHEN
    x_beliefatom = beliefatom_shop(belief_plan_healerunit_str(), DELETE_str())
    x_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    x_beliefatom.set_jkey(healer_name_str(), yao_str)
    sue_beliefdelta = beliefdelta_shop()
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    print(f"{before_sue_au.get_plan_obj(ball_rope).laborunit=}")
    after_sue_au = sue_beliefdelta.get_edited_belief(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.healerunit._healer_names == set()
    assert not after_ball_planunit.healerunit.healer_name_exists(yao_str)


def test_BeliefDelta_get_beliefdelta_example1_ContainsBeliefAtoms():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_beliefunit.add_voiceunit(yao_str)
    before_sue_beliefunit.add_voiceunit(zia_str)
    before_sue_beliefunit.add_voiceunit(bob_str)
    yao_voiceunit = before_sue_beliefunit.get_voice(yao_str)
    zia_voiceunit = before_sue_beliefunit.get_voice(zia_str)
    bob_voiceunit = before_sue_beliefunit.get_voice(bob_str)
    run_str = ";runners"
    yao_voiceunit.add_membership(run_str)
    zia_voiceunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_voiceunit.add_membership(fly_str)
    bob_voiceunit.add_membership(fly_str)
    assert before_sue_beliefunit.tally != 55
    assert before_sue_beliefunit.max_tree_traverse != 66
    assert before_sue_beliefunit.credor_respect != 77
    assert before_sue_beliefunit.debtor_respect != 88
    assert before_sue_beliefunit.voice_exists(yao_str)
    assert before_sue_beliefunit.voice_exists(zia_str)
    assert yao_voiceunit.get_membership(fly_str) is not None
    assert bob_voiceunit.get_membership(fly_str) is not None

    # WHEN
    ex1_beliefdelta = get_beliefdelta_example1()
    after_sue_beliefunit = ex1_beliefdelta.get_edited_belief(before_sue_beliefunit)

    # THEN
    assert after_sue_beliefunit.tally == 55
    assert after_sue_beliefunit.max_tree_traverse == 66
    assert after_sue_beliefunit.credor_respect == 77
    assert after_sue_beliefunit.debtor_respect == 88
    assert after_sue_beliefunit.voice_exists(yao_str)
    assert after_sue_beliefunit.voice_exists(zia_str) is False
