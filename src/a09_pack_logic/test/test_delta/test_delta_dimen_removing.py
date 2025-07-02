from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import acct_name_str, owner_acctunit_str
from src.a08_owner_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.delta import get_dimens_cruds_ownerdelta, ownerdelta_shop


def test_OwnerDelta_get_dimens_cruds_ownerdelta_ReturnsObjWithCorrectDimensAndCRUDsBy_acctunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    before_sue_owner = ownerunit_shop(sue_str)
    before_sue_owner.add_acctunit(yao_str)
    after_sue_owner = ownerunit_shop(sue_str)
    bob_str = "Bob"
    bob_acct_cred_points = 33
    bob_acct_debt_points = 44
    after_sue_owner.add_acctunit(bob_str, bob_acct_cred_points, bob_acct_debt_points)
    after_sue_owner.set_l1_concept(conceptunit_shop("casa"))
    old_ownerdelta = ownerdelta_shop()
    old_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    dimen_set = [owner_acctunit_str()]
    curd_set = {INSERT_str()}
    new_ownerdelta = get_dimens_cruds_ownerdelta(old_ownerdelta, dimen_set, curd_set)

    # THEN
    new_ownerdelta.get_dimen_sorted_owneratoms_list()
    assert len(new_ownerdelta.get_dimen_sorted_owneratoms_list()) == 1
    sue_insert_dict = new_ownerdelta.owneratoms.get(INSERT_str())
    sue_acctunit_dict = sue_insert_dict.get(owner_acctunit_str())
    bob_owneratom = sue_acctunit_dict.get(bob_str)
    assert bob_owneratom.get_value(acct_name_str()) == bob_str
    assert bob_owneratom.get_value("acct_cred_points") == bob_acct_cred_points
    assert bob_owneratom.get_value("acct_debt_points") == bob_acct_debt_points
