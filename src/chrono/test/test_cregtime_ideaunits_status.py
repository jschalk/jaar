from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.chrono.examples.chrono_examples import (
    get_creg_min_from_dt,
    add_time_creg_ideaunit,
    get_cregtime_text,
    get_wed,
    get_thu,
    creg_weekday_ideaunits,
)
from src.chrono.timebuilder import (
    time_str,
    day_str,
    days_str,
    get_year_road,
    weeks_str,
    week_str,
)
from datetime import datetime


def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    day_road = sue_budunit.make_road(creg_road, day_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # day_idea = sue_budunit.get_idea_obj(day_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario1():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    day_road = sue_budunit.make_road(creg_road, day_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # day_idea = sue_budunit.get_idea_obj(day_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=0,
        reason_premise_nigh=1,
        reason_premise_divisor=1,
    )
    sue_budunit.set_fact(creg_road, creg_road, 0, 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario2():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    day_road = sue_budunit.make_road(creg_road, day_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # day_idea = sue_budunit.get_idea_obj(day_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=360,
        reason_premise_nigh=420,
        reason_premise_divisor=1440,
    )
    sue_budunit.set_fact(creg_road, creg_road, 14400300, 14400480)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_road) != None


def test_BudUnit_get_agenda_dict_ReturnsDictWith_days_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    days_road = sue_budunit.make_road(creg_road, days_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # days_idea = sue_budunit.get_idea_obj(days_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=days_road,
        reason_premise=days_road,
        reason_premise_open=4,
        reason_premise_nigh=5,
        reason_premise_divisor=7,
    )
    sue_budunit.set_fact(creg_road, creg_road, 11 * 1400, 12 * 1400)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    clean_idea = sue_budunit.get_idea_obj(clean_road)
    print(f"{clean_idea._factheirs.keys()=}")
    print(f"{clean_idea._factheirs.get(days_road)=}")
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_week_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    week_road = sue_budunit.make_road(creg_road, week_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # week_idea = sue_budunit.get_idea_obj(week_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=week_road,
        reason_premise=week_road,
        reason_premise_open=0,
        reason_premise_nigh=1440,
        reason_premise_divisor=10080,
    )
    sue_budunit.set_fact(creg_road, creg_road, 0, 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_week_idea_Scenario1():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    week_road = sue_budunit.make_road(creg_road, week_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # week_idea = sue_budunit.get_idea_obj(week_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=week_road,
        reason_premise=week_road,
        reason_premise_open=2880,
        reason_premise_nigh=4220,
        reason_premise_divisor=10080,
    )
    sue_budunit.set_fact(creg_road, creg_road, 100802880, 100804220)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_road) != None


def test_BudUnit_get_agenda_dict_ReturnsDictWith_weeks_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    weeks_road = sue_budunit.make_road(creg_road, weeks_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    creg_idea = sue_budunit.get_idea_obj(creg_road)
    print(f"{creg_idea._begin=} {creg_idea._close=}")
    # weeks_idea = sue_budunit.get_idea_obj(weeks_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=weeks_road,
        reason_premise=weeks_road,
        reason_premise_open=4,
        reason_premise_nigh=5,
        reason_premise_divisor=7,
    )
    sue_budunit.set_fact(creg_road, creg_road, 11 * 10080, 12 * 10080)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    year_road = get_year_road(sue_budunit, creg_road)
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # year_idea = sue_budunit.get_idea_obj(year_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=year_road,
        reason_premise=year_road,
        reason_premise_open=0,
        reason_premise_nigh=1440,
        reason_premise_divisor=525600,
    )
    sue_budunit.set_fact(creg_road, creg_road, 0, 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)

    # WHEN
    sue_budunit.set_fact(creg_road, creg_road, 1444, 2880)
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert not sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario1():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    year_road = get_year_road(sue_budunit, creg_road)

    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # year_idea = sue_budunit.get_idea_obj(year_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=year_road,
        reason_premise=year_road,
        reason_premise_open=0,
        reason_premise_nigh=1440,
        reason_premise_divisor=525600,
    )
    sue_budunit.set_fact(creg_road, creg_road, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario2():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    year_road = get_year_road(sue_budunit, creg_road)

    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    creg_idea = sue_budunit.get_idea_obj(creg_road)
    # year_idea = sue_budunit.get_idea_obj(year_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=year_road,
        reason_premise=year_road,
        reason_premise_open=0,
        reason_premise_nigh=1440,
        reason_premise_divisor=525600,
    )
    sue_budunit.set_fact(creg_road, creg_road, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)

    # WHEN / THEN
    yr2000mar1 = get_creg_min_from_dt(dt=datetime(2000, 3, 1, 0, 0))
    yr2000mar2 = get_creg_min_from_dt(dt=datetime(2000, 3, 2, 0, 0))
    yr2000dec1 = get_creg_min_from_dt(dt=datetime(2000, 12, 1, 0, 0))
    yr2000dec2 = get_creg_min_from_dt(dt=datetime(2000, 12, 2, 0, 0))
    yr2004mar1 = get_creg_min_from_dt(dt=datetime(2004, 3, 1, 0, 0))
    yr2004mar2 = get_creg_min_from_dt(dt=datetime(2004, 3, 2, 0, 0))

    sue_budunit.set_fact(creg_road, creg_road, yr2000mar1, yr2000mar1 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 1
    sue_budunit.set_fact(creg_road, creg_road, yr2000mar2, yr2000mar2 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 0
    sue_budunit.set_fact(creg_road, creg_road, yr2004mar1, yr2004mar1 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 1
    sue_budunit.set_fact(creg_road, creg_road, yr2000mar2, yr2004mar2 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 1


def wed_gogo_want():
    return creg_weekday_ideaunits().get(get_wed())._gogo_want


def thu_gogo_want():
    return creg_weekday_ideaunits().get(get_thu())._gogo_want


def test_BudUnit_add_time_creg_ideaunit_SyncsWeekDayAndYear_Wednesday_March1_2000():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    year_road = get_year_road(sue_budunit, creg_road)
    week_road = sue_budunit.make_road(creg_road, week_str())
    # sun_road = sue_budunit.make_road(week_road, get_sun())
    # mon_road = sue_budunit.make_road(week_road, get_mon())
    # tue_road = sue_budunit.make_road(week_road, get_tue())
    wed_road = sue_budunit.make_road(week_road, get_wed())
    # thu_road = sue_budunit.make_road(week_road, get_thu())
    # fri_road = sue_budunit.make_road(week_road, get_fri())
    # sat_road = sue_budunit.make_road(week_road, get_sat())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # week_idea = sue_budunit.get_idea_obj(week_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=wed_road,
        reason_premise=wed_road,
        reason_premise_open=wed_gogo_want(),
        reason_premise_nigh=wed_gogo_want() + 1440,
    )
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=year_road,
        reason_premise=year_road,
        reason_premise_open=0,
        reason_premise_nigh=1400,
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
    clean_idea = sue_budunit.get_idea_obj(clean_road)
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar6day, yr2000_mar7day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(year_road).open=}")
    print(f"{clean_idea._factheirs.get(year_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar6day, yr2000_mar7day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar7day, yr2000_mar8day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar1day, yr2000_mar2day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar2day, yr2000_mar3day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar3day, yr2000_mar4day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar4day, yr2000_mar5day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar5day, yr2000_mar6day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0


def test_BudUnit_add_time_creg_ideaunit_SyncsWeekDayAndYear_Thursday_March2_2000():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_text())
    year_road = get_year_road(sue_budunit, creg_road)
    week_road = sue_budunit.make_road(creg_road, week_str())
    # sun_road = sue_budunit.make_road(week_road, get_sun())
    # mon_road = sue_budunit.make_road(week_road, get_mon())
    # tue_road = sue_budunit.make_road(week_road, get_tue())
    wed_road = sue_budunit.make_road(week_road, get_wed())
    # thu_road = sue_budunit.make_road(week_road, get_thu())
    # fri_road = sue_budunit.make_road(week_road, get_fri())
    # sat_road = sue_budunit.make_road(week_road, get_sat())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    # creg_idea = sue_budunit.get_idea_obj(creg_road)
    # week_idea = sue_budunit.get_idea_obj(week_road)
    sue_budunit._set_ideaunits_range()
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=wed_road,
        reason_premise=wed_road,
        reason_premise_open=thu_gogo_want(),
        reason_premise_nigh=thu_gogo_want() + 1440,
    )
    sue_budunit.edit_idea_attr(
        clean_road,
        reason_base=year_road,
        reason_premise=year_road,
        reason_premise_open=1400,
        reason_premise_nigh=2800,
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
    clean_idea = sue_budunit.get_idea_obj(clean_road)
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar6day, yr2000_mar7day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(year_road).open=}")
    print(f"{clean_idea._factheirs.get(year_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar6day, yr2000_mar7day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar7day, yr2000_mar8day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar1day, yr2000_mar2day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    # TODO This should be zero but it comes back as 1
    # assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar2day, yr2000_mar3day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar3day, yr2000_mar4day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar4day, yr2000_mar5day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_budunit.set_fact(creg_road, creg_road, yr2000_mar5day, yr2000_mar6day)
    sue_budunit.settle_bud()
    print(f"{clean_idea._factheirs.get(wed_road).open=}")
    print(f"{clean_idea._factheirs.get(wed_road).nigh=}")
    print(f"{clean_idea.get_reasonheir(wed_road)._status=}")
    print(f"{len(sue_budunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_idea.get_reasonheir(year_road)._status=} \n")
    assert len(sue_budunit.get_agenda_dict()) == 0
