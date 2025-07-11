from src.a01_term_logic.rope import get_parent_rope, get_tail_label
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    awardee_title_str,
    begin_str,
    believer_person_membership_str,
    believer_personunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_premiseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
    close_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    give_force_str,
    gogo_want_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    person_name_str,
    plan_rope_str,
    rplan_active_requisite_str,
    stop_want_str,
    take_force_str,
    task_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.test._util.example_deltas import get_believerdelta_example1


def test_BelieverDelta_get_edited_believer_ReturnsObj_SimplestScenario():
    # ESTABLISH
    ex1_believerdelta = believerdelta_shop()

    # WHEN
    sue_str = "Sue"
    sue_tally = 55
    before_sue_believerunit = believerunit_shop(sue_str, tally=sue_tally)
    after_sue_believerunit = ex1_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    assert after_sue_believerunit.tally == sue_tally
    assert after_sue_believerunit == before_sue_believerunit


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnitSimpleAttrs():
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    sue_str = "Sue"

    sue_tally = 44
    before_sue_believerunit = believerunit_shop(sue_str, tally=sue_tally)

    dimen = believerunit_str()
    x_believeratom = believeratom_shop(dimen, UPDATE_str())
    new1_value = 55
    new1_arg = "tally"
    x_believeratom.set_jvalue(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "max_tree_traverse"
    x_believeratom.set_jvalue(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "credor_respect"
    x_believeratom.set_jvalue(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "debtor_respect"
    x_believeratom.set_jvalue(new4_arg, new4_value)
    new9_value = 55550000
    new9_arg = "fund_pool"
    x_believeratom.set_jvalue(new9_arg, new9_value)
    new8_value = 0.5555
    new8_arg = "fund_iota"
    x_believeratom.set_jvalue(new8_arg, new8_value)
    sue_believerdelta.set_believeratom(x_believeratom)
    new6_value = 0.5
    new6_arg = "respect_bit"
    x_believeratom.set_jvalue(new6_arg, new6_value)
    sue_believerdelta.set_believeratom(x_believeratom)
    new7_value = 0.025
    new7_arg = "penny"
    x_believeratom.set_jvalue(new7_arg, new7_value)
    sue_believerdelta.set_believeratom(x_believeratom)

    # WHEN
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    print(f"{sue_believerdelta.believeratoms.keys()=}")
    assert after_sue_believerunit.max_tree_traverse == new2_value
    assert after_sue_believerunit.credor_respect == new3_value
    assert after_sue_believerunit.debtor_respect == new4_value
    assert after_sue_believerunit.tally == new1_value
    assert after_sue_believerunit.tally != before_sue_believerunit.tally
    assert after_sue_believerunit.fund_pool == new9_value
    assert after_sue_believerunit.fund_pool != before_sue_believerunit.fund_pool
    assert after_sue_believerunit.fund_iota == new8_value
    assert after_sue_believerunit.fund_iota != before_sue_believerunit.fund_iota
    assert after_sue_believerunit.respect_bit == new6_value
    assert after_sue_believerunit.respect_bit != before_sue_believerunit.respect_bit
    assert after_sue_believerunit.penny == new7_value
    assert after_sue_believerunit.penny != before_sue_believerunit.penny


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_person():
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    sue_str = "Sue"

    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_believerunit.add_personunit(yao_str)
    before_sue_believerunit.add_personunit(zia_str)

    dimen = believer_personunit_str()
    x_believeratom = believeratom_shop(dimen, DELETE_str())
    x_believeratom.set_jkey(person_name_str(), zia_str)
    sue_believerdelta.set_believeratom(x_believeratom)

    # WHEN
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    print(f"{sue_believerdelta.believeratoms=}")
    assert after_sue_believerunit != before_sue_believerunit
    assert after_sue_believerunit.person_exists(yao_str)
    assert after_sue_believerunit.person_exists(zia_str) is False


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_person():
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    sue_str = "Sue"

    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_believerunit.add_personunit(yao_str)
    assert before_sue_believerunit.person_exists(yao_str)
    assert before_sue_believerunit.person_exists(zia_str) is False

    # WHEN
    dimen = believer_personunit_str()
    x_believeratom = believeratom_shop(dimen, INSERT_str())
    x_believeratom.set_jkey(person_name_str(), zia_str)
    x_person_cred_points = 55
    x_person_debt_points = 66
    x_believeratom.set_jvalue("person_cred_points", x_person_cred_points)
    x_believeratom.set_jvalue("person_debt_points", x_person_debt_points)
    sue_believerdelta.set_believeratom(x_believeratom)
    print(f"{sue_believerdelta.believeratoms.keys()=}")
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    yao_personunit = after_sue_believerunit.get_person(yao_str)
    zia_personunit = after_sue_believerunit.get_person(zia_str)
    assert yao_personunit is not None
    assert zia_personunit is not None
    assert zia_personunit.person_cred_points == x_person_cred_points
    assert zia_personunit.person_debt_points == x_person_debt_points


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_update_person():
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    sue_str = "Sue"

    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_believerunit.add_personunit(yao_str)
    assert before_sue_believerunit.get_person(yao_str).person_cred_points == 1

    # WHEN
    dimen = believer_personunit_str()
    x_believeratom = believeratom_shop(dimen, UPDATE_str())
    x_believeratom.set_jkey(person_name_str(), yao_str)
    yao_person_cred_points = 55
    x_believeratom.set_jvalue("person_cred_points", yao_person_cred_points)
    sue_believerdelta.set_believeratom(x_believeratom)
    print(f"{sue_believerdelta.believeratoms.keys()=}")
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    yao_person = after_sue_believerunit.get_person(yao_str)
    assert yao_person.person_cred_points == yao_person_cred_points


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_membership():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_believerunit.add_personunit(yao_str)
    before_sue_believerunit.add_personunit(zia_str)
    before_sue_believerunit.add_personunit(bob_str)
    yao_personunit = before_sue_believerunit.get_person(yao_str)
    zia_personunit = before_sue_believerunit.get_person(zia_str)
    bob_personunit = before_sue_believerunit.get_person(bob_str)
    run_str = ";runners"
    yao_personunit.add_membership(run_str)
    zia_personunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_personunit.add_membership(fly_str)
    zia_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)
    before_group_titles_dict = (
        before_sue_believerunit.get_personunit_group_titles_dict()
    )
    assert len(before_group_titles_dict.get(run_str)) == 2
    assert len(before_group_titles_dict.get(fly_str)) == 3

    # WHEN
    yao_believeratom = believeratom_shop(believer_person_membership_str(), DELETE_str())
    yao_believeratom.set_jkey(group_title_str(), run_str)
    yao_believeratom.set_jkey(person_name_str(), yao_str)
    # print(f"{yao_believeratom=}")
    zia_believeratom = believeratom_shop(believer_person_membership_str(), DELETE_str())
    zia_believeratom.set_jkey(group_title_str(), fly_str)
    zia_believeratom.set_jkey(person_name_str(), zia_str)
    # print(f"{zia_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(yao_believeratom)
    sue_believerdelta.set_believeratom(zia_believeratom)
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    after_group_titles_dict = after_sue_believerunit.get_personunit_group_titles_dict()
    assert len(after_group_titles_dict.get(run_str)) == 1
    assert len(after_group_titles_dict.get(fly_str)) == 2


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_membership():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_believerunit.add_personunit(yao_str)
    before_sue_believerunit.add_personunit(zia_str)
    before_sue_believerunit.add_personunit(bob_str)
    run_str = ";runners"
    zia_personunit = before_sue_believerunit.get_person(zia_str)
    zia_personunit.add_membership(run_str)
    before_group_titles = before_sue_believerunit.get_personunit_group_titles_dict()
    assert len(before_group_titles.get(run_str)) == 1

    # WHEN
    yao_believeratom = believeratom_shop(believer_person_membership_str(), INSERT_str())
    yao_believeratom.set_jkey(group_title_str(), run_str)
    yao_believeratom.set_jkey(person_name_str(), yao_str)
    yao_run_group_cred_points = 17
    yao_believeratom.set_jvalue("group_cred_points", yao_run_group_cred_points)
    print(f"{yao_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(yao_believeratom)
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    after_group_titles = after_sue_believerunit.get_personunit_group_titles_dict()
    assert len(after_group_titles.get(run_str)) == 2
    after_yao_personunit = after_sue_believerunit.get_person(yao_str)
    after_yao_run_membership = after_yao_personunit.get_membership(run_str)
    assert after_yao_run_membership is not None
    assert after_yao_run_membership.group_cred_points == yao_run_group_cred_points


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_update_membership():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_believerunit.add_personunit(yao_str)
    before_yao_personunit = before_sue_believerunit.get_person(yao_str)
    run_str = ";runners"
    old_yao_run_group_cred_points = 3
    before_yao_personunit.add_membership(run_str, old_yao_run_group_cred_points)
    yao_run_membership = before_yao_personunit.get_membership(run_str)
    assert yao_run_membership.group_cred_points == old_yao_run_group_cred_points
    assert yao_run_membership.group_debt_points == 1

    # WHEN
    yao_believeratom = believeratom_shop(believer_person_membership_str(), UPDATE_str())
    yao_believeratom.set_jkey(group_title_str(), run_str)
    yao_believeratom.set_jkey(person_name_str(), yao_str)
    new_yao_run_group_cred_points = 7
    new_yao_run_group_debt_points = 11
    yao_believeratom.set_jvalue(group_cred_points_str(), new_yao_run_group_cred_points)
    yao_believeratom.set_jvalue(group_debt_points_str(), new_yao_run_group_debt_points)
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(yao_believeratom)
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    after_yao_personunit = after_sue_believerunit.get_person(yao_str)
    after_yao_run_membership = after_yao_personunit.get_membership(run_str)
    assert after_yao_run_membership.group_cred_points == new_yao_run_group_cred_points
    assert after_yao_run_membership.group_debt_points == new_yao_run_group_debt_points


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_planunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believerunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believerunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_believerunit.make_rope(sports_rope, disc_str)
    before_sue_believerunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_believerunit.set_plan(planunit_shop(disc_str), sports_rope)
    delete_disc_believeratom = believeratom_shop(believer_planunit_str(), DELETE_str())
    delete_disc_believeratom.set_jkey(plan_rope_str(), disc_rope)
    print(f"{disc_rope=}")
    delete_disc_believeratom.set_jkey(plan_rope_str(), disc_rope)
    print(f"{delete_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(delete_disc_believeratom)
    assert before_sue_believerunit.plan_exists(ball_rope)
    assert before_sue_believerunit.plan_exists(disc_rope)

    # WHEN
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    assert after_sue_believerunit.plan_exists(ball_rope)
    assert after_sue_believerunit.plan_exists(disc_rope) is False


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_planunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believerunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believerunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_believerunit.make_rope(sports_rope, disc_str)
    before_sue_believerunit.set_plan(planunit_shop(ball_str), sports_rope)
    assert before_sue_believerunit.plan_exists(ball_rope)
    assert before_sue_believerunit.plan_exists(disc_rope) is False

    # WHEN
    # x_addin = 140
    x_gogo_want = 1000
    x_stop_want = 1700
    # x_denom = 17
    # x_numor = 10
    x_task = True
    insert_disc_believeratom = believeratom_shop(believer_planunit_str(), INSERT_str())
    insert_disc_believeratom.set_jkey(plan_rope_str(), disc_rope)
    # insert_disc_believeratom.set_jvalue(addin_str(), x_addin)
    # insert_disc_believeratom.set_jvalue(begin_str(), x_begin)
    # insert_disc_believeratom.set_jvalue(close_str(), x_close)
    # insert_disc_believeratom.set_jvalue(denom_str(), x_denom)
    # insert_disc_believeratom.set_jvalue(numor_str(), x_numor)
    insert_disc_believeratom.set_jvalue(task_str(), x_task)
    insert_disc_believeratom.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_believeratom.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(insert_disc_believeratom)
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    assert after_sue_believerunit.plan_exists(ball_rope)
    assert after_sue_believerunit.plan_exists(disc_rope)
    disc_plan = after_sue_believerunit.get_plan_obj(disc_rope)
    assert disc_plan.gogo_want == x_gogo_want
    assert disc_plan.stop_want == x_stop_want


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_update_planunit_SimpleAttributes():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believerunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believerunit.make_rope(sports_rope, ball_str)
    before_sue_believerunit.set_plan(planunit_shop(ball_str), sports_rope)

    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    # x_numor = 10
    x_gogo_want = 1222
    x_stop_want = 1333
    x_task = True
    insert_disc_believeratom = believeratom_shop(believer_planunit_str(), UPDATE_str())
    insert_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    # insert_disc_believeratom.set_jvalue(addin_str(), x_addin)
    insert_disc_believeratom.set_jvalue(begin_str(), x_begin)
    insert_disc_believeratom.set_jvalue(close_str(), x_close)
    # insert_disc_believeratom.set_jvalue(denom_str(), x_denom)
    # insert_disc_believeratom.set_jvalue(numor_str(), x_numor)
    insert_disc_believeratom.set_jvalue(task_str(), x_task)
    insert_disc_believeratom.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_believeratom.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(insert_disc_believeratom)
    assert before_sue_believerunit.get_plan_obj(ball_rope).begin is None
    assert before_sue_believerunit.get_plan_obj(ball_rope).close is None
    assert before_sue_believerunit.get_plan_obj(ball_rope).task is False
    assert before_sue_believerunit.get_plan_obj(ball_rope).gogo_want is None
    assert before_sue_believerunit.get_plan_obj(ball_rope).stop_want is None

    # WHEN
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    assert after_sue_believerunit.get_plan_obj(ball_rope).begin == x_begin
    assert after_sue_believerunit.get_plan_obj(ball_rope).close == x_close
    assert after_sue_believerunit.get_plan_obj(ball_rope).gogo_want == x_gogo_want
    assert after_sue_believerunit.get_plan_obj(ball_rope).stop_want == x_stop_want
    assert after_sue_believerunit.get_plan_obj(ball_rope).task


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_plan_awardlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_believerunit.add_personunit(yao_str)
    before_sue_believerunit.add_personunit(zia_str)
    before_sue_believerunit.add_personunit(bob_str)
    yao_personunit = before_sue_believerunit.get_person(yao_str)
    zia_personunit = before_sue_believerunit.get_person(zia_str)
    bob_personunit = before_sue_believerunit.get_person(bob_str)
    run_str = ";runners"
    yao_personunit.add_membership(run_str)
    zia_personunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_personunit.add_membership(fly_str)
    zia_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)

    sports_str = "sports"
    sports_rope = before_sue_believerunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believerunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_believerunit.make_rope(sports_rope, disc_str)
    before_sue_believerunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_believerunit.set_plan(planunit_shop(disc_str), sports_rope)
    before_sue_believerunit.edit_plan_attr(ball_rope, awardlink=awardlink_shop(run_str))
    before_sue_believerunit.edit_plan_attr(ball_rope, awardlink=awardlink_shop(fly_str))
    before_sue_believerunit.edit_plan_attr(disc_rope, awardlink=awardlink_shop(run_str))
    before_sue_believerunit.edit_plan_attr(disc_rope, awardlink=awardlink_shop(fly_str))
    assert len(before_sue_believerunit.get_plan_obj(ball_rope).awardlinks) == 2
    assert len(before_sue_believerunit.get_plan_obj(disc_rope).awardlinks) == 2

    # WHEN
    delete_disc_believeratom = believeratom_shop(
        believer_plan_awardlink_str(), DELETE_str()
    )
    delete_disc_believeratom.set_jkey(plan_rope_str(), disc_rope)
    delete_disc_believeratom.set_jkey(awardee_title_str(), fly_str)
    print(f"{delete_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(delete_disc_believeratom)
    after_sue_believerunit = sue_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    assert len(after_sue_believerunit.get_plan_obj(ball_rope).awardlinks) == 2
    assert len(after_sue_believerunit.get_plan_obj(disc_rope).awardlinks) == 1


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_update_plan_awardlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_believerunit.add_personunit(yao_str)
    before_sue_believerunit.add_personunit(zia_str)
    yao_personunit = before_sue_believerunit.get_person(yao_str)
    run_str = ";runners"
    yao_personunit.add_membership(run_str)

    sports_str = "sports"
    sports_rope = before_sue_believerunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believerunit.make_rope(sports_rope, ball_str)
    before_sue_believerunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_believerunit.edit_plan_attr(ball_rope, awardlink=awardlink_shop(run_str))
    run_awardlink = before_sue_believerunit.get_plan_obj(ball_rope).awardlinks.get(
        run_str
    )
    assert run_awardlink.give_force == 1
    assert run_awardlink.take_force == 1

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_believeratom = believeratom_shop(
        believer_plan_awardlink_str(), UPDATE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(awardee_title_str(), run_str)
    update_disc_believeratom.set_jvalue(give_force_str(), x_give_force)
    update_disc_believeratom.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_believerunit)

    # THEN
    run_awardlink = after_sue_au.get_plan_obj(ball_rope).awardlinks.get(run_str)
    print(f"{run_awardlink.give_force=}")
    assert run_awardlink.give_force == x_give_force
    assert run_awardlink.take_force == x_take_force


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_plan_awardlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_believerunit.add_personunit(yao_str)
    before_sue_believerunit.add_personunit(zia_str)
    run_str = ";runners"
    yao_personunit = before_sue_believerunit.get_person(yao_str)
    yao_personunit.add_membership(run_str)
    sports_str = "sports"
    sports_rope = before_sue_believerunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believerunit.make_rope(sports_rope, ball_str)
    before_sue_believerunit.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_plan = before_sue_believerunit.get_plan_obj(ball_rope)
    assert before_ball_plan.awardlinks.get(run_str) is None

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_believeratom = believeratom_shop(
        believer_plan_awardlink_str(), INSERT_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(awardee_title_str(), run_str)
    update_disc_believeratom.set_jvalue(give_force_str(), x_give_force)
    update_disc_believeratom.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_believerunit)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.awardlinks.get(run_str) is not None


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_plan_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
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
    damaged_fopen = 55
    damaged_fnigh = 66
    update_disc_believeratom = believeratom_shop(
        believer_plan_factunit_str(), INSERT_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(fcontext_str(), knee_rope)
    update_disc_believeratom.set_jvalue(fstate_str(), damaged_rope)
    update_disc_believeratom.set_jvalue(fopen_str(), damaged_fopen)
    update_disc_believeratom.set_jvalue(fnigh_str(), damaged_fnigh)
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits != {}
    assert after_ball_plan.factunits.get(knee_rope) is not None
    assert after_ball_plan.factunits.get(knee_rope).fcontext == knee_rope
    assert after_ball_plan.factunits.get(knee_rope).fstate == damaged_rope
    assert after_ball_plan.factunits.get(knee_rope).fopen == damaged_fopen
    assert after_ball_plan.factunits.get(knee_rope).fnigh == damaged_fnigh


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_plan_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
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
        ball_rope, factunit=factunit_shop(fcontext=knee_rope, fstate=damaged_rope)
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.factunits != {}
    assert before_ball_plan.factunits.get(knee_rope) is not None

    # WHEN
    update_disc_believeratom = believeratom_shop(
        believer_plan_factunit_str(), DELETE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(fcontext_str(), knee_rope)
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits == {}


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_update_plan_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
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
    assert before_ball_plan.factunits.get(knee_rope).fstate == damaged_rope
    assert before_ball_plan.factunits.get(knee_rope).fopen is None
    assert before_ball_plan.factunits.get(knee_rope).fnigh is None

    # WHEN
    medical_fopen = 45
    medical_fnigh = 77
    update_disc_believeratom = believeratom_shop(
        believer_plan_factunit_str(), UPDATE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(fcontext_str(), knee_rope)
    update_disc_believeratom.set_jvalue(fstate_str(), medical_rope)
    update_disc_believeratom.set_jvalue(fopen_str(), medical_fopen)
    update_disc_believeratom.set_jvalue(fnigh_str(), medical_fnigh)
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits != {}
    assert after_ball_plan.factunits.get(knee_rope) is not None
    assert after_ball_plan.factunits.get(knee_rope).fstate == medical_rope
    assert after_ball_plan.factunits.get(knee_rope).fopen == medical_fopen
    assert after_ball_plan.factunits.get(knee_rope).fnigh == medical_fnigh


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_update_plan_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
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
        ball_rope, reason_rcontext=knee_rope, reason_premise=damaged_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.reasonunits != {}
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit is not None
    damaged_premiseunit = before_knee_reasonunit.get_premise(damaged_rope)
    assert damaged_premiseunit.pstate == damaged_rope
    assert damaged_premiseunit.popen is None
    assert damaged_premiseunit.pnigh is None
    assert damaged_premiseunit.pdivisor is None

    # WHEN
    damaged_popen = 45
    damaged_pnigh = 77
    damaged_pdivisor = 3
    update_disc_believeratom = believeratom_shop(
        believer_plan_reason_premiseunit_str(), UPDATE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey("rcontext", knee_rope)
    update_disc_believeratom.set_jkey("pstate", damaged_rope)
    update_disc_believeratom.set_jvalue("popen", damaged_popen)
    update_disc_believeratom.set_jvalue("pnigh", damaged_pnigh)
    update_disc_believeratom.set_jvalue("pdivisor", damaged_pdivisor)
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    after_damaged_premiseunit = after_knee_reasonunit.get_premise(damaged_rope)
    assert after_damaged_premiseunit.pstate == damaged_rope
    assert after_damaged_premiseunit.popen == damaged_popen
    assert after_damaged_premiseunit.pnigh == damaged_pnigh
    assert after_damaged_premiseunit.pdivisor == damaged_pdivisor


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_plan_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
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
        ball_rope, reason_rcontext=knee_rope, reason_premise=damaged_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_premise(damaged_rope) is not None
    assert before_knee_reasonunit.get_premise(medical_rope) is None

    # WHEN
    medical_popen = 45
    medical_pnigh = 77
    medical_pdivisor = 3
    update_disc_believeratom = believeratom_shop(
        believer_plan_reason_premiseunit_str(), INSERT_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey("rcontext", knee_rope)
    update_disc_believeratom.set_jkey("pstate", medical_rope)
    update_disc_believeratom.set_jvalue("popen", medical_popen)
    update_disc_believeratom.set_jvalue("pnigh", medical_pnigh)
    update_disc_believeratom.set_jvalue("pdivisor", medical_pdivisor)
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_rope)
    assert after_medical_premiseunit is not None
    assert after_medical_premiseunit.pstate == medical_rope
    assert after_medical_premiseunit.popen == medical_popen
    assert after_medical_premiseunit.pnigh == medical_pnigh
    assert after_medical_premiseunit.pdivisor == medical_pdivisor


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_plan_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
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
        ball_rope, reason_rcontext=knee_rope, reason_premise=damaged_rope
    )
    before_sue_au.edit_plan_attr(
        ball_rope, reason_rcontext=knee_rope, reason_premise=medical_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_premise(damaged_rope) is not None
    assert before_knee_reasonunit.get_premise(medical_rope) is not None

    # WHEN
    update_disc_believeratom = believeratom_shop(
        believer_plan_reason_premiseunit_str(), DELETE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey("rcontext", knee_rope)
    update_disc_believeratom.set_jkey("pstate", medical_rope)
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit.get_premise(damaged_rope) is not None
    assert after_knee_reasonunit.get_premise(medical_rope) is None


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_plan_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
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
    medical_rplan_active_requisite = True
    update_disc_believeratom = believeratom_shop(
        believer_plan_reasonunit_str(), INSERT_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey("rcontext", knee_rope)
    update_disc_believeratom.set_jvalue(
        rplan_active_requisite_str(),
        medical_rplan_active_requisite,
    )
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_premise(medical_rope) is None
    assert (
        after_knee_reasonunit.rplan_active_requisite == medical_rplan_active_requisite
    )


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_update_plan_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_medical_rplan_active_requisite = False
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan(planunit_shop(medical_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope,
        reason_rcontext=knee_rope,
        reason_rplan_active_requisite=before_medical_rplan_active_requisite,
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_ball_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_ball_reasonunit is not None
    assert (
        before_ball_reasonunit.rplan_active_requisite
        == before_medical_rplan_active_requisite
    )

    # WHEN
    after_medical_rplan_active_requisite = True
    update_disc_believeratom = believeratom_shop(
        believer_plan_reasonunit_str(), UPDATE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey("rcontext", knee_rope)
    update_disc_believeratom.set_jvalue(
        rplan_active_requisite_str(),
        after_medical_rplan_active_requisite,
    )
    # print(f"{update_disc_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_premise(medical_rope) is None
    assert (
        after_knee_reasonunit.rplan_active_requisite
        == after_medical_rplan_active_requisite
    )


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_plan_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_rplan_active_requisite = False
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.edit_plan_attr(
        ball_rope,
        reason_rcontext=knee_rope,
        reason_rplan_active_requisite=medical_rplan_active_requisite,
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.get_reasonunit(knee_rope) is not None

    # WHEN
    update_disc_believeratom = believeratom_shop(
        believer_plan_reasonunit_str(), DELETE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey("rcontext", knee_rope)
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.get_reasonunit(knee_rope) is None


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_plan_laborlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_personunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_planunit.laborunit._laborlinks == set()

    # WHEN
    update_disc_believeratom = believeratom_shop(
        believer_plan_laborlink_str(), INSERT_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(labor_title_str(), yao_str)
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.laborunit._laborlinks != set()
    assert after_ball_planunit.laborunit.get_laborlink(yao_str) is not None


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_plan_laborlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_personunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    before_ball_planunit.laborunit.set_laborlink(yao_str)
    assert before_ball_planunit.laborunit._laborlinks != set()
    assert before_ball_planunit.laborunit.get_laborlink(yao_str) is not None

    # WHEN
    update_disc_believeratom = believeratom_shop(
        believer_plan_laborlink_str(), DELETE_str()
    )
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(labor_title_str(), yao_str)
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(update_disc_believeratom)
    print(f"{before_sue_au.get_plan_obj(ball_rope).laborunit=}")
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.laborunit._laborlinks == set()


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_insert_plan_healerlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_personunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_planunit.healerlink._healer_names == set()
    assert not before_ball_planunit.healerlink.healer_name_exists(yao_str)

    # WHEN
    x_believeratom = believeratom_shop(believer_plan_healerlink_str(), INSERT_str())
    x_believeratom.set_jkey(plan_rope_str(), ball_rope)
    x_believeratom.set_jkey(healer_name_str(), yao_str)
    print(f"{x_believeratom=}")
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(x_believeratom)
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.healerlink._healer_names != set()
    assert after_ball_planunit.healerlink.healer_name_exists(yao_str)


def test_BelieverDelta_get_edited_believer_ReturnsObj_BelieverUnit_delete_plan_healerlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_personunit(yao_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    before_ball_planunit.healerlink.set_healer_name(yao_str)
    assert before_ball_planunit.healerlink._healer_names != set()
    assert before_ball_planunit.healerlink.healer_name_exists(yao_str)

    # WHEN
    x_believeratom = believeratom_shop(believer_plan_healerlink_str(), DELETE_str())
    x_believeratom.set_jkey(plan_rope_str(), ball_rope)
    x_believeratom.set_jkey(healer_name_str(), yao_str)
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.set_believeratom(x_believeratom)
    print(f"{before_sue_au.get_plan_obj(ball_rope).laborunit=}")
    after_sue_au = sue_believerdelta.get_edited_believer(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.healerlink._healer_names == set()
    assert not after_ball_planunit.healerlink.healer_name_exists(yao_str)


def test_BelieverDelta_get_believerdelta_example1_ContainsBelieverAtoms():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_believerunit.add_personunit(yao_str)
    before_sue_believerunit.add_personunit(zia_str)
    before_sue_believerunit.add_personunit(bob_str)
    yao_personunit = before_sue_believerunit.get_person(yao_str)
    zia_personunit = before_sue_believerunit.get_person(zia_str)
    bob_personunit = before_sue_believerunit.get_person(bob_str)
    run_str = ";runners"
    yao_personunit.add_membership(run_str)
    zia_personunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)
    assert before_sue_believerunit.tally != 55
    assert before_sue_believerunit.max_tree_traverse != 66
    assert before_sue_believerunit.credor_respect != 77
    assert before_sue_believerunit.debtor_respect != 88
    assert before_sue_believerunit.person_exists(yao_str)
    assert before_sue_believerunit.person_exists(zia_str)
    assert yao_personunit.get_membership(fly_str) is not None
    assert bob_personunit.get_membership(fly_str) is not None

    # WHEN
    ex1_believerdelta = get_believerdelta_example1()
    after_sue_believerunit = ex1_believerdelta.get_edited_believer(
        before_sue_believerunit
    )

    # THEN
    assert after_sue_believerunit.tally == 55
    assert after_sue_believerunit.max_tree_traverse == 66
    assert after_sue_believerunit.credor_respect == 77
    assert after_sue_believerunit.debtor_respect == 88
    assert after_sue_believerunit.person_exists(yao_str)
    assert after_sue_believerunit.person_exists(zia_str) is False
