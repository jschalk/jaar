from src.a01_term_logic.way import get_parent_way, get_tail_label
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    awardee_title_str,
    begin_str,
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_concept_awardlink_str,
    bud_concept_factunit_str,
    bud_concept_healerlink_str,
    bud_concept_laborlink_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_reasonunit_str,
    bud_conceptunit_str,
    budunit_str,
    close_str,
    concept_way_str,
    credit_vote_str,
    debtit_vote_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    give_force_str,
    gogo_want_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    rconcept_active_requisite_str,
    stop_want_str,
    take_force_str,
    task_str,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a08_bud_atom_logic._test_util.a08_str import DELETE_str, INSERT_str, UPDATE_str
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic._test_util.example_deltas import get_buddelta_example1
from src.a09_pack_logic.delta import buddelta_shop


def test_BudDelta_get_edited_bud_ReturnsObj_SimplestScenario():
    # ESTABLISH
    ex1_buddelta = buddelta_shop()

    # WHEN
    sue_str = "Sue"
    sue_tally = 55
    before_sue_budunit = budunit_shop(sue_str, tally=sue_tally)
    after_sue_budunit = ex1_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.tally == sue_tally
    assert after_sue_budunit == before_sue_budunit


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnitSimpleAttrs():
    # ESTABLISH
    sue_buddelta = buddelta_shop()
    sue_str = "Sue"

    sue_tally = 44
    before_sue_budunit = budunit_shop(sue_str, tally=sue_tally)

    dimen = budunit_str()
    x_budatom = budatom_shop(dimen, UPDATE_str())
    new1_value = 55
    new1_arg = "tally"
    x_budatom.set_jvalue(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "max_tree_traverse"
    x_budatom.set_jvalue(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "credor_respect"
    x_budatom.set_jvalue(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "debtor_respect"
    x_budatom.set_jvalue(new4_arg, new4_value)
    new9_value = 55550000
    new9_arg = "fund_pool"
    x_budatom.set_jvalue(new9_arg, new9_value)
    new8_value = 0.5555
    new8_arg = "fund_iota"
    x_budatom.set_jvalue(new8_arg, new8_value)
    sue_buddelta.set_budatom(x_budatom)
    new6_value = 0.5
    new6_arg = "respect_bit"
    x_budatom.set_jvalue(new6_arg, new6_value)
    sue_buddelta.set_budatom(x_budatom)
    new7_value = 0.025
    new7_arg = "penny"
    x_budatom.set_jvalue(new7_arg, new7_value)
    sue_buddelta.set_budatom(x_budatom)

    # WHEN
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    print(f"{sue_buddelta.budatoms.keys()=}")
    assert after_sue_budunit.max_tree_traverse == new2_value
    assert after_sue_budunit.credor_respect == new3_value
    assert after_sue_budunit.debtor_respect == new4_value
    assert after_sue_budunit.tally == new1_value
    assert after_sue_budunit.tally != before_sue_budunit.tally
    assert after_sue_budunit.fund_pool == new9_value
    assert after_sue_budunit.fund_pool != before_sue_budunit.fund_pool
    assert after_sue_budunit.fund_iota == new8_value
    assert after_sue_budunit.fund_iota != before_sue_budunit.fund_iota
    assert after_sue_budunit.respect_bit == new6_value
    assert after_sue_budunit.respect_bit != before_sue_budunit.respect_bit
    assert after_sue_budunit.penny == new7_value
    assert after_sue_budunit.penny != before_sue_budunit.penny


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_acct():
    # ESTABLISH
    sue_buddelta = buddelta_shop()
    sue_str = "Sue"

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)

    dimen = bud_acctunit_str()
    x_budatom = budatom_shop(dimen, DELETE_str())
    x_budatom.set_jkey(acct_name_str(), zia_str)
    sue_buddelta.set_budatom(x_budatom)

    # WHEN
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    print(f"{sue_buddelta.budatoms=}")
    assert after_sue_budunit != before_sue_budunit
    assert after_sue_budunit.acct_exists(yao_str)
    assert after_sue_budunit.acct_exists(zia_str) is False


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_acct():
    # ESTABLISH
    sue_buddelta = buddelta_shop()
    sue_str = "Sue"

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    assert before_sue_budunit.acct_exists(yao_str)
    assert before_sue_budunit.acct_exists(zia_str) is False

    # WHEN
    dimen = bud_acctunit_str()
    x_budatom = budatom_shop(dimen, INSERT_str())
    x_budatom.set_jkey(acct_name_str(), zia_str)
    x_credit_belief = 55
    x_debtit_belief = 66
    x_budatom.set_jvalue("credit_belief", x_credit_belief)
    x_budatom.set_jvalue("debtit_belief", x_debtit_belief)
    sue_buddelta.set_budatom(x_budatom)
    print(f"{sue_buddelta.budatoms.keys()=}")
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    yao_acctunit = after_sue_budunit.get_acct(yao_str)
    zia_acctunit = after_sue_budunit.get_acct(zia_str)
    assert yao_acctunit is not None
    assert zia_acctunit is not None
    assert zia_acctunit.credit_belief == x_credit_belief
    assert zia_acctunit.debtit_belief == x_debtit_belief


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_update_acct():
    # ESTABLISH
    sue_buddelta = buddelta_shop()
    sue_str = "Sue"

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_budunit.add_acctunit(yao_str)
    assert before_sue_budunit.get_acct(yao_str).credit_belief == 1

    # WHEN
    dimen = bud_acctunit_str()
    x_budatom = budatom_shop(dimen, UPDATE_str())
    x_budatom.set_jkey(acct_name_str(), yao_str)
    yao_credit_belief = 55
    x_budatom.set_jvalue("credit_belief", yao_credit_belief)
    sue_buddelta.set_budatom(x_budatom)
    print(f"{sue_buddelta.budatoms.keys()=}")
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    yao_acct = after_sue_budunit.get_acct(yao_str)
    assert yao_acct.credit_belief == yao_credit_belief


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_membership():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)
    before_sue_budunit.add_acctunit(bob_str)
    yao_acctunit = before_sue_budunit.get_acct(yao_str)
    zia_acctunit = before_sue_budunit.get_acct(zia_str)
    bob_acctunit = before_sue_budunit.get_acct(bob_str)
    run_str = ";runners"
    yao_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_acctunit.add_membership(fly_str)
    zia_acctunit.add_membership(fly_str)
    bob_acctunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_budunit.get_acctunit_group_titles_dict()
    assert len(before_group_titles_dict.get(run_str)) == 2
    assert len(before_group_titles_dict.get(fly_str)) == 3

    # WHEN
    yao_budatom = budatom_shop(bud_acct_membership_str(), DELETE_str())
    yao_budatom.set_jkey(group_title_str(), run_str)
    yao_budatom.set_jkey(acct_name_str(), yao_str)
    # print(f"{yao_budatom=}")
    zia_budatom = budatom_shop(bud_acct_membership_str(), DELETE_str())
    zia_budatom.set_jkey(group_title_str(), fly_str)
    zia_budatom.set_jkey(acct_name_str(), zia_str)
    # print(f"{zia_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(yao_budatom)
    sue_buddelta.set_budatom(zia_budatom)
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    after_group_titles_dict = after_sue_budunit.get_acctunit_group_titles_dict()
    assert len(after_group_titles_dict.get(run_str)) == 1
    assert len(after_group_titles_dict.get(fly_str)) == 2


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_membership():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)
    before_sue_budunit.add_acctunit(bob_str)
    run_str = ";runners"
    zia_acctunit = before_sue_budunit.get_acct(zia_str)
    zia_acctunit.add_membership(run_str)
    before_group_titles = before_sue_budunit.get_acctunit_group_titles_dict()
    assert len(before_group_titles.get(run_str)) == 1

    # WHEN
    yao_budatom = budatom_shop(bud_acct_membership_str(), INSERT_str())
    yao_budatom.set_jkey(group_title_str(), run_str)
    yao_budatom.set_jkey(acct_name_str(), yao_str)
    yao_run_credit_vote = 17
    yao_budatom.set_jvalue("credit_vote", yao_run_credit_vote)
    print(f"{yao_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(yao_budatom)
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    after_group_titles = after_sue_budunit.get_acctunit_group_titles_dict()
    assert len(after_group_titles.get(run_str)) == 2
    after_yao_acctunit = after_sue_budunit.get_acct(yao_str)
    after_yao_run_membership = after_yao_acctunit.get_membership(run_str)
    assert after_yao_run_membership is not None
    assert after_yao_run_membership.credit_vote == yao_run_credit_vote


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_update_membership():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_budunit.add_acctunit(yao_str)
    before_yao_acctunit = before_sue_budunit.get_acct(yao_str)
    run_str = ";runners"
    old_yao_run_credit_vote = 3
    before_yao_acctunit.add_membership(run_str, old_yao_run_credit_vote)
    yao_run_membership = before_yao_acctunit.get_membership(run_str)
    assert yao_run_membership.credit_vote == old_yao_run_credit_vote
    assert yao_run_membership.debtit_vote == 1

    # WHEN
    yao_budatom = budatom_shop(bud_acct_membership_str(), UPDATE_str())
    yao_budatom.set_jkey(group_title_str(), run_str)
    yao_budatom.set_jkey(acct_name_str(), yao_str)
    new_yao_run_credit_vote = 7
    new_yao_run_debtit_vote = 11
    yao_budatom.set_jvalue(credit_vote_str(), new_yao_run_credit_vote)
    yao_budatom.set_jvalue(debtit_vote_str(), new_yao_run_debtit_vote)
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(yao_budatom)
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    after_yao_acctunit = after_sue_budunit.get_acct(yao_str)
    after_yao_run_membership = after_yao_acctunit.get_membership(run_str)
    assert after_yao_run_membership.credit_vote == new_yao_run_credit_vote
    assert after_yao_run_membership.debtit_vote == new_yao_run_debtit_vote


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_conceptunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_budunit.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_budunit.make_way(sports_way, ball_str)
    disc_str = "Ultimate Disc"
    disc_way = before_sue_budunit.make_way(sports_way, disc_str)
    before_sue_budunit.set_concept(conceptunit_shop(ball_str), sports_way)
    before_sue_budunit.set_concept(conceptunit_shop(disc_str), sports_way)
    delete_disc_budatom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    delete_disc_budatom.set_jkey(concept_way_str(), disc_way)
    print(f"{disc_way=}")
    delete_disc_budatom.set_jkey(concept_way_str(), disc_way)
    print(f"{delete_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(delete_disc_budatom)
    assert before_sue_budunit.concept_exists(ball_way)
    assert before_sue_budunit.concept_exists(disc_way)

    # WHEN
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.concept_exists(ball_way)
    assert after_sue_budunit.concept_exists(disc_way) is False


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_conceptunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_budunit.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_budunit.make_way(sports_way, ball_str)
    disc_str = "Ultimate Disc"
    disc_way = before_sue_budunit.make_way(sports_way, disc_str)
    before_sue_budunit.set_concept(conceptunit_shop(ball_str), sports_way)
    assert before_sue_budunit.concept_exists(ball_way)
    assert before_sue_budunit.concept_exists(disc_way) is False

    # WHEN
    # x_addin = 140
    x_gogo_want = 1000
    x_stop_want = 1700
    # x_denom = 17
    # x_numor = 10
    x_task = True
    insert_disc_budatom = budatom_shop(bud_conceptunit_str(), INSERT_str())
    insert_disc_budatom.set_jkey(concept_way_str(), disc_way)
    # insert_disc_budatom.set_jvalue(addin_str(), x_addin)
    # insert_disc_budatom.set_jvalue(begin_str(), x_begin)
    # insert_disc_budatom.set_jvalue(close_str(), x_close)
    # insert_disc_budatom.set_jvalue(denom_str(), x_denom)
    # insert_disc_budatom.set_jvalue(numor_str(), x_numor)
    insert_disc_budatom.set_jvalue(task_str(), x_task)
    insert_disc_budatom.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_budatom.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(insert_disc_budatom)
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.concept_exists(ball_way)
    assert after_sue_budunit.concept_exists(disc_way)
    disc_concept = after_sue_budunit.get_concept_obj(disc_way)
    assert disc_concept.gogo_want == x_gogo_want
    assert disc_concept.stop_want == x_stop_want


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_update_conceptunit_SimpleAttributes():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_budunit.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_budunit.make_way(sports_way, ball_str)
    before_sue_budunit.set_concept(conceptunit_shop(ball_str), sports_way)

    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    # x_numor = 10
    x_gogo_want = 1222
    x_stop_want = 1333
    x_task = True
    insert_disc_budatom = budatom_shop(bud_conceptunit_str(), UPDATE_str())
    insert_disc_budatom.set_jkey(concept_way_str(), ball_way)
    # insert_disc_budatom.set_jvalue(addin_str(), x_addin)
    insert_disc_budatom.set_jvalue(begin_str(), x_begin)
    insert_disc_budatom.set_jvalue(close_str(), x_close)
    # insert_disc_budatom.set_jvalue(denom_str(), x_denom)
    # insert_disc_budatom.set_jvalue(numor_str(), x_numor)
    insert_disc_budatom.set_jvalue(task_str(), x_task)
    insert_disc_budatom.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_budatom.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(insert_disc_budatom)
    assert before_sue_budunit.get_concept_obj(ball_way).begin is None
    assert before_sue_budunit.get_concept_obj(ball_way).close is None
    assert before_sue_budunit.get_concept_obj(ball_way).task is False
    assert before_sue_budunit.get_concept_obj(ball_way).gogo_want is None
    assert before_sue_budunit.get_concept_obj(ball_way).stop_want is None

    # WHEN
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.get_concept_obj(ball_way).begin == x_begin
    assert after_sue_budunit.get_concept_obj(ball_way).close == x_close
    assert after_sue_budunit.get_concept_obj(ball_way).gogo_want == x_gogo_want
    assert after_sue_budunit.get_concept_obj(ball_way).stop_want == x_stop_want
    assert after_sue_budunit.get_concept_obj(ball_way).task


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_concept_awardlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)
    before_sue_budunit.add_acctunit(bob_str)
    yao_acctunit = before_sue_budunit.get_acct(yao_str)
    zia_acctunit = before_sue_budunit.get_acct(zia_str)
    bob_acctunit = before_sue_budunit.get_acct(bob_str)
    run_str = ";runners"
    yao_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_acctunit.add_membership(fly_str)
    zia_acctunit.add_membership(fly_str)
    bob_acctunit.add_membership(fly_str)

    sports_str = "sports"
    sports_way = before_sue_budunit.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_budunit.make_way(sports_way, ball_str)
    disc_str = "Ultimate Disc"
    disc_way = before_sue_budunit.make_way(sports_way, disc_str)
    before_sue_budunit.set_concept(conceptunit_shop(ball_str), sports_way)
    before_sue_budunit.set_concept(conceptunit_shop(disc_str), sports_way)
    before_sue_budunit.edit_concept_attr(ball_way, awardlink=awardlink_shop(run_str))
    before_sue_budunit.edit_concept_attr(ball_way, awardlink=awardlink_shop(fly_str))
    before_sue_budunit.edit_concept_attr(disc_way, awardlink=awardlink_shop(run_str))
    before_sue_budunit.edit_concept_attr(disc_way, awardlink=awardlink_shop(fly_str))
    assert len(before_sue_budunit.get_concept_obj(ball_way).awardlinks) == 2
    assert len(before_sue_budunit.get_concept_obj(disc_way).awardlinks) == 2

    # WHEN
    delete_disc_budatom = budatom_shop(bud_concept_awardlink_str(), DELETE_str())
    delete_disc_budatom.set_jkey(concept_way_str(), disc_way)
    delete_disc_budatom.set_jkey(awardee_title_str(), fly_str)
    print(f"{delete_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(delete_disc_budatom)
    after_sue_budunit = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    assert len(after_sue_budunit.get_concept_obj(ball_way).awardlinks) == 2
    assert len(after_sue_budunit.get_concept_obj(disc_way).awardlinks) == 1


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_update_concept_awardlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)
    yao_acctunit = before_sue_budunit.get_acct(yao_str)
    run_str = ";runners"
    yao_acctunit.add_membership(run_str)

    sports_str = "sports"
    sports_way = before_sue_budunit.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_budunit.make_way(sports_way, ball_str)
    before_sue_budunit.set_concept(conceptunit_shop(ball_str), sports_way)
    before_sue_budunit.edit_concept_attr(ball_way, awardlink=awardlink_shop(run_str))
    run_awardlink = before_sue_budunit.get_concept_obj(ball_way).awardlinks.get(run_str)
    assert run_awardlink.give_force == 1
    assert run_awardlink.take_force == 1

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_budatom = budatom_shop(bud_concept_awardlink_str(), UPDATE_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(awardee_title_str(), run_str)
    update_disc_budatom.set_jvalue(give_force_str(), x_give_force)
    update_disc_budatom.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    run_awardlink = after_sue_au.get_concept_obj(ball_way).awardlinks.get(run_str)
    print(f"{run_awardlink.give_force=}")
    assert run_awardlink.give_force == x_give_force
    assert run_awardlink.take_force == x_take_force


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_concept_awardlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)
    run_str = ";runners"
    yao_acctunit = before_sue_budunit.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    sports_str = "sports"
    sports_way = before_sue_budunit.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_budunit.make_way(sports_way, ball_str)
    before_sue_budunit.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_concept = before_sue_budunit.get_concept_obj(ball_way)
    assert before_ball_concept.awardlinks.get(run_str) is None

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_budatom = budatom_shop(bud_concept_awardlink_str(), INSERT_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(awardee_title_str(), run_str)
    update_disc_budatom.set_jvalue(give_force_str(), x_give_force)
    update_disc_budatom.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_concept.awardlinks.get(run_str) is not None


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_concept_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_au.make_way(knee_way, damaged_str)
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(damaged_str), knee_way)
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_concept.factunits == {}

    # WHEN
    damaged_fopen = 55
    damaged_fnigh = 66
    update_disc_budatom = budatom_shop(bud_concept_factunit_str(), INSERT_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(fcontext_str(), knee_way)
    update_disc_budatom.set_jvalue(fstate_str(), damaged_way)
    update_disc_budatom.set_jvalue(fopen_str(), damaged_fopen)
    update_disc_budatom.set_jvalue(fnigh_str(), damaged_fnigh)
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_concept.factunits != {}
    assert after_ball_concept.factunits.get(knee_way) is not None
    assert after_ball_concept.factunits.get(knee_way).fcontext == knee_way
    assert after_ball_concept.factunits.get(knee_way).fstate == damaged_way
    assert after_ball_concept.factunits.get(knee_way).fopen == damaged_fopen
    assert after_ball_concept.factunits.get(knee_way).fnigh == damaged_fnigh


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_concept_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_au.make_way(knee_way, damaged_str)
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(damaged_str), knee_way)
    before_sue_au.edit_concept_attr(
        ball_way, factunit=factunit_shop(fcontext=knee_way, fstate=damaged_way)
    )
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_concept.factunits != {}
    assert before_ball_concept.factunits.get(knee_way) is not None

    # WHEN
    update_disc_budatom = budatom_shop(bud_concept_factunit_str(), DELETE_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(fcontext_str(), knee_way)
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_concept.factunits == {}


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_update_concept_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_au.make_way(knee_way, damaged_str)
    medical_str = "get medical attention"
    medical_way = before_sue_au.make_way(knee_way, medical_str)
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(damaged_str), knee_way)
    before_sue_au.set_concept(conceptunit_shop(medical_str), knee_way)
    before_knee_factunit = factunit_shop(knee_way, damaged_way)
    before_sue_au.edit_concept_attr(ball_way, factunit=before_knee_factunit)
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_concept.factunits != {}
    assert before_ball_concept.factunits.get(knee_way) is not None
    assert before_ball_concept.factunits.get(knee_way).fstate == damaged_way
    assert before_ball_concept.factunits.get(knee_way).fopen is None
    assert before_ball_concept.factunits.get(knee_way).fnigh is None

    # WHEN
    medical_fopen = 45
    medical_fnigh = 77
    update_disc_budatom = budatom_shop(bud_concept_factunit_str(), UPDATE_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(fcontext_str(), knee_way)
    update_disc_budatom.set_jvalue(fstate_str(), medical_way)
    update_disc_budatom.set_jvalue(fopen_str(), medical_fopen)
    update_disc_budatom.set_jvalue(fnigh_str(), medical_fnigh)
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_concept.factunits != {}
    assert after_ball_concept.factunits.get(knee_way) is not None
    assert after_ball_concept.factunits.get(knee_way).fstate == medical_way
    assert after_ball_concept.factunits.get(knee_way).fopen == medical_fopen
    assert after_ball_concept.factunits.get(knee_way).fnigh == medical_fnigh


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_update_concept_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_au.make_way(knee_way, damaged_str)
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(damaged_str), knee_way)
    before_sue_au.edit_concept_attr(
        ball_way, reason_rcontext=knee_way, reason_premise=damaged_way
    )
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_concept.reasonunits != {}
    before_knee_reasonunit = before_ball_concept.get_reasonunit(knee_way)
    assert before_knee_reasonunit is not None
    damaged_premiseunit = before_knee_reasonunit.get_premise(damaged_way)
    assert damaged_premiseunit.pstate == damaged_way
    assert damaged_premiseunit.popen is None
    assert damaged_premiseunit.pnigh is None
    assert damaged_premiseunit.pdivisor is None

    # WHEN
    damaged_popen = 45
    damaged_pnigh = 77
    damaged_pdivisor = 3
    update_disc_budatom = budatom_shop(
        bud_concept_reason_premiseunit_str(), UPDATE_str()
    )
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey("rcontext", knee_way)
    update_disc_budatom.set_jkey("pstate", damaged_way)
    update_disc_budatom.set_jvalue("popen", damaged_popen)
    update_disc_budatom.set_jvalue("pnigh", damaged_pnigh)
    update_disc_budatom.set_jvalue("pdivisor", damaged_pdivisor)
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    after_knee_reasonunit = after_ball_concept.get_reasonunit(knee_way)
    assert after_knee_reasonunit is not None
    after_damaged_premiseunit = after_knee_reasonunit.get_premise(damaged_way)
    assert after_damaged_premiseunit.pstate == damaged_way
    assert after_damaged_premiseunit.popen == damaged_popen
    assert after_damaged_premiseunit.pnigh == damaged_pnigh
    assert after_damaged_premiseunit.pdivisor == damaged_pdivisor


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_concept_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_au.make_way(knee_way, damaged_str)
    medical_str = "get medical attention"
    medical_way = before_sue_au.make_way(knee_way, medical_str)
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(damaged_str), knee_way)
    before_sue_au.set_concept(conceptunit_shop(medical_str), knee_way)
    before_sue_au.edit_concept_attr(
        ball_way, reason_rcontext=knee_way, reason_premise=damaged_way
    )
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    before_knee_reasonunit = before_ball_concept.get_reasonunit(knee_way)
    assert before_knee_reasonunit.get_premise(damaged_way) is not None
    assert before_knee_reasonunit.get_premise(medical_way) is None

    # WHEN
    medical_popen = 45
    medical_pnigh = 77
    medical_pdivisor = 3
    update_disc_budatom = budatom_shop(
        bud_concept_reason_premiseunit_str(), INSERT_str()
    )
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey("rcontext", knee_way)
    update_disc_budatom.set_jkey("pstate", medical_way)
    update_disc_budatom.set_jvalue("popen", medical_popen)
    update_disc_budatom.set_jvalue("pnigh", medical_pnigh)
    update_disc_budatom.set_jvalue("pdivisor", medical_pdivisor)
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    after_knee_reasonunit = after_ball_concept.get_reasonunit(knee_way)
    after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_way)
    assert after_medical_premiseunit is not None
    assert after_medical_premiseunit.pstate == medical_way
    assert after_medical_premiseunit.popen == medical_popen
    assert after_medical_premiseunit.pnigh == medical_pnigh
    assert after_medical_premiseunit.pdivisor == medical_pdivisor


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_concept_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_au.make_way(knee_way, damaged_str)
    medical_str = "get medical attention"
    medical_way = before_sue_au.make_way(knee_way, medical_str)
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(damaged_str), knee_way)
    before_sue_au.set_concept(conceptunit_shop(medical_str), knee_way)
    before_sue_au.edit_concept_attr(
        ball_way, reason_rcontext=knee_way, reason_premise=damaged_way
    )
    before_sue_au.edit_concept_attr(
        ball_way, reason_rcontext=knee_way, reason_premise=medical_way
    )
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    before_knee_reasonunit = before_ball_concept.get_reasonunit(knee_way)
    assert before_knee_reasonunit.get_premise(damaged_way) is not None
    assert before_knee_reasonunit.get_premise(medical_way) is not None

    # WHEN
    update_disc_budatom = budatom_shop(
        bud_concept_reason_premiseunit_str(), DELETE_str()
    )
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey("rcontext", knee_way)
    update_disc_budatom.set_jkey("pstate", medical_way)
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    after_knee_reasonunit = after_ball_concept.get_reasonunit(knee_way)
    assert after_knee_reasonunit.get_premise(damaged_way) is not None
    assert after_knee_reasonunit.get_premise(medical_way) is None


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_concept_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    medical_str = "get medical attention"
    medical_way = before_sue_au.make_way(knee_way, medical_str)
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(medical_str), knee_way)
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_concept.get_reasonunit(knee_way) is None

    # WHEN
    medical_rconcept_active_requisite = True
    update_disc_budatom = budatom_shop(bud_concept_reasonunit_str(), INSERT_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey("rcontext", knee_way)
    update_disc_budatom.set_jvalue(
        rconcept_active_requisite_str(),
        medical_rconcept_active_requisite,
    )
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    after_knee_reasonunit = after_ball_concept.get_reasonunit(knee_way)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_premise(medical_way) is None
    assert (
        after_knee_reasonunit.rconcept_active_requisite
        == medical_rconcept_active_requisite
    )


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_update_concept_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    medical_str = "get medical attention"
    medical_way = before_sue_au.make_way(knee_way, medical_str)
    before_medical_rconcept_active_requisite = False
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.set_concept(conceptunit_shop(medical_str), knee_way)
    before_sue_au.edit_concept_attr(
        ball_way,
        reason_rcontext=knee_way,
        reason_rconcept_active_requisite=before_medical_rconcept_active_requisite,
    )
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    before_ball_reasonunit = before_ball_concept.get_reasonunit(knee_way)
    assert before_ball_reasonunit is not None
    assert (
        before_ball_reasonunit.rconcept_active_requisite
        == before_medical_rconcept_active_requisite
    )

    # WHEN
    after_medical_rconcept_active_requisite = True
    update_disc_budatom = budatom_shop(bud_concept_reasonunit_str(), UPDATE_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey("rcontext", knee_way)
    update_disc_budatom.set_jvalue(
        rconcept_active_requisite_str(),
        after_medical_rconcept_active_requisite,
    )
    # print(f"{update_disc_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    after_knee_reasonunit = after_ball_concept.get_reasonunit(knee_way)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_premise(medical_way) is None
    assert (
        after_knee_reasonunit.rconcept_active_requisite
        == after_medical_rconcept_active_requisite
    )


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_concept_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_au.make_l1_way(knee_str)
    medical_rconcept_active_requisite = False
    before_sue_au.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_au.edit_concept_attr(
        ball_way,
        reason_rcontext=knee_way,
        reason_rconcept_active_requisite=medical_rconcept_active_requisite,
    )
    before_ball_concept = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_concept.get_reasonunit(knee_way) is not None

    # WHEN
    update_disc_budatom = budatom_shop(bud_concept_reasonunit_str(), DELETE_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey("rcontext", knee_way)
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_concept = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_concept.get_reasonunit(knee_way) is None


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_concept_laborlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_conceptunit = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_conceptunit.laborunit._laborlinks == set()

    # WHEN
    update_disc_budatom = budatom_shop(bud_concept_laborlink_str(), INSERT_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(labor_title_str(), yao_str)
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_conceptunit = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_conceptunit.laborunit._laborlinks != set()
    assert after_ball_conceptunit.laborunit.get_laborlink(yao_str) is not None


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_concept_laborlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_conceptunit = before_sue_au.get_concept_obj(ball_way)
    before_ball_conceptunit.laborunit.set_laborlink(yao_str)
    assert before_ball_conceptunit.laborunit._laborlinks != set()
    assert before_ball_conceptunit.laborunit.get_laborlink(yao_str) is not None

    # WHEN
    update_disc_budatom = budatom_shop(bud_concept_laborlink_str(), DELETE_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(labor_title_str(), yao_str)
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(update_disc_budatom)
    print(f"{before_sue_au.get_concept_obj(ball_way).laborunit=}")
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_conceptunit = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_conceptunit.laborunit._laborlinks == set()


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_insert_concept_healerlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_conceptunit = before_sue_au.get_concept_obj(ball_way)
    assert before_ball_conceptunit.healerlink._healer_names == set()
    assert not before_ball_conceptunit.healerlink.healer_name_exists(yao_str)

    # WHEN
    x_budatom = budatom_shop(bud_concept_healerlink_str(), INSERT_str())
    x_budatom.set_jkey(concept_way_str(), ball_way)
    x_budatom.set_jkey(healer_name_str(), yao_str)
    print(f"{x_budatom=}")
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(x_budatom)
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_conceptunit = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_conceptunit.healerlink._healer_names != set()
    assert after_ball_conceptunit.healerlink.healer_name_exists(yao_str)


def test_BudDelta_get_edited_bud_ReturnsObj_BudUnit_delete_concept_healerlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_conceptunit = before_sue_au.get_concept_obj(ball_way)
    before_ball_conceptunit.healerlink.set_healer_name(yao_str)
    assert before_ball_conceptunit.healerlink._healer_names != set()
    assert before_ball_conceptunit.healerlink.healer_name_exists(yao_str)

    # WHEN
    x_budatom = budatom_shop(bud_concept_healerlink_str(), DELETE_str())
    x_budatom.set_jkey(concept_way_str(), ball_way)
    x_budatom.set_jkey(healer_name_str(), yao_str)
    sue_buddelta = buddelta_shop()
    sue_buddelta.set_budatom(x_budatom)
    print(f"{before_sue_au.get_concept_obj(ball_way).laborunit=}")
    after_sue_au = sue_buddelta.get_edited_bud(before_sue_au)

    # THEN
    after_ball_conceptunit = after_sue_au.get_concept_obj(ball_way)
    assert after_ball_conceptunit.healerlink._healer_names == set()
    assert not after_ball_conceptunit.healerlink.healer_name_exists(yao_str)


def test_BudDelta_get_buddelta_example1_ContainsBudAtoms():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)
    before_sue_budunit.add_acctunit(bob_str)
    yao_acctunit = before_sue_budunit.get_acct(yao_str)
    zia_acctunit = before_sue_budunit.get_acct(zia_str)
    bob_acctunit = before_sue_budunit.get_acct(bob_str)
    run_str = ";runners"
    yao_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    yao_acctunit.add_membership(fly_str)
    bob_acctunit.add_membership(fly_str)
    assert before_sue_budunit.tally != 55
    assert before_sue_budunit.max_tree_traverse != 66
    assert before_sue_budunit.credor_respect != 77
    assert before_sue_budunit.debtor_respect != 88
    assert before_sue_budunit.acct_exists(yao_str)
    assert before_sue_budunit.acct_exists(zia_str)
    assert yao_acctunit.get_membership(fly_str) is not None
    assert bob_acctunit.get_membership(fly_str) is not None

    # WHEN
    ex1_buddelta = get_buddelta_example1()
    after_sue_budunit = ex1_buddelta.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.tally == 55
    assert after_sue_budunit.max_tree_traverse == 66
    assert after_sue_budunit.credor_respect == 77
    assert after_sue_budunit.debtor_respect == 88
    assert after_sue_budunit.acct_exists(yao_str)
    assert after_sue_budunit.acct_exists(zia_str) is False
