from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_pack.atom import atom_insert, atom_update, budatom_shop
from src.f04_pack.atom_config import acct_name_str, credit_belief_str
from src.f04_pack.delta import buddelta_shop, get_minimal_buddelta


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_buddelta_ReturnsObjUPDATEBudAtom_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_credit_belief = 34
    new_bob_credit_belief = 7
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(bob_str, old_bob_credit_belief)
    sue_bud.add_acctunit(yao_str)

    accts_buddelta = buddelta_shop()
    bob_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    bob_atom.set_arg(acct_name_str(), bob_str)
    bob_atom.set_arg(credit_belief_str(), new_bob_credit_belief)
    yao_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    yao_atom.set_arg(acct_name_str(), yao_str)
    accts_buddelta.set_budatom(bob_atom)
    accts_buddelta.set_budatom(yao_atom)
    assert len(accts_buddelta.get_sorted_budatoms()) == 2

    # WHEN
    new_buddelta = get_minimal_buddelta(accts_buddelta, sue_bud)

    # THEN
    assert len(new_buddelta.get_sorted_budatoms()) == 1
    new_budatom = new_buddelta.get_sorted_budatoms()[0]
    assert new_budatom.crud_str == atom_update()
    new_jvalues = new_budatom.get_jvalues_dict()
    assert new_jvalues == {credit_belief_str(): new_bob_credit_belief}
