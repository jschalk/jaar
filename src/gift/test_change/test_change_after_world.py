from src._road.road import get_terminus_node, get_parent_road
from src._world.beliefunit import fiscallink_shop
from src._world.char import charlink_shop
from src._world.reason_idea import factunit_shop
from src._world.idea import ideaunit_shop
from src._world.beliefunit import beliefunit_shop
from src._world.world import worldunit_shop
from src.gift.atom import (
    atom_update,
    atom_delete,
    atom_insert,
    atomunit_shop,
)
from src.gift.change import changeunit_shop
from src.gift.examples.example_changes import get_changeunit_example1


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_SimplestScenario():
    # GIVEN
    ex1_changeunit = changeunit_shop()

    # WHEN
    sue_text = "Sue"
    sue_weight = 55
    before_sue_worldunit = worldunit_shop(sue_text, _weight=sue_weight)
    after_sue_worldunit = ex1_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    assert after_sue_worldunit._weight == sue_weight
    assert after_sue_worldunit == before_sue_worldunit


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnitSimpleAttrs():
    # GIVEN
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    sue_weight = 44
    before_sue_worldunit = worldunit_shop(sue_text, _weight=sue_weight)

    category = "worldunit"
    x_atomunit = atomunit_shop(category, atom_update())
    new1_value = 55
    new1_arg = "_weight"
    x_atomunit.set_optional_arg(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "_max_tree_traverse"
    x_atomunit.set_optional_arg(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "_char_credor_pool"
    x_atomunit.set_optional_arg(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "_char_debtor_pool"
    x_atomunit.set_optional_arg(new4_arg, new4_value)
    new5_value = "override"
    new5_arg = "_meld_strategy"
    x_atomunit.set_optional_arg(new5_arg, new5_value)
    new6_value = 0.5
    new6_arg = "_pixel"
    x_atomunit.set_optional_arg(new6_arg, new6_value)
    sue_changeunit.set_atomunit(x_atomunit)
    new7_value = 0.025
    new7_arg = "_penny"
    x_atomunit.set_optional_arg(new7_arg, new7_value)
    sue_changeunit.set_atomunit(x_atomunit)

    # WHEN
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    print(f"{sue_changeunit.atomunits.keys()=}")
    assert after_sue_worldunit._max_tree_traverse == new2_value
    assert after_sue_worldunit._char_credor_pool == new3_value
    assert after_sue_worldunit._char_debtor_pool == new4_value
    assert after_sue_worldunit._meld_strategy == new5_value
    assert after_sue_worldunit._weight == new1_value
    assert after_sue_worldunit._weight != before_sue_worldunit._weight
    assert after_sue_worldunit._pixel == new6_value
    assert after_sue_worldunit._pixel != before_sue_worldunit._pixel
    assert after_sue_worldunit._penny == new7_value
    assert after_sue_worldunit._penny != before_sue_worldunit._penny


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_char():
    # GIVEN
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_worldunit.add_charunit(rico_text)
    before_sue_worldunit.add_charunit(carm_text)

    category = "world_charunit"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg("char_id", carm_text)
    sue_changeunit.set_atomunit(x_atomunit)

    # WHEN
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    print(f"{sue_changeunit.atomunits=}")
    assert after_sue_worldunit != before_sue_worldunit
    assert after_sue_worldunit.char_exists(rico_text)
    assert after_sue_worldunit.char_exists(carm_text) is False


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_char():
    # GIVEN
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_worldunit.add_charunit(rico_text)
    assert before_sue_worldunit.char_exists(rico_text)
    assert before_sue_worldunit.char_exists(carm_text) is False

    # WHEN
    category = "world_charunit"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_required_arg("char_id", carm_text)
    x_credor_weight = 55
    x_debtor_weight = 66
    x_atomunit.set_optional_arg("credor_weight", x_credor_weight)
    x_atomunit.set_optional_arg("debtor_weight", x_debtor_weight)
    sue_changeunit.set_atomunit(x_atomunit)
    print(f"{sue_changeunit.atomunits.keys()=}")
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    rico_charunit = after_sue_worldunit.get_char(rico_text)
    carm_charunit = after_sue_worldunit.get_char(carm_text)
    assert rico_charunit != None
    assert carm_charunit != None
    assert carm_charunit.credor_weight == x_credor_weight
    assert carm_charunit.debtor_weight == x_debtor_weight


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_update_char():
    # GIVEN
    sue_changeunit = changeunit_shop()
    sue_text = "Sue"

    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_worldunit.add_charunit(rico_text)
    assert before_sue_worldunit.get_char(rico_text).credor_weight == 1

    # WHEN
    category = "world_charunit"
    x_atomunit = atomunit_shop(category, atom_update())
    x_atomunit.set_required_arg("char_id", rico_text)
    rico_credor_weight = 55
    x_atomunit.set_optional_arg("credor_weight", rico_credor_weight)
    sue_changeunit.set_atomunit(x_atomunit)
    print(f"{sue_changeunit.atomunits.keys()=}")
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    rico_char = after_sue_worldunit.get_char(rico_text)
    assert rico_char.credor_weight == rico_credor_weight


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_charlink():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_worldunit.add_charunit(rico_text)
    before_sue_worldunit.add_charunit(carm_text)
    before_sue_worldunit.add_charunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(rico_text))
    run_beliefunit.set_charlink(charlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_charlink(charlink_shop(rico_text))
    fly_beliefunit.set_charlink(charlink_shop(carm_text))
    fly_beliefunit.set_charlink(charlink_shop(dizz_text))
    before_sue_worldunit.set_beliefunit(run_beliefunit)
    before_sue_worldunit.set_beliefunit(fly_beliefunit)
    assert len(before_sue_worldunit.get_beliefunit(run_text)._chars) == 2
    assert len(before_sue_worldunit.get_beliefunit(fly_text)._chars) == 3

    # WHEN
    rico_atomunit = atomunit_shop("world_char_belieflink", atom_delete())
    rico_atomunit.set_required_arg("belief_id", run_text)
    rico_atomunit.set_required_arg("char_id", rico_text)
    # print(f"{rico_atomunit=}")
    carm_atomunit = atomunit_shop("world_char_belieflink", atom_delete())
    carm_atomunit.set_required_arg("belief_id", fly_text)
    carm_atomunit.set_required_arg("char_id", carm_text)
    # print(f"{carm_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(rico_atomunit)
    sue_changeunit.set_atomunit(carm_atomunit)
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    assert len(after_sue_worldunit.get_beliefunit(fly_text)._chars) == 2
    assert len(after_sue_worldunit.get_beliefunit(run_text)._chars) == 1


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_charlink():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_worldunit.add_charunit(rico_text)
    before_sue_worldunit.add_charunit(carm_text)
    before_sue_worldunit.add_charunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(carm_text))
    before_sue_worldunit.set_beliefunit(run_beliefunit)
    assert len(before_sue_worldunit.get_beliefunit(run_text)._chars) == 1

    # WHEN
    rico_atomunit = atomunit_shop("world_char_belieflink", atom_insert())
    rico_atomunit.set_required_arg("belief_id", run_text)
    rico_atomunit.set_required_arg("char_id", rico_text)
    rico_run_credor_weight = 17
    rico_atomunit.set_optional_arg("credor_weight", rico_run_credor_weight)
    print(f"{rico_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(rico_atomunit)
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    assert len(after_sue_worldunit.get_beliefunit(run_text)._chars) == 2
    after_run_beliefunit = after_sue_worldunit.get_beliefunit(run_text)
    after_run_rico_charlink = after_run_beliefunit.get_charlink(rico_text)
    assert after_run_rico_charlink != None
    assert after_run_rico_charlink.credor_weight == rico_run_credor_weight


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_update_charlink():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_worldunit.add_charunit(rico_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    old_rico_run_credor_weight = 3
    run_beliefunit.set_charlink(charlink_shop(rico_text, old_rico_run_credor_weight))
    before_sue_worldunit.set_beliefunit(run_beliefunit)
    before_run_beliefunit = before_sue_worldunit.get_beliefunit(run_text)
    before_run_rico_charlink = before_run_beliefunit.get_charlink(rico_text)
    assert before_run_rico_charlink.credor_weight == old_rico_run_credor_weight
    assert before_run_rico_charlink.debtor_weight == 1

    # WHEN
    rico_atomunit = atomunit_shop("world_char_belieflink", atom_update())
    rico_atomunit.set_required_arg("belief_id", run_text)
    rico_atomunit.set_required_arg("char_id", rico_text)
    new_rico_run_credor_weight = 7
    new_rico_run_debtor_weight = 11
    rico_atomunit.set_optional_arg("credor_weight", new_rico_run_credor_weight)
    rico_atomunit.set_optional_arg("debtor_weight", new_rico_run_debtor_weight)
    print(f"{rico_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(rico_atomunit)
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    after_run_beliefunit = after_sue_worldunit.get_beliefunit(run_text)
    after_run_rico_charlink = after_run_beliefunit.get_charlink(rico_text)
    assert after_run_rico_charlink.credor_weight == new_rico_run_credor_weight
    assert after_run_rico_charlink.debtor_weight == new_rico_run_debtor_weight


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_ideaunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_worldunit.make_road(sports_road, disc_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_worldunit.add_idea(ideaunit_shop(disc_text), sports_road)
    assert before_sue_worldunit.idea_exists(ball_road)
    assert before_sue_worldunit.idea_exists(disc_road)

    # WHEN
    delete_disc_atomunit = atomunit_shop("world_ideaunit", atom_delete())
    delete_disc_atomunit.set_required_arg(
        "label", get_terminus_node(disc_road, before_sue_worldunit._road_delimiter)
    )
    print(f"{disc_road=}")
    delete_disc_atomunit.set_required_arg(
        "parent_road",
        get_parent_road(disc_road, before_sue_worldunit._road_delimiter),
    )
    print(f"{delete_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(delete_disc_atomunit)
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    assert after_sue_worldunit.idea_exists(ball_road)
    assert after_sue_worldunit.idea_exists(disc_road) is False


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_ideaunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_worldunit.make_road(sports_road, disc_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_worldunit.idea_exists(ball_road)
    assert before_sue_worldunit.idea_exists(disc_road) is False

    # WHEN
    # x_addin = 140
    # x_begin = 1000
    # x_close = 1700
    # x_denom = 17
    x_meld_strategy = "override"
    x_numeric_road = None
    # x_numor = 10
    x_pledge = True
    insert_disc_atomunit = atomunit_shop("world_ideaunit", atom_insert())
    insert_disc_atomunit.set_required_arg("label", disc_text)
    insert_disc_atomunit.set_required_arg("parent_road", sports_road)
    # insert_disc_atomunit.set_optional_arg("_addin", x_addin)
    # insert_disc_atomunit.set_optional_arg("_begin", x_begin)
    # insert_disc_atomunit.set_optional_arg("_close", x_close)
    # insert_disc_atomunit.set_optional_arg("_denom", x_denom)
    insert_disc_atomunit.set_optional_arg("_meld_strategy", x_meld_strategy)
    insert_disc_atomunit.set_optional_arg("_numeric_road", x_numeric_road)
    # insert_disc_atomunit.set_optional_arg("_numor", x_numor)
    insert_disc_atomunit.set_optional_arg("pledge", x_pledge)

    print(f"{insert_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(insert_disc_atomunit)
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    assert after_sue_worldunit.idea_exists(ball_road)
    assert after_sue_worldunit.idea_exists(disc_road)


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_update_ideaunit_SimpleAttributes():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_worldunit.get_idea_obj(ball_road)._begin is None
    assert before_sue_worldunit.get_idea_obj(ball_road)._close is None
    assert before_sue_worldunit.get_idea_obj(ball_road)._meld_strategy == "default"
    assert before_sue_worldunit.get_idea_obj(ball_road).pledge is False

    # WHEN
    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    x_meld_strategy = "override"
    # x_numor = 10
    x_pledge = True
    insert_disc_atomunit = atomunit_shop("world_ideaunit", atom_update())
    insert_disc_atomunit.set_required_arg("label", ball_text)
    insert_disc_atomunit.set_required_arg("parent_road", sports_road)
    # insert_disc_atomunit.set_optional_arg("_addin", x_addin)
    insert_disc_atomunit.set_optional_arg("_begin", x_begin)
    insert_disc_atomunit.set_optional_arg("_close", x_close)
    # insert_disc_atomunit.set_optional_arg("_denom", x_denom)
    insert_disc_atomunit.set_optional_arg("_meld_strategy", x_meld_strategy)
    # insert_disc_atomunit.set_optional_arg("_numor", x_numor)
    insert_disc_atomunit.set_optional_arg("pledge", x_pledge)

    print(f"{insert_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(insert_disc_atomunit)
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    assert after_sue_worldunit.get_idea_obj(ball_road)._begin == x_begin
    assert after_sue_worldunit.get_idea_obj(ball_road)._close == x_close
    assert after_sue_worldunit.get_idea_obj(ball_road)._meld_strategy == x_meld_strategy
    assert after_sue_worldunit.get_idea_obj(ball_road).pledge


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_idea_fiscallink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_au.add_charunit(rico_text)
    before_sue_au.add_charunit(carm_text)
    before_sue_au.add_charunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(rico_text))
    run_beliefunit.set_charlink(charlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_charlink(charlink_shop(rico_text))
    fly_beliefunit.set_charlink(charlink_shop(carm_text))
    fly_beliefunit.set_charlink(charlink_shop(dizz_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    before_sue_au.set_beliefunit(fly_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.add_idea(ideaunit_shop(disc_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, fiscallink=fiscallink_shop(run_text))
    before_sue_au.edit_idea_attr(ball_road, fiscallink=fiscallink_shop(fly_text))
    before_sue_au.edit_idea_attr(disc_road, fiscallink=fiscallink_shop(run_text))
    before_sue_au.edit_idea_attr(disc_road, fiscallink=fiscallink_shop(fly_text))
    assert len(before_sue_au.get_idea_obj(ball_road)._fiscallinks) == 2
    assert len(before_sue_au.get_idea_obj(disc_road)._fiscallinks) == 2

    # WHEN
    delete_disc_atomunit = atomunit_shop("world_idea_fiscallink", atom_delete())
    delete_disc_atomunit.set_required_arg("road", disc_road)
    delete_disc_atomunit.set_required_arg("belief_id", fly_text)
    print(f"{delete_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(delete_disc_atomunit)
    after_sue_worldunit = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    assert len(after_sue_worldunit.get_idea_obj(ball_road)._fiscallinks) == 2
    assert len(after_sue_worldunit.get_idea_obj(disc_road)._fiscallinks) == 1


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_update_idea_fiscallink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_charunit(rico_text)
    before_sue_au.add_charunit(carm_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(rico_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, fiscallink=fiscallink_shop(run_text))
    run_fiscallink = before_sue_au.get_idea_obj(ball_road)._fiscallinks.get(run_text)
    assert run_fiscallink.credor_weight == 1
    assert run_fiscallink.debtor_weight == 1

    # WHEN
    x_credor_weight = 55
    x_debtor_weight = 66
    update_disc_atomunit = atomunit_shop("world_idea_fiscallink", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("belief_id", run_text)
    update_disc_atomunit.set_optional_arg("credor_weight", x_credor_weight)
    update_disc_atomunit.set_optional_arg("debtor_weight", x_debtor_weight)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    run_fiscallink = after_sue_au.get_idea_obj(ball_road)._fiscallinks.get(run_text)
    print(f"{run_fiscallink.credor_weight=}")
    assert run_fiscallink.credor_weight == x_credor_weight
    assert run_fiscallink.debtor_weight == x_debtor_weight


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_idea_fiscallink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_charunit(rico_text)
    before_sue_au.add_charunit(carm_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(rico_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._fiscallinks.get(run_text) is None

    # WHEN
    x_credor_weight = 55
    x_debtor_weight = 66
    update_disc_atomunit = atomunit_shop("world_idea_fiscallink", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("belief_id", run_text)
    update_disc_atomunit.set_optional_arg("credor_weight", x_credor_weight)
    update_disc_atomunit.set_optional_arg("debtor_weight", x_debtor_weight)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._fiscallinks.get(run_text) != None


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_idea_factunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_factunit", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg("pick", broken_road)
    update_disc_atomunit.set_optional_arg("open", broken_open)
    update_disc_atomunit.set_optional_arg("nigh", broken_nigh)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits != {}
    assert after_ball_idea._factunits.get(knee_road) != None
    assert after_ball_idea._factunits.get(knee_road).base == knee_road
    assert after_ball_idea._factunits.get(knee_road).pick == broken_road
    assert after_ball_idea._factunits.get(knee_road).open == broken_open
    assert after_ball_idea._factunits.get(knee_road).nigh == broken_nigh


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_idea_factunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_factunit", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits == {}


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_update_idea_factunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_factunit", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg("pick", medical_road)
    update_disc_atomunit.set_optional_arg("open", medical_open)
    update_disc_atomunit.set_optional_arg("nigh", medical_nigh)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits != {}
    assert after_ball_idea._factunits.get(knee_road) != None
    assert after_ball_idea._factunits.get(knee_road).pick == medical_road
    assert after_ball_idea._factunits.get(knee_road).open == medical_open
    assert after_ball_idea._factunits.get(knee_road).nigh == medical_nigh


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_update_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_reason_premiseunit", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_required_arg("need", broken_road)
    update_disc_atomunit.set_optional_arg("open", broken_open)
    update_disc_atomunit.set_optional_arg("nigh", broken_nigh)
    update_disc_atomunit.set_optional_arg("divisor", broken_divisor)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    after_broken_premiseunit = after_knee_reasonunit.get_premise(broken_road)
    assert after_broken_premiseunit.need == broken_road
    assert after_broken_premiseunit.open == broken_open
    assert after_broken_premiseunit.nigh == broken_nigh
    assert after_broken_premiseunit.divisor == broken_divisor


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_reason_premiseunit", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_required_arg("need", medical_road)
    update_disc_atomunit.set_optional_arg("open", medical_open)
    update_disc_atomunit.set_optional_arg("nigh", medical_nigh)
    update_disc_atomunit.set_optional_arg("divisor", medical_divisor)
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_road)
    assert after_medical_premiseunit != None
    assert after_medical_premiseunit.need == medical_road
    assert after_medical_premiseunit.open == medical_open
    assert after_medical_premiseunit.nigh == medical_nigh
    assert after_medical_premiseunit.divisor == medical_divisor


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_reason_premiseunit", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_required_arg("need", medical_road)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit.get_premise(broken_road) != None
    assert after_knee_reasonunit.get_premise(medical_road) is None


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_reasonunit", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg(
        "base_idea_active_requisite", medical_base_idea_active_requisite
    )
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert (
        after_knee_reasonunit.base_idea_active_requisite
        == medical_base_idea_active_requisite
    )


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_update_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_reasonunit", atom_update())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    update_disc_atomunit.set_optional_arg(
        "base_idea_active_requisite", after_medical_base_idea_active_requisite
    )
    # print(f"{update_disc_atomunit=}")
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert (
        after_knee_reasonunit.base_idea_active_requisite
        == after_medical_base_idea_active_requisite
    )


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
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
    update_disc_atomunit = atomunit_shop("world_idea_reasonunit", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("base", knee_road)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea.get_reasonunit(knee_road) is None


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_insert_idea_allyhold():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_au.add_charunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_ideaunit._cultureunit._allyholds == set()

    # WHEN
    update_disc_atomunit = atomunit_shop("world_idea_allyhold", atom_insert())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("belief_id", rico_text)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._cultureunit._allyholds != {}
    assert after_ball_ideaunit._cultureunit.get_allyhold(rico_text) != None


def test_ChangeUnit_get_edited_world_ReturnsCorrectObj_WorldUnit_delete_idea_allyhold():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_au.add_charunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    before_ball_ideaunit._cultureunit.set_allyhold(rico_text)
    assert before_ball_ideaunit._cultureunit._allyholds != {}
    assert before_ball_ideaunit._cultureunit.get_allyhold(rico_text) != None

    # WHEN
    update_disc_atomunit = atomunit_shop("world_idea_allyhold", atom_delete())
    update_disc_atomunit.set_required_arg("road", ball_road)
    update_disc_atomunit.set_required_arg("belief_id", rico_text)
    sue_changeunit = changeunit_shop()
    sue_changeunit.set_atomunit(update_disc_atomunit)
    print(f"{before_sue_au.get_idea_obj(ball_road)._cultureunit=}")
    after_sue_au = sue_changeunit.get_edited_world(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._cultureunit._allyholds == set()


def test_ChangeUnit_get_changeunit_example1_ContainsAtomUnits():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_worldunit.add_charunit(rico_text)
    before_sue_worldunit.add_charunit(carm_text)
    before_sue_worldunit.add_charunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(rico_text))
    run_beliefunit.set_charlink(charlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_charlink(charlink_shop(rico_text))
    fly_beliefunit.set_charlink(charlink_shop(dizz_text))
    before_sue_worldunit.set_beliefunit(run_beliefunit)
    before_sue_worldunit.set_beliefunit(fly_beliefunit)
    assert before_sue_worldunit._weight != 55
    assert before_sue_worldunit._max_tree_traverse != 66
    assert before_sue_worldunit._char_credor_pool != 77
    assert before_sue_worldunit._char_debtor_pool != 88
    assert before_sue_worldunit._meld_strategy != "override"
    assert before_sue_worldunit.char_exists(rico_text)
    assert before_sue_worldunit.char_exists(carm_text)
    assert before_sue_worldunit.get_beliefunit(run_text) != None
    assert before_sue_worldunit.get_beliefunit(fly_text) != None

    # WHEN
    ex1_changeunit = get_changeunit_example1()
    after_sue_worldunit = ex1_changeunit.get_edited_world(before_sue_worldunit)

    # THEN
    assert after_sue_worldunit._weight == 55
    assert after_sue_worldunit._max_tree_traverse == 66
    assert after_sue_worldunit._char_credor_pool == 77
    assert after_sue_worldunit._char_debtor_pool == 88
    assert after_sue_worldunit._meld_strategy == "override"
    assert after_sue_worldunit.char_exists(rico_text)
    assert after_sue_worldunit.char_exists(carm_text) is False
