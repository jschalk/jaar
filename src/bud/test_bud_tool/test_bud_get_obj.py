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
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str as premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
)


def test_bud_acctunit_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_str}
    sue_bud.add_acctunit(yao_str)

    # WHEN
    x_obj = bud_acctunit_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str)


def test_bud_acct_membership_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_str, "group_id": swim_str}
    sue_bud.add_acctunit(yao_str)
    sue_bud.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = bud_acct_membership_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str).get_membership(swim_str)


def test_bud_ideaunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
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
    casa_str = "casa"
    swim_str = "swim"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "group_id": swim_str}
    sue_bud.add_idea(casa_road)
    sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = bud_idea_awardlink_get_obj(sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).get_awardlink(swim_str)


def test_bud_idea_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
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
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)
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
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
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


def test_bud_get_obj_ReturnsObj_BudUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_str}
    sue_bud.add_acctunit(yao_str)

    # WHEN
    x_obj = bud_get_obj(budunit_str(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud


def test_bud_get_obj_ReturnsObj_bud_acctunit_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_str}
    sue_bud.add_acctunit(yao_str)

    # WHEN
    x_obj = bud_get_obj(bud_acctunit_str(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str)


def test_bud_get_obj_ReturnsObj_bud_acct_membership_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_bud = budunit_shop("Sue")
    required_args = {"acct_id": yao_str, "group_id": swim_str}
    sue_bud.add_acctunit(yao_str)
    sue_bud.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = bud_get_obj(bud_acct_membership_str(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str).get_membership(swim_str)


def test_bud_get_obj_ReturnsObj_bud_ideaunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road}

    # WHEN
    x_obj = bud_get_obj(bud_ideaunit_str(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road)


def test_bud_get_obj_ReturnsObj_bud_idea_awardlink_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "group_id": swim_str}
    sue_bud.add_idea(casa_road)
    sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = bud_get_obj(bud_idea_awardlink_str(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).get_awardlink(swim_str)


def test_bud_get_obj_ReturnsObj_bud_idea_reasonunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "base": week_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.get_idea_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    # WHEN
    x_obj = bud_get_obj(bud_idea_reasonunit_str(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).get_reasonunit(week_road)


def test_bud_get_obj_ReturnsObj_bud_idea_reason_premiseunit_get_obj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)
    thur_road = sue_bud.make_road(week_road, "thur")
    casa_required_args = {"road": casa_road, "base": week_road, "need": thur_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.add_idea(thur_road)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    casa_idea.set_reasonunit(reasonunit_shop(week_road))
    casa_idea.get_reasonunit(week_road).set_premise(thur_road)

    # WHEN
    x_obj = bud_get_obj(premiseunit_str(), sue_bud, casa_required_args)
    # THEN
    assert x_obj
    assert x_obj == casa_idea.get_reasonunit(week_road).get_premise(thur_road)


def test_bud_get_obj_ReturnsObj_bud_idea_factunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_idea(casa_road)
    required_args = {"road": casa_road, "base": week_road}
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(week_road)
    sue_bud.get_idea_obj(casa_road).set_factunit(factunit_shop(week_road))

    # WHEN
    x_obj = bud_get_obj(bud_idea_factunit_str(), sue_bud, required_args)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_idea_obj(casa_road).factunits.get(week_road)
