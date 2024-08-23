from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop


def test_BudUnit_get_idea_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_text = "week"
    week_road = yao_budunit.make_road(tech_road, week_text)
    week_idea = ideaunit_shop(week_text, _begin=0, _close=10800)
    yao_budunit.set_idea(week_idea, tech_road)
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"
    sun_text = "Sunday"
    mon_idea = ideaunit_shop(mon_text, _gogo_want=1440 * 0, _stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_text, _gogo_want=1440 * 1, _stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_text, _gogo_want=1440 * 2, _stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_text, _gogo_want=1440 * 3, _stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_text, _gogo_want=1440 * 4, _stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_text, _gogo_want=1440 * 5, _stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_text, _gogo_want=1440 * 6, _stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_road)
    yao_budunit.set_idea(tue_idea, week_road)
    yao_budunit.set_idea(wed_idea, week_road)
    yao_budunit.set_idea(thu_idea, week_road)
    yao_budunit.set_idea(fri_idea, week_road)
    yao_budunit.set_idea(sat_idea, week_road)
    yao_budunit.set_idea(sun_idea, week_road)
    yao_budunit.settle_bud()

    # WHEN
    ranged_ideas = yao_budunit.get_idea_ranged_kids(idea_road=week_road)

    # # THEN
    assert len(ranged_ideas) == 7


def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_text = "week"
    week_road = yao_budunit.make_road(tech_road, week_text)
    week_idea = ideaunit_shop(week_text, _begin=0, _close=10800)
    yao_budunit.set_idea(week_idea, tech_road)
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"
    sun_text = "Sunday"
    mon_idea = ideaunit_shop(mon_text, _gogo_want=1440 * 0, _stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_text, _gogo_want=1440 * 1, _stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_text, _gogo_want=1440 * 2, _stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_text, _gogo_want=1440 * 3, _stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_text, _gogo_want=1440 * 4, _stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_text, _gogo_want=1440 * 5, _stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_text, _gogo_want=1440 * 6, _stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_road)
    yao_budunit.set_idea(tue_idea, week_road)
    yao_budunit.set_idea(wed_idea, week_road)
    yao_budunit.set_idea(thu_idea, week_road)
    yao_budunit.set_idea(fri_idea, week_road)
    yao_budunit.set_idea(sat_idea, week_road)
    yao_budunit.set_idea(sun_idea, week_road)
    yao_budunit.settle_bud()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_ideas = yao_budunit.get_idea_ranged_kids(week_road, x_begin, x_close)

    # THEN
    # for idea_x in week_idea._kids.values():
    #     print(f"{idea_x._label=} {idea_x._gogo_calc=} {idea_x._stop_calc=} ")
    # print("")
    # for idea_x in ranged_ideas.values():
    #     print(f"{idea_x._label=} {idea_x._gogo_calc=} {idea_x._stop_calc=} ")
    assert len(ranged_ideas) == 3


def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_text = "week"
    week_road = yao_budunit.make_road(tech_road, week_text)
    week_idea = ideaunit_shop(week_text, _begin=0, _close=10800)
    yao_budunit.set_idea(week_idea, tech_road)
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"
    sun_text = "Sunday"
    mon_idea = ideaunit_shop(mon_text, _gogo_want=1440 * 0, _stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_text, _gogo_want=1440 * 1, _stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_text, _gogo_want=1440 * 2, _stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_text, _gogo_want=1440 * 3, _stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_text, _gogo_want=1440 * 4, _stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_text, _gogo_want=1440 * 5, _stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_text, _gogo_want=1440 * 6, _stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_road)
    yao_budunit.set_idea(tue_idea, week_road)
    yao_budunit.set_idea(wed_idea, week_road)
    yao_budunit.set_idea(thu_idea, week_road)
    yao_budunit.set_idea(fri_idea, week_road)
    yao_budunit.set_idea(sat_idea, week_road)
    yao_budunit.set_idea(sun_idea, week_road)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_idea_ranged_kids(week_road, 0, 1440)) == 1
    assert len(yao_budunit.get_idea_ranged_kids(week_road, 0, 2000)) == 2
    assert len(yao_budunit.get_idea_ranged_kids(week_road, 0, 3000)) == 3


def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_text = "week"
    week_road = yao_budunit.make_road(tech_road, week_text)
    week_idea = ideaunit_shop(week_text, _begin=0, _close=10800)
    yao_budunit.set_idea(week_idea, tech_road)
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"
    sun_text = "Sunday"
    mon_idea = ideaunit_shop(mon_text, _gogo_want=1440 * 0, _stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_text, _gogo_want=1440 * 1, _stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_text, _gogo_want=1440 * 2, _stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_text, _gogo_want=1440 * 3, _stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_text, _gogo_want=1440 * 4, _stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_text, _gogo_want=1440 * 5, _stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_text, _gogo_want=1440 * 6, _stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_road)
    yao_budunit.set_idea(tue_idea, week_road)
    yao_budunit.set_idea(wed_idea, week_road)
    yao_budunit.set_idea(thu_idea, week_road)
    yao_budunit.set_idea(fri_idea, week_road)
    yao_budunit.set_idea(sat_idea, week_road)
    yao_budunit.set_idea(sun_idea, week_road)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_idea_ranged_kids(week_road, 0)) == 1
    assert len(yao_budunit.get_idea_ranged_kids(week_road, 1440)) == 1

    # ESTABLISH
    weekday_text = "weekday"
    weekdays_idea = ideaunit_shop(weekday_text, _gogo_want=0, _stop_want=1440 * 5)
    yao_budunit.set_idea(weekdays_idea, week_road)

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    assert len(yao_budunit.get_idea_ranged_kids(week_road, 1440)) == 2
