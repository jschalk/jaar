from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_get_idea_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_idea = ideaunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_idea(week_idea, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_idea = ideaunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_way)
    yao_budunit.set_idea(tue_idea, week_way)
    yao_budunit.set_idea(wed_idea, week_way)
    yao_budunit.set_idea(thu_idea, week_way)
    yao_budunit.set_idea(fri_idea, week_way)
    yao_budunit.set_idea(sat_idea, week_way)
    yao_budunit.set_idea(sun_idea, week_way)
    yao_budunit.settle_bud()

    # WHEN
    ranged_ideas = yao_budunit.get_idea_ranged_kids(idea_way=week_way)

    # # THEN
    assert len(ranged_ideas) == 7


def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_idea = ideaunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_idea(week_idea, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_idea = ideaunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_way)
    yao_budunit.set_idea(tue_idea, week_way)
    yao_budunit.set_idea(wed_idea, week_way)
    yao_budunit.set_idea(thu_idea, week_way)
    yao_budunit.set_idea(fri_idea, week_way)
    yao_budunit.set_idea(sat_idea, week_way)
    yao_budunit.set_idea(sun_idea, week_way)
    yao_budunit.settle_bud()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_ideas = yao_budunit.get_idea_ranged_kids(week_way, x_begin, x_close)

    # THEN
    # for idea_x in week_idea._kids.values():
    #     print(f"{idea_x.idea_word=} {idea_x._gogo_calc=} {idea_x._stop_calc=} ")
    # print("")
    # for idea_x in ranged_ideas.values():
    #     print(f"{idea_x.idea_word=} {idea_x._gogo_calc=} {idea_x._stop_calc=} ")
    assert len(ranged_ideas) == 3


def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_idea = ideaunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_idea(week_idea, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_idea = ideaunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_way)
    yao_budunit.set_idea(tue_idea, week_way)
    yao_budunit.set_idea(wed_idea, week_way)
    yao_budunit.set_idea(thu_idea, week_way)
    yao_budunit.set_idea(fri_idea, week_way)
    yao_budunit.set_idea(sat_idea, week_way)
    yao_budunit.set_idea(sun_idea, week_way)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_idea_ranged_kids(week_way, 0, 1440)) == 1
    assert len(yao_budunit.get_idea_ranged_kids(week_way, 0, 2000)) == 2
    assert len(yao_budunit.get_idea_ranged_kids(week_way, 0, 3000)) == 3


def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_idea = ideaunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_idea(week_idea, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_idea = ideaunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_idea = ideaunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_idea = ideaunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_idea = ideaunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_idea = ideaunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_idea = ideaunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_idea = ideaunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_idea(mon_idea, week_way)
    yao_budunit.set_idea(tue_idea, week_way)
    yao_budunit.set_idea(wed_idea, week_way)
    yao_budunit.set_idea(thu_idea, week_way)
    yao_budunit.set_idea(fri_idea, week_way)
    yao_budunit.set_idea(sat_idea, week_way)
    yao_budunit.set_idea(sun_idea, week_way)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_idea_ranged_kids(week_way, 0)) == 1
    assert len(yao_budunit.get_idea_ranged_kids(week_way, 1440)) == 1

    # ESTABLISH
    weekday_str = "weekday"
    weekdays_idea = ideaunit_shop(weekday_str, gogo_want=0, stop_want=1440 * 5)
    yao_budunit.set_idea(weekdays_idea, week_way)

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    assert len(yao_budunit.get_idea_ranged_kids(week_way, 1440)) == 2
