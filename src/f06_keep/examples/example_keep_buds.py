from src.f02_bud.bud import BudUnit, budunit_shop, itemunit_shop, FiscTitle
from src.f06_keep.examples.keep_env import temp_fisc_title


def get_1title_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_title(temp_fisc_title())
    x_bud.settle_bud()
    return x_bud


def get_Jtitle2title_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_title(temp_fisc_title())
    x_bud.set_l1_item(itemunit_shop("A"))
    x_bud.settle_bud()
    return x_bud


def get_2title_bud(fisc_title: FiscTitle = None) -> BudUnit:
    if fisc_title is None:
        fisc_title = temp_fisc_title()
    a_str = "A"
    b_str = "B"
    x_bud = budunit_shop(owner_name=a_str)
    x_bud.set_fisc_title(fisc_title)
    item_b = itemunit_shop(b_str)
    x_bud.set_item(item_b, parent_road=temp_fisc_title())
    x_bud.settle_bud()
    return x_bud


def get_3title_bud() -> BudUnit:
    a_str = "A"
    x_bud = budunit_shop(a_str)
    x_bud.set_fisc_title(temp_fisc_title())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    x_bud.settle_bud()
    return x_bud


def get_3title_D_E_F_bud() -> BudUnit:
    d_str = "D"
    x_bud = budunit_shop(d_str)
    x_bud.set_fisc_title(temp_fisc_title())
    x_bud.set_l1_item(itemunit_shop("E"))
    x_bud.set_l1_item(itemunit_shop("F"))
    x_bud.settle_bud()
    return x_bud


def get_6title_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_title(temp_fisc_title())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("D"), c_road)
    x_bud.set_item(itemunit_shop("E"), c_road)
    x_bud.set_item(itemunit_shop("F"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7titleInsertH_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_title(temp_fisc_title())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("H"), c_road)
    x_bud.set_item(itemunit_shop("D"), c_road)
    x_bud.set_item(itemunit_shop("E"), c_road)
    x_bud.set_item(itemunit_shop("F"), x_bud.make_road(c_road, "H"))
    x_bud.settle_bud()
    return x_bud


def get_5titleHG_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_title(temp_fisc_title())
    x_bud.set_l1_item(itemunit_shop("B"))
    x_bud.set_l1_item(itemunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_item(itemunit_shop("H"), c_road)
    x_bud.set_item(itemunit_shop("G"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7titleJRoot_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_title(temp_fisc_title())
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
