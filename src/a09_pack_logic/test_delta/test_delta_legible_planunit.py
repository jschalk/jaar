from src.a06_plan_logic._test_util.a06_str import planunit_str
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._test_util.a08_str import UPDATE_str
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObjEstablishWithEmptyPlanDelta():
    # ESTABLISH / WHEN
    x_plandelta = plandelta_shop()
    sue_plan = planunit_shop("Sue")

    # THEN
    assert create_legible_list(x_plandelta, sue_plan) == []


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_tally():
    # ESTABLISH
    dimen = planunit_str()
    tally_str = "tally"
    tally_int = 55
    tally_planatom = planatom_shop(dimen, UPDATE_str())
    tally_planatom.set_arg(tally_str, tally_int)
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(tally_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.owner_name}'s plan tally set to {tally_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_credor_respect():
    # ESTABLISH
    dimen = planunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_credor_pool_int = 71
    acct_credor_pool_planatom = planatom_shop(dimen, UPDATE_str())
    acct_credor_pool_planatom.set_arg(acct_credor_pool_str, acct_credor_pool_int)

    print(f"{acct_credor_pool_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(acct_credor_pool_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.owner_name}'s credor pool is now {acct_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_debtor_respect():
    # ESTABLISH
    dimen = planunit_str()
    acct_debtor_pool_str = "debtor_respect"
    acct_debtor_pool_int = 78
    acct_debtor_pool_planatom = planatom_shop(dimen, UPDATE_str())
    acct_debtor_pool_planatom.set_arg(acct_debtor_pool_str, acct_debtor_pool_int)

    print(f"{acct_debtor_pool_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(acct_debtor_pool_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.owner_name}'s debtor pool is now {acct_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_plandelta = plandelta_shop()
    dimen = planunit_str()
    acct_credor_pool_str = "credor_respect"
    acct_debtor_pool_str = "debtor_respect"
    acct_pool_int = 83
    planunit_planatom = planatom_shop(dimen, UPDATE_str())
    planunit_planatom.set_arg(acct_credor_pool_str, acct_pool_int)
    planunit_planatom.set_arg(acct_debtor_pool_str, acct_pool_int)
    x_plandelta.set_planatom(planunit_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.owner_name}'s total pool is now {acct_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = planunit_str()
    max_tree_traverse_str = "max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_planatom = planatom_shop(dimen, UPDATE_str())
    max_tree_traverse_planatom.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(max_tree_traverse_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.owner_name}'s maximum number of Plan evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
