from src.a01_term_logic.rope import (
    create_rope,
    find_replace_rope_key_dict,
    get_default_central_label as root_label,
)
from src.a04_reason_logic.reason_plan import (
    PremiseUnit,
    factheir_shop,
    premises_get_from_dict,
    premiseunit_shop,
)
from src.a04_reason_logic.test._util.a04_str import (
    _chore_str,
    _status_str,
    knot_str,
    p_divisor_str,
    p_lower_str,
    p_state_str,
    p_upper_str,
)


def test_PremiseUnit_Exists():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)

    # WHEN
    email_premise = PremiseUnit(p_state=email_rope)

    # THEN
    assert email_premise.p_state == email_rope
    assert email_premise.p_lower is None
    assert email_premise.p_upper is None
    assert email_premise.p_divisor is None
    assert email_premise._status is None
    assert email_premise._chore is None
    assert email_premise.knot is None
    obj_attrs = set(email_premise.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        _status_str(),
        _chore_str(),
        knot_str(),
        p_divisor_str(),
        p_upper_str(),
        p_lower_str(),
        p_state_str(),
    }


def test_premiseunit_shop_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)

    # WHEN
    email_premise = premiseunit_shop(p_state=email_rope)

    # THEN
    assert email_premise.p_state == email_rope


def test_PremiseUnit_clear_status_CorrectlySetsAttrs():
    # WHEN
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    casa_premise = premiseunit_shop(p_state=casa_rope)
    # THEN
    assert casa_premise._status is None

    # ESTABLISH
    casa_premise._status = True
    assert casa_premise._status

    # WHEN
    casa_premise.clear_status()

    # THEN
    assert casa_premise._status is None


def test_PremiseUnit_is_range_IdentifiesStatus():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)

    # WHEN
    casa_premise = premiseunit_shop(p_state=casa_rope, p_lower=1, p_upper=3)
    # THEN
    assert casa_premise._is_range()

    # WHEN
    casa_premise = premiseunit_shop(p_state=casa_rope)
    # THEN
    assert casa_premise._is_range() is False

    # WHEN
    casa_premise = premiseunit_shop(
        p_state=casa_rope, p_divisor=5, p_lower=3, p_upper=3
    )
    # THEN
    assert casa_premise._is_range() is False


def test_PremiseUnit_is_segregate_CorrectlyIdentifiesSegregateStatus():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)

    # WHEN
    casa_premise = premiseunit_shop(p_state=casa_rope, p_lower=1, p_upper=3)
    # THEN
    assert casa_premise._is_segregate() is False

    # WHEN
    casa_premise = premiseunit_shop(p_state=casa_rope)
    # THEN
    assert casa_premise._is_segregate() is False

    # WHEN
    casa_premise = premiseunit_shop(
        p_state=casa_rope, p_divisor=5, p_lower=3, p_upper=3
    )
    # THEN
    assert casa_premise._is_segregate()


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineage():
    # ESTABLISH
    nation_rope = create_rope(root_label(), "Nation-States")
    usa_rope = create_rope(nation_rope, "USA")
    texas_rope = create_rope(usa_rope, "Texas")
    idaho_rope = create_rope(usa_rope, "Idaho")
    texas_fact = factheir_shop(f_context=usa_rope, f_state=texas_rope)

    # WHEN / THEN
    texas_premise = premiseunit_shop(p_state=texas_rope)
    assert texas_premise.is_in_lineage(fact_f_state=texas_fact.f_state)

    # WHEN / THEN
    idaho_premise = premiseunit_shop(p_state=idaho_rope)
    assert idaho_premise.is_in_lineage(fact_f_state=texas_fact.f_state) is False

    # WHEN / THEN
    usa_premise = premiseunit_shop(p_state=usa_rope)
    assert usa_premise.is_in_lineage(fact_f_state=texas_fact.f_state)

    # ESTABLISH
    sea_rope = create_rope("earth", "sea")  # "earth,sea"
    sea_premise = premiseunit_shop(p_state=sea_rope)

    # THEN
    sea_fact = factheir_shop(f_context=sea_rope, f_state=sea_rope)
    assert sea_premise.is_in_lineage(fact_f_state=sea_fact.f_state)
    seaside_rope = create_rope("earth", "seaside")  # "earth,seaside,beach"
    seaside_beach_rope = create_rope(seaside_rope, "beach")  # "earth,seaside,beach"
    seaside_fact = factheir_shop(seaside_beach_rope, seaside_beach_rope)
    assert sea_premise.is_in_lineage(fact_f_state=seaside_fact.f_state) is False


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineageWithNonDefaultKnot():
    # ESTABLISH
    slash_str = "/"
    nation_rope = create_rope(root_label(), "Nation-States", knot=slash_str)
    usa_rope = create_rope(nation_rope, "USA", knot=slash_str)
    texas_rope = create_rope(usa_rope, "Texas", knot=slash_str)
    idaho_rope = create_rope(usa_rope, "Idaho", knot=slash_str)

    # WHEN
    texas_fact = factheir_shop(f_context=usa_rope, f_state=texas_rope)

    # THEN
    texas_premise = premiseunit_shop(p_state=texas_rope, knot=slash_str)
    assert texas_premise.is_in_lineage(fact_f_state=texas_fact.f_state)

    idaho_premise = premiseunit_shop(p_state=idaho_rope, knot=slash_str)
    assert idaho_premise.is_in_lineage(fact_f_state=texas_fact.f_state) is False

    usa_premise = premiseunit_shop(p_state=usa_rope, knot=slash_str)
    print(f"  {usa_premise.p_state=}")
    print(f"{texas_fact.f_state=}")
    assert usa_premise.is_in_lineage(fact_f_state=texas_fact.f_state)

    # ESTABLISH
    # "earth,sea"
    # "earth,seaside"
    # "earth,seaside,beach"
    sea_rope = create_rope("earth", "sea", knot=slash_str)
    seaside_rope = create_rope("earth", "seaside", knot=slash_str)
    seaside_beach_rope = create_rope(seaside_rope, "beach", knot=slash_str)

    # WHEN
    sea_premise = premiseunit_shop(p_state=sea_rope, knot=slash_str)

    # THEN
    sea_fact = factheir_shop(f_context=sea_rope, f_state=sea_rope)
    assert sea_premise.is_in_lineage(fact_f_state=sea_fact.f_state)
    seaside_fact = factheir_shop(seaside_beach_rope, seaside_beach_rope)
    assert sea_premise.is_in_lineage(fact_f_state=seaside_fact.f_state) is False


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolFor_is_rangePremise():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_rope = create_rope(root_label(), yr_str)
    yr_premise = premiseunit_shop(p_state=yr_rope, p_lower=3, p_upper=13)

    # WHEN / THEN
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=5, f_upper=11, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=1, f_upper=11, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=8, f_upper=17, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=0, f_upper=2, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=15, f_upper=19, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=1, f_upper=19, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    # boundary tests
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=13, f_upper=19, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=0, f_upper=3, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=0, f_upper=0, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=3, f_upper=3, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=13, f_upper=13, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False
    yr_fact = factheir_shop(f_context=yr_rope, f_lower=17, f_upper=17, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_lower=20, f_upper=17, f_state=yr_rope)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregatePremise():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_rope = create_rope(root_label(), yr_str)
    yr_premise = premiseunit_shop(p_state=yr_rope, p_divisor=5, p_lower=0, p_upper=0)

    # WHEN / THEN
    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=5, f_upper=5)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=6, f_upper=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=4, f_upper=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=3, f_upper=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    # ESTABLISH
    yr_premise = premiseunit_shop(p_state=yr_rope, p_divisor=5, p_lower=0, p_upper=2)

    # WHEN / THEN
    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=2, f_upper=2)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(
        f_context=yr_rope, f_state=yr_rope, f_lower=102, f_upper=102
    )
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(f_context=yr_rope, f_state=yr_rope, f_lower=1, f_upper=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)


def test_PremiseUnitUnit_is_range_or_segregate_ReturnsCorrectBool():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)

    # WHEN / THEN
    wkday_premise = premiseunit_shop(p_state=wkday_rope)
    assert wkday_premise._is_range_or_segregate() is False

    wkday_premise = premiseunit_shop(p_state=wkday_rope, p_lower=5, p_upper=13)
    assert wkday_premise._is_range_or_segregate()

    wkday_premise = premiseunit_shop(
        p_state=wkday_rope, p_divisor=17, p_lower=7, p_upper=7
    )
    assert wkday_premise._is_range_or_segregate()


def test_PremiseUnitUnit_get_premise_status_Returns_active_Boolean():
    # WHEN assumes fact is in lineage
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_premise = premiseunit_shop(p_state=wkday_rope)

    # WHEN / THEN
    wkday_fact = factheir_shop(f_context=wkday_rope, f_state=wkday_rope)
    assert wkday_premise._get_active(factheir=wkday_fact)
    # if fact has range but premise does not reqquire range, fact's range does not matter
    wkday_fact = factheir_shop(
        f_context=wkday_rope, f_state=wkday_rope, f_lower=0, f_upper=2
    )
    assert wkday_premise._get_active(factheir=wkday_fact)


def test_PremiseUnitUnit_get_active_Returns_is_range_active_Boolean():
    # ESTABLISH assumes fact is in lineage
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_premise = premiseunit_shop(p_state=wkday_rope, p_lower=3, p_upper=7)

    # WHEN / THEN
    wkday_fact = factheir_shop(f_context=wkday_rope, f_state=wkday_rope)
    assert wkday_premise._get_active(factheir=wkday_fact) is False
    wkday_fact = factheir_shop(
        f_context=wkday_rope, f_state=wkday_rope, f_lower=0, f_upper=2
    )
    assert wkday_premise._get_active(factheir=wkday_fact) is False


def test_PremiseUnitUnit_set_status_SetsAttr_status_WhenFactUnitIsNull():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    after_str = "afternoon"
    after_rope = create_rope(wkday_rope, after_str)
    premise_2 = premiseunit_shop(p_state=after_rope)
    believer_fact_2 = None
    assert premise_2._status is None

    # WHEN
    premise_2.set_status(x_factheir=believer_fact_2)

    # ESTABLISH
    assert premise_2._status is False


def test_PremiseUnitUnit_set_status_SetsAttr_status_OfSimple():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_premise = premiseunit_shop(p_state=wed_rope)
    believer_fact = factheir_shop(f_context=wkday_rope, f_state=wed_rope)
    assert wed_premise._status is None

    # WHEN
    wed_premise.set_status(x_factheir=believer_fact)

    # THEN
    assert wed_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario2():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_after_str = "afternoon"
    wed_after_rope = create_rope(wed_rope, wed_after_str)
    wed_after_premise = premiseunit_shop(p_state=wed_after_rope)
    assert wed_after_premise._status is None

    # WHEN
    wed_fact = factheir_shop(f_context=wkday_rope, f_state=wed_rope)
    wed_after_premise.set_status(x_factheir=wed_fact)

    # THEN
    assert wed_after_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario3():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_noon_str = "noon"
    wed_noon_rope = create_rope(wed_rope, wed_noon_str)
    wed_premise = premiseunit_shop(p_state=wed_rope)
    assert wed_premise._status is None

    # WHEN
    noon_fact = factheir_shop(f_context=wkday_rope, f_state=wed_noon_rope)
    wed_premise.set_status(x_factheir=noon_fact)

    # THEN
    assert wed_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario4():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    thu_str = "thursday"
    thu_rope = create_rope(wkday_rope, thu_str)
    wed_premise = premiseunit_shop(p_state=wed_rope)
    thu_fact = factheir_shop(f_context=wkday_rope, f_state=thu_rope)
    assert wed_premise._status is None
    assert wed_premise.is_in_lineage(fact_f_state=thu_fact.f_state) is False
    assert thu_fact.f_lower is None
    assert thu_fact.f_upper is None

    # WHEN
    wed_premise.set_status(x_factheir=thu_fact)

    # THEN
    assert wed_premise._status is False


def test_PremiseUnit_set_status_SetsAttr_status_Scenario5():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_rope = create_rope(wkday_rope, wed_str)
    wed_cloudy_str = "cloudy"
    wed_cloudy_rope = create_rope(wed_rope, wed_cloudy_str)
    wed_rain_str = "rainy"
    wed_rain_rope = create_rope(wed_rope, wed_rain_str)
    wed_sun_premise = premiseunit_shop(p_state=wed_cloudy_rope)
    assert wed_sun_premise._status is None

    # WHEN
    wed_rain_fact = factheir_shop(f_context=wkday_rope, f_state=wed_rain_rope)
    wed_sun_premise.set_status(x_factheir=wed_rain_fact)

    # THEN
    assert wed_sun_premise._status is False


def test_PremiseUnit_set_status_SetsStatus_status_ScenarioTime():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    hr24_str = "24hr"
    hr24_rope = create_rope(timetech_rope, hr24_str)
    hr24_premise = premiseunit_shop(p_state=hr24_rope, p_lower=7, p_upper=7)
    assert hr24_premise._status is None

    # WHEN
    range_0_to_8_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=0, f_upper=8)
    hr24_premise.set_status(x_factheir=range_0_to_8_fact)

    # THEN
    assert hr24_premise._status


def test_PremiseUnit_get_chore_status_ReturnsObjWhen_status_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    no_range_premise = premiseunit_shop(p_state=hr24_rope)
    no_range_premise._status = False

    # WHEN / THEN
    no_range_fact = factheir_shop(f_context=hr24_rope, f_state=hr24_rope)
    assert no_range_premise._get_chore_status(factheir=no_range_fact) is False


def test_PremiseUnit_get_chore_status_ReturnsObjWhenBool_is_range_True():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_5_to_31_premise = premiseunit_shop(p_state=hr24_rope, p_lower=5, p_upper=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_41_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=7, f_upper=41)
    assert range_5_to_31_premise._get_chore_status(range_7_to_41_fact)


def test_PremiseUnit_get_chore_status_ReturnsObjWhenBool_is_range_False():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_5_to_31_premise = premiseunit_shop(p_state=hr24_rope, p_lower=5, p_upper=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_21_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=7, f_upper=21)
    assert range_5_to_31_premise._get_chore_status(range_7_to_21_fact) is False


def test_PremiseUnit_get_chore_status_ReturnsObjWhenBoolSegregateFalse_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(
        p_state=hr24_rope, p_divisor=5, p_lower=0, p_upper=0
    )
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_3_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=3, f_upper=5)
    assert o0_n0_d5_premise._get_chore_status(range_3_to_5_fact) is False


def test_PremiseUnit_get_chore_status_ReturnsObjWhenBoolSegregateFalse_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(
        p_state=hr24_rope, p_divisor=5, p_lower=0, p_upper=0
    )
    o0_n0_d5_premise._status = False

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=5, f_upper=7)
    assert o0_n0_d5_premise._get_chore_status(range_5_to_7_fact) is False


def test_PremiseUnit_get_chore_status_ReturnsObjWhenBoolSegregateTrue_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(
        p_state=hr24_rope, p_divisor=5, p_lower=0, p_upper=0
    )
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=5, f_upper=7)
    assert o0_n0_d5_premise._get_chore_status(range_5_to_7_fact)


def test_PremiseUnit_get_chore_status_ReturnsObjWhenBoolSegregateTrue_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(
        p_state=hr24_rope, p_divisor=5, p_lower=0, p_upper=0
    )
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=5, f_upper=5)
    assert o0_n0_d5_premise._get_chore_status(factheir=range_5_to_5_fact) is False


def test_PremiseUnit_get_chore_status_ReturnsObjNotNull():
    # ESTABLISH
    wk_str = "wkdays"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "Wednesday"
    wed_rope = create_rope(wk_rope, wed_str)
    wed_premise = premiseunit_shop(p_state=wed_rope)
    wed_premise._status = True

    # ESTABLISH
    factheir = factheir_shop(f_context=wk_rope, f_state=wed_rope)

    # THEN
    assert wed_premise._get_chore_status(factheir=factheir) is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_2_to_7_premise = premiseunit_shop(p_state=hr24_rope, p_lower=2, p_upper=7)
    assert range_2_to_7_premise._status is None
    assert range_2_to_7_premise._chore is None

    # WHEN
    range_0_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=0, f_upper=5)
    range_2_to_7_premise.set_status(x_factheir=range_0_to_5_fact)

    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._chore is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_rope = create_rope(root_label(), hr24_str)
    range_2_to_7_premise = premiseunit_shop(p_state=hr24_rope, p_lower=2, p_upper=7)
    range_0_to_8_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=0, f_upper=8)
    assert range_2_to_7_premise._status is None

    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_0_to_8_fact)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._chore

    # ESTABLISH
    range_3_to_5_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=3, f_upper=5)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_3_to_5_fact)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._chore is False

    # ESTABLISH
    range_8_to_8_fact = factheir_shop(hr24_rope, hr24_rope, f_lower=8, f_upper=8)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_8_to_8_fact)
    assert range_2_to_7_premise._status is False
    assert range_2_to_7_premise._chore is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario03():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    hr24_str = "24hr"
    hr24_rope = create_rope(timetech_rope, hr24_str)
    hr24_premise = premiseunit_shop(p_state=hr24_rope, p_lower=7, p_upper=7)
    assert hr24_premise._status is None

    # WHEN
    believer_fact = factheir_shop(
        f_context=hr24_rope, f_state=hr24_rope, f_lower=8, f_upper=10
    )
    hr24_premise.set_status(x_factheir=believer_fact)

    # THEN
    assert hr24_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusFalse():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(timetech_rope, wk_str)
    o1_n1_d6_premise = premiseunit_shop(
        p_state=wk_rope, p_divisor=6, p_lower=1, p_upper=1
    )
    assert o1_n1_d6_premise._status is None

    # WHEN
    range_6_to_6_fact = factheir_shop(wk_rope, wk_rope, f_lower=6, f_upper=6)
    o1_n1_d6_premise.set_status(x_factheir=range_6_to_6_fact)

    # THEN
    assert o1_n1_d6_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusTrue():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(timetech_rope, wk_str)
    wk_premise = premiseunit_shop(p_state=wk_rope, p_divisor=6, p_lower=1, p_upper=1)
    believer_fact = factheir_shop(
        f_context=wk_rope, f_state=wk_rope, f_lower=7, f_upper=7
    )
    assert wk_premise._status is None

    # WHEN
    wk_premise.set_status(x_factheir=believer_fact)

    # THEN
    assert wk_premise._status


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithDvisiorAndp_lower_p_upper():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(timetech_rope, wk_str)
    wk_premise = premiseunit_shop(p_state=wk_rope, p_divisor=6, p_lower=1, p_upper=1)

    # WHEN
    premise_dict = wk_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"p_state": wk_rope, "p_lower": 1, "p_upper": 1, "p_divisor": 6}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithp_lowerAndp_upper():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(timetech_rope, wk_str)
    wk_premise = premiseunit_shop(p_state=wk_rope, p_lower=1, p_upper=4)

    # WHEN
    premise_dict = wk_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"p_state": wk_rope, "p_lower": 1, "p_upper": 4}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOnlyRopeTerm():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(timetech_rope, wk_str)
    wk_premise = premiseunit_shop(p_state=wk_rope)

    # WHEN
    premise_dict = wk_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"p_state": wk_rope}
    assert premise_dict == static_dict


def test_PremiseUnit_get_obj_key():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_rope = create_rope(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_rope = create_rope(timetech_rope, wk_str)
    wk_premise = premiseunit_shop(p_state=wk_rope)

    # WHEN / THEN
    assert wk_premise.get_obj_key() == wk_rope


def test_PremiseUnit_find_replace_rope_casas():
    # ESTABLISH
    old_root_rope = create_rope("old_rope")
    wkday_str = "wkday"
    wkday_rope = create_rope(old_root_rope, wkday_str)
    sunday_str = "Sunday"
    old_sunday_rope = create_rope(wkday_rope, sunday_str)
    sunday_premise = premiseunit_shop(p_state=old_sunday_rope)
    print(sunday_premise)
    assert sunday_premise.p_state == old_sunday_rope

    # WHEN
    new_rope = create_rope("fun")
    sunday_premise.find_replace_rope(old_rope=old_root_rope, new_rope=new_rope)

    # THEN
    new_wkday_rope = create_rope(new_rope, wkday_str)
    new_sunday_rope = create_rope(new_wkday_rope, sunday_str)
    assert sunday_premise.p_state == new_sunday_rope


def test_PremiseUnits_get_from_dict_ReturnsCompleteObj():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    static_dict = {
        wkday_rope: {
            "p_state": wkday_rope,
            "p_lower": 1,
            "p_upper": 30,
            "p_divisor": 5,
        }
    }

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    wkday_premise = premises_dict.get(wkday_rope)
    assert wkday_premise == premiseunit_shop(wkday_rope, 1, 30, p_divisor=5)


def test_PremiseUnits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    static_dict = {wkday_rope: {"p_state": wkday_rope}}

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    wkday_premise = premises_dict.get(wkday_rope)
    assert wkday_premise == premiseunit_shop(wkday_rope)


def test_PremiseUnitsUnit_set_knot_SetsAttrsCorrectly():
    # ESTABLISH
    wk_str = "wkday"
    sun_str = "Sunday"
    slash_str = "/"
    slash_wk_rope = create_rope(root_label(), wk_str, knot=slash_str)
    slash_sun_rope = create_rope(slash_wk_rope, sun_str, knot=slash_str)
    sun_premiseunit = premiseunit_shop(slash_sun_rope, knot=slash_str)
    assert sun_premiseunit.knot == slash_str
    assert sun_premiseunit.p_state == slash_sun_rope

    # WHEN
    star_str = "*"
    sun_premiseunit.set_knot(new_knot=star_str)

    # THEN
    assert sun_premiseunit.knot == star_str
    star_wk_rope = create_rope(root_label(), wk_str, knot=star_str)
    star_sun_rope = create_rope(star_wk_rope, sun_str, knot=star_str)
    assert sun_premiseunit.p_state == star_sun_rope


def test_rope_find_replace_rope_key_dict_ReturnsCorrectPremisesUnit_Scenario1():
    # ESTABLISH
    casa_rope = create_rope(root_label(), "casa")
    old_seasons_rope = create_rope(casa_rope, "seasons")
    old_premise_x = premiseunit_shop(p_state=old_seasons_rope)
    old_premises_x = {old_premise_x.p_state: old_premise_x}

    assert old_premises_x.get(old_seasons_rope) == old_premise_x

    # WHEN
    new_seasons_rope = create_rope(casa_rope, "kookies")
    new_premises_x = find_replace_rope_key_dict(
        dict_x=old_premises_x, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )
    new_premise_x = premiseunit_shop(p_state=new_seasons_rope)

    assert new_premises_x.get(new_seasons_rope) == new_premise_x
    assert new_premises_x.get(old_seasons_rope) is None


def test_rope_find_replace_rope_key_dict_ReturnsCorrectPremisesUnit_Scenario2():
    # ESTABLISH
    old_belief_label = "El Paso"
    casa_str = "casa"
    seasons_str = "seasons"
    old_casa_rope = create_rope(old_belief_label, casa_str)
    old_seasons_rope = create_rope(old_casa_rope, seasons_str)
    old_premiseunit = premiseunit_shop(p_state=old_seasons_rope)
    old_premiseunits = {old_premiseunit.p_state: old_premiseunit}
    assert old_premiseunits.get(old_seasons_rope) == old_premiseunit

    # WHEN
    new_belief_label = "Austin"
    new_casa_rope = create_rope(new_belief_label, casa_str)
    new_seasons_rope = create_rope(new_casa_rope, seasons_str)
    new_premise_ropes = find_replace_rope_key_dict(
        dict_x=old_premiseunits, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )
    new_premiseunit = premiseunit_shop(p_state=new_seasons_rope)

    assert new_premise_ropes.get(new_seasons_rope) == new_premiseunit
    assert new_premise_ropes.get(old_seasons_rope) is None
