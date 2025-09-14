from src.a08_belief_atom_logic.atom_main import beliefatom_shop
from src.a09_pack_logic.delta import BeliefDelta, beliefdelta_shop
from src.a09_pack_logic.test._util.a09_terms import (
    DELETE_str,
    UPDATE_str,
    belief_voiceunit_str,
    beliefunit_str,
    voice_name_str,
)


def get_beliefdelta_sue_example() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    pool_beliefatom = beliefatom_shop(beliefunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
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

    tally_name = "tally"
    x_beliefatom = beliefatom_shop(beliefunit_str(), UPDATE_str())
    x_beliefatom.set_jvalue(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_beliefatom.set_jvalue(x_attribute, 66)
    x_attribute = "credor_respect"
    x_beliefatom.set_jvalue(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_beliefatom.set_jvalue(x_attribute, 88)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    dimen = belief_voiceunit_str()
    zia_str = "Zia"
    x_beliefatom = beliefatom_shop(dimen, DELETE_str())
    x_beliefatom.set_jkey(voice_name_str(), zia_str)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    return sue_beliefdelta
