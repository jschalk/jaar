from src.bud.bud import budunit_shop
from src.bud.idea import ideaunit_shop
from src.bud.reason_idea import reasonunit_shop
from src.bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_mop_example1,
)


def test_BudUnit_get_relevant_roads_EmptyRoadUnitReturnsEmpty():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    relevant_roads = sue_bud._get_relevant_roads({})

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 0
    assert relevant_roads == set()


def test_BudUnit_get_relevant_roads_RootRoadUnitReturnsOnlyItself():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    root_dict = {sue_bud._real_id: -1}
    relevant_roads = sue_bud._get_relevant_roads(root_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 1
    assert relevant_roads == {sue_bud._real_id}


def test_BudUnit_get_relevant_roads_SimpleReturnsOnlyAncestors():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    sun_str = "Sunday"
    sun_road = sue_bud.make_road(week_road, sun_str)
    sun_dict = {sun_road}
    relevant_roads = sue_bud._get_relevant_roads(sun_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads == {sue_bud._real_id, sun_road, week_road}


def test_BudUnit_get_relevant_roads_ReturnsSimpleReasonUnitBase():
    # ESTABLISH
    sue_bud = budunit_shop(_owner_id="Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    floor_str = "mop floor"
    floor_road = sue_bud.make_road(casa_road, floor_str)
    floor_idea = ideaunit_shop(floor_str)
    sue_bud.set_idea(floor_idea, parent_road=casa_road)

    unim_str = "unimportant"
    unim_road = sue_bud.make_l1_road(unim_str)
    unim_idea = ideaunit_shop(unim_str)
    sue_bud.set_idea(unim_idea, parent_road=sue_bud._real_id)

    status_str = "cleaniness status"
    status_road = sue_bud.make_road(casa_road, status_str)
    status_idea = ideaunit_shop(status_str)
    sue_bud.set_idea(status_idea, parent_road=casa_road)
    floor_reason = reasonunit_shop(base=status_road)
    floor_reason.set_premise(premise=status_road)
    sue_bud.edit_idea_attr(road=floor_road, reason=floor_reason)

    # WHEN
    floor_dict = {floor_road}
    relevant_roads = sue_bud._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads == {sue_bud._real_id, casa_road, status_road, floor_road}
    assert unim_road not in relevant_roads


def test_BudUnit_get_relevant_roads_ReturnsReasonUnitBaseAndDescendents():
    # ESTABLISH
    x_bud = get_budunit_mop_example1()
    casa_str = "casa"
    casa_road = x_bud.make_l1_road(casa_str)
    floor_str = "mop floor"
    floor_road = x_bud.make_road(casa_road, floor_str)

    unim_str = "unimportant"
    unim_road = x_bud.make_l1_road(unim_str)

    status_str = "cleaniness status"
    status_road = x_bud.make_road(casa_road, status_str)

    clean_str = "clean"
    clean_road = x_bud.make_road(status_road, clean_str)

    very_much_str = "very_much"
    very_much_road = x_bud.make_road(clean_road, very_much_str)

    moderately_str = "moderately"
    moderately_road = x_bud.make_road(clean_road, moderately_str)

    dirty_str = "dirty"
    dirty_road = x_bud.make_road(status_road, dirty_str)

    # WHEN
    floor_dict = {floor_road}
    relevant_roads = x_bud._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 8
    assert clean_road in relevant_roads
    assert dirty_road in relevant_roads
    assert moderately_road in relevant_roads
    assert very_much_road in relevant_roads
    assert relevant_roads == {
        x_bud._real_id,
        casa_road,
        status_road,
        floor_road,
        clean_road,
        dirty_road,
        very_much_road,
        moderately_road,
    }
    assert unim_road not in relevant_roads


def test_BudUnit_get_relevant_roads_ReturnSimple():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(_owner_id=yao_str)
    min_range_x_str = "a_minute_range"
    min_range_x_road = yao_bud.make_l1_road(min_range_x_str)
    min_range_idea = ideaunit_shop(min_range_x_str, begin=0, close=2880)
    yao_bud.set_l1_idea(min_range_idea)

    day_distance_str = "day_1ce"
    day_distance_road = yao_bud.make_l1_road(day_distance_str)
    day_distance_idea = ideaunit_shop(day_distance_str, begin=0, close=1440)
    yao_bud.set_l1_idea(day_distance_idea)

    hour_distance_str = "hour_distance"
    hour_distance_road = yao_bud.make_l1_road(hour_distance_str)
    hour_distance_idea = ideaunit_shop(hour_distance_str)
    yao_bud.set_l1_idea(hour_distance_idea)

    min_days_str = "days in minute_range"
    min_days_road = yao_bud.make_road(min_range_x_road, min_days_str)
    min_days_idea = ideaunit_shop(min_days_str)
    yao_bud.set_idea(min_days_idea, parent_road=min_range_x_road)

    # WHEN
    print(f"{yao_bud._idea_dict.keys()}")
    roads_dict = {min_days_road}
    relevant_roads = yao_bud._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert min_range_x_road in relevant_roads
    assert day_distance_road not in relevant_roads
    assert hour_distance_road not in relevant_roads
    assert min_days_road in relevant_roads
    assert yao_bud._real_id in relevant_roads
    # min_days_idea = yao_bud.get_idea_obj(min_days_road)


def test_BudUnit_get_inheritor_idea_list_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    tech_road = yao_budunit.make_l1_road("tech")
    week_str = "week"
    week_road = yao_budunit.make_road(tech_road, week_str)
    yao_budunit.set_idea(ideaunit_shop(week_str, begin=0, close=10800), tech_road)
    mon_str = "Monday"
    mon_road = yao_budunit.make_road(week_road, mon_str)
    yao_budunit.set_idea(ideaunit_shop(mon_str), week_road)
    yao_budunit.settle_bud()

    # WHEN
    x_inheritor_idea_list = yao_budunit.get_inheritor_idea_list(week_road, mon_road)

    # # THEN
    assert len(x_inheritor_idea_list) == 2
    week_idea = yao_budunit.get_idea_obj(week_road)
    mon_idea = yao_budunit.get_idea_obj(mon_road)
    assert x_inheritor_idea_list == [week_idea, mon_idea]
