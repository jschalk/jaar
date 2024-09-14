from src.s2_bud.reason_idea import (
    ReasonCore,
    reasoncore_shop,
    reasonheir_shop,
    reasonunit_shop,
    factheir_shop,
    premiseunit_shop,
    reasons_get_from_dict,
)
from src.s1_road.road import (
    get_default_fiscal_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)


def test_ReasonCore_attributesExist():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_premise = premiseunit_shop(need=wed_road)
    premises = {wed_premise.need: wed_premise}

    # WHEN
    wkday_reason = ReasonCore(
        base=wkday_road, premises=premises, base_idea_active_requisite=False
    )

    # THEN
    assert wkday_reason.base == wkday_road
    assert wkday_reason.premises == premises
    assert wkday_reason.base_idea_active_requisite is False
    assert wkday_reason.delimiter is None


def test_reasoncore_shop_ReturnsCorrectAttrWith_delimiter():
    # ESTABLISH
    slash_str = "/"
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str, delimiter=slash_str)
    print(f"{casa_road=} ")

    # WHEN
    casa_reason = reasonheir_shop(casa_road, delimiter=slash_str)

    # THEN
    assert casa_reason.delimiter == slash_str


def test_reasonheir_shop_ReturnsCorrectObj():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)

    # WHEN
    casa_reason = reasonheir_shop(casa_road)

    # THEN
    assert casa_reason.premises == {}
    assert casa_reason.delimiter == default_road_delimiter_if_none()


def test_ReasonHeir_clear_CorrectlyClearsField():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)
    email_str = "check email"
    email_road = create_road(casa_road, email_str)
    email_premise = premiseunit_shop(need=email_road)
    email_premises = {email_premise.need: email_premise}

    # WHEN
    casa_reason = reasonheir_shop(base=casa_road, premises=email_premises)
    # THEN
    assert casa_reason._status is None

    # ESTABLISH
    casa_reason._status = True
    assert casa_reason._status
    # WHEN
    casa_reason.clear_status()
    # THEN
    assert casa_reason._status is None
    assert casa_reason._base_idea_active_value is None


def test_ReasonHeir_set_status_CorrectlySetsStatus():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    fri_str = "friday"
    fri_road = create_road(wkday_road, fri_str)
    thu_str = "thursday"
    thu_road = create_road(wkday_road, thu_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_noon_str = "noon"
    wed_noon_road = create_road(wed_road, wed_noon_str)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premises = {wed_premise.need: wed_premise}
    wkday_reason = reasonheir_shop(base=wkday_road, premises=wed_premises)
    assert wkday_reason._status is None
    # WHEN
    wkday_fact = factheir_shop(base=wkday_road, pick=wed_noon_road)
    wkday_facts = {wkday_fact.base: wkday_fact}
    wkday_reason.set_status(factheirs=wkday_facts)
    # THEN
    assert wkday_reason._status is True

    # ESTABLISH
    thu_premise = premiseunit_shop(need=thu_road)
    two_premises = {wed_premise.need: wed_premise, thu_premise.need: thu_premise}
    two_reason = reasonheir_shop(base=wkday_road, premises=two_premises)
    assert two_reason._status is None
    # WHEN
    noon_fact = factheir_shop(base=wkday_road, pick=wed_noon_road)
    noon_facts = {noon_fact.base: noon_fact}
    two_reason.set_status(factheirs=noon_facts)
    # THEN
    assert two_reason._status is True

    # ESTABLISH
    two_reason.clear_status()
    assert two_reason._status is None
    # WHEN
    fri_fact = factheir_shop(base=wkday_road, pick=fri_road)
    fri_facts = {fri_fact.base: fri_fact}
    two_reason.set_status(factheirs=fri_facts)
    # THEN
    assert two_reason._status is False


def test_ReasonHeir_set_status_EmptyFactCorrectlySetsStatus():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premises = {wed_premise.need: wed_premise}
    wkday_reason = reasonheir_shop(base=wkday_road, premises=wed_premises)
    assert wkday_reason._status is None
    wkday_reason.set_status(factheirs=None)
    assert wkday_reason._status is False


def test_ReasonHeir_set_base_idea_active_value_Correctly():
    # ESTABLISH
    day_str = "day"
    day_road = create_road(root_label(), day_str)
    day_reason = reasonheir_shop(base=day_road)
    assert day_reason._base_idea_active_value is None

    # WHEN
    day_reason.set_base_idea_active_value(bool_x=True)

    # THEN
    assert day_reason._base_idea_active_value


def test_ReasonHeir_set_status_BudTrueCorrectlySetsStatusTrue():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    week_reason = reasonheir_shop(base=wkday_road, base_idea_active_requisite=True)
    week_reason.set_base_idea_active_value(bool_x=True)
    assert week_reason._status is None

    # WHEN
    week_reason.set_status(factheirs=None)

    # THEN
    assert week_reason._status is True


def test_ReasonHeir_set_status_BudFalseCorrectlySetsStatusTrue():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_road, base_idea_active_requisite=False)
    wkday_reason.set_base_idea_active_value(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs=None)

    # THEN
    assert wkday_reason._status is True


def test_ReasonHeir_set_status_BudTrueCorrectlySetsStatusFalse():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_road, base_idea_active_requisite=True)
    wkday_reason.set_base_idea_active_value(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs=None)

    # THEN
    assert wkday_reason._status is False


def test_ReasonHeir_set_status_BudNoneCorrectlySetsStatusFalse():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_road, base_idea_active_requisite=True)
    wkday_reason.set_base_idea_active_value(bool_x=None)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs={})

    # THEN
    assert wkday_reason._status is False


def test_reasonunit_shop_ReturnsCorrectObj():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)

    # WHEN
    wkday_reasonunit = reasonunit_shop(wkday_road)

    # THEN
    assert wkday_reasonunit.premises == {}
    assert wkday_reasonunit.delimiter == default_road_delimiter_if_none()


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithSinglethu_premiseequireds():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premises = {wed_premise.need: wed_premise}
    wkday_reason = reasonunit_shop(wkday_road, premises=wed_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "base": wkday_road,
        "premises": {wed_road: {"need": wed_road}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWith_base_idea_active_requisite():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wkday_base_idea_active_requisite = True
    wkday_reason = reasonunit_shop(
        wkday_road, base_idea_active_requisite=wkday_base_idea_active_requisite
    )

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "base": wkday_road,
        "base_idea_active_requisite": wkday_base_idea_active_requisite,
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithTwoPremisesReasons():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    thu_str = "thursday"
    thu_road = create_road(wkday_road, thu_str)
    wed_premise = premiseunit_shop(need=wed_road)
    thu_premise = premiseunit_shop(need=thu_road)
    two_premises = {wed_premise.need: wed_premise, thu_premise.need: thu_premise}
    wkday_reason = reasonunit_shop(wkday_road, premises=two_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "base": wkday_road,
        "premises": {wed_road: {"need": wed_road}, thu_road: {"need": thu_road}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_reasons_get_from_dict_ReturnsCorrectObj():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wkday_base_idea_active_requisite = False
    wkday_reasonunit = reasonunit_shop(
        wkday_road, base_idea_active_requisite=wkday_base_idea_active_requisite
    )
    x_wkday_reasonunits_dict = {wkday_reasonunit.base: wkday_reasonunit.get_dict()}
    assert x_wkday_reasonunits_dict is not None
    static_wkday_reason_dict = {
        wkday_road: {
            "base": wkday_road,
            "base_idea_active_requisite": wkday_base_idea_active_requisite,
        }
    }
    assert x_wkday_reasonunits_dict == static_wkday_reason_dict

    # WHEN
    reasonunits_dict = reasons_get_from_dict(x_wkday_reasonunits_dict)

    # THEN
    assert len(reasonunits_dict) == 1
    assert reasonunits_dict.get(wkday_reasonunit.base) == wkday_reasonunit


def test_ReasonHeir_correctSetsPledgeState():
    # ESTABLISH
    day_str = "ced_day"
    day_road = create_road(root_label(), day_str)
    range_3_to_6_premise = premiseunit_shop(need=day_road, open=3, nigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.need: range_3_to_6_premise}
    range_3_to_6_reason = reasonheir_shop(day_road, range_3_to_6_premises)
    assert range_3_to_6_reason._status is None

    # WHEN
    range_5_to_8_fact = factheir_shop(day_road, day_road, fopen=5, fnigh=8)
    range_5_to_8_facts = {range_5_to_8_fact.base: range_5_to_8_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_8_facts)
    # THEN
    assert range_3_to_6_reason._status is True
    assert range_3_to_6_reason._task is True

    # WHEN
    range_5_to_6_fact = factheir_shop(day_road, day_road, fopen=5, fnigh=6)
    range_5_to_6_facts = {range_5_to_6_fact.base: range_5_to_6_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_6_facts)
    # THEN
    assert range_3_to_6_reason._status is True
    assert range_3_to_6_reason._task is False

    # WHEN
    range_0_to_1_fact = factheir_shop(day_road, day_road, fopen=0, fnigh=1)
    range_0_to_1_facts = {range_0_to_1_fact.base: range_0_to_1_fact}
    range_3_to_6_reason.set_status(factheirs=range_0_to_1_facts)
    # THEN
    assert range_3_to_6_reason._status is False
    assert range_3_to_6_reason._task is None


def test_ReasonCore_get_premises_count():
    # ESTABLISH
    day_str = "day"
    day_road = create_road(root_label(), day_str)

    # WHEN
    day_reason = reasoncore_shop(base=day_road)
    # THEN
    assert day_reason.get_premises_count() == 0

    # WHEN
    range_3_to_6_premise = premiseunit_shop(need=day_road, open=3, nigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.need: range_3_to_6_premise}
    day_reason = reasoncore_shop(base=day_road, premises=range_3_to_6_premises)
    # THEN
    assert day_reason.get_premises_count() == 1


def test_ReasonCore_set_premise_CorrectlySetsPremise():
    # ESTABLISH
    day_str = "day"
    day_road = create_road(root_label(), day_str)
    day_reason = reasoncore_shop(base=day_road)
    assert day_reason.get_premises_count() == 0

    # WHEN
    day_reason.set_premise(premise=day_road, open=3, nigh=6)

    # THEN
    assert day_reason.get_premises_count() == 1
    range_3_to_6_premise = premiseunit_shop(need=day_road, open=3, nigh=6)
    premises = {range_3_to_6_premise.need: range_3_to_6_premise}
    assert day_reason.premises == premises


def test_ReasonCore_premise_exists_ReturnsObj():
    # ESTABLISH
    day_str = "day"
    day_road = create_road(root_label(), day_str)
    day_reason = reasoncore_shop(base=day_road)
    assert not day_reason.premise_exists(day_road)

    # WHEN
    day_reason.set_premise(day_road, open=3, nigh=6)

    # THEN
    assert day_reason.premise_exists(day_road)


def test_ReasonCore_get_single_premis_ReturnsCorrectObj():
    # ESTABLISH
    day_road = create_road(root_label(), "day")
    day_reason = reasoncore_shop(base=day_road)
    day_reason.set_premise(premise=day_road, open=3, nigh=6)
    day_reason.set_premise(premise=day_road, open=7, nigh=10)
    noon_road = create_road(day_road, "noon")
    day_reason.set_premise(premise=noon_road)
    assert day_reason.get_premises_count() == 2

    # WHEN / THEN
    assert day_reason.get_premise(premise=day_road).open == 7
    assert day_reason.get_premise(premise=noon_road).open is None


def test_ReasonCore_del_premise_CorrectlyDeletesPremise():
    # ESTABLISH
    day_str = "day"
    day_road = create_road(root_label(), day_str)
    day_reason = reasoncore_shop(base=day_road)
    day_reason.set_premise(premise=day_road, open=3, nigh=6)
    assert day_reason.get_premises_count() == 1

    # WHEN
    day_reason.del_premise(premise=day_road)

    # THEN
    assert day_reason.get_premises_count() == 0


def test_ReasonCore_find_replace_road_casas():
    # ESTABLISH
    weekday_str = "weekday"
    sunday_str = "Sunday"
    old_weekday_road = create_road(root_label(), weekday_str)
    old_sunday_road = create_road(old_weekday_road, sunday_str)
    x_reason = reasoncore_shop(base=old_weekday_road)
    x_reason.set_premise(premise=old_sunday_road)
    # print(f"{x_reason=}")
    assert x_reason.base == old_weekday_road
    assert len(x_reason.premises) == 1
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(old_sunday_road).need == old_sunday_road

    # WHEN
    old_road = root_label()
    new_road = "fun"
    x_reason.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_str)
    new_sunday_road = create_road(new_weekday_road, sunday_str)

    # THEN
    assert x_reason.base == new_weekday_road
    assert len(x_reason.premises) == 1
    assert x_reason.premises.get(new_sunday_road) is not None
    assert x_reason.premises.get(old_sunday_road) is None
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(new_sunday_road).need == new_sunday_road


def test_ReasonCore_set_delimiter_SetsAttrsCorrectly():
    # ESTABLISH
    week_str = "weekday"
    sun_str = "Sunday"
    slash_str = "/"
    slash_week_road = create_road(root_label(), week_str, delimiter=slash_str)
    slash_sun_road = create_road(slash_week_road, sun_str, delimiter=slash_str)
    week_reasonunit = reasoncore_shop(slash_week_road, delimiter=slash_str)
    week_reasonunit.set_premise(slash_sun_road)
    assert week_reasonunit.delimiter == slash_str
    assert week_reasonunit.base == slash_week_road
    assert week_reasonunit.premises.get(slash_sun_road).need == slash_sun_road

    # WHEN
    star_str = "*"
    week_reasonunit.set_delimiter(new_delimiter=star_str)

    # THEN
    assert week_reasonunit.delimiter == star_str
    star_week_road = create_road(root_label(), week_str, delimiter=star_str)
    star_sun_road = create_road(star_week_road, sun_str, delimiter=star_str)
    assert week_reasonunit.base == star_week_road
    assert week_reasonunit.premises.get(star_sun_road) is not None
    assert week_reasonunit.premises.get(star_sun_road).need == star_sun_road


def test_ReasonCore_get_obj_key():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)
    email_str = "check email"
    email_road = create_road(casa_road, email_str)
    email_premise = premiseunit_shop(need=email_road)
    premises_x = {email_premise.need: email_premise}

    # WHEN
    x_reason = reasonheir_shop(casa_road, premises=premises_x)

    # THEN
    assert x_reason.get_obj_key() == casa_road
