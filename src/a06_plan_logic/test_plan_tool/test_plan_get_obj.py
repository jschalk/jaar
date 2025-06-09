from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_plan_logic._test_util.a06_str import (
    concept_way_str,
    fcontext_str,
    fstate_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str as premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    planunit_str,
    pstate_str,
    rcontext_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.plan_tool import (
    plan_acct_membership_get_obj,
    plan_acctunit_get_obj,
    plan_concept_awardlink_get_obj,
    plan_concept_factunit_get_obj,
    plan_concept_reason_premiseunit_get_obj as premiseunit_get_obj,
    plan_concept_reasonunit_get_obj,
    plan_conceptunit_get_obj,
    plan_get_obj,
)


def test_plan_acctunit_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_plan = planunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_plan.add_acctunit(yao_str)

    # WHEN
    x_obj = plan_acctunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_acct(yao_str)


def test_plan_acct_membership_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    jkeys = {"acct_name": yao_str, "group_title": swim_str}
    sue_plan.add_acctunit(yao_str)
    sue_plan.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = plan_acct_membership_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_acct(yao_str).get_membership(swim_str)


def test_plan_conceptunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way}

    # WHEN
    x_obj = plan_conceptunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way)


def test_plan_concept_awardlink_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way, "awardee_title": swim_str}
    sue_plan.add_concept(casa_way)
    sue_plan.get_concept_obj(casa_way).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = plan_concept_awardlink_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way).get_awardlink(swim_str)


def test_plan_concept_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    wk_way = sue_plan.make_l1_way("wk")
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way, rcontext_str(): wk_way}
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(wk_way)
    sue_plan.get_concept_obj(casa_way).set_reasonunit(reasonunit_shop(wk_way))

    # WHEN
    x_obj = plan_concept_reasonunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way).get_reasonunit(wk_way)


def test_plan_concept_reason_premiseunit_get_obj_ReturnsObj():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    thur_way = sue_plan.make_way(wk_way, "thur")
    casa_jkeys = {
        concept_way_str(): casa_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(wk_way)
    sue_plan.add_concept(thur_way)
    casa_concept = sue_plan.get_concept_obj(casa_way)
    casa_concept.set_reasonunit(reasonunit_shop(wk_way))
    casa_concept.get_reasonunit(wk_way).set_premise(thur_way)

    # WHEN
    x_obj = premiseunit_get_obj(sue_plan, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_concept.get_reasonunit(wk_way).get_premise(thur_way)


def test_plan_concept_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    wk_way = sue_plan.make_l1_way("wk")
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way, fcontext_str(): wk_way}
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(wk_way)
    sue_plan.get_concept_obj(casa_way).set_factunit(factunit_shop(wk_way))

    # WHEN
    x_obj = plan_concept_factunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way).factunits.get(wk_way)


def test_plan_get_obj_ReturnsObj_PlanUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_plan = planunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_plan.add_acctunit(yao_str)

    # WHEN
    x_obj = plan_get_obj(planunit_str(), sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan


def test_plan_get_obj_ReturnsObj_plan_acctunit_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    sue_plan = planunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_plan.add_acctunit(yao_str)

    # WHEN
    x_obj = plan_get_obj(plan_acctunit_str(), sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_acct(yao_str)


def test_plan_get_obj_ReturnsObj_plan_acct_membership_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    jkeys = {"acct_name": yao_str, "group_title": swim_str}
    sue_plan.add_acctunit(yao_str)
    sue_plan.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = plan_get_obj(plan_acct_membership_str(), sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_acct(yao_str).get_membership(swim_str)


def test_plan_get_obj_ReturnsObj_plan_conceptunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way}

    # WHEN
    x_obj = plan_get_obj(plan_conceptunit_str(), sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way)


def test_plan_get_obj_ReturnsObj_plan_concept_awardlink_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way, "awardee_title": swim_str}
    sue_plan.add_concept(casa_way)
    sue_plan.get_concept_obj(casa_way).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = plan_get_obj(plan_concept_awardlink_str(), sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way).get_awardlink(swim_str)


def test_plan_get_obj_ReturnsObj_plan_concept_reasonunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    wk_way = sue_plan.make_l1_way("wk")
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way, rcontext_str(): wk_way}
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(wk_way)
    sue_plan.get_concept_obj(casa_way).set_reasonunit(reasonunit_shop(wk_way))

    # WHEN
    x_obj = plan_get_obj(plan_concept_reasonunit_str(), sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way).get_reasonunit(wk_way)


def test_plan_get_obj_ReturnsObj_plan_concept_reason_premiseunit_get_obj():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    thur_way = sue_plan.make_way(wk_way, "thur")
    casa_jkeys = {
        concept_way_str(): casa_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(wk_way)
    sue_plan.add_concept(thur_way)
    casa_concept = sue_plan.get_concept_obj(casa_way)
    casa_concept.set_reasonunit(reasonunit_shop(wk_way))
    casa_concept.get_reasonunit(wk_way).set_premise(thur_way)

    # WHEN
    x_obj = plan_get_obj(premiseunit_str(), sue_plan, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_concept.get_reasonunit(wk_way).get_premise(thur_way)


def test_plan_get_obj_ReturnsObj_plan_concept_factunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    wk_way = sue_plan.make_l1_way("wk")
    sue_plan.add_concept(casa_way)
    jkeys = {concept_way_str(): casa_way, fcontext_str(): wk_way}
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(wk_way)
    sue_plan.get_concept_obj(casa_way).set_factunit(factunit_shop(wk_way))

    # WHEN
    x_obj = plan_get_obj(plan_concept_factunit_str(), sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_concept_obj(casa_way).factunits.get(wk_way)
