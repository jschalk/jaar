from src._road.road import get_terminus_node, get_parent_road
from src.bud.lobby import awardlink_shop
from src.bud.reason_idea import factunit_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.gift.atom import (
    atom_update,
    atom_delete,
    atom_insert,
    atomunit_shop,
)
from src.gift.change import changeunit_shop
from src.gift.examples.example_changes import get_changeunit_example1


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_SimplestScenario():
    # ESTABLISH
    ex1_changeunit = changeunit_shop()

    # WHEN
    sue_text = "Sue"
    sue_weight = 55
    before_sue_budunit = budunit_shop(sue_text, _weight=sue_weight)
    after_sue_budunit = ex1_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit._weight == sue_weight
    assert after_sue_budunit == before_sue_budunit


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnitSimpleAttrs():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    sue_weight = 44
    before_sue_budunit = budunit_shop(sue_text, _weight=sue_weight)

    category = "budunit"
    x_atomunit = atomunit_shop(category, atom_update())
    new1_value = 55
    new1_arg = "_weight"
    x_atomunit.set_optional_arg(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "_max_tree_traverse"
    x_atomunit.set_optional_arg(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "_credor_respect"
    x_atomunit.set_optional_arg(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "_debtor_respect"
    x_atomunit.set_optional_arg(new4_arg, new4_value)
    new9_value = 55550000
    new9_arg = "_fund_pool"
    x_atomunit.set_optional_arg(new9_arg, new9_value)
    new8_value = 0.5555
    new8_arg = "_fund_coin"
    x_atomunit.set_optional_arg(new8_arg, new8_value)
    sue_changeunit.set_atomunit(x_atomunit)
    new6_value = 0.5
    new6_arg = "_bit"
    x_atomunit.set_optional_arg(new6_arg, new6_value)
    sue_changeunit.set_atomunit(x_atomunit)
    new7_value = 0.025
    new7_arg = "_penny"
    x_atomunit.set_optional_arg(new7_arg, new7_value)
    sue_changeunit.set_atomunit(x_atomunit)

    # WHEN
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    print(f"{sue_changeunit.atomunits.keys()=}")
    assert after_sue_budunit._max_tree_traverse == new2_value
    assert after_sue_budunit._credor_respect == new3_value
    assert after_sue_budunit._debtor_respect == new4_value
    assert after_sue_budunit._weight == new1_value
    assert after_sue_budunit._weight != before_sue_budunit._weight
    assert after_sue_budunit._fund_pool == new9_value
    assert after_sue_budunit._fund_pool != before_sue_budunit._fund_pool
    assert after_sue_budunit._fund_coin == new8_value
    assert after_sue_budunit._fund_coin != before_sue_budunit._fund_coin
    assert after_sue_budunit._bit == new6_value
    assert after_sue_budunit._bit != before_sue_budunit._bit
    assert after_sue_budunit._penny == new7_value
    assert after_sue_budunit._penny != before_sue_budunit._penny


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_char():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    before_sue_budunit.add_charunit(yao_text)
    before_sue_budunit.add_charunit(zia_text)

    category = "bud_charunit"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg("char_id", zia_text)
    sue_changeunit.set_atomunit(x_atomunit)

    # WHEN
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    print(f"{sue_changeunit.atomunits=}")
    assert after_sue_budunit != before_sue_budunit
    assert after_sue_budunit.char_exists(yao_text)
    assert after_sue_budunit.char_exists(zia_text) is False


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_char():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    before_sue_budunit.add_charunit(yao_text)
    assert before_sue_budunit.char_exists(yao_text)
    assert before_sue_budunit.char_exists(zia_text) is False

    # WHEN
    category = "bud_charunit"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_required_arg("char_id", zia_text)
    x_credor_weight = 55
    x_debtor_weight = 66
    x_atomunit.set_optional_arg("credor_weight", x_credor_weight)
    x_atomunit.set_optional_arg("debtor_weight", x_debtor_weight)
    sue_changeunit.set_atomunit(x_atomunit)
    print(f"{sue_changeunit.atomunits.keys()=}")
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    yao_charunit = after_sue_budunit.get_char(yao_text)
    zia_charunit = after_sue_budunit.get_char(zia_text)
    assert yao_charunit != None
    assert zia_charunit != None
    assert zia_charunit.credor_weight == x_credor_weight
    assert zia_charunit.debtor_weight == x_debtor_weight


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_char():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    before_sue_budunit.add_charunit(yao_text)
    assert before_sue_budunit.get_char(yao_text).credor_weight == 1

    # WHEN
    category = "bud_charunit"
    x_atomunit = atomunit_shop(category, atom_update())
    x_atomunit.set_required_arg("char_id", yao_text)
    yao_credor_weight = 55
    x_atomunit.set_optional_arg("credor_weight", yao_credor_weight)
    sue_changeunit.set_atomunit(x_atomunit)
    print(f"{sue_changeunit.atomunits.keys()=}")
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    yao_char = after_sue_budunit.get_char(yao_text)
    assert yao_char.credor_weight == yao_credor_weight


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_lobbyship():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    before_sue_budunit.add_charunit(yao_text)
    before_sue_budunit.add_charunit(zia_text)
    before_sue_budunit.add_charunit(bob_text)
    yao_charunit = before_sue_budunit.get_char(yao_text)
    zia_charunit = before_sue_budunit.get_char(zia_text)
    bob_charunit = before_sue_budunit.get_char(bob_text)
    run_text = ",runners"
    yao_charunit.add_lobbyship(run_text)
    zia_charunit.add_lobbyship(run_text)
    fly_text = ",flyers"
    yao_charunit.add_lobbyship(fly_text)
    zia_charunit.add_lobbyship(fly_text)
    bob_charunit.add_lobbyship(fly_text)
    before_lobby_ids_dict = before_sue_budunit.get_lobby_ids_dict()
    assert len(before_lobby_ids_dict.get(run_text)) == 2
    assert len(before_lobby_ids_dict.get(fly_text)) == 3

    # WHEN
    yao_atomunit = atomunit_shop("bud_char_lobbyship", atom_delete())
    yao_atomunit.set_required_arg("lobby_id", run_text)
    yao_atomunit.set_required_arg("char_id", yao_text)
    # print(f"{yao_atomunit=}")
    zia_atomunit = atomunit_shop("bud_char_lobbyship", atom_delete())
    zia_atomunit.set_required_arg("lobby_id", fly_text)
    zia_atomunit.set_required_arg("char_id", zia_text)
    # print(f"{zia_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(yao_atomunit)
    sue_changeunit.set_atomunit(zia_atomunit)
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_lobby_ids_dict = after_sue_budunit.get_lobby_ids_dict()
    assert len(after_lobby_ids_dict.get(run_text)) == 1
    assert len(after_lobby_ids_dict.get(fly_text)) == 2


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_lobbyship():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    before_sue_budunit.add_charunit(yao_text)
    before_sue_budunit.add_charunit(zia_text)
    before_sue_budunit.add_charunit(bob_text)
    run_text = ",runners"
    zia_charunit = before_sue_budunit.get_char(zia_text)
    zia_charunit.add_lobbyship(run_text)
    before_lobby_ids = before_sue_budunit.get_lobby_ids_dict()
    assert len(before_lobby_ids.get(run_text)) == 1

    # WHEN
    yao_atomunit = atomunit_shop("bud_char_lobbyship", atom_insert())
    yao_atomunit.set_required_arg("lobby_id", run_text)
    yao_atomunit.set_required_arg("char_id", yao_text)
    yao_run_credor_weight = 17
    yao_atomunit.set_optional_arg("credor_weight", yao_run_credor_weight)
    print(f"{yao_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(yao_atomunit)
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_lobby_ids = after_sue_budunit.get_lobby_ids_dict()
    assert len(after_lobby_ids.get(run_text)) == 2
    after_yao_charunit = after_sue_budunit.get_char(yao_text)
    after_yao_run_lobbyship = after_yao_charunit.get_lobbyship(run_text)
    assert after_yao_run_lobbyship != None
    assert after_yao_run_lobbyship.credor_weight == yao_run_credor_weight


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_lobbyship():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    before_sue_budunit.add_charunit(yao_text)
    before_yao_charunit = before_sue_budunit.get_char(yao_text)
    run_text = ",runners"
    old_yao_run_credor_weight = 3
    before_yao_charunit.add_lobbyship(run_text, old_yao_run_credor_weight)
    yao_run_lobbyship = before_yao_charunit.get_lobbyship(run_text)
    assert yao_run_lobbyship.credor_weight == old_yao_run_credor_weight
    assert yao_run_lobbyship.debtor_weight == 1

    # WHEN
    yao_atomunit = atomunit_shop("bud_char_lobbyship", atom_update())
    yao_atomunit.set_required_arg("lobby_id", run_text)
    yao_atomunit.set_required_arg("char_id", yao_text)
    new_yao_run_credor_weight = 7
    new_yao_run_debtor_weight = 11
    yao_atomunit.set_optional_arg("credor_weight", new_yao_run_credor_weight)
    yao_atomunit.set_optional_arg("debtor_weight", new_yao_run_debtor_weight)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(yao_atomunit)
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_yao_charunit = after_sue_budunit.get_char(yao_text)
    after_yao_run_lobbyship = after_yao_charunit.get_lobbyship(run_text)
    assert after_yao_run_lobbyship.credor_weight == new_yao_run_credor_weight
    assert after_yao_run_lobbyship.debtor_weight == new_yao_run_debtor_weight


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_ideaunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_budunit.make_road(sports_road, disc_text)
    before_sue_budunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_budunit.add_idea(ideaunit_shop(disc_text), sports_road)
    assert before_sue_budunit.idea_exists(ball_road)
    assert before_sue_budunit.idea_exists(disc_road)

    # WHEN
    delete_disc_atomunit = atomunit_shop("bud_ideaunit", atom_delete())
    delete_disc_atomunit.set_required_arg(
        "label", get_terminus_node(disc_road, before_sue_budunit._road_delimiter)
    )
    print(f"{disc_road=}")
    delete_disc_atomunit.set_required_arg(
        "parent_road",
        get_parent_road(disc_road, before_sue_budunit._road_delimiter),
    )
    print(f"{delete_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(delete_disc_atomunit)
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.idea_exists(ball_road)
    assert after_sue_budunit.idea_exists(disc_road) is False


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_ideaunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_budunit.make_road(sports_road, disc_text)
    before_sue_budunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_budunit.idea_exists(ball_road)
    assert before_sue_budunit.idea_exists(disc_road) is False

    # WHEN
    # x_addin = 140
    # x_begin = 1000
    # x_close = 1700
    # x_denom = 17
    x_numeric_road = None
    # x_numor = 10
    x_pledge = True
    insert_disc_atomunit = atomunit_shop("bud_ideaunit", atom_insert())
    insert_disc_atomunit.set_required_arg("label", disc_text)
    insert_disc_atomunit.set_required_arg("parent_road", sports_road)
    # insert_disc_atomunit.set_optional_arg("_addin", x_addin)
    # insert_disc_atomunit.set_optional_arg("_begin", x_begin)
    # insert_disc_atomunit.set_optional_arg("_close", x_close)
    # insert_disc_atomunit.set_optional_arg("_denom", x_denom)
    insert_disc_atomunit.set_optional_arg("_numeric_road", x_numeric_road)
    # insert_disc_atomunit.set_optional_arg("_numor", x_numor)
    insert_disc_atomunit.set_optional_arg("pledge", x_pledge)

    print(f"{insert_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(insert_disc_atomunit)
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.idea_exists(ball_road)
    assert after_sue_budunit.idea_exists(disc_road)


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_ideaunit_SimpleAttributes():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_text)
    before_sue_budunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_budunit.get_idea_obj(ball_road)._begin is None
    assert before_sue_budunit.get_idea_obj(ball_road)._close is None
    assert before_sue_budunit.get_idea_obj(ball_road).pledge is False

    # WHEN
    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    # x_numor = 10
    x_pledge = True
    insert_disc_atomunit = atomunit_shop("bud_ideaunit", atom_update())
    insert_disc_atomunit.set_required_arg("label", ball_text)
    insert_disc_atomunit.set_required_arg("parent_road", sports_road)
    # insert_disc_atomunit.set_optional_arg("_addin", x_addin)
    insert_disc_atomunit.set_optional_arg("_begin", x_begin)
    insert_disc_atomunit.set_optional_arg("_close", x_close)
    # insert_disc_atomunit.set_optional_arg("_denom", x_denom)
    # insert_disc_atomunit.set_optional_arg("_numor", x_numor)
    insert_disc_atomunit.set_optional_arg("pledge", x_pledge)

    print(f"{insert_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(insert_disc_atomunit)
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit.get_idea_obj(ball_road)._begin == x_begin
    assert after_sue_budunit.get_idea_obj(ball_road)._close == x_close
    assert after_sue_budunit.get_idea_obj(ball_road).pledge


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_idea_awardlink():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    before_sue_budunit.add_charunit(yao_text)
    before_sue_budunit.add_charunit(zia_text)
    before_sue_budunit.add_charunit(bob_text)
    yao_charunit = before_sue_budunit.get_char(yao_text)
    zia_charunit = before_sue_budunit.get_char(zia_text)
    bob_charunit = before_sue_budunit.get_char(bob_text)
    run_text = ",runners"
    yao_charunit.add_lobbyship(run_text)
    zia_charunit.add_lobbyship(run_text)
    fly_text = ",flyers"
    yao_charunit.add_lobbyship(fly_text)
    zia_charunit.add_lobbyship(fly_text)
    bob_charunit.add_lobbyship(fly_text)

    sports_text = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_budunit.make_road(sports_road, disc_text)
    before_sue_budunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_budunit.add_idea(ideaunit_shop(disc_text), sports_road)
    before_sue_budunit.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_text))
    before_sue_budunit.edit_idea_attr(ball_road, awardlink=awardlink_shop(fly_text))
    before_sue_budunit.edit_idea_attr(disc_road, awardlink=awardlink_shop(run_text))
    before_sue_budunit.edit_idea_attr(disc_road, awardlink=awardlink_shop(fly_text))
    assert len(before_sue_budunit.get_idea_obj(ball_road)._awardlinks) == 2
    assert len(before_sue_budunit.get_idea_obj(disc_road)._awardlinks) == 2

    # WHEN
    delete_disc_atomunit = atomunit_shop("bud_idea_awardlink", atom_delete())
    delete_disc_atomunit.set_required_arg("road", disc_road)
    delete_disc_atomunit.set_required_arg("lobby_id", fly_text)
    print(f"{delete_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(delete_disc_atomunit)
    after_sue_budunit = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert len(after_sue_budunit.get_idea_obj(ball_road)._awardlinks) == 2
    assert len(after_sue_budunit.get_idea_obj(disc_road)._awardlinks) == 1


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_idea_awardlink():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    before_sue_budunit.add_charunit(yao_text)
    before_sue_budunit.add_charunit(zia_text)
    yao_charunit = before_sue_budunit.get_char(yao_text)
    run_text = ",runners"
    yao_charunit.add_lobbyship(run_text)

    sports_text = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_text)
    before_sue_budunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_budunit.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_text))
    run_awardlink = before_sue_budunit.get_idea_obj(ball_road)._awardlinks.get(run_text)
    assert run_awardlink.give_weight == 1
    assert run_awardlink.take_weight == 1

    # WHEN
    x_give_weight = 55
    x_take_weight = 66
    update_disc_atomunit = atomunit_shop("bud_idea_awardlink", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("lobby_id", run_text)
    update_disc_atomunit.set_optional_arg("give_weight", x_give_weight)
    update_disc_atomunit.set_optional_arg("take_weight", x_take_weight)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    run_awardlink = after_sue_au.get_idea_obj(ball_road)._awardlinks.get(run_text)
    print(f"{run_awardlink.give_weight=}")
    assert run_awardlink.give_weight == x_give_weight
    assert run_awardlink.take_weight == x_take_weight


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_idea_awardlink():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    before_sue_budunit.add_charunit(yao_text)
    before_sue_budunit.add_charunit(zia_text)
    run_text = ",runners"
    yao_charunit = before_sue_budunit.get_char(yao_text)
    yao_charunit.add_lobbyship(run_text)
    sports_text = "sports"
    sports_road = before_sue_budunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_budunit.make_road(sports_road, ball_text)
    before_sue_budunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_idea = before_sue_budunit.get_idea_obj(ball_road)
    assert before_ball_idea._awardlinks.get(run_text) is None

    # WHEN
    x_give_weight = 55
    x_take_weight = 66
    update_disc_atomunit = atomunit_shop("bud_idea_awardlink", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("lobby_id", run_text)
    update_disc_atomunit.set_optional_arg("give_weight", x_give_weight)
    update_disc_atomunit.set_optional_arg("take_weight", x_take_weight)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._awardlinks.get(run_text) != None


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_idea_factunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._factunits == {}

    # WHEN
    broken_open = 55
    broken_nigh = 66
    update_disc_atomunit = atomunit_shop("bud_idea_factunit", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg("pick", broken_road)
    update_disc_atomunit.set_optional_arg("open", broken_open)
    update_disc_atomunit.set_optional_arg("nigh", broken_nigh)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits != {}
    assert after_ball_idea._factunits.get(knee_road) != None
    assert after_ball_idea._factunits.get(knee_road).base == knee_road
    assert after_ball_idea._factunits.get(knee_road).pick == broken_road
    assert after_ball_idea._factunits.get(knee_road).open == broken_open
    assert after_ball_idea._factunits.get(knee_road).nigh == broken_nigh


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_idea_factunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.edit_idea_attr(
        road=ball_road, factunit=factunit_shop(base=knee_road, pick=broken_road)
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._factunits != {}
    assert before_ball_idea._factunits.get(knee_road) != None

    # WHEN
    update_disc_atomunit = atomunit_shop("bud_idea_factunit", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits == {}


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_idea_factunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_knee_factunit = factunit_shop(knee_road, broken_road)
    before_sue_au.edit_idea_attr(ball_road, factunit=before_knee_factunit)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._factunits != {}
    assert before_ball_idea._factunits.get(knee_road) != None
    assert before_ball_idea._factunits.get(knee_road).pick == broken_road
    assert before_ball_idea._factunits.get(knee_road).open is None
    assert before_ball_idea._factunits.get(knee_road).nigh is None

    # WHEN
    medical_open = 45
    medical_nigh = 77
    update_disc_atomunit = atomunit_shop("bud_idea_factunit", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg("pick", medical_road)
    update_disc_atomunit.set_optional_arg("open", medical_open)
    update_disc_atomunit.set_optional_arg("nigh", medical_nigh)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits != {}
    assert after_ball_idea._factunits.get(knee_road) != None
    assert after_ball_idea._factunits.get(knee_road).pick == medical_road
    assert after_ball_idea._factunits.get(knee_road).open == medical_open
    assert after_ball_idea._factunits.get(knee_road).nigh == medical_nigh


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_idea_reason_premiseunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._reasonunits != {}
    before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_knee_reasonunit != None
    broken_premiseunit = before_knee_reasonunit.get_premise(broken_road)
    assert broken_premiseunit.need == broken_road
    assert broken_premiseunit.open is None
    assert broken_premiseunit.nigh is None
    assert broken_premiseunit.divisor is None

    # WHEN
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    update_disc_atomunit = atomunit_shop("bud_idea_reason_premiseunit", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_required_arg("need", broken_road)
    update_disc_atomunit.set_optional_arg("open", broken_open)
    update_disc_atomunit.set_optional_arg("nigh", broken_nigh)
    update_disc_atomunit.set_optional_arg("divisor", broken_divisor)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    after_broken_premiseunit = after_knee_reasonunit.get_premise(broken_road)
    assert after_broken_premiseunit.need == broken_road
    assert after_broken_premiseunit.open == broken_open
    assert after_broken_premiseunit.nigh == broken_nigh
    assert after_broken_premiseunit.divisor == broken_divisor


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_idea_reason_premiseunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_knee_reasonunit.get_premise(broken_road) != None
    assert before_knee_reasonunit.get_premise(medical_road) is None

    # WHEN
    medical_open = 45
    medical_nigh = 77
    medical_divisor = 3
    update_disc_atomunit = atomunit_shop("bud_idea_reason_premiseunit", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_required_arg("need", medical_road)
    update_disc_atomunit.set_optional_arg("open", medical_open)
    update_disc_atomunit.set_optional_arg("nigh", medical_nigh)
    update_disc_atomunit.set_optional_arg("divisor", medical_divisor)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_road)
    assert after_medical_premiseunit != None
    assert after_medical_premiseunit.need == medical_road
    assert after_medical_premiseunit.open == medical_open
    assert after_medical_premiseunit.nigh == medical_nigh
    assert after_medical_premiseunit.divisor == medical_divisor


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_idea_reason_premiseunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=medical_road
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_knee_reasonunit.get_premise(broken_road) != None
    assert before_knee_reasonunit.get_premise(medical_road) != None

    # WHEN
    update_disc_atomunit = atomunit_shop("bud_idea_reason_premiseunit", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_required_arg("need", medical_road)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit.get_premise(broken_road) != None
    assert after_knee_reasonunit.get_premise(medical_road) is None


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_idea_reasonunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea.get_reasonunit(knee_road) is None

    # WHEN
    medical_base_idea_active_requisite = True
    update_disc_atomunit = atomunit_shop("bud_idea_reasonunit", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg(
        "base_idea_active_requisite", medical_base_idea_active_requisite
    )
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert (
        after_knee_reasonunit.base_idea_active_requisite
        == medical_base_idea_active_requisite
    )


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_update_idea_reasonunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_medical_base_idea_active_requisite = False
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_sue_au.edit_idea_attr(
        road=ball_road,
        reason_base=knee_road,
        reason_base_idea_active_requisite=before_medical_base_idea_active_requisite,
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    before_ball_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_ball_reasonunit != None
    assert (
        before_ball_reasonunit.base_idea_active_requisite
        == before_medical_base_idea_active_requisite
    )

    # WHEN
    after_medical_base_idea_active_requisite = True
    update_disc_atomunit = atomunit_shop("bud_idea_reasonunit", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg(
        "base_idea_active_requisite", after_medical_base_idea_active_requisite
    )
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert (
        after_knee_reasonunit.base_idea_active_requisite
        == after_medical_base_idea_active_requisite
    )


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_idea_reasonunit():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    medical_base_idea_active_requisite = False
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.edit_idea_attr(
        road=ball_road,
        reason_base=knee_road,
        reason_base_idea_active_requisite=medical_base_idea_active_requisite,
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea.get_reasonunit(knee_road) != None

    # WHEN
    update_disc_atomunit = atomunit_shop("bud_idea_reasonunit", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea.get_reasonunit(knee_road) is None


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_insert_idea_lobbyhold():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    yao_text = "Yao"
    before_sue_au.add_charunit(yao_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_ideaunit._doerunit._lobbyholds == set()

    # WHEN
    update_disc_atomunit = atomunit_shop("bud_idea_lobbyhold", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("lobby_id", yao_text)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._doerunit._lobbyholds != {}
    assert after_ball_ideaunit._doerunit.get_lobbyhold(yao_text) != None


def test_ChangeUnit_get_edited_bud_ReturnsCorrectObj_BudUnit_delete_idea_lobbyhold():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    yao_text = "Yao"
    before_sue_au.add_charunit(yao_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    before_ball_ideaunit._doerunit.set_lobbyhold(yao_text)
    assert before_ball_ideaunit._doerunit._lobbyholds != {}
    assert before_ball_ideaunit._doerunit.get_lobbyhold(yao_text) != None

    # WHEN
    update_disc_atomunit = atomunit_shop("bud_idea_lobbyhold", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("lobby_id", yao_text)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    print(f"{before_sue_au.get_idea_obj(ball_road)._doerunit=}")
    after_sue_au = sue_changeunit.get_edited_bud(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._doerunit._lobbyholds == set()


def test_ChangeUnit_get_changeunit_example1_ContainsAtomUnits():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    before_sue_budunit.add_charunit(yao_text)
    before_sue_budunit.add_charunit(zia_text)
    before_sue_budunit.add_charunit(bob_text)
    yao_charunit = before_sue_budunit.get_char(yao_text)
    zia_charunit = before_sue_budunit.get_char(zia_text)
    bob_charunit = before_sue_budunit.get_char(bob_text)
    run_text = ",runners"
    yao_charunit.add_lobbyship(run_text)
    zia_charunit.add_lobbyship(run_text)
    fly_text = ",flyers"
    yao_charunit.add_lobbyship(fly_text)
    bob_charunit.add_lobbyship(fly_text)
    assert before_sue_budunit._weight != 55
    assert before_sue_budunit._max_tree_traverse != 66
    assert before_sue_budunit._credor_respect != 77
    assert before_sue_budunit._debtor_respect != 88
    assert before_sue_budunit.char_exists(yao_text)
    assert before_sue_budunit.char_exists(zia_text)
    assert yao_charunit.get_lobbyship(fly_text) != None
    assert bob_charunit.get_lobbyship(fly_text) != None

    # WHEN
    ex1_changeunit = get_changeunit_example1()
    after_sue_budunit = ex1_changeunit.get_edited_bud(before_sue_budunit)

    # THEN
    assert after_sue_budunit._weight == 55
    assert after_sue_budunit._max_tree_traverse == 66
    assert after_sue_budunit._credor_respect == 77
    assert after_sue_budunit._debtor_respect == 88
    assert after_sue_budunit.char_exists(yao_text)
    assert after_sue_budunit.char_exists(zia_text) is False
