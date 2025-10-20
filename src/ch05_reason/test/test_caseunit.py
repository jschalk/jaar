from src.ch02_rope.rope import create_rope, find_replace_rope_key_dict
from src.ch05_reason.reason import (
    CaseUnit,
    cases_get_from_dict,
    caseunit_shop,
    factheir_shop,
)
from src.ref.keywords import Ch05Keywords as kw


def test_CaseUnit_Exists():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope("Amy23", casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)

    # WHEN
    email_case = CaseUnit(reason_state=email_rope)

    # THEN
    assert email_case.reason_state == email_rope
    assert not email_case.reason_lower
    assert not email_case.reason_upper
    assert not email_case.reason_divisor
    assert not email_case.case_active
    assert not email_case.task
    assert not email_case.knot
    obj_attrs = set(email_case.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.case_active,
        kw.task,
        kw.knot,
        kw.reason_divisor,
        kw.reason_upper,
        kw.reason_lower,
        kw.reason_state,
    }


def test_caseunit_shop_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope("Amy23", casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)

    # WHEN
    email_case = caseunit_shop(email_rope)

    # THEN
    assert email_case.reason_state == email_rope


def test_CaseUnit_clear_case_active_SetAttrs():
    # WHEN
    casa_str = "casa"
    casa_rope = create_rope("Amy23", casa_str)
    casaunit = caseunit_shop(casa_rope)
    # THEN
    assert casaunit.case_active is None

    # ESTABLISH
    casaunit.case_active = True
    assert casaunit.case_active

    # WHEN
    casaunit.clear_case_active()

    # THEN
    assert casaunit.case_active is None


def test_CaseUnit_is_range_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope("Amy23", casa_str)

    # WHEN
    casaunit = caseunit_shop(casa_rope, reason_lower=1, reason_upper=3)
    # THEN
    assert casaunit._is_range()

    # WHEN
    casaunit = caseunit_shop(casa_rope)
    # THEN
    assert casaunit._is_range() is False

    # WHEN
    casaunit = caseunit_shop(
        reason_state=casa_rope, reason_divisor=5, reason_lower=3, reason_upper=3
    )
    # THEN
    assert casaunit._is_range() is False


def test_CaseUnit_is_segregate_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope("Amy23", casa_str)

    # WHEN
    casaunit = caseunit_shop(casa_rope, reason_lower=1, reason_upper=3)
    # THEN
    assert casaunit._is_segregate() is False

    # WHEN
    casaunit = caseunit_shop(casa_rope)
    # THEN
    assert casaunit._is_segregate() is False

    # WHEN
    casaunit = caseunit_shop(casa_rope, 3, reason_upper=3, reason_divisor=5)
    # THEN
    assert casaunit._is_segregate()


def test_CaseUnit_is_in_lineage_ReturnsObj_Scenario0_Default_knot():
    # ESTABLISH
    nation_rope = create_rope("Amy23", "Nation-States")
    usa_rope = create_rope(nation_rope, "USA")
    texas_rope = create_rope(usa_rope, "Texas")
    idaho_rope = create_rope(usa_rope, "Idaho")
    texas_fact = factheir_shop(usa_rope, texas_rope)

    # WHEN / THEN
    texas_case = caseunit_shop(texas_rope)
    assert texas_case.is_in_lineage(texas_fact.fact_state)

    # WHEN / THEN
    idaho_case = caseunit_shop(idaho_rope)
    assert idaho_case.is_in_lineage(texas_fact.fact_state) is False

    # WHEN / THEN
    usa_case = caseunit_shop(usa_rope)
    assert usa_case.is_in_lineage(texas_fact.fact_state)

    # ESTABLISH
    sea_rope = create_rope("earth", "sea")  # "earth,sea"
    sea_case = caseunit_shop(sea_rope)

    # THEN
    sea_fact = factheir_shop(sea_rope, sea_rope)
    assert sea_case.is_in_lineage(sea_fact.fact_state)
    seaside_rope = create_rope("earth", "seaside")  # "earth,seaside,beach"
    seaside_beach_rope = create_rope(seaside_rope, "beach")  # "earth,seaside,beach"
    seaside_fact = factheir_shop(seaside_beach_rope, seaside_beach_rope)
    assert sea_case.is_in_lineage(seaside_fact.fact_state) is False


def test_CaseUnit_is_in_lineage_ReturnsObj_WithNonDefault_knot():
    # ESTABLISH
    slash_str = "/"
    nation_rope = create_rope("Amy23", "Nation-States", knot=slash_str)
    usa_rope = create_rope(nation_rope, "USA", knot=slash_str)
    texas_rope = create_rope(usa_rope, "Texas", knot=slash_str)
    idaho_rope = create_rope(usa_rope, "Idaho", knot=slash_str)

    # WHEN
    texas_fact = factheir_shop(usa_rope, texas_rope)

    # THEN
    texas_case = caseunit_shop(texas_rope, knot=slash_str)
    assert texas_case.is_in_lineage(texas_fact.fact_state)

    idaho_case = caseunit_shop(idaho_rope, knot=slash_str)
    assert idaho_case.is_in_lineage(texas_fact.fact_state) is False

    usa_case = caseunit_shop(usa_rope, knot=slash_str)
    print(f"  {usa_case.reason_state=}")
    print(f"{texas_fact.fact_state=}")
    assert usa_case.is_in_lineage(texas_fact.fact_state)

    # ESTABLISH
    # "earth,sea"
    # "earth,seaside"
    # "earth,seaside,beach"
    sea_rope = create_rope("earth", "sea", knot=slash_str)
    seaside_rope = create_rope("earth", "seaside", knot=slash_str)
    seaside_beach_rope = create_rope(seaside_rope, "beach", knot=slash_str)

    # WHEN
    sea_case = caseunit_shop(sea_rope, knot=slash_str)

    # THEN
    sea_fact = factheir_shop(sea_rope, sea_rope)
    assert sea_case.is_in_lineage(sea_fact.fact_state)
    seaside_fact = factheir_shop(seaside_beach_rope, seaside_beach_rope)
    assert sea_case.is_in_lineage(seaside_fact.fact_state) is False


def test_CaseUnit_get_range_segregate_case_active_ReturnsObj_Scenario0_When_is_range_IsTrue():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_rope = create_rope("Amy23", yr_str)
    yr_case = caseunit_shop(yr_rope, reason_lower=3, reason_upper=13)

    # WHEN / THEN
    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=5, fact_upper=11)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=1, fact_upper=11)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=8, fact_upper=17)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=0, fact_upper=2)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=15, fact_upper=19)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=1, fact_upper=19)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)

    # boundary tests
    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=13, fact_upper=19)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=0, fact_upper=3)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=0, fact_upper=0)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False
    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=3, fact_upper=3)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)
    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=13, fact_upper=13)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False
    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=17, fact_upper=17)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=20, fact_upper=17)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False


def test_CaseUnit_get_range_segregate_case_active_ReturnsObj_Scenario1_When_is_segregate_IsTrue():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_rope = create_rope("Amy23", yr_str)
    yr_case = caseunit_shop(yr_rope, reason_divisor=5, reason_lower=0, reason_upper=0)

    # WHEN / THEN
    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=5, fact_upper=5)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=6, fact_upper=6)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=4, fact_upper=6)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=3, fact_upper=4)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    # ESTABLISH
    yr_case = caseunit_shop(
        reason_state=yr_rope, reason_divisor=5, reason_lower=0, reason_upper=2
    )

    # WHEN / THEN
    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=2, fact_upper=2)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=102, fact_upper=102)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact) is False

    yr_fact = factheir_shop(yr_rope, yr_rope, fact_lower=1, fact_upper=4)
    assert yr_case._get_range_segregate_case_active(factheir=yr_fact)


def test_CaseUnit_is_range_or_segregate_ReturnsObj():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)

    # WHEN / THEN
    wk_case = caseunit_shop(wk_rope)
    assert wk_case._is_range_or_segregate() is False

    wk_case = caseunit_shop(wk_rope, reason_lower=5, reason_upper=13)
    assert wk_case._is_range_or_segregate()

    wk_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=17, reason_lower=7, reason_upper=7
    )
    assert wk_case._is_range_or_segregate()


def test_CaseUnit_get_active_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN assumes fact is in lineage
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    wk_case = caseunit_shop(wk_rope)

    # WHEN / THEN
    wk_fact = factheir_shop(wk_rope, wk_rope)
    assert wk_case._get_active(factheir=wk_fact)
    # if fact has range but case does not reqquire range, fact's range does not matter
    wk_fact = factheir_shop(wk_rope, wk_rope, fact_lower=0, fact_upper=2)
    assert wk_case._get_active(factheir=wk_fact)


def test_CaseUnit_get_active_ReturnsObj_Scenario1_ChecksIf_is_range_IsActive():
    # ESTABLISH assumes fact is in lineage
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    wk_case = caseunit_shop(wk_rope, reason_lower=3, reason_upper=7)

    # WHEN / THEN
    wk_fact = factheir_shop(wk_rope, wk_rope)
    assert wk_case._get_active(factheir=wk_fact) is False
    wk_fact = factheir_shop(wk_rope, wk_rope, fact_lower=0, fact_upper=2)
    assert wk_case._get_active(factheir=wk_fact) is False


def test_CaseUnit_set_case_active_SetsAttr_Scenario0_WhenFactUnitIsNull():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    after_str = "afternoon"
    after_rope = create_rope(wk_rope, after_str)
    x_caseunit = caseunit_shop(after_rope)
    belief_fact_2 = None
    assert x_caseunit.case_active is None

    # WHEN
    x_caseunit.set_case_active(x_factheir=belief_fact_2)

    # THEN
    assert x_caseunit.case_active is False


def test_CaseUnit_set_case_active_SetsAttr_Scenario1_case_active_OfSimple():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_case = caseunit_shop(wed_rope)
    belief_fact = factheir_shop(wk_rope, wed_rope)
    assert wed_case.case_active is None

    # WHEN
    wed_case.set_case_active(x_factheir=belief_fact)

    # THEN
    assert wed_case.case_active


def test_CaseUnit_set_case_active_SetsAttr_Scenario2():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_after_str = "afternoon"
    wed_after_rope = create_rope(wed_rope, wed_after_str)
    wed_after_case = caseunit_shop(wed_after_rope)
    assert wed_after_case.case_active is None

    # WHEN
    wed_fact = factheir_shop(wk_rope, wed_rope)
    wed_after_case.set_case_active(x_factheir=wed_fact)

    # THEN
    assert wed_after_case.case_active


def test_CaseUnit_set_case_active_SetsAttr_Scenario3():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_noon_str = "noon"
    wed_noon_rope = create_rope(wed_rope, wed_noon_str)
    wed_case = caseunit_shop(wed_rope)
    assert wed_case.case_active is None

    # WHEN
    noon_fact = factheir_shop(wk_rope, wed_noon_rope)
    wed_case.set_case_active(x_factheir=noon_fact)

    # THEN
    assert wed_case.case_active


def test_CaseUnit_set_case_active_SetsAttr_Scenario4():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    thu_str = "thur"
    thu_rope = create_rope(wk_rope, thu_str)
    wed_case = caseunit_shop(wed_rope)
    thu_fact = factheir_shop(wk_rope, thu_rope)
    assert wed_case.case_active is None
    assert wed_case.is_in_lineage(thu_fact.fact_state) is False
    assert thu_fact.fact_lower is None
    assert thu_fact.fact_upper is None

    # WHEN
    wed_case.set_case_active(x_factheir=thu_fact)

    # THEN
    assert wed_case.case_active is False


def test_CaseUnit_set_case_active_SetsAttr_Scenario5():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope("Amy23", wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_cloudy_str = "cloudy"
    wed_cloudy_rope = create_rope(wed_rope, wed_cloudy_str)
    wed_rain_str = "rainy"
    wed_rain_rope = create_rope(wed_rope, wed_rain_str)
    wed_sun_case = caseunit_shop(wed_cloudy_rope)
    assert wed_sun_case.case_active is None

    # WHEN
    wed_rain_fact = factheir_shop(wk_rope, wed_rain_rope)
    wed_sun_case.set_case_active(x_factheir=wed_rain_fact)

    # THEN
    assert wed_sun_case.case_active is False


def test_CaseUnit_set_case_active_SetsAttr_Scenario6_Clock():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    hr24_str = "24hr"
    hr24_rope = create_rope(clock_rope, hr24_str)
    hr24_case = caseunit_shop(hr24_rope, reason_lower=7, reason_upper=7)
    assert hr24_case.case_active is None

    # WHEN
    range_0_to_8_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=0, fact_upper=8)
    hr24_case.set_case_active(x_factheir=range_0_to_8_fact)

    # THEN
    assert hr24_case.case_active


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario0_When_case_active_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    no_range_case = caseunit_shop(hr24_rope)
    no_range_case.case_active = False

    # WHEN / THEN
    no_range_fact = factheir_shop(hr24_rope, hr24_rope)
    assert no_range_case._get_task_bool(factheir=no_range_fact) is False


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario1_When_is_range_IsTrue():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    range_5_to_31_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=5, reason_upper=31
    )
    range_5_to_31_case.case_active = True

    # WHEN / THEN
    range_7_to_41_fact = factheir_shop(
        hr24_rope, hr24_rope, fact_lower=7, fact_upper=41
    )
    assert range_5_to_31_case._get_task_bool(range_7_to_41_fact)


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario2_When_is_range_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    range_5_to_31_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=5, reason_upper=31
    )
    range_5_to_31_case.case_active = True

    # WHEN / THEN
    range_7_to_21_fact = factheir_shop(
        hr24_rope, hr24_rope, fact_lower=7, fact_upper=21
    )
    assert range_5_to_31_case._get_task_bool(range_7_to_21_fact) is False


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario3_When_is_segregate_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case.case_active = True

    # WHEN / THEN
    range_3_to_5_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=3, fact_upper=5)
    assert o0_n0_d5_case._get_task_bool(range_3_to_5_fact) is False


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario4_When_is_segregate_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case.case_active = False

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=5, fact_upper=7)
    assert o0_n0_d5_case._get_task_bool(range_5_to_7_fact) is False


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario5_When_is_segregate_IsTrue():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case.case_active = True

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=5, fact_upper=7)
    assert o0_n0_d5_case._get_task_bool(range_5_to_7_fact)


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario6_When_is_segregate_IsTrue():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    o0_n0_d5_case = caseunit_shop(
        reason_state=hr24_rope, reason_divisor=5, reason_lower=0, reason_upper=0
    )
    o0_n0_d5_case.case_active = True

    # WHEN / THEN
    range_5_to_5_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=5, fact_upper=5)
    assert o0_n0_d5_case._get_task_bool(factheir=range_5_to_5_fact) is False


def test_CaseUnit_get_task_bool_ReturnsObj_Scenario7_NotNull():
    # ESTABLISH
    wk_str = "wks"
    wk_rope = create_rope("Amy23", wk_str)
    wed_str = "wed"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_case = caseunit_shop(wed_rope)
    wed_case.case_active = True

    # WHEN
    factheir = factheir_shop(wk_rope, wed_rope)

    # THEN
    assert wed_case._get_task_bool(factheir=factheir) is False


def test_CaseUnit_set_case_active_SetAttrs_Scenario01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    range_2_to_7_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=2, reason_upper=7
    )
    assert range_2_to_7_case.case_active is None
    assert range_2_to_7_case.task is None

    # WHEN
    range_0_to_5_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=0, fact_upper=5)
    range_2_to_7_case.set_case_active(x_factheir=range_0_to_5_fact)

    # THEN
    assert range_2_to_7_case.case_active
    assert range_2_to_7_case.task is False


def test_CaseUnit_set_case_active_SetAttrs_Scenario02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope("Amy23", hr24_str)
    range_2_to_7_case = caseunit_shop(
        reason_state=hr24_rope, reason_lower=2, reason_upper=7
    )
    range_0_to_8_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=0, fact_upper=8)
    assert range_2_to_7_case.case_active is None

    # WHEN
    range_2_to_7_case.set_case_active(x_factheir=range_0_to_8_fact)
    # THEN
    assert range_2_to_7_case.case_active
    assert range_2_to_7_case.task

    # ESTABLISH
    range_3_to_5_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=3, fact_upper=5)
    # WHEN
    range_2_to_7_case.set_case_active(x_factheir=range_3_to_5_fact)
    # THEN
    assert range_2_to_7_case.case_active
    assert range_2_to_7_case.task is False

    # ESTABLISH
    range_8_to_8_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=8, fact_upper=8)
    # WHEN
    range_2_to_7_case.set_case_active(x_factheir=range_8_to_8_fact)
    assert range_2_to_7_case.case_active is False
    assert range_2_to_7_case.task is False


def test_CaseUnit_set_case_active_SetAttrs_Scenario03():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    hr24_str = "24hr"
    hr24_rope = create_rope(clock_rope, hr24_str)
    hr24_case = caseunit_shop(hr24_rope, reason_lower=7, reason_upper=7)
    assert hr24_case.case_active is None

    # WHEN
    belief_fact = factheir_shop(hr24_rope, hr24_rope, fact_lower=8, fact_upper=10)
    hr24_case.set_case_active(x_factheir=belief_fact)

    # THEN
    assert hr24_case.case_active is False


def test_CaseUnit_set_case_active_SetAttrs_Scenario4_CEDWeek_case_active_False():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    o1_n1_d6_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=6, reason_lower=1, reason_upper=1
    )
    assert o1_n1_d6_case.case_active is None

    # WHEN
    range_6_to_6_fact = factheir_shop(wk_rope, wk_rope, fact_lower=6, fact_upper=6)
    o1_n1_d6_case.set_case_active(x_factheir=range_6_to_6_fact)

    # THEN
    assert o1_n1_d6_case.case_active is False


def test_CaseUnit_set_case_active_SetAttrs_Scenario5_CEDWeek_case_active_True():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=6, reason_lower=1, reason_upper=1
    )
    belief_fact = factheir_shop(wk_rope, wk_rope, fact_lower=7, fact_upper=7)
    assert wk_case.case_active is None

    # WHEN
    wk_case.set_case_active(x_factheir=belief_fact)

    # THEN
    assert wk_case.case_active


def test_CaseUnit_to_dict_ReturnsObj_Scenario0_With_divisor_reason_lower_reason_upper():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(
        reason_state=wk_rope, reason_divisor=6, reason_lower=1, reason_upper=1
    )

    # WHEN
    case_dict = wk_case.to_dict()

    # THEN
    assert case_dict is not None
    static_dict = {
        kw.reason_state: wk_rope,
        kw.reason_lower: 1,
        kw.reason_upper: 1,
        kw.reason_divisor: 6,
    }
    assert case_dict == static_dict


def test_CaseUnit_to_dict_ReturnsObj_Scenario1_With_reason_lower_reason_upper_WithOut_divisor():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(wk_rope, reason_lower=1, reason_upper=4)

    # WHEN
    case_dict = wk_case.to_dict()

    # THEN
    assert case_dict is not None
    static_dict = {kw.reason_state: wk_rope, "reason_lower": 1, "reason_upper": 4}
    assert case_dict == static_dict


def test_CaseUnit_to_dict_ReturnsObj_Scenario2_WithOnlyRopeTerms():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(wk_rope)

    # WHEN
    case_dict = wk_case.to_dict()

    # THEN
    assert case_dict is not None
    static_dict = {kw.reason_state: wk_rope}
    assert case_dict == static_dict


def test_CaseUnit_get_obj_key():
    # ESTABLISH
    clock_str = "clock"
    clock_rope = create_rope("Amy23", clock_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(clock_rope, wk_str)
    wk_case = caseunit_shop(wk_rope)

    # WHEN / THEN
    assert wk_case.get_obj_key() == wk_rope


def test_CaseUnit_find_replace_rope_casas():
    # ESTABLISH
    old_root_rope = create_rope("old_rope")
    wk_str = "wk"
    wk_rope = create_rope(old_root_rope, wk_str)
    sun_str = "Sun"
    old_sun_rope = create_rope(wk_rope, sun_str)
    sun_case = caseunit_shop(old_sun_rope)
    print(sun_case)
    assert sun_case.reason_state == old_sun_rope

    # WHEN
    new_rope = create_rope("fun")
    sun_case.find_replace_rope(old_rope=old_root_rope, new_rope=new_rope)

    # THEN
    new_wk_rope = create_rope(new_rope, wk_str)
    new_sun_rope = create_rope(new_wk_rope, sun_str)
    assert sun_case.reason_state == new_sun_rope


def test_cases_get_from_dict_ReturnsObj_Scenario0_FromCompleteDict():
    # ESTABLISH
    wk_str = "wks"
    wk_rope = create_rope("Amy23", wk_str)
    static_dict = {
        wk_rope: {
            kw.reason_state: wk_rope,
            kw.reason_lower: 1,
            kw.reason_upper: 30,
            kw.reason_divisor: 5,
        }
    }

    # WHEN
    cases_dict = cases_get_from_dict(static_dict)

    # THEN
    assert len(cases_dict) == 1
    wk_case = cases_dict.get(wk_rope)
    assert wk_case == caseunit_shop(wk_rope, 1, 30, reason_divisor=5)


def test_cases_get_from_dict_ReturnsObj_Scenario1_FromIncompleteDict():
    # ESTABLISH
    wk_str = "wks"
    wk_rope = create_rope("Amy23", wk_str)
    static_dict = {wk_rope: {kw.reason_state: wk_rope}}

    # WHEN
    cases_dict = cases_get_from_dict(static_dict)

    # THEN
    assert len(cases_dict) == 1
    wk_case = cases_dict.get(wk_rope)
    assert wk_case == caseunit_shop(wk_rope)


def test_CaseUnitsUnit_set_knot_SetAttrs():
    # ESTABLISH
    wk_str = "wk"
    sun_str = "Sun"
    slash_str = "/"
    slash_wk_rope = create_rope("Amy23", wk_str, knot=slash_str)
    slash_sun_rope = create_rope(slash_wk_rope, sun_str, knot=slash_str)
    sun_caseunit = caseunit_shop(slash_sun_rope, knot=slash_str)
    assert sun_caseunit.knot == slash_str
    assert sun_caseunit.reason_state == slash_sun_rope

    # WHEN
    colon_str = ":"
    sun_caseunit.set_knot(new_knot=colon_str)

    # THEN
    assert sun_caseunit.knot == colon_str
    colon_wk_rope = create_rope("Amy23", wk_str, knot=colon_str)
    colon_sun_rope = create_rope(colon_wk_rope, sun_str, knot=colon_str)
    assert sun_caseunit.reason_state == colon_sun_rope


def test_rope_find_replace_rope_key_dict_ReturnsCasesUnit_Scenario1():
    # ESTABLISH
    casa_rope = create_rope("Amy23", "casa")
    old_seasons_rope = create_rope(casa_rope, "seasons")
    old_case_x = caseunit_shop(old_seasons_rope)
    old_cases_x = {old_case_x.reason_state: old_case_x}

    assert old_cases_x.get(old_seasons_rope) == old_case_x

    # WHEN
    new_seasons_rope = create_rope(casa_rope, "kookies")
    new_cases_x = find_replace_rope_key_dict(
        dict_x=old_cases_x, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )
    new_case_x = caseunit_shop(new_seasons_rope)

    # THEN
    assert new_cases_x.get(new_seasons_rope) == new_case_x
    assert new_cases_x.get(old_seasons_rope) is None


def test_rope_find_replace_rope_key_dict_ReturnsCasesUnit_Scenario2():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    old_first_label = "El Paso"
    casa_str = "casa"
    seasons_str = "seasons"
    old_casa_rope = create_rope(old_first_label, casa_str)
    old_seasons_rope = create_rope(old_casa_rope, seasons_str)
    old_caseunit = caseunit_shop(old_seasons_rope)
    old_caseunits = {old_caseunit.reason_state: old_caseunit}
    new_first_label = "Austin"
    new_casa_rope = create_rope(new_first_label, casa_str)
    new_seasons_rope = create_rope(new_casa_rope, seasons_str)

    # WHEN
    new_case_ropes = find_replace_rope_key_dict(
        dict_x=old_caseunits, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )
    new_caseunit = caseunit_shop(new_seasons_rope)

    # THEN
    assert new_case_ropes.get(new_seasons_rope) == new_caseunit
    assert new_case_ropes.get(old_seasons_rope) is None
