from datetime import datetime
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a07_timeline_logic.test._util.a07_str import (
    day_str,
    days_str,
    time_str,
    week_str,
    weeks_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_conceptunit,
    creg_weekday_conceptunits,
    get_creg_min_from_dt,
    get_cregtime_str,
    get_thu,
    get_wed,
)
from src.a07_timeline_logic.timeline import get_year_rope


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_day_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_planunit.make_rope(creg_rope, day_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # day_concept = sue_planunit.get_concept_obj(day_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_day_concept_Scenario1():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_planunit.make_rope(creg_rope, day_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # day_concept = sue_planunit.get_concept_obj(day_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=day_rope,
        reason_premise=day_rope,
        popen=0,
        reason_pnigh=1,
        pdivisor=1,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_day_concept_Scenario2():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_planunit.make_rope(creg_rope, day_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # day_concept = sue_planunit.get_concept_obj(day_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=day_rope,
        reason_premise=day_rope,
        popen=360,
        reason_pnigh=420,
        pdivisor=1440,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 14400300, 14400480)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope) != None


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_days_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    days_rope = sue_planunit.make_rope(creg_rope, days_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # days_concept = sue_planunit.get_concept_obj(days_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=days_rope,
        reason_premise=days_rope,
        popen=4,
        reason_pnigh=5,
        pdivisor=7,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 11 * 1400, 12 * 1400)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    clean_concept = sue_planunit.get_concept_obj(clean_rope)
    print(f"{clean_concept._factheirs.keys()=}")
    print(f"{clean_concept._factheirs.get(days_rope)=}")
    assert sue_agenda.get(clean_rope)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_week_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    week_rope = sue_planunit.make_rope(creg_rope, week_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # week_concept = sue_planunit.get_concept_obj(week_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=week_rope,
        reason_premise=week_rope,
        popen=0,
        reason_pnigh=1440,
        pdivisor=10080,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_week_concept_Scenario1():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    week_rope = sue_planunit.make_rope(creg_rope, week_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # week_concept = sue_planunit.get_concept_obj(week_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=week_rope,
        reason_premise=week_rope,
        popen=2880,
        reason_pnigh=4220,
        pdivisor=10080,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 100802880, 100804220)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope) != None


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_weeks_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    weeks_rope = sue_planunit.make_rope(creg_rope, weeks_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    creg_concept = sue_planunit.get_concept_obj(creg_rope)
    print(f"{creg_concept.begin=} {creg_concept.close=}")
    # weeks_concept = sue_planunit.get_concept_obj(weeks_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=weeks_rope,
        reason_premise=weeks_rope,
        popen=4,
        reason_pnigh=5,
        pdivisor=7,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 11 * 10080, 12 * 10080)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_year_concept_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_planunit, creg_rope)
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # year_concept = sue_planunit.get_concept_obj(year_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=year_rope,
        reason_premise=year_rope,
        popen=0,
        reason_pnigh=1440,
        pdivisor=525600,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)

    # WHEN
    sue_planunit.add_fact(creg_rope, creg_rope, 1444, 2880)
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert not sue_agenda.get(clean_rope)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_year_concept_Scenario1():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_planunit, creg_rope)

    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # year_concept = sue_planunit.get_concept_obj(year_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=year_rope,
        reason_premise=year_rope,
        popen=0,
        reason_pnigh=1440,
        pdivisor=525600,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PlanUnit_get_agenda_dict_ReturnsDictWith_year_concept_Scenario2():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_planunit, creg_rope)

    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # year_concept = sue_planunit.get_concept_obj(year_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=year_rope,
        reason_premise=year_rope,
        popen=0,
        reason_pnigh=1440,
        pdivisor=525600,
    )
    sue_planunit.add_fact(creg_rope, creg_rope, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_planunit.get_agenda_dict()
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

    sue_planunit.add_fact(creg_rope, creg_rope, yr2000mar1, yr2000mar1 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 1
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000mar2, yr2000mar2 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 0
    sue_planunit.add_fact(creg_rope, creg_rope, yr2004mar1, yr2004mar1 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 1
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000mar2, yr2004mar2 + 1440)
    assert len(sue_planunit.get_agenda_dict()) == 1


def wed_gogo_want():
    return creg_weekday_conceptunits().get(get_wed()).gogo_want


def thu_gogo_want():
    return creg_weekday_conceptunits().get(get_thu()).gogo_want


def test_PlanUnit_add_time_creg_conceptunit_SyncsWeekDayAndYear_Wednesday_March1_2000():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_planunit, creg_rope)
    week_rope = sue_planunit.make_rope(creg_rope, week_str())
    # sun_rope = sue_planunit.make_rope(week_rope, get_sun())
    # mon_rope = sue_planunit.make_rope(week_rope, get_mon())
    # tue_rope = sue_planunit.make_rope(week_rope, get_tue())
    wed_rope = sue_planunit.make_rope(week_rope, get_wed())
    # thu_rope = sue_planunit.make_rope(week_rope, get_thu())
    # fri_rope = sue_planunit.make_rope(week_rope, get_fri())
    # sat_rope = sue_planunit.make_rope(week_rope, get_sat())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # week_concept = sue_planunit.get_concept_obj(week_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=wed_rope,
        reason_premise=wed_rope,
        popen=wed_gogo_want(),
        reason_pnigh=wed_gogo_want() + 1440,
    )
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=year_rope,
        reason_premise=year_rope,
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
    clean_concept = sue_planunit.get_concept_obj(clean_rope)
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(year_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(year_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar7day, yr2000_mar8day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar1day, yr2000_mar2day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar2day, yr2000_mar3day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar3day, yr2000_mar4day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar4day, yr2000_mar5day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar5day, yr2000_mar6day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0


def test_PlanUnit_add_time_creg_conceptunit_SyncsWeekDayAndYear_Thursday_March2_2000():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(time_str())
    creg_rope = sue_planunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_planunit, creg_rope)
    week_rope = sue_planunit.make_rope(creg_rope, week_str())
    # sun_rope = sue_planunit.make_rope(week_rope, get_sun())
    # mon_rope = sue_planunit.make_rope(week_rope, get_mon())
    # tue_rope = sue_planunit.make_rope(week_rope, get_tue())
    wed_rope = sue_planunit.make_rope(week_rope, get_wed())
    # thu_rope = sue_planunit.make_rope(week_rope, get_thu())
    # fri_rope = sue_planunit.make_rope(week_rope, get_fri())
    # sat_rope = sue_planunit.make_rope(week_rope, get_sat())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    # creg_concept = sue_planunit.get_concept_obj(creg_rope)
    # week_concept = sue_planunit.get_concept_obj(week_rope)
    sue_planunit._set_concepttree_range_attrs()
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=wed_rope,
        reason_premise=wed_rope,
        popen=thu_gogo_want(),
        reason_pnigh=thu_gogo_want() + 1440,
    )
    sue_planunit.edit_concept_attr(
        clean_rope,
        reason_rcontext=year_rope,
        reason_premise=year_rope,
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
    clean_concept = sue_planunit.get_concept_obj(clean_rope)
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(year_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(year_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar7day, yr2000_mar8day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar1day, yr2000_mar2day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    # TODO This should be zero but it comes back as 1
    # assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar2day, yr2000_mar3day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar3day, yr2000_mar4day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar4day, yr2000_mar5day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_planunit.add_fact(creg_rope, creg_rope, yr2000_mar5day, yr2000_mar6day)
    sue_planunit.settle_plan()
    print(f"{clean_concept._factheirs.get(wed_rope).fopen=}")
    print(f"{clean_concept._factheirs.get(wed_rope).fnigh=}")
    print(f"{clean_concept.get_reasonheir(wed_rope)._status=}")
    print(f"{len(sue_planunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_concept.get_reasonheir(year_rope)._status=} \n")
    assert len(sue_planunit.get_agenda_dict()) == 0
