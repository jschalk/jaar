from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_belief_atom.atom_main import beliefatom_shop
from src.ch09_belief_lesson.delta import beliefdelta_shop
from src.ch09_belief_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObjEstablishWithEmptyBeliefDelta():
    # ESTABLISH / WHEN
    x_beliefdelta = beliefdelta_shop()
    sue_belief = beliefunit_shop("Sue")

    # THEN
    assert create_legible_list(x_beliefdelta, sue_belief) == []


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_tally():
    # ESTABLISH
    dimen = kw.beliefunit
    tally_str = kw.tally
    tally_int = 55
    tally_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    tally_beliefatom.set_arg(tally_str, tally_int)
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(tally_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s belief tally set to {tally_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_credor_respect():
    # ESTABLISH
    dimen = kw.beliefunit
    credor_respect_int = 71
    credor_respect_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    credor_respect_beliefatom.set_arg(kw.credor_respect, credor_respect_int)

    print(f"{credor_respect_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(credor_respect_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s credor pool is now {credor_respect_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_debtor_respect():
    # ESTABLISH
    dimen = kw.beliefunit
    voice_debtor_pool_int = 78
    voice_debtor_pool_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    voice_debtor_pool_beliefatom.set_arg(kw.debtor_respect, voice_debtor_pool_int)

    print(f"{voice_debtor_pool_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(voice_debtor_pool_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s debtor pool is now {voice_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_beliefdelta = beliefdelta_shop()
    dimen = kw.beliefunit
    voice_pool_int = 83
    beliefunit_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    beliefunit_beliefatom.set_arg(kw.credor_respect, voice_pool_int)
    beliefunit_beliefatom.set_arg(kw.debtor_respect, voice_pool_int)
    x_beliefdelta.set_beliefatom(beliefunit_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s total pool is now {voice_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = kw.beliefunit
    max_tree_traverse_str = kw.max_tree_traverse
    max_tree_traverse_int = 71
    max_tree_traverse_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    max_tree_traverse_beliefatom.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(max_tree_traverse_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s maximum number of Belief evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
