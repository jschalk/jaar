from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.gift.atom import atom_insert
from src.gift.atom_config import bud_acctunit_text
from src.gift.change import changeunit_shop, get_filtered_changeunit


def test_ChangeUnit_get_filtered_changeunit_ReturnsObjFilteredBy_acctunit_insert():
    # ESTABLISH
    sue_text = "Sue"
    yao_text = "Yao"
    before_sue_bud = budunit_shop(sue_text)
    before_sue_bud.add_acctunit(yao_text)
    after_sue_bud = budunit_shop(sue_text)
    bob_text = "Bob"
    bob_credit_score = 33
    bob_debtit_score = 44
    after_sue_bud.add_acctunit(bob_text, bob_credit_score, bob_debtit_score)
    after_sue_bud.set_l1_idea(ideaunit_shop("casa"))
    old_changeunit = changeunit_shop()
    old_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    category_set = [bud_acctunit_text()]
    curd_set = {atom_insert()}
    new_changeunit = get_filtered_changeunit(old_changeunit, category_set, curd_set)

    # THEN
    new_changeunit.get_category_sorted_atomunits_list()
    assert len(new_changeunit.get_category_sorted_atomunits_list()) == 1
    sue_insert_dict = new_changeunit.atomunits.get(atom_insert())
    sue_acctunit_dict = sue_insert_dict.get("bud_acctunit")
    bob_atomunit = sue_acctunit_dict.get(bob_text)
    assert bob_atomunit.get_value("acct_id") == bob_text
    assert bob_atomunit.get_value("credit_score") == bob_credit_score
    assert bob_atomunit.get_value("debtit_score") == bob_debtit_score
