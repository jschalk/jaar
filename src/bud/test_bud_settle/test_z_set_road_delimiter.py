from src.bud.reason_idea import reasonunit_shop, factunit_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises
from src._road.road import create_road


def test_bud_set_road_delimiter_RaisesErrorIfNew_delimiter_IsAnIdea_label():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    print(f"{zia_bud._max_tree_traverse=}")
    casa_text = "casa"
    casa_road = zia_bud.make_l1_road(casa_text)
    zia_bud.set_l1_idea(ideaunit_shop(casa_text))
    slash_text = "/"
    casa_text = f"casa cook{slash_text}clean"
    zia_bud.set_idea(ideaunit_shop(casa_text), parent_road=casa_road)

    # WHEN / THEN
    casa_road = zia_bud.make_road(casa_road, casa_text)
    print(f"{casa_road=}")
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_road_delimiter(slash_text)
    assert (
        str(excinfo.value)
        == f"Cannot modify delimiter to '{slash_text}' because it already exists an idea label '{casa_road}'"
    )


def test_bud_set_road_delimiter_CorrectlyModifies_parent_road():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_text = "casa"
    zia_bud.set_l1_idea(ideaunit_shop(casa_text))
    semicolon_casa_road = zia_bud.make_l1_road(casa_text)
    cook_text = "cook"
    zia_bud.set_idea(ideaunit_shop(cook_text), semicolon_casa_road)
    semicolon_cook_road = zia_bud.make_road(semicolon_casa_road, cook_text)
    cook_idea = zia_bud.get_idea_obj(semicolon_cook_road)
    semicolon_text = ";"
    assert zia_bud._road_delimiter == semicolon_text
    semicolon_cook_road = zia_bud.make_road(semicolon_casa_road, cook_text)
    # print(f"{zia_bud._real_id=} {zia_bud._idearoot._label=} {casa_road=}")
    # print(f"{cook_idea._parent_road=} {cook_idea._label=}")
    # semicolon_casa_idea = zia_bud.get_idea_obj(semicolon_casa_road)
    # print(f"{semicolon_casa_idea._parent_road=} {semicolon_casa_idea._label=}")
    assert cook_idea.get_road() == semicolon_cook_road

    # WHEN
    slash_text = "/"
    zia_bud.set_road_delimiter(slash_text)

    # THEN
    assert cook_idea.get_road() != semicolon_cook_road
    zia_real_id = zia_bud._real_id
    slash_casa_road = create_road(zia_real_id, casa_text, delimiter=slash_text)
    slash_cook_road = create_road(slash_casa_road, cook_text, delimiter=slash_text)
    assert cook_idea.get_road() == slash_cook_road


def test_bud_set_road_delimiter_CorrectlyModifiesReasonUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_text = "casa"
    zia_bud.set_l1_idea(ideaunit_shop(casa_text))
    time_text = "time"
    semicolon_time_road = zia_bud.make_l1_road(time_text)
    _8am_text = "8am"
    semicolon_8am_road = zia_bud.make_road(semicolon_time_road, _8am_text)

    semicolon_time_reasonunit = reasonunit_shop(base=semicolon_time_road)
    semicolon_time_reasonunit.set_premise(semicolon_8am_road)

    semicolon_casa_road = zia_bud.make_l1_road(casa_text)
    zia_bud.edit_idea_attr(road=semicolon_casa_road, reason=semicolon_time_reasonunit)
    casa_idea = zia_bud.get_idea_obj(semicolon_casa_road)
    assert casa_idea._reasonunits.get(semicolon_time_road) is not None
    gen_time_reasonunit = casa_idea._reasonunits.get(semicolon_time_road)
    assert gen_time_reasonunit.premises.get(semicolon_8am_road) is not None

    # WHEN
    slash_text = "/"
    zia_bud.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = zia_bud.make_l1_road(time_text)
    slash_8am_road = zia_bud.make_road(slash_time_road, _8am_text)
    slash_casa_road = zia_bud.make_l1_road(casa_text)
    casa_idea = zia_bud.get_idea_obj(slash_casa_road)
    slash_time_road = zia_bud.make_l1_road(time_text)
    slash_8am_road = zia_bud.make_road(slash_time_road, _8am_text)
    assert casa_idea._reasonunits.get(slash_time_road) is not None
    gen_time_reasonunit = casa_idea._reasonunits.get(slash_time_road)
    assert gen_time_reasonunit.premises.get(slash_8am_road) is not None

    assert casa_idea._reasonunits.get(semicolon_time_road) is None
    assert gen_time_reasonunit.premises.get(semicolon_8am_road) is None


def test_bud_set_road_delimiter_CorrectlyModifiesFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_text = "casa"
    zia_bud.set_l1_idea(ideaunit_shop(casa_text))
    time_text = "time"
    semicolon_time_road = zia_bud.make_l1_road(time_text)
    _8am_text = "8am"
    semicolon_8am_road = zia_bud.make_road(semicolon_time_road, _8am_text)
    semicolon_time_factunit = factunit_shop(semicolon_time_road, semicolon_8am_road)

    semicolon_casa_road = zia_bud.make_l1_road(casa_text)
    zia_bud.edit_idea_attr(semicolon_casa_road, factunit=semicolon_time_factunit)
    casa_idea = zia_bud.get_idea_obj(semicolon_casa_road)
    print(f"{casa_idea._factunits=} {semicolon_time_road=}")
    assert casa_idea._factunits.get(semicolon_time_road) is not None
    gen_time_factunit = casa_idea._factunits.get(semicolon_time_road)

    # WHEN
    slash_text = "/"
    zia_bud.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = zia_bud.make_l1_road(time_text)
    slash_casa_road = zia_bud.make_l1_road(casa_text)
    casa_idea = zia_bud.get_idea_obj(slash_casa_road)
    slash_time_road = zia_bud.make_l1_road(time_text)
    slash_8am_road = zia_bud.make_road(slash_time_road, _8am_text)
    assert casa_idea._factunits.get(slash_time_road) is not None
    gen_time_factunit = casa_idea._factunits.get(slash_time_road)
    assert gen_time_factunit.base is not None
    assert gen_time_factunit.base == slash_time_road
    assert gen_time_factunit.pick is not None
    assert gen_time_factunit.pick == slash_8am_road

    assert casa_idea._factunits.get(semicolon_time_road) is None


def test_bud_set_road_delimiter_CorrectlyModifies_range_pushs():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_text = "casa"
    zia_bud.set_l1_idea(ideaunit_shop(casa_text))
    semicolon_casa_road = zia_bud.make_l1_road(casa_text)
    cook_text = "cook"
    zia_bud.set_idea(ideaunit_shop(cook_text), parent_road=semicolon_casa_road)
    semicolon_cook_road = zia_bud.make_road(semicolon_casa_road, cook_text)

    # range_push
    heat_text = "heat numbers"
    zia_bud.set_l1_idea(ideaunit_shop(heat_text, _begin=0, _close=6))
    semicolon_heat_road = zia_bud.make_l1_road(heat_text)
    zia_bud.edit_idea_attr(semicolon_cook_road, range_push=semicolon_heat_road)

    cook_idea = zia_bud.get_idea_obj(semicolon_cook_road)
    assert semicolon_heat_road in cook_idea._range_pushs

    # WHEN
    slash_text = "/"
    zia_bud.set_road_delimiter(slash_text)

    # THEN
    slash_heat_road = zia_bud.make_l1_road(heat_text)
    assert semicolon_heat_road not in cook_idea._range_pushs
    assert slash_heat_road in cook_idea._range_pushs
