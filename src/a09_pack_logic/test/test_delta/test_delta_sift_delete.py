# from src.a06_believer_logic.believer_tool import pass
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_partner_membership_str,
    believer_partnerunit_str,
    group_title_str,
    partner_name_str,
)
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import DELETE_str
from src.a09_pack_logic.delta import believerdelta_shop, get_minimal_believerdelta


def test_get_minimal_believerdelta_ReturnsObjWithoutUnecessaryDELETE_believer_partnerunit():
    # ESTABLISH believerdelta with 2 partnerunits, believerdelta DELETE 3 believerdeltas,
    # assert believerdelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)

    partners_believerdelta = believerdelta_shop()
    bob_atom = believeratom_shop(believer_partnerunit_str(), DELETE_str())
    bob_atom.set_arg(partner_name_str(), bob_str)
    yao_atom = believeratom_shop(believer_partnerunit_str(), DELETE_str())
    yao_atom.set_arg(partner_name_str(), yao_str)
    zia_atom = believeratom_shop(believer_partnerunit_str(), DELETE_str())
    zia_atom.set_arg(partner_name_str(), zia_str)
    partners_believerdelta.set_believeratom(bob_atom)
    partners_believerdelta.set_believeratom(yao_atom)
    partners_believerdelta.set_believeratom(zia_atom)
    assert len(partners_believerdelta.get_sorted_believeratoms()) == 3
    assert len(sue_believer.partners) == 2

    # WHEN
    new_believerdelta = get_minimal_believerdelta(partners_believerdelta, sue_believer)

    # THEN
    assert len(new_believerdelta.get_sorted_believeratoms()) == 2


def test_sift_ReturnsObjWithoutUnecessaryDELETE_believer_partner_membership():
    # ESTABLISH believerdelta with 2 partnerunits, believerdelta DELETE 3 believerdeltas,
    # assert believerdelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)
    yao_partnerunit = sue_believer.get_partner(yao_str)
    run_str = ";run"
    swim_str = ";swim"
    run_str = ";run"
    yao_partnerunit.add_membership(run_str)
    yao_partnerunit.add_membership(swim_str)
    print(f"{yao_partnerunit._memberships.keys()=}")

    partners_believerdelta = believerdelta_shop()
    bob_run_atom = believeratom_shop(believer_partner_membership_str(), DELETE_str())
    bob_run_atom.set_arg(partner_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = believeratom_shop(believer_partner_membership_str(), DELETE_str())
    yao_run_atom.set_arg(partner_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = believeratom_shop(believer_partner_membership_str(), DELETE_str())
    zia_run_atom.set_arg(partner_name_str(), zia_str)
    zia_run_atom.set_arg(group_title_str(), run_str)
    partners_believerdelta.set_believeratom(bob_run_atom)
    partners_believerdelta.set_believeratom(yao_run_atom)
    partners_believerdelta.set_believeratom(zia_run_atom)
    print(f"{len(partners_believerdelta.get_dimen_sorted_believeratoms_list())=}")
    assert len(partners_believerdelta.get_dimen_sorted_believeratoms_list()) == 3

    # WHEN
    new_believerdelta = get_minimal_believerdelta(partners_believerdelta, sue_believer)

    # THEN
    assert len(new_believerdelta.get_dimen_sorted_believeratoms_list()) == 1
