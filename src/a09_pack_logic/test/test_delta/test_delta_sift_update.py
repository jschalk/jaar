from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_name_str,
    plan_acctunit_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import INSERT_str, UPDATE_str
from src.a09_pack_logic.delta import get_minimal_plandelta, plandelta_shop


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_plandelta_ReturnsObjUPDATEPlanAtom_plan_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_acct_cred_points = 34
    new_bob_acct_cred_points = 7
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(bob_str, old_bob_acct_cred_points)
    sue_plan.add_acctunit(yao_str)

    accts_plandelta = plandelta_shop()
    bob_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    bob_atom.set_arg(acct_cred_points_str(), new_bob_acct_cred_points)
    yao_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    yao_atom.set_arg(acct_name_str(), yao_str)
    accts_plandelta.set_planatom(bob_atom)
    accts_plandelta.set_planatom(yao_atom)
    assert len(accts_plandelta.get_sorted_planatoms()) == 2

    # WHEN
    new_plandelta = get_minimal_plandelta(accts_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_sorted_planatoms()) == 1
    new_planatom = new_plandelta.get_sorted_planatoms()[0]
    assert new_planatom.crud_str == UPDATE_str()
    new_jvalues = new_planatom.get_jvalues_dict()
    assert new_jvalues == {acct_cred_points_str(): new_bob_acct_cred_points}
