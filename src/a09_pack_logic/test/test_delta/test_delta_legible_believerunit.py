from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import believerunit_str
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import UPDATE_str
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObjEstablishWithEmptyBelieverDelta():
    # ESTABLISH / WHEN
    x_believerdelta = believerdelta_shop()
    sue_believer = believerunit_shop("Sue")

    # THEN
    assert create_legible_list(x_believerdelta, sue_believer) == []


def test_create_legible_list_ReturnsObjEstablishWithBelieverUpdate_tally():
    # ESTABLISH
    dimen = believerunit_str()
    tally_str = "tally"
    tally_int = 55
    tally_believeratom = believeratom_shop(dimen, UPDATE_str())
    tally_believeratom.set_arg(tally_str, tally_int)
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(tally_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{sue_believer.believer_name}'s believer tally set to {tally_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBelieverUpdate_credor_respect():
    # ESTABLISH
    dimen = believerunit_str()
    partner_credor_pool_str = "credor_respect"
    partner_credor_pool_int = 71
    partner_credor_pool_believeratom = believeratom_shop(dimen, UPDATE_str())
    partner_credor_pool_believeratom.set_arg(
        partner_credor_pool_str, partner_credor_pool_int
    )

    print(f"{partner_credor_pool_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(partner_credor_pool_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = (
        f"{sue_believer.believer_name}'s credor pool is now {partner_credor_pool_int}"
    )
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBelieverUpdate_debtor_respect():
    # ESTABLISH
    dimen = believerunit_str()
    partner_debtor_pool_str = "debtor_respect"
    partner_debtor_pool_int = 78
    partner_debtor_pool_believeratom = believeratom_shop(dimen, UPDATE_str())
    partner_debtor_pool_believeratom.set_arg(
        partner_debtor_pool_str, partner_debtor_pool_int
    )

    print(f"{partner_debtor_pool_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(partner_debtor_pool_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = (
        f"{sue_believer.believer_name}'s debtor pool is now {partner_debtor_pool_int}"
    )
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBelieverUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_believerdelta = believerdelta_shop()
    dimen = believerunit_str()
    partner_credor_pool_str = "credor_respect"
    partner_debtor_pool_str = "debtor_respect"
    partner_pool_int = 83
    believerunit_believeratom = believeratom_shop(dimen, UPDATE_str())
    believerunit_believeratom.set_arg(partner_credor_pool_str, partner_pool_int)
    believerunit_believeratom.set_arg(partner_debtor_pool_str, partner_pool_int)
    x_believerdelta.set_believeratom(believerunit_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{sue_believer.believer_name}'s total pool is now {partner_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBelieverUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = believerunit_str()
    max_tree_traverse_str = "max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_believeratom = believeratom_shop(dimen, UPDATE_str())
    max_tree_traverse_believeratom.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(max_tree_traverse_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{sue_believer.believer_name}'s maximum number of Believer evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
