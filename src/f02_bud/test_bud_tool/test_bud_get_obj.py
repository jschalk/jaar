from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_item import reasonunit_shop, factunit_shop
from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import (
    bud_acctunit_get_obj,
    bud_acct_membership_get_obj,
    bud_itemunit_get_obj,
    bud_item_awardlink_get_obj,
    bud_item_reasonunit_get_obj,
    bud_item_reason_premiseunit_get_obj as premiseunit_get_obj,
    bud_item_factunit_get_obj,
    bud_get_obj,
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str as premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
)


def test_bud_acctunit_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_bud.add_acctunit(yao_str)

    # WHEN
    x_obj = bud_acctunit_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str)


def test_bud_acct_membership_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_bud = budunit_shop("Sue")
    jkeys = {"acct_name": yao_str, "group_label": swim_str}
    sue_bud.add_acctunit(yao_str)
    sue_bud.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = bud_acct_membership_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str).get_membership(swim_str)


def test_bud_itemunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road}

    # WHEN
    x_obj = bud_itemunit_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road)


def test_bud_item_awardlink_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road, "awardee_tag": swim_str}
    sue_bud.add_item(casa_road)
    sue_bud.get_item_obj(casa_road).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = bud_item_awardlink_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road).get_awardlink(swim_str)


def test_bud_item_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road, "base": week_road}
    sue_bud.add_item(casa_road)
    sue_bud.add_item(week_road)
    sue_bud.get_item_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    # WHEN
    x_obj = bud_item_reasonunit_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road).get_reasonunit(week_road)


def test_bud_item_reason_premiseunit_get_obj_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)
    thur_road = sue_bud.make_road(week_road, "thur")
    casa_jkeys = {"road": casa_road, "base": week_road, "need": thur_road}
    sue_bud.add_item(casa_road)
    sue_bud.add_item(week_road)
    sue_bud.add_item(thur_road)
    casa_item = sue_bud.get_item_obj(casa_road)
    casa_item.set_reasonunit(reasonunit_shop(week_road))
    casa_item.get_reasonunit(week_road).set_premise(thur_road)

    # WHEN
    x_obj = premiseunit_get_obj(sue_bud, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_item.get_reasonunit(week_road).get_premise(thur_road)


def test_bud_item_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road, "base": week_road}
    sue_bud.add_item(casa_road)
    sue_bud.add_item(week_road)
    sue_bud.get_item_obj(casa_road).set_factunit(factunit_shop(week_road))

    # WHEN
    x_obj = bud_item_factunit_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road).factunits.get(week_road)


def test_bud_get_obj_ReturnsObj_BudUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_bud.add_acctunit(yao_str)

    # WHEN
    x_obj = bud_get_obj(budunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud


def test_bud_get_obj_ReturnsObj_bud_acctunit_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_bud.add_acctunit(yao_str)

    # WHEN
    x_obj = bud_get_obj(bud_acctunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str)


def test_bud_get_obj_ReturnsObj_bud_acct_membership_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_bud = budunit_shop("Sue")
    jkeys = {"acct_name": yao_str, "group_label": swim_str}
    sue_bud.add_acctunit(yao_str)
    sue_bud.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = bud_get_obj(bud_acct_membership_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_acct(yao_str).get_membership(swim_str)


def test_bud_get_obj_ReturnsObj_bud_itemunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road}

    # WHEN
    x_obj = bud_get_obj(bud_itemunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road)


def test_bud_get_obj_ReturnsObj_bud_item_awardlink_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road, "awardee_tag": swim_str}
    sue_bud.add_item(casa_road)
    sue_bud.get_item_obj(casa_road).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = bud_get_obj(bud_item_awardlink_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road).get_awardlink(swim_str)


def test_bud_get_obj_ReturnsObj_bud_item_reasonunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road, "base": week_road}
    sue_bud.add_item(casa_road)
    sue_bud.add_item(week_road)
    sue_bud.get_item_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    # WHEN
    x_obj = bud_get_obj(bud_item_reasonunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road).get_reasonunit(week_road)


def test_bud_get_obj_ReturnsObj_bud_item_reason_premiseunit_get_obj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)
    thur_road = sue_bud.make_road(week_road, "thur")
    casa_jkeys = {"road": casa_road, "base": week_road, "need": thur_road}
    sue_bud.add_item(casa_road)
    sue_bud.add_item(week_road)
    sue_bud.add_item(thur_road)
    casa_item = sue_bud.get_item_obj(casa_road)
    casa_item.set_reasonunit(reasonunit_shop(week_road))
    casa_item.get_reasonunit(week_road).set_premise(thur_road)

    # WHEN
    x_obj = bud_get_obj(premiseunit_str(), sue_bud, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_item.get_reasonunit(week_road).get_premise(thur_road)


def test_bud_get_obj_ReturnsObj_bud_item_factunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_road = sue_bud.make_l1_road("week")
    sue_bud.add_item(casa_road)
    jkeys = {"road": casa_road, "base": week_road}
    sue_bud.add_item(casa_road)
    sue_bud.add_item(week_road)
    sue_bud.get_item_obj(casa_road).set_factunit(factunit_shop(week_road))

    # WHEN
    x_obj = bud_get_obj(bud_item_factunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_road).factunits.get(week_road)
