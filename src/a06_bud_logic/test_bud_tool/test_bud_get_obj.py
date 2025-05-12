from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_item import reasonunit_shop, factunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_tool import (
    bud_acctunit_get_obj,
    bud_acct_membership_get_obj,
    bud_itemunit_get_obj,
    bud_item_awardlink_get_obj,
    bud_item_reasonunit_get_obj,
    bud_item_reason_premiseunit_get_obj as premiseunit_get_obj,
    bud_item_factunit_get_obj,
    bud_get_obj,
)
from src.a06_bud_logic._utils.str_a06 import (
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
    item_way_str,
    base_str,
    fbase_str,
    need_str,
    fneed_str,
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
    casa_way = sue_bud.make_l1_way(casa_str)
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way}

    # WHEN
    x_obj = bud_itemunit_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way)


def test_bud_item_awardlink_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_way = sue_bud.make_l1_way(casa_str)
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way, "awardee_label": swim_str}
    sue_bud.add_item(casa_way)
    sue_bud.get_item_obj(casa_way).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = bud_item_awardlink_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way).get_awardlink(swim_str)


def test_bud_item_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    week_way = sue_bud.make_l1_way("week")
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way, base_str(): week_way}
    sue_bud.add_item(casa_way)
    sue_bud.add_item(week_way)
    sue_bud.get_item_obj(casa_way).set_reasonunit(reasonunit_shop(week_way))

    # WHEN
    x_obj = bud_item_reasonunit_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way).get_reasonunit(week_way)


def test_bud_item_reason_premiseunit_get_obj_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    thur_way = sue_bud.make_way(week_way, "thur")
    casa_jkeys = {item_way_str(): casa_way, base_str(): week_way, need_str(): thur_way}
    sue_bud.add_item(casa_way)
    sue_bud.add_item(week_way)
    sue_bud.add_item(thur_way)
    casa_item = sue_bud.get_item_obj(casa_way)
    casa_item.set_reasonunit(reasonunit_shop(week_way))
    casa_item.get_reasonunit(week_way).set_premise(thur_way)

    # WHEN
    x_obj = premiseunit_get_obj(sue_bud, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_item.get_reasonunit(week_way).get_premise(thur_way)


def test_bud_item_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    week_way = sue_bud.make_l1_way("week")
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way, fbase_str(): week_way}
    sue_bud.add_item(casa_way)
    sue_bud.add_item(week_way)
    sue_bud.get_item_obj(casa_way).set_factunit(factunit_shop(week_way))

    # WHEN
    x_obj = bud_item_factunit_get_obj(sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way).factunits.get(week_way)


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
    casa_way = sue_bud.make_l1_way(casa_str)
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way}

    # WHEN
    x_obj = bud_get_obj(bud_itemunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way)


def test_bud_get_obj_ReturnsObj_bud_item_awardlink_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_way = sue_bud.make_l1_way(casa_str)
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way, "awardee_label": swim_str}
    sue_bud.add_item(casa_way)
    sue_bud.get_item_obj(casa_way).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = bud_get_obj(bud_item_awardlink_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way).get_awardlink(swim_str)


def test_bud_get_obj_ReturnsObj_bud_item_reasonunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    week_way = sue_bud.make_l1_way("week")
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way, base_str(): week_way}
    sue_bud.add_item(casa_way)
    sue_bud.add_item(week_way)
    sue_bud.get_item_obj(casa_way).set_reasonunit(reasonunit_shop(week_way))

    # WHEN
    x_obj = bud_get_obj(bud_item_reasonunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way).get_reasonunit(week_way)


def test_bud_get_obj_ReturnsObj_bud_item_reason_premiseunit_get_obj():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    thur_way = sue_bud.make_way(week_way, "thur")
    casa_jkeys = {item_way_str(): casa_way, base_str(): week_way, need_str(): thur_way}
    sue_bud.add_item(casa_way)
    sue_bud.add_item(week_way)
    sue_bud.add_item(thur_way)
    casa_item = sue_bud.get_item_obj(casa_way)
    casa_item.set_reasonunit(reasonunit_shop(week_way))
    casa_item.get_reasonunit(week_way).set_premise(thur_way)

    # WHEN
    x_obj = bud_get_obj(premiseunit_str(), sue_bud, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_item.get_reasonunit(week_way).get_premise(thur_way)


def test_bud_get_obj_ReturnsObj_bud_item_factunit_get_obj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    week_way = sue_bud.make_l1_way("week")
    sue_bud.add_item(casa_way)
    jkeys = {item_way_str(): casa_way, fbase_str(): week_way}
    sue_bud.add_item(casa_way)
    sue_bud.add_item(week_way)
    sue_bud.get_item_obj(casa_way).set_factunit(factunit_shop(week_way))

    # WHEN
    x_obj = bud_get_obj(bud_item_factunit_str(), sue_bud, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_bud.get_item_obj(casa_way).factunits.get(week_way)
