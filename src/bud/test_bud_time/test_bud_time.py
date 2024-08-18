from src._road.road import RoadUnit, is_string_in_road
from src.bud.idea import IdeaUnit, ideaunit_shop
from src.bud.bud import budunit_shop, BudUnit
from src.bud.bud_time import (
    add_time_hreg_ideaunit,
    time_str,  # "time"
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

# from src.bud.examples.example_time import get_budunit_sue_TimeExample
from copy import deepcopy as copy_deepcopy


def kidless(x_budunit: BudUnit, idea_road: RoadUnit) -> IdeaUnit:
    x_ideaunit = copy_deepcopy(x_budunit.get_idea_obj(idea_road))
    x_ideaunit._kids = {}
    x_ideaunit._fund_onset = None
    x_ideaunit._fund_cease = None
    x_ideaunit._fund_ratio = None
    x_ideaunit._fund_coin = None
    x_ideaunit._is_expanded = None
    return x_ideaunit


def kidlist(x_budunit: BudUnit, idea_road: RoadUnit) -> set[RoadUnit]:
    x_ideaunit = x_budunit.get_idea_obj(idea_road)
    return set(x_ideaunit._kids.keys())


def compare_kidless_ideas(src_budunit: BudUnit, x_budunit: BudUnit):
    # src_budunit.settle_bud()
    # x_budunit.settle_bud()

    for src_road in src_budunit._idea_dict.keys():
        # print(f"'{src_road}'")

        # TODO Fix these failures to pass assert that are skipped.
        if not is_string_in_road(
            "ZZ;time;jajatime;years;", src_road
        ) and src_road not in {
            "ZZ;time;tech;400 year segment;0-100-25 leap years;4year with leap",
            "ZZ;time;tech;400 year segment;100-104-0 leap years;4year wo leap",
            "ZZ;time;tech;400 year segment;104-200-24 leap years;4year with leap",
            "ZZ;time;tech;400 year segment;200-204-0 leap years;4year wo leap",
            "ZZ;time;tech;400 year segment;204-300-24 leap years;4year with leap",
        }:
            if kidless(src_budunit, src_road) != kidless(x_budunit, src_road):
                print(f"'{src_road}' failure")
                src_ideaunit = src_budunit.get_idea_obj(src_road)
                x_ideaunit = x_budunit.get_idea_obj(src_road)
                print(f"{src_ideaunit._begin=} \t\t {x_ideaunit._begin=}")
                print(f"{src_ideaunit._close=} \t\t {x_ideaunit._close=}")
                print(f"{src_ideaunit._numor=} \t\t {x_ideaunit._numor=}")
                print(f"{src_ideaunit._denom=} \t\t {x_ideaunit._denom=}")
                print(f"{src_ideaunit._addin=} \t\t {x_ideaunit._addin=}")
                print(f"{src_ideaunit._reest=} \t\t {x_ideaunit._reest=}")
                # print(f"{src_ideaunit._parent_road=} \t\t {x_ideaunit._parent_road=}")
            assert kidless(src_budunit, src_road) == kidless(x_budunit, src_road)


def compare_kidlists(src_budunit: BudUnit, x_budunit: BudUnit):
    for src_road in src_budunit._idea_dict.keys():
        if kidlist(src_budunit, src_road) != kidlist(x_budunit, src_road):
            print(f"   Kidlist failure at {src_road=}")
            print(f"{kidlist(src_budunit, src_road)=}")
        assert kidlist(src_budunit, src_road) == kidlist(x_budunit, src_road)


def test_add_time_hreg_ideaunit_ReturnsObjWith_days():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    days_road = sue_budunit.make_road(jaja_road, days_str())
    print(f"{time_road=}")
    print(f"{jaja_road=}")
    print(f"{day_road=}")
    assert not sue_budunit.idea_exists(time_road)
    assert not sue_budunit.idea_exists(jaja_road)
    assert not sue_budunit.idea_exists(day_road)
    assert not sue_budunit.idea_exists(days_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(jaja_road)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    assert jaja_idea._begin == 0
    assert jaja_idea._close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea._gogo_want == 0
    assert day_idea._stop_want == 1440
    assert day_idea._denom == 1440
    assert day_idea._reest
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea._denom == 1440
    assert not days_idea._reest


def test_add_time_hreg_ideaunit_ReturnsObjWith_weeks():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    week_road = sue_budunit.make_road(jaja_road, week_str())
    sun_road = sue_budunit.make_road(week_road, get_sun())
    mon_road = sue_budunit.make_road(week_road, get_mon())
    tue_road = sue_budunit.make_road(week_road, get_tue())
    wed_road = sue_budunit.make_road(week_road, get_wed())
    thu_road = sue_budunit.make_road(week_road, get_thu())
    fri_road = sue_budunit.make_road(week_road, get_fri())
    sat_road = sue_budunit.make_road(week_road, get_sat())
    weeks_road = sue_budunit.make_road(jaja_road, weeks_str())

    assert not sue_budunit.idea_exists(week_road)
    assert not sue_budunit.idea_exists(sun_road)
    assert not sue_budunit.idea_exists(mon_road)
    assert not sue_budunit.idea_exists(tue_road)
    assert not sue_budunit.idea_exists(wed_road)
    assert not sue_budunit.idea_exists(thu_road)
    assert not sue_budunit.idea_exists(fri_road)
    assert not sue_budunit.idea_exists(sat_road)
    assert not sue_budunit.idea_exists(weeks_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(week_road)
    week_idea = sue_budunit.get_idea_obj(week_road)
    assert week_idea._gogo_want == 0
    assert week_idea._stop_want == 10080
    assert week_idea._denom == 10080
    assert week_idea._reest
    assert sue_budunit.idea_exists(sun_road)
    assert sue_budunit.idea_exists(mon_road)
    assert sue_budunit.idea_exists(tue_road)
    assert sue_budunit.idea_exists(wed_road)
    assert sue_budunit.idea_exists(thu_road)
    assert sue_budunit.idea_exists(fri_road)
    assert sue_budunit.idea_exists(sat_road)
    assert sue_budunit.idea_exists(weeks_road)
    weeks_idea = sue_budunit.get_idea_obj(weeks_road)
    assert weeks_idea._denom == 10080
    assert not weeks_idea._reest


def test_add_time_hreg_ideaunit_ReturnsObjWith_years():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    year_road = sue_budunit.make_road(jaja_road, year_str())
    years_road = sue_budunit.make_road(jaja_road, years_str())
    jan_road = sue_budunit.make_road(year_road, jan_str())
    feb_road = sue_budunit.make_road(year_road, feb_str())
    mar_road = sue_budunit.make_road(year_road, mar_str())
    apr_road = sue_budunit.make_road(year_road, apr_str())
    may_road = sue_budunit.make_road(year_road, may_str())
    jun_road = sue_budunit.make_road(year_road, jun_str())
    jul_road = sue_budunit.make_road(year_road, jul_str())
    aug_road = sue_budunit.make_road(year_road, aug_str())
    sep_road = sue_budunit.make_road(year_road, sep_str())
    oct_road = sue_budunit.make_road(year_road, oct_str())
    nov_road = sue_budunit.make_road(year_road, nov_str())
    dec_road = sue_budunit.make_road(year_road, dec_str())
    assert not sue_budunit.idea_exists(jan_road)
    assert not sue_budunit.idea_exists(feb_road)
    assert not sue_budunit.idea_exists(mar_road)
    assert not sue_budunit.idea_exists(apr_road)
    assert not sue_budunit.idea_exists(may_road)
    assert not sue_budunit.idea_exists(jun_road)
    assert not sue_budunit.idea_exists(jul_road)
    assert not sue_budunit.idea_exists(aug_road)
    assert not sue_budunit.idea_exists(sep_road)
    assert not sue_budunit.idea_exists(oct_road)
    assert not sue_budunit.idea_exists(nov_road)
    assert not sue_budunit.idea_exists(dec_road)
    assert not sue_budunit.idea_exists(year_road)
    assert not sue_budunit.idea_exists(years_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(year_road)
    print(f"{year_road=}")
    year_idea = sue_budunit.get_idea_obj(year_road)
    assert year_idea._gogo_want == 0
    assert year_idea._stop_want == 525600
    assert year_idea._denom == 525600
    assert year_idea._reest
    assert sue_budunit.idea_exists(years_road)
    assert sue_budunit.idea_exists(jan_road)
    assert sue_budunit.idea_exists(feb_road)
    assert sue_budunit.idea_exists(mar_road)
    assert sue_budunit.idea_exists(apr_road)
    assert sue_budunit.idea_exists(may_road)
    assert sue_budunit.idea_exists(jun_road)
    assert sue_budunit.idea_exists(jul_road)
    assert sue_budunit.idea_exists(aug_road)
    assert sue_budunit.idea_exists(sep_road)
    assert sue_budunit.idea_exists(oct_road)
    assert sue_budunit.idea_exists(nov_road)
    assert sue_budunit.idea_exists(dec_road)
    assert sue_budunit.get_idea_obj(jan_road)._gogo_want == 0
    assert sue_budunit.get_idea_obj(feb_road)._gogo_want == 44640
    assert sue_budunit.get_idea_obj(mar_road)._gogo_want == 84960
    assert sue_budunit.get_idea_obj(apr_road)._gogo_want == 129600
    assert sue_budunit.get_idea_obj(may_road)._gogo_want == 172800
    assert sue_budunit.get_idea_obj(jun_road)._gogo_want == 217440
    assert sue_budunit.get_idea_obj(jul_road)._gogo_want == 260640
    assert sue_budunit.get_idea_obj(aug_road)._gogo_want == 305280
    assert sue_budunit.get_idea_obj(sep_road)._gogo_want == 349920
    assert sue_budunit.get_idea_obj(oct_road)._gogo_want == 393120
    assert sue_budunit.get_idea_obj(nov_road)._gogo_want == 437760
    assert sue_budunit.get_idea_obj(dec_road)._gogo_want == 480960
    assert sue_budunit.get_idea_obj(jan_road)._stop_want == 44640
    assert sue_budunit.get_idea_obj(feb_road)._stop_want == 84960
    assert sue_budunit.get_idea_obj(mar_road)._stop_want == 129600
    assert sue_budunit.get_idea_obj(apr_road)._stop_want == 172800
    assert sue_budunit.get_idea_obj(may_road)._stop_want == 217440
    assert sue_budunit.get_idea_obj(jun_road)._stop_want == 260640
    assert sue_budunit.get_idea_obj(jul_road)._stop_want == 305280
    assert sue_budunit.get_idea_obj(aug_road)._stop_want == 349920
    assert sue_budunit.get_idea_obj(sep_road)._stop_want == 393120
    assert sue_budunit.get_idea_obj(oct_road)._stop_want == 437760
    assert sue_budunit.get_idea_obj(nov_road)._stop_want == 480960
    assert sue_budunit.get_idea_obj(dec_road)._stop_want == 525600

    years_idea = sue_budunit.get_idea_obj(years_road)
    assert years_idea._gogo_want == 0
    assert years_idea._stop_want == 2800
    assert not years_idea._reest

    # assert sue_budunit is not None
    # assert sue_budunit.idea_exists(time_road)
    # assert sue_budunit.idea_exists(tech_road)
    # assert sue_budunit.idea_exists(week_road)
    # assert sue_budunit.idea_exists(jaja_road)
    # assert kidlist(sue_budunit, time_road) == kidlist(ex1_budunit, time_road)
    # assert kidlist(sue_budunit, tech_road) == kidlist(ex1_budunit, tech_road)
    # assert kidlist(sue_budunit, year365_road) == kidlist(ex1_budunit, year365_road)
    # assert kidlist(sue_budunit, year366_road) == kidlist(ex1_budunit, year366_road)
    # assert kidlist(sue_budunit, day_road) == kidlist(ex1_budunit, day_road)
    # assert kidlist(sue_budunit, hour_road) == kidlist(ex1_budunit, hour_road)
    # assert kidlist(sue_budunit, month_road) == kidlist(ex1_budunit, month_road)
    # assert kidlist(sue_budunit, week_road) == kidlist(ex1_budunit, week_road)
    # assert kidlist(sue_budunit, jaja_road) == kidlist(ex1_budunit, jaja_road)
    # compare_kidlists(ex1_budunit, sue_budunit)

    # compare_kidless_ideas(ex1_budunit, sue_budunit)
    # # assert sue_budunit == ex1_budunit


# def test_add_time_hreg_ideaunit_ReturnsObj():
#     # ESTABLISH
# c400_road = sue_budunit.make_road(tech_road, c400_str())
# year4_noleap_road = sue_budunit.make_road(tech_road, year4_no__leap_str())
# year4_withleap_road = sue_budunit.make_road(tech_road, year4_withleap_str())
# year365_road = sue_budunit.make_road(tech_road, year365_str())
# year366_road = sue_budunit.make_road(tech_road, year366_str())
# month_road = sue_budunit.make_road(tech_road, month_str())
# hour_road = sue_budunit.make_road(tech_road, hour_str())
# weekday_idea_road = sue_budunit.make_road(tech_road, weekday_idea_str())

# ex1_budunit = get_budunit_sue_TimeExample()

#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     tech_road = sue_budunit.make_road(time_road, tech_str())
#     week_road = sue_budunit.make_road(tech_road, week_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     c400_road = sue_budunit.make_road(tech_road, c400_str())
#     year4_noleap_road = sue_budunit.make_road(tech_road, year4_no__leap_str())
#     year4_withleap_road = sue_budunit.make_road(tech_road, year4_withleap_str())
#     year365_road = sue_budunit.make_road(tech_road, year365_str())
#     year366_road = sue_budunit.make_road(tech_road, year366_str())
#     month_road = sue_budunit.make_road(tech_road, month_str())
#     day_road = sue_budunit.make_road(tech_road, day_str())
#     hour_road = sue_budunit.make_road(tech_road, hour_str())
#     weekday_idea_road = sue_budunit.make_road(tech_road, weekday_idea_str())

#     ex1_budunit = get_budunit_sue_TimeExample()

#     assert not sue_budunit.idea_exists(time_road)
#     assert not sue_budunit.idea_exists(tech_road)
#     assert not sue_budunit.idea_exists(week_road)

#     # WHEN
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)

#     # THEN
#     assert sue_budunit is not None
#     assert sue_budunit.idea_exists(time_road)
#     assert sue_budunit.idea_exists(tech_road)
#     assert sue_budunit.idea_exists(week_road)
#     assert sue_budunit.idea_exists(jaja_road)
#     assert kidlist(sue_budunit, time_road) == kidlist(ex1_budunit, time_road)
#     assert kidlist(sue_budunit, tech_road) == kidlist(ex1_budunit, tech_road)
#     assert kidlist(sue_budunit, year365_road) == kidlist(ex1_budunit, year365_road)
#     assert kidlist(sue_budunit, year366_road) == kidlist(ex1_budunit, year366_road)
#     assert kidlist(sue_budunit, day_road) == kidlist(ex1_budunit, day_road)
#     assert kidlist(sue_budunit, hour_road) == kidlist(ex1_budunit, hour_road)
#     assert kidlist(sue_budunit, month_road) == kidlist(ex1_budunit, month_road)
#     assert kidlist(sue_budunit, week_road) == kidlist(ex1_budunit, week_road)
#     assert kidlist(sue_budunit, jaja_road) == kidlist(ex1_budunit, jaja_road)
#     compare_kidlists(ex1_budunit, sue_budunit)

#     compare_kidless_ideas(ex1_budunit, sue_budunit)
#     # assert sue_budunit == ex1_budunit


# def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario1():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_hreg_ideas(c400_count=7)

#     # WHEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     x_begin = 1440
#     x_close = 4 * 1440
#     ranged_ideas = sue_budunit.get_idea_ranged_kids(week_road, x_begin, x_close)

#     # THEN
#     # for idea_x in ranged_ideas.values():
#     #     print(
#     #         f"{x_begin=} {x_close=} {idea_x._label=} {idea_x._begin=} {idea_x._close=} "
#     #     )
#     assert len(ranged_ideas) == 3


# def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario2():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_hreg_ideas(c400_count=7)

#     # WHEN THEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     assert len(sue_budunit.get_idea_ranged_kids(week_road, begin=0, close=1440)) == 1
#     assert len(sue_budunit.get_idea_ranged_kids(week_road, begin=0, close=2000)) == 2
#     assert len(sue_budunit.get_idea_ranged_kids(week_road, begin=0, close=3000)) == 3


# def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario3():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_hreg_ideas(c400_count=7)

#     # WHEN THEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     assert len(sue_budunit.get_idea_ranged_kids(idea_road=week_road, begin=0)) == 1
#     assert len(sue_budunit.get_idea_ranged_kids(idea_road=week_road, begin=1440)) == 1


# def test_BudUnit_create_axiom_facts_CorrectlyCreatesNthLevelAxiomFact_Scenario4_1():
#     # ESTABLISH
#     sue_bud = get_budunit_sue_TimeExample()
#     time_road = sue_bud.make_l1_road("time")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")
#     timetech_road = sue_bud.make_road(time_road, "tech")
#     sue_bud.set_fact(jajatime_road, jajatime_road, open=1500, nigh=1500)

#     # WHEN
#     x_axiom_factunits = sue_bud._get_axiom_factunits()

#     # THEN
#     yr400_road = sue_bud.make_road(jajatime_road, "400 year segment")
#     yr400s_road = sue_bud.make_road(jajatime_road, "400 year segments")
#     days_road = sue_bud.make_road(jajatime_road, "days")
#     day_road = sue_bud.make_road(jajatime_road, "day")
#     week_road = sue_bud.make_road(jajatime_road, "week")

#     assert x_axiom_factunits.get(yr400_road).open == 1500
#     assert x_axiom_factunits.get(yr400_road).nigh == 1500
#     assert x_axiom_factunits.get(yr400s_road).open > 0
#     assert x_axiom_factunits.get(yr400s_road).open < 1
#     assert x_axiom_factunits.get(yr400s_road).nigh > 0
#     assert x_axiom_factunits.get(yr400s_road).nigh < 1
#     assert x_axiom_factunits.get(days_road).open >= 1
#     assert x_axiom_factunits.get(days_road).open <= 2
#     assert x_axiom_factunits.get(days_road).nigh >= 1
#     assert x_axiom_factunits.get(days_road).nigh <= 2
#     assert x_axiom_factunits.get(day_road).open == 60
#     assert x_axiom_factunits.get(day_road).nigh == 60
#     assert x_axiom_factunits.get(week_road).open == 1500
#     assert int(x_axiom_factunits.get(week_road).nigh) == 1500
#     assert x_axiom_factunits.get(week_road).open == 1500
#     assert int(x_axiom_factunits.get(week_road).nigh) == 1500


# def test_BudUnit_create_axiom_facts_CorrectlyCreatesNthLevelAxiomFact_Scenario5():
#     # ESTABLISH
#     sue_bud = get_budunit_sue_TimeExample()
#     time_road = sue_bud.make_l1_road("time")
#     timetech_road = sue_bud.make_road(time_road, "tech")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")
#     sue_bud.set_fact(jajatime_road, jajatime_road, 1500, nigh=1063954002)

#     # WHEN
#     lhu = sue_bud._get_axiom_factunits()

#     # THEN
#     yr400_road = sue_bud.make_road(jajatime_road, "400 year segment")
#     yr400s_road = sue_bud.make_road(jajatime_road, "400 year segments")
#     days_road = sue_bud.make_road(jajatime_road, "days")
#     day_road = sue_bud.make_road(jajatime_road, "day")
#     week_road = sue_bud.make_road(jajatime_road, "week")

#     assert lhu[yr400_road].open == 0
#     assert lhu[yr400_road].nigh == 210379680
#     assert lhu[yr400s_road].open > 0
#     assert lhu[yr400s_road].open < 1
#     assert lhu[yr400s_road].nigh > 5
#     assert lhu[yr400s_road].nigh < 6
#     axiom_days = lhu.get(days_road)
#     assert int(axiom_days.open) == 1  # 0 / 1440
#     assert int(axiom_days.nigh) == 738856  # 1063953183 / 1440
#     axiom_day = lhu.get(day_road)
#     assert axiom_day.open == 0  # 0 / 1440
#     assert axiom_day.nigh == 1440  # 1362  # 1063953183 / 1440
#     axiom_jajatime_week = lhu.get(week_road)
#     assert axiom_jajatime_week.open == 0  # 0 / 1440
#     assert int(axiom_jajatime_week.nigh) == 10080  # 1063953183 / 1440
#     axiom_timetech_week = lhu.get(week_road)
#     assert axiom_timetech_week.open == 0  # 0 / 1440
#     assert int(axiom_timetech_week.nigh) == 10080  # 1063953183 / 1440


# def test_BudUnit_create_axiom_facts_CorrectlyCreatesNthLevelAxiomFact_Scenario6():
#     # ESTABLISH
#     sue_bud = get_budunit_sue_TimeExample()
#     time_road = sue_bud.make_l1_road("time")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")
#     sue_bud.set_fact(jajatime_road, jajatime_road, 1063954000, nigh=1063954002)

#     # WHEN
#     lhu = sue_bud._get_axiom_factunits()

#     # THEN
#     yr400_road = sue_bud.make_road(jajatime_road, "400 year segment")
#     yr400s_road = sue_bud.make_road(jajatime_road, "400 year segments")
#     days_road = sue_bud.make_road(jajatime_road, "days")
#     day_road = sue_bud.make_road(jajatime_road, "day")

#     assert lhu.get(yr400_road).open == 12055600.0
#     assert lhu.get(yr400_road).nigh == 12055602.0
#     assert lhu.get(yr400s_road).open > 5
#     assert lhu.get(yr400s_road).open < 6
#     assert lhu.get(yr400s_road).nigh > 5
#     assert lhu.get(yr400s_road).nigh < 6
#     axiom_days = lhu.get(days_road)
#     assert int(axiom_days.open) == 738856  # 1063954000 / 1440
#     assert int(axiom_days.nigh) == 738856  # 1063954000 / 1440
#     axiom_day = lhu.get(day_road)
#     assert axiom_day.open == 1360  # 0 / 1440
#     assert int(axiom_day.nigh) == 1362  # 1063953183 / 1440


# def test_BudUnit_create_axiom_facts_CorrectlyCreatesNthLevelAxiomFact_Scenario7():
#     # ESTABLISH
#     sue_bud = get_budunit_sue_TimeExample()
#     time_road = sue_bud.make_l1_road("time")
#     timetech_road = sue_bud.make_road(time_road, "tech")
#     techweek_road = sue_bud.make_road(timetech_road, "week")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")

#     # WHEN minute range that should be Thursday to Monday midnight
#     sue_bud.set_fact(jajatime_road, jajatime_road, 1063951200, nigh=1063956960)
#     lhu = sue_bud._get_axiom_factunits()

#     # THEN
#     week_road = sue_bud.make_road(jajatime_road, "week")
#     week_open = lhu.get(week_road).open
#     week_nigh = lhu.get(week_road).nigh
#     week_text = "week"
#     print(
#         f"for {sue_bud.make_road(jajatime_road,week_text)}: {week_open=} {week_nigh=}"
#     )
#     assert lhu.get(week_road).open == 7200
#     assert lhu.get(week_road).nigh == 2880

#     week_open = lhu.get(week_road).open
#     week_nigh = lhu.get(week_road).nigh
#     print(
#         f"for {sue_bud.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
#     )
#     assert lhu.get(week_road).open == 7200
#     assert lhu.get(week_road).nigh == 2880
#     print(f"{techweek_road=}")
#     print(lhu[techweek_road])
#     print(lhu[sue_bud.make_road(techweek_road, "Thursday")])
#     print(lhu[sue_bud.make_road(techweek_road, "Friday")])
#     print(lhu[sue_bud.make_road(techweek_road, "Saturday")])
#     print(lhu[sue_bud.make_road(techweek_road, "Sunday")])
#     print(lhu[sue_bud.make_road(techweek_road, "Monday")])
#     print(lhu[sue_bud.make_road(techweek_road, "Tuesday")])
#     print(lhu[sue_bud.make_road(techweek_road, "Wednesday")])


# def test_BudUnit_create_axiom_facts_CorrectlyCreatesNthLevelAxiomFact_Scenario8():
#     # ESTABLISH
#     sue_bud = get_budunit_sue_TimeExample()
#     time_road = sue_bud.make_l1_road("time")
#     timetech_road = sue_bud.make_road(time_road, "tech")
#     techweek_road = sue_bud.make_road(timetech_road, "week")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")

#     # WHEN minute range that should be Thursday to Monday midnight
#     sue_bud.set_fact(jajatime_road, jajatime_road, 1063951200, nigh=1063951200)
#     lhu = sue_bud._get_axiom_factunits()

#     # THEN
#     week_open = lhu[techweek_road].open
#     week_nigh = lhu[techweek_road].nigh
#     print(f"for {techweek_road}: {week_open=} {week_nigh=}")
#     assert lhu[techweek_road].open == 7200
#     assert lhu[techweek_road].nigh == 7200

#     week_road = sue_bud.make_road(jajatime_road, "week")
#     week_open = lhu.get(week_road).open
#     week_nigh = lhu.get(week_road).nigh
#     week_text = "week"
#     print(
#         f"for {sue_bud.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
#     )
#     assert lhu.get(week_road).open == 7200
#     assert lhu.get(week_road).nigh == 7200
#     print(lhu.get(techweek_road))
#     print(lhu.get(sue_bud.make_road(techweek_road, "Thursday")))
#     print(lhu.get(sue_bud.make_road(techweek_road, "Friday")))
#     print(lhu.get(sue_bud.make_road(techweek_road, "Saturday")))
#     print(lhu.get(sue_bud.make_road(techweek_road, "Sunday")))
#     print(lhu.get(sue_bud.make_road(techweek_road, "Monday")))
#     print(lhu.get(sue_bud.make_road(techweek_road, "Tuesday")))
#     print(lhu.get(sue_bud.make_road(techweek_road, "Wednesday")))


# def test_BudUnit_get_agenda_dict_DoesNotReturnPledgeItemsOutsideRange():
#     # ESTABLISH
#     sue_text = "Sue"
#     sue_bud = get_budunit_sue_TimeExample()
#     clean_text = "clean"
#     clean_road = sue_bud.make_l1_road(clean_text)
#     sue_bud.set_l1_idea(ideaunit_shop(clean_text, pledge=True))
#     time_road = sue_bud.make_l1_road("time")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")
#     jajaday = sue_bud.make_road(jajatime_road, "day")

#     sue_bud.edit_idea_attr(
#         road=clean_road,
#         reason_base=jajatime_road,
#         reason_premise=jajaday,
#         begin=480,
#         close=480,
#     )

#     # WHEN
#     open_x = 1063971180
#     nigh_x1 = 2063971523
#     sue_bud.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x1)

#     # THEN
#     agenda_dict = sue_bud.get_agenda_dict()
#     print(f"{agenda_dict.keys()=}")
#     assert len(agenda_dict) == 1
#     assert clean_road in agenda_dict.keys()

#     # WHEN
#     nigh_x2 = 1063971923
#     sue_bud.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x2)

#     # THEN
#     agenda_dict = sue_bud.get_agenda_dict()
#     assert len(agenda_dict) == 0


# def test_BudUnit_create_agenda_item_CorrectlyCreatesAllBudAttributes():
#     # WHEN "I am cleaning the cookery since I'm in the flat and it's 8am and it's dirty and it's for my family"

#     # ESTABLISH
#     sue_bud = get_budunit_sue_TimeExample()
#     assert len(sue_bud._accts) == 0
#     assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
#     assert len(sue_bud._idearoot._kids) == 1

#     clean_things_text = "cleaning things"
#     clean_things_road = sue_bud.make_l1_road(clean_things_text)
#     clean_cookery_text = "clean cookery"
#     clean_cookery_road = sue_bud.make_road(clean_things_road, clean_cookery_text)
#     clean_cookery_idea = ideaunit_shop(
#         clean_cookery_text, _parent_road=clean_things_road
#     )
#     print(f"{clean_cookery_idea.get_road()=}")
#     house_text = "house"
#     house_road = sue_bud.make_l1_road(house_text)
#     cookery_room_text = "cookery room"
#     cookery_room_road = sue_bud.make_road(house_road, cookery_room_text)
#     cookery_dirty_text = "dirty"
#     cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_text)

#     # create gregorian timeline
#     time_road = sue_bud.make_l1_road("time")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")
#     daytime_road = sue_bud.make_road(jajatime_road, "day")
#     open_8am = 480
#     nigh_8am = 480

#     dirty_cookery_reason = reasonunit_shop(cookery_room_road)
#     dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
#     clean_cookery_idea.set_reasonunit(reason=dirty_cookery_reason)

#     daytime_reason = reasonunit_shop(daytime_road)
#     daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
#     clean_cookery_idea.set_reasonunit(reason=daytime_reason)

#     family_text = ",family"
#     awardlink_z = awardlink_shop(group_id=family_text)
#     clean_cookery_idea.set_awardlink(awardlink_z)

#     assert len(sue_bud._accts) == 0
#     assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
#     assert len(sue_bud._idearoot._kids) == 1
#     assert sue_bud.get_idea_obj(daytime_road)._begin == 0
#     assert sue_bud.get_idea_obj(daytime_road)._close == 1440
#     print(f"{clean_cookery_idea.get_road()=}")

#     # ESTABLISH
#     sue_bud.set_dominate_pledge_idea(idea_kid=clean_cookery_idea)

#     # THEN
#     # for idea_kid in sue_bud._idearoot._kids.keys():
#     #     print(f"  {idea_kid=}")

#     print(f"{clean_cookery_idea.get_road()=}")
#     assert sue_bud.get_idea_obj(clean_cookery_road) is not None
#     assert sue_bud.get_idea_obj(clean_cookery_road)._label == clean_cookery_text
#     assert sue_bud.get_idea_obj(clean_cookery_road).pledge
#     assert len(sue_bud.get_idea_obj(clean_cookery_road)._reasonunits) == 2
#     assert sue_bud.get_idea_obj(clean_things_road) is not None
#     assert sue_bud.get_idea_obj(cookery_room_road) is not None
#     assert sue_bud.get_idea_obj(cookery_dirty_road) is not None
#     assert sue_bud.get_idea_obj(daytime_road)._begin == 0
#     assert sue_bud.get_idea_obj(daytime_road)._close == 1440
#     assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
#     assert sue_bud.get_acctunit_group_ids_dict().get(family_text) is None

#     assert len(sue_bud._idearoot._kids) == 3

# def test_IdeaCore_get_agenda_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
#     # ESTABLISH
#     sue_bud = get_budunit_sue_TimeExample()

#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     laundry_text = "do_laundry"
#     laundry_road = sue_bud.make_road(casa_road, laundry_text)
#     sue_bud.set_l1_idea(ideaunit_shop(casa_text))
#     sue_bud.set_idea(ideaunit_shop(laundry_text, pledge=True), casa_road)
#     time_road = sue_bud.make_l1_road("time")
#     jajatime_road = sue_bud.make_road(time_road, "jajatime")
#     sue_bud.edit_idea_attr(
#         road=laundry_road,
#         reason_base=jajatime_road,
#         reason_premise=jajatime_road,
#         reason_premise_open=3420.0,
#         reason_premise_nigh=3420.0,
#         reason_premise_divisor=10080.0,
#     )
#     print("set first fact")
#     sue_bud.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064135133)
#     print("get 1st agenda dictionary")
#     sue_agenda_dict = sue_bud.get_agenda_dict()
#     print(f"{sue_agenda_dict.keys()=}")
#     assert sue_agenda_dict == {}

#     laundry_idea = sue_bud.get_idea_obj(laundry_road)
#     laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
#     laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
#     laundry_factheir = laundry_idea._factheirs.get(jajatime_road)
#     # print(
#     #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.open % 10080=}"
#     # )
#     # print(
#     #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.nigh % 10080=}"
#     # )
#     # print(f"{laundry_reasonheir.base=} {laundry_premise=}")
#     # for x_ideaunit in sue_bud._idea_dict.values():
#     #     if x_ideaunit._label in [laundry_text]:
#     #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
#     #         print(f"{x_ideaunit._kids.keys()=}")

#     # WHEN
#     print("set 2nd fact")
#     sue_bud.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064136133)
#     print("get 2nd agenda dictionary")
#     sue_agenda_dict = sue_bud.get_agenda_dict()
#     print(f"{sue_agenda_dict.keys()=}")

#     laundry_idea = sue_bud.get_idea_obj(laundry_road)
#     laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
#     laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
#     laundry_factheir = laundry_idea._factheirs.get(jajatime_road)
#     # print(
#     #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.open % 10080=}"
#     # )
#     # print(
#     #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.nigh % 10080=}"
#     # )
#     # for x_ideaunit in sue_bud._idea_dict.values():
#     #     if x_ideaunit._label in [laundry_text]:
#     #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
#     #         print(f"{x_ideaunit._kids.keys()=}")
#     #         jaja_factheir = x_ideaunit._factheirs.get(jajatime_road)
#     #         print(f"{jaja_factheir.open % 10080=}")
#     #         print(f"{jaja_factheir.nigh % 10080=}")

#     # THEN
#     assert sue_agenda_dict == {}
