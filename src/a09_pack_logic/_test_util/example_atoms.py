from src.a01_way_logic.way import create_way, FiscLabel
from src.a06_bud_logic._test_util.a06_str import bud_conceptunit_str
from src.a06_bud_logic._test_util.a06_str import concept_way_str
from src.a08_bud_atom_logic._test_util.a08_str import atom_insert
from src.a08_bud_atom_logic.atom import budatom_shop, BudAtom


def get_atom_example_conceptunit_sports(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    x_dimen = bud_conceptunit_str()
    sports_way = create_way(fisc_label, sports_str)
    insert_conceptunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_conceptunit_budatom.set_jkey(concept_way_str(), sports_way)
    return insert_conceptunit_budatom


def get_atom_example_conceptunit_ball(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_label, sports_str)
    ball_str = "basketball"
    x_dimen = bud_conceptunit_str()
    ball_way = create_way(sports_way, ball_str)
    insert_conceptunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_conceptunit_budatom.set_jkey(concept_way_str(), ball_way)
    return insert_conceptunit_budatom


def get_atom_example_conceptunit_knee(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = bud_conceptunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_way = create_way(sports_way, knee_str)
    insert_conceptunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_conceptunit_budatom.set_jkey(concept_way_str(), knee_way)
    insert_conceptunit_budatom.set_jvalue(begin_str, knee_begin)
    insert_conceptunit_budatom.set_jvalue(close_str, knee_close)
    return insert_conceptunit_budatom
