from src.a06_bud_logic.bud import budunit_shop

# from src.a06_bud_logic.bud_tool import pass
from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    bud_acct_membership_str,
    acct_name_str,
    group_title_str,
)
from src.a08_bud_atom_logic.atom import atom_delete, budatom_shop
from src.a09_pack_logic.delta import buddelta_shop, get_minimal_buddelta


def test_get_minimal_buddelta_ReturnsObjWithoutUnecessaryDELETE_bud_acctunit():
    # ESTABLISH buddelta with 2 acctunits, buddelta DELETE 3 buddeltas,
    # assert buddelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)

    accts_buddelta = buddelta_shop()
    bob_atom = budatom_shop(bud_acctunit_str(), atom_delete())
    bob_atom.set_arg(acct_name_str(), bob_str)
    yao_atom = budatom_shop(bud_acctunit_str(), atom_delete())
    yao_atom.set_arg(acct_name_str(), yao_str)
    zia_atom = budatom_shop(bud_acctunit_str(), atom_delete())
    zia_atom.set_arg(acct_name_str(), zia_str)
    accts_buddelta.set_budatom(bob_atom)
    accts_buddelta.set_budatom(yao_atom)
    accts_buddelta.set_budatom(zia_atom)
    assert len(accts_buddelta.get_sorted_budatoms()) == 3
    assert len(sue_bud.accts) == 2

    # WHEN
    new_buddelta = get_minimal_buddelta(accts_buddelta, sue_bud)

    # THEN
    assert len(new_buddelta.get_sorted_budatoms()) == 2


def test_sift_ReturnsObjWithoutUnecessaryDELETE_bud_acct_membership():
    # ESTABLISH buddelta with 2 acctunits, buddelta DELETE 3 buddeltas,
    # assert buddelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    yao_acctunit = sue_bud.get_acct(yao_str)
    run_str = ";run"
    swim_str = ";swim"
    run_str = ";run"
    yao_acctunit.add_membership(run_str)
    yao_acctunit.add_membership(swim_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    accts_buddelta = buddelta_shop()
    bob_run_atom = budatom_shop(bud_acct_membership_str(), atom_delete())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = budatom_shop(bud_acct_membership_str(), atom_delete())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = budatom_shop(bud_acct_membership_str(), atom_delete())
    zia_run_atom.set_arg(acct_name_str(), zia_str)
    zia_run_atom.set_arg(group_title_str(), run_str)
    accts_buddelta.set_budatom(bob_run_atom)
    accts_buddelta.set_budatom(yao_run_atom)
    accts_buddelta.set_budatom(zia_run_atom)
    print(f"{len(accts_buddelta.get_dimen_sorted_budatoms_list())=}")
    assert len(accts_buddelta.get_dimen_sorted_budatoms_list()) == 3

    # WHEN
    new_buddelta = get_minimal_buddelta(accts_buddelta, sue_bud)

    # THEN
    assert len(new_buddelta.get_dimen_sorted_budatoms_list()) == 1
