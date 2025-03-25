from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_favor.atom_config import acct_name_str
from src.f04_favor.atom import atom_insert
from src.f04_favor.delta import buddelta_shop, get_dimens_cruds_buddelta


def test_BudDelta_get_dimens_cruds_buddelta_ReturnsObjWithCorrectDimensAndCRUDsBy_acctunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    before_sue_bud = budunit_shop(sue_str)
    before_sue_bud.add_acctunit(yao_str)
    after_sue_bud = budunit_shop(sue_str)
    bob_str = "Bob"
    bob_credit_belief = 33
    bob_debtit_belief = 44
    after_sue_bud.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    after_sue_bud.set_l1_item(itemunit_shop("casa"))
    old_buddelta = buddelta_shop()
    old_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    dimen_set = [bud_acctunit_str()]
    curd_set = {atom_insert()}
    new_buddelta = get_dimens_cruds_buddelta(old_buddelta, dimen_set, curd_set)

    # THEN
    new_buddelta.get_dimen_sorted_budatoms_list()
    assert len(new_buddelta.get_dimen_sorted_budatoms_list()) == 1
    sue_insert_dict = new_buddelta.budatoms.get(atom_insert())
    sue_acctunit_dict = sue_insert_dict.get(bud_acctunit_str())
    bob_budatom = sue_acctunit_dict.get(bob_str)
    assert bob_budatom.get_value(acct_name_str()) == bob_str
    assert bob_budatom.get_value("credit_belief") == bob_credit_belief
    assert bob_budatom.get_value("debtit_belief") == bob_debtit_belief
