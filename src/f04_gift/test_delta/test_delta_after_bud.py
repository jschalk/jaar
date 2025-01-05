from src.f01_road.road import get_terminus_title, get_parent_road
from src.f02_bud.group import awardlink_shop
from src.f02_bud.reason_item import factunit_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
)
from src.f04_gift.atom import atom_update, atom_delete, atom_insert, atomunit_shop
from src.f04_gift.atom_config import (
    acct_name_str,
    awardee_tag_str,
    group_label_str,
    team_tag_str,
    healer_name_str,
    parent_road_str,
    item_title_str,
    base_item_active_requisite_str,
    pledge_str,
    begin_str,
    close_str,
    credit_vote_str,
    debtit_vote_str,
    gogo_want_str,
    stop_want_str,
    fopen_str,
    fnigh_str,
    give_force_str,
    take_force_str,
)
from src.f04_gift.delta import deltaunit_shop
from src.f04_gift.examples.example_deltas import get_deltaunit_example1


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_SimplestScenario():
    # ESTABLISH
    ex1_deltaunit = deltaunit_shop()

    # WHEN
    sue_str = "Sue"
    sue_tally = 55
    before_sue_budunit = budunit_shop(sue_str, tally=sue_tally)
    after_sue_budunit = ex1_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.tally == sue_tally
    assert after_sue_budunit == before_sue_budunit


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnitSimpleAttrs():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    sue_str = "Sue"

    sue_tally = 44
    before_sue_budunit = budunit_shop(sue_str, tally=sue_tally)

    category = budunit_str()
    x_atomunit = atomunit_shop(category, atom_update())
    new1_value = 55
    new1_arg = "tally"
    x_atomunit.set_jvalue(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "max_tree_traverse"
    x_atomunit.set_jvalue(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "credor_respect"
    x_atomunit.set_jvalue(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "debtor_respect"
    x_atomunit.set_jvalue(new4_arg, new4_value)
    new9_value = 55550000
    new9_arg = "fund_pool"
    x_atomunit.set_jvalue(new9_arg, new9_value)
    new8_value = 0.5555
    new8_arg = "fund_coin"
    x_atomunit.set_jvalue(new8_arg, new8_value)
    sue_deltaunit.set_atomunit(x_atomunit)
    new6_value = 0.5
    new6_arg = "respect_bit"
    x_atomunit.set_jvalue(new6_arg, new6_value)
    sue_deltaunit.set_atomunit(x_atomunit)
    new7_value = 0.025
    new7_arg = "penny"
    x_atomunit.set_jvalue(new7_arg, new7_value)
    sue_deltaunit.set_atomunit(x_atomunit)
    new0_value = 9900000
    new0_arg = "deal_time_int"
    x_atomunit.set_jvalue(new0_arg, new0_value)
    sue_deltaunit.set_atomunit(x_atomunit)

    # WHEN
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    print(f"{sue_deltaunit.atomunits.keys()=}")
    assert after_sue_budunit.max_tree_traverse == new2_value
    assert after_sue_budunit.credor_respect == new3_value
    assert after_sue_budunit.debtor_respect == new4_value
    assert after_sue_budunit.tally == new1_value
    assert after_sue_budunit.tally != before_sue_budunit.tally
    assert after_sue_budunit.fund_pool == new9_value
    assert after_sue_budunit.fund_pool != before_sue_budunit.fund_pool
    assert after_sue_budunit.fund_coin == new8_value
    assert after_sue_budunit.fund_coin != before_sue_budunit.fund_coin
    assert after_sue_budunit.respect_bit == new6_value
    assert after_sue_budunit.respect_bit != before_sue_budunit.respect_bit
    assert after_sue_budunit.penny == new7_value
    assert after_sue_budunit.penny != before_sue_budunit.penny
    assert after_sue_budunit.deal_time_int == new0_value
    assert after_sue_budunit.deal_time_int != before_sue_budunit.deal_time_int


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_acct():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    sue_str = "Sue"

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    before_sue_budunit.add_acctunit(zia_str)

    category = bud_acctunit_str()
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_jkey(acct_name_str(), zia_str)
    sue_deltaunit.set_atomunit(x_atomunit)

    # WHEN
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    print(f"{sue_deltaunit.atomunits=}")
    assert after_sue_budunit != before_sue_budunit
    assert after_sue_budunit.acct_exists(yao_str)
    assert after_sue_budunit.acct_exists(zia_str) is False


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_acct():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    sue_str = "Sue"

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    assert before_sue_budunit.acct_exists(yao_str)
    assert before_sue_budunit.acct_exists(zia_str) is False

    # WHEN
    category = bud_acctunit_str()
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_jkey(acct_name_str(), zia_str)
    x_credit_belief = 55
    x_debtit_belief = 66
    x_atomunit.set_jvalue("credit_belief", x_credit_belief)
    x_atomunit.set_jvalue("debtit_belief", x_debtit_belief)
    sue_deltaunit.set_atomunit(x_atomunit)
    print(f"{sue_deltaunit.atomunits.keys()=}")
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    yao_acctunit = after_sue_budunit.get_acct(yao_str)
    zia_acctunit = after_sue_budunit.get_acct(zia_str)
    assert yao_acctunit is not None
    assert zia_acctunit is not None
    assert zia_acctunit.credit_belief == x_credit_belief
    assert zia_acctunit.debtit_belief == x_debtit_belief


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_acct():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    sue_str = "Sue"

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_budunit.add_acctunit(yao_str)
    assert before_sue_budunit.get_acct(yao_str).credit_belief == 1

    # WHEN
    category = bud_acctunit_str()
    x_atomunit = atomunit_shop(category, atom_update())
    x_atomunit.set_jkey(acct_name_str(), yao_str)
    yao_credit_belief = 55
    x_atomunit.set_jvalue("credit_belief", yao_credit_belief)
    sue_deltaunit.set_atomunit(x_atomunit)
    print(f"{sue_deltaunit.atomunits.keys()=}")
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    yao_acct = after_sue_budunit.get_acct(yao_str)
    assert yao_acct.credit_belief == yao_credit_belief


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_membership():
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
    before_group_labels_dict = before_sue_budunit.get_acctunit_group_labels_dict()
    assert len(before_group_labels_dict.get(run_str)) == 2
    assert len(before_group_labels_dict.get(fly_str)) == 3

    # WHEN
    yao_atomunit = atomunit_shop(bud_acct_membership_str(), atom_delete())
    yao_atomunit.set_jkey(group_label_str(), run_str)
    yao_atomunit.set_jkey(acct_name_str(), yao_str)
    # print(f"{yao_atomunit=}")
    zia_atomunit = atomunit_shop(bud_acct_membership_str(), atom_delete())
    zia_atomunit.set_jkey(group_label_str(), fly_str)
    zia_atomunit.set_jkey(acct_name_str(), zia_str)
    # print(f"{zia_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(yao_atomunit)
    sue_deltaunit.set_atomunit(zia_atomunit)
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_group_labels_dict = after_sue_budunit.get_acctunit_group_labels_dict()
    assert len(after_group_labels_dict.get(run_str)) == 1
    assert len(after_group_labels_dict.get(fly_str)) == 2


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_membership():
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
    before_group_labels = before_sue_budunit.get_acctunit_group_labels_dict()
    assert len(before_group_labels.get(run_str)) == 1

    # WHEN
    yao_atomunit = atomunit_shop(bud_acct_membership_str(), atom_insert())
    yao_atomunit.set_jkey(group_label_str(), run_str)
    yao_atomunit.set_jkey(acct_name_str(), yao_str)
    yao_run_credit_vote = 17
    yao_atomunit.set_jvalue("credit_vote", yao_run_credit_vote)
    print(f"{yao_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(yao_atomunit)
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_group_labels = after_sue_budunit.get_acctunit_group_labels_dict()
    assert len(after_group_labels.get(run_str)) == 2
    after_yao_acctunit = after_sue_budunit.get_acct(yao_str)
    after_yao_run_membership = after_yao_acctunit.get_membership(run_str)
    assert after_yao_run_membership is not None
    assert after_yao_run_membership.credit_vote == yao_run_credit_vote


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_membership():
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
    yao_atomunit = atomunit_shop(bud_acct_membership_str(), atom_update())
    yao_atomunit.set_jkey(group_label_str(), run_str)
    yao_atomunit.set_jkey(acct_name_str(), yao_str)
    new_yao_run_credit_vote = 7
    new_yao_run_debtit_vote = 11
    yao_atomunit.set_jvalue(credit_vote_str(), new_yao_run_credit_vote)
    yao_atomunit.set_jvalue(debtit_vote_str(), new_yao_run_debtit_vote)
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(yao_atomunit)
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_yao_acctunit = after_sue_budunit.get_acct(yao_str)
    after_yao_run_membership = after_yao_acctunit.get_membership(run_str)
    assert after_yao_run_membership.credit_vote == new_yao_run_credit_vote
    assert after_yao_run_membership.debtit_vote == new_yao_run_debtit_vote


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_itemunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_str)
    disc_str = "Ultimate Disc"
    disc_road = before_sue_budunit.make_road(sports_road, disc_str)
    before_sue_budunit.set_item(itemunit_shop(ball_str), sports_road)
    before_sue_budunit.set_item(itemunit_shop(disc_str), sports_road)
    assert before_sue_budunit.item_exists(ball_road)
    assert before_sue_budunit.item_exists(disc_road)

    # WHEN
    delete_disc_atomunit = atomunit_shop(bud_itemunit_str(), atom_delete())
    delete_disc_atomunit.set_jkey(
        item_title_str(), get_terminus_title(disc_road, before_sue_budunit.bridge)
    )
    print(f"{disc_road=}")
    delete_disc_atomunit.set_jkey(
        parent_road_str(),
        get_parent_road(disc_road, before_sue_budunit.bridge),
    )
    print(f"{delete_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(delete_disc_atomunit)
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.item_exists(ball_road)
    assert after_sue_budunit.item_exists(disc_road) is False


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_itemunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_str)
    disc_str = "Ultimate Disc"
    disc_road = before_sue_budunit.make_road(sports_road, disc_str)
    before_sue_budunit.set_item(itemunit_shop(ball_str), sports_road)
    assert before_sue_budunit.item_exists(ball_road)
    assert before_sue_budunit.item_exists(disc_road) is False

    # WHEN
    # x_addin = 140
    x_gogo_want = 1000
    x_stop_want = 1700
    # x_denom = 17
    # x_numor = 10
    x_pledge = True
    insert_disc_atomunit = atomunit_shop(bud_itemunit_str(), atom_insert())
    insert_disc_atomunit.set_jkey(item_title_str(), disc_str)
    insert_disc_atomunit.set_jkey(parent_road_str(), sports_road)
    # insert_disc_atomunit.set_jvalue(addin_str(), x_addin)
    # insert_disc_atomunit.set_jvalue(begin_str(), x_begin)
    # insert_disc_atomunit.set_jvalue(close_str(), x_close)
    # insert_disc_atomunit.set_jvalue(denom_str(), x_denom)
    # insert_disc_atomunit.set_jvalue(numor_str(), x_numor)
    insert_disc_atomunit.set_jvalue(pledge_str(), x_pledge)
    insert_disc_atomunit.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_atomunit.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(insert_disc_atomunit)
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.item_exists(ball_road)
    assert after_sue_budunit.item_exists(disc_road)
    disc_item = after_sue_budunit.get_item_obj(disc_road)
    assert disc_item.gogo_want == x_gogo_want
    assert disc_item.stop_want == x_stop_want


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_itemunit_SimpleAttributes():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_budunit = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_str)
    before_sue_budunit.set_item(itemunit_shop(ball_str), sports_road)

    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    # x_numor = 10
    x_gogo_want = 1222
    x_stop_want = 1333
    x_pledge = True
    insert_disc_atomunit = atomunit_shop(bud_itemunit_str(), atom_update())
    insert_disc_atomunit.set_jkey(item_title_str(), ball_str)
    insert_disc_atomunit.set_jkey(parent_road_str(), sports_road)
    # insert_disc_atomunit.set_jvalue(addin_str(), x_addin)
    insert_disc_atomunit.set_jvalue(begin_str(), x_begin)
    insert_disc_atomunit.set_jvalue(close_str(), x_close)
    # insert_disc_atomunit.set_jvalue(denom_str(), x_denom)
    # insert_disc_atomunit.set_jvalue(numor_str(), x_numor)
    insert_disc_atomunit.set_jvalue(pledge_str(), x_pledge)
    insert_disc_atomunit.set_jvalue(gogo_want_str(), x_gogo_want)
    insert_disc_atomunit.set_jvalue(stop_want_str(), x_stop_want)

    print(f"{insert_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(insert_disc_atomunit)
    assert before_sue_budunit.get_item_obj(ball_road).begin is None
    assert before_sue_budunit.get_item_obj(ball_road).close is None
    assert before_sue_budunit.get_item_obj(ball_road).pledge is False
    assert before_sue_budunit.get_item_obj(ball_road).gogo_want is None
    assert before_sue_budunit.get_item_obj(ball_road).stop_want is None

    # WHEN
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.get_item_obj(ball_road).begin == x_begin
    assert after_sue_budunit.get_item_obj(ball_road).close == x_close
    assert after_sue_budunit.get_item_obj(ball_road).gogo_want == x_gogo_want
    assert after_sue_budunit.get_item_obj(ball_road).stop_want == x_stop_want
    assert after_sue_budunit.get_item_obj(ball_road).pledge


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_item_awardlink():
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
    sports_road = before_sue_budunit.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_str)
    disc_str = "Ultimate Disc"
    disc_road = before_sue_budunit.make_road(sports_road, disc_str)
    before_sue_budunit.set_item(itemunit_shop(ball_str), sports_road)
    before_sue_budunit.set_item(itemunit_shop(disc_str), sports_road)
    before_sue_budunit.edit_item_attr(ball_road, awardlink=awardlink_shop(run_str))
    before_sue_budunit.edit_item_attr(ball_road, awardlink=awardlink_shop(fly_str))
    before_sue_budunit.edit_item_attr(disc_road, awardlink=awardlink_shop(run_str))
    before_sue_budunit.edit_item_attr(disc_road, awardlink=awardlink_shop(fly_str))
    assert len(before_sue_budunit.get_item_obj(ball_road).awardlinks) == 2
    assert len(before_sue_budunit.get_item_obj(disc_road).awardlinks) == 2

    # WHEN
    delete_disc_atomunit = atomunit_shop(bud_item_awardlink_str(), atom_delete())
    delete_disc_atomunit.set_jkey("road", disc_road)
    delete_disc_atomunit.set_jkey(awardee_tag_str(), fly_str)
    print(f"{delete_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(delete_disc_atomunit)
    after_sue_budunit = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert len(after_sue_budunit.get_item_obj(ball_road).awardlinks) == 2
    assert len(after_sue_budunit.get_item_obj(disc_road).awardlinks) == 1


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_item_awardlink():
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
    sports_road = before_sue_budunit.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_str)
    before_sue_budunit.set_item(itemunit_shop(ball_str), sports_road)
    before_sue_budunit.edit_item_attr(ball_road, awardlink=awardlink_shop(run_str))
    run_awardlink = before_sue_budunit.get_item_obj(ball_road).awardlinks.get(run_str)
    assert run_awardlink.give_force == 1
    assert run_awardlink.take_force == 1

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_atomunit = atomunit_shop(bud_item_awardlink_str(), atom_update())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey(awardee_tag_str(), run_str)
    update_disc_atomunit.set_jvalue(give_force_str(), x_give_force)
    update_disc_atomunit.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    run_awardlink = after_sue_au.get_item_obj(ball_road).awardlinks.get(run_str)
    print(f"{run_awardlink.give_force=}")
    assert run_awardlink.give_force == x_give_force
    assert run_awardlink.take_force == x_take_force


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_item_awardlink():
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
    sports_road = before_sue_budunit.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_str)
    before_sue_budunit.set_item(itemunit_shop(ball_str), sports_road)
    before_ball_item = before_sue_budunit.get_item_obj(ball_road)
    assert before_ball_item.awardlinks.get(run_str) is None

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_atomunit = atomunit_shop(bud_item_awardlink_str(), atom_insert())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey(awardee_tag_str(), run_str)
    update_disc_atomunit.set_jvalue(give_force_str(), x_give_force)
    update_disc_atomunit.set_jvalue(take_force_str(), x_take_force)
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    assert after_ball_item.awardlinks.get(run_str) is not None


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_item_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_str)
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(broken_str), knee_road)
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    assert before_ball_item.factunits == {}

    # WHEN
    broken_fopen = 55
    broken_fnigh = 66
    update_disc_atomunit = atomunit_shop(bud_item_factunit_str(), atom_insert())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    update_disc_atomunit.set_jvalue("pick", broken_road)
    update_disc_atomunit.set_jvalue(fopen_str(), broken_fopen)
    update_disc_atomunit.set_jvalue(fnigh_str(), broken_fnigh)
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    assert after_ball_item.factunits != {}
    assert after_ball_item.factunits.get(knee_road) is not None
    assert after_ball_item.factunits.get(knee_road).base == knee_road
    assert after_ball_item.factunits.get(knee_road).pick == broken_road
    assert after_ball_item.factunits.get(knee_road).fopen == broken_fopen
    assert after_ball_item.factunits.get(knee_road).fnigh == broken_fnigh


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_item_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_str)
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(broken_str), knee_road)
    before_sue_au.edit_item_attr(
        road=ball_road, factunit=factunit_shop(base=knee_road, pick=broken_road)
    )
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    assert before_ball_item.factunits != {}
    assert before_ball_item.factunits.get(knee_road) is not None

    # WHEN
    update_disc_atomunit = atomunit_shop(bud_item_factunit_str(), atom_delete())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    assert after_ball_item.factunits == {}


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_item_factunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_str)
    medical_str = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_str)
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(broken_str), knee_road)
    before_sue_au.set_item(itemunit_shop(medical_str), knee_road)
    before_knee_factunit = factunit_shop(knee_road, broken_road)
    before_sue_au.edit_item_attr(ball_road, factunit=before_knee_factunit)
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    assert before_ball_item.factunits != {}
    assert before_ball_item.factunits.get(knee_road) is not None
    assert before_ball_item.factunits.get(knee_road).pick == broken_road
    assert before_ball_item.factunits.get(knee_road).fopen is None
    assert before_ball_item.factunits.get(knee_road).fnigh is None

    # WHEN
    medical_fopen = 45
    medical_fnigh = 77
    update_disc_atomunit = atomunit_shop(bud_item_factunit_str(), atom_update())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    update_disc_atomunit.set_jvalue("pick", medical_road)
    update_disc_atomunit.set_jvalue(fopen_str(), medical_fopen)
    update_disc_atomunit.set_jvalue(fnigh_str(), medical_fnigh)
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    assert after_ball_item.factunits != {}
    assert after_ball_item.factunits.get(knee_road) is not None
    assert after_ball_item.factunits.get(knee_road).pick == medical_road
    assert after_ball_item.factunits.get(knee_road).fopen == medical_fopen
    assert after_ball_item.factunits.get(knee_road).fnigh == medical_fnigh


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_item_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_str)
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(broken_str), knee_road)
    before_sue_au.edit_item_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    assert before_ball_item.reasonunits != {}
    before_knee_reasonunit = before_ball_item.get_reasonunit(knee_road)
    assert before_knee_reasonunit is not None
    broken_premiseunit = before_knee_reasonunit.get_premise(broken_road)
    assert broken_premiseunit.need == broken_road
    assert broken_premiseunit.open is None
    assert broken_premiseunit.nigh is None
    assert broken_premiseunit.divisor is None

    # WHEN
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    update_disc_atomunit = atomunit_shop(
        bud_item_reason_premiseunit_str(), atom_update()
    )
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    update_disc_atomunit.set_jkey("need", broken_road)
    update_disc_atomunit.set_jvalue("open", broken_open)
    update_disc_atomunit.set_jvalue("nigh", broken_nigh)
    update_disc_atomunit.set_jvalue("divisor", broken_divisor)
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    after_knee_reasonunit = after_ball_item.get_reasonunit(knee_road)
    assert after_knee_reasonunit is not None
    after_broken_premiseunit = after_knee_reasonunit.get_premise(broken_road)
    assert after_broken_premiseunit.need == broken_road
    assert after_broken_premiseunit.open == broken_open
    assert after_broken_premiseunit.nigh == broken_nigh
    assert after_broken_premiseunit.divisor == broken_divisor


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_item_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_str)
    medical_str = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_str)
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(broken_str), knee_road)
    before_sue_au.set_item(itemunit_shop(medical_str), knee_road)
    before_sue_au.edit_item_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    before_knee_reasonunit = before_ball_item.get_reasonunit(knee_road)
    assert before_knee_reasonunit.get_premise(broken_road) is not None
    assert before_knee_reasonunit.get_premise(medical_road) is None

    # WHEN
    medical_open = 45
    medical_nigh = 77
    medical_divisor = 3
    update_disc_atomunit = atomunit_shop(
        bud_item_reason_premiseunit_str(), atom_insert()
    )
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    update_disc_atomunit.set_jkey("need", medical_road)
    update_disc_atomunit.set_jvalue("open", medical_open)
    update_disc_atomunit.set_jvalue("nigh", medical_nigh)
    update_disc_atomunit.set_jvalue("divisor", medical_divisor)
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    after_knee_reasonunit = after_ball_item.get_reasonunit(knee_road)
    after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_road)
    assert after_medical_premiseunit is not None
    assert after_medical_premiseunit.need == medical_road
    assert after_medical_premiseunit.open == medical_open
    assert after_medical_premiseunit.nigh == medical_nigh
    assert after_medical_premiseunit.divisor == medical_divisor


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_item_reason_premiseunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_str)
    medical_str = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_str)
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(broken_str), knee_road)
    before_sue_au.set_item(itemunit_shop(medical_str), knee_road)
    before_sue_au.edit_item_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_sue_au.edit_item_attr(
        ball_road, reason_base=knee_road, reason_premise=medical_road
    )
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    before_knee_reasonunit = before_ball_item.get_reasonunit(knee_road)
    assert before_knee_reasonunit.get_premise(broken_road) is not None
    assert before_knee_reasonunit.get_premise(medical_road) is not None

    # WHEN
    update_disc_atomunit = atomunit_shop(
        bud_item_reason_premiseunit_str(), atom_delete()
    )
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    update_disc_atomunit.set_jkey("need", medical_road)
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    after_knee_reasonunit = after_ball_item.get_reasonunit(knee_road)
    assert after_knee_reasonunit.get_premise(broken_road) is not None
    assert after_knee_reasonunit.get_premise(medical_road) is None


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_item_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    medical_str = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_str)
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(medical_str), knee_road)
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    assert before_ball_item.get_reasonunit(knee_road) is None

    # WHEN
    medical_base_item_active_requisite = True
    update_disc_atomunit = atomunit_shop(bud_item_reasonunit_str(), atom_insert())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    update_disc_atomunit.set_jvalue(
        base_item_active_requisite_str(), medical_base_item_active_requisite
    )
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    after_knee_reasonunit = after_ball_item.get_reasonunit(knee_road)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert (
        after_knee_reasonunit.base_item_active_requisite
        == medical_base_item_active_requisite
    )


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_item_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    medical_str = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_str)
    before_medical_base_item_active_requisite = False
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.set_item(itemunit_shop(medical_str), knee_road)
    before_sue_au.edit_item_attr(
        road=ball_road,
        reason_base=knee_road,
        reason_base_item_active_requisite=before_medical_base_item_active_requisite,
    )
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    before_ball_reasonunit = before_ball_item.get_reasonunit(knee_road)
    assert before_ball_reasonunit is not None
    assert (
        before_ball_reasonunit.base_item_active_requisite
        == before_medical_base_item_active_requisite
    )

    # WHEN
    after_medical_base_item_active_requisite = True
    update_disc_atomunit = atomunit_shop(bud_item_reasonunit_str(), atom_update())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    update_disc_atomunit.set_jvalue(
        base_item_active_requisite_str(), after_medical_base_item_active_requisite
    )
    # print(f"{update_disc_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    after_knee_reasonunit = after_ball_item.get_reasonunit(knee_road)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert (
        after_knee_reasonunit.base_item_active_requisite
        == after_medical_base_item_active_requisite
    )


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_item_reasonunit():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_au.make_l1_road(knee_str)
    medical_base_item_active_requisite = False
    before_sue_au.set_l1_item(itemunit_shop(knee_str))
    before_sue_au.edit_item_attr(
        road=ball_road,
        reason_base=knee_road,
        reason_base_item_active_requisite=medical_base_item_active_requisite,
    )
    before_ball_item = before_sue_au.get_item_obj(ball_road)
    assert before_ball_item.get_reasonunit(knee_road) is not None

    # WHEN
    update_disc_atomunit = atomunit_shop(bud_item_reasonunit_str(), atom_delete())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey("base", knee_road)
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_item = after_sue_au.get_item_obj(ball_road)
    assert after_ball_item.get_reasonunit(knee_road) is None


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_item_teamlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    before_ball_itemunit = before_sue_au.get_item_obj(ball_road)
    assert before_ball_itemunit.teamunit._teamlinks == set()

    # WHEN
    update_disc_atomunit = atomunit_shop(bud_item_teamlink_str(), atom_insert())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey(team_tag_str(), yao_str)
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_itemunit = after_sue_au.get_item_obj(ball_road)
    assert after_ball_itemunit.teamunit._teamlinks != set()
    assert after_ball_itemunit.teamunit.get_teamlink(yao_str) is not None


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_item_teamlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    before_ball_itemunit = before_sue_au.get_item_obj(ball_road)
    before_ball_itemunit.teamunit.set_teamlink(yao_str)
    assert before_ball_itemunit.teamunit._teamlinks != set()
    assert before_ball_itemunit.teamunit.get_teamlink(yao_str) is not None

    # WHEN
    update_disc_atomunit = atomunit_shop(bud_item_teamlink_str(), atom_delete())
    update_disc_atomunit.set_jkey("road", ball_road)
    update_disc_atomunit.set_jkey(team_tag_str(), yao_str)
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(update_disc_atomunit)
    print(f"{before_sue_au.get_item_obj(ball_road).teamunit=}")
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_itemunit = after_sue_au.get_item_obj(ball_road)
    assert after_ball_itemunit.teamunit._teamlinks == set()


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_item_healerlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    before_ball_itemunit = before_sue_au.get_item_obj(ball_road)
    assert before_ball_itemunit.healerlink._healer_names == set()
    assert not before_ball_itemunit.healerlink.healer_name_exists(yao_str)

    # WHEN
    x_atomunit = atomunit_shop(bud_item_healerlink_str(), atom_insert())
    x_atomunit.set_jkey("road", ball_road)
    x_atomunit.set_jkey(healer_name_str(), yao_str)
    print(f"{x_atomunit=}")
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(x_atomunit)
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_itemunit = after_sue_au.get_item_obj(ball_road)
    assert after_ball_itemunit.healerlink._healer_names != set()
    assert after_ball_itemunit.healerlink.healer_name_exists(yao_str)


def test_DeltaUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_item_healerlink():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    yao_str = "Yao"
    before_sue_au.add_acctunit(yao_str)
    sports_str = "sports"
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_item(itemunit_shop(ball_str), sports_road)
    before_ball_itemunit = before_sue_au.get_item_obj(ball_road)
    before_ball_itemunit.healerlink.set_healer_name(yao_str)
    assert before_ball_itemunit.healerlink._healer_names != set()
    assert before_ball_itemunit.healerlink.healer_name_exists(yao_str)

    # WHEN
    x_atomunit = atomunit_shop(bud_item_healerlink_str(), atom_delete())
    x_atomunit.set_jkey("road", ball_road)
    x_atomunit.set_jkey(healer_name_str(), yao_str)
    sue_deltaunit = deltaunit_shop()
    sue_deltaunit.set_atomunit(x_atomunit)
    print(f"{before_sue_au.get_item_obj(ball_road).teamunit=}")
    after_sue_au = sue_deltaunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_itemunit = after_sue_au.get_item_obj(ball_road)
    assert after_ball_itemunit.healerlink._healer_names == set()
    assert not after_ball_itemunit.healerlink.healer_name_exists(yao_str)


def test_DeltaUnit_get_deltaunit_example1_ContainsAtomUnits():
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
    assert before_sue_budunit.deal_time_int != 990000
    assert before_sue_budunit.acct_exists(yao_str)
    assert before_sue_budunit.acct_exists(zia_str)
    assert yao_acctunit.get_membership(fly_str) is not None
    assert bob_acctunit.get_membership(fly_str) is not None

    # WHEN
    ex1_deltaunit = get_deltaunit_example1()
    after_sue_budunit = ex1_deltaunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.tally == 55
    assert after_sue_budunit.max_tree_traverse == 66
    assert after_sue_budunit.credor_respect == 77
    assert after_sue_budunit.debtor_respect == 88
    assert after_sue_budunit.deal_time_int == 990000
    assert after_sue_budunit.acct_exists(yao_str)
    assert after_sue_budunit.acct_exists(zia_str) is False
