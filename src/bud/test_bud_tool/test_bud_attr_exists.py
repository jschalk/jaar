from src.bud.group import awardlink_shop
from src.bud.reason_idea import factunit_shop, reasonunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_tool import (
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
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_teamlink_text,
    bud_idea_healerlink_text,
    bud_idea_factunit_text,
    bud_attr_exists,
)


def test_budunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not budunit_exists(None)
    assert budunit_exists(budunit_shop("Sue"))


def test_bud_acctunit_exists_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_text}

    # WHEN / THEN
    assert not bud_acctunit_exists(None, {})
    assert not bud_acctunit_exists(sue_bud, required_args)

    # WHEN
    sue_bud.add_acctunit(yao_text)

    #  THEN
    assert bud_acctunit_exists(sue_bud, required_args)


def test_bud_acct_membership_exists_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    swim_text = ";swim"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_text, "group_id": swim_text}

    # WHEN / THEN
    assert not bud_acct_membership_exists(None, {})
    assert not bud_acct_membership_exists(sue_bud, required_args)

    # WHEN
    sue_bud.add_acctunit(yao_text)
    # THEN
    assert not bud_acct_membership_exists(sue_bud, required_args)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(";run")
    # THEN
    assert not bud_acct_membership_exists(sue_bud, required_args)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(swim_text)
    # THEN
    assert bud_acct_membership_exists(sue_bud, required_args)


def test_bud_ideaunit_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    sweep_road = sue_bud.make_road(clean_road, "sweep")
    root_road = sue_bud._real_id
    root_required_args = {"road": root_road}
    casa_required_args = {"road": casa_road}
    clean_required_args = {"road": clean_road}
    sweep_required_args = {"road": sweep_road}

    # WHEN / THEN
    assert not bud_ideaunit_exists(None, {})
    assert not bud_ideaunit_exists(sue_bud, {})
    assert bud_ideaunit_exists(sue_bud, root_required_args)
    assert not bud_ideaunit_exists(sue_bud, casa_required_args)
    assert not bud_ideaunit_exists(sue_bud, clean_required_args)
    assert not bud_ideaunit_exists(sue_bud, sweep_required_args)

    # WHEN
    sue_bud.add_idea(casa_road)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, {})
    assert bud_ideaunit_exists(sue_bud, root_required_args)
    assert bud_ideaunit_exists(sue_bud, casa_required_args)
    assert not bud_ideaunit_exists(sue_bud, clean_required_args)
    assert not bud_ideaunit_exists(sue_bud, sweep_required_args)

    # WHEN
    sue_bud.add_idea(clean_road)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, {})
    assert bud_ideaunit_exists(sue_bud, root_required_args)
    assert bud_ideaunit_exists(sue_bud, casa_required_args)
    assert bud_ideaunit_exists(sue_bud, clean_required_args)
    assert not bud_ideaunit_exists(sue_bud, sweep_required_args)


def test_bud_idea_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"
    root_road = sue_bud._real_id
    root_required_args = {"road": root_road, "group_id": swim_text}
    casa_required_args = {"road": casa_road, "group_id": swim_text}
    clean_required_args = {"road": clean_road, "group_id": swim_text}

    # WHEN / THEN
    assert not bud_idea_awardlink_exists(None, {})
    assert not bud_idea_awardlink_exists(sue_bud, {})
    assert not bud_idea_awardlink_exists(sue_bud, root_required_args)
    assert not bud_idea_awardlink_exists(sue_bud, casa_required_args)
    assert not bud_idea_awardlink_exists(sue_bud, clean_required_args)

    # WHEN
    sue_bud._idearoot.set_awardlink(awardlink_shop(swim_text))

    # THEN
    assert not bud_idea_awardlink_exists(sue_bud, {})
    assert bud_idea_awardlink_exists(sue_bud, root_required_args)
    assert not bud_idea_awardlink_exists(sue_bud, casa_required_args)
    assert not bud_idea_awardlink_exists(sue_bud, clean_required_args)


def test_bud_idea_reasonunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    root_required_args = {"road": root_road, "base": week_road}
    casa_required_args = {"road": casa_road, "base": week_road}
    clean_required_args = {"road": clean_road, "base": week_road}

    # WHEN / THEN
    assert not bud_idea_reasonunit_exists(None, {})
    assert not bud_idea_reasonunit_exists(sue_bud, {})
    assert not bud_idea_reasonunit_exists(sue_bud, root_required_args)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_required_args)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not bud_idea_reasonunit_exists(sue_bud, {})
    assert bud_idea_reasonunit_exists(sue_bud, root_required_args)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_required_args)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_required_args)


def test_bud_idea_reason_premiseunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    thur_road = sue_bud.make_road(week_road, "thur")
    root_required_args = {"road": root_road, "base": week_road, "need": thur_road}
    casa_required_args = {"road": casa_road, "base": week_road, "need": thur_road}
    clean_required_args = {"road": clean_road, "base": week_road, "need": thur_road}

    # WHEN / THEN
    assert not premiseunit_exists(None, {})
    assert not premiseunit_exists(sue_bud, {})
    assert not premiseunit_exists(sue_bud, root_required_args)
    assert not premiseunit_exists(sue_bud, casa_required_args)
    assert not premiseunit_exists(sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not premiseunit_exists(sue_bud, {})
    assert not premiseunit_exists(sue_bud, root_required_args)
    assert not premiseunit_exists(sue_bud, casa_required_args)
    assert not premiseunit_exists(sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(thur_road)
    sue_bud._idearoot.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert not premiseunit_exists(sue_bud, {})
    assert premiseunit_exists(sue_bud, root_required_args)
    assert not premiseunit_exists(sue_bud, casa_required_args)
    assert not premiseunit_exists(sue_bud, clean_required_args)


def test_bud_idea_teamlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"
    root_required_args = {"road": root_road, "group_id": swim_text}
    casa_required_args = {"road": casa_road, "group_id": swim_text}
    clean_required_args = {"road": clean_road, "group_id": swim_text}

    # WHEN / THEN
    assert not bud_idea_teamlink_exists(None, {})
    assert not bud_idea_teamlink_exists(sue_bud, {})
    assert not bud_idea_teamlink_exists(sue_bud, root_required_args)
    assert not bud_idea_teamlink_exists(sue_bud, casa_required_args)
    assert not bud_idea_teamlink_exists(sue_bud, clean_required_args)

    # WHEN
    sue_bud._idearoot._teamunit.set_teamlink(swim_text)

    # THEN
    assert not bud_idea_teamlink_exists(sue_bud, {})
    assert bud_idea_teamlink_exists(sue_bud, root_required_args)
    assert not bud_idea_teamlink_exists(sue_bud, casa_required_args)
    assert not bud_idea_teamlink_exists(sue_bud, clean_required_args)


def test_bud_idea_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"
    root_required_args = {"road": root_road, "healer_id": swim_text}
    casa_required_args = {"road": casa_road, "healer_id": swim_text}
    clean_required_args = {"road": clean_road, "healer_id": swim_text}

    # WHEN / THEN
    assert not bud_idea_healerlink_exists(None, {})
    assert not bud_idea_healerlink_exists(sue_bud, {})
    assert not bud_idea_healerlink_exists(sue_bud, root_required_args)
    assert not bud_idea_healerlink_exists(sue_bud, casa_required_args)
    assert not bud_idea_healerlink_exists(sue_bud, clean_required_args)

    # WHEN
    sue_bud._idearoot._healerlink.set_healer_id(swim_text)

    # THEN
    assert not bud_idea_healerlink_exists(sue_bud, {})
    assert bud_idea_healerlink_exists(sue_bud, root_required_args)
    assert not bud_idea_healerlink_exists(sue_bud, casa_required_args)
    assert not bud_idea_healerlink_exists(sue_bud, clean_required_args)


def test_bud_idea_factunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    root_required_args = {"road": root_road, "base": week_road}
    casa_required_args = {"road": casa_road, "base": week_road}
    clean_required_args = {"road": clean_road, "base": week_road}

    # WHEN / THEN
    assert not bud_idea_factunit_exists(None, {})
    assert not bud_idea_factunit_exists(sue_bud, {})
    assert not bud_idea_factunit_exists(sue_bud, root_required_args)
    assert not bud_idea_factunit_exists(sue_bud, casa_required_args)
    assert not bud_idea_factunit_exists(sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_factunit(factunit_shop(week_road))

    # THEN
    assert not bud_idea_factunit_exists(sue_bud, {})
    assert bud_idea_factunit_exists(sue_bud, root_required_args)
    assert not bud_idea_factunit_exists(sue_bud, casa_required_args)
    assert not bud_idea_factunit_exists(sue_bud, clean_required_args)


def test_bud_attr_exists_ReturnsObj_budunit():
    # ESTABLISH / WHEN / THEN
    assert not bud_attr_exists(budunit_text(), None, {})
    assert bud_attr_exists(budunit_text(), budunit_shop("Sue"), {})


def test_bud_attr_exists_ReturnsObj_bud_acctunit():
    # ESTABLISH
    yao_text = "Yao"
    sue_bud = budunit_shop("Sue")
    x_required_args = {"acct_id": yao_text}

    # WHEN / THEN
    assert not bud_attr_exists(bud_acctunit_text(), None, {})
    assert not bud_attr_exists(bud_acctunit_text(), sue_bud, x_required_args)

    # WHEN
    sue_bud.add_acctunit(yao_text)

    #  THEN
    assert bud_attr_exists(bud_acctunit_text(), sue_bud, x_required_args)


def test_bud_attr_exists_ReturnsObj_bud_acct_membership():
    # ESTABLISH
    yao_text = "Yao"
    swim_text = ";swim"
    sue_bud = budunit_shop("Sue")
    x_required_args = {"acct_id": yao_text, "group_id": swim_text}
    x_category = bud_acct_membership_text()

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, x_required_args)

    # WHEN
    sue_bud.add_acctunit(yao_text)
    # THEN
    assert not bud_attr_exists(x_category, sue_bud, x_required_args)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(";run")
    # THEN
    assert not bud_attr_exists(x_category, sue_bud, x_required_args)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(swim_text)
    # THEN
    assert bud_attr_exists(x_category, sue_bud, x_required_args)


def test_bud_attr_exists_ReturnsObj_bud_ideaunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    sweep_road = sue_bud.make_road(clean_road, "sweep")
    x_parent_road = sue_bud._real_id
    root_required_args = {"road": x_parent_road}
    casa_required_args = {"road": casa_road}
    clean_required_args = {"road": clean_road}
    sweep_required_args = {"road": sweep_road}
    x_category = bud_ideaunit_text()

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)
    assert not bud_attr_exists(x_category, sue_bud, sweep_required_args)

    # WHEN
    sue_bud.add_idea(casa_road)
    # THEN
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)
    assert not bud_attr_exists(x_category, sue_bud, sweep_required_args)

    # WHEN
    sue_bud.add_idea(clean_road)
    # THEN
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert bud_attr_exists(x_category, sue_bud, clean_required_args)
    assert not bud_attr_exists(x_category, sue_bud, sweep_required_args)


def test_bud_attr_exists_ReturnsObj_bud_idea_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"
    x_category = bud_idea_awardlink_text()
    root_required_args = {"road": root_road, "group_id": swim_text}
    casa_required_args = {"road": casa_road, "group_id": swim_text}
    clean_required_args = {"road": clean_road, "group_id": swim_text}

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert not bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)

    # WHEN
    sue_bud._idearoot.set_awardlink(awardlink_shop(swim_text))

    # THEN
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)


def test_bud_attr_exists_ReturnsObj_bud_idea_reasonunit():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    x_category = bud_idea_reasonunit_text()
    root_required_args = {"road": root_road, "base": week_road}
    casa_required_args = {"road": casa_road, "base": week_road}
    clean_required_args = {"road": clean_road, "base": week_road}

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert not bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)


def test_bud_attr_exists_ReturnsObj_bud_idea_reason_premiseunit():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    thur_road = sue_bud.make_road(week_road, "thur")
    x_category = bud_idea_reason_premiseunit_text()
    root_required_args = {"road": root_road, "base": week_road, "need": thur_road}
    casa_required_args = {"road": casa_road, "base": week_road, "need": thur_road}
    clean_required_args = {"road": clean_road, "base": week_road, "need": thur_road}

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert not bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(thur_road)
    sue_bud._idearoot.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)


def test_bud_attr_exists_ReturnsObj_bud_idea_teamlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"
    x_category = bud_idea_teamlink_text()
    root_required_args = {"road": root_road, "group_id": swim_text}
    casa_required_args = {"road": casa_road, "group_id": swim_text}
    clean_required_args = {"road": clean_road, "group_id": swim_text}

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert not bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)

    # WHEN
    sue_bud._idearoot._teamunit.set_teamlink(swim_text)

    # THEN
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)


def test_bud_attr_exists_ReturnsObj_bud_idea_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"
    x_category = bud_idea_healerlink_text()
    root_required_args = {"road": root_road, "healer_id": swim_text}
    casa_required_args = {"road": casa_road, "healer_id": swim_text}
    clean_required_args = {"road": clean_road, "healer_id": swim_text}

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert not bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)

    # WHEN
    sue_bud._idearoot._healerlink.set_healer_id(swim_text)

    # THEN
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)


def test_bud_attr_exists_ReturnsObj_bud_idea_factunit():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    x_category = bud_idea_factunit_text()
    root_required_args = {"road": root_road, "base": week_road}
    casa_required_args = {"road": casa_road, "base": week_road}
    clean_required_args = {"road": clean_road, "base": week_road}

    # WHEN / THEN
    assert not bud_attr_exists(x_category, None, {})
    assert not bud_attr_exists(x_category, sue_bud, {})
    assert not bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_factunit(factunit_shop(week_road))

    # THEN
    assert bud_attr_exists(x_category, sue_bud, root_required_args)
    assert not bud_attr_exists(x_category, sue_bud, casa_required_args)
    assert not bud_attr_exists(x_category, sue_bud, clean_required_args)
