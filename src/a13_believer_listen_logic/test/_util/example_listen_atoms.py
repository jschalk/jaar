from src.a01_term_logic.rope import create_rope
from src.a01_term_logic.term import CoinLabel
from src.a06_believer_logic.test._util.a06_str import (
    believer_partnerunit_str,
    believer_plan_factunit_str,
    believer_planunit_str,
    believerunit_str,
    fact_context_str,
    fact_lower_str,
    fact_upper_str,
    partner_name_str,
    plan_rope_str,
)
from src.a08_believer_atom_logic.atom_main import BelieverAtom, believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import BelieverDelta, believerdelta_shop


def get_atom_example_planunit_sports(coin_label: CoinLabel = None) -> BelieverAtom:
    if not coin_label:
        coin_label = "amy23"
    sports_str = "sports"
    x_dimen = believer_planunit_str()
    sports_rope = create_rope(coin_label, sports_str)
    insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_planunit_believeratom.set_jkey(plan_rope_str(), sports_rope)
    return insert_planunit_believeratom


def get_atom_example_planunit_ball(coin_label: CoinLabel = None) -> BelieverAtom:
    if not coin_label:
        coin_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(coin_label, sports_str)
    ball_str = "basketball"
    x_dimen = believer_planunit_str()
    bball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_planunit_believeratom.set_jkey(plan_rope_str(), bball_rope)
    return insert_planunit_believeratom


def get_atom_example_planunit_knee(coin_label: CoinLabel = None) -> BelieverAtom:
    if not coin_label:
        coin_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(coin_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = believer_planunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_planunit_believeratom.set_jkey(plan_rope_str(), knee_rope)
    insert_planunit_believeratom.set_jvalue(begin_str, knee_begin)
    insert_planunit_believeratom.set_jvalue(close_str, knee_close)
    return insert_planunit_believeratom


def get_atom_example_factunit_knee(coin_label: CoinLabel = None) -> BelieverAtom:
    if not coin_label:
        coin_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(coin_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(coin_label, knee_str)
    knee_fact_lower = 7
    knee_fact_upper = 23
    x_dimen = believer_plan_factunit_str()
    insert_factunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_factunit_believeratom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_believeratom.set_jkey(fact_context_str(), knee_rope)
    insert_factunit_believeratom.set_jvalue(fact_lower_str(), knee_fact_lower)
    insert_factunit_believeratom.set_jvalue(fact_upper_str(), knee_fact_upper)
    return insert_factunit_believeratom


def get_believerdelta_sue_example() -> BelieverDelta:
    sue_believerdelta = believerdelta_shop()

    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 77)
    sue_believerdelta.set_believeratom(pool_believeratom)

    dimen = believer_partnerunit_str()
    sue_str = "Sue"
    sue_believeratom = believeratom_shop(dimen, DELETE_str())
    sue_believeratom.set_jkey(partner_name_str(), sue_str)
    sue_believerdelta.set_believeratom(sue_believeratom)
    return sue_believerdelta
