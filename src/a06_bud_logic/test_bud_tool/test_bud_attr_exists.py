from src.a01_way_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_idea import factunit_shop, reasonunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_tool import (
    budunit_exists,
    bud_acctunit_exists,
    bud_acct_membership_exists,
    bud_ideaunit_exists,
    bud_idea_awardlink_exists,
    bud_idea_reasonunit_exists,
    bud_idea_reason_premiseunit_exists as premiseunit_exists,
    bud_idea_teamlink_exists,
    bud_idea_healerlink_exists,
    bud_idea_factunit_exists,
    bud_attr_exists,
)
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
    acct_name_str,
    awardee_label_str,
    context_str,
    fcontext_str,
    group_label_str,
    rbranch_str,
    idea_way_str,
    team_label_str,
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
    jkeys = {acct_name_str(): yao_str, group_label_str(): swim_str}

    # WHEN / THEN
    assert not bud_acct_membership_exists(None, {})
    assert not bud_acct_membership_exists(sue_bud, jkeys)

    # WHEN
    sue_bud.add_acctunit(yao_str)
    # THEN
    assert not bud_acct_membership_exists(sue_bud, jkeys)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_str)
    yao_idea.add_membership(";run")
    # THEN
    assert not bud_acct_membership_exists(sue_bud, jkeys)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_str)
    yao_idea.add_membership(swim_str)
    # THEN
    assert bud_acct_membership_exists(sue_bud, jkeys)


def test_bud_ideaunit_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_way = sue_bud.make_way(clean_way, "sweep")
    root_way = to_way(sue_bud.fisc_tag)
    root_jkeys = {idea_way_str(): root_way}
    casa_jkeys = {idea_way_str(): casa_way}
    clean_jkeys = {idea_way_str(): clean_way}
    sweep_jkeys = {idea_way_str(): sweep_way}

    # WHEN / THEN
    assert not bud_ideaunit_exists(None, {})
    assert not bud_ideaunit_exists(sue_bud, {})
    assert bud_ideaunit_exists(sue_bud, root_jkeys)
    assert not bud_ideaunit_exists(sue_bud, casa_jkeys)
    assert not bud_ideaunit_exists(sue_bud, clean_jkeys)
    assert not bud_ideaunit_exists(sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_idea(casa_way)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, {})
    assert bud_ideaunit_exists(sue_bud, root_jkeys)
    assert bud_ideaunit_exists(sue_bud, casa_jkeys)
    assert not bud_ideaunit_exists(sue_bud, clean_jkeys)
    assert not bud_ideaunit_exists(sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_idea(clean_way)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, {})
    assert bud_ideaunit_exists(sue_bud, root_jkeys)
    assert bud_ideaunit_exists(sue_bud, casa_jkeys)
    assert bud_ideaunit_exists(sue_bud, clean_jkeys)
    assert not bud_ideaunit_exists(sue_bud, sweep_jkeys)


def test_bud_idea_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    swim_str = "Swim"
    root_way = to_way(sue_bud.fisc_tag)
    root_jkeys = {idea_way_str(): root_way, awardee_label_str(): swim_str}
    casa_jkeys = {idea_way_str(): casa_way, awardee_label_str(): swim_str}
    clean_jkeys = {idea_way_str(): clean_way, awardee_label_str(): swim_str}

    # WHEN / THEN
    assert not bud_idea_awardlink_exists(None, {})
    assert not bud_idea_awardlink_exists(sue_bud, {})
    assert not bud_idea_awardlink_exists(sue_bud, root_jkeys)
    assert not bud_idea_awardlink_exists(sue_bud, casa_jkeys)
    assert not bud_idea_awardlink_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.idearoot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not bud_idea_awardlink_exists(sue_bud, {})
    assert bud_idea_awardlink_exists(sue_bud, root_jkeys)
    assert not bud_idea_awardlink_exists(sue_bud, casa_jkeys)
    assert not bud_idea_awardlink_exists(sue_bud, clean_jkeys)


def test_bud_idea_reasonunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    root_jkeys = {idea_way_str(): root_way, context_str(): week_way}
    casa_jkeys = {idea_way_str(): casa_way, context_str(): week_way}
    clean_jkeys = {idea_way_str(): clean_way, context_str(): week_way}

    # WHEN / THEN
    assert not bud_idea_reasonunit_exists(None, {})
    assert not bud_idea_reasonunit_exists(sue_bud, {})
    assert not bud_idea_reasonunit_exists(sue_bud, root_jkeys)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_jkeys)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(week_way)
    sue_bud.idearoot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not bud_idea_reasonunit_exists(sue_bud, {})
    assert bud_idea_reasonunit_exists(sue_bud, root_jkeys)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_jkeys)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_jkeys)


def test_bud_idea_reason_premiseunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    thur_way = sue_bud.make_way(week_way, "thur")
    root_jkeys = {
        idea_way_str(): root_way,
        context_str(): week_way,
        rbranch_str(): thur_way,
    }
    casa_jkeys = {
        idea_way_str(): casa_way,
        context_str(): week_way,
        rbranch_str(): thur_way,
    }
    clean_jkeys = {
        idea_way_str(): clean_way,
        context_str(): week_way,
        rbranch_str(): thur_way,
    }

    # WHEN / THEN
    assert not premiseunit_exists(None, {})
    assert not premiseunit_exists(sue_bud, {})
    assert not premiseunit_exists(sue_bud, root_jkeys)
    assert not premiseunit_exists(sue_bud, casa_jkeys)
    assert not premiseunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(week_way)
    sue_bud.idearoot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not premiseunit_exists(sue_bud, {})
    assert not premiseunit_exists(sue_bud, root_jkeys)
    assert not premiseunit_exists(sue_bud, casa_jkeys)
    assert not premiseunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(thur_way)
    sue_bud.idearoot.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert not premiseunit_exists(sue_bud, {})
    assert premiseunit_exists(sue_bud, root_jkeys)
    assert not premiseunit_exists(sue_bud, casa_jkeys)
    assert not premiseunit_exists(sue_bud, clean_jkeys)


def test_bud_idea_teamlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    swim_str = "Swim"
    root_jkeys = {idea_way_str(): root_way, team_label_str(): swim_str}
    casa_jkeys = {idea_way_str(): casa_way, team_label_str(): swim_str}
    clean_jkeys = {idea_way_str(): clean_way, team_label_str(): swim_str}

    # WHEN / THEN
    assert not bud_idea_teamlink_exists(None, {})
    assert not bud_idea_teamlink_exists(sue_bud, {})
    assert not bud_idea_teamlink_exists(sue_bud, root_jkeys)
    assert not bud_idea_teamlink_exists(sue_bud, casa_jkeys)
    assert not bud_idea_teamlink_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.idearoot.teamunit.set_teamlink(swim_str)

    # THEN
    assert not bud_idea_teamlink_exists(sue_bud, {})
    assert bud_idea_teamlink_exists(sue_bud, root_jkeys)
    assert not bud_idea_teamlink_exists(sue_bud, casa_jkeys)
    assert not bud_idea_teamlink_exists(sue_bud, clean_jkeys)


def test_bud_idea_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    swim_str = "Swim"
    root_jkeys = {idea_way_str(): root_way, healer_name_str(): swim_str}
    casa_jkeys = {idea_way_str(): casa_way, healer_name_str(): swim_str}
    clean_jkeys = {idea_way_str(): clean_way, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not bud_idea_healerlink_exists(None, {})
    assert not bud_idea_healerlink_exists(sue_bud, {})
    assert not bud_idea_healerlink_exists(sue_bud, root_jkeys)
    assert not bud_idea_healerlink_exists(sue_bud, casa_jkeys)
    assert not bud_idea_healerlink_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.idearoot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not bud_idea_healerlink_exists(sue_bud, {})
    assert bud_idea_healerlink_exists(sue_bud, root_jkeys)
    assert not bud_idea_healerlink_exists(sue_bud, casa_jkeys)
    assert not bud_idea_healerlink_exists(sue_bud, clean_jkeys)


def test_bud_idea_factunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    root_jkeys = {idea_way_str(): root_way, fcontext_str(): week_way}
    casa_jkeys = {idea_way_str(): casa_way, fcontext_str(): week_way}
    clean_jkeys = {idea_way_str(): clean_way, fcontext_str(): week_way}

    # WHEN / THEN
    assert not bud_idea_factunit_exists(None, {})
    assert not bud_idea_factunit_exists(sue_bud, {})
    assert not bud_idea_factunit_exists(sue_bud, root_jkeys)
    assert not bud_idea_factunit_exists(sue_bud, casa_jkeys)
    assert not bud_idea_factunit_exists(sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(week_way)
    sue_bud.idearoot.set_factunit(factunit_shop(week_way))

    # THEN
    assert not bud_idea_factunit_exists(sue_bud, {})
    assert bud_idea_factunit_exists(sue_bud, root_jkeys)
    assert not bud_idea_factunit_exists(sue_bud, casa_jkeys)
    assert not bud_idea_factunit_exists(sue_bud, clean_jkeys)


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
    x_jkeys = {acct_name_str(): yao_str, group_label_str(): swim_str}
    x_dimen = bud_acct_membership_str()

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, x_jkeys)

    # WHEN
    sue_bud.add_acctunit(yao_str)
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, x_jkeys)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_str)
    yao_idea.add_membership(";run")
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, x_jkeys)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_str)
    yao_idea.add_membership(swim_str)
    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, x_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_ideaunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_way = sue_bud.make_way(clean_way, "sweep")
    x_parent_way = to_way(sue_bud.fisc_tag)
    root_jkeys = {idea_way_str(): x_parent_way}
    casa_jkeys = {idea_way_str(): casa_way}
    clean_jkeys = {idea_way_str(): clean_way}
    sweep_jkeys = {idea_way_str(): sweep_way}
    x_dimen = bud_ideaunit_str()

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_idea(casa_way)
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, sweep_jkeys)

    # WHEN
    sue_bud.add_idea(clean_way)
    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, sweep_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_idea_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    swim_str = "Swim"
    x_dimen = bud_idea_awardlink_str()
    root_jkeys = {idea_way_str(): root_way, awardee_label_str(): swim_str}
    casa_jkeys = {idea_way_str(): casa_way, awardee_label_str(): swim_str}
    clean_jkeys = {idea_way_str(): clean_way, awardee_label_str(): swim_str}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.idearoot.set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_idea_reasonunit():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    x_dimen = bud_idea_reasonunit_str()
    root_jkeys = {idea_way_str(): root_way, context_str(): week_way}
    casa_jkeys = {idea_way_str(): casa_way, context_str(): week_way}
    clean_jkeys = {idea_way_str(): clean_way, context_str(): week_way}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(week_way)
    sue_bud.idearoot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_idea_reason_premiseunit():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    thur_way = sue_bud.make_way(week_way, "thur")
    x_dimen = bud_idea_reason_premiseunit_str()
    root_jkeys = {
        idea_way_str(): root_way,
        context_str(): week_way,
        rbranch_str(): thur_way,
    }
    casa_jkeys = {
        idea_way_str(): casa_way,
        context_str(): week_way,
        rbranch_str(): thur_way,
    }
    clean_jkeys = {
        idea_way_str(): clean_way,
        context_str(): week_way,
        rbranch_str(): thur_way,
    }

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(week_way)
    sue_bud.idearoot.set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(thur_way)
    sue_bud.idearoot.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_idea_teamlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    swim_str = "Swim"
    x_dimen = bud_idea_teamlink_str()
    root_jkeys = {idea_way_str(): root_way, team_label_str(): swim_str}
    casa_jkeys = {idea_way_str(): casa_way, team_label_str(): swim_str}
    clean_jkeys = {idea_way_str(): clean_way, team_label_str(): swim_str}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.idearoot.teamunit.set_teamlink(swim_str)

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_idea_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    swim_str = "Swim"
    x_dimen = bud_idea_healerlink_str()
    root_jkeys = {idea_way_str(): root_way, healer_name_str(): swim_str}
    casa_jkeys = {idea_way_str(): casa_way, healer_name_str(): swim_str}
    clean_jkeys = {idea_way_str(): clean_way, healer_name_str(): swim_str}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.idearoot.healerlink.set_healer_name(swim_str)

    # THEN
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)


def test_bud_attr_exists_ReturnsObj_bud_idea_factunit():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    root_way = to_way(sue_bud.fisc_tag)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    x_dimen = bud_idea_factunit_str()
    root_jkeys = {idea_way_str(): root_way, fcontext_str(): week_way}
    casa_jkeys = {idea_way_str(): casa_way, fcontext_str(): week_way}
    clean_jkeys = {idea_way_str(): clean_way, fcontext_str(): week_way}

    # WHEN / THEN
    assert not bud_attr_exists(x_dimen, None, {})
    assert not bud_attr_exists(x_dimen, sue_bud, {})
    assert not bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)

    # WHEN
    sue_bud.add_idea(week_way)
    sue_bud.idearoot.set_factunit(factunit_shop(week_way))

    # THEN
    assert bud_attr_exists(x_dimen, sue_bud, root_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, casa_jkeys)
    assert not bud_attr_exists(x_dimen, sue_bud, clean_jkeys)
