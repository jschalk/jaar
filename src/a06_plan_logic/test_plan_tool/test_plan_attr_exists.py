from src.a01_term_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    awardee_title_str,
    concept_way_str,
    fcontext_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    planunit_str,
    pstate_str,
    rcontext_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.plan_tool import (
    plan_acct_membership_exists,
    plan_acctunit_exists,
    plan_attr_exists,
    plan_concept_awardlink_exists,
    plan_concept_factunit_exists,
    plan_concept_healerlink_exists,
    plan_concept_laborlink_exists,
    plan_concept_reason_premiseunit_exists as premiseunit_exists,
    plan_concept_reasonunit_exists,
    plan_conceptunit_exists,
    planunit_exists,
)


def test_planunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not planunit_exists(None)
    assert planunit_exists(planunit_shop("Sue"))


def test_plan_acctunit_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_plan = planunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not plan_acctunit_exists(None, {})
    assert not plan_acctunit_exists(sue_plan, jkeys)

    # WHEN
    sue_plan.add_acctunit(yao_str)

    # THEN
    assert plan_acctunit_exists(sue_plan, jkeys)


def test_plan_acct_membership_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}

    # WHEN / THEN
    assert not plan_acct_membership_exists(None, {})
    assert not plan_acct_membership_exists(sue_plan, jkeys)

    # WHEN
    sue_plan.add_acctunit(yao_str)
    # THEN
    assert not plan_acct_membership_exists(sue_plan, jkeys)

    # WHEN
    yao_concept = sue_plan.get_acct(yao_str)
    yao_concept.add_membership(";run")
    # THEN
    assert not plan_acct_membership_exists(sue_plan, jkeys)

    # WHEN
    yao_concept = sue_plan.get_acct(yao_str)
    yao_concept.add_membership(swim_str)
    # THEN
    assert plan_acct_membership_exists(sue_plan, jkeys)


def test_plan_conceptunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    sweep_way = sue_plan.make_way(clean_way, "sweep")
    root_way = to_way(sue_plan.vow_label)
    root_jkeys = {concept_way_str(): root_way}
    casa_jkeys = {concept_way_str(): casa_way}
    clean_jkeys = {concept_way_str(): clean_way}
    sweep_jkeys = {concept_way_str(): sweep_way}

    # WHEN / THEN
    assert not plan_conceptunit_exists(None, {})
    assert not plan_conceptunit_exists(sue_plan, {})
    assert plan_conceptunit_exists(sue_plan, root_jkeys)
    assert not plan_conceptunit_exists(sue_plan, casa_jkeys)
    assert not plan_conceptunit_exists(sue_plan, clean_jkeys)
    assert not plan_conceptunit_exists(sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(casa_way)
    # THEN
    assert not plan_conceptunit_exists(sue_plan, {})
    assert plan_conceptunit_exists(sue_plan, root_jkeys)
    assert plan_conceptunit_exists(sue_plan, casa_jkeys)
    assert not plan_conceptunit_exists(sue_plan, clean_jkeys)
    assert not plan_conceptunit_exists(sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(clean_way)
    # THEN
    assert not plan_conceptunit_exists(sue_plan, {})
    assert plan_conceptunit_exists(sue_plan, root_jkeys)
    assert plan_conceptunit_exists(sue_plan, casa_jkeys)
    assert plan_conceptunit_exists(sue_plan, clean_jkeys)
    assert not plan_conceptunit_exists(sue_plan, sweep_jkeys)


def test_plan_concept_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    swim_str = "Swim"
    root_way = to_way(sue_plan.vow_label)
    root_jkeys = {concept_way_str(): root_way, awardee_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, awardee_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not plan_concept_awardlink_exists(None, {})
    assert not plan_concept_awardlink_exists(sue_plan, {})
    assert not plan_concept_awardlink_exists(sue_plan, root_jkeys)
    assert not plan_concept_awardlink_exists(sue_plan, casa_jkeys)
    assert not plan_concept_awardlink_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.conceptroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not plan_concept_awardlink_exists(sue_plan, {})
    assert plan_concept_awardlink_exists(sue_plan, root_jkeys)
    assert not plan_concept_awardlink_exists(sue_plan, casa_jkeys)
    assert not plan_concept_awardlink_exists(sue_plan, clean_jkeys)


def test_plan_concept_reasonunit_exists_ReturnsObj():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    root_jkeys = {concept_way_str(): root_way, rcontext_str(): wk_way}
    casa_jkeys = {concept_way_str(): casa_way, rcontext_str(): wk_way}
    clean_jkeys = {concept_way_str(): clean_way, rcontext_str(): wk_way}

    # WHEN / THEN
    assert not plan_concept_reasonunit_exists(None, {})
    assert not plan_concept_reasonunit_exists(sue_plan, {})
    assert not plan_concept_reasonunit_exists(sue_plan, root_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, casa_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_way)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_way))

    # THEN
    assert not plan_concept_reasonunit_exists(sue_plan, {})
    assert plan_concept_reasonunit_exists(sue_plan, root_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, casa_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, clean_jkeys)


def test_plan_concept_reason_premiseunit_exists_ReturnsObj():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    thur_way = sue_plan.make_way(wk_way, "thur")
    root_jkeys = {
        concept_way_str(): root_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }
    casa_jkeys = {
        concept_way_str(): casa_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }
    clean_jkeys = {
        concept_way_str(): clean_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }

    # WHEN / THEN
    assert not premiseunit_exists(None, {})
    assert not premiseunit_exists(sue_plan, {})
    assert not premiseunit_exists(sue_plan, root_jkeys)
    assert not premiseunit_exists(sue_plan, casa_jkeys)
    assert not premiseunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_way)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_way))

    # THEN
    assert not premiseunit_exists(sue_plan, {})
    assert not premiseunit_exists(sue_plan, root_jkeys)
    assert not premiseunit_exists(sue_plan, casa_jkeys)
    assert not premiseunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(thur_way)
    sue_plan.conceptroot.get_reasonunit(wk_way).set_premise(thur_way)

    # THEN
    assert not premiseunit_exists(sue_plan, {})
    assert premiseunit_exists(sue_plan, root_jkeys)
    assert not premiseunit_exists(sue_plan, casa_jkeys)
    assert not premiseunit_exists(sue_plan, clean_jkeys)


def test_plan_concept_laborlink_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    swim_str = "Swim"
    root_jkeys = {concept_way_str(): root_way, labor_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, labor_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not plan_concept_laborlink_exists(None, {})
    assert not plan_concept_laborlink_exists(sue_plan, {})
    assert not plan_concept_laborlink_exists(sue_plan, root_jkeys)
    assert not plan_concept_laborlink_exists(sue_plan, casa_jkeys)
    assert not plan_concept_laborlink_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.conceptroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not plan_concept_laborlink_exists(sue_plan, {})
    assert plan_concept_laborlink_exists(sue_plan, root_jkeys)
    assert not plan_concept_laborlink_exists(sue_plan, casa_jkeys)
    assert not plan_concept_laborlink_exists(sue_plan, clean_jkeys)


def test_plan_concept_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    swim_str = "Swim"
    root_jkeys = {concept_way_str(): root_way, healer_name_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, healer_name_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not plan_concept_healerlink_exists(None, {})
    assert not plan_concept_healerlink_exists(sue_plan, {})
    assert not plan_concept_healerlink_exists(sue_plan, root_jkeys)
    assert not plan_concept_healerlink_exists(sue_plan, casa_jkeys)
    assert not plan_concept_healerlink_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.conceptroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not plan_concept_healerlink_exists(sue_plan, {})
    assert plan_concept_healerlink_exists(sue_plan, root_jkeys)
    assert not plan_concept_healerlink_exists(sue_plan, casa_jkeys)
    assert not plan_concept_healerlink_exists(sue_plan, clean_jkeys)


def test_plan_concept_factunit_exists_ReturnsObj():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    root_jkeys = {concept_way_str(): root_way, fcontext_str(): wk_way}
    casa_jkeys = {concept_way_str(): casa_way, fcontext_str(): wk_way}
    clean_jkeys = {concept_way_str(): clean_way, fcontext_str(): wk_way}

    # WHEN / THEN
    assert not plan_concept_factunit_exists(None, {})
    assert not plan_concept_factunit_exists(sue_plan, {})
    assert not plan_concept_factunit_exists(sue_plan, root_jkeys)
    assert not plan_concept_factunit_exists(sue_plan, casa_jkeys)
    assert not plan_concept_factunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_way)
    sue_plan.conceptroot.set_factunit(factunit_shop(wk_way))

    # THEN
    assert not plan_concept_factunit_exists(sue_plan, {})
    assert plan_concept_factunit_exists(sue_plan, root_jkeys)
    assert not plan_concept_factunit_exists(sue_plan, casa_jkeys)
    assert not plan_concept_factunit_exists(sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_planunit():
    # ESTABLISH / WHEN / THEN
    assert not plan_attr_exists(planunit_str(), None, {})
    assert plan_attr_exists(planunit_str(), planunit_shop("Sue"), {})


def test_plan_attr_exists_ReturnsObj_plan_acctunit():
    # ESTABLISH
    yao_str = "Yao"
    sue_plan = planunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not plan_attr_exists(plan_acctunit_str(), None, {})
    assert not plan_attr_exists(plan_acctunit_str(), sue_plan, x_jkeys)

    # WHEN
    sue_plan.add_acctunit(yao_str)

    # THEN
    assert plan_attr_exists(plan_acctunit_str(), sue_plan, x_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_acct_membership():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}
    x_dimen = plan_acct_membership_str()

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, x_jkeys)

    # WHEN
    sue_plan.add_acctunit(yao_str)
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, x_jkeys)

    # WHEN
    yao_concept = sue_plan.get_acct(yao_str)
    yao_concept.add_membership(";run")
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, x_jkeys)

    # WHEN
    yao_concept = sue_plan.get_acct(yao_str)
    yao_concept.add_membership(swim_str)
    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, x_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_conceptunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    sweep_way = sue_plan.make_way(clean_way, "sweep")
    x_parent_way = to_way(sue_plan.vow_label)
    root_jkeys = {concept_way_str(): x_parent_way}
    casa_jkeys = {concept_way_str(): casa_way}
    clean_jkeys = {concept_way_str(): clean_way}
    sweep_jkeys = {concept_way_str(): sweep_way}
    x_dimen = plan_conceptunit_str()

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(casa_way)
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(clean_way)
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_awardlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    swim_str = "Swim"
    x_dimen = plan_concept_awardlink_str()
    root_jkeys = {concept_way_str(): root_way, awardee_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, awardee_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.conceptroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_reasonunit():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    x_dimen = plan_concept_reasonunit_str()
    root_jkeys = {concept_way_str(): root_way, rcontext_str(): wk_way}
    casa_jkeys = {concept_way_str(): casa_way, rcontext_str(): wk_way}
    clean_jkeys = {concept_way_str(): clean_way, rcontext_str(): wk_way}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_way)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_way))

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_reason_premiseunit():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    thur_way = sue_plan.make_way(wk_way, "thur")
    x_dimen = plan_concept_reason_premiseunit_str()
    root_jkeys = {
        concept_way_str(): root_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }
    casa_jkeys = {
        concept_way_str(): casa_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }
    clean_jkeys = {
        concept_way_str(): clean_way,
        rcontext_str(): wk_way,
        pstate_str(): thur_way,
    }

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_way)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_way))

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(thur_way)
    sue_plan.conceptroot.get_reasonunit(wk_way).set_premise(thur_way)

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_laborlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    swim_str = "Swim"
    x_dimen = plan_concept_laborlink_str()
    root_jkeys = {concept_way_str(): root_way, labor_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, labor_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.conceptroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_healerlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    swim_str = "Swim"
    x_dimen = plan_concept_healerlink_str()
    root_jkeys = {concept_way_str(): root_way, healer_name_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, healer_name_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.conceptroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_factunit():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    root_way = to_way(sue_plan.vow_label)
    wk_str = "wk"
    wk_way = sue_plan.make_l1_way(wk_str)
    x_dimen = plan_concept_factunit_str()
    root_jkeys = {concept_way_str(): root_way, fcontext_str(): wk_way}
    casa_jkeys = {concept_way_str(): casa_way, fcontext_str(): wk_way}
    clean_jkeys = {concept_way_str(): clean_way, fcontext_str(): wk_way}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_way)
    sue_plan.conceptroot.set_factunit(factunit_shop(wk_way))

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
