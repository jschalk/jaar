from src.a06_bud_logic._utils.str_helpers import budunit_str
from src.a08_bud_atom_logic.atom_config import atom_update
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObjEstablishWithEmptyBudDelta():
    # ESTABLISH / WHEN
    x_buddelta = buddelta_shop()
    sue_bud = budunit_shop("Sue")

    # THEN
    assert create_legible_list(x_buddelta, sue_bud) == []


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_tally():
    # ESTABLISH
    dimen = budunit_str()
    tally_str = "tally"
    tally_int = 55
    tally_budatom = budatom_shop(dimen, atom_update())
    tally_budatom.set_arg(tally_str, tally_int)
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(tally_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{sue_bud.owner_name}'s bud tally set to {tally_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_credor_respect():
    # ESTABLISH
    dimen = budunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_credor_pool_int = 71
    acct_credor_pool_budatom = budatom_shop(dimen, atom_update())
    acct_credor_pool_budatom.set_arg(acct_credor_pool_str, acct_credor_pool_int)

    print(f"{acct_credor_pool_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(acct_credor_pool_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{sue_bud.owner_name}'s credor pool is now {acct_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_debtor_respect():
    # ESTABLISH
    dimen = budunit_str()
    acct_debtor_pool_str = "debtor_respect"
    acct_debtor_pool_int = 78
    acct_debtor_pool_budatom = budatom_shop(dimen, atom_update())
    acct_debtor_pool_budatom.set_arg(acct_debtor_pool_str, acct_debtor_pool_int)

    print(f"{acct_debtor_pool_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(acct_debtor_pool_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{sue_bud.owner_name}'s debtor pool is now {acct_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_buddelta = buddelta_shop()
    dimen = budunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_debtor_pool_str = "debtor_respect"
    acct_pool_int = 83
    budunit_budatom = budatom_shop(dimen, atom_update())
    budunit_budatom.set_arg(acct_credor_pool_str, acct_pool_int)
    budunit_budatom.set_arg(acct_debtor_pool_str, acct_pool_int)
    x_buddelta.set_budatom(budunit_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{sue_bud.owner_name}'s total pool is now {acct_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = budunit_str()
    max_tree_traverse_str = "max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_budatom = budatom_shop(dimen, atom_update())
    max_tree_traverse_budatom.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(max_tree_traverse_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{sue_bud.owner_name}'s maximum number of Bud evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
