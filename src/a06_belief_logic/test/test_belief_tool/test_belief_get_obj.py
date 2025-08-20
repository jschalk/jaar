from src.a03_group_logic.group import awardunit_shop
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.belief_tool import (
    belief_get_obj,
    belief_partner_membership_get_obj,
    belief_partnerunit_get_obj,
    belief_plan_awardunit_get_obj,
    belief_plan_factunit_get_obj,
    belief_plan_reason_caseunit_get_obj as caseunit_get_obj,
    belief_plan_reasonunit_get_obj,
    belief_planunit_get_obj,
)
from src.a06_belief_logic.test._util.a06_str import (
    belief_partner_membership_str,
    belief_partnerunit_str,
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str as caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    beliefunit_str,
    fact_context_str,
    fact_state_str,
    plan_rope_str,
    reason_context_str,
    reason_state_str,
)


def test_belief_partnerunit_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {"partner_name": yao_str}
    sue_belief.add_partnerunit(yao_str)

    # WHEN
    x_obj = belief_partnerunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_partner(yao_str)


def test_belief_partner_membership_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {"partner_name": yao_str, "group_title": swim_str}
    sue_belief.add_partnerunit(yao_str)
    sue_belief.get_partner(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = belief_partner_membership_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_partner(yao_str).get_membership(swim_str)


def test_belief_planunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope}

    # WHEN
    x_obj = belief_planunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope)


def test_belief_plan_awardunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, "awardee_title": swim_str}
    sue_belief.add_plan(casa_rope)
    sue_belief.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(swim_str))

    # WHEN
    x_obj = belief_plan_awardunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope).get_awardunit(swim_str)


def test_belief_plan_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, reason_context_str(): wk_rope}
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(wk_rope)
    sue_belief.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = belief_plan_reasonunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope).get_reasonunit(wk_rope)


def test_belief_plan_reason_caseunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
    casa_jkeys = {
        plan_rope_str(): casa_rope,
        reason_context_str(): wk_rope,
        reason_state_str(): thur_rope,
    }
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(wk_rope)
    sue_belief.add_plan(thur_rope)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = caseunit_get_obj(sue_belief, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_plan.get_reasonunit(wk_rope).get_case(thur_rope)


def test_belief_plan_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, fact_context_str(): wk_rope}
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(wk_rope)
    sue_belief.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = belief_plan_factunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope).factunits.get(wk_rope)


def test_belief_get_obj_ReturnsObj_BeliefUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {"partner_name": yao_str}
    sue_belief.add_partnerunit(yao_str)

    # WHEN
    x_obj = belief_get_obj(beliefunit_str(), sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief


def test_belief_get_obj_ReturnsObj_belief_partnerunit_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {"partner_name": yao_str}
    sue_belief.add_partnerunit(yao_str)

    # WHEN
    x_obj = belief_get_obj(belief_partnerunit_str(), sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_partner(yao_str)


def test_belief_get_obj_ReturnsObj_belief_partner_membership_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {"partner_name": yao_str, "group_title": swim_str}
    sue_belief.add_partnerunit(yao_str)
    sue_belief.get_partner(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = belief_get_obj(belief_partner_membership_str(), sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_partner(yao_str).get_membership(swim_str)


def test_belief_get_obj_ReturnsObj_belief_planunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope}

    # WHEN
    x_obj = belief_get_obj(belief_planunit_str(), sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope)


def test_belief_get_obj_ReturnsObj_belief_plan_awardunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, "awardee_title": swim_str}
    sue_belief.add_plan(casa_rope)
    sue_belief.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(swim_str))

    # WHEN
    x_obj = belief_get_obj(belief_plan_awardunit_str(), sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope).get_awardunit(swim_str)


def test_belief_get_obj_ReturnsObj_belief_plan_reasonunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, reason_context_str(): wk_rope}
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(wk_rope)
    sue_belief.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = belief_get_obj(belief_plan_reasonunit_str(), sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope).get_reasonunit(wk_rope)


def test_belief_get_obj_ReturnsObj_belief_plan_reason_caseunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
    casa_jkeys = {
        plan_rope_str(): casa_rope,
        reason_context_str(): wk_rope,
        reason_state_str(): thur_rope,
    }
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(wk_rope)
    sue_belief.add_plan(thur_rope)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = belief_get_obj(caseunit_str(), sue_belief, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_plan.get_reasonunit(wk_rope).get_case(thur_rope)


def test_belief_get_obj_ReturnsObj_belief_plan_factunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, fact_context_str(): wk_rope}
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(wk_rope)
    sue_belief.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = belief_get_obj(belief_plan_factunit_str(), sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_plan_obj(casa_rope).factunits.get(wk_rope)
