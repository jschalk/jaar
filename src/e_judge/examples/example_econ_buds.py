from src.bud.bud import BudUnit, budunit_shop, ideaunit_shop, FiscalID
from src.e_judge.examples.econ_env import temp_fiscal_id


def get_1node_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.settle_bud()
    return x_bud


def get_Jnode2node_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.set_l1_idea(ideaunit_shop("A"))
    x_bud.settle_bud()
    return x_bud


def get_2node_bud(fiscal_id: FiscalID = None) -> BudUnit:
    if fiscal_id is None:
        fiscal_id = temp_fiscal_id()
    a_str = "A"
    b_str = "B"
    x_bud = budunit_shop(_owner_id=a_str)
    x_bud.set_fiscal_id(fiscal_id)
    idea_b = ideaunit_shop(b_str)
    x_bud.set_idea(idea_b, parent_road=temp_fiscal_id())
    x_bud.settle_bud()
    return x_bud


def get_3node_bud() -> BudUnit:
    a_str = "A"
    x_bud = budunit_shop(a_str)
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    x_bud.settle_bud()
    return x_bud


def get_3node_D_E_F_bud() -> BudUnit:
    d_str = "D"
    x_bud = budunit_shop(d_str)
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.set_l1_idea(ideaunit_shop("E"))
    x_bud.set_l1_idea(ideaunit_shop("F"))
    x_bud.settle_bud()
    return x_bud


def get_6node_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_idea(ideaunit_shop("D"), c_road)
    x_bud.set_idea(ideaunit_shop("E"), c_road)
    x_bud.set_idea(ideaunit_shop("F"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7nodeInsertH_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_idea(ideaunit_shop("H"), c_road)
    x_bud.set_idea(ideaunit_shop("D"), c_road)
    x_bud.set_idea(ideaunit_shop("E"), c_road)
    x_bud.set_idea(ideaunit_shop("F"), x_bud.make_road(c_road, "H"))
    x_bud.settle_bud()
    return x_bud


def get_5nodeHG_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    c_road = x_bud.make_l1_road("C")
    x_bud.set_idea(ideaunit_shop("H"), c_road)
    x_bud.set_idea(ideaunit_shop("G"), c_road)
    x_bud.settle_bud()
    return x_bud


def get_7nodeJRoot_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fiscal_id(temp_fiscal_id())
    x_bud.set_l1_idea(ideaunit_shop("A"))

    a_road = x_bud.make_l1_road("A")
    x_bud.set_idea(ideaunit_shop("B"), a_road)
    x_bud.set_idea(ideaunit_shop("C"), a_road)
    c_road = x_bud.make_l1_road("C")
    x_bud.set_idea(ideaunit_shop("D"), c_road)
    x_bud.set_idea(ideaunit_shop("E"), c_road)
    x_bud.set_idea(ideaunit_shop("F"), c_road)
    x_bud.settle_bud()
    return x_bud
