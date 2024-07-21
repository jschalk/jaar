from src.bud.bud import budunit_shop
from src.bud.idea import ideaunit_shop
from src.bud.examples.example_buds import (
    get_budunit_with_4_levels_and_2reasons_2facts,
)
from pytest import raises as pytest_raises
from src.bud.reason_idea import reasonunit_shop, factunit_shop
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
)


def test_BudUnit_edit_idea_label_FailsWhenIdeaDoesNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    casa_text = "casa"
    casa_road = yao_bud.make_l1_road(casa_text)
    swim_text = "swim"
    yao_bud.add_l1_idea(ideaunit_shop(casa_text))
    yao_bud.add_idea(ideaunit_shop(swim_text), parent_road=casa_road)

    # WHEN / THEN
    no_idea_road = yao_bud.make_l1_road("bees")
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert str(excinfo.value) == f"Idea old_road='{no_idea_road}' does not exist"


def test_BudUnit_edit_idea_label_RaisesErrorForLevel0IdeaWhen_real_id_isNone():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(_owner_id=yao_text)

    casa_text = "casa"
    casa_road = yao_bud.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = yao_bud.make_road(casa_road, swim_text)
    yao_bud.add_l1_idea(ideaunit_shop(casa_text))
    yao_bud.add_idea(ideaunit_shop(swim_text), parent_road=casa_road)
    assert yao_bud._owner_id == yao_text
    assert yao_bud._idearoot._label == yao_bud._real_id
    casa_idea = yao_bud.get_idea_obj(casa_road)
    assert casa_idea._parent_road == yao_bud._real_id
    swim_idea = yao_bud.get_idea_obj(swim_road)
    assert swim_idea._parent_road == casa_road

    # WHEN
    moon_text = "moon"
    yao_bud.edit_idea_label(old_road=yao_bud._real_id, new_label=moon_text)

    # THEN
    # with pytest_raises(Exception) as excinfo:
    #     moon_text = "moon"
    #     yao_bud.edit_idea_label(old_road=yao_bud._real_id, new_label=moon_text)
    # assert (
    #     str(excinfo.value)
    #     == f"Cannot set idearoot to string other than '{yao_bud._real_id}'"
    # )

    assert yao_bud._idearoot._label != moon_text
    assert yao_bud._idearoot._label == yao_bud._real_id


def test_BudUnit_edit_idea_label_RaisesErrorForLevel0When_real_id_IsDifferent():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(_owner_id=yao_text)
    casa_text = "casa"
    casa_road = yao_bud.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = yao_bud.make_road(casa_road, swim_text)
    yao_bud.add_l1_idea(ideaunit_shop(casa_text))
    yao_bud.add_idea(ideaunit_shop(swim_text), parent_road=casa_road)
    sun_text = "sun"
    yao_bud._real_id = sun_text
    yao_bud._idearoot._bud_real_id = sun_text
    assert yao_bud._owner_id == yao_text
    assert yao_bud._real_id == sun_text
    assert yao_bud._idearoot._bud_real_id == sun_text
    assert yao_bud._idearoot._label == root_label()
    casa_idea = yao_bud.get_idea_obj(casa_road)
    assert casa_idea._parent_road == root_label()
    swim_idea = yao_bud.get_idea_obj(swim_road)
    assert swim_idea._parent_road == casa_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        yao_bud.edit_idea_label(old_road=root_label(), new_label=moon_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{sun_text}'"
    )


def test_bud_set_real_id_CorrectlySetsAttr():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(_owner_id=yao_text)
    casa_text = "casa"
    old_casa_road = yao_bud.make_l1_road(casa_text)
    swim_text = "swim"
    old_swim_road = yao_bud.make_road(old_casa_road, swim_text)
    yao_bud.add_l1_idea(ideaunit_shop(casa_text))
    yao_bud.add_idea(ideaunit_shop(swim_text), parent_road=old_casa_road)
    assert yao_bud._owner_id == yao_text
    assert yao_bud._idearoot._label == yao_bud._real_id
    casa_idea = yao_bud.get_idea_obj(old_casa_road)
    assert casa_idea._parent_road == yao_bud._real_id
    swim_idea = yao_bud.get_idea_obj(old_swim_road)
    assert swim_idea._parent_road == old_casa_road
    assert yao_bud._real_id == yao_bud._real_id

    # WHEN
    real_id_text = "Sun"
    yao_bud.set_real_id(real_id=real_id_text)

    # THEN
    new_casa_road = yao_bud.make_l1_road(casa_text)
    swim_text = "swim"
    new_swim_road = yao_bud.make_road(new_casa_road, swim_text)
    assert yao_bud._real_id == real_id_text
    assert yao_bud._idearoot._label == real_id_text
    casa_idea = yao_bud.get_idea_obj(new_casa_road)
    assert casa_idea._parent_road == real_id_text
    swim_idea = yao_bud.get_idea_obj(new_swim_road)
    assert swim_idea._parent_road == new_casa_road


def test_BudUnit_find_replace_road_CorrectlyModifies_kids_Scenario1():
    # ESTABLISH Idea with kids that will be different
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)

    old_casa_text = "casa"
    old_casa_road = yao_bud.make_l1_road(old_casa_text)
    bloomers_text = "bloomers"
    old_bloomers_road = yao_bud.make_road(old_casa_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = yao_bud.make_road(old_bloomers_road, roses_text)
    red_text = "red"
    old_red_road = yao_bud.make_road(old_roses_road, red_text)

    yao_bud.add_l1_idea(ideaunit_shop(old_casa_text))
    yao_bud.add_idea(ideaunit_shop(bloomers_text), parent_road=old_casa_road)
    yao_bud.add_idea(ideaunit_shop(roses_text), parent_road=old_bloomers_road)
    yao_bud.add_idea(ideaunit_shop(red_text), parent_road=old_roses_road)
    r_idea_roses = yao_bud.get_idea_obj(old_roses_road)
    r_idea_bloomers = yao_bud.get_idea_obj(old_bloomers_road)

    assert r_idea_bloomers._kids.get(roses_text) is not None
    assert r_idea_roses._parent_road == old_bloomers_road
    assert r_idea_roses._kids.get(red_text) is not None
    r_idea_red = r_idea_roses._kids.get(red_text)
    assert r_idea_red._parent_road == old_roses_road

    # WHEN
    new_casa_text = "casita"
    new_casa_road = yao_bud.make_l1_road(new_casa_text)
    yao_bud.edit_idea_label(old_road=old_casa_road, new_label=new_casa_text)

    # THEN
    assert yao_bud._idearoot._kids.get(new_casa_text) is not None
    assert yao_bud._idearoot._kids.get(old_casa_text) is None

    assert r_idea_bloomers._parent_road == new_casa_road
    assert r_idea_bloomers._kids.get(roses_text) is not None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = yao_bud.make_road(new_casa_road, bloomers_text)
    assert r_idea_roses._parent_road == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) is not None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = yao_bud.make_road(new_bloomers_road, roses_text)
    assert r_idea_red._parent_road == new_roses_road


def test_bud_edit_idea_label_Modifies_factunits():
    # ESTABLISH bud with factunits that will be different
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)

    casa_text = "casa"
    casa_road = yao_bud.make_l1_road(casa_text)
    bloomers_text = "bloomers"
    bloomers_road = yao_bud.make_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = yao_bud.make_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = yao_bud.make_l1_road(old_water_text)
    rain_text = "rain"
    old_rain_road = yao_bud.make_road(old_water_road, rain_text)

    yao_bud.add_l1_idea(ideaunit_shop(casa_text))
    yao_bud.add_idea(ideaunit_shop(roses_text), parent_road=bloomers_road)
    yao_bud.add_idea(ideaunit_shop(rain_text), parent_road=old_water_road)
    yao_bud.set_fact(base=old_water_road, pick=old_rain_road)

    idea_x = yao_bud.get_idea_obj(roses_road)
    assert yao_bud._idearoot._factunits[old_water_road] is not None
    old_water_rain_factunit = yao_bud._idearoot._factunits[old_water_road]
    assert old_water_rain_factunit.base == old_water_road
    assert old_water_rain_factunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = yao_bud.make_l1_road(new_water_text)
    yao_bud.add_l1_idea(ideaunit_shop(new_water_text))
    assert yao_bud._idearoot._factunits.get(new_water_road) is None
    yao_bud.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert yao_bud._idearoot._factunits.get(old_water_road) is None
    assert yao_bud._idearoot._factunits.get(new_water_road) is not None
    new_water_rain_factunit = yao_bud._idearoot._factunits[new_water_road]
    assert new_water_rain_factunit.base == new_water_road
    new_rain_road = yao_bud.make_road(new_water_road, rain_text)
    assert new_water_rain_factunit.pick == new_rain_road

    assert yao_bud._idearoot._factunits.get(new_water_road)
    factunit_obj = yao_bud._idearoot._factunits.get(new_water_road)
    # for factunit_key, factunit_obj in yao_bud._idearoot._factunits.items():
    #     assert factunit_key == new_water_road
    assert factunit_obj.base == new_water_road
    assert factunit_obj.pick == new_rain_road


def test_bud_edit_idea_label_Modifies_idearoot_range_source_road():
    # ESTABLISH this should never happen but best be thorough
    yao_bud = budunit_shop("Yao")
    old_casa_text = "casa"
    old_casa_road = yao_bud.make_l1_road(old_casa_text)
    yao_bud.add_l1_idea(ideaunit_shop(old_casa_text))
    yao_bud.edit_idea_attr(yao_bud._real_id, range_source_road=old_casa_road)
    assert yao_bud._idearoot._range_source_road == old_casa_road

    # WHEN
    new_casa_text = "casita"
    yao_bud.edit_idea_label(old_road=old_casa_road, new_label=new_casa_text)

    # THEN
    new_casa_road = yao_bud.make_l1_road(new_casa_text)
    assert yao_bud._idearoot._range_source_road == new_casa_road


def test_bud_edit_idea_label_ModifiesIdeaUnitN_range_source_road():
    bob_bud = budunit_shop("Bob")
    casa_text = "casa"
    casa_road = bob_bud.make_l1_road(casa_text)
    old_water_text = "water"
    old_water_road = bob_bud.make_road(casa_road, old_water_text)
    rain_text = "rain"
    old_rain_road = bob_bud.make_road(old_water_road, rain_text)
    mood_text = "mood"
    mood_road = bob_bud.make_l1_road(mood_text)
    bob_bud.add_l1_idea(ideaunit_shop(casa_text))
    bob_bud.add_idea(ideaunit_shop(old_water_text), parent_road=casa_road)
    bob_bud.add_idea(ideaunit_shop(rain_text), parent_road=old_water_road)
    bob_bud.add_l1_idea(ideaunit_shop(mood_text))

    bob_bud.edit_idea_attr(road=mood_road, range_source_road=old_rain_road)
    mood_idea = bob_bud.get_idea_obj(mood_road)
    assert mood_idea._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = bob_bud.make_road(casa_road, new_water_text)
    new_rain_road = bob_bud.make_road(new_water_road, rain_text)
    bob_bud.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    # for idea_x in bob_bud._idearoot._kids.values():
    #     print(f"{idea_x._parent_road=} {idea_x._label=}")
    #     for idea_y in idea_x._kids.values():
    #         print(f"{idea_y._parent_road=} {idea_y._label=}")
    #         for idea_z in idea_y._kids.values():
    #             print(f"{idea_z._parent_road=} {idea_z._label=}")
    assert old_rain_road != new_rain_road
    assert mood_idea._range_source_road == new_rain_road


def test_bud_edit_idea_label_ModifiesIdeaReasonUnitsScenario1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_bud.make_l1_road(old_weekday_text)
    wednesday_text = "Wednesday"
    old_wednesday_road = sue_bud.make_road(old_weekday_road, wednesday_text)
    casa_idea = sue_bud.get_idea_obj(sue_bud.make_l1_road("casa"))
    # casa_wk_reason = reasonunit_shop(weekday, premises={wed_premise.need: wed_premise})
    # nation_reason = reasonunit_shop(nationstate, premises={usa_premise.need: usa_premise})
    assert len(casa_idea._reasonunits) == 2
    assert casa_idea._reasonunits.get(old_weekday_road) is not None
    wednesday_idea = sue_bud.get_idea_obj(old_weekday_road)
    casa_weekday_reason = casa_idea._reasonunits.get(old_weekday_road)
    assert casa_weekday_reason.premises.get(old_wednesday_road) is not None
    assert (
        casa_weekday_reason.premises.get(old_wednesday_road).need == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = sue_bud.make_l1_road(new_weekday_text)
    new_wednesday_road = sue_bud.make_road(new_weekday_road, wednesday_text)
    assert casa_idea._reasonunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, reason_x in casa_idea._reasonunits.items():
    #     print(f"Before {key_x=} {reason_x.base=}")
    print(f"BEFORE {wednesday_idea._label=}")
    print(f"BEFORE {wednesday_idea._parent_road=}")
    sue_bud.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    # for key_x, reason_x in casa_idea._reasonunits.items():
    #     print(f"AFTER {key_x=} {reason_x.base=}")
    print(f"AFTER {wednesday_idea._label=}")
    print(f"AFTER {wednesday_idea._parent_road=}")

    # THEN
    assert casa_idea._reasonunits.get(new_weekday_road) is not None
    assert casa_idea._reasonunits.get(old_weekday_road) is None
    casa_weekday_reason = casa_idea._reasonunits.get(new_weekday_road)
    assert casa_weekday_reason.premises.get(new_wednesday_road) is not None
    assert (
        casa_weekday_reason.premises.get(new_wednesday_road).need == new_wednesday_road
    )
    assert len(casa_idea._reasonunits) == 2


def test_bud_set_owner_id_CorrectlyModifiesBoth():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    assert sue_bud._owner_id == "Sue"
    assert sue_bud._idearoot._label == sue_bud._real_id
    # mid_label1 = "Yao"
    # sue_bud.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert sue_bud._owner_id == old_label
    # assert sue_bud._idearoot._label == mid_label1

    # WHEN
    bob_text = "Bob"
    sue_bud.set_owner_id(new_owner_id=bob_text)

    # THEN
    assert sue_bud._owner_id == bob_text
    assert sue_bud._idearoot._label == sue_bud._real_id


def test_bud_edit_idea_label_RaisesErrorIfdelimiterIsInLabel():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_bud.make_l1_road(old_weekday_text)

    # WHEN / THEN
    new_weekday_text = "days, of week"
    with pytest_raises(Exception) as excinfo:
        sue_bud.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_weekday_road}' because new_label {new_weekday_text} contains delimiter {sue_bud._road_delimiter}"
    )


def test_bud_set_road_delimiter_RaisesErrorIfNew_delimiter_IsAnIdea_label():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    print(f"{zia_bud._max_tree_traverse=}")
    casa_text = "casa"
    casa_road = zia_bud.make_l1_road(casa_text)
    zia_bud.add_l1_idea(ideaunit_shop(casa_text))
    slash_text = "/"
    casa_text = f"casa cook{slash_text}clean"
    zia_bud.add_idea(ideaunit_shop(casa_text), parent_road=casa_road)

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
    zia_bud.add_l1_idea(ideaunit_shop(casa_text))
    comma_casa_road = zia_bud.make_l1_road(casa_text)
    cook_text = "cook"
    zia_bud.add_idea(ideaunit_shop(cook_text), parent_road=comma_casa_road)
    comma_cook_road = zia_bud.make_road(comma_casa_road, cook_text)
    cook_idea = zia_bud.get_idea_obj(comma_cook_road)
    comma_text = ","
    assert zia_bud._road_delimiter == comma_text
    comma_cook_road = zia_bud.make_road(comma_casa_road, cook_text)
    # print(f"{zia_bud._real_id=} {zia_bud._idearoot._label=} {casa_road=}")
    # print(f"{cook_idea._parent_road=} {cook_idea._label=}")
    # comma_casa_idea = zia_bud.get_idea_obj(comma_casa_road)
    # print(f"{comma_casa_idea._parent_road=} {comma_casa_idea._label=}")
    assert cook_idea.get_road() == comma_cook_road

    # WHEN
    slash_text = "/"
    zia_bud.set_road_delimiter(slash_text)

    # THEN
    assert cook_idea.get_road() != comma_cook_road
    zia_real_id = zia_bud._real_id
    slash_casa_road = create_road(zia_real_id, casa_text, delimiter=slash_text)
    slash_cook_road = create_road(slash_casa_road, cook_text, delimiter=slash_text)
    assert cook_idea.get_road() == slash_cook_road


def test_bud_set_road_delimiter_CorrectlyModifiesReasonUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_text = "casa"
    zia_bud.add_l1_idea(ideaunit_shop(casa_text))
    time_text = "time"
    comma_time_road = zia_bud.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = zia_bud.make_road(comma_time_road, _8am_text)

    comma_time_reasonunit = reasonunit_shop(base=comma_time_road)
    comma_time_reasonunit.set_premise(comma_8am_road)

    comma_casa_road = zia_bud.make_l1_road(casa_text)
    zia_bud.edit_idea_attr(road=comma_casa_road, reason=comma_time_reasonunit)
    casa_idea = zia_bud.get_idea_obj(comma_casa_road)
    assert casa_idea._reasonunits.get(comma_time_road) is not None
    gen_time_reasonunit = casa_idea._reasonunits.get(comma_time_road)
    assert gen_time_reasonunit.premises.get(comma_8am_road) is not None

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

    assert casa_idea._reasonunits.get(comma_time_road) is None
    assert gen_time_reasonunit.premises.get(comma_8am_road) is None


def test_bud_set_road_delimiter_CorrectlyModifiesFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_text = "casa"
    zia_bud.add_l1_idea(ideaunit_shop(casa_text))
    time_text = "time"
    comma_time_road = zia_bud.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = zia_bud.make_road(comma_time_road, _8am_text)
    comma_time_factunit = factunit_shop(comma_time_road, comma_8am_road)

    comma_casa_road = zia_bud.make_l1_road(casa_text)
    zia_bud.edit_idea_attr(comma_casa_road, factunit=comma_time_factunit)
    casa_idea = zia_bud.get_idea_obj(comma_casa_road)
    print(f"{casa_idea._factunits=} {comma_time_road=}")
    assert casa_idea._factunits.get(comma_time_road) is not None
    gen_time_factunit = casa_idea._factunits.get(comma_time_road)

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

    assert casa_idea._factunits.get(comma_time_road) is None


def test_bud_set_road_delimiter_CorrectlyModifies_numeric_roadAND_range_source_road():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_text = "casa"
    zia_bud.add_l1_idea(ideaunit_shop(casa_text))
    comma_casa_road = zia_bud.make_l1_road(casa_text)
    cook_text = "cook"
    zia_bud.add_idea(ideaunit_shop(cook_text), parent_road=comma_casa_road)
    comma_cook_road = zia_bud.make_road(comma_casa_road, cook_text)

    # numeric_road
    taste_text = "foot taste"
    zia_bud.add_l1_idea(ideaunit_shop(taste_text, _begin=0, _close=6))
    comma_taste_road = zia_bud.make_l1_road(taste_text)
    zia_bud.edit_idea_attr(comma_cook_road, numeric_road=comma_taste_road)

    # range_source_road
    heat_text = "heat numbers"
    zia_bud.add_l1_idea(ideaunit_shop(heat_text, _begin=0, _close=6))
    comma_heat_road = zia_bud.make_l1_road(heat_text)
    zia_bud.edit_idea_attr(comma_cook_road, range_source_road=comma_heat_road)

    cook_idea = zia_bud.get_idea_obj(comma_cook_road)
    assert cook_idea._numeric_road == comma_taste_road
    assert cook_idea._range_source_road == comma_heat_road

    # WHEN
    slash_text = "/"
    zia_bud.set_road_delimiter(slash_text)

    # THEN
    slash_taste_road = zia_bud.make_l1_road(taste_text)
    assert cook_idea._numeric_road != comma_taste_road
    assert cook_idea._numeric_road == slash_taste_road
    slash_heat_road = zia_bud.make_l1_road(heat_text)
    assert cook_idea._range_source_road != comma_heat_road
    assert cook_idea._range_source_road == slash_heat_road
