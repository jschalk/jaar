from datetime import datetime
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a07_calendar_logic._test_util.a07_str import (
    day_str,
    days_str,
    time_str,
    week_str,
    weeks_str,
)
from src.a07_calendar_logic._test_util.calendar_examples import (
    add_time_creg_conceptunit,
    creg_weekday_conceptunits,
    get_creg_min_from_dt,
    get_cregtime_str,
    get_thu,
    get_wed,
)
from src.a07_calendar_logic.chrono import get_year_way


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_day_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    day_way = sue_planunit.make_way(creg_way, day_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # day_concept = sue_planunit.get_concept_obj(day_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_way)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_day_concept_Scenario1():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    day_way = sue_planunit.make_way(creg_way, day_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # day_concept = sue_planunit.get_concept_obj(day_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=day_way,
        reason_premise=day_way,
        popen=0,
        reason_pnigh=1,
        pdivisor=1,
    )
    sue_planunit.add_fact(creg_way, creg_way, 0, 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_way)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_day_concept_Scenario2():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    day_way = sue_planunit.make_way(creg_way, day_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # day_concept = sue_planunit.get_concept_obj(day_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=day_way,
        reason_premise=day_way,
        popen=360,
        reason_pnigh=420,
        pdivisor=1440,
    )
    sue_planunit.add_fact(creg_way, creg_way, 14400300, 14400480)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_way) != None


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_days_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    days_way = sue_planunit.make_way(creg_way, days_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # days_concept = sue_planunit.get_concept_obj(days_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=days_way,
        reason_premise=days_way,
        popen=4,
        reason_pnigh=5,
        pdivisor=7,
    )
    sue_planunit.add_fact(creg_way, creg_way, 11 * 1400, 12 * 1400)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    clean_concept = sue_planunit.get_concept_obj(clean_way)
    print(f"{clean_concept._factheirs.keys()=}")
    print(f"{clean_concept._factheirs.get(days_way)=}")
    assert sue_agenda.get(clean_way)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_week_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    week_way = sue_planunit.make_way(creg_way, week_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # week_concept = sue_planunit.get_concept_obj(week_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=week_way,
        reason_premise=week_way,
        popen=0,
        reason_pnigh=1440,
        pdivisor=10080,
    )
    sue_planunit.add_fact(creg_way, creg_way, 0, 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_way)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_week_concept_Scenario1():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    week_way = sue_planunit.make_way(creg_way, week_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # week_concept = sue_planunit.get_concept_obj(week_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=week_way,
        reason_premise=week_way,
        popen=2880,
        reason_pnigh=4220,
        pdivisor=10080,
    )
    sue_planunit.add_fact(creg_way, creg_way, 100802880, 100804220)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_way) != None


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_weeks_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    weeks_way = sue_planunit.make_way(creg_way, weeks_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    creg_concept = sue_planunit.get_concept_obj(creg_way)
    print(f"{creg_concept.begin=} {creg_concept.close=}")
    # weeks_concept = sue_planunit.get_concept_obj(weeks_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=weeks_way,
        reason_premise=weeks_way,
        popen=4,
        reason_pnigh=5,
        pdivisor=7,
    )
    sue_planunit.add_fact(creg_way, creg_way, 11 * 10080, 12 * 10080)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_way)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_year_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    year_way = get_year_way(sue_planunit, creg_way)
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # year_concept = sue_planunit.get_concept_obj(year_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=year_way,
        reason_premise=year_way,
        popen=0,
        reason_pnigh=1440,
        pdivisor=525600,
    )
    sue_planunit.add_fact(creg_way, creg_way, 0, 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_way)

    # WHEN
    sue_planunit.add_fact(creg_way, creg_way, 1444, 2880)
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert not sue_agenda.get(clean_way)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_year_concept_Scenario1():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    year_way = get_year_way(sue_planunit, creg_way)

    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # year_concept = sue_planunit.get_concept_obj(year_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=year_way,
        reason_premise=year_way,
        popen=0,
        reason_pnigh=1440,
        pdivisor=525600,
    )
    sue_planunit.add_fact(creg_way, creg_way, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_way)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_year_concept_Scenario2():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    year_way = get_year_way(sue_planunit, creg_way)

    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    creg_concept = sue_planunit.get_concept_obj(creg_way)
    # year_concept = sue_planunit.get_concept_obj(year_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=year_way,
        reason_premise=year_way,
        popen=0,
        reason_pnigh=1440,
        pdivisor=525600,
    )
    sue_planunit.add_fact(creg_way, creg_way, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_way)

    # WHEN / THEN
    yr2000mar1 = get_creg_min_from_dt(dt=datetime(2000, 3, 1, 0, 0))
    yr2000mar2 = get_creg_min_from_dt(dt=datetime(2000, 3, 2, 0, 0))
    yr2000dec1 = get_creg_min_from_dt(dt=datetime(2000, 12, 1, 0, 0))
    yr2000dec2 = get_creg_min_from_dt(dt=datetime(2000, 12, 2, 0, 0))
    yr2004mar1 = get_creg_min_from_dt(dt=datetime(2004, 3, 1, 0, 0))
    yr2004mar2 = get_creg_min_from_dt(dt=datetime(2004, 3, 2, 0, 0))

    sue_planunit.add_fact(creg_way, creg_way, yr2000mar1, yr2000mar1 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 1
    sue_planunit.add_fact(creg_way, creg_way, yr2000mar2, yr2000mar2 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 0
    sue_planunit.add_fact(creg_way, creg_way, yr2004mar1, yr2004mar1 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 1
    sue_planunit.add_fact(creg_way, creg_way, yr2000mar2, yr2004mar2 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 1


def wed_gogo_want():
    return creg_weekday_conceptunits().get(get_wed()).gogo_want


def thu_gogo_want():
    return creg_weekday_conceptunits().get(get_thu()).gogo_want


def test_PlanUnit_add_time_creg_conceptunit_SyncsWeekDayAndYear_Wednesday_March1_2000():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    year_way = get_year_way(sue_planunit, creg_way)
    week_way = sue_planunit.make_way(creg_way, week_str())
    # sun_way = sue_planunit.make_way(week_way, get_sun())
    # mon_way = sue_planunit.make_way(week_way, get_mon())
    # tue_way = sue_planunit.make_way(week_way, get_tue())
    wed_way = sue_planunit.make_way(week_way, get_wed())
    # thu_way = sue_planunit.make_way(week_way, get_thu())
    # fri_way = sue_planunit.make_way(week_way, get_fri())
    # sat_way = sue_planunit.make_way(week_way, get_sat())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # week_concept = sue_planunit.get_concept_obj(week_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=wed_way,
        reason_premise=wed_way,
        popen=wed_gogo_want(),
        reason_pnigh=wed_gogo_want() + 1440,
    )
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=year_way,
        reason_premise=year_way,
        popen=0,
        reason_pnigh=1400,
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
    clean_concept = sue_planunit.get_concept_obj(clean_way)
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(year_way).fopen=}")
    print(f"{clean_concept._factheirs.get(year_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar7day, yr2000_mar8day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar1day, yr2000_mar2day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar2day, yr2000_mar3day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar3day, yr2000_mar4day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar4day, yr2000_mar5day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar5day, yr2000_mar6day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0


def test_PlanUnit_add_time_creg_conceptunit_SyncsWeekDayAndYear_Thursday_March2_2000():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    year_way = get_year_way(sue_planunit, creg_way)
    week_way = sue_planunit.make_way(creg_way, week_str())
    # sun_way = sue_planunit.make_way(week_way, get_sun())
    # mon_way = sue_planunit.make_way(week_way, get_mon())
    # tue_way = sue_planunit.make_way(week_way, get_tue())
    wed_way = sue_planunit.make_way(week_way, get_wed())
    # thu_way = sue_planunit.make_way(week_way, get_thu())
    # fri_way = sue_planunit.make_way(week_way, get_fri())
    # sat_way = sue_planunit.make_way(week_way, get_sat())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_way)
    # week_concept = sue_planunit.get_concept_obj(week_way)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_way = sue_planunit.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_planunit.make_way(casa_way, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=wed_way,
        reason_premise=wed_way,
        popen=thu_gogo_want(),
        reason_pnigh=thu_gogo_want() + 1440,
    )
    sue_planunit.edit_concept_attr(
        clean_way,
        reason_rcontext=year_way,
        reason_premise=year_way,
        popen=1400,
        reason_pnigh=2800,
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
    clean_concept = sue_planunit.get_concept_obj(clean_way)
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(year_way).fopen=}")
    print(f"{clean_concept._factheirs.get(year_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar7day, yr2000_mar8day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar1day, yr2000_mar2day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    # TODO This should be zero but it comes back as 1
    # assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar2day, yr2000_mar3day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar3day, yr2000_mar4day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar4day, yr2000_mar5day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_way, creg_way, yr2000_mar5day, yr2000_mar6day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_way).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_way).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_way)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_concept.get_reasonheir(year_way)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0
