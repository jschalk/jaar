from src.a01_term_logic.way import to_way
from src.a04_reason_logic.reason_concept import reasonunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic._test_util.example_buds import (
    get_budunit_with_4_levels,
    get_mop_with_reason_budunit_example1,
)
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_get_relevant_ways_EmptyWayTermReturnsEmpty():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    relevant_ways = sue_bud._get_relevant_ways({})

    # THEN
    print(f"{relevant_ways=}")
    assert len(relevant_ways) == 0
    assert relevant_ways == set()


def test_BudUnit_get_relevant_ways_RootWayTermReturnsOnlyItself():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_way = to_way(sue_bud.vow_label)

    # WHEN
    root_dict = {root_way: -1}
    relevant_ways = sue_bud._get_relevant_ways(root_dict)

    # THEN
    print(f"{relevant_ways=}")
    assert len(relevant_ways) == 1
    assert relevant_ways == {root_way}


def test_BudUnit_get_relevant_ways_SimpleReturnsOnlyAncestors():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_way = to_way(sue_bud.vow_label)

    # WHEN
    wk_str = "wkdays"
    wk_way = sue_bud.make_l1_way(wk_str)
    sun_str = "Sunday"
    sun_way = sue_bud.make_way(wk_way, sun_str)
    sun_dict = {sun_way}
    relevant_ways = sue_bud._get_relevant_ways(sun_dict)

    # THEN
    print(f"{relevant_ways=}")
    assert len(relevant_ways) == 3
    assert relevant_ways == {root_way, sun_way, wk_way}


def test_BudUnit_get_relevant_ways_ReturnsSimpleReasonUnitRcontext():
    # ESTABLISH
    sue_bud = budunit_shop(owner_name="Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    floor_str = "mop floor"
    floor_way = sue_bud.make_way(casa_way, floor_str)
    floor_concept = conceptunit_shop(floor_str)
    sue_bud.set_concept(floor_concept, parent_way=casa_way)

    unim_str = "unimportant"
    unim_way = sue_bud.make_l1_way(unim_str)
    unim_concept = conceptunit_shop(unim_str)
    sue_bud.set_concept(unim_concept, parent_way=sue_bud.vow_label)

    status_str = "cleaniness status"
    status_way = sue_bud.make_way(casa_way, status_str)
    status_concept = conceptunit_shop(status_str)
    sue_bud.set_concept(status_concept, parent_way=casa_way)
    floor_reason = reasonunit_shop(rcontext=status_way)
    floor_reason.set_premise(premise=status_way)
    sue_bud.edit_concept_attr(floor_way, reason=floor_reason)

    # WHEN
    floor_dict = {floor_way}
    relevant_ways = sue_bud._get_relevant_ways(floor_dict)

    # THEN
    print(f"{relevant_ways=}")
    assert len(relevant_ways) == 4
    root_way = to_way(sue_bud.vow_label)
    assert relevant_ways == {root_way, casa_way, status_way, floor_way}
    assert unim_way not in relevant_ways


def test_BudUnit_get_relevant_ways_ReturnsReasonUnitRcontextAndDescendents():
    # ESTABLISH
    x_bud = get_mop_with_reason_budunit_example1()
    root_way = to_way(x_bud.vow_label)
    casa_str = "casa"
    casa_way = x_bud.make_l1_way(casa_str)
    floor_str = "mop floor"
    floor_way = x_bud.make_way(casa_way, floor_str)

    unim_str = "unimportant"
    unim_way = x_bud.make_l1_way(unim_str)

    status_str = "cleaniness status"
    status_way = x_bud.make_way(casa_way, status_str)

    clean_str = "clean"
    clean_way = x_bud.make_way(status_way, clean_str)

    very_much_str = "very_much"
    very_much_way = x_bud.make_way(clean_way, very_much_str)

    moderately_str = "moderately"
    moderately_way = x_bud.make_way(clean_way, moderately_str)

    dirty_str = "dirty"
    dirty_way = x_bud.make_way(status_way, dirty_str)

    # WHEN
    floor_dict = {floor_way}
    relevant_ways = x_bud._get_relevant_ways(floor_dict)

    # THEN
    print(f"{relevant_ways=}")
    assert len(relevant_ways) == 8
    assert clean_way in relevant_ways
    assert dirty_way in relevant_ways
    assert moderately_way in relevant_ways
    assert very_much_way in relevant_ways
    assert relevant_ways == {
        root_way,
        casa_way,
        status_way,
        floor_way,
        clean_way,
        dirty_way,
        very_much_way,
        moderately_way,
    }
    assert unim_way not in relevant_ways


def test_BudUnit_get_relevant_ways_ReturnSimple():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)
    root_way = to_way(yao_bud.vow_label)
    min_range_x_str = "a_minute_range"
    min_range_x_way = yao_bud.make_l1_way(min_range_x_str)
    min_range_concept = conceptunit_shop(min_range_x_str, begin=0, close=2880)
    yao_bud.set_l1_concept(min_range_concept)

    day_length_str = "day_1ce"
    day_length_way = yao_bud.make_l1_way(day_length_str)
    day_length_concept = conceptunit_shop(day_length_str, begin=0, close=1440)
    yao_bud.set_l1_concept(day_length_concept)

    hr_length_str = "hr_length"
    hr_length_way = yao_bud.make_l1_way(hr_length_str)
    hr_length_concept = conceptunit_shop(hr_length_str)
    yao_bud.set_l1_concept(hr_length_concept)

    min_days_str = "days in minute_range"
    min_days_way = yao_bud.make_way(min_range_x_way, min_days_str)
    min_days_concept = conceptunit_shop(min_days_str)
    yao_bud.set_concept(min_days_concept, parent_way=min_range_x_way)

    # WHEN
    print(f"{yao_bud._concept_dict.keys()}")
    ways_dict = {min_days_way}
    relevant_ways = yao_bud._get_relevant_ways(ways_dict)

    # THEN
    print(f"{relevant_ways=}")
    assert len(relevant_ways) == 3
    assert min_range_x_way in relevant_ways
    assert day_length_way not in relevant_ways
    assert hr_length_way not in relevant_ways
    assert min_days_way in relevant_ways
    assert root_way in relevant_ways
    # min_days_concept = yao_bud.get_concept_obj(min_days_way)


def test_BudUnit_get_inheritor_concept_list_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao")
    tech_way = yao_budunit.make_l1_way("tech")
    wk_str = "wk"
    wk_way = yao_budunit.make_way(tech_way, wk_str)
    yao_budunit.set_concept(conceptunit_shop(wk_str, begin=0, close=10800), tech_way)
    mon_str = "Monday"
    mon_way = yao_budunit.make_way(wk_way, mon_str)
    yao_budunit.set_concept(conceptunit_shop(mon_str), wk_way)
    yao_budunit.settle_bud()

    # WHEN
    x_inheritor_concept_list = yao_budunit.get_inheritor_concept_list(wk_way, mon_way)

    # # THEN
    assert len(x_inheritor_concept_list) == 2
    wk_concept = yao_budunit.get_concept_obj(wk_way)
    mon_concept = yao_budunit.get_concept_obj(mon_way)
    assert x_inheritor_concept_list == [wk_concept, mon_concept]
