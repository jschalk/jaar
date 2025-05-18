from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    bud_acct_membership_str,
    acct_name_str,
    group_title_str,
)
from src.a08_bud_atom_logic.atom import atom_insert, budatom_shop
from src.a09_pack_logic.delta import buddelta_shop, get_minimal_buddelta


def test_get_minimal_buddelta_ReturnsObjWithoutUnecessaryINSERT_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)

    accts_buddelta = buddelta_shop()
    bob_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    bob_atom.set_arg(acct_name_str(), bob_str)
    yao_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    yao_atom.set_arg(acct_name_str(), yao_str)
    zia_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    zia_atom.set_arg(acct_name_str(), zia_str)
    accts_buddelta.set_budatom(bob_atom)
    accts_buddelta.set_budatom(yao_atom)
    accts_buddelta.set_budatom(zia_atom)
    assert len(accts_buddelta.get_sorted_budatoms()) == 3
    assert len(sue_bud.accts) == 2

    # WHEN
    new_buddelta = get_minimal_buddelta(accts_buddelta, sue_bud)

    # THEN
    assert len(new_buddelta.get_sorted_budatoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_bud_acct_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    yao_acctunit = sue_bud.get_acct(yao_str)
    run_str = ";run"
    run_str = ";run"
    yao_acctunit.add_membership(run_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    accts_buddelta = buddelta_shop()
    bob_run_atom = budatom_shop(bud_acct_membership_str(), atom_insert())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = budatom_shop(bud_acct_membership_str(), atom_insert())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = budatom_shop(bud_acct_membership_str(), atom_insert())
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
    assert len(new_buddelta.get_dimen_sorted_budatoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
