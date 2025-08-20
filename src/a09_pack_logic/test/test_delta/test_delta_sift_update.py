from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    belief_partnerunit_str,
    partner_cred_points_str,
    partner_name_str,
)
from src.a08_belief_atom_logic.atom_main import beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import INSERT_str, UPDATE_str
from src.a09_pack_logic.delta import beliefdelta_shop, get_minimal_beliefdelta


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_beliefdelta_ReturnsObjUPDATEBeliefAtom_belief_partnerunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_partner_cred_points = 34
    new_bob_partner_cred_points = 7
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(bob_str, old_bob_partner_cred_points)
    sue_belief.add_partnerunit(yao_str)

    partners_beliefdelta = beliefdelta_shop()
    bob_atom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    bob_atom.set_arg(partner_name_str(), bob_str)
    bob_atom.set_arg(partner_cred_points_str(), new_bob_partner_cred_points)
    yao_atom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    yao_atom.set_arg(partner_name_str(), yao_str)
    partners_beliefdelta.set_beliefatom(bob_atom)
    partners_beliefdelta.set_beliefatom(yao_atom)
    assert len(partners_beliefdelta.get_sorted_beliefatoms()) == 2

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(partners_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_sorted_beliefatoms()) == 1
    new_beliefatom = new_beliefdelta.get_sorted_beliefatoms()[0]
    assert new_beliefatom.crud_str == UPDATE_str()
    new_jvalues = new_beliefatom.get_jvalues_dict()
    assert new_jvalues == {partner_cred_points_str(): new_bob_partner_cred_points}
