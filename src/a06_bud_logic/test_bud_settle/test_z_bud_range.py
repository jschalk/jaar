from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_get_concept_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_concept = conceptunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_concept(week_concept, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_concept = conceptunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_concept = conceptunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_concept = conceptunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_concept = conceptunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_concept = conceptunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_concept = conceptunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_concept = conceptunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_concept(mon_concept, week_way)
    yao_budunit.set_concept(tue_concept, week_way)
    yao_budunit.set_concept(wed_concept, week_way)
    yao_budunit.set_concept(thu_concept, week_way)
    yao_budunit.set_concept(fri_concept, week_way)
    yao_budunit.set_concept(sat_concept, week_way)
    yao_budunit.set_concept(sun_concept, week_way)
    yao_budunit.settle_bud()

    # WHEN
    ranged_concepts = yao_budunit.get_concept_ranged_kids(concept_way=week_way)

    # # THEN
    assert len(ranged_concepts) == 7


def test_BudUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_concept = conceptunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_concept(week_concept, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_concept = conceptunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_concept = conceptunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_concept = conceptunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_concept = conceptunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_concept = conceptunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_concept = conceptunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_concept = conceptunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_concept(mon_concept, week_way)
    yao_budunit.set_concept(tue_concept, week_way)
    yao_budunit.set_concept(wed_concept, week_way)
    yao_budunit.set_concept(thu_concept, week_way)
    yao_budunit.set_concept(fri_concept, week_way)
    yao_budunit.set_concept(sat_concept, week_way)
    yao_budunit.set_concept(sun_concept, week_way)
    yao_budunit.settle_bud()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_concepts = yao_budunit.get_concept_ranged_kids(week_way, x_begin, x_close)

    # THEN
    # for concept_x in week_concept._kids.values():
    #     print(f"{concept_x.concept_label=} {concept_x._gogo_calc=} {concept_x._stop_calc=} ")
    # print("")
    # for concept_x in ranged_concepts.values():
    #     print(f"{concept_x.concept_label=} {concept_x._gogo_calc=} {concept_x._stop_calc=} ")
    assert len(ranged_concepts) == 3


def test_BudUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_concept = conceptunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_concept(week_concept, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_concept = conceptunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_concept = conceptunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_concept = conceptunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_concept = conceptunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_concept = conceptunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_concept = conceptunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_concept = conceptunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_concept(mon_concept, week_way)
    yao_budunit.set_concept(tue_concept, week_way)
    yao_budunit.set_concept(wed_concept, week_way)
    yao_budunit.set_concept(thu_concept, week_way)
    yao_budunit.set_concept(fri_concept, week_way)
    yao_budunit.set_concept(sat_concept, week_way)
    yao_budunit.set_concept(sun_concept, week_way)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_concept_ranged_kids(week_way, 0, 1440)) == 1
    assert len(yao_budunit.get_concept_ranged_kids(week_way, 0, 2000)) == 2
    assert len(yao_budunit.get_concept_ranged_kids(week_way, 0, 3000)) == 3


def test_BudUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_way = yao_budunit.make_l1_way("time")
    tech_way = yao_budunit.make_way(time_way, "tech")
    week_str = "week"
    week_way = yao_budunit.make_way(tech_way, week_str)
    week_concept = conceptunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_concept(week_concept, tech_way)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_concept = conceptunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_concept = conceptunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_concept = conceptunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_concept = conceptunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_concept = conceptunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_concept = conceptunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_concept = conceptunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_concept(mon_concept, week_way)
    yao_budunit.set_concept(tue_concept, week_way)
    yao_budunit.set_concept(wed_concept, week_way)
    yao_budunit.set_concept(thu_concept, week_way)
    yao_budunit.set_concept(fri_concept, week_way)
    yao_budunit.set_concept(sat_concept, week_way)
    yao_budunit.set_concept(sun_concept, week_way)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_concept_ranged_kids(week_way, 0)) == 1
    assert len(yao_budunit.get_concept_ranged_kids(week_way, 1440)) == 1

    # ESTABLISH
    weekday_str = "weekday"
    weekdays_concept = conceptunit_shop(weekday_str, gogo_want=0, stop_want=1440 * 5)
    yao_budunit.set_concept(weekdays_concept, week_way)

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    assert len(yao_budunit.get_concept_ranged_kids(week_way, 1440)) == 2
