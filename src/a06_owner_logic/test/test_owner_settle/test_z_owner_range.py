from src.a05_plan_logic.plan import planunit_shop
from src.a06_owner_logic.owner import ownerunit_shop


def test_OwnerUnit_get_plan_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_ownerunit = ownerunit_shop("Yao")
    time_rope = yao_ownerunit.make_l1_rope("time")
    tech_rope = yao_ownerunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_ownerunit.make_rope(tech_rope, wk_str)
    wk_plan = planunit_shop(wk_str, begin=0, close=10800)
    yao_ownerunit.set_plan(wk_plan, tech_rope)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_ownerunit.set_plan(mon_plan, wk_rope)
    yao_ownerunit.set_plan(tue_plan, wk_rope)
    yao_ownerunit.set_plan(wed_plan, wk_rope)
    yao_ownerunit.set_plan(thu_plan, wk_rope)
    yao_ownerunit.set_plan(fri_plan, wk_rope)
    yao_ownerunit.set_plan(sat_plan, wk_rope)
    yao_ownerunit.set_plan(sun_plan, wk_rope)
    yao_ownerunit.settle_owner()

    # WHEN
    ranged_plans = yao_ownerunit.get_plan_ranged_kids(plan_rope=wk_rope)

    # # THEN
    assert len(ranged_plans) == 7


def test_OwnerUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_ownerunit = ownerunit_shop("Yao")
    time_rope = yao_ownerunit.make_l1_rope("time")
    tech_rope = yao_ownerunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_ownerunit.make_rope(tech_rope, wk_str)
    wk_plan = planunit_shop(wk_str, begin=0, close=10800)
    yao_ownerunit.set_plan(wk_plan, tech_rope)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_ownerunit.set_plan(mon_plan, wk_rope)
    yao_ownerunit.set_plan(tue_plan, wk_rope)
    yao_ownerunit.set_plan(wed_plan, wk_rope)
    yao_ownerunit.set_plan(thu_plan, wk_rope)
    yao_ownerunit.set_plan(fri_plan, wk_rope)
    yao_ownerunit.set_plan(sat_plan, wk_rope)
    yao_ownerunit.set_plan(sun_plan, wk_rope)
    yao_ownerunit.settle_owner()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_plans = yao_ownerunit.get_plan_ranged_kids(wk_rope, x_begin, x_close)

    # THEN
    # for plan_x in wk_plan._kids.values():
    #     print(f"{plan_x.plan_label=} {plan_x._gogo_calc=} {plan_x._stop_calc=} ")
    # print("")
    # for plan_x in ranged_plans.values():
    #     print(f"{plan_x.plan_label=} {plan_x._gogo_calc=} {plan_x._stop_calc=} ")
    assert len(ranged_plans) == 3


def test_OwnerUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_ownerunit = ownerunit_shop("Yao")
    time_rope = yao_ownerunit.make_l1_rope("time")
    tech_rope = yao_ownerunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_ownerunit.make_rope(tech_rope, wk_str)
    wk_plan = planunit_shop(wk_str, begin=0, close=10800)
    yao_ownerunit.set_plan(wk_plan, tech_rope)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_ownerunit.set_plan(mon_plan, wk_rope)
    yao_ownerunit.set_plan(tue_plan, wk_rope)
    yao_ownerunit.set_plan(wed_plan, wk_rope)
    yao_ownerunit.set_plan(thu_plan, wk_rope)
    yao_ownerunit.set_plan(fri_plan, wk_rope)
    yao_ownerunit.set_plan(sat_plan, wk_rope)
    yao_ownerunit.set_plan(sun_plan, wk_rope)
    yao_ownerunit.settle_owner()

    # WHEN / THEN
    assert len(yao_ownerunit.get_plan_ranged_kids(wk_rope, 0, 1440)) == 1
    assert len(yao_ownerunit.get_plan_ranged_kids(wk_rope, 0, 2000)) == 2
    assert len(yao_ownerunit.get_plan_ranged_kids(wk_rope, 0, 3000)) == 3


def test_OwnerUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_ownerunit = ownerunit_shop("Yao")
    time_rope = yao_ownerunit.make_l1_rope("time")
    tech_rope = yao_ownerunit.make_rope(time_rope, "tech")
    wk_str = "wk"
    wk_rope = yao_ownerunit.make_rope(tech_rope, wk_str)
    wk_plan = planunit_shop(wk_str, begin=0, close=10800)
    yao_ownerunit.set_plan(wk_plan, tech_rope)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_ownerunit.set_plan(mon_plan, wk_rope)
    yao_ownerunit.set_plan(tue_plan, wk_rope)
    yao_ownerunit.set_plan(wed_plan, wk_rope)
    yao_ownerunit.set_plan(thu_plan, wk_rope)
    yao_ownerunit.set_plan(fri_plan, wk_rope)
    yao_ownerunit.set_plan(sat_plan, wk_rope)
    yao_ownerunit.set_plan(sun_plan, wk_rope)
    yao_ownerunit.settle_owner()

    # WHEN / THEN
    assert len(yao_ownerunit.get_plan_ranged_kids(wk_rope, 0)) == 1
    assert len(yao_ownerunit.get_plan_ranged_kids(wk_rope, 1440)) == 1

    # ESTABLISH
    wkday_str = "wkday"
    wkdays_plan = planunit_shop(wkday_str, gogo_want=0, stop_want=1440 * 5)
    yao_ownerunit.set_plan(wkdays_plan, wk_rope)

    # WHEN
    yao_ownerunit.settle_owner()

    # THEN
    assert len(yao_ownerunit.get_plan_ranged_kids(wk_rope, 1440)) == 2
