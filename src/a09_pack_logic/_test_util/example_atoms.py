from src.a01_term_logic.way import VowLabel, create_way
from src.a06_plan_logic._test_util.a06_str import concept_way_str, plan_conceptunit_str
from src.a08_plan_atom_logic._test_util.a08_str import INSERT_str
from src.a08_plan_atom_logic.atom import PlanAtom, planatom_shop


def get_atom_example_conceptunit_sports(vow_label: VowLabel = None) -> PlanAtom:
    if not vow_label:
        vow_label = "accord23"
    sports_str = "sports"
    x_dimen = plan_conceptunit_str()
    sports_way = create_way(vow_label, sports_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_way_str(), sports_way)
    return insert_conceptunit_planatom


def get_atom_example_conceptunit_ball(vow_label: VowLabel = None) -> PlanAtom:
    if not vow_label:
        vow_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(vow_label, sports_str)
    ball_str = "basketball"
    x_dimen = plan_conceptunit_str()
    ball_way = create_way(sports_way, ball_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_way_str(), ball_way)
    return insert_conceptunit_planatom


def get_atom_example_conceptunit_knee(vow_label: VowLabel = None) -> PlanAtom:
    if not vow_label:
        vow_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(vow_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = plan_conceptunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_way = create_way(sports_way, knee_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_way_str(), knee_way)
    insert_conceptunit_planatom.set_jvalue(begin_str, knee_begin)
    insert_conceptunit_planatom.set_jvalue(close_str, knee_close)
    return insert_conceptunit_planatom
