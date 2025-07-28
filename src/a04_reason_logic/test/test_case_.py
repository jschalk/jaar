from src.a01_term_logic.rope import (
    create_rope,
    find_replace_rope_key_dict,
    get_default_central_label as root_label,
)
from src.a04_reason_logic.reason_plan import (
    CaseUnit,
    cases_get_from_dict,
    caseunit_shop,
    factheir_shop,
)
from src.a04_reason_logic.test._util.a04_str import (
    _chore_str,
    _status_str,
    knot_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
)


def test_CaseUnit_Exists():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)

    # WHEN
    email_case = CaseUnit(reason_state=email_rope)

    # THEN
    assert email_case.reason_state == email_rope
    assert email_case.reason_lower is None
    assert email_case.reason_upper is None
    assert email_case.reason_divisor is None
    assert email_case._status is None
    assert email_case._chore is None
    assert email_case.knot is None
    obj_attrs = set(email_case.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        _status_str(),
        _chore_str(),
        knot_str(),
        reason_divisor_str(),
        reason_upper_str(),
        reason_lower_str(),
        reason_state_str(),
    }


def test_caseunit_shop_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)

    # WHEN
    email_case = caseunit_shop(reason_state=email_rope)

    # THEN
    assert email_case.reason_state == email_rope


def test_CaseUnit_clear_status_CorrectlySetsAttrs():
    # WHEN
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    casa_case = caseunit_shop(reason_state=casa_rope)
    # THEN
    assert casa_case._status is None

    # ESTABLISH
    casa_case._status = True
    assert casa_case._status

    # WHEN
    casa_case.clear_status()

    # THEN
    assert casa_case._status is None


def test_CaseUnit_is_range_IdentifiesStatus():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)

    # WHEN
    casa_case = caseunit_shop(reason_state=casa_rope, reason_lower=1, reason_upper=3)
    # THEN
    assert casa_case._is_range()

    # WHEN
    casa_case = caseunit_shop(reason_state=casa_rope)
    # THEN
    assert casa_case._is_range() is False

    # WHEN
    casa_case = caseunit_shop(
        reason_state=casa_rope, reason_divisor=5, reason_lower=3, reason_upper=3
    )
    # THEN
    assert casa_case._is_range() is False


def test_CaseUnit_is_segregate_CorrectlyIdentifiesSegregateStatus():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)

    # WHEN
    casa_case = caseunit_shop(reason_state=casa_rope, reason_lower=1, reason_upper=3)
    # THEN
    assert casa_case._is_segregate() is False

    # WHEN
    casa_case = caseunit_shop(reason_state=casa_rope)
    # THEN
    assert casa_case._is_segregate() is False

    # WHEN
    casa_case = caseunit_shop(
        reason_state=casa_rope, reason_divisor=5, reason_lower=3, reason_upper=3
    )
    # THEN
    assert casa_case._is_segregate()


def test_CaseUnit_is_in_lineage_CorrectlyIdentifiesLineage():
    # ESTABLISH
    nation_rope = create_rope(root_label(), "Nation-States")
    usa_rope = create_rope(nation_rope, "USA")
    texas_rope = create_rope(usa_rope, "Texas")
    idaho_rope = create_rope(usa_rope, "Idaho")
    texas_fact = factheir_shop(f_context=usa_rope, f_state=texas_rope)

    # WHEN / THEN
    texas_case = caseunit_shop(reason_state=texas_rope)
    assert texas_case.is_in_lineage(fact_f_state=texas_fact.f_state)

    # WHEN / THEN
    idaho_case = caseunit_shop(reason_state=idaho_rope)
    assert idaho_case.is_in_lineage(fact_f_state=texas_fact.f_state) is False

    # WHEN / THEN
    usa_case = caseunit_shop(reason_state=usa_rope)
    assert usa_case.is_in_lineage(fact_f_state=texas_fact.f_state)

    # ESTABLISH
    sea_rope = create_rope("earth", "sea")  # "earth,sea"
    sea_case = caseunit_shop(reason_state=sea_rope)

    # THEN
    sea_fact = factheir_shop(f_context=sea_rope, f_state=sea_rope)
    assert sea_case.is_in_lineage(fact_f_state=sea_fact.f_state)
    seaside_rope = create_rope("earth", "seaside")  # "earth,seaside,beach"
    seaside_beach_rope = create_rope(seaside_rope, "beach")  # "earth,seaside,beach"
    seaside_fact = factheir_shop(seaside_beach_rope, seaside_beach_rope)
    assert sea_case.is_in_lineage(fact_f_state=seaside_fact.f_state) is False


def test_CaseUnit_is_in_lineage_CorrectlyIdentifiesLineageWithNonDefaultKnot():
    # ESTABLISH
    slash_str = "/"
    nation_rope = create_rope(root_label(), "Nation-States", knot=slash_str)
    usa_rope = create_rope(nation_rope, "USA", knot=slash_str)
    texas_rope = create_rope(usa_rope, "Texas", knot=slash_str)
    idaho_rope = create_rope(usa_rope, "Idaho", knot=slash_str)

    # WHEN
    texas_fact = factheir_shop(f_context=usa_rope, f_state=texas_rope)

    # THEN
    texas_case = caseunit_shop(reason_state=texas_rope, knot=slash_str)
    assert texas_case.is_in_lineage(fact_f_state=texas_fact.f_state)

    idaho_case = caseunit_shop(reason_state=idaho_rope, knot=slash_str)
    assert idaho_case.is_in_lineage(fact_f_state=texas_fact.f_state) is False

    usa_case = caseunit_shop(reason_state=usa_rope, knot=slash_str)
    print(f"  {usa_case.reason_state=}")
    print(f"{texas_fact.f_state=}")
    assert usa_case.is_in_lineage(fact_f_state=texas_fact.f_state)

    # ESTABLISH
    # "earth,sea"
    # "earth,seaside"
    # "earth,seaside,beach"
    sea_rope = create_rope("earth", "sea", knot=slash_str)
    seaside_rope = create_rope("earth", "seaside", knot=slash_str)
    seaside_beach_rope = create_rope(seaside_rope, "beach", knot=slash_str)

    # WHEN
    sea_case = caseunit_shop(reason_state=sea_rope, knot=slash_str)

    # THEN
    sea_fact = factheir_shop(f_context=sea_rope, f_state=sea_rope)
    assert sea_case.is_in_lineage(fact_f_state=sea_fact.f_state)
    seaside_fact = factheir_shop(seaside_beach_rope, seaside_beach_rope)
    assert sea_case.is_in_lineage(fact_f_state=seaside_fact.f_state) is False


def test_CaseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolFor_is_rangeCase():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_rope = create_rope(root_label(), yr_str)
    yr_case = caseunit_shop(reason_state=yr_rope, reason_lower=3, reason_upper=13)

    # WHEN / THEN
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=5, f_upper=11, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=1, f_upper=11, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=8, f_upper=17, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=0, f_upper=2, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=15, f_upper=19, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=1, f_upper=19, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)

    # boundary tests
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=13, f_upper=19, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=0, f_upper=3, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=0, f_upper=0, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=3, f_upper=3, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=13, f_upper=13, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=17, f_upper=17, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=20, f_upper=17, f_state=yr_rope)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False


def test_CaseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregateCase():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_rope = create_rope(root_label(), yr_str)
    yr_case = caseunit_shop(
        reason_state=yr_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )

    # WHEN / THEN
    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=5, f_upper=5)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=6, f_upper=6)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=4, f_upper=6)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=3, f_upper=4)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    # ESTABLISH
    yr_case = caseunit_shop(
        reason_state=yr_rope, reason_divisor=5, reason_lower=0, reason_upper=2
    )

    # WHEN / THEN
    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=2, f_upper=2)
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(
        f_context=yr_rope, f_state=yr_rope, f_lower=102, f_upper=102
    )
    assert yr_case._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=1, f_upper=4)
    assert yr_case._get_range_segregate_status(factheir=yr_fact)


def test_CaseUnitUnit_is_range_or_segregate_ReturnsCorrectBool():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)

    # WHEN / THEN
    wk_case = caseunit_shop(reason_state=wk_rope)
    assert wk_case._is_range_or_segregate() is False

    wk_case = caseunit_shop(reason_state=wk_rope, reason_lower=5, reason_upper=13)
    assert wk_case._is_range_or_segregate()

    wk_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=17, reason_lower=7, reason_upper=7
    )
    assert wk_case._is_range_or_segregate()


def test_CaseUnitUnit_get_case_status_Returns_active_Boolean():
    # WHEN assumes fact is in lineage
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_case = caseunit_shop(reason_state=wk_rope)

    # WHEN / THEN
    wk_fact = factheir_shop(f_context=wk_rope, f_state=wk_rope)
    assert wk_case._get_active(factheir=wk_fact)
    # if fact has range but case does not reqquire range, fact's range does not matter
    wk_fact = factheir_shop(f_context=wk_rope, f_state=wk_rope, f_lower=0, f_upper=2)
    assert wk_case._get_active(factheir=wk_fact)


def test_CaseUnitUnit_get_active_Returns_is_range_active_Boolean():
    # ESTABLISH assumes fact is in lineage
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_case = caseunit_shop(reason_state=wk_rope, reason_lower=3, reason_upper=7)

    # WHEN / THEN
    wk_fact = factheir_shop(f_context=wk_rope, f_state=wk_rope)
    assert wk_case._get_active(factheir=wk_fact) is False
    wk_fact = factheir_shop(f_context=wk_rope, f_state=wk_rope, f_lower=0, f_upper=2)
    assert wk_case._get_active(factheir=wk_fact) is False


def test_CaseUnitUnit_set_status_SetsAttr_status_WhenFactUnitIsNull():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    after_str = "afternoon"
    after_rope = create_rope(wk_rope, after_str)
    case_2 = caseunit_shop(reason_state=after_rope)
    believer_fact_2 = None
    assert case_2._status is None

    # WHEN
    case_2.set_status(x_factheir=believer_fact_2)

    # ESTABLISH
    assert case_2._status is False


def test_CaseUnitUnit_set_status_SetsAttr_status_OfSimple():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    believer_fact = factheir_shop(f_context=wk_rope, f_state=wed_rope)
    assert wed_case._status is None

    # WHEN
    wed_case.set_status(x_factheir=believer_fact)

    # THEN
    assert wed_case._status


def test_CaseUnit_set_status_SetsAttr_status_Scenario2():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_after_str = "afternoon"
    wed_after_rope = create_rope(wed_rope, wed_after_str)
    wed_after_case = caseunit_shop(reason_state=wed_after_rope)
    assert wed_after_case._status is None

    # WHEN
    wed_fact = factheir_shop(f_context=wk_rope, f_state=wed_rope)
    wed_after_case.set_status(x_factheir=wed_fact)

    # THEN
    assert wed_after_case._status


def test_CaseUnit_set_status_SetsAttr_status_Scenario3():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_noon_str = "noon"
    wed_noon_rope = create_rope(wed_rope, wed_noon_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    assert wed_case._status is None

    # WHEN
    noon_fact = factheir_shop(f_context=wk_rope, f_state=wed_noon_rope)
    wed_case.set_status(x_factheir=noon_fact)

    # THEN
    assert wed_case._status


def test_CaseUnit_set_status_SetsAttr_status_Scenario4():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    thu_str = "thur"
    thu_rope = create_rope(wk_rope, thu_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    thu_fact = factheir_shop(f_context=wk_rope, f_state=thu_rope)
    assert wed_case._status is None
    assert wed_case.is_in_lineage(fact_f_state=thu_fact.f_state) is False
    assert thu_fact.f_lower is None
    assert thu_fact.f_upper is None

    # WHEN
    wed_case.set_status(x_factheir=thu_fact)

    # THEN
    assert wed_case._status is False


def test_CaseUnit_set_status_SetsAttr_status_Scenario5():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_cloudy_str = "cloudy"
    wed_cloudy_rope = create_rope(wed_rope, wed_cloudy_str)
    wed_rain_str = "rainy"
    wed_rain_rope = create_rope(wed_rope, wed_rain_str)
    wed_sun_case = caseunit_shop(reason_state=wed_cloudy_rope)
    assert wed_sun_case._status is None

    # WHEN
    wed_rain_fact = factheir_shop(f_context=wk_rope, f_state=wed_rain_rope)
    wed_sun_case.set_status(x_factheir=wed_rain_fact)

    # THEN
    assert wed_sun_case._status is False


def test_CaseUnit_set_status_SetsStatus_status_ScenarioClock():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    hr24_str = "24hr"
    hr24_rope = create_rope(clock_rope, hr24_str)
    hr24_case = caseunit_shop(reason_state=hr24_rope, reason_lower=7, reason_upper=7)
    assert hr24_case._status is None

    # WHEN
    range_0_to_8_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=0, f_upper=8)
    hr24_case.set_status(x_factheir=range_0_to_8_fact)

    # THEN
    assert hr24_case._status


def test_CaseUnit_get_chore_status_ReturnsObjWhen_status_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    no_range_case = caseunit_shop(reason_state=hr24_rope)
    no_range_case._status = False

    # WHEN / THEN
    no_range_fact = factheir_shop(f_context=hr24_rope, f_state=hr24_rope)
    assert no_range_case._get_chore_status(factheir=no_range_fact) is False


def test_CaseUnit_get_chore_status_ReturnsObjWhenBool_is_range_True():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_5_to_31_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=5, reason_upper=31
    )
    range_5_to_31_case._status = True

    # WHEN / THEN
    range_7_to_41_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=7, f_upper=41)
    assert range_5_to_31_case._get_chore_status(range_7_to_41_fact)


def test_CaseUnit_get_chore_status_ReturnsObjWhenBool_is_range_False():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_5_to_31_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=5, reason_upper=31
    )
    range_5_to_31_case._status = True

    # WHEN / THEN
    range_7_to_21_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=7, f_upper=21)
    assert range_5_to_31_case._get_chore_status(range_7_to_21_fact) is False


def test_CaseUnit_get_chore_status_ReturnsObjWhenBoolSegregateFalse_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case._status = True

    # WHEN / THEN
    range_3_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=3, f_upper=5)
    assert o0_n0_d5_case._get_chore_status(range_3_to_5_fact) is False


def test_CaseUnit_get_chore_status_ReturnsObjWhenBoolSegregateFalse_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case._status = False

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=5, f_upper=7)
    assert o0_n0_d5_case._get_chore_status(range_5_to_7_fact) is False


def test_CaseUnit_get_chore_status_ReturnsObjWhenBoolSegregateTrue_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case._status = True

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=5, f_upper=7)
    assert o0_n0_d5_case._get_chore_status(range_5_to_7_fact)


def test_CaseUnit_get_chore_status_ReturnsObjWhenBoolSegregateTrue_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case._status = True

    # WHEN / THEN
    range_5_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=5, f_upper=5)
    assert o0_n0_d5_case._get_chore_status(factheir=range_5_to_5_fact) is False


def test_CaseUnit_get_chore_status_ReturnsObjNotNull():
    # ESTABLISH
    wk_str = "wks"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_case._status = True

    # ESTABLISH
    factheir = factheir_shop(f_context=wk_rope, f_state=wed_rope)

    # THEN
    assert wed_case._get_chore_status(factheir=factheir) is False


def test_CaseUnit_set_status_SetsAttrs_Scenario01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_2_to_7_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=2, reason_upper=7
    )
    assert range_2_to_7_case._status is None
    assert range_2_to_7_case._chore is None

    # WHEN
    range_0_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=0, f_upper=5)
    range_2_to_7_case.set_status(x_factheir=range_0_to_5_fact)

    # THEN
    assert range_2_to_7_case._status
    assert range_2_to_7_case._chore is False


def test_CaseUnit_set_status_SetsAttrs_Scenario02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_2_to_7_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=2, reason_upper=7
    )
    range_0_to_8_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=0, f_upper=8)
    assert range_2_to_7_case._status is None

    # WHEN
    range_2_to_7_case.set_status(x_factheir=range_0_to_8_fact)
    # THEN
    assert range_2_to_7_case._status
    assert range_2_to_7_case._chore

    # ESTABLISH
    range_3_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=3, f_upper=5)
    # WHEN
    range_2_to_7_case.set_status(x_factheir=range_3_to_5_fact)
    # THEN
    assert range_2_to_7_case._status
    assert range_2_to_7_case._chore is False

    # ESTABLISH
    range_8_to_8_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=8, f_upper=8)
    # WHEN
    range_2_to_7_case.set_status(x_factheir=range_8_to_8_fact)
    assert range_2_to_7_case._status is False
    assert range_2_to_7_case._chore is False


def test_CaseUnit_set_status_SetsAttrs_Scenario03():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    hr24_str = "24hr"
    hr24_rope = create_rope(clock_rope, hr24_str)
    hr24_case = caseunit_shop(reason_state=hr24_rope, reason_lower=7, reason_upper=7)
    assert hr24_case._status is None

    # WHEN
    believer_fact = factheir_shop(
        f_context=hr24_rope, f_state=hr24_rope, f_lower=8, f_upper=10
    )
    hr24_case.set_status(x_factheir=believer_fact)

    # THEN
    assert hr24_case._status is False


def test_CaseUnit_set_status_CorrectlySetCEDWeekStatusFalse():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    o1_n1_d6_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=6, reason_lower=1, reason_upper=1
    )
    assert o1_n1_d6_case._status is None

    # WHEN
    range_6_to_6_fact = factheir_shop(wk_rope, wk_rope, f_lower=6, f_upper=6)
    o1_n1_d6_case.set_status(x_factheir=range_6_to_6_fact)

    # THEN
    assert o1_n1_d6_case._status is False


def test_CaseUnit_set_status_CorrectlySetCEDWeekStatusTrue():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=6, reason_lower=1, reason_upper=1
    )
    believer_fact = factheir_shop(
        f_context=wk_rope, f_state=wk_rope, f_lower=7, f_upper=7
    )
    assert wk_case._status is None

    # WHEN
    wk_case.set_status(x_factheir=believer_fact)

    # THEN
    assert wk_case._status


def test_CaseUnit_get_dict_ReturnsCorrectDictWithDvisiorAndreason_lower_reason_upper():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=6, reason_lower=1, reason_upper=1
    )

    # WHEN
    case_dict = wk_case.get_dict()

    # THEN
    assert case_dict is not None
    static_dict = {
        "reason_state": wk_rope,
        "reason_lower": 1,
        "reason_upper": 1,
        "reason_divisor": 6,
    }
    assert case_dict == static_dict


def test_CaseUnit_get_dict_ReturnsCorrectDictWithreason_lowerAndreason_upper():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(reason_state=wk_rope, reason_lower=1, reason_upper=4)

    # WHEN
    case_dict = wk_case.get_dict()

    # THEN
    assert case_dict is not None
    static_dict = {"reason_state": wk_rope, "reason_lower": 1, "reason_upper": 4}
    assert case_dict == static_dict


def test_CaseUnit_get_dict_ReturnsCorrectDictWithOnlyRopeTerm():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(reason_state=wk_rope)

    # WHEN
    case_dict = wk_case.get_dict()

    # THEN
    assert case_dict is not None
    static_dict = {"reason_state": wk_rope}
    assert case_dict == static_dict


def test_CaseUnit_get_obj_key():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope(root_label(), clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(reason_state=wk_rope)

    # WHEN / THEN
    assert wk_case.get_obj_key() == wk_rope


def test_CaseUnit_find_replace_rope_casas():
    # ESTABLISH
    old_root_rope = create_rope("old_rope")
    wk_str = "wk"
    wk_rope = create_rope(old_root_rope, wk_str)
    sun_str = "Sun"
    old_sun_rope = create_rope(wk_rope, sun_str)
    sun_case = caseunit_shop(reason_state=old_sun_rope)
    print(sun_case)
    assert sun_case.reason_state == old_sun_rope

    # WHEN
    new_rope = create_rope("fun")
    sun_case.find_replace_rope(old_rope=old_root_rope, new_rope=new_rope)

    # THEN
    new_wk_rope = create_rope(new_rope, wk_str)
    new_sun_rope = create_rope(new_wk_rope, sun_str)
    assert sun_case.reason_state == new_sun_rope


def test_CaseUnits_get_from_dict_ReturnsCompleteObj():
    # ESTABLISH
    wk_str = "wks"
    wk_rope = create_rope(root_label(), wk_str)
    static_dict = {
        wk_rope: {
            "reason_state": wk_rope,
            "reason_lower": 1,
            "reason_upper": 30,
            "reason_divisor": 5,
        }
    }

    # WHEN
    cases_dict = cases_get_from_dict(static_dict)

    # THEN
    assert len(cases_dict) == 1
    wk_case = cases_dict.get(wk_rope)
    assert wk_case == caseunit_shop(wk_rope, 1, 30, reason_divisor=5)


def test_CaseUnits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    wk_str = "wks"
    wk_rope = create_rope(root_label(), wk_str)
    static_dict = {wk_rope: {"reason_state": wk_rope}}

    # WHEN
    cases_dict = cases_get_from_dict(static_dict)

    # THEN
    assert len(cases_dict) == 1
    wk_case = cases_dict.get(wk_rope)
    assert wk_case == caseunit_shop(wk_rope)


def test_CaseUnitsUnit_set_knot_SetsAttrsCorrectly():
    # ESTABLISH
    wk_str = "wk"
    sun_str = "Sun"
    slash_str = "/"
    slash_wk_rope = create_rope(root_label(), wk_str, knot=slash_str)
    slash_sun_rope = create_rope(slash_wk_rope, sun_str, knot=slash_str)
    sun_caseunit = caseunit_shop(slash_sun_rope, knot=slash_str)
    assert sun_caseunit.knot == slash_str
    assert sun_caseunit.reason_state == slash_sun_rope

    # WHEN
    star_str = "*"
    sun_caseunit.set_knot(new_knot=star_str)

    # THEN
    assert sun_caseunit.knot == star_str
    star_wk_rope = create_rope(root_label(), wk_str, knot=star_str)
    star_sun_rope = create_rope(star_wk_rope, sun_str, knot=star_str)
    assert sun_caseunit.reason_state == star_sun_rope


def test_rope_find_replace_rope_key_dict_ReturnsCorrectCasesUnit_Scenario1():
    # ESTABLISH
    casa_rope = create_rope(root_label(), "casa")
    old_seasons_rope = create_rope(casa_rope, "seasons")
    old_case_x = caseunit_shop(reason_state=old_seasons_rope)
    old_cases_x = {old_case_x.reason_state: old_case_x}

    assert old_cases_x.get(old_seasons_rope) == old_case_x

    # WHEN
    new_seasons_rope = create_rope(casa_rope, "kookies")
    new_cases_x = find_replace_rope_key_dict(
        dict_x=old_cases_x, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )
    new_case_x = caseunit_shop(reason_state=new_seasons_rope)

    assert new_cases_x.get(new_seasons_rope) == new_case_x
    assert new_cases_x.get(old_seasons_rope) is None


def test_rope_find_replace_rope_key_dict_ReturnsCorrectCasesUnit_Scenario2():
    # ESTABLISH
    old_belief_label = "El Paso"
    casa_str = "casa"
    seasons_str = "seasons"
    old_casa_rope = create_rope(old_belief_label, casa_str)
    old_seasons_rope = create_rope(old_casa_rope, seasons_str)
    old_caseunit = caseunit_shop(reason_state=old_seasons_rope)
    old_caseunits = {old_caseunit.reason_state: old_caseunit}
    assert old_caseunits.get(old_seasons_rope) == old_caseunit

    # WHEN
    new_belief_label = "Austin"
    new_casa_rope = create_rope(new_belief_label, casa_str)
    new_seasons_rope = create_rope(new_casa_rope, seasons_str)
    new_case_ropes = find_replace_rope_key_dict(
        dict_x=old_caseunits, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )
    new_caseunit = caseunit_shop(reason_state=new_seasons_rope)

    assert new_case_ropes.get(new_seasons_rope) == new_caseunit
    assert new_case_ropes.get(old_seasons_rope) is None
