from src.a01_way_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_tool import (
    budunit_exists,
    bud_acctunit_exists,
    bud_acct_membership_exists,
    bud_conceptunit_exists,
    bud_concept_awardlink_exists,
    bud_concept_reasonunit_exists,
    bud_concept_reason_premiseunit_exists as premiseunit_exists,
    bud_concept_laborlink_exists,
    bud_concept_healerlink_exists,
    bud_concept_factunit_exists,
    bud_attr_exists,
)
from src.a06_bud_logic._test_util.a06_str import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
    acct_name_str,
    awardee_title_str,
    rcontext_str,
    fcontext_str,
    group_title_str,
    pstate_str,
    concept_way_str,
    labor_title_str,
    healer_name_str,
)


def test_budunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not budunit_exists(None)
    assert budunit_exists(budunit_shop("Sue"))


def test_bud_acctunit_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not bud_acctunit_exists(None, {})
    assert not bud_acctunit_exists(sue_bud, jkeys)

    # WHEN
    sue_bud.add_acctunit(yao_str)

    # THEN
    assert bud_acctunit_exists(sue_bud, jkeys)


def test_bud_acct_membership_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_bud = budunit_shop("Sue")
    jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}

    # WHEN / THEN
    assert not bud_acct_membership_exists(None, {})
    assert not bud_acct_membership_exists(sue_bud, jkeys)

    # WHEN
    sue_bud.add_acctunit(yao_str)
    # THEN
    assert not bud_acct_membership_exists(sue_bud, jkeys)

    # WHEN
    yao_concept = sue_bud.get_acct(yao_str)
    yao_concept.add_membership(";run")
    # THEN
    assert not bud_acct_membership_exists(sue_bud, jkeys)

    # WHEN
    yao_concept = sue_bud.get_acct(yao_str)
    yao_concept.add_membership(swim_str)
    # THEN
    assert bud_acct_membership_exists(sue_bud, jkeys)


def test_bud_conceptunit_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_way = sue_bud.make_way(clean_way, "sweep")
    root_way = to_way(sue_bud.fisc_label)
    root_jkeys = {concept_way_str(): root_way}
    casa_jkeys = {concept_way_str(): casa_way}
    clean_jkeys = {concept_way_str(): clean_way}
    sweep_jkeys = {concept_way_str(): sweep_way}

    # WHEN / THEN
    assert not bud_conceptunit_exists(None, {})
    assert not bud_conceptunit_exists(sue_bud, {})
    assert bud_conceptunit_exists(sue_bud, root_jkeys)
    assert not bud_conceptunit_exists(sue_bud, casa_jkeys)
    assert not bud_conceptunit_exists(sue_bud, clean_jkeys)
    assert not bud_conceptunit_exists(sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_concept(casa_way)
    # THEN
    assert not bud_conceptunit_exists(sue_bud, {})
    assert bud_conceptunit_exists(sue_bud, root_jkeys)
    assert bud_conceptunit_exists(sue_bud, casa_jkeys)
    assert not bud_conceptunit_exists(sue_bud, clean_jkeys)
    assert not bud_conceptunit_exists(sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_concept(clean_way)
    # THEN
    assert not bud_conceptunit_exists(sue_bud, {})
    assert bud_conceptunit_exists(sue_bud, root_jkeys)
    assert bud_conceptunit_exists(sue_bud, casa_jkeys)
    assert bud_conceptunit_exists(sue_bud, clean_jkeys)
    assert not bud_conceptunit_exists(sue_bud, sweep_jkeys)


def test_bud_concept_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    swim_str = "Swim"
    root_way = to_way(sue_bud.fisc_label)
    root_jkeys = {concept_way_str(): root_way, awardee_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, awardee_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not bud_concept_awardlink_exists(None, {})
    assert not bud_concept_awardlink_exists(sue_bud, {})
    assert not bud_concept_awardlink_exists(sue_bud, root_jkeys)
    assert not bud_concept_awardlink_exists(sue_bud, casa_jkeys)
    assert not bud_concept_awardlink_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.conceptroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not bud_concept_awardlink_exists(sue_bud, {})
    assert bud_concept_awardlink_exists(sue_bud, root_jkeys)
    assert not bud_concept_awardlink_exists(sue_bud, casa_jkeys)
    assert not bud_concept_awardlink_exists(sue_bud, clean_jkeys)


def test_bud_concept_reasonunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    root_jkeys = {concept_way_str(): root_way, rcontext_str(): week_way}
    casa_jkeys = {concept_way_str(): casa_way, rcontext_str(): week_way}
    clean_jkeys = {concept_way_str(): clean_way, rcontext_str(): week_way}

    # WHEN / THEN
    assert not bud_concept_reasonunit_exists(None, {})
    assert not bud_concept_reasonunit_exists(sue_bud, {})
    assert not bud_concept_reasonunit_exists(sue_bud, root_jkeys)
    assert not bud_concept_reasonunit_exists(sue_bud, casa_jkeys)
    assert not bud_concept_reasonunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(week_way)
    sue_bud.conceptroot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not bud_concept_reasonunit_exists(sue_bud, {})
    assert bud_concept_reasonunit_exists(sue_bud, root_jkeys)
    assert not bud_concept_reasonunit_exists(sue_bud, casa_jkeys)
    assert not bud_concept_reasonunit_exists(sue_bud, clean_jkeys)


def test_bud_concept_reason_premiseunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    thur_way = sue_bud.make_way(week_way, "thur")
    root_jkeys = {
        concept_way_str(): root_way,
        rcontext_str(): week_way,
        pstate_str(): thur_way,
    }
    casa_jkeys = {
        concept_way_str(): casa_way,
        rcontext_str(): week_way,
        pstate_str(): thur_way,
    }
    clean_jkeys = {
        concept_way_str(): clean_way,
        rcontext_str(): week_way,
        pstate_str(): thur_way,
    }

    # WHEN / THEN
    assert not premiseunit_exists(None, {})
    assert not premiseunit_exists(sue_bud, {})
    assert not premiseunit_exists(sue_bud, root_jkeys)
    assert not premiseunit_exists(sue_bud, casa_jkeys)
    assert not premiseunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(week_way)
    sue_bud.conceptroot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not premiseunit_exists(sue_bud, {})
    assert not premiseunit_exists(sue_bud, root_jkeys)
    assert not premiseunit_exists(sue_bud, casa_jkeys)
    assert not premiseunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(thur_way)
    sue_bud.conceptroot.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert not premiseunit_exists(sue_bud, {})
    assert premiseunit_exists(sue_bud, root_jkeys)
    assert not premiseunit_exists(sue_bud, casa_jkeys)
    assert not premiseunit_exists(sue_bud, clean_jkeys)


def test_bud_concept_laborlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    swim_str = "Swim"
    root_jkeys = {concept_way_str(): root_way, labor_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, labor_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not bud_concept_laborlink_exists(None, {})
    assert not bud_concept_laborlink_exists(sue_bud, {})
    assert not bud_concept_laborlink_exists(sue_bud, root_jkeys)
    assert not bud_concept_laborlink_exists(sue_bud, casa_jkeys)
    assert not bud_concept_laborlink_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.conceptroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not bud_concept_laborlink_exists(sue_bud, {})
    assert bud_concept_laborlink_exists(sue_bud, root_jkeys)
    assert not bud_concept_laborlink_exists(sue_bud, casa_jkeys)
    assert not bud_concept_laborlink_exists(sue_bud, clean_jkeys)


def test_bud_concept_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    swim_str = "Swim"
    root_jkeys = {concept_way_str(): root_way, healer_name_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, healer_name_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not bud_concept_healerlink_exists(None, {})
    assert not bud_concept_healerlink_exists(sue_bud, {})
    assert not bud_concept_healerlink_exists(sue_bud, root_jkeys)
    assert not bud_concept_healerlink_exists(sue_bud, casa_jkeys)
    assert not bud_concept_healerlink_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.conceptroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not bud_concept_healerlink_exists(sue_bud, {})
    assert bud_concept_healerlink_exists(sue_bud, root_jkeys)
    assert not bud_concept_healerlink_exists(sue_bud, casa_jkeys)
    assert not bud_concept_healerlink_exists(sue_bud, clean_jkeys)


def test_bud_concept_factunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    root_jkeys = {concept_way_str(): root_way, fcontext_str(): week_way}
    casa_jkeys = {concept_way_str(): casa_way, fcontext_str(): week_way}
    clean_jkeys = {concept_way_str(): clean_way, fcontext_str(): week_way}

    # WHEN / THEN
    assert not bud_concept_factunit_exists(None, {})
    assert not bud_concept_factunit_exists(sue_bud, {})
    assert not bud_concept_factunit_exists(sue_bud, root_jkeys)
    assert not bud_concept_factunit_exists(sue_bud, casa_jkeys)
    assert not bud_concept_factunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(week_way)
    sue_bud.conceptroot.set_factunit(factunit_shop(week_way))

    # THEN
    assert not bud_concept_factunit_exists(sue_bud, {})
    assert bud_concept_factunit_exists(sue_bud, root_jkeys)
    assert not bud_concept_factunit_exists(sue_bud, casa_jkeys)
    assert not bud_concept_factunit_exists(sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_budunit():
    # ESTABLISH / WHEN / THEN
    assert not bud_attr_exists(budunit_str(), None, {})
    assert bud_attr_exists(budunit_str(), budunit_shop("Sue"), {})


def test_bud_attr_exists_ReturnsObj_bud_acctunit():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str}

    # WHEN / THEN
    assert not bud_attr_exists(bud_acctunit_str(), None, {})
    assert not bud_attr_exists(bud_acctunit_str(), sue_bud, x_jkeys)

    # WHEN
    sue_bud.add_acctunit(yao_str)

    # THEN
    assert bud_attr_exists(bud_acctunit_str(), sue_bud, x_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_acct_membership():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_bud = budunit_shop("Sue")
    x_jkeys = {acct_name_str(): yao_str, group_title_str(): swim_str}
    x_dimen = bud_acct_membership_str()

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, x_jkeys)

    # WHEN
    sue_bud.add_acctunit(yao_str)
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, x_jkeys)

    # WHEN
    yao_concept = sue_bud.get_acct(yao_str)
    yao_concept.add_membership(";run")
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, x_jkeys)

    # WHEN
    yao_concept = sue_bud.get_acct(yao_str)
    yao_concept.add_membership(swim_str)
    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, x_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_conceptunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_way = sue_bud.make_way(clean_way, "sweep")
    x_parent_way = to_way(sue_bud.fisc_label)
    root_jkeys = {concept_way_str(): x_parent_way}
    casa_jkeys = {concept_way_str(): casa_way}
    clean_jkeys = {concept_way_str(): clean_way}
    sweep_jkeys = {concept_way_str(): sweep_way}
    x_dimen = bud_conceptunit_str()

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_concept(casa_way)
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_concept(clean_way)
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, sweep_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_concept_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    swim_str = "Swim"
    x_dimen = bud_concept_awardlink_str()
    root_jkeys = {concept_way_str(): root_way, awardee_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, awardee_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, awardee_title_str(): swim_str}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.conceptroot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_concept_reasonunit():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    x_dimen = bud_concept_reasonunit_str()
    root_jkeys = {concept_way_str(): root_way, rcontext_str(): week_way}
    casa_jkeys = {concept_way_str(): casa_way, rcontext_str(): week_way}
    clean_jkeys = {concept_way_str(): clean_way, rcontext_str(): week_way}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(week_way)
    sue_bud.conceptroot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_concept_reason_premiseunit():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    thur_way = sue_bud.make_way(week_way, "thur")
    x_dimen = bud_concept_reason_premiseunit_str()
    root_jkeys = {
        concept_way_str(): root_way,
        rcontext_str(): week_way,
        pstate_str(): thur_way,
    }
    casa_jkeys = {
        concept_way_str(): casa_way,
        rcontext_str(): week_way,
        pstate_str(): thur_way,
    }
    clean_jkeys = {
        concept_way_str(): clean_way,
        rcontext_str(): week_way,
        pstate_str(): thur_way,
    }

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(week_way)
    sue_bud.conceptroot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(thur_way)
    sue_bud.conceptroot.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_concept_laborlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    swim_str = "Swim"
    x_dimen = bud_concept_laborlink_str()
    root_jkeys = {concept_way_str(): root_way, labor_title_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, labor_title_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, labor_title_str(): swim_str}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.conceptroot.laborunit.set_laborlink(swim_str)

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_concept_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    swim_str = "Swim"
    x_dimen = bud_concept_healerlink_str()
    root_jkeys = {concept_way_str(): root_way, healer_name_str(): swim_str}
    casa_jkeys = {concept_way_str(): casa_way, healer_name_str(): swim_str}
    clean_jkeys = {concept_way_str(): clean_way, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.conceptroot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_concept_factunit():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_label)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    x_dimen = bud_concept_factunit_str()
    root_jkeys = {concept_way_str(): root_way, fcontext_str(): week_way}
    casa_jkeys = {concept_way_str(): casa_way, fcontext_str(): week_way}
    clean_jkeys = {concept_way_str(): clean_way, fcontext_str(): week_way}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_concept(week_way)
    sue_bud.conceptroot.set_factunit(factunit_shop(week_way))

    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
