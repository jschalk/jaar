from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_gift.atom import atom_insert, atom_update, atomunit_shop
from src.f04_gift.atom_config import acct_name_str, credit_belief_str
from src.f04_gift.delta import deltaunit_shop, get_minimal_deltaunit


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_deltaunit_ReturnsObjUPDATEAtomUnit_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_credit_belief = 34
    new_bob_credit_belief = 7
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(bob_str, old_bob_credit_belief)
    sue_bud.add_acctunit(yao_str)

    accts_deltaunit = deltaunit_shop()
    bob_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    bob_atom.set_arg(acct_name_str(), bob_str)
    bob_atom.set_arg(credit_belief_str(), new_bob_credit_belief)
    yao_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    yao_atom.set_arg(acct_name_str(), yao_str)
    accts_deltaunit.set_atomunit(bob_atom)
    accts_deltaunit.set_atomunit(yao_atom)
    assert len(accts_deltaunit.get_sorted_atomunits()) == 2

    # WHEN
    new_deltaunit = get_minimal_deltaunit(accts_deltaunit, sue_bud)

    # THEN
    assert len(new_deltaunit.get_sorted_atomunits()) == 1
    new_atomunit = new_deltaunit.get_sorted_atomunits()[0]
    assert new_atomunit.crud_str == atom_update()
    new_jvalues = new_atomunit.get_jvalues_dict()
    assert new_jvalues == {credit_belief_str(): new_bob_credit_belief}
