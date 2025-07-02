from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_person_membership_str,
    believer_personunit_str,
    group_title_str,
    person_name_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.delta import believerdelta_shop, get_minimal_believerdelta


def test_get_minimal_believerdelta_ReturnsObjWithoutUnecessaryINSERT_believer_personunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_personunit(yao_str)
    sue_believer.add_personunit(bob_str)

    persons_believerdelta = believerdelta_shop()
    bob_atom = believeratom_shop(believer_personunit_str(), INSERT_str())
    bob_atom.set_arg(person_name_str(), bob_str)
    yao_atom = believeratom_shop(believer_personunit_str(), INSERT_str())
    yao_atom.set_arg(person_name_str(), yao_str)
    zia_atom = believeratom_shop(believer_personunit_str(), INSERT_str())
    zia_atom.set_arg(person_name_str(), zia_str)
    persons_believerdelta.set_believeratom(bob_atom)
    persons_believerdelta.set_believeratom(yao_atom)
    persons_believerdelta.set_believeratom(zia_atom)
    assert len(persons_believerdelta.get_sorted_believeratoms()) == 3
    assert len(sue_believer.persons) == 2

    # WHEN
    new_believerdelta = get_minimal_believerdelta(persons_believerdelta, sue_believer)

    # THEN
    assert len(new_believerdelta.get_sorted_believeratoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_believer_person_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_personunit(yao_str)
    sue_believer.add_personunit(bob_str)
    yao_personunit = sue_believer.get_person(yao_str)
    run_str = ";run"
    run_str = ";run"
    yao_personunit.add_membership(run_str)
    print(f"{yao_personunit._memberships.keys()=}")

    persons_believerdelta = believerdelta_shop()
    bob_run_atom = believeratom_shop(believer_person_membership_str(), INSERT_str())
    bob_run_atom.set_arg(person_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = believeratom_shop(believer_person_membership_str(), INSERT_str())
    yao_run_atom.set_arg(person_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = believeratom_shop(believer_person_membership_str(), INSERT_str())
    zia_run_atom.set_arg(person_name_str(), zia_str)
    zia_run_atom.set_arg(group_title_str(), run_str)
    persons_believerdelta.set_believeratom(bob_run_atom)
    persons_believerdelta.set_believeratom(yao_run_atom)
    persons_believerdelta.set_believeratom(zia_run_atom)
    print(f"{len(persons_believerdelta.get_dimen_sorted_believeratoms_list())=}")
    assert len(persons_believerdelta.get_dimen_sorted_believeratoms_list()) == 3

    # WHEN
    new_believerdelta = get_minimal_believerdelta(persons_believerdelta, sue_believer)

    # THEN
    assert len(new_believerdelta.get_dimen_sorted_believeratoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
