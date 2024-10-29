from src.f02_bud.bud_tool import budunit_str
from src.f04_gift.atom_config import atom_update
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.delta import deltaunit_shop
from src.f04_gift.legible import create_legible_list
from src.f02_bud.bud import budunit_shop


def test_create_legible_list_ReturnsObjEstablishWithEmptyDelta():
    # ESTABLISH / WHEN
    x_deltaunit = deltaunit_shop()
    sue_bud = budunit_shop("Sue")

    # THEN
    assert create_legible_list(x_deltaunit, sue_bud) == []


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_tally():
    # ESTABLISH
    category = budunit_str()
    tally_str = "tally"
    tally_int = 55
    tally_atomunit = atomunit_shop(category, atom_update())
    tally_atomunit.set_arg(tally_str, tally_int)
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(tally_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s bud tally set to {tally_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_purview_time_id():
    # ESTABLISH
    category = budunit_str()
    purview_time_id_str = "purview_time_id"
    purview_time_id_int = 55
    purview_time_id_atomunit = atomunit_shop(category, atom_update())
    purview_time_id_atomunit.set_arg(purview_time_id_str, purview_time_id_int)
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(purview_time_id_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s bud purview_time_id set to {purview_time_id_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_credor_respect():
    # ESTABLISH
    category = budunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_credor_pool_int = 71
    acct_credor_pool_atomunit = atomunit_shop(category, atom_update())
    acct_credor_pool_atomunit.set_arg(acct_credor_pool_str, acct_credor_pool_int)

    print(f"{acct_credor_pool_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(acct_credor_pool_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s credor pool is now {acct_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_debtor_respect():
    # ESTABLISH
    category = budunit_str()
    acct_debtor_pool_str = "debtor_respect"
    acct_debtor_pool_int = 78
    acct_debtor_pool_atomunit = atomunit_shop(category, atom_update())
    acct_debtor_pool_atomunit.set_arg(acct_debtor_pool_str, acct_debtor_pool_int)

    print(f"{acct_debtor_pool_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(acct_debtor_pool_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s debtor pool is now {acct_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_deltaunit = deltaunit_shop()
    category = budunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_debtor_pool_str = "debtor_respect"
    acct_pool_int = 83
    budunit_atomunit = atomunit_shop(category, atom_update())
    budunit_atomunit.set_arg(acct_credor_pool_str, acct_pool_int)
    budunit_atomunit.set_arg(acct_debtor_pool_str, acct_pool_int)
    x_deltaunit.set_atomunit(budunit_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s total pool is now {acct_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_max_tree_traverse():
    # ESTABLISH
    category = budunit_str()
    max_tree_traverse_str = "max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_atomunit = atomunit_shop(category, atom_update())
    max_tree_traverse_atomunit.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(max_tree_traverse_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s maximum number of Bud evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
