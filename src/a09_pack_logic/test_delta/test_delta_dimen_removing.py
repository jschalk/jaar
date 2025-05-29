from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.a06_str import bud_acctunit_str, acct_name_str
from src.a08_bud_atom_logic._test_util.a08_str import INSERT_str
from src.a09_pack_logic.delta import buddelta_shop, get_dimens_cruds_buddelta


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
    after_sue_bud.set_l1_concept(conceptunit_shop("casa"))
    old_buddelta = buddelta_shop()
    old_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    dimen_set = [bud_acctunit_str()]
    curd_set = {INSERT_str()}
    new_buddelta = get_dimens_cruds_buddelta(old_buddelta, dimen_set, curd_set)

    # THEN
    new_buddelta.get_dimen_sorted_budatoms_list()
    assert len(new_buddelta.get_dimen_sorted_budatoms_list()) == 1
    sue_insert_dict = new_buddelta.budatoms.get(INSERT_str())
    sue_acctunit_dict = sue_insert_dict.get(bud_acctunit_str())
    bob_budatom = sue_acctunit_dict.get(bob_str)
    assert bob_budatom.get_value(acct_name_str()) == bob_str
    assert bob_budatom.get_value("credit_belief") == bob_credit_belief
    assert bob_budatom.get_value("debtit_belief") == bob_debtit_belief
