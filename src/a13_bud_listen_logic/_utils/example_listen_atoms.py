from src.a01_way_logic.way import create_way, FiscLabel
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_conceptunit_str,
    bud_concept_factunit_str,
    acct_name_str,
    concept_way_str,
    fcontext_str,
    fopen_str,
    fnigh_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_insert, atom_update, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop, BudAtom
from src.a09_pack_logic.delta import buddelta_shop, BudDelta


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
    bball_way = create_way(sports_way, ball_str)
    insert_conceptunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_conceptunit_budatom.set_jkey(concept_way_str(), bball_way)
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


def get_atom_example_factunit_knee(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_label, sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way(fisc_label, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_dimen = bud_concept_factunit_str()
    insert_factunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_factunit_budatom.set_jkey(concept_way_str(), ball_way)
    insert_factunit_budatom.set_jkey(fcontext_str(), knee_way)
    insert_factunit_budatom.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_budatom.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_budatom


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    pool_budatom = budatom_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_budatom.set_jvalue(pool_attribute, 77)
    sue_buddelta.set_budatom(pool_budatom)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_budatom = budatom_shop(dimen, atom_delete())
    sue_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(sue_budatom)
    return sue_buddelta
