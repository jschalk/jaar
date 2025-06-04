from src.a01_term_logic.way import (
    create_way,
    find_replace_way_key_dict,
    get_default_axiom_label as root_label,
)
from src.a04_reason_logic._test_util.a04_str import (
    _status_str,
    _task_str,
    bridge_str,
    pdivisor_str,
    pnigh_str,
    popen_str,
    pstate_str,
)
from src.a04_reason_logic.reason_concept import (
    PremiseUnit,
    factheir_shop,
    premises_get_from_dict,
    premiseunit_shop,
)


def test_PremiseUnit_Exists():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)
    email_str = "check email"
    email_way = create_way(casa_way, email_str)

    # WHEN
    email_premise = PremiseUnit(pstate=email_way)

    # THEN
    assert email_premise.pstate == email_way
    assert email_premise.popen is None
    assert email_premise.pnigh is None
    assert email_premise.pdivisor is None
    assert email_premise._status is None
    assert email_premise._task is None
    assert email_premise.bridge is None
    obj_attrs = set(email_premise.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        _status_str(),
        _task_str(),
        bridge_str(),
        pdivisor_str(),
        pnigh_str(),
        popen_str(),
        pstate_str(),
    }


def test_premiseunit_shop_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)
    email_str = "check email"
    email_way = create_way(casa_way, email_str)

    # WHEN
    email_premise = premiseunit_shop(pstate=email_way)

    # THEN
    assert email_premise.pstate == email_way


def test_PremiseUnit_clear_status_CorrectlySetsAttrs():
    # WHEN
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)
    casa_premise = premiseunit_shop(pstate=casa_way)
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
    casa_way = create_way(root_label(), casa_str)

    # WHEN
    casa_premise = premiseunit_shop(pstate=casa_way, popen=1, pnigh=3)
    # THEN
    assert casa_premise._is_range()

    # WHEN
    casa_premise = premiseunit_shop(pstate=casa_way)
    # THEN
    assert casa_premise._is_range() is False

    # WHEN
    casa_premise = premiseunit_shop(pstate=casa_way, pdivisor=5, popen=3, pnigh=3)
    # THEN
    assert casa_premise._is_range() is False


def test_PremiseUnit_is_segregate_CorrectlyIdentifiesSegregateStatus():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)

    # WHEN
    casa_premise = premiseunit_shop(pstate=casa_way, popen=1, pnigh=3)
    # THEN
    assert casa_premise._is_segregate() is False

    # WHEN
    casa_premise = premiseunit_shop(pstate=casa_way)
    # THEN
    assert casa_premise._is_segregate() is False

    # WHEN
    casa_premise = premiseunit_shop(pstate=casa_way, pdivisor=5, popen=3, pnigh=3)
    # THEN
    assert casa_premise._is_segregate()


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineage():
    # ESTABLISH
    nation_way = create_way(root_label(), "Nation-States")
    usa_way = create_way(nation_way, "USA")
    texas_way = create_way(usa_way, "Texas")
    idaho_way = create_way(usa_way, "Idaho")
    texas_fact = factheir_shop(fcontext=usa_way, fstate=texas_way)

    # WHEN / THEN
    texas_premise = premiseunit_shop(pstate=texas_way)
    assert texas_premise.is_in_lineage(fact_fstate=texas_fact.fstate)

    # WHEN / THEN
    idaho_premise = premiseunit_shop(pstate=idaho_way)
    assert idaho_premise.is_in_lineage(fact_fstate=texas_fact.fstate) is False

    # WHEN / THEN
    usa_premise = premiseunit_shop(pstate=usa_way)
    assert usa_premise.is_in_lineage(fact_fstate=texas_fact.fstate)

    # ESTABLISH
    sea_way = create_way("earth", "sea")  # "earth,sea"
    sea_premise = premiseunit_shop(pstate=sea_way)

    # THEN
    sea_fact = factheir_shop(fcontext=sea_way, fstate=sea_way)
    assert sea_premise.is_in_lineage(fact_fstate=sea_fact.fstate)
    seaside_way = create_way("earth", "seaside")  # "earth,seaside,beach"
    seaside_beach_way = create_way(seaside_way, "beach")  # "earth,seaside,beach"
    seaside_fact = factheir_shop(seaside_beach_way, seaside_beach_way)
    assert sea_premise.is_in_lineage(fact_fstate=seaside_fact.fstate) is False


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineageWithNonDefaultBridge():
    # ESTABLISH
    slash_str = "/"
    nation_way = create_way(root_label(), "Nation-States", bridge=slash_str)
    usa_way = create_way(nation_way, "USA", bridge=slash_str)
    texas_way = create_way(usa_way, "Texas", bridge=slash_str)
    idaho_way = create_way(usa_way, "Idaho", bridge=slash_str)

    # WHEN
    texas_fact = factheir_shop(fcontext=usa_way, fstate=texas_way)

    # THEN
    texas_premise = premiseunit_shop(pstate=texas_way, bridge=slash_str)
    assert texas_premise.is_in_lineage(fact_fstate=texas_fact.fstate)

    idaho_premise = premiseunit_shop(pstate=idaho_way, bridge=slash_str)
    assert idaho_premise.is_in_lineage(fact_fstate=texas_fact.fstate) is False

    usa_premise = premiseunit_shop(pstate=usa_way, bridge=slash_str)
    print(f"  {usa_premise.pstate=}")
    print(f"{texas_fact.fstate=}")
    assert usa_premise.is_in_lineage(fact_fstate=texas_fact.fstate)

    # ESTABLISH
    # "earth,sea"
    # "earth,seaside"
    # "earth,seaside,beach"
    sea_way = create_way("earth", "sea", bridge=slash_str)
    seaside_way = create_way("earth", "seaside", bridge=slash_str)
    seaside_beach_way = create_way(seaside_way, "beach", bridge=slash_str)

    # WHEN
    sea_premise = premiseunit_shop(pstate=sea_way, bridge=slash_str)

    # THEN
    sea_fact = factheir_shop(fcontext=sea_way, fstate=sea_way)
    assert sea_premise.is_in_lineage(fact_fstate=sea_fact.fstate)
    seaside_fact = factheir_shop(seaside_beach_way, seaside_beach_way)
    assert sea_premise.is_in_lineage(fact_fstate=seaside_fact.fstate) is False


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolFor_is_rangePremise():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_way = create_way(root_label(), yr_str)
    yr_premise = premiseunit_shop(pstate=yr_way, popen=3, pnigh=13)

    # WHEN / THEN
    yr_fact = factheir_shop(fcontext=yr_way, fopen=5, fnigh=11, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(fcontext=yr_way, fopen=1, fnigh=11, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(fcontext=yr_way, fopen=8, fnigh=17, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(fcontext=yr_way, fopen=0, fnigh=2, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(fcontext=yr_way, fopen=15, fnigh=19, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(fcontext=yr_way, fopen=1, fnigh=19, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    # boundary tests
    yr_fact = factheir_shop(fcontext=yr_way, fopen=13, fnigh=19, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(fcontext=yr_way, fopen=0, fnigh=3, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(fcontext=yr_way, fopen=0, fnigh=0, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False
    yr_fact = factheir_shop(fcontext=yr_way, fopen=3, fnigh=3, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)
    yr_fact = factheir_shop(fcontext=yr_way, fopen=13, fnigh=13, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False
    yr_fact = factheir_shop(fcontext=yr_way, fopen=17, fnigh=17, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(fcontext=yr_way, fopen=20, fnigh=17, fstate=yr_way)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregatePremise():
    # ESTABLISH
    yr_str = "ced_yr"
    yr_way = create_way(root_label(), yr_str)
    yr_premise = premiseunit_shop(pstate=yr_way, pdivisor=5, popen=0, pnigh=0)

    # WHEN / THEN
    yr_fact = factheir_shop(fcontext=yr_way, fstate=yr_way, fopen=5, fnigh=5)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(fcontext=yr_way, fstate=yr_way, fopen=6, fnigh=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(fcontext=yr_way, fstate=yr_way, fopen=4, fnigh=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(fcontext=yr_way, fstate=yr_way, fopen=3, fnigh=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    # ESTABLISH
    yr_premise = premiseunit_shop(pstate=yr_way, pdivisor=5, popen=0, pnigh=2)

    # WHEN / THEN
    yr_fact = factheir_shop(fcontext=yr_way, fstate=yr_way, fopen=2, fnigh=2)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(fcontext=yr_way, fstate=yr_way, fopen=102, fnigh=102)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(fcontext=yr_way, fstate=yr_way, fopen=1, fnigh=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)


def test_PremiseUnitUnit_is_range_or_segregate_ReturnsCorrectBool():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)

    # WHEN / THEN
    wkday_premise = premiseunit_shop(pstate=wkday_way)
    assert wkday_premise._is_range_or_segregate() is False

    wkday_premise = premiseunit_shop(pstate=wkday_way, popen=5, pnigh=13)
    assert wkday_premise._is_range_or_segregate()

    wkday_premise = premiseunit_shop(pstate=wkday_way, pdivisor=17, popen=7, pnigh=7)
    assert wkday_premise._is_range_or_segregate()


def test_PremiseUnitUnit_get_premise_status_Returns_active_Boolean():
    # WHEN assumes fact is in lineage
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_premise = premiseunit_shop(pstate=wkday_way)

    # WHEN / THEN
    wkday_fact = factheir_shop(fcontext=wkday_way, fstate=wkday_way)
    assert wkday_premise._get_active(factheir=wkday_fact)
    # if fact has range but premise does not reqquire range, fact's range does not matter
    wkday_fact = factheir_shop(fcontext=wkday_way, fstate=wkday_way, fopen=0, fnigh=2)
    assert wkday_premise._get_active(factheir=wkday_fact)


def test_PremiseUnitUnit_get_active_Returns_is_range_active_Boolean():
    # ESTABLISH assumes fact is in lineage
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_premise = premiseunit_shop(pstate=wkday_way, popen=3, pnigh=7)

    # WHEN / THEN
    wkday_fact = factheir_shop(fcontext=wkday_way, fstate=wkday_way)
    assert wkday_premise._get_active(factheir=wkday_fact) is False
    wkday_fact = factheir_shop(fcontext=wkday_way, fstate=wkday_way, fopen=0, fnigh=2)
    assert wkday_premise._get_active(factheir=wkday_fact) is False


def test_PremiseUnitUnit_set_status_SetsAttr_status_WhenFactUnitIsNull():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    after_str = "afternoon"
    after_way = create_way(wkday_way, after_str)
    premise_2 = premiseunit_shop(pstate=after_way)
    bud_fact_2 = None
    assert premise_2._status is None

    # WHEN
    premise_2.set_status(x_factheir=bud_fact_2)

    # ESTABLISH
    assert premise_2._status is False


def test_PremiseUnitUnit_set_status_SetsAttr_status_OfSimple():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    bud_fact = factheir_shop(fcontext=wkday_way, fstate=wed_way)
    assert wed_premise._status is None

    # WHEN
    wed_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert wed_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario2():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_after_str = "afternoon"
    wed_after_way = create_way(wed_way, wed_after_str)
    wed_after_premise = premiseunit_shop(pstate=wed_after_way)
    assert wed_after_premise._status is None

    # WHEN
    wed_fact = factheir_shop(fcontext=wkday_way, fstate=wed_way)
    wed_after_premise.set_status(x_factheir=wed_fact)

    # THEN
    assert wed_after_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario3():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_noon_str = "noon"
    wed_noon_way = create_way(wed_way, wed_noon_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    assert wed_premise._status is None

    # WHEN
    noon_fact = factheir_shop(fcontext=wkday_way, fstate=wed_noon_way)
    wed_premise.set_status(x_factheir=noon_fact)

    # THEN
    assert wed_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario4():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    thu_str = "thursday"
    thu_way = create_way(wkday_way, thu_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    thu_fact = factheir_shop(fcontext=wkday_way, fstate=thu_way)
    assert wed_premise._status is None
    assert wed_premise.is_in_lineage(fact_fstate=thu_fact.fstate) is False
    assert thu_fact.fopen is None
    assert thu_fact.fnigh is None

    # WHEN
    wed_premise.set_status(x_factheir=thu_fact)

    # THEN
    assert wed_premise._status is False


def test_PremiseUnit_set_status_SetsAttr_status_Scenario5():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_way = create_way(wkday_way, wed_str)
    wed_cloudy_str = "cloudy"
    wed_cloudy_way = create_way(wed_way, wed_cloudy_str)
    wed_rain_str = "rainy"
    wed_rain_way = create_way(wed_way, wed_rain_str)
    wed_sun_premise = premiseunit_shop(pstate=wed_cloudy_way)
    assert wed_sun_premise._status is None

    # WHEN
    wed_rain_fact = factheir_shop(fcontext=wkday_way, fstate=wed_rain_way)
    wed_sun_premise.set_status(x_factheir=wed_rain_fact)

    # THEN
    assert wed_sun_premise._status is False


def test_PremiseUnit_set_status_SetsStatus_status_ScenarioTime():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    hr24_str = "24hr"
    hr24_way = create_way(timetech_way, hr24_str)
    hr24_premise = premiseunit_shop(pstate=hr24_way, popen=7, pnigh=7)
    assert hr24_premise._status is None

    # WHEN
    range_0_to_8_fact = factheir_shop(hr24_way, hr24_way, fopen=0, fnigh=8)
    hr24_premise.set_status(x_factheir=range_0_to_8_fact)

    # THEN
    assert hr24_premise._status


def test_PremiseUnit_get_task_status_ReturnsObjWhen_status_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    no_range_premise = premiseunit_shop(pstate=hr24_way)
    no_range_premise._status = False

    # WHEN / THEN
    no_range_fact = factheir_shop(fcontext=hr24_way, fstate=hr24_way)
    assert no_range_premise._get_task_status(factheir=no_range_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBool_is_range_True():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    range_5_to_31_premise = premiseunit_shop(pstate=hr24_way, popen=5, pnigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_41_fact = factheir_shop(hr24_way, hr24_way, fopen=7, fnigh=41)
    assert range_5_to_31_premise._get_task_status(range_7_to_41_fact)


def test_PremiseUnit_get_task_status_ReturnsObjWhenBool_is_range_False():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    range_5_to_31_premise = premiseunit_shop(pstate=hr24_way, popen=5, pnigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_21_fact = factheir_shop(hr24_way, hr24_way, fopen=7, fnigh=21)
    assert range_5_to_31_premise._get_task_status(range_7_to_21_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateFalse_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(pstate=hr24_way, pdivisor=5, popen=0, pnigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_3_to_5_fact = factheir_shop(hr24_way, hr24_way, fopen=3, fnigh=5)
    assert o0_n0_d5_premise._get_task_status(range_3_to_5_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateFalse_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(pstate=hr24_way, pdivisor=5, popen=0, pnigh=0)
    o0_n0_d5_premise._status = False

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_way, hr24_way, fopen=5, fnigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateTrue_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(pstate=hr24_way, pdivisor=5, popen=0, pnigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_way, hr24_way, fopen=5, fnigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_fact)


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateTrue_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(pstate=hr24_way, pdivisor=5, popen=0, pnigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_5_fact = factheir_shop(hr24_way, hr24_way, fopen=5, fnigh=5)
    assert o0_n0_d5_premise._get_task_status(factheir=range_5_to_5_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjNotNull():
    # ESTABLISH
    wk_str = "wkdays"
    wk_way = create_way(root_label(), wk_str)
    wed_str = "Wednesday"
    wed_way = create_way(wk_way, wed_str)
    wed_premise = premiseunit_shop(pstate=wed_way)
    wed_premise._status = True

    # ESTABLISH
    factheir = factheir_shop(fcontext=wk_way, fstate=wed_way)

    # THEN
    assert wed_premise._get_task_status(factheir=factheir) is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    range_2_to_7_premise = premiseunit_shop(pstate=hr24_way, popen=2, pnigh=7)
    assert range_2_to_7_premise._status is None
    assert range_2_to_7_premise._task is None

    # WHEN
    range_0_to_5_fact = factheir_shop(hr24_way, hr24_way, fopen=0, fnigh=5)
    range_2_to_7_premise.set_status(x_factheir=range_0_to_5_fact)

    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_way = create_way(root_label(), hr24_str)
    range_2_to_7_premise = premiseunit_shop(pstate=hr24_way, popen=2, pnigh=7)
    range_0_to_8_fact = factheir_shop(hr24_way, hr24_way, fopen=0, fnigh=8)
    assert range_2_to_7_premise._status is None

    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_0_to_8_fact)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task

    # ESTABLISH
    range_3_to_5_fact = factheir_shop(hr24_way, hr24_way, fopen=3, fnigh=5)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_3_to_5_fact)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task is False

    # ESTABLISH
    range_8_to_8_fact = factheir_shop(hr24_way, hr24_way, fopen=8, fnigh=8)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_8_to_8_fact)
    assert range_2_to_7_premise._status is False
    assert range_2_to_7_premise._task is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario03():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    hr24_str = "24hr"
    hr24_way = create_way(timetech_way, hr24_str)
    hr24_premise = premiseunit_shop(pstate=hr24_way, popen=7, pnigh=7)
    assert hr24_premise._status is None

    # WHEN
    bud_fact = factheir_shop(fcontext=hr24_way, fstate=hr24_way, fopen=8, fnigh=10)
    hr24_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert hr24_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusFalse():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_way = create_way(timetech_way, wk_str)
    o1_n1_d6_premise = premiseunit_shop(pstate=wk_way, pdivisor=6, popen=1, pnigh=1)
    assert o1_n1_d6_premise._status is None

    # WHEN
    range_6_to_6_fact = factheir_shop(wk_way, wk_way, fopen=6, fnigh=6)
    o1_n1_d6_premise.set_status(x_factheir=range_6_to_6_fact)

    # THEN
    assert o1_n1_d6_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusTrue():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_way = create_way(timetech_way, wk_str)
    wk_premise = premiseunit_shop(pstate=wk_way, pdivisor=6, popen=1, pnigh=1)
    bud_fact = factheir_shop(fcontext=wk_way, fstate=wk_way, fopen=7, fnigh=7)
    assert wk_premise._status is None

    # WHEN
    wk_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert wk_premise._status


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithDvisiorAndPopen_Pnigh():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_way = create_way(timetech_way, wk_str)
    wk_premise = premiseunit_shop(pstate=wk_way, pdivisor=6, popen=1, pnigh=1)

    # WHEN
    premise_dict = wk_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"pstate": wk_way, "popen": 1, "pnigh": 1, "pdivisor": 6}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithPopenAndPnigh():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_way = create_way(timetech_way, wk_str)
    wk_premise = premiseunit_shop(pstate=wk_way, popen=1, pnigh=4)

    # WHEN
    premise_dict = wk_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"pstate": wk_way, "popen": 1, "pnigh": 4}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOnlyWayTerm():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_way = create_way(timetech_way, wk_str)
    wk_premise = premiseunit_shop(pstate=wk_way)

    # WHEN
    premise_dict = wk_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"pstate": wk_way}
    assert premise_dict == static_dict


def test_PremiseUnit_get_obj_key():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_way = create_way(root_label(), timetech_str)
    wk_str = "ced_wk"
    wk_way = create_way(timetech_way, wk_str)
    wk_premise = premiseunit_shop(pstate=wk_way)

    # WHEN / THEN
    assert wk_premise.get_obj_key() == wk_way


def test_PremiseUnit_find_replace_way_casas():
    # ESTABLISH
    old_root_way = create_way("old_way")
    wkday_str = "wkday"
    wkday_way = create_way(old_root_way, wkday_str)
    sunday_str = "Sunday"
    old_sunday_way = create_way(wkday_way, sunday_str)
    sunday_premise = premiseunit_shop(pstate=old_sunday_way)
    print(sunday_premise)
    assert sunday_premise.pstate == old_sunday_way

    # WHEN
    new_way = create_way("fun")
    sunday_premise.find_replace_way(old_way=old_root_way, new_way=new_way)

    # THEN
    new_wkday_way = create_way(new_way, wkday_str)
    new_sunday_way = create_way(new_wkday_way, sunday_str)
    assert sunday_premise.pstate == new_sunday_way


def test_PremiseUnits_get_from_dict_ReturnsCompleteObj():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    static_dict = {
        wkday_way: {
            "pstate": wkday_way,
            "popen": 1,
            "pnigh": 30,
            "pdivisor": 5,
        }
    }

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    wkday_premise = premises_dict.get(wkday_way)
    assert wkday_premise == premiseunit_shop(wkday_way, 1, 30, pdivisor=5)


def test_PremiseUnits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    static_dict = {wkday_way: {"pstate": wkday_way}}

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    wkday_premise = premises_dict.get(wkday_way)
    assert wkday_premise == premiseunit_shop(wkday_way)


def test_PremiseUnitsUnit_set_bridge_SetsAttrsCorrectly():
    # ESTABLISH
    wk_str = "wkday"
    sun_str = "Sunday"
    slash_str = "/"
    slash_wk_way = create_way(root_label(), wk_str, bridge=slash_str)
    slash_sun_way = create_way(slash_wk_way, sun_str, bridge=slash_str)
    sun_premiseunit = premiseunit_shop(slash_sun_way, bridge=slash_str)
    assert sun_premiseunit.bridge == slash_str
    assert sun_premiseunit.pstate == slash_sun_way

    # WHEN
    star_str = "*"
    sun_premiseunit.set_bridge(new_bridge=star_str)

    # THEN
    assert sun_premiseunit.bridge == star_str
    star_wk_way = create_way(root_label(), wk_str, bridge=star_str)
    star_sun_way = create_way(star_wk_way, sun_str, bridge=star_str)
    assert sun_premiseunit.pstate == star_sun_way


def test_way_find_replace_way_key_dict_ReturnsCorrectPremisesUnit_Scenario1():
    # ESTABLISH
    casa_way = create_way(root_label(), "casa")
    old_seasons_way = create_way(casa_way, "seasons")
    old_premise_x = premiseunit_shop(pstate=old_seasons_way)
    old_premises_x = {old_premise_x.pstate: old_premise_x}

    assert old_premises_x.get(old_seasons_way) == old_premise_x

    # WHEN
    new_seasons_way = create_way(casa_way, "kookies")
    new_premises_x = find_replace_way_key_dict(
        dict_x=old_premises_x, old_way=old_seasons_way, new_way=new_seasons_way
    )
    new_premise_x = premiseunit_shop(pstate=new_seasons_way)

    assert new_premises_x.get(new_seasons_way) == new_premise_x
    assert new_premises_x.get(old_seasons_way) is None


def test_way_find_replace_way_key_dict_ReturnsCorrectPremisesUnit_Scenario2():
    # ESTABLISH
    old_fisc_label = "El Paso"
    casa_str = "casa"
    seasons_str = "seasons"
    old_casa_way = create_way(old_fisc_label, casa_str)
    old_seasons_way = create_way(old_casa_way, seasons_str)
    old_premiseunit = premiseunit_shop(pstate=old_seasons_way)
    old_premiseunits = {old_premiseunit.pstate: old_premiseunit}
    assert old_premiseunits.get(old_seasons_way) == old_premiseunit

    # WHEN
    new_fisc_label = "Austin"
    new_casa_way = create_way(new_fisc_label, casa_str)
    new_seasons_way = create_way(new_casa_way, seasons_str)
    new_premise_ways = find_replace_way_key_dict(
        dict_x=old_premiseunits, old_way=old_seasons_way, new_way=new_seasons_way
    )
    new_premiseunit = premiseunit_shop(pstate=new_seasons_way)

    assert new_premise_ways.get(new_seasons_way) == new_premiseunit
    assert new_premise_ways.get(old_seasons_way) is None
