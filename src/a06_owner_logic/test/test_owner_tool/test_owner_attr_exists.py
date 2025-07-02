from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.owner_tool import (
    owner_acct_membership_exists,
    owner_acctunit_exists,
    owner_attr_exists,
    owner_concept_awardlink_exists,
    owner_concept_factunit_exists,
    owner_concept_healerlink_exists,
    owner_concept_laborlink_exists,
    owner_concept_reason_premiseunit_exists as premiseunit_exists,
    owner_concept_reasonunit_exists,
    owner_conceptunit_exists,
    ownerunit_exists,
)
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    awardee_title_str,
    concept_rope_str,
    fcontext_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_concept_awardlink_str,
    owner_concept_factunit_str,
    owner_concept_healerlink_str,
    owner_concept_laborlink_str,
    owner_concept_reason_premiseunit_str,
    owner_concept_reasonunit_str,
    owner_conceptunit_str,
    ownerunit_str,
    pstate_str,
    rcontext_str,
)


def test_ownerunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not ownerunit_exists(None)
    assert ownerunit_exists(ownerunit_shop("Sue"))


def test_owner_acctunit_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_owner = ownerunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not owner_acctunit_exists(None, {})
    assert not owner_acctunit_exists(sue_owner, jkeys)

    # WHEN
    sue_owner.add_acctunit(yao_str)

    # THEN
    assert owner_acctunit_exists(sue_owner, jkeys)


def test_owner_acct_membership_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_owner = ownerunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}

    # WHEN / THEN
    assert not owner_acct_membership_exists(None, {})
    assert not owner_acct_membership_exists(sue_owner, jkeys)

    # WHEN
    sue_owner.add_acctunit(yao_str)
    # THEN
    assert not owner_acct_membership_exists(sue_owner, jkeys)

    # WHEN
    yao_concept = sue_owner.get_acct(yao_str)
    yao_concept.add_membership(";run")
    # THEN
    assert not owner_acct_membership_exists(sue_owner, jkeys)

    # WHEN
    yao_concept = sue_owner.get_acct(yao_str)
    yao_concept.add_membership(swim_str)
    # THEN
    assert owner_acct_membership_exists(sue_owner, jkeys)


def test_owner_conceptunit_exists_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    sweep_rope = sue_owner.make_rope(clean_rope, "sweep")
    root_rope = to_rope(sue_owner.belief_label)
    root_jkeys = {concept_rope_str(): root_rope}
    casa_jkeys = {concept_rope_str(): casa_rope}
    clean_jkeys = {concept_rope_str(): clean_rope}
    sweep_jkeys = {concept_rope_str(): sweep_rope}

    # WHEN / THEN
    assert not owner_conceptunit_exists(None, {})
    assert not owner_conceptunit_exists(sue_owner, {})
    assert owner_conceptunit_exists(sue_owner, root_jkeys)
    assert not owner_conceptunit_exists(sue_owner, casa_jkeys)
    assert not owner_conceptunit_exists(sue_owner, clean_jkeys)
    assert not owner_conceptunit_exists(sue_owner, sweep_jkeys)

    # WHEN
    sue_owner.add_concept(casa_rope)
    # THEN
    assert not owner_conceptunit_exists(sue_owner, {})
    assert owner_conceptunit_exists(sue_owner, root_jkeys)
    assert owner_conceptunit_exists(sue_owner, casa_jkeys)
    assert not owner_conceptunit_exists(sue_owner, clean_jkeys)
    assert not owner_conceptunit_exists(sue_owner, sweep_jkeys)

    # WHEN
    sue_owner.add_concept(clean_rope)
    # THEN
    assert not owner_conceptunit_exists(sue_owner, {})
    assert owner_conceptunit_exists(sue_owner, root_jkeys)
    assert owner_conceptunit_exists(sue_owner, casa_jkeys)
    assert owner_conceptunit_exists(sue_owner, clean_jkeys)
    assert not owner_conceptunit_exists(sue_owner, sweep_jkeys)


def test_owner_concept_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    swim_str = "Swim"
    root_rope = to_rope(sue_owner.belief_label)
    root_jkeys = {concept_rope_str(): root_rope, awardee_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, awardee_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not owner_concept_awardlink_exists(None, {})
    assert not owner_concept_awardlink_exists(sue_owner, {})
    assert not owner_concept_awardlink_exists(sue_owner, root_jkeys)
    assert not owner_concept_awardlink_exists(sue_owner, casa_jkeys)
    assert not owner_concept_awardlink_exists(sue_owner, clean_jkeys)

    # WHEN
    sue_owner.conceptroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not owner_concept_awardlink_exists(sue_owner, {})
    assert owner_concept_awardlink_exists(sue_owner, root_jkeys)
    assert not owner_concept_awardlink_exists(sue_owner, casa_jkeys)
    assert not owner_concept_awardlink_exists(sue_owner, clean_jkeys)


def test_owner_concept_reasonunit_exists_ReturnsObj():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    root_jkeys = {concept_rope_str(): root_rope, rcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, rcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, rcontext_str(): wk_rope}

    # WHEN / THEN
    assert not owner_concept_reasonunit_exists(None, {})
    assert not owner_concept_reasonunit_exists(sue_owner, {})
    assert not owner_concept_reasonunit_exists(sue_owner, root_jkeys)
    assert not owner_concept_reasonunit_exists(sue_owner, casa_jkeys)
    assert not owner_concept_reasonunit_exists(sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(wk_rope)
    sue_owner.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not owner_concept_reasonunit_exists(sue_owner, {})
    assert owner_concept_reasonunit_exists(sue_owner, root_jkeys)
    assert not owner_concept_reasonunit_exists(sue_owner, casa_jkeys)
    assert not owner_concept_reasonunit_exists(sue_owner, clean_jkeys)


def test_owner_concept_reason_premiseunit_exists_ReturnsObj():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    thur_rope = sue_owner.make_rope(wk_rope, "thur")
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
    assert not premiseunit_exists(sue_owner, {})
    assert not premiseunit_exists(sue_owner, root_jkeys)
    assert not premiseunit_exists(sue_owner, casa_jkeys)
    assert not premiseunit_exists(sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(wk_rope)
    sue_owner.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not premiseunit_exists(sue_owner, {})
    assert not premiseunit_exists(sue_owner, root_jkeys)
    assert not premiseunit_exists(sue_owner, casa_jkeys)
    assert not premiseunit_exists(sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(thur_rope)
    sue_owner.conceptroot.get_reasonunit(wk_rope).set_premise(thur_rope)

    # THEN
    assert not premiseunit_exists(sue_owner, {})
    assert premiseunit_exists(sue_owner, root_jkeys)
    assert not premiseunit_exists(sue_owner, casa_jkeys)
    assert not premiseunit_exists(sue_owner, clean_jkeys)


def test_owner_concept_laborlink_exists_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    swim_str = "Swim"
    root_jkeys = {concept_rope_str(): root_rope, labor_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, labor_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not owner_concept_laborlink_exists(None, {})
    assert not owner_concept_laborlink_exists(sue_owner, {})
    assert not owner_concept_laborlink_exists(sue_owner, root_jkeys)
    assert not owner_concept_laborlink_exists(sue_owner, casa_jkeys)
    assert not owner_concept_laborlink_exists(sue_owner, clean_jkeys)

    # WHEN
    sue_owner.conceptroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not owner_concept_laborlink_exists(sue_owner, {})
    assert owner_concept_laborlink_exists(sue_owner, root_jkeys)
    assert not owner_concept_laborlink_exists(sue_owner, casa_jkeys)
    assert not owner_concept_laborlink_exists(sue_owner, clean_jkeys)


def test_owner_concept_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    swim_str = "Swim"
    root_jkeys = {concept_rope_str(): root_rope, healer_name_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, healer_name_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not owner_concept_healerlink_exists(None, {})
    assert not owner_concept_healerlink_exists(sue_owner, {})
    assert not owner_concept_healerlink_exists(sue_owner, root_jkeys)
    assert not owner_concept_healerlink_exists(sue_owner, casa_jkeys)
    assert not owner_concept_healerlink_exists(sue_owner, clean_jkeys)

    # WHEN
    sue_owner.conceptroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not owner_concept_healerlink_exists(sue_owner, {})
    assert owner_concept_healerlink_exists(sue_owner, root_jkeys)
    assert not owner_concept_healerlink_exists(sue_owner, casa_jkeys)
    assert not owner_concept_healerlink_exists(sue_owner, clean_jkeys)


def test_owner_concept_factunit_exists_ReturnsObj():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    root_jkeys = {concept_rope_str(): root_rope, fcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, fcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, fcontext_str(): wk_rope}

    # WHEN / THEN
    assert not owner_concept_factunit_exists(None, {})
    assert not owner_concept_factunit_exists(sue_owner, {})
    assert not owner_concept_factunit_exists(sue_owner, root_jkeys)
    assert not owner_concept_factunit_exists(sue_owner, casa_jkeys)
    assert not owner_concept_factunit_exists(sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(wk_rope)
    sue_owner.conceptroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not owner_concept_factunit_exists(sue_owner, {})
    assert owner_concept_factunit_exists(sue_owner, root_jkeys)
    assert not owner_concept_factunit_exists(sue_owner, casa_jkeys)
    assert not owner_concept_factunit_exists(sue_owner, clean_jkeys)


def test_owner_attr_exists_ReturnsObj_ownerunit():
    # ESTABLISH / WHEN / THEN
    assert not owner_attr_exists(ownerunit_str(), None, {})
    assert owner_attr_exists(ownerunit_str(), ownerunit_shop("Sue"), {})


def test_owner_attr_exists_ReturnsObj_owner_acctunit():
    # ESTABLISH
    yao_str = "Yao"
    sue_owner = ownerunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not owner_attr_exists(owner_acctunit_str(), None, {})
    assert not owner_attr_exists(owner_acctunit_str(), sue_owner, x_jkeys)

    # WHEN
    sue_owner.add_acctunit(yao_str)

    # THEN
    assert owner_attr_exists(owner_acctunit_str(), sue_owner, x_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_acct_membership():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_owner = ownerunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}
    x_dimen = owner_acct_membership_str()

    # WHEN / THEN
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, x_jkeys)

    # WHEN
    sue_owner.add_acctunit(yao_str)
    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, x_jkeys)

    # WHEN
    yao_concept = sue_owner.get_acct(yao_str)
    yao_concept.add_membership(";run")
    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, x_jkeys)

    # WHEN
    yao_concept = sue_owner.get_acct(yao_str)
    yao_concept.add_membership(swim_str)
    # THEN
    assert owner_attr_exists(x_dimen, sue_owner, x_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_conceptunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    sweep_rope = sue_owner.make_rope(clean_rope, "sweep")
    x_parent_rope = to_rope(sue_owner.belief_label)
    root_jkeys = {concept_rope_str(): x_parent_rope}
    casa_jkeys = {concept_rope_str(): casa_rope}
    clean_jkeys = {concept_rope_str(): clean_rope}
    sweep_jkeys = {concept_rope_str(): sweep_rope}
    x_dimen = owner_conceptunit_str()

    # WHEN / THEN
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, sweep_jkeys)

    # WHEN
    sue_owner.add_concept(casa_rope)
    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, sweep_jkeys)

    # WHEN
    sue_owner.add_concept(clean_rope)
    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert owner_attr_exists(x_dimen, sue_owner, clean_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, sweep_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_concept_awardlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    swim_str = "Swim"
    x_dimen = owner_concept_awardlink_str()
    root_jkeys = {concept_rope_str(): root_rope, awardee_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, awardee_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert not owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)

    # WHEN
    sue_owner.conceptroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_concept_reasonunit():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    x_dimen = owner_concept_reasonunit_str()
    root_jkeys = {concept_rope_str(): root_rope, rcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, rcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, rcontext_str(): wk_rope}

    # WHEN / THEN
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert not owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(wk_rope)
    sue_owner.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_concept_reason_premiseunit():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    thur_rope = sue_owner.make_rope(wk_rope, "thur")
    x_dimen = owner_concept_reason_premiseunit_str()
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
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert not owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(wk_rope)
    sue_owner.conceptroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(thur_rope)
    sue_owner.conceptroot.get_reasonunit(wk_rope).set_premise(thur_rope)

    # THEN
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_concept_laborlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    swim_str = "Swim"
    x_dimen = owner_concept_laborlink_str()
    root_jkeys = {concept_rope_str(): root_rope, labor_title_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, labor_title_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert not owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)

    # WHEN
    sue_owner.conceptroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_concept_healerlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    swim_str = "Swim"
    x_dimen = owner_concept_healerlink_str()
    root_jkeys = {concept_rope_str(): root_rope, healer_name_str(): swim_str}
    casa_jkeys = {concept_rope_str(): casa_rope, healer_name_str(): swim_str}
    clean_jkeys = {concept_rope_str(): clean_rope, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert not owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)

    # WHEN
    sue_owner.conceptroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)


def test_owner_attr_exists_ReturnsObj_owner_concept_factunit():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    root_rope = to_rope(sue_owner.belief_label)
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    x_dimen = owner_concept_factunit_str()
    root_jkeys = {concept_rope_str(): root_rope, fcontext_str(): wk_rope}
    casa_jkeys = {concept_rope_str(): casa_rope, fcontext_str(): wk_rope}
    clean_jkeys = {concept_rope_str(): clean_rope, fcontext_str(): wk_rope}

    # WHEN / THEN
    assert not owner_attr_exists(x_dimen, None, {})
    assert not owner_attr_exists(x_dimen, sue_owner, {})
    assert not owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)

    # WHEN
    sue_owner.add_concept(wk_rope)
    sue_owner.conceptroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert owner_attr_exists(x_dimen, sue_owner, root_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, casa_jkeys)
    assert not owner_attr_exists(x_dimen, sue_owner, clean_jkeys)
