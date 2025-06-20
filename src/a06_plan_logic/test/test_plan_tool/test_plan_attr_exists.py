from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
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
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    awardee_title_str,
    concept_rope_str,
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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    sweep_rope = sue_plan.make_rope(clean_rope, "sweep")
    root_rope = to_rope(sue_plan.vow_label)
    root_jkeys = {concept_rope_str(): root_rope}
    casa_jkeys = {concept_rope_str(): casa_rope}
    clean_jkeys = {concept_rope_str(): clean_rope}
    sweep_jkeys = {concept_rope_str(): sweep_rope}

    # WHEN / THEN
    assert not plan_conceptunit_exists(None, {})
    assert not plan_conceptunit_exists(sue_plan, {})
    assert plan_conceptunit_exists(sue_plan, root_jkeys)
    assert not plan_conceptunit_exists(sue_plan, casa_jkeys)
    assert not plan_conceptunit_exists(sue_plan, clean_jkeys)
    assert not plan_conceptunit_exists(sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(casa_rope)
    # THEN
    assert not plan_conceptunit_exists(sue_plan, {})
    assert plan_conceptunit_exists(sue_plan, root_jkeys)
    assert plan_conceptunit_exists(sue_plan, casa_jkeys)
    assert not plan_conceptunit_exists(sue_plan, clean_jkeys)
    assert not plan_conceptunit_exists(sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(clean_rope)
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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    swim_str = "Swim"
    root_rope = to_rope(sue_plan.vow_label)
    root_jkeys = {concept_rope_str(): root_rope, awardee_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, awardee_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, awardee_title_str(): swim_str}

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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    wk_str = "wk"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    root_jkeys = {concept_rope_str(): root_rope, rcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, rcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, rcontext_str(): wk_rope}

    # WHEN / THEN
    assert not plan_concept_reasonunit_exists(None, {})
    assert not plan_concept_reasonunit_exists(sue_plan, {})
    assert not plan_concept_reasonunit_exists(sue_plan, root_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, casa_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_rope)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not plan_concept_reasonunit_exists(sue_plan, {})
    assert plan_concept_reasonunit_exists(sue_plan, root_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, casa_jkeys)
    assert not plan_concept_reasonunit_exists(sue_plan, clean_jkeys)


def test_plan_concept_reason_premiseunit_exists_ReturnsObj():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    wk_str = "wk"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    thur_rope = sue_plan.make_rope(wk_rope, "thur")
    root_jkeys = {
        concept_rope_str(): root_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    casa_jkeys = {
        concept_rope_str(): casa_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    clean_jkeys = {
        concept_rope_str(): clean_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }

    # WHEN / THEN
    assert not premiseunit_exists(None, {})
    assert not premiseunit_exists(sue_plan, {})
    assert not premiseunit_exists(sue_plan, root_jkeys)
    assert not premiseunit_exists(sue_plan, casa_jkeys)
    assert not premiseunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_rope)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not premiseunit_exists(sue_plan, {})
    assert not premiseunit_exists(sue_plan, root_jkeys)
    assert not premiseunit_exists(sue_plan, casa_jkeys)
    assert not premiseunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(thur_rope)
    sue_plan.conceptroot.get_reasonunit(wk_rope).set_premise(thur_rope)

    # THEN
    assert not premiseunit_exists(sue_plan, {})
    assert premiseunit_exists(sue_plan, root_jkeys)
    assert not premiseunit_exists(sue_plan, casa_jkeys)
    assert not premiseunit_exists(sue_plan, clean_jkeys)


def test_plan_concept_laborlink_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    swim_str = "Swim"
    root_jkeys = {concept_rope_str(): root_rope, labor_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, labor_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, labor_title_str(): swim_str}

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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    swim_str = "Swim"
    root_jkeys = {concept_rope_str(): root_rope, healer_name_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, healer_name_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, healer_name_str(): swim_str}

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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    wk_str = "wk"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    root_jkeys = {concept_rope_str(): root_rope, fcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, fcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, fcontext_str(): wk_rope}

    # WHEN / THEN
    assert not plan_concept_factunit_exists(None, {})
    assert not plan_concept_factunit_exists(sue_plan, {})
    assert not plan_concept_factunit_exists(sue_plan, root_jkeys)
    assert not plan_concept_factunit_exists(sue_plan, casa_jkeys)
    assert not plan_concept_factunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_rope)
    sue_plan.conceptroot.set_factunit(factunit_shop(wk_rope))

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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    sweep_rope = sue_plan.make_rope(clean_rope, "sweep")
    x_parent_rope = to_rope(sue_plan.vow_label)
    root_jkeys = {concept_rope_str(): x_parent_rope}
    casa_jkeys = {concept_rope_str(): casa_rope}
    clean_jkeys = {concept_rope_str(): clean_rope}
    sweep_jkeys = {concept_rope_str(): sweep_rope}
    x_dimen = plan_conceptunit_str()

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(casa_rope)
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_concept(clean_rope)
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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    swim_str = "Swim"
    x_dimen = plan_concept_awardlink_str()
    root_jkeys = {concept_rope_str(): root_rope, awardee_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, awardee_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, awardee_title_str(): swim_str}

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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    wk_str = "wk"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    x_dimen = plan_concept_reasonunit_str()
    root_jkeys = {concept_rope_str(): root_rope, rcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, rcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, rcontext_str(): wk_rope}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_rope)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_reason_premiseunit():
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    wk_str = "wk"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    thur_rope = sue_plan.make_rope(wk_rope, "thur")
    x_dimen = plan_concept_reason_premiseunit_str()
    root_jkeys = {
        concept_rope_str(): root_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    casa_jkeys = {
        concept_rope_str(): casa_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    clean_jkeys = {
        concept_rope_str(): clean_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_rope)
    sue_plan.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(thur_rope)
    sue_plan.conceptroot.get_reasonunit(wk_rope).set_premise(thur_rope)

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_concept_laborlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    swim_str = "Swim"
    x_dimen = plan_concept_laborlink_str()
    root_jkeys = {concept_rope_str(): root_rope, labor_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, labor_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, labor_title_str(): swim_str}

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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    swim_str = "Swim"
    x_dimen = plan_concept_healerlink_str()
    root_jkeys = {concept_rope_str(): root_rope, healer_name_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, healer_name_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, healer_name_str(): swim_str}

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
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_plan.vow_label)
    wk_str = "wk"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    x_dimen = plan_concept_factunit_str()
    root_jkeys = {concept_rope_str(): root_rope, fcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, fcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, fcontext_str(): wk_rope}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_concept(wk_rope)
    sue_plan.conceptroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
