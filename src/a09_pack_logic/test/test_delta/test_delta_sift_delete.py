# from src.a06_owner_logic.owner_tool import pass
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    group_title_str,
    owner_acct_membership_str,
    owner_acctunit_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import DELETE_str
from src.a09_pack_logic.delta import get_minimal_ownerdelta, ownerdelta_shop


def test_get_minimal_ownerdelta_ReturnsObjWithoutUnecessaryDELETE_owner_acctunit():
    # ESTABLISH ownerdelta with 2 acctunits, ownerdelta DELETE 3 ownerdeltas,
    # assert ownerdelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_owner = ownerunit_shop("Sue")
    sue_owner.add_acctunit(yao_str)
    sue_owner.add_acctunit(bob_str)

    accts_ownerdelta = ownerdelta_shop()
    bob_atom = owneratom_shop(owner_acctunit_str(), DELETE_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    yao_atom = owneratom_shop(owner_acctunit_str(), DELETE_str())
    yao_atom.set_arg(acct_name_str(), yao_str)
    zia_atom = owneratom_shop(owner_acctunit_str(), DELETE_str())
    zia_atom.set_arg(acct_name_str(), zia_str)
    accts_ownerdelta.set_owneratom(bob_atom)
    accts_ownerdelta.set_owneratom(yao_atom)
    accts_ownerdelta.set_owneratom(zia_atom)
    assert len(accts_ownerdelta.get_sorted_owneratoms()) == 3
    assert len(sue_owner.accts) == 2

    # WHEN
    new_ownerdelta = get_minimal_ownerdelta(accts_ownerdelta, sue_owner)

    # THEN
    assert len(new_ownerdelta.get_sorted_owneratoms()) == 2


def test_sift_ReturnsObjWithoutUnecessaryDELETE_owner_acct_membership():
    # ESTABLISH ownerdelta with 2 acctunits, ownerdelta DELETE 3 ownerdeltas,
    # assert ownerdelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_owner = ownerunit_shop("Sue")
    sue_owner.add_acctunit(yao_str)
    sue_owner.add_acctunit(bob_str)
    yao_acctunit = sue_owner.get_acct(yao_str)
    run_str = ";run"
    swim_str = ";swim"
    run_str = ";run"
    yao_acctunit.add_membership(run_str)
    yao_acctunit.add_membership(swim_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    accts_ownerdelta = ownerdelta_shop()
    bob_run_atom = owneratom_shop(owner_acct_membership_str(), DELETE_str())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = owneratom_shop(owner_acct_membership_str(), DELETE_str())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = owneratom_shop(owner_acct_membership_str(), DELETE_str())
    zia_run_atom.set_arg(acct_name_str(), zia_str)
    zia_run_atom.set_arg(group_title_str(), run_str)
    accts_ownerdelta.set_owneratom(bob_run_atom)
    accts_ownerdelta.set_owneratom(yao_run_atom)
    accts_ownerdelta.set_owneratom(zia_run_atom)
    print(f"{len(accts_ownerdelta.get_dimen_sorted_owneratoms_list())=}")
    assert len(accts_ownerdelta.get_dimen_sorted_owneratoms_list()) == 3

    # WHEN
    new_ownerdelta = get_minimal_ownerdelta(accts_ownerdelta, sue_owner)

    # THEN
    assert len(new_ownerdelta.get_dimen_sorted_owneratoms_list()) == 1
