from src.a05_item_logic.item import itemunit_shop
from src.f02_bud.bud import budunit_shop


def test_BudUnit_get_item_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_str = "week"
    week_road = yao_budunit.make_road(tech_road, week_str)
    week_item = itemunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_item(week_item, tech_road)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_item = itemunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_item = itemunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_item = itemunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_item = itemunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_item = itemunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_item = itemunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_item = itemunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_item(mon_item, week_road)
    yao_budunit.set_item(tue_item, week_road)
    yao_budunit.set_item(wed_item, week_road)
    yao_budunit.set_item(thu_item, week_road)
    yao_budunit.set_item(fri_item, week_road)
    yao_budunit.set_item(sat_item, week_road)
    yao_budunit.set_item(sun_item, week_road)
    yao_budunit.settle_bud()

    # WHEN
    ranged_items = yao_budunit.get_item_ranged_kids(item_road=week_road)

    # # THEN
    assert len(ranged_items) == 7


def test_BudUnit_get_item_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_str = "week"
    week_road = yao_budunit.make_road(tech_road, week_str)
    week_item = itemunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_item(week_item, tech_road)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_item = itemunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_item = itemunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_item = itemunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_item = itemunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_item = itemunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_item = itemunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_item = itemunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_item(mon_item, week_road)
    yao_budunit.set_item(tue_item, week_road)
    yao_budunit.set_item(wed_item, week_road)
    yao_budunit.set_item(thu_item, week_road)
    yao_budunit.set_item(fri_item, week_road)
    yao_budunit.set_item(sat_item, week_road)
    yao_budunit.set_item(sun_item, week_road)
    yao_budunit.settle_bud()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_items = yao_budunit.get_item_ranged_kids(week_road, x_begin, x_close)

    # THEN
    # for item_x in week_item._kids.values():
    #     print(f"{item_x.item_title=} {item_x._gogo_calc=} {item_x._stop_calc=} ")
    # print("")
    # for item_x in ranged_items.values():
    #     print(f"{item_x.item_title=} {item_x._gogo_calc=} {item_x._stop_calc=} ")
    assert len(ranged_items) == 3


def test_BudUnit_get_item_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_str = "week"
    week_road = yao_budunit.make_road(tech_road, week_str)
    week_item = itemunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_item(week_item, tech_road)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_item = itemunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_item = itemunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_item = itemunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_item = itemunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_item = itemunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_item = itemunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_item = itemunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_item(mon_item, week_road)
    yao_budunit.set_item(tue_item, week_road)
    yao_budunit.set_item(wed_item, week_road)
    yao_budunit.set_item(thu_item, week_road)
    yao_budunit.set_item(fri_item, week_road)
    yao_budunit.set_item(sat_item, week_road)
    yao_budunit.set_item(sun_item, week_road)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_item_ranged_kids(week_road, 0, 1440)) == 1
    assert len(yao_budunit.get_item_ranged_kids(week_road, 0, 2000)) == 2
    assert len(yao_budunit.get_item_ranged_kids(week_road, 0, 3000)) == 3


def test_BudUnit_get_item_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    time_road = yao_budunit.make_l1_road("time")
    tech_road = yao_budunit.make_road(time_road, "tech")
    week_str = "week"
    week_road = yao_budunit.make_road(tech_road, week_str)
    week_item = itemunit_shop(week_str, begin=0, close=10800)
    yao_budunit.set_item(week_item, tech_road)
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sun_str = "Sunday"
    mon_item = itemunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_item = itemunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_item = itemunit_shop(wed_str, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_item = itemunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_item = itemunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_item = itemunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_item = itemunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_budunit.set_item(mon_item, week_road)
    yao_budunit.set_item(tue_item, week_road)
    yao_budunit.set_item(wed_item, week_road)
    yao_budunit.set_item(thu_item, week_road)
    yao_budunit.set_item(fri_item, week_road)
    yao_budunit.set_item(sat_item, week_road)
    yao_budunit.set_item(sun_item, week_road)
    yao_budunit.settle_bud()

    # WHEN / THEN
    assert len(yao_budunit.get_item_ranged_kids(week_road, 0)) == 1
    assert len(yao_budunit.get_item_ranged_kids(week_road, 1440)) == 1

    # ESTABLISH
    weekday_str = "weekday"
    weekdays_item = itemunit_shop(weekday_str, gogo_want=0, stop_want=1440 * 5)
    yao_budunit.set_item(weekdays_item, week_road)

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    assert len(yao_budunit.get_item_ranged_kids(week_road, 1440)) == 2
