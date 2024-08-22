from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_time import (
    get_year_road,
    get_time_min_from_dt,
    add_time_hreg_ideaunit,
    time_str,  # "time"
    week_str,  # "week"
    get_jajatime_text,
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
    get_sun,  # "Sunday"
    get_mon,  # "Monday"
    get_tue,  # "Tuesday"
    get_wed,  # "Wednesday"
    get_thu,  # "Thursday"
    get_fri,  # "Friday"
    get_sat,  # "Saturday"
    week_str,  # "week"
    weeks_str,  # f"{get_week()}s"
    day_str,  # "day"
    days_str,  # f"{get_day()}s"
    year_str,
    years_str,
    jan_str,
    feb_str,
    mar_str,
    apr_str,
    may_str,
    jun_str,
    jul_str,
    aug_str,
    sep_str,
    oct_str,
    nov_str,
    dec_str,
)
from datetime import datetime


def get_time_min_from_year(year_num: int) -> int:
    return get_time_min_from_dt(dt=datetime(year_num, 1, 1, 0, 0))


def _get_year_min_length(year_num: int) -> int:
    x_gogo = get_time_min_from_year(year_num)
    x_stop = get_time_min_from_year(year_num + 1)
    return x_stop - x_gogo


def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 0, 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario2():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 14400300, 14400480)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_road) != None


def test_BudUnit_get_agenda_dict_ReturnsDictWith_days_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    days_road = sue_budunit.make_road(jaja_road, days_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 11 * 1400, 12 * 1400)

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
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    week_road = sue_budunit.make_road(jaja_road, week_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 0, 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_week_idea_Scenario1():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    week_road = sue_budunit.make_road(jaja_road, week_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 100802880, 100804220)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_road) != None


def test_BudUnit_get_agenda_dict_ReturnsDictWith_weeks_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    weeks_road = sue_budunit.make_road(jaja_road, weeks_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    print(f"{jaja_idea._begin=} {jaja_idea._close=}")
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
    sue_budunit.set_fact(jaja_road, jaja_road, 11 * 10080, 12 * 10080)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    year_road = get_year_road(sue_budunit, jaja_road)
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 0, 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)

    # WHEN
    sue_budunit.set_fact(jaja_road, jaja_road, 1444, 2880)
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert not sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario1():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    year_road = get_year_road(sue_budunit, jaja_road)

    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)


def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario2():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    year_road = get_year_road(sue_budunit, jaja_road)

    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
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
    sue_budunit.set_fact(jaja_road, jaja_road, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_budunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_road)

    # WHEN / THEN
    yr2000mar1 = get_time_min_from_dt(dt=datetime(2000, 3, 1, 0, 0))
    yr2000mar2 = get_time_min_from_dt(dt=datetime(2000, 3, 2, 0, 0))
    yr2000dec1 = get_time_min_from_dt(dt=datetime(2000, 12, 1, 0, 0))
    yr2000dec2 = get_time_min_from_dt(dt=datetime(2000, 12, 2, 0, 0))
    yr2004mar1 = get_time_min_from_dt(dt=datetime(2004, 3, 1, 0, 0))
    yr2004mar2 = get_time_min_from_dt(dt=datetime(2004, 3, 2, 0, 0))

    sue_budunit.set_fact(jaja_road, jaja_road, yr2000mar1, yr2000mar1 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 1
    sue_budunit.set_fact(jaja_road, jaja_road, yr2000mar2, yr2000mar2 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 0
    sue_budunit.set_fact(jaja_road, jaja_road, yr2004mar1, yr2004mar1 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 1
    sue_budunit.set_fact(jaja_road, jaja_road, yr2000mar2, yr2004mar2 + 1440)
    assert len(sue_budunit.get_agenda_dict()) == 1
