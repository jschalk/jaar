from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_name_str,
    owner_acctunit_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import INSERT_str, UPDATE_str
from src.a09_pack_logic.delta import get_minimal_ownerdelta, ownerdelta_shop


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_ownerdelta_ReturnsObjUPDATEOwnerAtom_owner_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_acct_cred_points = 34
    new_bob_acct_cred_points = 7
    sue_owner = ownerunit_shop("Sue")
    sue_owner.add_acctunit(bob_str, old_bob_acct_cred_points)
    sue_owner.add_acctunit(yao_str)

    accts_ownerdelta = ownerdelta_shop()
    bob_atom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    bob_atom.set_arg(acct_cred_points_str(), new_bob_acct_cred_points)
    yao_atom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    yao_atom.set_arg(acct_name_str(), yao_str)
    accts_ownerdelta.set_owneratom(bob_atom)
    accts_ownerdelta.set_owneratom(yao_atom)
    assert len(accts_ownerdelta.get_sorted_owneratoms()) == 2

    # WHEN
    new_ownerdelta = get_minimal_ownerdelta(accts_ownerdelta, sue_owner)

    # THEN
    assert len(new_ownerdelta.get_sorted_owneratoms()) == 1
    new_owneratom = new_ownerdelta.get_sorted_owneratoms()[0]
    assert new_owneratom.crud_str == UPDATE_str()
    new_jvalues = new_owneratom.get_jvalues_dict()
    assert new_jvalues == {acct_cred_points_str(): new_bob_acct_cred_points}
