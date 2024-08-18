from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_time import (
    get_time_min_from_dt,
    add_time_hreg_ideaunit,
    time_str,  # "time"
    week_str,  # "week"
    get_jajatime_text,  # "jajatime"
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
    year4_no__leap_str,
    year4_withleap_str,
    year365_str,
    year366_str,
    month_str,
    hour_str,
    weekday_idea_str,
    year1_str,
    year2_str,
    year3_str,
    year4_str,
    node_0_100_str,
    node_1_4_str,
    node_1_96_str,
    node_2_4_str,
    node_2_96_str,
    node_3_4_str,
    node_3_96_str,
)
from datetime import datetime


def get_time_min_from_year(year_num: int) -> int:
    return get_time_min_from_dt(dt=datetime(year_num, 1, 1, 0, 0))


def _get_year_min_length(year_num: int) -> int:
    x_gogo = get_time_min_from_year(year_num)
    x_stop = get_time_min_from_year(year_num + 1)
    return x_stop - x_gogo


def test_BudUnit_get_time_min_from_dt_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    # THEN
    assert get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    assert get_time_min_from_dt(dt=datetime(1, 1, 1, 0, 0)) == 527040
    assert get_time_min_from_dt(dt=datetime(1, 1, 2, 0, 0)) == 527040 + 1440
    assert get_time_min_from_dt(dt=datetime(400, 1, 1, 0, 0)) == 210379680
    assert get_time_min_from_dt(dt=datetime(800, 1, 1, 0, 0)) == 420759360
    assert get_time_min_from_dt(dt=datetime(1200, 1, 1, 0, 0)) == 631139040


def test_get_time_min_from_year_ReturnsObj():
    assert _get_year_min_length(2000) == 527040
    assert _get_year_min_length(2001) == 525600
    assert _get_year_min_length(2002) == 525600
    assert _get_year_min_length(2003) == 525600
    assert _get_year_min_length(2004) == 527040


def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    # day_idea = sue_budunit.get_idea_obj(day_road)
    sue_budunit.tree_range_traverse_calc()
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


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario1():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     day_road = sue_budunit.make_road(jaja_road, day_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # day_idea = sue_budunit.get_idea_obj(day_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=day_road,
#         reason_premise=day_road,
#         reason_premise_open=0,
#         reason_premise_nigh=1,
#         reason_premise_divisor=1,
#     )
#     sue_budunit.set_fact(jaja_road, jaja_road, 0, 1440)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()
#     print(f"{sue_agenda=}")

#     # THEN
#     assert sue_agenda.get(clean_road)


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_day_idea_Scenario2():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     day_road = sue_budunit.make_road(jaja_road, day_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # day_idea = sue_budunit.get_idea_obj(day_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=day_road,
#         reason_premise=day_road,
#         reason_premise_open=360,
#         reason_premise_nigh=420,
#         reason_premise_divisor=1440,
#     )
#     sue_budunit.set_fact(jaja_road, jaja_road, 14400300, 14400480)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()

#     # THEN
#     assert sue_agenda.get(clean_road) != None


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_days_idea_Scenario0():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     days_road = sue_budunit.make_road(jaja_road, days_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # days_idea = sue_budunit.get_idea_obj(days_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=days_road,
#         reason_premise=days_road,
#         reason_premise_open=4,
#         reason_premise_nigh=5,
#         reason_premise_divisor=7,
#     )
#     sue_budunit.set_fact(jaja_road, jaja_road, 11, 12)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()

#     # THEN
#     assert sue_agenda.get(clean_road)


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_week_idea_Scenario0():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     week_road = sue_budunit.make_road(jaja_road, week_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # week_idea = sue_budunit.get_idea_obj(week_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=week_road,
#         reason_premise=week_road,
#         reason_premise_open=0,
#         reason_premise_nigh=1440,
#         reason_premise_divisor=10080,
#     )
#     sue_budunit.set_fact(jaja_road, jaja_road, 0, 1440)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()
#     print(f"{sue_agenda=}")

#     # THEN
#     assert sue_agenda.get(clean_road)


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_week_idea_Scenario1():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     week_road = sue_budunit.make_road(jaja_road, week_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # week_idea = sue_budunit.get_idea_obj(week_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=week_road,
#         reason_premise=week_road,
#         reason_premise_open=2880,
#         reason_premise_nigh=4220,
#         reason_premise_divisor=10080,
#     )
#     sue_budunit.set_fact(jaja_road, jaja_road, 100802880, 100804220)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()

#     # THEN
#     assert sue_agenda.get(clean_road) != None


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_weeks_idea_Scenario0():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     weeks_road = sue_budunit.make_road(jaja_road, weeks_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # weeks_idea = sue_budunit.get_idea_obj(weeks_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=weeks_road,
#         reason_premise=weeks_road,
#         reason_premise_open=4,
#         reason_premise_nigh=5,
#         reason_premise_divisor=7,
#     )
#     sue_budunit.set_fact(weeks_road, weeks_road, 11, 12)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()

#     # THEN
#     assert sue_agenda.get(clean_road)
#     assert 1 == 4


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario0():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     year_road = sue_budunit.make_road(jaja_road, year_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # year_idea = sue_budunit.get_idea_obj(year_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=year_road,
#         reason_premise=year_road,
#         reason_premise_open=0,
#         reason_premise_nigh=1440,
#         reason_premise_divisor=525600,
#     )
#     sue_budunit.set_fact(jaja_road, jaja_road, 0, 1440)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()
#     print(f"{sue_agenda=}")

#     # THEN
#     assert sue_agenda.get(clean_road)


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario1():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     year_road = sue_budunit.make_road(jaja_road, year_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     # jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # year_idea = sue_budunit.get_idea_obj(year_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=year_road,
#         reason_premise=year_road,
#         reason_premise_open=0,
#         reason_premise_nigh=1440,
#         reason_premise_divisor=525600,
#     )
#     sue_budunit.set_fact(jaja_road, jaja_road, 525600, 525600 + 1440)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()
#     print(f"{sue_agenda=}")

#     # THEN
#     assert sue_agenda.get(clean_road)


# def test_BudUnit_get_agenda_dict_ReturnsDictWith_year_idea_Scenario2():
#     # ESTABLISH
#     year4_gogo = get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
#     year4_stop = get_time_min_from_dt(dt=datetime(2000, 12, 31, 0, 0))

#     assert year4_stop - year4_gogo == 527040
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     year_road = sue_budunit.make_road(jaja_road, year_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     jaja_idea = sue_budunit.get_idea_obj(jaja_road)
#     # year_idea = sue_budunit.get_idea_obj(year_road)
#     sue_budunit.tree_range_traverse_calc()
#     casa_text = "casa"
#     casa_road = sue_budunit.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_budunit.make_road(casa_road, clean_text)
#     sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
#     sue_budunit.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
#     sue_budunit.edit_idea_attr(
#         clean_road,
#         reason_base=year_road,
#         reason_premise=year_road,
#         reason_premise_open=0,
#         reason_premise_nigh=1440,
#         reason_premise_divisor=525600,
#     )
#     sue_budunit.set_fact(year_road, year_road, 525600, 525600 + 1440)

#     # WHEN
#     sue_agenda = sue_budunit.get_agenda_dict()
#     print(f"{sue_agenda=}")

#     # THEN
#     assert sue_agenda.get(clean_road)
