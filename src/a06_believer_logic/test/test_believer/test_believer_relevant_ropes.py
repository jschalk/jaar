from src.a01_term_logic.rope import to_rope
from src.a04_reason_logic.reason_plan import reasonunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
    get_mop_with_reason_believerunit_example1,
)


def test_BelieverUnit_get_relevant_ropes_EmptyRopeTermReturnsEmpty():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()

    # WHEN
    relevant_ropes = sue_believer._get_relevant_ropes({})

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 0
    assert relevant_ropes == set()


def test_BelieverUnit_get_relevant_ropes_RootRopeTermReturnsOnlyItself():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    root_rope = to_rope(sue_believer.belief_label)

    # WHEN
    root_dict = {root_rope: -1}
    relevant_ropes = sue_believer._get_relevant_ropes(root_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 1
    assert relevant_ropes == {root_rope}


def test_BelieverUnit_get_relevant_ropes_SimpleReturnsOnlyAncestors():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    root_rope = to_rope(sue_believer.belief_label)

    # WHEN
    wk_str = "sem_jours"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_believer.make_rope(wk_rope, sun_str)
    sun_dict = {sun_rope}
    relevant_ropes = sue_believer._get_relevant_ropes(sun_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert relevant_ropes == {root_rope, sun_rope, wk_rope}


def test_BelieverUnit_get_relevant_ropes_ReturnsSimpleReasonUnitreason_context():
    # ESTABLISH
    sue_believer = believerunit_shop(believer_name="Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_believer.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str)
    sue_believer.set_plan(floor_plan, parent_rope=casa_rope)

    unim_str = "unimportant"
    unim_rope = sue_believer.make_l1_rope(unim_str)
    unim_plan = planunit_shop(unim_str)
    sue_believer.set_plan(unim_plan, parent_rope=sue_believer.belief_label)

    status_str = "cleaniness status"
    status_rope = sue_believer.make_rope(casa_rope, status_str)
    status_plan = planunit_shop(status_str)
    sue_believer.set_plan(status_plan, parent_rope=casa_rope)
    floor_reason = reasonunit_shop(reason_context=status_rope)
    floor_reason.set_case(case=status_rope)
    sue_believer.edit_plan_attr(floor_rope, reason=floor_reason)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = sue_believer._get_relevant_ropes(floor_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 4
    root_rope = to_rope(sue_believer.belief_label)
    assert relevant_ropes == {root_rope, casa_rope, status_rope, floor_rope}
    assert unim_rope not in relevant_ropes


def test_BelieverUnit_get_relevant_ropes_ReturnsReasonUnitreason_contextAndDescendents():
    # ESTABLISH
    x_believer = get_mop_with_reason_believerunit_example1()
    root_rope = to_rope(x_believer.belief_label)
    casa_str = "casa"
    casa_rope = x_believer.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = x_believer.make_rope(casa_rope, floor_str)

    unim_str = "unimportant"
    unim_rope = x_believer.make_l1_rope(unim_str)

    status_str = "cleaniness status"
    status_rope = x_believer.make_rope(casa_rope, status_str)

    clean_str = "clean"
    clean_rope = x_believer.make_rope(status_rope, clean_str)

    very_much_str = "very_much"
    very_much_rope = x_believer.make_rope(clean_rope, very_much_str)

    moderately_str = "moderately"
    moderately_rope = x_believer.make_rope(clean_rope, moderately_str)

    dirty_str = "dirty"
    dirty_rope = x_believer.make_rope(status_rope, dirty_str)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = x_believer._get_relevant_ropes(floor_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 8
    assert clean_rope in relevant_ropes
    assert dirty_rope in relevant_ropes
    assert moderately_rope in relevant_ropes
    assert very_much_rope in relevant_ropes
    assert relevant_ropes == {
        root_rope,
        casa_rope,
        status_rope,
        floor_rope,
        clean_rope,
        dirty_rope,
        very_much_rope,
        moderately_rope,
    }
    assert unim_rope not in relevant_ropes


def test_BelieverUnit_get_relevant_ropes_ReturnSimple():
    # ESTABLISH
    yao_str = "Yao"
    yao_believer = believerunit_shop(believer_name=yao_str)
    root_rope = to_rope(yao_believer.belief_label)
    min_range_x_str = "a_minute_range"
    min_range_x_rope = yao_believer.make_l1_rope(min_range_x_str)
    min_range_plan = planunit_shop(min_range_x_str, begin=0, close=2880)
    yao_believer.set_l1_plan(min_range_plan)

    jour_length_str = "jour_1ce"
    jour_length_rope = yao_believer.make_l1_rope(jour_length_str)
    jour_length_plan = planunit_shop(jour_length_str, begin=0, close=1440)
    yao_believer.set_l1_plan(jour_length_plan)

    hr_length_str = "hr_length"
    hr_length_rope = yao_believer.make_l1_rope(hr_length_str)
    hr_length_plan = planunit_shop(hr_length_str)
    yao_believer.set_l1_plan(hr_length_plan)

    min_jours_str = "jours in minute_range"
    min_jours_rope = yao_believer.make_rope(min_range_x_rope, min_jours_str)
    min_jours_plan = planunit_shop(min_jours_str)
    yao_believer.set_plan(min_jours_plan, parent_rope=min_range_x_rope)

    # WHEN
    print(f"{yao_believer._plan_dict.keys()}")
    ropes_dict = {min_jours_rope}
    relevant_ropes = yao_believer._get_relevant_ropes(ropes_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert min_range_x_rope in relevant_ropes
    assert jour_length_rope not in relevant_ropes
    assert hr_length_rope not in relevant_ropes
    assert min_jours_rope in relevant_ropes
    assert root_rope in relevant_ropes
    # min_jours_plan = yao_believer.get_plan_obj(min_jours_rope)


def test_BelieverUnit_get_inheritor_plan_list_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_believerunit = believerunit_shop("Yao")
    tech_rope = yao_believerunit.make_l1_rope("tech")
    wk_str = "wk"
    wk_rope = yao_believerunit.make_rope(tech_rope, wk_str)
    yao_believerunit.set_plan(planunit_shop(wk_str, begin=0, close=10800), tech_rope)
    mon_str = "Mon"
    mon_rope = yao_believerunit.make_rope(wk_rope, mon_str)
    yao_believerunit.set_plan(planunit_shop(mon_str), wk_rope)
    yao_believerunit.settle_believer()

    # WHEN
    x_inheritor_plan_list = yao_believerunit.get_inheritor_plan_list(wk_rope, mon_rope)

    # # THEN
    assert len(x_inheritor_plan_list) == 2
    wk_plan = yao_believerunit.get_plan_obj(wk_rope)
    mon_plan = yao_believerunit.get_plan_obj(mon_rope)
    assert x_inheritor_plan_list == [wk_plan, mon_plan]
