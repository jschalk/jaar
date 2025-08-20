from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    belief_partner_membership_str,
    belief_partnerunit_str,
    group_title_str,
    partner_name_str,
)
from src.a08_belief_atom_logic.atom_main import beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.delta import beliefdelta_shop, get_minimal_beliefdelta


def test_get_minimal_beliefdelta_ReturnsObjWithoutUnecessaryINSERT_belief_partnerunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)

    partners_beliefdelta = beliefdelta_shop()
    bob_atom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    bob_atom.set_arg(partner_name_str(), bob_str)
    yao_atom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    yao_atom.set_arg(partner_name_str(), yao_str)
    zia_atom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    zia_atom.set_arg(partner_name_str(), zia_str)
    partners_beliefdelta.set_beliefatom(bob_atom)
    partners_beliefdelta.set_beliefatom(yao_atom)
    partners_beliefdelta.set_beliefatom(zia_atom)
    assert len(partners_beliefdelta.get_sorted_beliefatoms()) == 3
    assert len(sue_belief.partners) == 2

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(partners_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_sorted_beliefatoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_belief_partner_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)
    yao_partnerunit = sue_belief.get_partner(yao_str)
    run_str = ";run"
    run_str = ";run"
    yao_partnerunit.add_membership(run_str)
    print(f"{yao_partnerunit._memberships.keys()=}")

    partners_beliefdelta = beliefdelta_shop()
    bob_run_atom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
    bob_run_atom.set_arg(partner_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
    yao_run_atom.set_arg(partner_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
    zia_run_atom.set_arg(partner_name_str(), zia_str)
    zia_run_atom.set_arg(group_title_str(), run_str)
    partners_beliefdelta.set_beliefatom(bob_run_atom)
    partners_beliefdelta.set_beliefatom(yao_run_atom)
    partners_beliefdelta.set_beliefatom(zia_run_atom)
    print(f"{len(partners_beliefdelta.get_dimen_sorted_beliefatoms_list())=}")
    assert len(partners_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 3

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(partners_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
