from src.a01_term_logic.rope import create_rope
from src.a01_term_logic.term import BankLabel
from src.a06_plan_logic.test._util.a06_str import concept_rope_str, plan_conceptunit_str
from src.a08_plan_atom_logic.atom import PlanAtom, planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import INSERT_str


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
    ball_rope = create_rope(sports_rope, ball_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_rope_str(), ball_rope)
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
