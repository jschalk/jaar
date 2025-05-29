from src.a01_way_logic.way import (
    get_default_fisc_label as root_label,
    get_default_fisc_way,
    create_way,
    default_bridge_if_None,
)
from src.a04_reason_logic.reason_concept import (
    ReasonCore,
    reasoncore_shop,
    reasonheir_shop,
    reasonunit_shop,
    factheir_shop,
    premiseunit_shop,
    reasons_get_from_dict,
)


def test_ReasonCore_attributesExist():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    premises = {wed_premise.pstate: wed_premise}

    # WHEN
    wkday_reason = ReasonCore(
        wkday_way, premises=premises, rconcept_active_requisite=False
    )

    # THEN
    assert wkday_reason.rcontext == wkday_way
    assert wkday_reason.premises == premises
    assert wkday_reason.rconcept_active_requisite is False
    assert wkday_reason.bridge is None


def test_reasoncore_shop_ReturnsCorrectAttrWith_bridge():
    # ESTABLISH
    slash_str = "/"
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str, bridge=slash_str)
    print(f"{casa_way=} ")

    # WHEN
    casa_reason = reasonheir_shop(casa_way, bridge=slash_str)

    # THEN
    assert casa_reason.bridge == slash_str


def test_reasonheir_shop_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)

    # WHEN
    casa_reason = reasonheir_shop(casa_way)

    # THEN
    assert casa_reason.premises == {}
    assert casa_reason.bridge == default_bridge_if_None()


def test_ReasonHeir_clear_CorrectlyClearsField():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)
    email_str = "check email"
    email_way = create_way(casa_way, email_str)
    email_premise = premiseunit_shop(pstate=email_way)
    email_premises = {email_premise.pstate: email_premise}

    # WHEN
    casa_reason = reasonheir_shop(rcontext=casa_way, premises=email_premises)
    # THEN
    assert casa_reason._status is None

    # ESTABLISH
    casa_reason._status = True
    assert casa_reason._status
    # WHEN
    casa_reason.clear_status()
    # THEN
    assert casa_reason._status is None
    assert casa_reason._rcontext_concept_active_value is None


def test_ReasonHeir_set_status_CorrectlySetsStatus():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    fri_str = "friday"
    fri_way = create_way(wkday_way, fri_str)
    thu_str = "thursday"
    thu_way = create_way(wkday_way, thu_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_noon_str = "noon"
    wed_noon_way = create_way(wed_way, wed_noon_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    wed_premises = {wed_premise.pstate: wed_premise}
    wkday_reason = reasonheir_shop(rcontext=wkday_way, premises=wed_premises)
    assert wkday_reason._status is None
    # WHEN
    wkday_fact = factheir_shop(fcontext=wkday_way, fstate=wed_noon_way)
    wkday_facts = {wkday_fact.fcontext: wkday_fact}
    wkday_reason.set_status(factheirs=wkday_facts)
    # THEN
    assert wkday_reason._status is True

    # ESTABLISH
    thu_premise = premiseunit_shop(pstate=thu_way)
    two_premises = {wed_premise.pstate: wed_premise, thu_premise.pstate: thu_premise}
    two_reason = reasonheir_shop(rcontext=wkday_way, premises=two_premises)
    assert two_reason._status is None
    # WHEN
    noon_fact = factheir_shop(fcontext=wkday_way, fstate=wed_noon_way)
    noon_facts = {noon_fact.fcontext: noon_fact}
    two_reason.set_status(factheirs=noon_facts)
    # THEN
    assert two_reason._status is True

    # ESTABLISH
    two_reason.clear_status()
    assert two_reason._status is None
    # WHEN
    fri_fact = factheir_shop(fcontext=wkday_way, fstate=fri_way)
    fri_facts = {fri_fact.fcontext: fri_fact}
    two_reason.set_status(factheirs=fri_facts)
    # THEN
    assert two_reason._status is False


def test_ReasonHeir_set_status_EmptyFactCorrectlySetsStatus():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    wed_premises = {wed_premise.pstate: wed_premise}
    wkday_reason = reasonheir_shop(rcontext=wkday_way, premises=wed_premises)
    assert wkday_reason._status is None
    wkday_reason.set_status(factheirs=None)
    assert wkday_reason._status is False


def test_ReasonHeir_set_rcontext_concept_active_value_Correctly():
    # ESTABLISH
    day_str = "day"
    day_way = create_way(root_label(), day_str)
    day_reason = reasonheir_shop(rcontext=day_way)
    assert day_reason._rcontext_concept_active_value is None

    # WHEN
    day_reason.set_rcontext_concept_active_value(bool_x=True)

    # THEN
    assert day_reason._rcontext_concept_active_value


def test_ReasonHeir_set_status_BudTrueCorrectlySetsStatusTrue():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    week_reason = reasonheir_shop(rcontext=wkday_way, rconcept_active_requisite=True)
    week_reason.set_rcontext_concept_active_value(bool_x=True)
    assert week_reason._status is None

    # WHEN
    week_reason.set_status(factheirs=None)

    # THEN
    assert week_reason._status is True


def test_ReasonHeir_set_status_BudFalseCorrectlySetsStatusTrue():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_way, rconcept_active_requisite=False)
    wkday_reason.set_rcontext_concept_active_value(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs=None)

    # THEN
    assert wkday_reason._status is True


def test_ReasonHeir_set_status_BudTrueCorrectlySetsStatusFalse():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_way, rconcept_active_requisite=True)
    wkday_reason.set_rcontext_concept_active_value(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs=None)

    # THEN
    assert wkday_reason._status is False


def test_ReasonHeir_set_status_BudNoneCorrectlySetsStatusFalse():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_way, rconcept_active_requisite=True)
    wkday_reason.set_rcontext_concept_active_value(bool_x=None)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs={})

    # THEN
    assert wkday_reason._status is False


def test_reasonunit_shop_ReturnsObj():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)

    # WHEN
    wkday_reasonunit = reasonunit_shop(wkday_way)

    # THEN
    assert wkday_reasonunit.premises == {}
    assert wkday_reasonunit.bridge == default_bridge_if_None()


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithSinglethu_premiseequireds():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    wed_premises = {wed_premise.pstate: wed_premise}
    wkday_reason = reasonunit_shop(wkday_way, premises=wed_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "rcontext": wkday_way,
        "premises": {wed_way: {"pstate": wed_way}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWith_rconcept_active_requisite():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_rconcept_active_requisite = True
    wkday_reason = reasonunit_shop(
        wkday_way,
        rconcept_active_requisite=wkday_rconcept_active_requisite,
    )

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "rcontext": wkday_way,
        "rconcept_active_requisite": wkday_rconcept_active_requisite,
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithTwoPremisesReasons():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    thu_str = "thursday"
    thu_way = create_way(wkday_way, thu_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    thu_premise = premiseunit_shop(pstate=thu_way)
    two_premises = {wed_premise.pstate: wed_premise, thu_premise.pstate: thu_premise}
    wkday_reason = reasonunit_shop(wkday_way, premises=two_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "rcontext": wkday_way,
        "premises": {wed_way: {"pstate": wed_way}, thu_way: {"pstate": thu_way}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_reasons_get_from_dict_ReturnsObj():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_rconcept_active_requisite = False
    wkday_reasonunit = reasonunit_shop(
        wkday_way,
        rconcept_active_requisite=wkday_rconcept_active_requisite,
    )
    x_wkday_reasonunits_dict = {wkday_reasonunit.rcontext: wkday_reasonunit.get_dict()}
    assert x_wkday_reasonunits_dict is not None
    static_wkday_reason_dict = {
        wkday_way: {
            "rcontext": wkday_way,
            "rconcept_active_requisite": wkday_rconcept_active_requisite,
        }
    }
    assert x_wkday_reasonunits_dict == static_wkday_reason_dict

    # WHEN
    reasonunits_dict = reasons_get_from_dict(x_wkday_reasonunits_dict)

    # THEN
    assert len(reasonunits_dict) == 1
    assert reasonunits_dict.get(wkday_reasonunit.rcontext) == wkday_reasonunit


def test_ReasonHeir_correctSetsPledgeState():
    # ESTABLISH
    day_str = "ced_day"
    day_way = create_way(root_label(), day_str)
    range_3_to_6_premise = premiseunit_shop(pstate=day_way, popen=3, pnigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.pstate: range_3_to_6_premise}
    range_3_to_6_reason = reasonheir_shop(day_way, range_3_to_6_premises)
    assert range_3_to_6_reason._status is None

    # WHEN
    range_5_to_8_fact = factheir_shop(day_way, day_way, fopen=5, fnigh=8)
    range_5_to_8_facts = {range_5_to_8_fact.fcontext: range_5_to_8_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_8_facts)
    # THEN
    assert range_3_to_6_reason._status is True
    assert range_3_to_6_reason._task is True

    # WHEN
    range_5_to_6_fact = factheir_shop(day_way, day_way, fopen=5, fnigh=6)
    range_5_to_6_facts = {range_5_to_6_fact.fcontext: range_5_to_6_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_6_facts)
    # THEN
    assert range_3_to_6_reason._status is True
    assert range_3_to_6_reason._task is False

    # WHEN
    range_0_to_1_fact = factheir_shop(day_way, day_way, fopen=0, fnigh=1)
    range_0_to_1_facts = {range_0_to_1_fact.fcontext: range_0_to_1_fact}
    range_3_to_6_reason.set_status(factheirs=range_0_to_1_facts)
    # THEN
    assert range_3_to_6_reason._status is False
    assert range_3_to_6_reason._task is None


def test_ReasonCore_get_premises_count():
    # ESTABLISH
    day_str = "day"
    day_way = create_way(root_label(), day_str)

    # WHEN
    day_reason = reasoncore_shop(rcontext=day_way)
    # THEN
    assert day_reason.get_premises_count() == 0

    # WHEN
    range_3_to_6_premise = premiseunit_shop(pstate=day_way, popen=3, pnigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.pstate: range_3_to_6_premise}
    day_reason = reasoncore_shop(rcontext=day_way, premises=range_3_to_6_premises)
    # THEN
    assert day_reason.get_premises_count() == 1


def test_ReasonCore_set_premise_CorrectlySetsPremise():
    # ESTABLISH
    day_str = "day"
    day_way = create_way(root_label(), day_str)
    day_reason = reasoncore_shop(rcontext=day_way)
    assert day_reason.get_premises_count() == 0

    # WHEN
    day_reason.set_premise(premise=day_way, popen=3, pnigh=6)

    # THEN
    assert day_reason.get_premises_count() == 1
    range_3_to_6_premise = premiseunit_shop(pstate=day_way, popen=3, pnigh=6)
    premises = {range_3_to_6_premise.pstate: range_3_to_6_premise}
    assert day_reason.premises == premises


def test_ReasonCore_premise_exists_ReturnsObj():
    # ESTABLISH
    day_str = "day"
    day_way = create_way(root_label(), day_str)
    day_reason = reasoncore_shop(rcontext=day_way)
    assert not day_reason.premise_exists(day_way)

    # WHEN
    day_reason.set_premise(day_way, popen=3, pnigh=6)

    # THEN
    assert day_reason.premise_exists(day_way)


def test_ReasonCore_get_single_premis_ReturnsObj():
    # ESTABLISH
    day_way = create_way(root_label(), "day")
    day_reason = reasoncore_shop(rcontext=day_way)
    day_reason.set_premise(premise=day_way, popen=3, pnigh=6)
    day_reason.set_premise(premise=day_way, popen=7, pnigh=10)
    noon_way = create_way(day_way, "noon")
    day_reason.set_premise(premise=noon_way)
    assert day_reason.get_premises_count() == 2

    # WHEN / THEN
    assert day_reason.get_premise(premise=day_way).popen == 7
    assert day_reason.get_premise(premise=noon_way).popen is None


def test_ReasonCore_del_premise_CorrectlyDeletesPremise():
    # ESTABLISH
    day_str = "day"
    day_way = create_way(root_label(), day_str)
    day_reason = reasoncore_shop(rcontext=day_way)
    day_reason.set_premise(premise=day_way, popen=3, pnigh=6)
    assert day_reason.get_premises_count() == 1

    # WHEN
    day_reason.del_premise(premise=day_way)

    # THEN
    assert day_reason.get_premises_count() == 0


def test_ReasonCore_find_replace_way_casas():
    # ESTABLISH
    weekday_str = "weekday"
    sunday_str = "Sunday"
    old_weekday_way = create_way(root_label(), weekday_str)
    old_sunday_way = create_way(old_weekday_way, sunday_str)
    x_reason = reasoncore_shop(rcontext=old_weekday_way)
    x_reason.set_premise(premise=old_sunday_way)
    # print(f"{x_reason=}")
    assert x_reason.rcontext == old_weekday_way
    assert len(x_reason.premises) == 1
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(old_sunday_way).pstate == old_sunday_way

    # WHEN
    old_way = get_default_fisc_way()
    new_way = create_way("fun")
    x_reason.find_replace_way(old_way=old_way, new_way=new_way)
    new_weekday_way = create_way(new_way, weekday_str)
    new_sunday_way = create_way(new_weekday_way, sunday_str)

    # THEN
    assert x_reason.rcontext == new_weekday_way
    assert len(x_reason.premises) == 1
    assert x_reason.premises.get(new_sunday_way) is not None
    assert x_reason.premises.get(old_sunday_way) is None
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(new_sunday_way).pstate == new_sunday_way


def test_ReasonCore_set_bridge_SetsAttrsCorrectly():
    # ESTABLISH
    week_str = "weekday"
    sun_str = "Sunday"
    slash_str = "/"
    slash_week_way = create_way(root_label(), week_str, bridge=slash_str)
    slash_sun_way = create_way(slash_week_way, sun_str, bridge=slash_str)
    week_reasonunit = reasoncore_shop(slash_week_way, bridge=slash_str)
    week_reasonunit.set_premise(slash_sun_way)
    assert week_reasonunit.bridge == slash_str
    assert week_reasonunit.rcontext == slash_week_way
    assert week_reasonunit.premises.get(slash_sun_way).pstate == slash_sun_way

    # WHEN
    star_str = "*"
    week_reasonunit.set_bridge(new_bridge=star_str)

    # THEN
    assert week_reasonunit.bridge == star_str
    star_week_way = create_way(root_label(), week_str, bridge=star_str)
    star_sun_way = create_way(star_week_way, sun_str, bridge=star_str)
    assert week_reasonunit.rcontext == star_week_way
    assert week_reasonunit.premises.get(star_sun_way) is not None
    assert week_reasonunit.premises.get(star_sun_way).pstate == star_sun_way


def test_ReasonCore_get_obj_key():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)
    email_str = "check email"
    email_way = create_way(casa_way, email_str)
    email_premise = premiseunit_shop(pstate=email_way)
    premises_x = {email_premise.pstate: email_premise}

    # WHEN
    x_reason = reasonheir_shop(casa_way, premises=premises_x)

    # THEN
    assert x_reason.get_obj_key() == casa_way
