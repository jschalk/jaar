from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import PlanAttrHolder, planattrholder_shop


def test_PlanAttrHolder_Exists():
    # ESTABLISH / WHEN
    new_obj = PlanAttrHolder()

    # THEN
    assert new_obj.star is None
    assert new_obj.uid is None
    assert new_obj.reason is None
    assert new_obj.reason_context is None
    assert new_obj.reason_case is None
    assert new_obj.reason_lower is None
    assert new_obj.reason_upper is None
    assert new_obj.reason_divisor is None
    assert new_obj.reason_del_case_reason_context is None
    assert new_obj.reason_del_case_reason_state is None
    assert new_obj.reason_plan_active_requisite is None
    assert new_obj.laborunit is None
    assert new_obj.healerlink is None
    assert new_obj.begin is None
    assert new_obj.close is None
    assert new_obj.addin is None
    assert new_obj.numor is None
    assert new_obj.denom is None
    assert new_obj.morph is None
    assert new_obj.task is None
    assert new_obj.factunit is None
    assert new_obj.descendant_task_count is None
    assert new_obj.all_partner_cred is None
    assert new_obj.all_partner_debt is None
    assert new_obj.awardlink is None
    assert new_obj.awardlink_del is None
    assert new_obj.is_expanded is None


def test_PlanAttrHolder_CalculatesCaseRanges():
    # ESTABLISH
    plan_attr = PlanAttrHolder(reason_case="some_rope")
    assert plan_attr.reason_lower is None
    assert plan_attr.reason_upper is None
    # assert plan_attr.reason_case_numor is None
    assert plan_attr.reason_divisor is None
    # assert plan_attr.reason_case_morph is None

    # WHEN
    plan_attr.set_case_range_influenced_by_case_plan(
        reason_lower=5.0,
        reason_upper=20.0,
        # case_numor,
        case_denom=4.0,
        # case_morph,
    )

    # THEN
    assert plan_attr.reason_lower == 5.0
    assert plan_attr.reason_upper == 20.0
    # assert plan_attr.reason_case_numor is None
    assert plan_attr.reason_divisor == 4.0
    # assert plan_attr.reason_case_morph is None


def test_planattrholder_shop_ReturnsObj():
    # ESTABLISH
    sue_healerlink = healerlink_shop({"Sue", "Yim"})

    # WHEN
    x_planattrholder = planattrholder_shop(healerlink=sue_healerlink)

    # THEN
    assert x_planattrholder.healerlink == sue_healerlink
