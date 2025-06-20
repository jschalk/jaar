from src.a01_term_logic.rope import to_rope
from src.a04_reason_logic.reason_concept import reasonunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.example_plans import (
    get_mop_with_reason_planunit_example1,
    get_planunit_with_4_levels,
)


def test_PlanUnit_get_relevant_ropes_EmptyRopeTermReturnsEmpty():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()

    # WHEN
    relevant_ropes = sue_plan._get_relevant_ropes({})

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 0
    assert relevant_ropes == set()


def test_PlanUnit_get_relevant_ropes_RootRopeTermReturnsOnlyItself():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    root_rope = to_rope(sue_plan.vow_label)

    # WHEN
    root_dict = {root_rope: -1}
    relevant_ropes = sue_plan._get_relevant_ropes(root_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 1
    assert relevant_ropes == {root_rope}


def test_PlanUnit_get_relevant_ropes_SimpleReturnsOnlyAncestors():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    root_rope = to_rope(sue_plan.vow_label)

    # WHEN
    wk_str = "wkdays"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    sun_str = "Sunday"
    sun_rope = sue_plan.make_rope(wk_rope, sun_str)
    sun_dict = {sun_rope}
    relevant_ropes = sue_plan._get_relevant_ropes(sun_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert relevant_ropes == {root_rope, sun_rope, wk_rope}


def test_PlanUnit_get_relevant_ropes_ReturnsSimpleReasonUnitRcontext():
    # ESTABLISH
    sue_plan = planunit_shop(owner_name="Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_plan.make_rope(casa_rope, floor_str)
    floor_concept = conceptunit_shop(floor_str)
    sue_plan.set_concept(floor_concept, parent_rope=casa_rope)

    unim_str = "unimportant"
    unim_rope = sue_plan.make_l1_rope(unim_str)
    unim_concept = conceptunit_shop(unim_str)
    sue_plan.set_concept(unim_concept, parent_rope=sue_plan.vow_label)

    status_str = "cleaniness status"
    status_rope = sue_plan.make_rope(casa_rope, status_str)
    status_concept = conceptunit_shop(status_str)
    sue_plan.set_concept(status_concept, parent_rope=casa_rope)
    floor_reason = reasonunit_shop(rcontext=status_rope)
    floor_reason.set_premise(premise=status_rope)
    sue_plan.edit_concept_attr(floor_rope, reason=floor_reason)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = sue_plan._get_relevant_ropes(floor_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 4
    root_rope = to_rope(sue_plan.vow_label)
    assert relevant_ropes == {root_rope, casa_rope, status_rope, floor_rope}
    assert unim_rope not in relevant_ropes


def test_PlanUnit_get_relevant_ropes_ReturnsReasonUnitRcontextAndDescendents():
    # ESTABLISH
    x_plan = get_mop_with_reason_planunit_example1()
    root_rope = to_rope(x_plan.vow_label)
    casa_str = "casa"
    casa_rope = x_plan.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = x_plan.make_rope(casa_rope, floor_str)

    unim_str = "unimportant"
    unim_rope = x_plan.make_l1_rope(unim_str)

    status_str = "cleaniness status"
    status_rope = x_plan.make_rope(casa_rope, status_str)

    clean_str = "clean"
    clean_rope = x_plan.make_rope(status_rope, clean_str)

    very_much_str = "very_much"
    very_much_rope = x_plan.make_rope(clean_rope, very_much_str)

    moderately_str = "moderately"
    moderately_rope = x_plan.make_rope(clean_rope, moderately_str)

    dirty_str = "dirty"
    dirty_rope = x_plan.make_rope(status_rope, dirty_str)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = x_plan._get_relevant_ropes(floor_dict)

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


def test_PlanUnit_get_relevant_ropes_ReturnSimple():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(owner_name=yao_str)
    root_rope = to_rope(yao_plan.vow_label)
    min_range_x_str = "a_minute_range"
    min_range_x_rope = yao_plan.make_l1_rope(min_range_x_str)
    min_range_concept = conceptunit_shop(min_range_x_str, begin=0, close=2880)
    yao_plan.set_l1_concept(min_range_concept)

    day_length_str = "day_1ce"
    day_length_rope = yao_plan.make_l1_rope(day_length_str)
    day_length_concept = conceptunit_shop(day_length_str, begin=0, close=1440)
    yao_plan.set_l1_concept(day_length_concept)

    hr_length_str = "hr_length"
    hr_length_rope = yao_plan.make_l1_rope(hr_length_str)
    hr_length_concept = conceptunit_shop(hr_length_str)
    yao_plan.set_l1_concept(hr_length_concept)

    min_days_str = "days in minute_range"
    min_days_rope = yao_plan.make_rope(min_range_x_rope, min_days_str)
    min_days_concept = conceptunit_shop(min_days_str)
    yao_plan.set_concept(min_days_concept, parent_rope=min_range_x_rope)

    # WHEN
    print(f"{yao_plan._concept_dict.keys()}")
    ropes_dict = {min_days_rope}
    relevant_ropes = yao_plan._get_relevant_ropes(ropes_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert min_range_x_rope in relevant_ropes
    assert day_length_rope not in relevant_ropes
    assert hr_length_rope not in relevant_ropes
    assert min_days_rope in relevant_ropes
    assert root_rope in relevant_ropes
    # min_days_concept = yao_plan.get_concept_obj(min_days_rope)


def test_PlanUnit_get_inheritor_concept_list_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    tech_rope = yao_planunit.make_l1_rope("tech")
    wk_str = "wk"
    wk_rope = yao_planunit.make_rope(tech_rope, wk_str)
    yao_planunit.set_concept(conceptunit_shop(wk_str, begin=0, close=10800), tech_rope)
    mon_str = "Monday"
    mon_rope = yao_planunit.make_rope(wk_rope, mon_str)
    yao_planunit.set_concept(conceptunit_shop(mon_str), wk_rope)
    yao_planunit.settle_plan()

    # WHEN
    x_inheritor_concept_list = yao_planunit.get_inheritor_concept_list(
        wk_rope, mon_rope
    )

    # # THEN
    assert len(x_inheritor_concept_list) == 2
    wk_concept = yao_planunit.get_concept_obj(wk_rope)
    mon_concept = yao_planunit.get_concept_obj(mon_rope)
    assert x_inheritor_concept_list == [wk_concept, mon_concept]
