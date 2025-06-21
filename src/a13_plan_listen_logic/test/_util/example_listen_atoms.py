from src.a01_term_logic.rope import create_rope
from src.a01_term_logic.term import BankLabel
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    concept_rope_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    plan_acctunit_str,
    plan_concept_factunit_str,
    plan_conceptunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic.atom import PlanAtom, planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import PlanDelta, plandelta_shop


def get_atom_example_conceptunit_sports(bank_label: BankLabel = None) -> PlanAtom:
    if not bank_label:
        bank_label = "accord23"
    sports_str = "sports"
    x_dimen = plan_conceptunit_str()
    sports_rope = create_rope(bank_label, sports_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_rope_str(), sports_rope)
    return insert_conceptunit_planatom


def get_atom_example_conceptunit_ball(bank_label: BankLabel = None) -> PlanAtom:
    if not bank_label:
        bank_label = "accord23"
    sports_str = "sports"
    sports_rope = create_rope(bank_label, sports_str)
    ball_str = "basketball"
    x_dimen = plan_conceptunit_str()
    bball_rope = create_rope(sports_rope, ball_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_rope_str(), bball_rope)
    return insert_conceptunit_planatom


def get_atom_example_conceptunit_knee(bank_label: BankLabel = None) -> PlanAtom:
    if not bank_label:
        bank_label = "accord23"
    sports_str = "sports"
    sports_rope = create_rope(bank_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = plan_conceptunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_rope_str(), knee_rope)
    insert_conceptunit_planatom.set_jvalue(begin_str, knee_begin)
    insert_conceptunit_planatom.set_jvalue(close_str, knee_close)
    return insert_conceptunit_planatom


def get_atom_example_factunit_knee(bank_label: BankLabel = None) -> PlanAtom:
    if not bank_label:
        bank_label = "accord23"
    sports_str = "sports"
    sports_rope = create_rope(bank_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(bank_label, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_dimen = plan_concept_factunit_str()
    insert_factunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_factunit_planatom.set_jkey(concept_rope_str(), ball_rope)
    insert_factunit_planatom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_planatom.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_planatom.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_planatom


def get_plandelta_sue_example() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 77)
    sue_plandelta.set_planatom(pool_planatom)

    dimen = plan_acctunit_str()
    sue_str = "Sue"
    sue_planatom = planatom_shop(dimen, DELETE_str())
    sue_planatom.set_jkey(acct_name_str(), sue_str)
    sue_plandelta.set_planatom(sue_planatom)
    return sue_plandelta
