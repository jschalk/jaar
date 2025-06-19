from src.a01_term_logic.rope import (
    create_rope,
    default_knot_if_None,
    get_default_axiom_label as root_label,
)
from src.a04_reason_logic.reason_concept import (
    ReasonCore,
    factheir_shop,
    premiseunit_shop,
    reasoncore_shop,
    reasonheir_shop,
    reasons_get_from_dict,
    reasonunit_shop,
)
from src.a04_reason_logic.test._util.a04_str import (
    knot_str,
    rconcept_active_requisite_str,
    rcontext_str,
)


def test_ReasonCore_Exists():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_rope)
    premises = {wed_premise.pstate: wed_premise}

    # WHEN
    wkday_reason = ReasonCore(
        wkday_rope, premises=premises, rconcept_active_requisite=False
    )

    # THEN
    assert wkday_reason.rcontext == wkday_rope
    assert wkday_reason.premises == premises
    assert wkday_reason.rconcept_active_requisite is False
    assert wkday_reason.knot is None
    obj_attrs = set(wkday_reason.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        knot_str(),
        "premises",
        rconcept_active_requisite_str(),
        rcontext_str(),
    }


def test_reasoncore_shop_ReturnsCorrectAttrWith_knot():
    # ESTABLISH
    slash_str = "/"
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str, knot=slash_str)
    print(f"{casa_rope=} ")

    # WHEN
    casa_reason = reasonheir_shop(casa_rope, knot=slash_str)

    # THEN
    assert casa_reason.knot == slash_str


def test_reasonheir_shop_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)

    # WHEN
    casa_reason = reasonheir_shop(casa_rope)

    # THEN
    assert casa_reason.premises == {}
    assert casa_reason.knot == default_knot_if_None()


def test_ReasonHeir_clear_CorrectlyClearsField():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)
    email_premise = premiseunit_shop(pstate=email_rope)
    email_premises = {email_premise.pstate: email_premise}

    # WHEN
    casa_reason = reasonheir_shop(rcontext=casa_rope, premises=email_premises)
    # THEN
    assert casa_reason._status is None

    # ESTABLISH
    casa_reason._status = True
    assert casa_reason._status
    # WHEN
    casa_reason.clear_status()
    # THEN
    assert casa_reason._status is None
    assert casa_reason._rconcept_active_value is None


def test_ReasonHeir_set_status_CorrectlySetsStatus():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    fri_str = "friday"
    fri_rope = create_rope(wkday_rope, fri_str)
    thu_str = "thursday"
    thu_rope = create_rope(wkday_rope, thu_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_noon_str = "noon"
    wed_noon_rope = create_rope(wed_rope, wed_noon_str)
    wed_premise = premiseunit_shop(pstate=wed_rope)
    wed_premises = {wed_premise.pstate: wed_premise}
    wkday_reason = reasonheir_shop(rcontext=wkday_rope, premises=wed_premises)
    assert wkday_reason._status is None
    # WHEN
    wkday_fact = factheir_shop(fcontext=wkday_rope, fstate=wed_noon_rope)
    wkday_facts = {wkday_fact.fcontext: wkday_fact}
    wkday_reason.set_status(factheirs=wkday_facts)
    # THEN
    assert wkday_reason._status is True

    # ESTABLISH
    thu_premise = premiseunit_shop(pstate=thu_rope)
    two_premises = {wed_premise.pstate: wed_premise, thu_premise.pstate: thu_premise}
    two_reason = reasonheir_shop(rcontext=wkday_rope, premises=two_premises)
    assert two_reason._status is None
    # WHEN
    noon_fact = factheir_shop(fcontext=wkday_rope, fstate=wed_noon_rope)
    noon_facts = {noon_fact.fcontext: noon_fact}
    two_reason.set_status(factheirs=noon_facts)
    # THEN
    assert two_reason._status is True

    # ESTABLISH
    two_reason.clear_status()
    assert two_reason._status is None
    # WHEN
    fri_fact = factheir_shop(fcontext=wkday_rope, fstate=fri_rope)
    fri_facts = {fri_fact.fcontext: fri_fact}
    two_reason.set_status(factheirs=fri_facts)
    # THEN
    assert two_reason._status is False


def test_ReasonHeir_set_status_EmptyFactCorrectlySetsStatus():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_rope)
    wed_premises = {wed_premise.pstate: wed_premise}
    wkday_reason = reasonheir_shop(rcontext=wkday_rope, premises=wed_premises)
    assert wkday_reason._status is None
    wkday_reason.set_status(factheirs=None)
    assert wkday_reason._status is False


def test_ReasonHeir_set_rconcept_active_value_Correctly():
    # ESTABLISH
    day_str = "day"
    day_rope = create_rope(root_label(), day_str)
    day_reason = reasonheir_shop(rcontext=day_rope)
    assert day_reason._rconcept_active_value is None

    # WHEN
    day_reason.set_rconcept_active_value(bool_x=True)

    # THEN
    assert day_reason._rconcept_active_value


def test_ReasonHeir_set_status_PlanTrueCorrectlySetsStatusTrue():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wk_reason = reasonheir_shop(rcontext=wkday_rope, rconcept_active_requisite=True)
    wk_reason.set_rconcept_active_value(bool_x=True)
    assert wk_reason._status is None

    # WHEN
    wk_reason.set_status(factheirs=None)

    # THEN
    assert wk_reason._status is True


def test_ReasonHeir_set_status_PlanFalseCorrectlySetsStatusTrue():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_rope, rconcept_active_requisite=False)
    wkday_reason.set_rconcept_active_value(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs=None)

    # THEN
    assert wkday_reason._status is True


def test_ReasonHeir_set_status_PlanTrueCorrectlySetsStatusFalse():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_rope, rconcept_active_requisite=True)
    wkday_reason.set_rconcept_active_value(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs=None)

    # THEN
    assert wkday_reason._status is False


def test_ReasonHeir_set_status_PlanNoneCorrectlySetsStatusFalse():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_reason = reasonheir_shop(wkday_rope, rconcept_active_requisite=True)
    wkday_reason.set_rconcept_active_value(bool_x=None)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(factheirs={})

    # THEN
    assert wkday_reason._status is False


def test_reasonunit_shop_ReturnsObj():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)

    # WHEN
    wkday_reasonunit = reasonunit_shop(wkday_rope)

    # THEN
    assert wkday_reasonunit.premises == {}
    assert wkday_reasonunit.knot == default_knot_if_None()


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithSinglethu_premiseequireds():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_rope)
    wed_premises = {wed_premise.pstate: wed_premise}
    wkday_reason = reasonunit_shop(wkday_rope, premises=wed_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "rcontext": wkday_rope,
        "premises": {wed_rope: {"pstate": wed_rope}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWith_rconcept_active_requisite():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_rconcept_active_requisite = True
    wkday_reason = reasonunit_shop(
        wkday_rope,
        rconcept_active_requisite=wkday_rconcept_active_requisite,
    )

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "rcontext": wkday_rope,
        "rconcept_active_requisite": wkday_rconcept_active_requisite,
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithTwoPremisesReasons():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    thu_str = "thursday"
    thu_rope = create_rope(wkday_rope, thu_str)
    wed_premise = premiseunit_shop(pstate=wed_rope)
    thu_premise = premiseunit_shop(pstate=thu_rope)
    two_premises = {wed_premise.pstate: wed_premise, thu_premise.pstate: thu_premise}
    wkday_reason = reasonunit_shop(wkday_rope, premises=two_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict is not None
    static_wkday_reason_dict = {
        "rcontext": wkday_rope,
        "premises": {wed_rope: {"pstate": wed_rope}, thu_rope: {"pstate": thu_rope}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_reasons_get_from_dict_ReturnsObj():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_rconcept_active_requisite = False
    wkday_reasonunit = reasonunit_shop(
        wkday_rope,
        rconcept_active_requisite=wkday_rconcept_active_requisite,
    )
    x_wkday_reasonunits_dict = {wkday_reasonunit.rcontext: wkday_reasonunit.get_dict()}
    assert x_wkday_reasonunits_dict is not None
    static_wkday_reason_dict = {
        wkday_rope: {
            "rcontext": wkday_rope,
            "rconcept_active_requisite": wkday_rconcept_active_requisite,
        }
    }
    assert x_wkday_reasonunits_dict == static_wkday_reason_dict

    # WHEN
    reasonunits_dict = reasons_get_from_dict(x_wkday_reasonunits_dict)

    # THEN
    assert len(reasonunits_dict) == 1
    assert reasonunits_dict.get(wkday_reasonunit.rcontext) == wkday_reasonunit


def test_ReasonHeir_correctSetsTaskState():
    # ESTABLISH
    day_str = "ced_day"
    day_rope = create_rope(root_label(), day_str)
    range_3_to_6_premise = premiseunit_shop(pstate=day_rope, popen=3, pnigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.pstate: range_3_to_6_premise}
    range_3_to_6_reason = reasonheir_shop(day_rope, range_3_to_6_premises)
    assert range_3_to_6_reason._status is None

    # WHEN
    range_5_to_8_fact = factheir_shop(day_rope, day_rope, fopen=5, fnigh=8)
    range_5_to_8_facts = {range_5_to_8_fact.fcontext: range_5_to_8_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_8_facts)
    # THEN
    assert range_3_to_6_reason._status is True
    assert range_3_to_6_reason._chore is True

    # WHEN
    range_5_to_6_fact = factheir_shop(day_rope, day_rope, fopen=5, fnigh=6)
    range_5_to_6_facts = {range_5_to_6_fact.fcontext: range_5_to_6_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_6_facts)
    # THEN
    assert range_3_to_6_reason._status is True
    assert range_3_to_6_reason._chore is False

    # WHEN
    range_0_to_1_fact = factheir_shop(day_rope, day_rope, fopen=0, fnigh=1)
    range_0_to_1_facts = {range_0_to_1_fact.fcontext: range_0_to_1_fact}
    range_3_to_6_reason.set_status(factheirs=range_0_to_1_facts)
    # THEN
    assert range_3_to_6_reason._status is False
    assert range_3_to_6_reason._chore is None


def test_ReasonCore_get_premises_count():
    # ESTABLISH
    day_str = "day"
    day_rope = create_rope(root_label(), day_str)

    # WHEN
    day_reason = reasoncore_shop(rcontext=day_rope)
    # THEN
    assert day_reason.get_premises_count() == 0

    # WHEN
    range_3_to_6_premise = premiseunit_shop(pstate=day_rope, popen=3, pnigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.pstate: range_3_to_6_premise}
    day_reason = reasoncore_shop(rcontext=day_rope, premises=range_3_to_6_premises)
    # THEN
    assert day_reason.get_premises_count() == 1


def test_ReasonCore_set_premise_CorrectlySetsPremise():
    # ESTABLISH
    day_str = "day"
    day_rope = create_rope(root_label(), day_str)
    day_reason = reasoncore_shop(rcontext=day_rope)
    assert day_reason.get_premises_count() == 0

    # WHEN
    day_reason.set_premise(premise=day_rope, popen=3, pnigh=6)

    # THEN
    assert day_reason.get_premises_count() == 1
    range_3_to_6_premise = premiseunit_shop(pstate=day_rope, popen=3, pnigh=6)
    premises = {range_3_to_6_premise.pstate: range_3_to_6_premise}
    assert day_reason.premises == premises


def test_ReasonCore_premise_exists_ReturnsObj():
    # ESTABLISH
    day_str = "day"
    day_rope = create_rope(root_label(), day_str)
    day_reason = reasoncore_shop(rcontext=day_rope)
    assert not day_reason.premise_exists(day_rope)

    # WHEN
    day_reason.set_premise(day_rope, popen=3, pnigh=6)

    # THEN
    assert day_reason.premise_exists(day_rope)


def test_ReasonCore_get_single_premis_ReturnsObj():
    # ESTABLISH
    day_rope = create_rope(root_label(), "day")
    day_reason = reasoncore_shop(rcontext=day_rope)
    day_reason.set_premise(premise=day_rope, popen=3, pnigh=6)
    day_reason.set_premise(premise=day_rope, popen=7, pnigh=10)
    noon_rope = create_rope(day_rope, "noon")
    day_reason.set_premise(premise=noon_rope)
    assert day_reason.get_premises_count() == 2

    # WHEN / THEN
    assert day_reason.get_premise(premise=day_rope).popen == 7
    assert day_reason.get_premise(premise=noon_rope).popen is None


def test_ReasonCore_del_premise_CorrectlyDeletesPremise():
    # ESTABLISH
    day_str = "day"
    day_rope = create_rope(root_label(), day_str)
    day_reason = reasoncore_shop(rcontext=day_rope)
    day_reason.set_premise(premise=day_rope, popen=3, pnigh=6)
    assert day_reason.get_premises_count() == 1

    # WHEN
    day_reason.del_premise(premise=day_rope)

    # THEN
    assert day_reason.get_premises_count() == 0


def test_ReasonCore_find_replace_rope_casas():
    # ESTABLISH
    wkday_str = "wkday"
    sunday_str = "Sunday"
    old_rope = create_rope("old_fun")
    old_wkday_rope = create_rope(old_rope, wkday_str)
    old_sunday_rope = create_rope(old_wkday_rope, sunday_str)
    x_reason = reasoncore_shop(rcontext=old_wkday_rope)
    x_reason.set_premise(premise=old_sunday_rope)
    # print(f"{x_reason=}")
    assert x_reason.rcontext == old_wkday_rope
    assert len(x_reason.premises) == 1
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(old_sunday_rope).pstate == old_sunday_rope

    # WHEN
    new_rope = create_rope("fun")
    x_reason.find_replace_rope(old_rope=old_rope, new_rope=new_rope)
    new_wkday_rope = create_rope(new_rope, wkday_str)
    new_sunday_rope = create_rope(new_wkday_rope, sunday_str)

    # THEN
    assert x_reason.rcontext == new_wkday_rope
    assert len(x_reason.premises) == 1
    assert x_reason.premises.get(new_sunday_rope) is not None
    assert x_reason.premises.get(old_sunday_rope) is None
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(new_sunday_rope).pstate == new_sunday_rope


def test_ReasonCore_set_knot_SetsAttrsCorrectly():
    # ESTABLISH
    wk_str = "wkday"
    sun_str = "Sunday"
    slash_str = "/"
    slash_wk_rope = create_rope(root_label(), wk_str, knot=slash_str)
    slash_sun_rope = create_rope(slash_wk_rope, sun_str, knot=slash_str)
    wk_reasonunit = reasoncore_shop(slash_wk_rope, knot=slash_str)
    wk_reasonunit.set_premise(slash_sun_rope)
    assert wk_reasonunit.knot == slash_str
    assert wk_reasonunit.rcontext == slash_wk_rope
    assert wk_reasonunit.premises.get(slash_sun_rope).pstate == slash_sun_rope

    # WHEN
    star_str = "*"
    wk_reasonunit.set_knot(new_knot=star_str)

    # THEN
    assert wk_reasonunit.knot == star_str
    star_wk_rope = create_rope(root_label(), wk_str, knot=star_str)
    star_sun_rope = create_rope(star_wk_rope, sun_str, knot=star_str)
    assert wk_reasonunit.rcontext == star_wk_rope
    assert wk_reasonunit.premises.get(star_sun_rope) is not None
    assert wk_reasonunit.premises.get(star_sun_rope).pstate == star_sun_rope


def test_ReasonCore_get_obj_key():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)
    email_premise = premiseunit_shop(pstate=email_rope)
    premises_x = {email_premise.pstate: email_premise}

    # WHEN
    x_reason = reasonheir_shop(casa_rope, premises=premises_x)

    # THEN
    assert x_reason.get_obj_key() == casa_rope
