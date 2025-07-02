from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import PlanAttrHolder, planattrholder_shop


def test_PlanAttrHolder_Exists():
    new_obj = PlanAttrHolder()
    assert new_obj.mass is None
    assert new_obj.uid is None
    assert new_obj.reason is None
    assert new_obj.reason_rcontext is None
    assert new_obj.reason_premise is None
    assert new_obj.popen is None
    assert new_obj.reason_pnigh is None
    assert new_obj.pdivisor is None
    assert new_obj.reason_del_premise_rcontext is None
    assert new_obj.reason_del_premise_pstate is None
    assert new_obj.reason_rplan_active_requisite is None
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
    assert new_obj.all_acct_cred is None
    assert new_obj.all_acct_debt is None
    assert new_obj.awardlink is None
    assert new_obj.awardlink_del is None
    assert new_obj.is_expanded is None


def test_PlanAttrHolder_CorrectlyCalculatesPremiseRanges():
    # ESTABLISH
    plan_attr = PlanAttrHolder(reason_premise="some_rope")
    assert plan_attr.popen is None
    assert plan_attr.reason_pnigh is None
    # assert plan_attr.reason_premise_numor is None
    assert plan_attr.pdivisor is None
    # assert plan_attr.reason_premise_morph is None

    # WHEN
    plan_attr.set_premise_range_influenced_by_premise_plan(
        popen=5.0,
        pnigh=20.0,
        # premise_numor,
        premise_denom=4.0,
        # premise_morph,
    )
    assert plan_attr.popen == 5.0
    assert plan_attr.reason_pnigh == 20.0
    # assert plan_attr.reason_premise_numor is None
    assert plan_attr.pdivisor == 4.0
    # assert plan_attr.reason_premise_morph is None


def test_planattrholder_shop_ReturnsObj():
    # ESTABLISH
    sue_healerlink = healerlink_shop({"Sue", "Yim"})

    # WHEN
    x_planattrholder = planattrholder_shop(healerlink=sue_healerlink)

    # THEN
    assert x_planattrholder.healerlink == sue_healerlink
