from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.believer_tool import (
    believer_acct_membership_exists,
    believer_acctunit_exists,
    believer_attr_exists,
    believer_plan_awardlink_exists,
    believer_plan_factunit_exists,
    believer_plan_healerlink_exists,
    believer_plan_laborlink_exists,
    believer_plan_reason_premiseunit_exists as premiseunit_exists,
    believer_plan_reasonunit_exists,
    believer_planunit_exists,
    believerunit_exists,
)
from src.a06_believer_logic.test._util.a06_str import (
    acct_name_str,
    awardee_title_str,
    believer_acct_membership_str,
    believer_acctunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_premiseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
    fcontext_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    plan_rope_str,
    pstate_str,
    rcontext_str,
)


def test_believerunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not believerunit_exists(None)
    assert believerunit_exists(believerunit_shop("Sue"))


def test_believer_acctunit_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_believer = believerunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not believer_acctunit_exists(None, {})
    assert not believer_acctunit_exists(sue_believer, jkeys)

    # WHEN
    sue_believer.add_acctunit(yao_str)

    # THEN
    assert believer_acctunit_exists(sue_believer, jkeys)


def test_believer_acct_membership_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_believer = believerunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}

    # WHEN / THEN
    assert not believer_acct_membership_exists(None, {})
    assert not believer_acct_membership_exists(sue_believer, jkeys)

    # WHEN
    sue_believer.add_acctunit(yao_str)
    # THEN
    assert not believer_acct_membership_exists(sue_believer, jkeys)

    # WHEN
    yao_plan = sue_believer.get_acct(yao_str)
    yao_plan.add_membership(";run")
    # THEN
    assert not believer_acct_membership_exists(sue_believer, jkeys)

    # WHEN
    yao_plan = sue_believer.get_acct(yao_str)
    yao_plan.add_membership(swim_str)
    # THEN
    assert believer_acct_membership_exists(sue_believer, jkeys)


def test_believer_planunit_exists_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    sweep_rope = sue_believer.make_rope(clean_rope, "sweep")
    root_rope = to_rope(sue_believer.belief_label)
    root_jkeys = {plan_rope_str(): root_rope}
    casa_jkeys = {plan_rope_str(): casa_rope}
    clean_jkeys = {plan_rope_str(): clean_rope}
    sweep_jkeys = {plan_rope_str(): sweep_rope}

    # WHEN / THEN
    assert not believer_planunit_exists(None, {})
    assert not believer_planunit_exists(sue_believer, {})
    assert believer_planunit_exists(sue_believer, root_jkeys)
    assert not believer_planunit_exists(sue_believer, casa_jkeys)
    assert not believer_planunit_exists(sue_believer, clean_jkeys)
    assert not believer_planunit_exists(sue_believer, sweep_jkeys)

    # WHEN
    sue_believer.add_plan(casa_rope)
    # THEN
    assert not believer_planunit_exists(sue_believer, {})
    assert believer_planunit_exists(sue_believer, root_jkeys)
    assert believer_planunit_exists(sue_believer, casa_jkeys)
    assert not believer_planunit_exists(sue_believer, clean_jkeys)
    assert not believer_planunit_exists(sue_believer, sweep_jkeys)

    # WHEN
    sue_believer.add_plan(clean_rope)
    # THEN
    assert not believer_planunit_exists(sue_believer, {})
    assert believer_planunit_exists(sue_believer, root_jkeys)
    assert believer_planunit_exists(sue_believer, casa_jkeys)
    assert believer_planunit_exists(sue_believer, clean_jkeys)
    assert not believer_planunit_exists(sue_believer, sweep_jkeys)


def test_believer_plan_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    swim_str = "Swim"
    root_rope = to_rope(sue_believer.belief_label)
    root_jkeys = {plan_rope_str(): root_rope, awardee_title_str(): swim_str}
    casa_jkeys = {plan_rope_str(): casa_rope, awardee_title_str(): swim_str}
    clean_jkeys = {plan_rope_str(): clean_rope, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not believer_plan_awardlink_exists(None, {})
    assert not believer_plan_awardlink_exists(sue_believer, {})
    assert not believer_plan_awardlink_exists(sue_believer, root_jkeys)
    assert not believer_plan_awardlink_exists(sue_believer, casa_jkeys)
    assert not believer_plan_awardlink_exists(sue_believer, clean_jkeys)

    # WHEN
    sue_believer.planroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not believer_plan_awardlink_exists(sue_believer, {})
    assert believer_plan_awardlink_exists(sue_believer, root_jkeys)
    assert not believer_plan_awardlink_exists(sue_believer, casa_jkeys)
    assert not believer_plan_awardlink_exists(sue_believer, clean_jkeys)


def test_believer_plan_reasonunit_exists_ReturnsObj():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    root_jkeys = {plan_rope_str(): root_rope, rcontext_str(): wk_rope}
    casa_jkeys = {plan_rope_str(): casa_rope, rcontext_str(): wk_rope}
    clean_jkeys = {plan_rope_str(): clean_rope, rcontext_str(): wk_rope}

    # WHEN / THEN
    assert not believer_plan_reasonunit_exists(None, {})
    assert not believer_plan_reasonunit_exists(sue_believer, {})
    assert not believer_plan_reasonunit_exists(sue_believer, root_jkeys)
    assert not believer_plan_reasonunit_exists(sue_believer, casa_jkeys)
    assert not believer_plan_reasonunit_exists(sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(wk_rope)
    sue_believer.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not believer_plan_reasonunit_exists(sue_believer, {})
    assert believer_plan_reasonunit_exists(sue_believer, root_jkeys)
    assert not believer_plan_reasonunit_exists(sue_believer, casa_jkeys)
    assert not believer_plan_reasonunit_exists(sue_believer, clean_jkeys)


def test_believer_plan_reason_premiseunit_exists_ReturnsObj():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    thur_rope = sue_believer.make_rope(wk_rope, "thur")
    root_jkeys = {
        plan_rope_str(): root_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    casa_jkeys = {
        plan_rope_str(): casa_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    clean_jkeys = {
        plan_rope_str(): clean_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }

    # WHEN / THEN
    assert not premiseunit_exists(None, {})
    assert not premiseunit_exists(sue_believer, {})
    assert not premiseunit_exists(sue_believer, root_jkeys)
    assert not premiseunit_exists(sue_believer, casa_jkeys)
    assert not premiseunit_exists(sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(wk_rope)
    sue_believer.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not premiseunit_exists(sue_believer, {})
    assert not premiseunit_exists(sue_believer, root_jkeys)
    assert not premiseunit_exists(sue_believer, casa_jkeys)
    assert not premiseunit_exists(sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(thur_rope)
    sue_believer.planroot.get_reasonunit(wk_rope).set_premise(thur_rope)

    # THEN
    assert not premiseunit_exists(sue_believer, {})
    assert premiseunit_exists(sue_believer, root_jkeys)
    assert not premiseunit_exists(sue_believer, casa_jkeys)
    assert not premiseunit_exists(sue_believer, clean_jkeys)


def test_believer_plan_laborlink_exists_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    swim_str = "Swim"
    root_jkeys = {plan_rope_str(): root_rope, labor_title_str(): swim_str}
    casa_jkeys = {plan_rope_str(): casa_rope, labor_title_str(): swim_str}
    clean_jkeys = {plan_rope_str(): clean_rope, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not believer_plan_laborlink_exists(None, {})
    assert not believer_plan_laborlink_exists(sue_believer, {})
    assert not believer_plan_laborlink_exists(sue_believer, root_jkeys)
    assert not believer_plan_laborlink_exists(sue_believer, casa_jkeys)
    assert not believer_plan_laborlink_exists(sue_believer, clean_jkeys)

    # WHEN
    sue_believer.planroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not believer_plan_laborlink_exists(sue_believer, {})
    assert believer_plan_laborlink_exists(sue_believer, root_jkeys)
    assert not believer_plan_laborlink_exists(sue_believer, casa_jkeys)
    assert not believer_plan_laborlink_exists(sue_believer, clean_jkeys)


def test_believer_plan_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    swim_str = "Swim"
    root_jkeys = {plan_rope_str(): root_rope, healer_name_str(): swim_str}
    casa_jkeys = {plan_rope_str(): casa_rope, healer_name_str(): swim_str}
    clean_jkeys = {plan_rope_str(): clean_rope, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not believer_plan_healerlink_exists(None, {})
    assert not believer_plan_healerlink_exists(sue_believer, {})
    assert not believer_plan_healerlink_exists(sue_believer, root_jkeys)
    assert not believer_plan_healerlink_exists(sue_believer, casa_jkeys)
    assert not believer_plan_healerlink_exists(sue_believer, clean_jkeys)

    # WHEN
    sue_believer.planroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not believer_plan_healerlink_exists(sue_believer, {})
    assert believer_plan_healerlink_exists(sue_believer, root_jkeys)
    assert not believer_plan_healerlink_exists(sue_believer, casa_jkeys)
    assert not believer_plan_healerlink_exists(sue_believer, clean_jkeys)


def test_believer_plan_factunit_exists_ReturnsObj():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    root_jkeys = {plan_rope_str(): root_rope, fcontext_str(): wk_rope}
    casa_jkeys = {plan_rope_str(): casa_rope, fcontext_str(): wk_rope}
    clean_jkeys = {plan_rope_str(): clean_rope, fcontext_str(): wk_rope}

    # WHEN / THEN
    assert not believer_plan_factunit_exists(None, {})
    assert not believer_plan_factunit_exists(sue_believer, {})
    assert not believer_plan_factunit_exists(sue_believer, root_jkeys)
    assert not believer_plan_factunit_exists(sue_believer, casa_jkeys)
    assert not believer_plan_factunit_exists(sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(wk_rope)
    sue_believer.planroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not believer_plan_factunit_exists(sue_believer, {})
    assert believer_plan_factunit_exists(sue_believer, root_jkeys)
    assert not believer_plan_factunit_exists(sue_believer, casa_jkeys)
    assert not believer_plan_factunit_exists(sue_believer, clean_jkeys)


def test_believer_attr_exists_ReturnsObj_believerunit():
    # ESTABLISH / WHEN / THEN
    assert not believer_attr_exists(believerunit_str(), None, {})
    assert believer_attr_exists(believerunit_str(), believerunit_shop("Sue"), {})


def test_believer_attr_exists_ReturnsObj_believer_acctunit():
    # ESTABLISH
    yao_str = "Yao"
    sue_believer = believerunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not believer_attr_exists(believer_acctunit_str(), None, {})
    assert not believer_attr_exists(believer_acctunit_str(), sue_believer, x_jkeys)

    # WHEN
    sue_believer.add_acctunit(yao_str)

    # THEN
    assert believer_attr_exists(believer_acctunit_str(), sue_believer, x_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_acct_membership():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_believer = believerunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}
    x_dimen = believer_acct_membership_str()

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, x_jkeys)

    # WHEN
    sue_believer.add_acctunit(yao_str)
    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, x_jkeys)

    # WHEN
    yao_plan = sue_believer.get_acct(yao_str)
    yao_plan.add_membership(";run")
    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, x_jkeys)

    # WHEN
    yao_plan = sue_believer.get_acct(yao_str)
    yao_plan.add_membership(swim_str)
    # THEN
    assert believer_attr_exists(x_dimen, sue_believer, x_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_planunit():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    sweep_rope = sue_believer.make_rope(clean_rope, "sweep")
    x_parent_rope = to_rope(sue_believer.belief_label)
    root_jkeys = {plan_rope_str(): x_parent_rope}
    casa_jkeys = {plan_rope_str(): casa_rope}
    clean_jkeys = {plan_rope_str(): clean_rope}
    sweep_jkeys = {plan_rope_str(): sweep_rope}
    x_dimen = believer_planunit_str()

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, sweep_jkeys)

    # WHEN
    sue_believer.add_plan(casa_rope)
    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, sweep_jkeys)

    # WHEN
    sue_believer.add_plan(clean_rope)
    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert believer_attr_exists(x_dimen, sue_believer, clean_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, sweep_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_plan_awardlink():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    swim_str = "Swim"
    x_dimen = believer_plan_awardlink_str()
    root_jkeys = {plan_rope_str(): root_rope, awardee_title_str(): swim_str}
    casa_jkeys = {plan_rope_str(): casa_rope, awardee_title_str(): swim_str}
    clean_jkeys = {plan_rope_str(): clean_rope, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert not believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)

    # WHEN
    sue_believer.planroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_plan_reasonunit():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    x_dimen = believer_plan_reasonunit_str()
    root_jkeys = {plan_rope_str(): root_rope, rcontext_str(): wk_rope}
    casa_jkeys = {plan_rope_str(): casa_rope, rcontext_str(): wk_rope}
    clean_jkeys = {plan_rope_str(): clean_rope, rcontext_str(): wk_rope}

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert not believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(wk_rope)
    sue_believer.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_plan_reason_premiseunit():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    thur_rope = sue_believer.make_rope(wk_rope, "thur")
    x_dimen = believer_plan_reason_premiseunit_str()
    root_jkeys = {
        plan_rope_str(): root_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    casa_jkeys = {
        plan_rope_str(): casa_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    clean_jkeys = {
        plan_rope_str(): clean_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert not believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(wk_rope)
    sue_believer.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(thur_rope)
    sue_believer.planroot.get_reasonunit(wk_rope).set_premise(thur_rope)

    # THEN
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_plan_laborlink():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    swim_str = "Swim"
    x_dimen = believer_plan_laborlink_str()
    root_jkeys = {plan_rope_str(): root_rope, labor_title_str(): swim_str}
    casa_jkeys = {plan_rope_str(): casa_rope, labor_title_str(): swim_str}
    clean_jkeys = {plan_rope_str(): clean_rope, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert not believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)

    # WHEN
    sue_believer.planroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_plan_healerlink():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    swim_str = "Swim"
    x_dimen = believer_plan_healerlink_str()
    root_jkeys = {plan_rope_str(): root_rope, healer_name_str(): swim_str}
    casa_jkeys = {plan_rope_str(): casa_rope, healer_name_str(): swim_str}
    clean_jkeys = {plan_rope_str(): clean_rope, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert not believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)

    # WHEN
    sue_believer.planroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)


def test_believer_attr_exists_ReturnsObj_believer_plan_factunit():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_believer.belief_label)
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    x_dimen = believer_plan_factunit_str()
    root_jkeys = {plan_rope_str(): root_rope, fcontext_str(): wk_rope}
    casa_jkeys = {plan_rope_str(): casa_rope, fcontext_str(): wk_rope}
    clean_jkeys = {plan_rope_str(): clean_rope, fcontext_str(): wk_rope}

    # WHEN / THEN
    assert not believer_attr_exists(x_dimen, None, {})
    assert not believer_attr_exists(x_dimen, sue_believer, {})
    assert not believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)

    # WHEN
    sue_believer.add_plan(wk_rope)
    sue_believer.planroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert believer_attr_exists(x_dimen, sue_believer, root_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, casa_jkeys)
    assert not believer_attr_exists(x_dimen, sue_believer, clean_jkeys)
