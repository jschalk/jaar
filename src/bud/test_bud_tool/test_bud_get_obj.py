from src.bud.group import awardlink_shop
from src.bud.reason_idea import reasonunit_shop, factunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_tool import (
    bud_acctunit_get_obj,
    bud_acct_membership_get_obj,
    bud_ideaunit_get_obj,
    bud_idea_awardlink_get_obj,
    bud_idea_reasonunit_get_obj,
    bud_idea_reason_premiseunit_get_obj as premiseunit_get_obj,
    bud_idea_factunit_get_obj,
    bud_get_obj,
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text as premiseunit_text,
    bud_idea_teamlink_text,
    bud_idea_healerlink_text,
    bud_idea_factunit_text,
    bud_attr_different,
)


def test_bud_acctunit_get_obj_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_text}
    sue_bud.add_acctunit(yao_text)

    # WHEN
    x_obj = bud_acctunit_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_text)


def test_bud_acct_membership_get_obj_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    swim_text = ";swim"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_text, "group_id": swim_text}
    sue_bud.add_acctunit(yao_text)
    sue_bud.get_acct(yao_text).add_membership(swim_text)

    # WHEN
    x_obj = bud_acct_membership_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_text).get_membership(swim_text)


def test_bud_ideaunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road}

    # WHEN
    x_obj = bud_ideaunit_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road)


def test_bud_idea_awardlink_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    swim_text = "swim"
    casa_road = sue_bud.make_l1_road(casa_text)
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "group_id": swim_text}
    sue_bud.add_idea(casa_road)
    sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(swim_text))

    # WHEN
    x_obj = bud_idea_awardlink_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).get_awardlink(swim_text)


def test_bud_idea_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "base": week_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.get_idea_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    # WHEN
    x_obj = bud_idea_reasonunit_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).get_reasonunit(week_road)


def test_bud_idea_reason_premiseunit_get_obj_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    thur_road = sue_bud.make_road(week_road, "thur")
    casa_required_args = {"road": casa_road, "base": week_road, "need": thur_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.add_idea(thur_road)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    casa_idea.set_reasonunit(reasonunit_shop(week_road))
    casa_idea.get_reasonunit(week_road).set_premise(thur_road)

    # WHEN
    x_obj = premiseunit_get_obj(sue_bud, casa_required_args)
    # THEN
    assert x_obj
    assert x_obj == casa_idea.get_reasonunit(week_road).get_premise(thur_road)


def test_bud_idea_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "base": week_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.get_idea_obj(casa_road).set_factunit(factunit_shop(week_road))

    # WHEN
    x_obj = bud_idea_factunit_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).factunits.get(week_road)


def test_bud_get_obj_ReturnsObj_bud_acctunit_get_obj():
    # ESTABLISH
    yao_text = "Yao"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_text}
    sue_bud.add_acctunit(yao_text)

    # WHEN
    x_obj = bud_get_obj(bud_acctunit_text(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_text)


def test_bud_get_obj_ReturnsObj_bud_acct_membership_get_obj():
    # ESTABLISH
    yao_text = "Yao"
    swim_text = ";swim"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_text, "group_id": swim_text}
    sue_bud.add_acctunit(yao_text)
    sue_bud.get_acct(yao_text).add_membership(swim_text)

    # WHEN
    x_obj = bud_get_obj(bud_acct_membership_text(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_text).get_membership(swim_text)


def test_bud_get_obj_ReturnsObj_bud_ideaunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road}

    # WHEN
    x_obj = bud_get_obj(bud_ideaunit_text(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road)


def test_bud_get_obj_ReturnsObj_bud_idea_awardlink_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    swim_text = "swim"
    casa_road = sue_bud.make_l1_road(casa_text)
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "group_id": swim_text}
    sue_bud.add_idea(casa_road)
    sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(swim_text))

    # WHEN
    x_obj = bud_get_obj(bud_idea_awardlink_text(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).get_awardlink(swim_text)


def test_bud_get_obj_ReturnsObj_bud_idea_reasonunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "base": week_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.get_idea_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    # WHEN
    x_obj = bud_get_obj(bud_idea_reasonunit_text(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).get_reasonunit(week_road)


def test_bud_get_obj_ReturnsObj_bud_idea_reason_premiseunit_get_obj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    thur_road = sue_bud.make_road(week_road, "thur")
    casa_required_args = {"road": casa_road, "base": week_road, "need": thur_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.add_idea(thur_road)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    casa_idea.set_reasonunit(reasonunit_shop(week_road))
    casa_idea.get_reasonunit(week_road).set_premise(thur_road)

    # WHEN
    x_obj = bud_get_obj(premiseunit_text(), sue_bud, casa_required_args)
    # THEN
    assert x_obj
    assert x_obj == casa_idea.get_reasonunit(week_road).get_premise(thur_road)


def test_bud_get_obj_ReturnsObj_bud_idea_factunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "base": week_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.get_idea_obj(casa_road).set_factunit(factunit_shop(week_road))

    # WHEN
    x_obj = bud_get_obj(bud_idea_factunit_text(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).factunits.get(week_road)
