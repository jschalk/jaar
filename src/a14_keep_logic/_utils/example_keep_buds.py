from src.a06_bud_logic.bud import BudUnit, budunit_shop, itemunit_shop, FiscTag
from src.a14_keep_logic._utils.env_a14 import temp_fisc_tag


def get_1tag_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_tag(temp_fisc_tag())
    x_bud.settle_bud()
    return x_bud


def get_Jtag2tag_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_tag(temp_fisc_tag())
    x_bud.set_l1_item(itemunit_shop("A"))
    x_bud.settle_bud()
    return x_bud


def get_2tag_bud(fisc_tag: FiscTag = None) -> BudUnit:
    if fisc_tag is None:
        fisc_tag = temp_fisc_tag()
    a_str = "A"
    b_str = "B"
    x_bud = budunit_shop(owner_name=a_str)
    x_bud.set_fisc_tag(fisc_tag)
    item_b = itemunit_shop(b_str)
    x_bud.set_item(item_b, parent_road=temp_fisc_tag())
    x_bud.settle_bud()
    return x_bud


def get_3tag_bud() -> BudUnit:
    a_str = "A"
    x_bud = budunit_shop(a_str)
    x_bud.set_fisc_tag(temp_fisc_tag())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    x_bud.settle_bud()
    return x_bud


def get_3tag_D_E_F_bud() -> BudUnit:
    d_str = "D"
    x_bud = budunit_shop(d_str)
    x_bud.set_fisc_tag(temp_fisc_tag())
    x_bud.set_l1_item(itemunit_shop("E"))
    x_bud.set_l1_item(itemunit_shop("F"))
    x_bud.settle_bud()
    return x_bud


def get_6tag_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_tag(temp_fisc_tag())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("D"), c_road)
    x_bud.set_item(itemunit_shop("E"), c_road)
    x_bud.set_item(itemunit_shop("F"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7tagInsertH_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_tag(temp_fisc_tag())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("H"), c_road)
    x_bud.set_item(itemunit_shop("D"), c_road)
    x_bud.set_item(itemunit_shop("E"), c_road)
    x_bud.set_item(itemunit_shop("F"), x_bud.make_road(c_road, "H"))
    x_bud.settle_bud()
    return x_bud


def get_5tagHG_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_tag(temp_fisc_tag())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("H"), c_road)
    x_bud.set_item(itemunit_shop("G"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7tagJRoot_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_tag(temp_fisc_tag())
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
