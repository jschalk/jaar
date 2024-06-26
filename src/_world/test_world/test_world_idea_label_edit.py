from src._world.world import worldunit_shop
from src._world.idea import ideaunit_shop
from src._world.examples.example_worlds import (
    get_world_with_4_levels_and_2reasons_2facts,
)
from pytest import raises as pytest_raises
from src._world.reason_idea import reasonunit_shop, factunit_shop
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
)


def test_WorldUnit_edit_idea_label_FailsWhenIdeaDoesNotExist():
    # GIVEN
    tim_world = worldunit_shop("Tim")

    casa_text = "casa"
    casa_road = tim_world.make_l1_road(casa_text)
    swim_text = "swim"
    tim_world.add_l1_idea(ideaunit_shop(casa_text))
    tim_world.add_idea(ideaunit_shop(swim_text), parent_road=casa_road)

    # WHEN / THEN
    no_idea_road = tim_world.make_l1_road("bees")
    with pytest_raises(Exception) as excinfo:
        tim_world.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert str(excinfo.value) == f"Idea old_road='{no_idea_road}' does not exist"


def test_WorldUnit_edit_idea_label_RaisesErrorForLevel0IdeaWhen_real_id_isNone():
    # GIVEN
    tim_text = "Tim"
    tim_world = worldunit_shop(_owner_id=tim_text)

    casa_text = "casa"
    casa_road = tim_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = tim_world.make_road(casa_road, swim_text)
    tim_world.add_l1_idea(ideaunit_shop(casa_text))
    tim_world.add_idea(ideaunit_shop(swim_text), parent_road=casa_road)
    assert tim_world._owner_id == tim_text
    assert tim_world._idearoot._label == tim_world._real_id
    casa_idea = tim_world.get_idea_obj(casa_road)
    assert casa_idea._parent_road == tim_world._real_id
    swim_idea = tim_world.get_idea_obj(swim_road)
    assert swim_idea._parent_road == casa_road

    # WHEN
    moon_text = "moon"
    tim_world.edit_idea_label(old_road=tim_world._real_id, new_label=moon_text)

    # THEN
    # with pytest_raises(Exception) as excinfo:
    #     moon_text = "moon"
    #     tim_world.edit_idea_label(old_road=tim_world._real_id, new_label=moon_text)
    # assert (
    #     str(excinfo.value)
    #     == f"Cannot set idearoot to string othher than '{tim_world._real_id}'"
    # )

    assert tim_world._idearoot._label != moon_text
    assert tim_world._idearoot._label == tim_world._real_id


def test_WorldUnit_edit_idea_label_RaisesErrorForLevel0When_real_id_IsDifferent():
    # GIVEN
    tim_text = "Tim"
    tim_world = worldunit_shop(_owner_id=tim_text)
    casa_text = "casa"
    casa_road = tim_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = tim_world.make_road(casa_road, swim_text)
    tim_world.add_l1_idea(ideaunit_shop(casa_text))
    tim_world.add_idea(ideaunit_shop(swim_text), parent_road=casa_road)
    sun_text = "sun"
    tim_world._real_id = sun_text
    tim_world._idearoot._world_real_id = sun_text
    assert tim_world._owner_id == tim_text
    assert tim_world._real_id == sun_text
    assert tim_world._idearoot._world_real_id == sun_text
    assert tim_world._idearoot._label == root_label()
    casa_idea = tim_world.get_idea_obj(casa_road)
    assert casa_idea._parent_road == root_label()
    swim_idea = tim_world.get_idea_obj(swim_road)
    assert swim_idea._parent_road == casa_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        tim_world.edit_idea_label(old_road=root_label(), new_label=moon_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{sun_text}'"
    )


def test_world_set_real_id_CorrectlySetsAttr():
    # GIVEN
    tim_text = "Tim"
    tim_world = worldunit_shop(_owner_id=tim_text)
    casa_text = "casa"
    old_casa_road = tim_world.make_l1_road(casa_text)
    swim_text = "swim"
    old_swim_road = tim_world.make_road(old_casa_road, swim_text)
    tim_world.add_l1_idea(ideaunit_shop(casa_text))
    tim_world.add_idea(ideaunit_shop(swim_text), parent_road=old_casa_road)
    assert tim_world._owner_id == tim_text
    assert tim_world._idearoot._label == tim_world._real_id
    casa_idea = tim_world.get_idea_obj(old_casa_road)
    assert casa_idea._parent_road == tim_world._real_id
    swim_idea = tim_world.get_idea_obj(old_swim_road)
    assert swim_idea._parent_road == old_casa_road
    assert tim_world._real_id == tim_world._real_id

    # WHEN
    real_id_text = "Sun"
    tim_world.set_real_id(real_id=real_id_text)

    # THEN
    new_casa_road = tim_world.make_l1_road(casa_text)
    swim_text = "swim"
    new_swim_road = tim_world.make_road(new_casa_road, swim_text)
    assert tim_world._real_id == real_id_text
    assert tim_world._idearoot._label == real_id_text
    casa_idea = tim_world.get_idea_obj(new_casa_road)
    assert casa_idea._parent_road == real_id_text
    swim_idea = tim_world.get_idea_obj(new_swim_road)
    assert swim_idea._parent_road == new_casa_road


def test_WorldUnit_find_replace_road_CorrectlyModifies_kids_Scenario1():
    # GIVEN Idea with kids that will be different
    tim_text = "Tim"
    tim_world = worldunit_shop(tim_text)

    old_casa_text = "casa"
    old_casa_road = tim_world.make_l1_road(old_casa_text)
    bloomers_text = "bloomers"
    old_bloomers_road = tim_world.make_road(old_casa_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = tim_world.make_road(old_bloomers_road, roses_text)
    red_text = "red"
    old_red_road = tim_world.make_road(old_roses_road, red_text)

    tim_world.add_l1_idea(ideaunit_shop(old_casa_text))
    tim_world.add_idea(ideaunit_shop(bloomers_text), parent_road=old_casa_road)
    tim_world.add_idea(ideaunit_shop(roses_text), parent_road=old_bloomers_road)
    tim_world.add_idea(ideaunit_shop(red_text), parent_road=old_roses_road)
    r_idea_roses = tim_world.get_idea_obj(old_roses_road)
    r_idea_bloomers = tim_world.get_idea_obj(old_bloomers_road)

    assert r_idea_bloomers._kids.get(roses_text) != None
    assert r_idea_roses._parent_road == old_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    assert r_idea_red._parent_road == old_roses_road

    # WHEN
    new_casa_text = "globe"
    new_casa_road = tim_world.make_l1_road(new_casa_text)
    tim_world.edit_idea_label(old_road=old_casa_road, new_label=new_casa_text)

    # THEN
    assert tim_world._idearoot._kids.get(new_casa_text) != None
    assert tim_world._idearoot._kids.get(old_casa_text) is None

    assert r_idea_bloomers._parent_road == new_casa_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = tim_world.make_road(new_casa_road, bloomers_text)
    assert r_idea_roses._parent_road == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = tim_world.make_road(new_bloomers_road, roses_text)
    assert r_idea_red._parent_road == new_roses_road


def test_world_edit_idea_label_Modifies_factunits():
    # GIVEN world with factunits that will be different
    tim_text = "Tim"
    tim_world = worldunit_shop(tim_text)

    casa_text = "casa"
    casa_road = tim_world.make_l1_road(casa_text)
    bloomers_text = "bloomers"
    bloomers_road = tim_world.make_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = tim_world.make_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = tim_world.make_l1_road(old_water_text)
    rain_text = "rain"
    old_rain_road = tim_world.make_road(old_water_road, rain_text)

    tim_world.add_l1_idea(ideaunit_shop(casa_text))
    tim_world.add_idea(ideaunit_shop(roses_text), parent_road=bloomers_road)
    tim_world.add_idea(ideaunit_shop(rain_text), parent_road=old_water_road)
    tim_world.set_fact(base=old_water_road, pick=old_rain_road)

    idea_x = tim_world.get_idea_obj(roses_road)
    assert tim_world._idearoot._factunits[old_water_road] != None
    old_water_rain_factunit = tim_world._idearoot._factunits[old_water_road]
    assert old_water_rain_factunit.base == old_water_road
    assert old_water_rain_factunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = tim_world.make_l1_road(new_water_text)
    tim_world.add_l1_idea(ideaunit_shop(new_water_text))
    assert tim_world._idearoot._factunits.get(new_water_road) is None
    tim_world.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert tim_world._idearoot._factunits.get(old_water_road) is None
    assert tim_world._idearoot._factunits.get(new_water_road) != None
    new_water_rain_factunit = tim_world._idearoot._factunits[new_water_road]
    assert new_water_rain_factunit.base == new_water_road
    new_rain_road = tim_world.make_road(new_water_road, rain_text)
    assert new_water_rain_factunit.pick == new_rain_road

    assert tim_world._idearoot._factunits.get(new_water_road)
    factunit_obj = tim_world._idearoot._factunits.get(new_water_road)
    # for factunit_key, factunit_obj in tim_world._idearoot._factunits.items():
    #     assert factunit_key == new_water_road
    assert factunit_obj.base == new_water_road
    assert factunit_obj.pick == new_rain_road


def test_world_edit_idea_label_Modifies_idearoot_range_source_road():
    # GIVEN this should never happen but best be thorough
    tim_world = worldunit_shop("Tim")
    old_casa_text = "casa"
    old_casa_road = tim_world.make_l1_road(old_casa_text)
    tim_world.add_l1_idea(ideaunit_shop(old_casa_text))
    tim_world.edit_idea_attr(tim_world._real_id, range_source_road=old_casa_road)
    assert tim_world._idearoot._range_source_road == old_casa_road

    # WHEN
    new_casa_text = "globe"
    tim_world.edit_idea_label(old_road=old_casa_road, new_label=new_casa_text)

    # THEN
    new_casa_road = tim_world.make_l1_road(new_casa_text)
    assert tim_world._idearoot._range_source_road == new_casa_road


def test_world_edit_idea_label_ModifiesIdeaUnitN_range_source_road():
    bob_world = worldunit_shop("Bob")
    casa_text = "casa"
    casa_road = bob_world.make_l1_road(casa_text)
    old_water_text = "water"
    old_water_road = bob_world.make_road(casa_road, old_water_text)
    rain_text = "rain"
    old_rain_road = bob_world.make_road(old_water_road, rain_text)
    mood_text = "mood"
    mood_road = bob_world.make_l1_road(mood_text)
    bob_world.add_l1_idea(ideaunit_shop(casa_text))
    bob_world.add_idea(ideaunit_shop(old_water_text), parent_road=casa_road)
    bob_world.add_idea(ideaunit_shop(rain_text), parent_road=old_water_road)
    bob_world.add_l1_idea(ideaunit_shop(mood_text))

    bob_world.edit_idea_attr(road=mood_road, range_source_road=old_rain_road)
    mood_idea = bob_world.get_idea_obj(mood_road)
    assert mood_idea._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = bob_world.make_road(casa_road, new_water_text)
    new_rain_road = bob_world.make_road(new_water_road, rain_text)
    bob_world.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    # for idea_x in bob_world._idearoot._kids.values():
    #     print(f"{idea_x._parent_road=} {idea_x._label=}")
    #     for idea_y in idea_x._kids.values():
    #         print(f"{idea_y._parent_road=} {idea_y._label=}")
    #         for idea_z in idea_y._kids.values():
    #             print(f"{idea_z._parent_road=} {idea_z._label=}")
    assert old_rain_road != new_rain_road
    assert mood_idea._range_source_road == new_rain_road


def test_world_edit_idea_label_ModifiesIdeaReasonUnitsScenario1():
    # GIVEN
    sue_world = get_world_with_4_levels_and_2reasons_2facts()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_world.make_l1_road(old_weekday_text)
    wednesday_text = "Wednesday"
    old_wednesday_road = sue_world.make_road(old_weekday_road, wednesday_text)
    casa_idea = sue_world.get_idea_obj(sue_world.make_l1_road("casa"))
    # casa_wk_reason = reasonunit_shop(weekday, premises={wed_premise.need: wed_premise})
    # nation_reason = reasonunit_shop(nationstate, premises={usa_premise.need: usa_premise})
    assert len(casa_idea._reasonunits) == 2
    assert casa_idea._reasonunits.get(old_weekday_road) != None
    wednesday_idea = sue_world.get_idea_obj(old_weekday_road)
    casa_weekday_reason = casa_idea._reasonunits.get(old_weekday_road)
    assert casa_weekday_reason.premises.get(old_wednesday_road) != None
    assert (
        casa_weekday_reason.premises.get(old_wednesday_road).need == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = sue_world.make_l1_road(new_weekday_text)
    new_wednesday_road = sue_world.make_road(new_weekday_road, wednesday_text)
    assert casa_idea._reasonunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, reason_x in casa_idea._reasonunits.items():
    #     print(f"Before {key_x=} {reason_x.base=}")
    print(f"BEFORE {wednesday_idea._label=}")
    print(f"BEFORE {wednesday_idea._parent_road=}")
    sue_world.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    # for key_x, reason_x in casa_idea._reasonunits.items():
    #     print(f"AFTER {key_x=} {reason_x.base=}")
    print(f"AFTER {wednesday_idea._label=}")
    print(f"AFTER {wednesday_idea._parent_road=}")

    # THEN
    assert casa_idea._reasonunits.get(new_weekday_road) != None
    assert casa_idea._reasonunits.get(old_weekday_road) is None
    casa_weekday_reason = casa_idea._reasonunits.get(new_weekday_road)
    assert casa_weekday_reason.premises.get(new_wednesday_road) != None
    assert (
        casa_weekday_reason.premises.get(new_wednesday_road).need == new_wednesday_road
    )
    assert len(casa_idea._reasonunits) == 2


def test_world_set_owner_id_CorrectlyModifiesBoth():
    # GIVEN
    sue_world = get_world_with_4_levels_and_2reasons_2facts()
    assert sue_world._owner_id == "Sue"
    assert sue_world._idearoot._label == sue_world._real_id
    # mid_label1 = "Tim"
    # sue_world.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert sue_world._owner_id == old_label
    # assert sue_world._idearoot._label == mid_label1

    # WHEN
    bob_text = "Bob"
    sue_world.set_owner_id(new_owner_id=bob_text)

    # THEN
    assert sue_world._owner_id == bob_text
    assert sue_world._idearoot._label == sue_world._real_id


def test_world_edit_idea_label_RaisesErrorIfdelimiterIsInLabel():
    # GIVEN
    sue_world = get_world_with_4_levels_and_2reasons_2facts()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_world.make_l1_road(old_weekday_text)

    # WHEN / THEN
    new_weekday_text = "days, of week"
    with pytest_raises(Exception) as excinfo:
        sue_world.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_weekday_road}' because new_label {new_weekday_text} contains delimiter {sue_world._road_delimiter}"
    )


def test_world_set_road_delimiter_RaisesErrorIfNew_delimiter_IsAnIdea_label():
    # GIVEN
    luca_world = worldunit_shop("Luca", "Texas")
    print(f"{luca_world._max_tree_traverse=}")
    casa_text = "casa"
    casa_road = luca_world.make_l1_road(casa_text)
    luca_world.add_l1_idea(ideaunit_shop(casa_text))
    slash_text = "/"
    casa_text = f"casa cook{slash_text}clean"
    luca_world.add_idea(ideaunit_shop(casa_text), parent_road=casa_road)

    # WHEN / THEN
    casa_road = luca_world.make_road(casa_road, casa_text)
    print(f"{casa_road=}")
    with pytest_raises(Exception) as excinfo:
        luca_world.set_road_delimiter(slash_text)
    assert (
        str(excinfo.value)
        == f"Cannot modify delimiter to '{slash_text}' because it already exists an idea label '{casa_road}'"
    )


def test_world_set_road_delimiter_CorrectlyModifies_parent_road():
    # GIVEN
    luca_world = worldunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_world.add_l1_idea(ideaunit_shop(casa_text))
    comma_casa_road = luca_world.make_l1_road(casa_text)
    cook_text = "cook"
    luca_world.add_idea(ideaunit_shop(cook_text), parent_road=comma_casa_road)
    comma_cook_road = luca_world.make_road(comma_casa_road, cook_text)
    cook_idea = luca_world.get_idea_obj(comma_cook_road)
    comma_text = ","
    assert luca_world._road_delimiter == comma_text
    comma_cook_road = luca_world.make_road(comma_casa_road, cook_text)
    # print(f"{luca_world._real_id=} {luca_world._idearoot._label=} {casa_road=}")
    # print(f"{cook_idea._parent_road=} {cook_idea._label=}")
    # comma_casa_idea = luca_world.get_idea_obj(comma_casa_road)
    # print(f"{comma_casa_idea._parent_road=} {comma_casa_idea._label=}")
    assert cook_idea.get_road() == comma_cook_road

    # WHEN
    slash_text = "/"
    luca_world.set_road_delimiter(slash_text)

    # THEN
    assert cook_idea.get_road() != comma_cook_road
    luca_real_id = luca_world._real_id
    slash_casa_road = create_road(luca_real_id, casa_text, delimiter=slash_text)
    slash_cook_road = create_road(slash_casa_road, cook_text, delimiter=slash_text)
    assert cook_idea.get_road() == slash_cook_road


def test_world_set_road_delimiter_CorrectlyModifiesReasonUnit():
    # GIVEN
    luca_world = worldunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_world.add_l1_idea(ideaunit_shop(casa_text))
    time_text = "time"
    comma_time_road = luca_world.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_world.make_road(comma_time_road, _8am_text)

    comma_time_reasonunit = reasonunit_shop(base=comma_time_road)
    comma_time_reasonunit.set_premise(comma_8am_road)

    comma_casa_road = luca_world.make_l1_road(casa_text)
    luca_world.edit_idea_attr(road=comma_casa_road, reason=comma_time_reasonunit)
    casa_idea = luca_world.get_idea_obj(comma_casa_road)
    assert casa_idea._reasonunits.get(comma_time_road) != None
    gen_time_reasonunit = casa_idea._reasonunits.get(comma_time_road)
    assert gen_time_reasonunit.premises.get(comma_8am_road) != None

    # WHEN
    slash_text = "/"
    luca_world.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = luca_world.make_l1_road(time_text)
    slash_8am_road = luca_world.make_road(slash_time_road, _8am_text)
    slash_casa_road = luca_world.make_l1_road(casa_text)
    casa_idea = luca_world.get_idea_obj(slash_casa_road)
    slash_time_road = luca_world.make_l1_road(time_text)
    slash_8am_road = luca_world.make_road(slash_time_road, _8am_text)
    assert casa_idea._reasonunits.get(slash_time_road) != None
    gen_time_reasonunit = casa_idea._reasonunits.get(slash_time_road)
    assert gen_time_reasonunit.premises.get(slash_8am_road) != None

    assert casa_idea._reasonunits.get(comma_time_road) is None
    assert gen_time_reasonunit.premises.get(comma_8am_road) is None


def test_world_set_road_delimiter_CorrectlyModifiesFactUnit():
    # GIVEN
    luca_world = worldunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_world.add_l1_idea(ideaunit_shop(casa_text))
    time_text = "time"
    comma_time_road = luca_world.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_world.make_road(comma_time_road, _8am_text)
    comma_time_factunit = factunit_shop(comma_time_road, comma_8am_road)

    comma_casa_road = luca_world.make_l1_road(casa_text)
    luca_world.edit_idea_attr(comma_casa_road, factunit=comma_time_factunit)
    casa_idea = luca_world.get_idea_obj(comma_casa_road)
    print(f"{casa_idea._factunits=} {comma_time_road=}")
    assert casa_idea._factunits.get(comma_time_road) != None
    gen_time_factunit = casa_idea._factunits.get(comma_time_road)

    # WHEN
    slash_text = "/"
    luca_world.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = luca_world.make_l1_road(time_text)
    slash_casa_road = luca_world.make_l1_road(casa_text)
    casa_idea = luca_world.get_idea_obj(slash_casa_road)
    slash_time_road = luca_world.make_l1_road(time_text)
    slash_8am_road = luca_world.make_road(slash_time_road, _8am_text)
    assert casa_idea._factunits.get(slash_time_road) != None
    gen_time_factunit = casa_idea._factunits.get(slash_time_road)
    assert gen_time_factunit.base != None
    assert gen_time_factunit.base == slash_time_road
    assert gen_time_factunit.pick != None
    assert gen_time_factunit.pick == slash_8am_road

    assert casa_idea._factunits.get(comma_time_road) is None


def test_world_set_road_delimiter_CorrectlyModifies_numeric_roadAND_range_source_road():
    # GIVEN
    luca_world = worldunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_world.add_l1_idea(ideaunit_shop(casa_text))
    comma_casa_road = luca_world.make_l1_road(casa_text)
    cook_text = "cook"
    luca_world.add_idea(ideaunit_shop(cook_text), parent_road=comma_casa_road)
    comma_cook_road = luca_world.make_road(comma_casa_road, cook_text)

    # numeric_road
    taste_text = "foot taste"
    luca_world.add_l1_idea(ideaunit_shop(taste_text, _begin=0, _close=6))
    comma_taste_road = luca_world.make_l1_road(taste_text)
    luca_world.edit_idea_attr(comma_cook_road, numeric_road=comma_taste_road)

    # range_source
    heat_text = "heat numbers"
    luca_world.add_l1_idea(ideaunit_shop(heat_text, _begin=0, _close=6))
    comma_heat_road = luca_world.make_l1_road(heat_text)
    luca_world.edit_idea_attr(comma_cook_road, range_source_road=comma_heat_road)

    cook_idea = luca_world.get_idea_obj(comma_cook_road)
    assert cook_idea._numeric_road == comma_taste_road
    assert cook_idea._range_source_road == comma_heat_road

    # WHEN
    slash_text = "/"
    luca_world.set_road_delimiter(slash_text)

    # THEN
    slash_taste_road = luca_world.make_l1_road(taste_text)
    assert cook_idea._numeric_road != comma_taste_road
    assert cook_idea._numeric_road == slash_taste_road
    slash_heat_road = luca_world.make_l1_road(heat_text)
    assert cook_idea._range_source_road != comma_heat_road
    assert cook_idea._range_source_road == slash_heat_road
