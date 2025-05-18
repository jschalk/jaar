from src.a06_bud_logic.bud import BudUnit, budunit_shop, conceptunit_shop, FiscLabel
from src.a14_keep_logic._utils.env_a14 import temp_fisc_label


def get_1label_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.settle_bud()
    return x_bud


def get_Jlabel2label_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.set_l1_concept(conceptunit_shop("A"))
    x_bud.settle_bud()
    return x_bud


def get_2label_bud(fisc_label: FiscLabel = None) -> BudUnit:
    if fisc_label is None:
        fisc_label = temp_fisc_label()
    a_str = "A"
    b_str = "B"
    x_bud = budunit_shop(owner_name=a_str)
    x_bud.set_fisc_label(fisc_label)
    concept_b = conceptunit_shop(b_str)
    x_bud.set_concept(concept_b, parent_way=temp_fisc_label())
    x_bud.settle_bud()
    return x_bud


def get_3label_bud() -> BudUnit:
    a_str = "A"
    x_bud = budunit_shop(a_str)
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.set_l1_concept(conceptunit_shop("B"))
    x_bud.set_l1_concept(conceptunit_shop("C"))
    x_bud.settle_bud()
    return x_bud


def get_3label_D_E_F_bud() -> BudUnit:
    d_str = "D"
    x_bud = budunit_shop(d_str)
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.set_l1_concept(conceptunit_shop("E"))
    x_bud.set_l1_concept(conceptunit_shop("F"))
    x_bud.settle_bud()
    return x_bud


def get_6label_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.set_l1_concept(conceptunit_shop("B"))
    x_bud.set_l1_concept(conceptunit_shop("C"))
    c_way = x_bud.make_l1_way("C")
    x_bud.set_concept(conceptunit_shop("D"), c_way)
    x_bud.set_concept(conceptunit_shop("E"), c_way)
    x_bud.set_concept(conceptunit_shop("F"), c_way)
    x_bud.settle_bud()
    return x_bud


def get_7labelInsertH_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.set_l1_concept(conceptunit_shop("B"))
    x_bud.set_l1_concept(conceptunit_shop("C"))
    c_way = x_bud.make_l1_way("C")
    x_bud.set_concept(conceptunit_shop("H"), c_way)
    x_bud.set_concept(conceptunit_shop("D"), c_way)
    x_bud.set_concept(conceptunit_shop("E"), c_way)
    x_bud.set_concept(conceptunit_shop("F"), x_bud.make_way(c_way, "H"))
    x_bud.settle_bud()
    return x_bud


def get_5labelHG_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.set_l1_concept(conceptunit_shop("B"))
    x_bud.set_l1_concept(conceptunit_shop("C"))
    c_way = x_bud.make_l1_way("C")
    x_bud.set_concept(conceptunit_shop("H"), c_way)
    x_bud.set_concept(conceptunit_shop("G"), c_way)
    x_bud.settle_bud()
    return x_bud


def get_7labelJRoot_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_label(temp_fisc_label())
    x_bud.set_l1_concept(conceptunit_shop("A"))

    a_way = x_bud.make_l1_way("A")
    x_bud.set_concept(conceptunit_shop("B"), a_way)
    x_bud.set_concept(conceptunit_shop("C"), a_way)
    c_way = x_bud.make_l1_way("C")
    x_bud.set_concept(conceptunit_shop("D"), c_way)
    x_bud.set_concept(conceptunit_shop("E"), c_way)
    x_bud.set_concept(conceptunit_shop("F"), c_way)
    x_bud.settle_bud()
    return x_bud
