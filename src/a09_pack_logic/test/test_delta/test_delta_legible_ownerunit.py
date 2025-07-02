from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import ownerunit_str
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import UPDATE_str
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObjEstablishWithEmptyOwnerDelta():
    # ESTABLISH / WHEN
    x_ownerdelta = ownerdelta_shop()
    sue_owner = ownerunit_shop("Sue")

    # THEN
    assert create_legible_list(x_ownerdelta, sue_owner) == []


def test_create_legible_list_ReturnsObjEstablishWithOwnerUpdate_tally():
    # ESTABLISH
    dimen = ownerunit_str()
    tally_str = "tally"
    tally_int = 55
    tally_owneratom = owneratom_shop(dimen, UPDATE_str())
    tally_owneratom.set_arg(tally_str, tally_int)
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(tally_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{sue_owner.owner_name}'s owner tally set to {tally_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithOwnerUpdate_credor_respect():
    # ESTABLISH
    dimen = ownerunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_credor_pool_int = 71
    acct_credor_pool_owneratom = owneratom_shop(dimen, UPDATE_str())
    acct_credor_pool_owneratom.set_arg(acct_credor_pool_str, acct_credor_pool_int)

    print(f"{acct_credor_pool_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(acct_credor_pool_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{sue_owner.owner_name}'s credor pool is now {acct_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithOwnerUpdate_debtor_respect():
    # ESTABLISH
    dimen = ownerunit_str()
    acct_debtor_pool_str = "debtor_respect"
    acct_debtor_pool_int = 78
    acct_debtor_pool_owneratom = owneratom_shop(dimen, UPDATE_str())
    acct_debtor_pool_owneratom.set_arg(acct_debtor_pool_str, acct_debtor_pool_int)

    print(f"{acct_debtor_pool_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(acct_debtor_pool_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{sue_owner.owner_name}'s debtor pool is now {acct_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithOwnerUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_ownerdelta = ownerdelta_shop()
    dimen = ownerunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_debtor_pool_str = "debtor_respect"
    acct_pool_int = 83
    ownerunit_owneratom = owneratom_shop(dimen, UPDATE_str())
    ownerunit_owneratom.set_arg(acct_credor_pool_str, acct_pool_int)
    ownerunit_owneratom.set_arg(acct_debtor_pool_str, acct_pool_int)
    x_ownerdelta.set_owneratom(ownerunit_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{sue_owner.owner_name}'s total pool is now {acct_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithOwnerUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = ownerunit_str()
    max_tree_traverse_str = "max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_owneratom = owneratom_shop(dimen, UPDATE_str())
    max_tree_traverse_owneratom.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(max_tree_traverse_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{sue_owner.owner_name}'s maximum number of Owner evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
