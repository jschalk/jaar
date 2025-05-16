from src.a06_bud_logic.bud import BudUnit, budunit_shop, ideaunit_shop, FiscWord
from src.a14_keep_logic._utils.env_a14 import temp_fisc_word


def get_1word_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.settle_bud()
    return x_bud


def get_Jword2word_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.set_l1_idea(ideaunit_shop("A"))
    x_bud.settle_bud()
    return x_bud


def get_2word_bud(fisc_word: FiscWord = None) -> BudUnit:
    if fisc_word is None:
        fisc_word = temp_fisc_word()
    a_str = "A"
    b_str = "B"
    x_bud = budunit_shop(owner_name=a_str)
    x_bud.set_fisc_word(fisc_word)
    idea_b = ideaunit_shop(b_str)
    x_bud.set_idea(idea_b, parent_way=temp_fisc_word())
    x_bud.settle_bud()
    return x_bud


def get_3word_bud() -> BudUnit:
    a_str = "A"
    x_bud = budunit_shop(a_str)
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    x_bud.settle_bud()
    return x_bud


def get_3word_D_E_F_bud() -> BudUnit:
    d_str = "D"
    x_bud = budunit_shop(d_str)
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.set_l1_idea(ideaunit_shop("E"))
    x_bud.set_l1_idea(ideaunit_shop("F"))
    x_bud.settle_bud()
    return x_bud


def get_6word_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    c_way = x_bud.make_l1_way("C")
    x_bud.set_idea(ideaunit_shop("D"), c_way)
    x_bud.set_idea(ideaunit_shop("E"), c_way)
    x_bud.set_idea(ideaunit_shop("F"), c_way)
    x_bud.settle_bud()
    return x_bud


def get_7wordInsertH_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    c_way = x_bud.make_l1_way("C")
    x_bud.set_idea(ideaunit_shop("H"), c_way)
    x_bud.set_idea(ideaunit_shop("D"), c_way)
    x_bud.set_idea(ideaunit_shop("E"), c_way)
    x_bud.set_idea(ideaunit_shop("F"), x_bud.make_way(c_way, "H"))
    x_bud.settle_bud()
    return x_bud


def get_5wordHG_bud() -> BudUnit:
    x_bud = budunit_shop("A")
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.set_l1_idea(ideaunit_shop("B"))
    x_bud.set_l1_idea(ideaunit_shop("C"))
    c_way = x_bud.make_l1_way("C")
    x_bud.set_idea(ideaunit_shop("H"), c_way)
    x_bud.set_idea(ideaunit_shop("G"), c_way)
    x_bud.settle_bud()
    return x_bud


def get_7wordJRoot_bud() -> BudUnit:
    x_bud = budunit_shop("J")
    x_bud.set_fisc_word(temp_fisc_word())
    x_bud.set_l1_idea(ideaunit_shop("A"))

    a_way = x_bud.make_l1_way("A")
    x_bud.set_idea(ideaunit_shop("B"), a_way)
    x_bud.set_idea(ideaunit_shop("C"), a_way)
    c_way = x_bud.make_l1_way("C")
    x_bud.set_idea(ideaunit_shop("D"), c_way)
    x_bud.set_idea(ideaunit_shop("E"), c_way)
    x_bud.set_idea(ideaunit_shop("F"), c_way)
    x_bud.settle_bud()
    return x_bud
