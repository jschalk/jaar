from src.f2_bud.idea import ideaunit_shop
from src.f2_bud.bud import budunit_shop
from src.f2_bud.bud_tool import bud_acctunit_str
from src.f4_gift.atom_config import acct_id_str
from src.f4_gift.atom import atom_insert
from src.f4_gift.delta import deltaunit_shop, get_filtered_deltaunit


def test_DeltaUnit_get_filtered_deltaunit_ReturnsObjFilteredBy_acctunit_insert():
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
    after_sue_bud.set_l1_idea(ideaunit_shop("casa"))
    old_deltaunit = deltaunit_shop()
    old_deltaunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    category_set = [bud_acctunit_str()]
    curd_set = {atom_insert()}
    new_deltaunit = get_filtered_deltaunit(old_deltaunit, category_set, curd_set)

    # THEN
    new_deltaunit.get_category_sorted_atomunits_list()
    assert len(new_deltaunit.get_category_sorted_atomunits_list()) == 1
    sue_insert_dict = new_deltaunit.atomunits.get(atom_insert())
    sue_acctunit_dict = sue_insert_dict.get(bud_acctunit_str())
    bob_atomunit = sue_acctunit_dict.get(bob_str)
    assert bob_atomunit.get_value(acct_id_str()) == bob_str
    assert bob_atomunit.get_value("credit_belief") == bob_credit_belief
    assert bob_atomunit.get_value("debtit_belief") == bob_debtit_belief
