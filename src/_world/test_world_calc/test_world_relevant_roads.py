from src._world.world import worldunit_shop
from src._world.idea import ideaunit_shop
from src._world.reason_idea import reasonunit_shop
from src._world.examples.example_worlds import (
    get_world_with_4_levels as example_worlds_get_world_with_4_levels,
    get_world_mop_example1 as example_world_get_world_mop_example1,
)


def test_WorldUnit_get_relevant_roads_EmptyRoadUnitReturnsEmpty():
    # ESTABLISH
    x_world = example_worlds_get_world_with_4_levels()
    x_world.calc_world_metrics()

    # WHEN
    relevant_roads = x_world._get_relevant_roads({})

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 0
    assert relevant_roads == {}


def test_WorldUnit_get_relevant_roads_RootRoadUnitReturnsOnlyItself():
    # ESTABLISH
    x_world = example_worlds_get_world_with_4_levels()
    x_world.calc_world_metrics()

    # WHEN
    root_dict = {x_world._real_id: -1}
    relevant_roads = x_world._get_relevant_roads(root_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 1
    assert relevant_roads == {x_world._real_id: -1}


def test_WorldUnit_get_relevant_roads_SimpleReturnsOnlyAncestors():
    # ESTABLISH
    x_world = example_worlds_get_world_with_4_levels()
    x_world.calc_world_metrics()

    # WHEN
    week_text = "weekdays"
    week_road = x_world.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_world.make_road(week_road, sun_text)
    sun_dict = {sun_road}
    relevant_roads = x_world._get_relevant_roads(sun_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads == {x_world._real_id: -1, sun_road: -1, week_road: -1}


def test_WorldUnit_get_relevant_roads_ReturnsSimpleReasonUnitBase():
    # ESTABLISH
    neo_world = worldunit_shop(_owner_id="Neo")
    casa_text = "casa"
    casa_road = neo_world.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = neo_world.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text)
    neo_world.add_idea(floor_idea, parent_road=casa_road)

    unim_text = "unimportant"
    unim_road = neo_world.make_l1_road(unim_text)
    unim_idea = ideaunit_shop(unim_text)
    neo_world.add_idea(unim_idea, parent_road=neo_world._real_id)

    status_text = "cleaniness status"
    status_road = neo_world.make_road(casa_road, status_text)
    status_idea = ideaunit_shop(status_text)
    neo_world.add_idea(status_idea, parent_road=casa_road)
    floor_reason = reasonunit_shop(base=status_road)
    floor_reason.set_premise(premise=status_road)
    neo_world.edit_idea_attr(road=floor_road, reason=floor_reason)

    # WHEN
    neo_world.calc_world_metrics()
    floor_dict = {floor_road}
    relevant_roads = neo_world._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads == {
        neo_world._real_id: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


def test_WorldUnit_get_relevant_roads_ReturnsReasonUnitBaseAndDescendents():
    # ESTABLISH
    x_world = example_world_get_world_mop_example1()
    casa_text = "casa"
    casa_road = x_world.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = x_world.make_road(casa_road, floor_text)

    unim_text = "unimportant"
    unim_road = x_world.make_l1_road(unim_text)

    status_text = "cleaniness status"
    status_road = x_world.make_road(casa_road, status_text)

    clean_text = "clean"
    clean_road = x_world.make_road(status_road, clean_text)

    very_much_text = "very_much"
    very_much_road = x_world.make_road(clean_road, very_much_text)

    moderately_text = "moderately"
    moderately_road = x_world.make_road(clean_road, moderately_text)

    dirty_text = "dirty"
    dirty_road = x_world.make_road(status_road, dirty_text)

    # WHEN
    x_world.calc_world_metrics()
    floor_dict = {floor_road}
    relevant_roads = x_world._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 8
    assert relevant_roads.get(clean_road) != None
    assert relevant_roads.get(dirty_road) != None
    assert relevant_roads.get(moderately_road) != None
    assert relevant_roads.get(very_much_road) != None
    assert relevant_roads == {
        x_world._real_id: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
        clean_road: -1,
        dirty_road: -1,
        very_much_road: -1,
        moderately_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


def test_WorldUnit_get_relevant_roads_numeric_road_ReturnSimple():
    # ESTABLISH
    yao_text = "Yao"
    yao_world = worldunit_shop(_owner_id=yao_text)
    casa_text = "casa"
    casa_road = yao_world.make_l1_road(casa_text)
    yao_world.add_l1_idea(ideaunit_shop(casa_text))
    casa_idea = yao_world.get_idea_obj(casa_road)
    day_text = "day_range"
    day_road = yao_world.make_l1_road(day_text)
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    yao_world.add_l1_idea(day_idea)
    yao_world.edit_idea_attr(road=casa_road, denom=11, numeric_road=day_road)
    assert casa_idea._begin == 4
    print(f"{casa_idea._label=} {casa_idea._begin=} {casa_idea._close=}")

    # WHEN
    yao_world.calc_world_metrics()
    roads_dict = {casa_road}
    relevant_roads = yao_world._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads.get(casa_road) != None
    assert relevant_roads.get(day_road) != None
    assert relevant_roads == {
        yao_world._real_id: -1,
        casa_road: -1,
        day_road: -1,
    }


def test_WorldUnit_get_relevant_roads_range_source_road_ReturnSimple():
    # ESTABLISH
    yao_text = "Yao"
    yao_world = worldunit_shop(_owner_id=yao_text)
    min_range_text = "a_minute_range"
    min_range_road = yao_world.make_l1_road(min_range_text)
    min_range_idea = ideaunit_shop(min_range_text, _begin=0, _close=2880)
    yao_world.add_l1_idea(min_range_idea)

    day_len_text = "day_length"
    day_len_road = yao_world.make_l1_road(day_len_text)
    day_len_idea = ideaunit_shop(day_len_text, _begin=0, _close=1440)
    yao_world.add_l1_idea(day_len_idea)

    min_days_text = "days in minute_range"
    min_days_road = yao_world.make_road(min_range_road, min_days_text)
    min_days_idea = ideaunit_shop(min_days_text, _range_source_road=day_len_road)
    yao_world.add_idea(min_days_idea, parent_road=min_range_road)

    # WHEN
    yao_world.calc_world_metrics()
    print(f"{yao_world._idea_dict.keys()}")
    roads_dict = {min_days_road}
    relevant_roads = yao_world._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads.get(min_range_road) != None
    assert relevant_roads.get(day_len_road) != None
    assert relevant_roads.get(min_days_road) != None
    assert relevant_roads.get(yao_world._real_id) != None
    # min_days_idea = yao_world.get_idea_obj(min_days_road)
