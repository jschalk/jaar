from src.a06_plan_logic._util.a06_str import (
    acct_name_str,
    plan_acctunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic._util.a08_str import DELETE_str, UPDATE_str
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a09_pack_logic.delta import PlanDelta, plandelta_shop


def get_plandelta_sue_example() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 77)
    sue_plandelta.set_planatom(pool_planatom)

    dimen = plan_acctunit_str()
    sue_str = "Sue"
    sue_planatom = planatom_shop(dimen, DELETE_str())
    sue_planatom.set_jkey(acct_name_str(), sue_str)
    sue_plandelta.set_planatom(sue_planatom)
    return sue_plandelta


def get_plandelta_example1() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    tally_name = "tally"
    x_planatom = planatom_shop(planunit_str(), UPDATE_str())
    x_planatom.set_jvalue(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_planatom.set_jvalue(x_attribute, 66)
    x_attribute = "credor_respect"
    x_planatom.set_jvalue(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_planatom.set_jvalue(x_attribute, 88)
    sue_plandelta.set_planatom(x_planatom)

    dimen = plan_acctunit_str()
    zia_str = "Zia"
    x_planatom = planatom_shop(dimen, DELETE_str())
    x_planatom.set_jkey(acct_name_str(), zia_str)
    sue_plandelta.set_planatom(x_planatom)
    return sue_plandelta
