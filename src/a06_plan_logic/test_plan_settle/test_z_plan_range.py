from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_get_concept_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    time_rope = yao_planunit.make_l1_rope("time")
    tech_rope = yao_planunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_planunit.make_rope(tech_rope, wk_str)
    wk_concept = conceptunit_shop(wk_str, begin=0, close=10800)
    yao_planunit.set_concept(wk_concept, tech_rope)
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
    yao_planunit.set_concept(mon_concept, wk_rope)
    yao_planunit.set_concept(tue_concept, wk_rope)
    yao_planunit.set_concept(wed_concept, wk_rope)
    yao_planunit.set_concept(thu_concept, wk_rope)
    yao_planunit.set_concept(fri_concept, wk_rope)
    yao_planunit.set_concept(sat_concept, wk_rope)
    yao_planunit.set_concept(sun_concept, wk_rope)
    yao_planunit.settle_plan()

    # WHEN
    ranged_concepts = yao_planunit.get_concept_ranged_kids(concept_rope=wk_rope)

    # # THEN
    assert len(ranged_concepts) == 7


def test_PlanUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    time_rope = yao_planunit.make_l1_rope("time")
    tech_rope = yao_planunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_planunit.make_rope(tech_rope, wk_str)
    wk_concept = conceptunit_shop(wk_str, begin=0, close=10800)
    yao_planunit.set_concept(wk_concept, tech_rope)
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
    yao_planunit.set_concept(mon_concept, wk_rope)
    yao_planunit.set_concept(tue_concept, wk_rope)
    yao_planunit.set_concept(wed_concept, wk_rope)
    yao_planunit.set_concept(thu_concept, wk_rope)
    yao_planunit.set_concept(fri_concept, wk_rope)
    yao_planunit.set_concept(sat_concept, wk_rope)
    yao_planunit.set_concept(sun_concept, wk_rope)
    yao_planunit.settle_plan()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_concepts = yao_planunit.get_concept_ranged_kids(wk_rope, x_begin, x_close)

    # THEN
    # for concept_x in wk_concept._kids.values():
    #     print(f"{concept_x.concept_label=} {concept_x._gogo_calc=} {concept_x._stop_calc=} ")
    # print("")
    # for concept_x in ranged_concepts.values():
    #     print(f"{concept_x.concept_label=} {concept_x._gogo_calc=} {concept_x._stop_calc=} ")
    assert len(ranged_concepts) == 3


def test_PlanUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    time_rope = yao_planunit.make_l1_rope("time")
    tech_rope = yao_planunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_planunit.make_rope(tech_rope, wk_str)
    wk_concept = conceptunit_shop(wk_str, begin=0, close=10800)
    yao_planunit.set_concept(wk_concept, tech_rope)
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
    yao_planunit.set_concept(mon_concept, wk_rope)
    yao_planunit.set_concept(tue_concept, wk_rope)
    yao_planunit.set_concept(wed_concept, wk_rope)
    yao_planunit.set_concept(thu_concept, wk_rope)
    yao_planunit.set_concept(fri_concept, wk_rope)
    yao_planunit.set_concept(sat_concept, wk_rope)
    yao_planunit.set_concept(sun_concept, wk_rope)
    yao_planunit.settle_plan()

    # WHEN / THEN
    assert len(yao_planunit.get_concept_ranged_kids(wk_rope, 0, 1440)) == 1
    assert len(yao_planunit.get_concept_ranged_kids(wk_rope, 0, 2000)) == 2
    assert len(yao_planunit.get_concept_ranged_kids(wk_rope, 0, 3000)) == 3


def test_PlanUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    time_rope = yao_planunit.make_l1_rope("time")
    tech_rope = yao_planunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_planunit.make_rope(tech_rope, wk_str)
    wk_concept = conceptunit_shop(wk_str, begin=0, close=10800)
    yao_planunit.set_concept(wk_concept, tech_rope)
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
    yao_planunit.set_concept(mon_concept, wk_rope)
    yao_planunit.set_concept(tue_concept, wk_rope)
    yao_planunit.set_concept(wed_concept, wk_rope)
    yao_planunit.set_concept(thu_concept, wk_rope)
    yao_planunit.set_concept(fri_concept, wk_rope)
    yao_planunit.set_concept(sat_concept, wk_rope)
    yao_planunit.set_concept(sun_concept, wk_rope)
    yao_planunit.settle_plan()

    # WHEN / THEN
    assert len(yao_planunit.get_concept_ranged_kids(wk_rope, 0)) == 1
    assert len(yao_planunit.get_concept_ranged_kids(wk_rope, 1440)) == 1

    # ESTABLISH
    wkday_str = "wkday"
    wkdays_concept = conceptunit_shop(wkday_str, gogo_want=0, stop_want=1440 * 5)
    yao_planunit.set_concept(wkdays_concept, wk_rope)

    # WHEN
    yao_planunit.settle_plan()

    # THEN
    assert len(yao_planunit.get_concept_ranged_kids(wk_rope, 1440)) == 2
