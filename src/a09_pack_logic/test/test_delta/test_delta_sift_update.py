from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_personunit_str,
    person_cred_points_str,
    person_name_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import INSERT_str, UPDATE_str
from src.a09_pack_logic.delta import believerdelta_shop, get_minimal_believerdelta


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_believerdelta_ReturnsObjUPDATEBelieverAtom_believer_personunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_person_cred_points = 34
    new_bob_person_cred_points = 7
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_personunit(bob_str, old_bob_person_cred_points)
    sue_believer.add_personunit(yao_str)

    persons_believerdelta = believerdelta_shop()
    bob_atom = believeratom_shop(believer_personunit_str(), INSERT_str())
    bob_atom.set_arg(person_name_str(), bob_str)
    bob_atom.set_arg(person_cred_points_str(), new_bob_person_cred_points)
    yao_atom = believeratom_shop(believer_personunit_str(), INSERT_str())
    yao_atom.set_arg(person_name_str(), yao_str)
    persons_believerdelta.set_believeratom(bob_atom)
    persons_believerdelta.set_believeratom(yao_atom)
    assert len(persons_believerdelta.get_sorted_believeratoms()) == 2

    # WHEN
    new_believerdelta = get_minimal_believerdelta(persons_believerdelta, sue_believer)

    # THEN
    assert len(new_believerdelta.get_sorted_believeratoms()) == 1
    new_believeratom = new_believerdelta.get_sorted_believeratoms()[0]
    assert new_believeratom.crud_str == UPDATE_str()
    new_jvalues = new_believeratom.get_jvalues_dict()
    assert new_jvalues == {person_cred_points_str(): new_bob_person_cred_points}
