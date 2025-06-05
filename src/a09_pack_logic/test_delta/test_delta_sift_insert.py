from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    group_title_str,
    plan_acct_membership_str,
    plan_acctunit_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._test_util.a08_str import INSERT_str
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a09_pack_logic.delta import get_minimal_plandelta, plandelta_shop


def test_get_minimal_plandelta_ReturnsObjWithoutUnecessaryINSERT_plan_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)

    accts_plandelta = plandelta_shop()
    bob_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    yao_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    yao_atom.set_arg(acct_name_str(), yao_str)
    zia_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)
    accts_plandelta.set_planatom(bob_atom)
    accts_plandelta.set_planatom(yao_atom)
    accts_plandelta.set_planatom(zia_atom)
    assert len(accts_plandelta.get_sorted_planatoms()) == 3
    assert len(sue_plan.accts) == 2

    # WHEN
    new_plandelta = get_minimal_plandelta(accts_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_sorted_planatoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_plan_acct_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)
    yao_acctunit = sue_plan.get_acct(yao_str)
    run_str = ";run"
    run_str = ";run"
    yao_acctunit.add_membership(run_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    accts_plandelta = plandelta_shop()
    bob_run_atom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    zia_run_atom.set_arg(acct_name_str(), zia_str)
    zia_run_atom.set_arg(group_title_str(), run_str)
    accts_plandelta.set_planatom(bob_run_atom)
    accts_plandelta.set_planatom(yao_run_atom)
    accts_plandelta.set_planatom(zia_run_atom)
    print(f"{len(accts_plandelta.get_dimen_sorted_planatoms_list())=}")
    assert len(accts_plandelta.get_dimen_sorted_planatoms_list()) == 3

    # WHEN
    new_plandelta = get_minimal_plandelta(accts_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_dimen_sorted_planatoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
