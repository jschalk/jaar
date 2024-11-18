from src.f02_bud.reason_item import (
    PremiseUnit,
    premiseunit_shop,
    factheir_shop,
    premiseunit_shop,
    premises_get_from_dict,
)
from src.f01_road.road import (
    get_default_fiscal_id_roadnode as root_label,
    create_road,
    find_replace_road_key_dict,
)


def test_PremiseUnit_Exists():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)
    email_str = "check email"
    email_road = create_road(casa_road, email_str)

    # WHEN
    email_premise = PremiseUnit(need=email_road)

    # THEN
    assert email_premise.need == email_road
    assert email_premise.open is None
    assert email_premise.nigh is None
    assert email_premise.divisor is None
    assert email_premise._status is None
    assert email_premise._task is None
    assert email_premise.wall is None


def test_premiseunit_shop_ReturnsCorrectObj():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)
    email_str = "check email"
    email_road = create_road(casa_road, email_str)

    # WHEN
    email_premise = premiseunit_shop(need=email_road)

    # THEN
    assert email_premise.need == email_road


def test_PremiseUnit_clear_status_CorrectlySetsAttrs():
    # WHEN
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)
    casa_premise = premiseunit_shop(need=casa_road)
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
    casa_road = create_road(root_label(), casa_str)

    # WHEN
    casa_premise = premiseunit_shop(need=casa_road, open=1, nigh=3)
    # THEN
    assert casa_premise._is_range()

    # WHEN
    casa_premise = premiseunit_shop(need=casa_road)
    # THEN
    assert casa_premise._is_range() is False

    # WHEN
    casa_premise = premiseunit_shop(need=casa_road, divisor=5, open=3, nigh=3)
    # THEN
    assert casa_premise._is_range() is False


def test_PremiseUnit_is_segregate_CorrectlyIdentifiesSegregateStatus():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)

    # WHEN
    casa_premise = premiseunit_shop(need=casa_road, open=1, nigh=3)
    # THEN
    assert casa_premise._is_segregate() is False

    # WHEN
    casa_premise = premiseunit_shop(need=casa_road)
    # THEN
    assert casa_premise._is_segregate() is False

    # WHEN
    casa_premise = premiseunit_shop(need=casa_road, divisor=5, open=3, nigh=3)
    # THEN
    assert casa_premise._is_segregate()


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineage():
    # ESTABLISH
    nation_road = create_road(root_label(), "Nation-States")
    usa_road = create_road(nation_road, "USA")
    texas_road = create_road(usa_road, "Texas")
    idaho_road = create_road(usa_road, "Idaho")
    texas_fact = factheir_shop(base=usa_road, pick=texas_road)

    # WHEN / THEN
    texas_premise = premiseunit_shop(need=texas_road)
    assert texas_premise.is_in_lineage(fact_pick=texas_fact.pick)

    # WHEN / THEN
    idaho_premise = premiseunit_shop(need=idaho_road)
    assert idaho_premise.is_in_lineage(fact_pick=texas_fact.pick) is False

    # WHEN / THEN
    usa_premise = premiseunit_shop(need=usa_road)
    assert usa_premise.is_in_lineage(fact_pick=texas_fact.pick)

    # ESTABLISH
    sea_road = create_road("earth", "sea")  # "earth,sea"
    sea_premise = premiseunit_shop(need=sea_road)

    # THEN
    sea_fact = factheir_shop(base=sea_road, pick=sea_road)
    assert sea_premise.is_in_lineage(fact_pick=sea_fact.pick)
    seaside_road = create_road("earth", "seaside")  # "earth,seaside,beach"
    seaside_beach_road = create_road(seaside_road, "beach")  # "earth,seaside,beach"
    seaside_fact = factheir_shop(seaside_beach_road, seaside_beach_road)
    assert sea_premise.is_in_lineage(fact_pick=seaside_fact.pick) is False


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineageWithNonDefaultWall():
    # ESTABLISH
    slash_str = "/"
    nation_road = create_road(root_label(), "Nation-States", wall=slash_str)
    usa_road = create_road(nation_road, "USA", wall=slash_str)
    texas_road = create_road(usa_road, "Texas", wall=slash_str)
    idaho_road = create_road(usa_road, "Idaho", wall=slash_str)

    # WHEN
    texas_fact = factheir_shop(base=usa_road, pick=texas_road)

    # THEN
    texas_premise = premiseunit_shop(need=texas_road, wall=slash_str)
    assert texas_premise.is_in_lineage(fact_pick=texas_fact.pick)

    idaho_premise = premiseunit_shop(need=idaho_road, wall=slash_str)
    assert idaho_premise.is_in_lineage(fact_pick=texas_fact.pick) is False

    usa_premise = premiseunit_shop(need=usa_road, wall=slash_str)
    print(f"  {usa_premise.need=}")
    print(f"{texas_fact.pick=}")
    assert usa_premise.is_in_lineage(fact_pick=texas_fact.pick)

    # ESTABLISH
    # "earth,sea"
    # "earth,seaside"
    # "earth,seaside,beach"
    sea_road = create_road("earth", "sea", wall=slash_str)
    seaside_road = create_road("earth", "seaside", wall=slash_str)
    seaside_beach_road = create_road(seaside_road, "beach", wall=slash_str)

    # WHEN
    sea_premise = premiseunit_shop(need=sea_road, wall=slash_str)

    # THEN
    sea_fact = factheir_shop(base=sea_road, pick=sea_road)
    assert sea_premise.is_in_lineage(fact_pick=sea_fact.pick)
    seaside_fact = factheir_shop(seaside_beach_road, seaside_beach_road)
    assert sea_premise.is_in_lineage(fact_pick=seaside_fact.pick) is False


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolFor_is_rangePremise():
    # ESTABLISH
    yr_str = "ced_year"
    yr_road = create_road(root_label(), yr_str)
    yr_premise = premiseunit_shop(need=yr_road, open=3, nigh=13)

    # WHEN / THEN
    yr_fact = factheir_shop(base=yr_road, fopen=5, fnigh=11, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(base=yr_road, fopen=1, fnigh=11, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(base=yr_road, fopen=8, fnigh=17, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(base=yr_road, fopen=0, fnigh=2, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, fopen=15, fnigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, fopen=1, fnigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    # boundary tests
    yr_fact = factheir_shop(base=yr_road, fopen=13, fnigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, fopen=0, fnigh=3, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregatePremise():
    # ESTABLISH
    yr_str = "ced_year"
    yr_road = create_road(root_label(), yr_str)
    yr_premise = premiseunit_shop(need=yr_road, divisor=5, open=0, nigh=0)

    # WHEN / THEN
    yr_fact = factheir_shop(base=yr_road, pick=yr_road, fopen=5, fnigh=5)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, fopen=6, fnigh=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, fopen=4, fnigh=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, fopen=3, fnigh=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    # ESTABLISH
    yr_premise = premiseunit_shop(need=yr_road, divisor=5, open=0, nigh=2)

    # WHEN / THEN
    yr_fact = factheir_shop(base=yr_road, pick=yr_road, fopen=2, fnigh=2)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, fopen=102, fnigh=102)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, fopen=1, fnigh=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact)


def test_PremiseUnitUnit_is_range_or_segregate_ReturnsCorrectBool():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)

    # WHEN / THEN
    wkday_premise = premiseunit_shop(need=wkday_road)
    assert wkday_premise._is_range_or_segregate() is False

    wkday_premise = premiseunit_shop(need=wkday_road, open=5, nigh=13)
    assert wkday_premise._is_range_or_segregate()

    wkday_premise = premiseunit_shop(need=wkday_road, divisor=17, open=7, nigh=7)
    assert wkday_premise._is_range_or_segregate()


def test_PremiseUnitUnit_get_premise_status_Returns_active_Boolean():
    # WHEN assumes fact is in lineage
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wkday_premise = premiseunit_shop(need=wkday_road)

    # WHEN / THEN
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_premise._get_active(factheir=wkday_fact)
    # if fact has range but premise does not reqquire range, fact's range does not matter
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road, fopen=0, fnigh=2)
    assert wkday_premise._get_active(factheir=wkday_fact)


def test_PremiseUnitUnit_get_active_Returns_is_range_active_Boolean():
    # ESTABLISH assumes fact is in lineage
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wkday_premise = premiseunit_shop(need=wkday_road, open=3, nigh=7)

    # WHEN / THEN
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_premise._get_active(factheir=wkday_fact) is False
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road, fopen=0, fnigh=2)
    assert wkday_premise._get_active(factheir=wkday_fact) is False


def test_PremiseUnitUnit_set_status_SetsAttr_status_WhenFactUnitIsNull():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    after_str = "afternoon"
    after_road = create_road(wkday_road, after_str)
    premise_2 = premiseunit_shop(need=after_road)
    bud_fact_2 = None
    assert premise_2._status is None

    # WHEN
    premise_2.set_status(x_factheir=bud_fact_2)

    # ESTABLISH
    assert premise_2._status is False


def test_PremiseUnitUnit_set_status_SetsAttr_status_OfSimple():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_premise = premiseunit_shop(need=wed_road)
    bud_fact = factheir_shop(base=wkday_road, pick=wed_road)
    assert wed_premise._status is None

    # WHEN
    wed_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert wed_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario2():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_after_str = "afternoon"
    wed_after_road = create_road(wed_road, wed_after_str)
    wed_after_premise = premiseunit_shop(need=wed_after_road)
    assert wed_after_premise._status is None

    # WHEN
    wed_fact = factheir_shop(base=wkday_road, pick=wed_road)
    wed_after_premise.set_status(x_factheir=wed_fact)

    # THEN
    assert wed_after_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario3():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_noon_str = "noon"
    wed_noon_road = create_road(wed_road, wed_noon_str)
    wed_premise = premiseunit_shop(need=wed_road)
    assert wed_premise._status is None

    # WHEN
    noon_fact = factheir_shop(base=wkday_road, pick=wed_noon_road)
    wed_premise.set_status(x_factheir=noon_fact)

    # THEN
    assert wed_premise._status


def test_PremiseUnit_set_status_SetsAttr_status_Scenario4():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    thu_str = "thursday"
    thu_road = create_road(wkday_road, thu_str)
    wed_premise = premiseunit_shop(need=wed_road)
    thu_fact = factheir_shop(base=wkday_road, pick=thu_road)
    assert wed_premise._status is None
    assert wed_premise.is_in_lineage(fact_pick=thu_fact.pick) is False
    assert thu_fact.fopen is None
    assert thu_fact.fnigh is None

    # WHEN
    wed_premise.set_status(x_factheir=thu_fact)

    # THEN
    assert wed_premise._status is False


def test_PremiseUnit_set_status_SetsAttr_status_Scenario5():
    # ESTABLISH
    wkday_str = "weekday"
    wkday_road = create_road(root_label(), wkday_str)
    wed_str = "wednesday"
    wed_road = create_road(wkday_road, wed_str)
    wed_cloudy_str = "cloudy"
    wed_cloudy_road = create_road(wed_road, wed_cloudy_str)
    wed_rain_str = "rainy"
    wed_rain_road = create_road(wed_road, wed_rain_str)
    wed_sun_premise = premiseunit_shop(need=wed_cloudy_road)
    assert wed_sun_premise._status is None

    # WHEN
    wed_rain_fact = factheir_shop(base=wkday_road, pick=wed_rain_road)
    wed_sun_premise.set_status(x_factheir=wed_rain_fact)

    # THEN
    assert wed_sun_premise._status is False


def test_PremiseUnit_set_status_SetsStatus_status_ScenarioTime():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    hr24_str = "24hr"
    hr24_road = create_road(timetech_road, hr24_str)
    hr24_premise = premiseunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_premise._status is None

    # WHEN
    range_0_to_8_fact = factheir_shop(hr24_road, hr24_road, fopen=0, fnigh=8)
    hr24_premise.set_status(x_factheir=range_0_to_8_fact)

    # THEN
    assert hr24_premise._status


def test_PremiseUnit_get_task_status_ReturnsObjWhen_status_IsFalse():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    no_range_premise = premiseunit_shop(need=hr24_road)
    no_range_premise._status = False

    # WHEN / THEN
    no_range_fact = factheir_shop(base=hr24_road, pick=hr24_road)
    assert no_range_premise._get_task_status(factheir=no_range_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBool_is_range_True():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    range_5_to_31_premise = premiseunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_41_fact = factheir_shop(hr24_road, hr24_road, fopen=7, fnigh=41)
    assert range_5_to_31_premise._get_task_status(range_7_to_41_fact)


def test_PremiseUnit_get_task_status_ReturnsObjWhenBool_is_range_False():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    range_5_to_31_premise = premiseunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_21_fact = factheir_shop(hr24_road, hr24_road, fopen=7, fnigh=21)
    assert range_5_to_31_premise._get_task_status(range_7_to_21_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateFalse_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_3_to_5_fact = factheir_shop(hr24_road, hr24_road, fopen=3, fnigh=5)
    assert o0_n0_d5_premise._get_task_status(range_3_to_5_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateFalse_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = False

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_road, hr24_road, fopen=5, fnigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateTrue_01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_road, hr24_road, fopen=5, fnigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_fact)


def test_PremiseUnit_get_task_status_ReturnsObjWhenBoolSegregateTrue_02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_5_fact = factheir_shop(hr24_road, hr24_road, fopen=5, fnigh=5)
    assert o0_n0_d5_premise._get_task_status(factheir=range_5_to_5_fact) is False


def test_PremiseUnit_get_task_status_ReturnsObjNotNull():
    # ESTABLISH
    week_str = "weekdays"
    week_road = create_road(root_label(), week_str)
    wed_str = "Wednesday"
    wed_road = create_road(week_road, wed_str)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = True

    # ESTABLISH
    factheir = factheir_shop(base=week_road, pick=wed_road)

    # THEN
    assert wed_premise._get_task_status(factheir=factheir) is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario01():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    range_2_to_7_premise = premiseunit_shop(need=hr24_road, open=2, nigh=7)
    assert range_2_to_7_premise._status is None
    assert range_2_to_7_premise._task is None

    # WHEN
    range_0_to_5_fact = factheir_shop(hr24_road, hr24_road, fopen=0, fnigh=5)
    range_2_to_7_premise.set_status(x_factheir=range_0_to_5_fact)

    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario02():
    # ESTABLISH
    hr24_str = "24hr"
    hr24_road = create_road(root_label(), hr24_str)
    range_2_to_7_premise = premiseunit_shop(need=hr24_road, open=2, nigh=7)
    range_0_to_8_fact = factheir_shop(hr24_road, hr24_road, fopen=0, fnigh=8)
    assert range_2_to_7_premise._status is None

    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_0_to_8_fact)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task

    # ESTABLISH
    range_3_to_5_fact = factheir_shop(hr24_road, hr24_road, fopen=3, fnigh=5)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_3_to_5_fact)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task is False

    # ESTABLISH
    range_8_to_8_fact = factheir_shop(hr24_road, hr24_road, fopen=8, fnigh=8)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_8_to_8_fact)
    assert range_2_to_7_premise._status is False
    assert range_2_to_7_premise._task is False


def test_PremiseUnit_set_status_SetsAttrs_Scenario03():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    hr24_str = "24hr"
    hr24_road = create_road(timetech_road, hr24_str)
    hr24_premise = premiseunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_premise._status is None

    # WHEN
    bud_fact = factheir_shop(base=hr24_road, pick=hr24_road, fopen=8, fnigh=10)
    hr24_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert hr24_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusFalse():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    week_str = "ced_week"
    week_road = create_road(timetech_road, week_str)
    o1_n1_d6_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    assert o1_n1_d6_premise._status is None

    # WHEN
    range_6_to_6_fact = factheir_shop(week_road, week_road, fopen=6, fnigh=6)
    o1_n1_d6_premise.set_status(x_factheir=range_6_to_6_fact)

    # THEN
    assert o1_n1_d6_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusTrue():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    week_str = "ced_week"
    week_road = create_road(timetech_road, week_str)
    week_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    bud_fact = factheir_shop(base=week_road, pick=week_road, fopen=7, fnigh=7)
    assert week_premise._status is None

    # WHEN
    week_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert week_premise._status


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithDvisiorAndOpen_Nigh():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    week_str = "ced_week"
    week_road = create_road(timetech_road, week_str)
    week_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"need": week_road, "open": 1, "nigh": 1, "divisor": 6}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOpenAndNigh():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    week_str = "ced_week"
    week_road = create_road(timetech_road, week_str)
    week_premise = premiseunit_shop(need=week_road, open=1, nigh=4)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"need": week_road, "open": 1, "nigh": 4}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOnlyRoadUnit():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    week_str = "ced_week"
    week_road = create_road(timetech_road, week_str)
    week_premise = premiseunit_shop(need=week_road)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict is not None
    static_dict = {"need": week_road}
    assert premise_dict == static_dict


def test_PremiseUnit_get_obj_key():
    # ESTABLISH
    timetech_str = "timetech"
    timetech_road = create_road(root_label(), timetech_str)
    week_str = "ced_week"
    week_road = create_road(timetech_road, week_str)
    week_premise = premiseunit_shop(need=week_road)

    # WHEN / THEN
    assert week_premise.get_obj_key() == week_road


def test_PremiseUnit_find_replace_road_casas():
    # ESTABLISH
    old_root_road = root_label()
    weekday_str = "weekday"
    weekday_road = create_road(root_label(), weekday_str)
    sunday_str = "Sunday"
    old_sunday_road = create_road(weekday_road, sunday_str)
    sunday_premise = premiseunit_shop(need=old_sunday_road)
    print(sunday_premise)
    assert sunday_premise.need == old_sunday_road

    # WHEN
    new_road = "fun"
    sunday_premise.find_replace_road(old_road=old_root_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_str)
    new_sunday_road = create_road(new_weekday_road, sunday_str)

    # THEN
    assert sunday_premise.need == new_sunday_road


def test_PremiseUnits_get_from_dict_ReturnsCompleteObj():
    # ESTABLISH
    weekday_str = "weekdays"
    weekday_road = create_road(root_label(), weekday_str)
    static_dict = {
        weekday_road: {
            "need": weekday_road,
            "open": 1,
            "nigh": 30,
            "divisor": 5,
        }
    }

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    weekday_premise = premises_dict.get(weekday_road)
    assert weekday_premise == premiseunit_shop(weekday_road, 1, 30, divisor=5)


def test_PremiseUnits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    weekday_str = "weekdays"
    weekday_road = create_road(root_label(), weekday_str)
    static_dict = {weekday_road: {"need": weekday_road}}

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    weekday_premise = premises_dict.get(weekday_road)
    assert weekday_premise == premiseunit_shop(weekday_road)


def test_PremiseUnitsUnit_set_wall_SetsAttrsCorrectly():
    # ESTABLISH
    week_str = "weekday"
    sun_str = "Sunday"
    slash_str = "/"
    slash_week_road = create_road(root_label(), week_str, wall=slash_str)
    slash_sun_road = create_road(slash_week_road, sun_str, wall=slash_str)
    sun_premiseunit = premiseunit_shop(slash_sun_road, wall=slash_str)
    assert sun_premiseunit.wall == slash_str
    assert sun_premiseunit.need == slash_sun_road

    # WHEN
    star_str = "*"
    sun_premiseunit.set_wall(new_wall=star_str)

    # THEN
    assert sun_premiseunit.wall == star_str
    star_week_road = create_road(root_label(), week_str, wall=star_str)
    star_sun_road = create_road(star_week_road, sun_str, wall=star_str)
    assert sun_premiseunit.need == star_sun_road


def test_road_find_replace_road_key_dict_ReturnsCorrectPremisesUnit_Scenario1():
    # ESTABLISH
    casa_road = create_road(root_label(), "casa")
    old_seasons_road = create_road(casa_road, "seasons")
    old_premise_x = premiseunit_shop(need=old_seasons_road)
    old_premises_x = {old_premise_x.need: old_premise_x}

    assert old_premises_x.get(old_seasons_road) == old_premise_x

    # WHEN
    new_seasons_road = create_road(casa_road, "kookies")
    new_premises_x = find_replace_road_key_dict(
        dict_x=old_premises_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_premise_x = premiseunit_shop(need=new_seasons_road)

    assert new_premises_x.get(new_seasons_road) == new_premise_x
    assert new_premises_x.get(old_seasons_road) is None


def test_road_find_replace_road_key_dict_ReturnsCorrectPremisesUnit_Scenario2():
    # ESTABLISH
    old_fiscal_id = "El Paso"
    casa_str = "casa"
    seasons_str = "seasons"
    old_casa_road = create_road(old_fiscal_id, casa_str)
    old_seasons_road = create_road(old_casa_road, seasons_str)
    old_premiseunit = premiseunit_shop(need=old_seasons_road)
    old_premiseunits = {old_premiseunit.need: old_premiseunit}
    assert old_premiseunits.get(old_seasons_road) == old_premiseunit

    # WHEN
    new_fiscal_id = "Austin"
    new_casa_road = create_road(new_fiscal_id, casa_str)
    new_seasons_road = create_road(new_casa_road, seasons_str)
    new_premise_roads = find_replace_road_key_dict(
        dict_x=old_premiseunits, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_premiseunit = premiseunit_shop(need=new_seasons_road)

    assert new_premise_roads.get(new_seasons_road) == new_premiseunit
    assert new_premise_roads.get(old_seasons_road) is None
