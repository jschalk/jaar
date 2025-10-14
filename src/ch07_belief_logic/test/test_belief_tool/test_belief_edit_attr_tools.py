from pytest import raises as pytest_raises
from src.ch02_rope.rope import create_rope, default_knot_if_None, to_rope
from src.ch04_voice.group import awardunit_shop
from src.ch04_voice.labor import laborunit_shop
from src.ch05_reason.reason import caseunit_shop, factunit_shop, reasonunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    set_caseunit_to_belief,
)
from src.ch07_belief_logic.test._util.ch07_examples import (
    ChExampleStrsSlashknot as exx,
    get_beliefunit_with_4_levels,
)
from src.ref.keywords import Ch07Keywords as wx


def test_set_caseunit_to_belief_SetAttr_Scenario0_Pass_reason_case():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob, knot=exx.slash_str)
    casa_rope = bob_belief.make_l1_rope(exx.casa_str)
    wk_rope = bob_belief.make_l1_rope(exx.wk_str)
    wed_rope = bob_belief.make_rope(wk_rope, exx.wed_str)
    bob_belief.set_l1_plan(planunit_shop(exx.casa_str))
    bob_belief.set_l1_plan(planunit_shop(exx.wk_str))
    bob_belief.set_plan(planunit_shop(exx.wed_str), wk_rope)
    casa_plan = bob_belief.get_plan_obj(casa_rope)
    assert not casa_plan.reasonunits.get(wk_rope)

    # WHEN
    set_caseunit_to_belief(
        bob_belief, casa_rope, reason_context=wk_rope, reason_case=wed_rope
    )

    # THEN
    assert casa_plan.reasonunits.get(wk_rope)


def test_set_caseunit_to_belief_SetAttr_Scenario1_Pass_reason_lower_reason_upper():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob, knot=exx.slash_str)
    mop_rope = bob_belief.make_l1_rope(exx.mop_str)
    clean_rope = bob_belief.make_l1_rope(exx.clean_str)
    dirtyness_rope = bob_belief.make_rope(clean_rope, exx.dirtyness_str)
    bob_belief.add_plan(dirtyness_rope)
    bob_belief.add_plan(mop_rope)
    dirtyness_jkeys = {
        wx.plan_rope: mop_rope,
        wx.reason_context: dirtyness_rope,
        wx.reason_state: dirtyness_rope,
    }
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    assert not belief_plan_reason_caseunit_exists(bob_belief, dirtyness_jkeys)

    # WHEN
    set_caseunit_to_belief(
        belief=bob_belief,
        plan_rope=mop_rope,
        reason_context=dirtyness_rope,
        reason_case=dirtyness_rope,
        reason_lower=dirtyness_reason_lower,
        reason_upper=dirtyness_reason_upper,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, dirtyness_jkeys)
    dirtyness_case = belief_plan_reason_caseunit_get_obj(bob_belief, dirtyness_jkeys)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper


def test_set_caseunit_to_belief_SetAttr_Scenario2_Pass_reason_divisor():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob, knot=exx.slash_str)
    mop_rope = bob_belief.make_l1_rope(exx.mop_str)
    clean_rope = bob_belief.make_l1_rope(exx.clean_str)
    dirtyness_rope = bob_belief.make_rope(clean_rope, exx.dirtyness_str)
    bob_belief.add_plan(dirtyness_rope)
    bob_belief.add_plan(mop_rope)
    dirtyness_jkeys = {
        wx.plan_rope: mop_rope,
        wx.reason_context: dirtyness_rope,
        wx.reason_state: dirtyness_rope,
    }
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    dirtyness_reason_divisor = 11
    assert not belief_plan_reason_caseunit_exists(bob_belief, dirtyness_jkeys)

    # WHEN
    set_caseunit_to_belief(
        belief=bob_belief,
        plan_rope=mop_rope,
        reason_context=dirtyness_rope,
        reason_case=dirtyness_rope,
        reason_lower=dirtyness_reason_lower,
        reason_upper=dirtyness_reason_upper,
        reason_divisor=dirtyness_reason_divisor,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, dirtyness_jkeys)
    dirtyness_case = belief_plan_reason_caseunit_get_obj(bob_belief, dirtyness_jkeys)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper
    assert dirtyness_case.reason_divisor == dirtyness_reason_divisor
