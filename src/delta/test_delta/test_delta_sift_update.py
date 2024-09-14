from src.bud.bud import budunit_shop
from src.bud.bud_tool import bud_acctunit_str
from src.delta.atom import atom_insert, atom_update, atomunit_shop
from src.delta.atom_config import acct_id_str, credit_belief_str
from src.delta.delta import deltaunit_shop, sift_deltaunit


# all other atom categorys are covered by test_sift_atom tests
def test_sift_deltaunit_ReturnsObjUPDATEAtomUnit_bud_acctunit():
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
    bob_atom.set_arg(acct_id_str(), bob_str)
    bob_atom.set_arg(credit_belief_str(), new_bob_credit_belief)
    yao_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    yao_atom.set_arg(acct_id_str(), yao_str)
    accts_deltaunit.set_atomunit(bob_atom)
    accts_deltaunit.set_atomunit(yao_atom)
    assert len(accts_deltaunit.get_sorted_atomunits()) == 2

    # WHEN
    new_deltaunit = sift_deltaunit(accts_deltaunit, sue_bud)

    # THEN
    assert len(new_deltaunit.get_sorted_atomunits()) == 1
    new_atomunit = new_deltaunit.get_sorted_atomunits()[0]
    assert new_atomunit.crud_str == atom_update()
    new_optional_args = new_atomunit.get_optional_args_dict()
    assert new_optional_args == {credit_belief_str(): new_bob_credit_belief}
