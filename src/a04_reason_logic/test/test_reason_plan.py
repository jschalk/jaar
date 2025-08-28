from src.a01_term_logic.rope import (
    create_rope,
    default_knot_if_None,
    get_default_central_label as root_label,
)
from src.a04_reason_logic.reason import (
    ReasonCore,
    caseunit_shop,
    factheir_shop,
    reasoncore_shop,
    reasonheir_shop,
    reasons_get_from_dict,
    reasonunit_shop,
)
from src.a04_reason_logic.test._util.a04_str import (
    cases_str,
    knot_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_state_str,
)


def test_ReasonCore_Exists():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    cases = {wed_case.reason_state: wed_case}

    # WHEN
    wk_reason = ReasonCore(wk_rope, cases=cases, reason_active_requisite=False)

    # THEN
    assert wk_reason.reason_context == wk_rope
    assert wk_reason.cases == cases
    assert wk_reason.reason_active_requisite is False
    assert wk_reason.knot is None
    obj_attrs = set(wk_reason.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        knot_str(),
        cases_str(),
        reason_active_requisite_str(),
        reason_context_str(),
    }


def test_reasoncore_shop_ReturnsAttrWith_knot():
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
    assert casa_reason.cases == {}
    assert casa_reason.knot == default_knot_if_None()


def test_ReasonHeir_clear_SetsAttrs():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)
    email_case = caseunit_shop(reason_state=email_rope)
    email_cases = {email_case.reason_state: email_case}

    # WHEN
    casa_reason = reasonheir_shop(reason_context=casa_rope, cases=email_cases)
    # THEN
    assert casa_reason.status is None

    # ESTABLISH
    casa_reason.status = True
    assert casa_reason.status
    # WHEN
    casa_reason.clear_status()
    # THEN
    assert casa_reason.status is None
    assert casa_reason._reason_active_heir is None


def test_ReasonHeir_set_status_SetsStatus():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    fri_str = "fri"
    fri_rope = create_rope(wk_rope, fri_str)
    thu_str = "thur"
    thu_rope = create_rope(wk_rope, thu_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_noon_str = "noon"
    wed_noon_rope = create_rope(wed_rope, wed_noon_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_cases = {wed_case.reason_state: wed_case}
    wk_reason = reasonheir_shop(reason_context=wk_rope, cases=wed_cases)
    assert wk_reason.status is None
    # WHEN
    wk_fact = factheir_shop(fact_context=wk_rope, fact_state=wed_noon_rope)
    wk_facts = {wk_fact.fact_context: wk_fact}
    wk_reason.set_status(factheirs=wk_facts)
    # THEN
    assert wk_reason.status is True

    # ESTABLISH
    thu_case = caseunit_shop(reason_state=thu_rope)
    two_cases = {wed_case.reason_state: wed_case, thu_case.reason_state: thu_case}
    two_reason = reasonheir_shop(reason_context=wk_rope, cases=two_cases)
    assert two_reason.status is None
    # WHEN
    noon_fact = factheir_shop(fact_context=wk_rope, fact_state=wed_noon_rope)
    noon_facts = {noon_fact.fact_context: noon_fact}
    two_reason.set_status(factheirs=noon_facts)
    # THEN
    assert two_reason.status is True

    # ESTABLISH
    two_reason.clear_status()
    assert two_reason.status is None
    # WHEN
    fri_fact = factheir_shop(fact_context=wk_rope, fact_state=fri_rope)
    fri_facts = {fri_fact.fact_context: fri_fact}
    two_reason.set_status(factheirs=fri_facts)
    # THEN
    assert two_reason.status is False


def test_ReasonHeir_set_status_EmptyFactSetsStatus():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_cases = {wed_case.reason_state: wed_case}
    wk_reason = reasonheir_shop(reason_context=wk_rope, cases=wed_cases)
    assert wk_reason.status is None

    # WHEN
    wk_reason.set_status(factheirs=None)

    # THEN
    assert wk_reason.status is False


def test_ReasonHeir_set_reason_active_heir_SetsAttr():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasonheir_shop(reason_context=wk_rope)
    assert wk_reason._reason_active_heir is None

    # WHEN
    wk_reason.set_reason_active_heir(bool_x=True)

    # THEN
    assert wk_reason._reason_active_heir


def test_ReasonHeir_set_status_BeliefTrueSetsStatusTrue():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasonheir_shop(reason_context=wk_rope, reason_active_requisite=True)
    wk_reason.set_reason_active_heir(bool_x=True)
    assert wk_reason.status is None

    # WHEN
    wk_reason.set_status(factheirs=None)

    # THEN
    assert wk_reason.status is True


def test_ReasonHeir_set_status_BeliefFalseSetsStatusTrue():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasonheir_shop(wk_rope, reason_active_requisite=False)
    wk_reason.set_reason_active_heir(bool_x=False)
    assert wk_reason.status is None

    # WHEN
    wk_reason.set_status(factheirs=None)

    # THEN
    assert wk_reason.status is True


def test_ReasonHeir_set_status_BeliefTrueSetsStatusFalse():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasonheir_shop(wk_rope, reason_active_requisite=True)
    wk_reason.set_reason_active_heir(bool_x=False)
    assert wk_reason.status is None

    # WHEN
    wk_reason.set_status(factheirs=None)

    # THEN
    assert wk_reason.status is False


def test_ReasonHeir_set_status_BeliefNoneSetsStatusFalse():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasonheir_shop(wk_rope, reason_active_requisite=True)
    wk_reason.set_reason_active_heir(bool_x=None)
    assert wk_reason.status is None

    # WHEN
    wk_reason.set_status(factheirs={})

    # THEN
    assert wk_reason.status is False


def test_reasonunit_shop_ReturnsObj():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)

    # WHEN
    wk_reasonunit = reasonunit_shop(wk_rope)

    # THEN
    assert wk_reasonunit.cases == {}
    assert wk_reasonunit.knot == default_knot_if_None()


def test_ReasonUnit_to_dict_ReturnsDictWithSinglethu_caseequireds():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_cases = {wed_case.reason_state: wed_case}
    wk_reason = reasonunit_shop(wk_rope, cases=wed_cases)

    # WHEN
    wk_reason_dict = wk_reason.to_dict()

    # THEN
    assert wk_reason_dict is not None
    static_wk_reason_dict = {
        "reason_context": wk_rope,
        cases_str(): {wed_rope: {reason_state_str(): wed_rope}},
    }
    print(wk_reason_dict)
    assert wk_reason_dict == static_wk_reason_dict


def test_ReasonUnit_to_dict_ReturnsDictWith_reason_active_requisite():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason_active_requisite = True
    wk_reason = reasonunit_shop(
        wk_rope,
        reason_active_requisite=wk_reason_active_requisite,
    )

    # WHEN
    wk_reason_dict = wk_reason.to_dict()

    # THEN
    assert wk_reason_dict is not None
    static_wk_reason_dict = {
        "reason_context": wk_rope,
        "reason_active_requisite": wk_reason_active_requisite,
    }
    print(wk_reason_dict)
    assert wk_reason_dict == static_wk_reason_dict


def test_ReasonUnit_to_dict_ReturnsDictWithTwoCasesReasons():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    thu_str = "thur"
    thu_rope = create_rope(wk_rope, thu_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    thu_case = caseunit_shop(reason_state=thu_rope)
    two_cases = {wed_case.reason_state: wed_case, thu_case.reason_state: thu_case}
    wk_reason = reasonunit_shop(wk_rope, cases=two_cases)

    # WHEN
    wk_reason_dict = wk_reason.to_dict()

    # THEN
    assert wk_reason_dict is not None
    static_wk_reason_dict = {
        "reason_context": wk_rope,
        cases_str(): {
            wed_rope: {reason_state_str(): wed_rope},
            thu_rope: {reason_state_str(): thu_rope},
        },
    }
    print(wk_reason_dict)
    assert wk_reason_dict == static_wk_reason_dict


def test_reasons_get_from_dict_ReturnsObj():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason_active_requisite = False
    wk_reasonunit = reasonunit_shop(
        wk_rope,
        reason_active_requisite=wk_reason_active_requisite,
    )
    x_wk_reasonunits_dict = {wk_reasonunit.reason_context: wk_reasonunit.to_dict()}
    assert x_wk_reasonunits_dict is not None
    static_wk_reason_dict = {
        wk_rope: {
            "reason_context": wk_rope,
            "reason_active_requisite": wk_reason_active_requisite,
        }
    }
    assert x_wk_reasonunits_dict == static_wk_reason_dict

    # WHEN
    reasonunits_dict = reasons_get_from_dict(x_wk_reasonunits_dict)

    # THEN
    assert len(reasonunits_dict) == 1
    assert reasonunits_dict.get(wk_reasonunit.reason_context) == wk_reasonunit


def test_ReasonHeir_correctSetsTaskState():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    range_3_to_6_case = caseunit_shop(
        reason_state=wk_rope, reason_lower=3, reason_upper=6
    )
    range_3_to_6_cases = {range_3_to_6_case.reason_state: range_3_to_6_case}
    range_3_to_6_reason = reasonheir_shop(wk_rope, range_3_to_6_cases)
    assert range_3_to_6_reason.status is None

    # WHEN
    range_5_to_8_fact = factheir_shop(wk_rope, wk_rope, fact_lower=5, fact_upper=8)
    range_5_to_8_facts = {range_5_to_8_fact.fact_context: range_5_to_8_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_8_facts)
    # THEN
    assert range_3_to_6_reason.status is True
    assert range_3_to_6_reason.chore is True

    # WHEN
    range_5_to_6_fact = factheir_shop(wk_rope, wk_rope, fact_lower=5, fact_upper=6)
    range_5_to_6_facts = {range_5_to_6_fact.fact_context: range_5_to_6_fact}
    range_3_to_6_reason.set_status(factheirs=range_5_to_6_facts)
    # THEN
    assert range_3_to_6_reason.status is True
    assert range_3_to_6_reason.chore is False

    # WHEN
    range_0_to_1_fact = factheir_shop(wk_rope, wk_rope, fact_lower=0, fact_upper=1)
    range_0_to_1_facts = {range_0_to_1_fact.fact_context: range_0_to_1_fact}
    range_3_to_6_reason.set_status(factheirs=range_0_to_1_facts)
    # THEN
    assert range_3_to_6_reason.status is False
    assert range_3_to_6_reason.chore is None


def test_ReasonCore_get_cases_count():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)

    # WHEN
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    # THEN
    assert wk_reason.get_cases_count() == 0

    # WHEN
    range_3_to_6_case = caseunit_shop(
        reason_state=wk_rope, reason_lower=3, reason_upper=6
    )
    range_3_to_6_cases = {range_3_to_6_case.reason_state: range_3_to_6_case}
    wk_reason = reasoncore_shop(reason_context=wk_rope, cases=range_3_to_6_cases)
    # THEN
    assert wk_reason.get_cases_count() == 1


def test_ReasonCore_set_case_SetsCase():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    assert wk_reason.get_cases_count() == 0

    # WHEN
    wk_reason.set_case(case=wk_rope, reason_lower=3, reason_upper=6)

    # THEN
    assert wk_reason.get_cases_count() == 1
    range_3_to_6_case = caseunit_shop(
        reason_state=wk_rope, reason_lower=3, reason_upper=6
    )
    cases = {range_3_to_6_case.reason_state: range_3_to_6_case}
    assert wk_reason.cases == cases


def test_ReasonCore_case_exists_ReturnsObj():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    assert not wk_reason.case_exists(wk_rope)

    # WHEN
    wk_reason.set_case(wk_rope, reason_lower=3, reason_upper=6)

    # THEN
    assert wk_reason.case_exists(wk_rope)


def test_ReasonCore_get_single_premis_ReturnsObj():
    # ESTABLISH
    wk_rope = create_rope(root_label(), "wk")
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    wk_reason.set_case(case=wk_rope, reason_lower=3, reason_upper=6)
    wk_reason.set_case(case=wk_rope, reason_lower=7, reason_upper=10)
    noon_rope = create_rope(wk_rope, "noon")
    wk_reason.set_case(case=noon_rope)
    assert wk_reason.get_cases_count() == 2

    # WHEN / THEN
    assert wk_reason.get_case(case=wk_rope).reason_lower == 7
    assert wk_reason.get_case(case=noon_rope).reason_lower is None


def test_ReasonCore_del_case_DeletesCase():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    wk_reason.set_case(case=wk_rope, reason_lower=3, reason_upper=6)
    assert wk_reason.get_cases_count() == 1

    # WHEN
    wk_reason.del_case(case=wk_rope)

    # THEN
    assert wk_reason.get_cases_count() == 0


def test_ReasonCore_find_replace_rope_casas():
    # ESTABLISH
    wk_str = "wk"
    sun_str = "Sun"
    old_rope = create_rope("old_fun")
    old_wk_rope = create_rope(old_rope, wk_str)
    old_sun_rope = create_rope(old_wk_rope, sun_str)
    x_reason = reasoncore_shop(reason_context=old_wk_rope)
    x_reason.set_case(case=old_sun_rope)
    # print(f"{x_reason=}")
    assert x_reason.reason_context == old_wk_rope
    assert len(x_reason.cases) == 1
    print(f"{x_reason.cases=}")
    new_rope = create_rope("fun")
    assert x_reason.cases.get(old_sun_rope).reason_state == old_sun_rope

    # WHEN
    x_reason.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    # THEN
    new_wk_rope = create_rope(new_rope, wk_str)
    new_sun_rope = create_rope(new_wk_rope, sun_str)
    assert x_reason.reason_context == new_wk_rope
    assert len(x_reason.cases) == 1
    assert x_reason.cases.get(new_sun_rope) is not None
    assert x_reason.cases.get(old_sun_rope) is None
    print(f"{x_reason.cases=}")
    assert x_reason.cases.get(new_sun_rope).reason_state == new_sun_rope


def test_ReasonCore_set_knot_SetsAttrs():
    # ESTABLISH
    wk_str = "wk"
    sun_str = "Sun"
    slash_str = "/"
    slash_wk_rope = create_rope(root_label(), wk_str, knot=slash_str)
    slash_sun_rope = create_rope(slash_wk_rope, sun_str, knot=slash_str)
    wk_reasonunit = reasoncore_shop(slash_wk_rope, knot=slash_str)
    wk_reasonunit.set_case(slash_sun_rope)
    assert wk_reasonunit.knot == slash_str
    assert wk_reasonunit.reason_context == slash_wk_rope
    assert wk_reasonunit.cases.get(slash_sun_rope).reason_state == slash_sun_rope

    # WHEN
    colon_str = ":"
    wk_reasonunit.set_knot(new_knot=colon_str)

    # THEN
    assert wk_reasonunit.knot == colon_str
    colon_wk_rope = create_rope(root_label(), wk_str, knot=colon_str)
    colon_sun_rope = create_rope(colon_wk_rope, sun_str, knot=colon_str)
    assert wk_reasonunit.reason_context == colon_wk_rope
    assert wk_reasonunit.cases.get(colon_sun_rope) is not None
    assert wk_reasonunit.cases.get(colon_sun_rope).reason_state == colon_sun_rope


def test_ReasonCore_get_obj_key():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)
    email_case = caseunit_shop(reason_state=email_rope)
    cases_x = {email_case.reason_state: email_case}

    # WHEN
    x_reason = reasonheir_shop(casa_rope, cases=cases_x)

    # THEN
    assert x_reason.get_obj_key() == casa_rope
