from src.a01_term_logic.rope import create_rope
from src.a01_term_logic.term import BeliefLabel
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    concept_rope_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    owner_acctunit_str,
    owner_concept_factunit_str,
    owner_conceptunit_str,
    ownerunit_str,
)
from src.a08_owner_atom_logic.atom import OwnerAtom, owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import OwnerDelta, ownerdelta_shop


def get_atom_example_conceptunit_sports(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    x_dimen = owner_conceptunit_str()
    sports_rope = create_rope(belief_label, sports_str)
    insert_conceptunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_conceptunit_owneratom.set_jkey(concept_rope_str(), sports_rope)
    return insert_conceptunit_owneratom


def get_atom_example_conceptunit_ball(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    ball_str = "basketball"
    x_dimen = owner_conceptunit_str()
    bball_rope = create_rope(sports_rope, ball_str)
    insert_conceptunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_conceptunit_owneratom.set_jkey(concept_rope_str(), bball_rope)
    return insert_conceptunit_owneratom


def get_atom_example_conceptunit_knee(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = owner_conceptunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_conceptunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_conceptunit_owneratom.set_jkey(concept_rope_str(), knee_rope)
    insert_conceptunit_owneratom.set_jvalue(begin_str, knee_begin)
    insert_conceptunit_owneratom.set_jvalue(close_str, knee_close)
    return insert_conceptunit_owneratom


def get_atom_example_factunit_knee(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(belief_label, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_dimen = owner_concept_factunit_str()
    insert_factunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_factunit_owneratom.set_jkey(concept_rope_str(), ball_rope)
    insert_factunit_owneratom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_owneratom.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_owneratom.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_owneratom


def get_ownerdelta_sue_example() -> OwnerDelta:
    sue_ownerdelta = ownerdelta_shop()

    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 77)
    sue_ownerdelta.set_owneratom(pool_owneratom)

    dimen = owner_acctunit_str()
    sue_str = "Sue"
    sue_owneratom = owneratom_shop(dimen, DELETE_str())
    sue_owneratom.set_jkey(acct_name_str(), sue_str)
    sue_ownerdelta.set_owneratom(sue_owneratom)
    return sue_ownerdelta
