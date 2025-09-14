from datetime import datetime
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a07_timeline_logic.test._util.a07_terms import (
    day_str,
    days_str,
    time_str,
    week_str,
    weeks_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    creg_weekday_planunits,
    get_creg_min_from_dt,
    get_cregtime_str,
    get_thu,
    get_wed,
)
from src.a07_timeline_logic.timeline_main import get_year_rope


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_day_plan_Scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # day_plan = sue_beliefunit.get_plan_obj(day_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope)


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_day_plan_Scenario1():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # day_plan = sue_beliefunit.get_plan_obj(day_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=day_rope,
        reason_case=day_rope,
        reason_lower=0,
        reason_upper=1,
        reason_divisor=1,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_day_plan_Scenario2():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # day_plan = sue_beliefunit.get_plan_obj(day_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=day_rope,
        reason_case=day_rope,
        reason_lower=360,
        reason_upper=420,
        reason_divisor=1440,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 14400300, 14400480)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope) != None


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_days_plan_Scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    days_rope = sue_beliefunit.make_rope(creg_rope, days_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # days_plan = sue_beliefunit.get_plan_obj(days_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=days_rope,
        reason_case=days_rope,
        reason_lower=4,
        reason_upper=5,
        reason_divisor=7,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 11 * 1400, 12 * 1400)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()

    # THEN
    clean_plan = sue_beliefunit.get_plan_obj(clean_rope)
    print(f"{clean_plan.factheirs.keys()=}")
    print(f"{clean_plan.factheirs.get(days_rope)=}")
    assert sue_agenda.get(clean_rope)


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_week_plan_Scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    week_rope = sue_beliefunit.make_rope(creg_rope, week_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # week_plan = sue_beliefunit.get_plan_obj(week_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=week_rope,
        reason_case=week_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=10080,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_week_plan_Scenario1():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    week_rope = sue_beliefunit.make_rope(creg_rope, week_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # week_plan = sue_beliefunit.get_plan_obj(week_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=week_rope,
        reason_case=week_rope,
        reason_lower=2880,
        reason_upper=4220,
        reason_divisor=10080,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 100802880, 100804220)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope) != None


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_weeks_plan_Scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    weeks_rope = sue_beliefunit.make_rope(creg_rope, weeks_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    print(f"{creg_plan.begin=} {creg_plan.close=}")
    # weeks_plan = sue_beliefunit.get_plan_obj(weeks_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=weeks_rope,
        reason_case=weeks_rope,
        reason_lower=4,
        reason_upper=5,
        reason_divisor=7,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 11 * 10080, 12 * 10080)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope)


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_year_plan_Scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_beliefunit, creg_rope)
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # year_plan = sue_beliefunit.get_plan_obj(year_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=525600,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)

    # WHEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, 1444, 2880)
    sue_agenda = sue_beliefunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert not sue_agenda.get(clean_rope)


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_year_plan_Scenario1():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_beliefunit, creg_rope)

    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # year_plan = sue_beliefunit.get_plan_obj(year_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=525600,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_BeliefUnit_get_agenda_dict_ReturnsDictWith_year_plan_Scenario2():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_beliefunit, creg_rope)

    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # year_plan = sue_beliefunit.get_plan_obj(year_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=525600,
    )
    sue_beliefunit.add_fact(creg_rope, creg_rope, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_beliefunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)

    # WHEN / THEN
    yr2000mar1 = get_creg_min_from_dt(dt=datetime(2000, 3, 1, 0, 0))
    yr2000mar2 = get_creg_min_from_dt(dt=datetime(2000, 3, 2, 0, 0))
    yr2000dec1 = get_creg_min_from_dt(dt=datetime(2000, 12, 1, 0, 0))
    yr2000dec2 = get_creg_min_from_dt(dt=datetime(2000, 12, 2, 0, 0))
    yr2004mar1 = get_creg_min_from_dt(dt=datetime(2004, 3, 1, 0, 0))
    yr2004mar2 = get_creg_min_from_dt(dt=datetime(2004, 3, 2, 0, 0))

    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000mar1, yr2000mar1 + 1440)
    assert len(sue_beliefunit.get_agenda_dict()) == 1
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000mar2, yr2000mar2 + 1440)
    assert len(sue_beliefunit.get_agenda_dict()) == 0
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2004mar1, yr2004mar1 + 1440)
    assert len(sue_beliefunit.get_agenda_dict()) == 1
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000mar2, yr2004mar2 + 1440)
    assert len(sue_beliefunit.get_agenda_dict()) == 1


def wed_gogo_want():
    return creg_weekday_planunits().get(get_wed()).gogo_want


def thu_gogo_want():
    return creg_weekday_planunits().get(get_thu()).gogo_want


def test_BeliefUnit_add_time_creg_planunit_SyncsWeekDayAndYear_Wednesday_March1_2000():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_beliefunit, creg_rope)
    week_rope = sue_beliefunit.make_rope(creg_rope, week_str())
    # sun_rope = sue_beliefunit.make_rope(week_rope, get_sun())
    # mon_rope = sue_beliefunit.make_rope(week_rope, get_mon())
    # tue_rope = sue_beliefunit.make_rope(week_rope, get_tue())
    wed_rope = sue_beliefunit.make_rope(week_rope, get_wed())
    # thu_rope = sue_beliefunit.make_rope(week_rope, get_thu())
    # fri_rope = sue_beliefunit.make_rope(week_rope, get_fri())
    # sat_rope = sue_beliefunit.make_rope(week_rope, get_sat())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # week_plan = sue_beliefunit.get_plan_obj(week_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=wed_rope,
        reason_case=wed_rope,
        reason_lower=wed_gogo_want(),
        reason_upper=wed_gogo_want() + 1440,
    )
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1400,
    )

    yr2000_mar1day = get_creg_min_from_dt(datetime(2000, 3, 1, 0, 0))
    yr2000_mar2day = get_creg_min_from_dt(datetime(2000, 3, 2, 0, 0))
    yr2000_mar3day = get_creg_min_from_dt(datetime(2000, 3, 3, 0, 0))
    yr2000_mar4day = get_creg_min_from_dt(datetime(2000, 3, 4, 0, 0))
    yr2000_mar5day = get_creg_min_from_dt(datetime(2000, 3, 5, 0, 0))
    yr2000_mar6day = get_creg_min_from_dt(datetime(2000, 3, 6, 0, 0))
    yr2000_mar7day = get_creg_min_from_dt(datetime(2000, 3, 7, 0, 0))
    yr2000_mar8day = get_creg_min_from_dt(datetime(2000, 3, 8, 0, 0))
    print(f"{wed_gogo_want()=}")
    print(f"{wed_gogo_want()+1440=}")
    clean_plan = sue_beliefunit.get_plan_obj(clean_rope)
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(year_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(year_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar7day, yr2000_mar8day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar1day, yr2000_mar2day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar2day, yr2000_mar3day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar3day, yr2000_mar4day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar4day, yr2000_mar5day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar5day, yr2000_mar6day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0


def test_BeliefUnit_add_time_creg_planunit_SyncsWeekDayAndYear_Thursday_March2_2000():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_beliefunit, creg_rope)
    week_rope = sue_beliefunit.make_rope(creg_rope, week_str())
    # sun_rope = sue_beliefunit.make_rope(week_rope, get_sun())
    # mon_rope = sue_beliefunit.make_rope(week_rope, get_mon())
    # tue_rope = sue_beliefunit.make_rope(week_rope, get_tue())
    wed_rope = sue_beliefunit.make_rope(week_rope, get_wed())
    # thu_rope = sue_beliefunit.make_rope(week_rope, get_thu())
    # fri_rope = sue_beliefunit.make_rope(week_rope, get_fri())
    # sat_rope = sue_beliefunit.make_rope(week_rope, get_sat())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    # creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    # week_plan = sue_beliefunit.get_plan_obj(week_rope)
    sue_beliefunit._set_plantree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=wed_rope,
        reason_case=wed_rope,
        reason_lower=thu_gogo_want(),
        reason_upper=thu_gogo_want() + 1440,
    )
    sue_beliefunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=1400,
        reason_upper=2800,
    )

    yr2000_mar1day = get_creg_min_from_dt(datetime(2000, 3, 1, 0, 0))
    yr2000_mar2day = get_creg_min_from_dt(datetime(2000, 3, 2, 0, 0))
    yr2000_mar3day = get_creg_min_from_dt(datetime(2000, 3, 3, 0, 0))
    yr2000_mar4day = get_creg_min_from_dt(datetime(2000, 3, 4, 0, 0))
    yr2000_mar5day = get_creg_min_from_dt(datetime(2000, 3, 5, 0, 0))
    yr2000_mar6day = get_creg_min_from_dt(datetime(2000, 3, 6, 0, 0))
    yr2000_mar7day = get_creg_min_from_dt(datetime(2000, 3, 7, 0, 0))
    yr2000_mar8day = get_creg_min_from_dt(datetime(2000, 3, 8, 0, 0))
    print(f"{wed_gogo_want()=}")
    print(f"{wed_gogo_want()+1440=}")
    clean_plan = sue_beliefunit.get_plan_obj(clean_rope)
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(year_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(year_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar7day, yr2000_mar8day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar1day, yr2000_mar2day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    # TODO This should be zero but it comes back as 1
    print(f"{sue_beliefunit.get_agenda_dict().keys()=}") == 1
    assert len(sue_beliefunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar2day, yr2000_mar3day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar3day, yr2000_mar4day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar4day, yr2000_mar5day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_beliefunit.add_fact(creg_rope, creg_rope, yr2000_mar5day, yr2000_mar6day)
    sue_beliefunit.cashout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).status=}")
    print(f"{len(sue_beliefunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).status=} \n")
    assert len(sue_beliefunit.get_agenda_dict()) == 0
