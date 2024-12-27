from src.f02_bud.bud import BudUnit, budunit_shop, itemunit_shop, dealID
from src.f06_keep.examples.keep_env import temp_deal_id


def get_1idea_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_deal_id(temp_deal_id())
    x_bud.settle_bud()
    return x_bud


def get_Jidea2idea_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_deal_id(temp_deal_id())
    x_bud.set_l1_item(itemunit_shop("A"))
    x_bud.settle_bud()
    return x_bud


def get_2idea_bud(deal_id: dealID = None) -> BudUnit:
    if deal_id is None:
        deal_id = temp_deal_id()
    a_str = "A"
    b_str = "B"
    x_bud = budunit_shop(_owner_id=a_str)
    x_bud.set_deal_id(deal_id)
    item_b = itemunit_shop(b_str)
    x_bud.set_item(item_b, parent_road=temp_deal_id())
    x_bud.settle_bud()
    return x_bud


def get_3idea_bud() -> BudUnit:
    a_str = "A"
    x_bud = budunit_shop(a_str)
    x_bud.set_deal_id(temp_deal_id())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    x_bud.settle_bud()
    return x_bud


def get_3idea_D_E_F_bud() -> BudUnit:
    d_str = "D"
    x_bud = budunit_shop(d_str)
    x_bud.set_deal_id(temp_deal_id())
    x_bud.set_l1_item(itemunit_shop("E"))
    x_bud.set_l1_item(itemunit_shop("F"))
    x_bud.settle_bud()
    return x_bud


def get_6idea_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_deal_id(temp_deal_id())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("D"), c_road)
    x_bud.set_item(itemunit_shop("E"), c_road)
    x_bud.set_item(itemunit_shop("F"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7ideaInsertH_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_deal_id(temp_deal_id())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("H"), c_road)
    x_bud.set_item(itemunit_shop("D"), c_road)
    x_bud.set_item(itemunit_shop("E"), c_road)
    x_bud.set_item(itemunit_shop("F"), x_bud.make_road(c_road, "H"))
    x_bud.settle_bud()
    return x_bud


def get_5ideaHG_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_deal_id(temp_deal_id())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("H"), c_road)
    x_bud.set_item(itemunit_shop("G"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7ideaJRoot_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_deal_id(temp_deal_id())
    x_bud.set_l1_item(itemunit_shop("A"))

    a_road = x_bud.make_l1_road("A")
    x_bud.set_item(itemunit_shop("B"), a_road)
    x_bud.set_item(itemunit_shop("C"), a_road)
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("D"), c_road)
    x_bud.set_item(itemunit_shop("E"), c_road)
    x_bud.set_item(itemunit_shop("F"), c_road)
    x_bud.settle_bud()
    return x_bud
