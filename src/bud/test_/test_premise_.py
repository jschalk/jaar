from src.bud.reason_idea import (
    PremiseUnit,
    premiseunit_shop,
    factheir_shop,
    premiseunit_shop,
    premises_get_from_dict,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    find_replace_road_key_dict,
)
from pytest import raises as pytest_raises


def test_PremiseUnit_Exists():
    # ESTABLISH
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    email_text = "check email"
    email_road = create_road(casa_road, email_text)

    # WHEN
    email_premise = PremiseUnit(need=email_road)

    # THEN
    assert email_premise.need == email_road
    assert email_premise.open is None
    assert email_premise.nigh is None
    assert email_premise.divisor is None
    assert email_premise._status is None
    assert email_premise._task is None
    assert email_premise.delimiter is None


def test_premiseunit_shop_ReturnsCorrectObj():
    # ESTABLISH
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    email_text = "check email"
    email_road = create_road(casa_road, email_text)

    # WHEN
    email_premise = premiseunit_shop(need=email_road)

    # THEN
    assert email_premise.need == email_road


def test_PremiseUnit_clear_status_CorrectlySetsAttrs():
    # WHEN
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
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


def test_PremiseUnit_is_range_CorrectlyIdentifiesRangeStatus():
    # ESTABLISH
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)

    # WHEN
    casa_premise = premiseunit_shop(need=casa_road, open=1, nigh=3)
    # THEN
    assert casa_premise._is_range() == True

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
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)

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
    assert casa_premise._is_segregate() == True


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


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineageWithNonDefaultDelimiter():
    # ESTABLISH
    slash_text = "/"
    nation_road = create_road(root_label(), "Nation-States", delimiter=slash_text)
    usa_road = create_road(nation_road, "USA", delimiter=slash_text)
    texas_road = create_road(usa_road, "Texas", delimiter=slash_text)
    idaho_road = create_road(usa_road, "Idaho", delimiter=slash_text)

    # WHEN
    texas_fact = factheir_shop(base=usa_road, pick=texas_road)

    # THEN
    texas_premise = premiseunit_shop(need=texas_road, delimiter=slash_text)
    assert texas_premise.is_in_lineage(fact_pick=texas_fact.pick)

    idaho_premise = premiseunit_shop(need=idaho_road, delimiter=slash_text)
    assert idaho_premise.is_in_lineage(fact_pick=texas_fact.pick) is False

    usa_premise = premiseunit_shop(need=usa_road, delimiter=slash_text)
    print(f"  {usa_premise.need=}")
    print(f"{texas_fact.pick=}")
    assert usa_premise.is_in_lineage(fact_pick=texas_fact.pick)

    # ESTABLISH
    # "earth,sea"
    # "earth,seaside"
    # "earth,seaside,beach"
    sea_road = create_road("earth", "sea", delimiter=slash_text)
    seaside_road = create_road("earth", "seaside", delimiter=slash_text)
    seaside_beach_road = create_road(seaside_road, "beach", delimiter=slash_text)

    # WHEN
    sea_premise = premiseunit_shop(need=sea_road, delimiter=slash_text)

    # THEN
    sea_fact = factheir_shop(base=sea_road, pick=sea_road)
    assert sea_premise.is_in_lineage(fact_pick=sea_fact.pick)
    seaside_fact = factheir_shop(seaside_beach_road, seaside_beach_road)
    assert sea_premise.is_in_lineage(fact_pick=seaside_fact.pick) is False


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForRangePremise():
    # ESTABLISH
    yr_text = "ced_year"
    yr_road = create_road(root_label(), yr_text)
    yr_premise = premiseunit_shop(need=yr_road, open=3, nigh=13)

    # WHEN / THEN
    yr_fact = factheir_shop(base=yr_road, open=5, nigh=11, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True

    yr_fact = factheir_shop(base=yr_road, open=1, nigh=11, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True

    yr_fact = factheir_shop(base=yr_road, open=8, nigh=17, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True

    yr_fact = factheir_shop(base=yr_road, open=0, nigh=2, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, open=15, nigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, open=1, nigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True

    # boundary tests
    yr_fact = factheir_shop(base=yr_road, open=13, nigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, open=0, nigh=3, pick=yr_road)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregatePremise():
    # ESTABLISH
    yr_text = "ced_year"
    yr_road = create_road(root_label(), yr_text)
    yr_premise = premiseunit_shop(need=yr_road, divisor=5, open=0, nigh=0)

    # WHEN / THEN
    yr_fact = factheir_shop(base=yr_road, pick=yr_road, open=5, nigh=5)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, open=6, nigh=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, open=4, nigh=6)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, open=3, nigh=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    # ESTABLISH
    yr_premise = premiseunit_shop(need=yr_road, divisor=5, open=0, nigh=2)

    # WHEN / THEN
    yr_fact = factheir_shop(base=yr_road, pick=yr_road, open=2, nigh=2)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, open=102, nigh=102)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) is False

    yr_fact = factheir_shop(base=yr_road, pick=yr_road, open=1, nigh=4)
    assert yr_premise._get_range_segregate_status(factheir=yr_fact) == True


def test_PremiseUnitUnit_is_range_or_segregate_ReturnsCorrectBool():
    # ESTABLISH
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)

    # WHEN / THEN
    wkday_premise = premiseunit_shop(need=wkday_road)
    assert wkday_premise._is_range_or_segregate() is False

    wkday_premise = premiseunit_shop(need=wkday_road, open=5, nigh=13)
    assert wkday_premise._is_range_or_segregate() == True

    wkday_premise = premiseunit_shop(need=wkday_road, divisor=17, open=7, nigh=7)
    assert wkday_premise._is_range_or_segregate() == True


def test_PremiseUnitUnit_get_premise_status_ReturnsCorrect_active():
    # WHEN assumes fact is in lineage
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_premise = premiseunit_shop(need=wkday_road)

    # WHEN / THEN
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_premise._get_active(factheir=wkday_fact) == True
    # if fact has range but premise does not reqquire range, fact's range does not matter
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road, open=0, nigh=2)
    assert wkday_premise._get_active(factheir=wkday_fact) == True


def test_PremiseUnitUnit_get_active_returnsCorrectRanged_active():
    # ESTABLISH assumes fact is in lineage
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_premise = premiseunit_shop(need=wkday_road, open=3, nigh=7)

    # WHEN / THEN
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_premise._get_active(factheir=wkday_fact) is False
    wkday_fact = factheir_shop(base=wkday_road, pick=wkday_road, open=0, nigh=2)
    assert wkday_premise._get_active(factheir=wkday_fact) is False


def test_PremiseUnitUnit_set_status_CorrectlySets_status_WhenFactUnitIsNull():
    # ESTABLISH
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    after_text = "afternoon"
    after_road = create_road(wkday_road, after_text)
    premise_2 = premiseunit_shop(need=after_road)
    bud_fact_2 = None
    assert premise_2._status is None

    # WHEN
    premise_2.set_status(x_factheir=bud_fact_2)

    # ESTABLISH
    assert premise_2._status is False


def test_PremiseUnitUnit_set_status_CorrectlySetsStatusOfSimple():
    # ESTABLISH
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_premise = premiseunit_shop(need=wed_road)
    bud_fact = factheir_shop(base=wkday_road, pick=wed_road)
    assert wed_premise._status is None

    # WHEN
    wed_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert wed_premise._status == True


def test_PremiseUnit_set_status_CorrectlySetsStatus_2():
    # ESTABLISH
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_after_text = "afternoon"
    wed_after_road = create_road(wed_road, wed_after_text)
    wed_after_premise = premiseunit_shop(need=wed_after_road)
    assert wed_after_premise._status is None

    # WHEN
    wed_fact = factheir_shop(base=wkday_road, pick=wed_road)
    wed_after_premise.set_status(x_factheir=wed_fact)

    # THEN
    assert wed_after_premise._status == True


def test_PremiseUnit_set_status_CorrectlySetsStatus_3():
    # ESTABLISH
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_noon_text = "noon"
    wed_noon_road = create_road(wed_road, wed_noon_text)
    wed_premise = premiseunit_shop(need=wed_road)
    assert wed_premise._status is None

    # WHEN
    noon_fact = factheir_shop(base=wkday_road, pick=wed_noon_road)
    wed_premise.set_status(x_factheir=noon_fact)

    # THEN
    assert wed_premise._status == True


def test_PremiseUnit_set_status_CorrectlySetsStatus_4():
    # ESTABLISH
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    thu_text = "thursday"
    thu_road = create_road(wkday_road, thu_text)
    wed_premise = premiseunit_shop(need=wed_road)
    thu_fact = factheir_shop(base=wkday_road, pick=thu_road)
    assert wed_premise._status is None
    assert wed_premise.is_in_lineage(fact_pick=thu_fact.pick) is False
    assert thu_fact.open is None
    assert thu_fact.nigh is None

    # WHEN
    wed_premise.set_status(x_factheir=thu_fact)

    # THEN
    assert wed_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetsStatus_5():
    # ESTABLISH
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_sun_text = "sunny"
    wed_sun_road = create_road(wed_road, wed_sun_text)
    wed_rain_text = "rainy"
    wed_rain_road = create_road(wed_road, wed_rain_text)
    wed_sun_premise = premiseunit_shop(need=wed_sun_road)
    assert wed_sun_premise._status is None

    # WHEN
    wed_rain_fact = factheir_shop(base=wkday_road, pick=wed_rain_road)
    wed_sun_premise.set_status(x_factheir=wed_rain_fact)

    # THEN
    assert wed_sun_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeStatusTrue():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    hr24_text = "24hr"
    hr24_road = create_road(timetech_road, hr24_text)
    hr24_premise = premiseunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_premise._status is None

    # WHEN
    range_0_to_8_fact = factheir_shop(hr24_road, hr24_road, open=0, nigh=8)
    hr24_premise.set_status(x_factheir=range_0_to_8_fact)

    # THEN
    assert hr24_premise._status == True


def test_PremiseUnit_set_task_CorrectlySetsTaskBool_01():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    no_range_premise = premiseunit_shop(need=hr24_road)
    no_range_premise._status = False

    # WHEN / THEN
    no_range_fact = factheir_shop(base=hr24_road, pick=hr24_road)
    assert no_range_premise._get_task_status(factheir=no_range_fact) is False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolRangeTrue():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_5_to_31_premise = premiseunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_41_fact = factheir_shop(hr24_road, hr24_road, open=7, nigh=41)
    assert range_5_to_31_premise._get_task_status(range_7_to_41_fact) == True


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolRangeFalse():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_5_to_31_premise = premiseunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_21_fact = factheir_shop(hr24_road, hr24_road, open=7, nigh=21)
    assert range_5_to_31_premise._get_task_status(range_7_to_21_fact) is False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateFalse_01():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_3_to_5_fact = factheir_shop(hr24_road, hr24_road, open=3, nigh=5)
    assert o0_n0_d5_premise._get_task_status(range_3_to_5_fact) is False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateFalse_03():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = False

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_road, hr24_road, open=5, nigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_fact) is False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateTrue_01():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_7_fact = factheir_shop(hr24_road, hr24_road, open=5, nigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_fact) == True


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateTrue_02():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_5_fact = factheir_shop(hr24_road, hr24_road, open=5, nigh=5)
    assert o0_n0_d5_premise._get_task_status(factheir=range_5_to_5_fact) is False


def test_PremiseUnit_set_task_NotNull():
    # ESTABLISH
    week_text = "weekdays"
    week_road = create_road(root_label(), week_text)
    wed_text = "Wednesday"
    wed_road = create_road(week_road, wed_text)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = True

    # ESTABLISH
    factheir = factheir_shop(base=week_road, pick=wed_road)

    # THEN
    assert wed_premise._get_task_status(factheir=factheir) is False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeTaskTrue_v1():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_2_to_7_premise = premiseunit_shop(need=hr24_road, open=2, nigh=7)
    assert range_2_to_7_premise._status is None
    assert range_2_to_7_premise._task is None

    # WHEN
    range_0_to_5_fact = factheir_shop(hr24_road, hr24_road, open=0, nigh=5)
    range_2_to_7_premise.set_status(x_factheir=range_0_to_5_fact)

    # THEN
    assert range_2_to_7_premise._status == True
    assert range_2_to_7_premise._task is False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeTaskTrue_v2():
    # ESTABLISH
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_2_to_7_premise = premiseunit_shop(need=hr24_road, open=2, nigh=7)
    range_0_to_8_fact = factheir_shop(hr24_road, hr24_road, open=0, nigh=8)
    assert range_2_to_7_premise._status is None

    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_0_to_8_fact)
    # THEN
    assert range_2_to_7_premise._status == True
    assert range_2_to_7_premise._task == True

    # ESTABLISH
    range_3_to_5_fact = factheir_shop(hr24_road, hr24_road, open=3, nigh=5)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_3_to_5_fact)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task is False

    # ESTABLISH
    range_8_to_8_fact = factheir_shop(hr24_road, hr24_road, open=8, nigh=8)
    # WHEN
    range_2_to_7_premise.set_status(x_factheir=range_8_to_8_fact)
    assert range_2_to_7_premise._status is False
    assert range_2_to_7_premise._task is False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeStatusFalse():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    hr24_text = "24hr"
    hr24_road = create_road(timetech_road, hr24_text)
    hr24_premise = premiseunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_premise._status is None

    # WHEN
    bud_fact = factheir_shop(base=hr24_road, pick=hr24_road, open=8, nigh=10)
    hr24_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert hr24_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusFalse():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    o1_n1_d6_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    assert o1_n1_d6_premise._status is None

    # WHEN
    range_6_to_6_fact = factheir_shop(week_road, week_road, open=6, nigh=6)
    o1_n1_d6_premise.set_status(x_factheir=range_6_to_6_fact)

    # THEN
    assert o1_n1_d6_premise._status is False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusTrue():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    bud_fact = factheir_shop(base=week_road, pick=week_road, open=7, nigh=7)
    assert week_premise._status is None

    # WHEN
    week_premise.set_status(x_factheir=bud_fact)

    # THEN
    assert week_premise._status == True


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithDvisiorAndOpen_Nigh():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict != None
    static_dict = {"need": week_road, "open": 1, "nigh": 1, "divisor": 6}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOpenAndNigh():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road, open=1, nigh=4)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict != None
    static_dict = {"need": week_road, "open": 1, "nigh": 4}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOnlyRoadUnit():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict != None
    static_dict = {"need": week_road}
    assert premise_dict == static_dict


def test_PremiseUnit_get_obj_key():
    # ESTABLISH
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road)

    # WHEN / THEN
    assert week_premise.get_obj_key() == week_road


def test_PremiseUnit_find_replace_road_casas():
    # ESTABLISH
    old_root_road = root_label()
    weekday_text = "weekday"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    old_sunday_road = create_road(weekday_road, sunday_text)
    sunday_premise = premiseunit_shop(need=old_sunday_road)
    print(sunday_premise)
    assert sunday_premise.need == old_sunday_road

    # WHEN
    new_road = "fun"
    sunday_premise.find_replace_road(old_road=old_root_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_text)
    new_sunday_road = create_road(new_weekday_road, sunday_text)

    # THEN
    assert sunday_premise.need == new_sunday_road


def test_PremiseUnits_get_from_dict_ReturnsCompleteObj():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
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
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    static_dict = {weekday_road: {"need": weekday_road}}

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    weekday_premise = premises_dict.get(weekday_road)
    assert weekday_premise == premiseunit_shop(weekday_road)


def test_PremiseUnitsUnit_set_delimiter_SetsAttrsCorrectly():
    # ESTABLISH
    week_text = "weekday"
    sun_text = "Sunday"
    slash_text = "/"
    slash_week_road = create_road(root_label(), week_text, delimiter=slash_text)
    slash_sun_road = create_road(slash_week_road, sun_text, delimiter=slash_text)
    sun_premiseunit = premiseunit_shop(slash_sun_road, delimiter=slash_text)
    assert sun_premiseunit.delimiter == slash_text
    assert sun_premiseunit.need == slash_sun_road

    # WHEN
    star_text = "*"
    sun_premiseunit.set_delimiter(new_delimiter=star_text)

    # THEN
    assert sun_premiseunit.delimiter == star_text
    star_week_road = create_road(root_label(), week_text, delimiter=star_text)
    star_sun_road = create_road(star_week_road, sun_text, delimiter=star_text)
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
    old_real_id = "El Paso"
    casa_text = "casa"
    seasons_text = "seasons"
    old_casa_road = create_road(old_real_id, casa_text)
    old_seasons_road = create_road(old_casa_road, seasons_text)
    old_premiseunit = premiseunit_shop(need=old_seasons_road)
    old_premiseunits = {old_premiseunit.need: old_premiseunit}
    assert old_premiseunits.get(old_seasons_road) == old_premiseunit

    # WHEN
    new_real_id = "Austin"
    new_casa_road = create_road(new_real_id, casa_text)
    new_seasons_road = create_road(new_casa_road, seasons_text)
    new_premise_roads = find_replace_road_key_dict(
        dict_x=old_premiseunits, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_premiseunit = premiseunit_shop(need=new_seasons_road)

    assert new_premise_roads.get(new_seasons_road) == new_premiseunit
    assert new_premise_roads.get(old_seasons_road) is None
