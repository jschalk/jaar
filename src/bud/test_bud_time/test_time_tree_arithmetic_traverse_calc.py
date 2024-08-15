from src.bud.bud import budunit_shop
from src.bud.bud_time import (
    _get_jajatime_week_legible_text,
    add_time_hreg_ideaunit,
    time_str,  # "time"
    tech_str,  # "tech"
    week_str,  # "week"
    min_str,  # "minutes"
    get_jajatime_text,  # "jajatime"
    get_Sun,  # "Sunday"
    get_Mon,  # "Monday"
    get_Tue,  # "Tuesday"
    get_Wed,  # "Wednesday"
    get_Thu,  # "Thursday"
    get_Fri,  # "Friday"
    get_Sat,  # "Saturday"
    c400_str,  # "400 year segment"
    c400s_str,  # f"{get_c400()}s"
    week_str,  # "week"
    weeks_str,  # f"{get_week()}s"
    day_str,  # "day"
    days_str,  # f"{get_day()}s"
    Jan,  # "Jan"
    Feb28,  # "Feb28"
    Feb29,  # "Feb29"
    Mar,  # "Mar"
    Apr,  # "Apr"
    May,  # "May"
    Jun,  # "Jun"
    Jul,  # "Jul"
    Aug,  # "Aug"
    Sep,  # "Sep"
    Oct,  # "Oct"
    Nov,  # "Nov"
    Dec,  # "Dec"
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


def test_BudUnit_tree_arithmetic_traverse_calc_Sets_day_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(jaja_road)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    assert jaja_idea._begin == 0
    assert jaja_idea._close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea._denom == 1022679
    assert not day_idea._gogo_calc
    assert not day_idea._stop_calc

    # WHEN
    sue_budunit.tree_arithmetic_traverse_calc()

    # THEN
    assert day_idea._denom == 1022679
    assert day_idea._gogo_calc == 0
    assert day_idea._stop_calc == 1440


def test_BudUnit_tree_arithmetic_traverse_calc_Sets_days_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    days_road = sue_budunit.make_road(jaja_road, days_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(jaja_road)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    assert jaja_idea._begin == 0
    assert jaja_idea._close == 1472657760
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea._denom == 1440
    assert not days_idea._gogo_calc
    assert not days_idea._stop_calc

    # WHEN
    sue_budunit.tree_arithmetic_traverse_calc()

    # THEN
    assert days_idea._denom == 1440
    assert days_idea._gogo_calc == 0
    assert days_idea._stop_calc == 1022679
