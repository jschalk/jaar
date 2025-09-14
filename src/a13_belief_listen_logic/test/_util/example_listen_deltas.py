from src.a01_rope_logic.term import MomentLabel
from src.a08_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.a09_pack_logic.delta import BeliefDelta, beliefdelta_shop
from src.a13_belief_listen_logic._ref.a13_terms import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    belief_planunit_str,
    belief_voiceunit_str,
    parent_rope_str,
    plan_label_str,
    voice_name_str,
)


def get_atom_example_planunit_sports(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    x_dimen = belief_planunit_str()
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_label_str(), sports_str)
    insert_planunit_beliefatom.set_jkey(parent_rope_str(), moment_label)
    return insert_planunit_beliefatom


def get_beliefdelta_sue_example() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    beliefunit_str = beliefunit_str()
    pool_beliefatom = beliefatom_shop(beliefunit_str(), UPDATE_str())
    pool_attribute = "_credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 77)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)

    dimen = belief_voiceunit_str()
    sue_str = "Sue"
    sue_beliefatom = beliefatom_shop(dimen, DELETE_str())
    sue_beliefatom.set_jkey(voice_name_str(), sue_str)
    sue_beliefdelta.set_beliefatom(sue_beliefatom)
    return sue_beliefdelta


def get_beliefdelta_example1() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    beliefunit_str = beliefunit_str()
    star_name = "star"
    x_beliefatom = beliefatom_shop(beliefunit_str(), UPDATE_str())
    x_beliefatom.set_jvalue(star_name, 55)
    x_attribute = "_max_tree_traverse"
    x_beliefatom.set_jvalue(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_beliefatom.set_jvalue(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_beliefatom.set_jvalue(x_attribute, 88)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    dimen = belief_voiceunit_str()
    sue_str = "Sue"
    x_beliefatom = beliefatom_shop(dimen, DELETE_str())
    x_beliefatom.set_jkey(voice_name_str(), sue_str)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    return sue_beliefdelta


def get_beliefdelta_example2() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    beliefunit_str = beliefunit_str()
    x_beliefatom = beliefatom_shop(beliefunit_str(), UPDATE_str())
    x_attribute = "_credor_respect"
    x_beliefatom.set_jvalue(x_attribute, 77)

    dimen = belief_voiceunit_str()
    sue_str = "Sue"
    x_beliefatom = beliefatom_shop(dimen, DELETE_str())
    x_beliefatom.set_jkey(voice_name_str(), sue_str)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    return sue_beliefdelta
