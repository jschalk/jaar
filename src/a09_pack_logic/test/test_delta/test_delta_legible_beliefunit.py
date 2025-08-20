from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import beliefunit_str
from src.a08_belief_atom_logic.atom_main import beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import UPDATE_str
from src.a09_pack_logic.delta import beliefdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObjEstablishWithEmptyBeliefDelta():
    # ESTABLISH / WHEN
    x_beliefdelta = beliefdelta_shop()
    sue_belief = beliefunit_shop("Sue")

    # THEN
    assert create_legible_list(x_beliefdelta, sue_belief) == []


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_tally():
    # ESTABLISH
    dimen = beliefunit_str()
    tally_str = "tally"
    tally_int = 55
    tally_beliefatom = beliefatom_shop(dimen, UPDATE_str())
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
    dimen = beliefunit_str()
    partner_credor_pool_str = "credor_respect"
    partner_credor_pool_int = 71
    partner_credor_pool_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    partner_credor_pool_beliefatom.set_arg(
        partner_credor_pool_str, partner_credor_pool_int
    )

    print(f"{partner_credor_pool_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(partner_credor_pool_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s credor pool is now {partner_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_debtor_respect():
    # ESTABLISH
    dimen = beliefunit_str()
    partner_debtor_pool_str = "debtor_respect"
    partner_debtor_pool_int = 78
    partner_debtor_pool_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    partner_debtor_pool_beliefatom.set_arg(
        partner_debtor_pool_str, partner_debtor_pool_int
    )

    print(f"{partner_debtor_pool_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(partner_debtor_pool_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s debtor pool is now {partner_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_beliefdelta = beliefdelta_shop()
    dimen = beliefunit_str()
    partner_credor_pool_str = "credor_respect"
    partner_debtor_pool_str = "debtor_respect"
    partner_pool_int = 83
    beliefunit_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    beliefunit_beliefatom.set_arg(partner_credor_pool_str, partner_pool_int)
    beliefunit_beliefatom.set_arg(partner_debtor_pool_str, partner_pool_int)
    x_beliefdelta.set_beliefatom(beliefunit_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{sue_belief.belief_name}'s total pool is now {partner_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBeliefUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = beliefunit_str()
    max_tree_traverse_str = "max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_beliefatom = beliefatom_shop(dimen, UPDATE_str())
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
