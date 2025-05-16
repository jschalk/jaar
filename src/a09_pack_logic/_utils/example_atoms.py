from src.a01_way_logic.way import create_way, FiscWord
from src.a06_bud_logic._utils.str_a06 import bud_ideaunit_str
from src.a06_bud_logic._utils.str_a06 import idea_way_str
from src.a08_bud_atom_logic._utils.str_a08 import atom_insert
from src.a08_bud_atom_logic.atom import budatom_shop, BudAtom


def get_atom_example_ideaunit_sports(fisc_word: FiscWord = None) -> BudAtom:
    if not fisc_word:
        fisc_word = "accord23"
    sports_str = "sports"
    x_dimen = bud_ideaunit_str()
    sports_way = create_way(fisc_word, sports_str)
    insert_ideaunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_ideaunit_budatom.set_jkey(idea_way_str(), sports_way)
    return insert_ideaunit_budatom


def get_atom_example_ideaunit_ball(fisc_word: FiscWord = None) -> BudAtom:
    if not fisc_word:
        fisc_word = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_word, sports_str)
    ball_str = "basketball"
    x_dimen = bud_ideaunit_str()
    ball_way = create_way(sports_way, ball_str)
    insert_ideaunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_ideaunit_budatom.set_jkey(idea_way_str(), ball_way)
    return insert_ideaunit_budatom


def get_atom_example_ideaunit_knee(fisc_word: FiscWord = None) -> BudAtom:
    if not fisc_word:
        fisc_word = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_word, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = bud_ideaunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_way = create_way(sports_way, knee_str)
    insert_ideaunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_ideaunit_budatom.set_jkey(idea_way_str(), knee_way)
    insert_ideaunit_budatom.set_jvalue(begin_str, knee_begin)
    insert_ideaunit_budatom.set_jvalue(close_str, knee_close)
    return insert_ideaunit_budatom
