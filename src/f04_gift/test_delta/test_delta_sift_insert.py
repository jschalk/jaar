from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import bud_acctunit_str, bud_acct_membership_str
from src.f04_gift.atom import atom_insert, atomunit_shop
from src.f04_gift.atom_config import acct_name_str, group_label_str
from src.f04_gift.delta import deltaunit_shop, get_minimal_deltaunit


def test_get_minimal_deltaunit_ReturnsObjWithoutUnecessaryINSERT_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)

    accts_deltaunit = deltaunit_shop()
    bob_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    bob_atom.set_arg(acct_name_str(), bob_str)
    yao_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    yao_atom.set_arg(acct_name_str(), yao_str)
    zia_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    zia_atom.set_arg(acct_name_str(), zia_str)
    accts_deltaunit.set_atomunit(bob_atom)
    accts_deltaunit.set_atomunit(yao_atom)
    accts_deltaunit.set_atomunit(zia_atom)
    assert len(accts_deltaunit.get_sorted_atomunits()) == 3
    assert len(sue_bud.accts) == 2

    # WHEN
    new_deltaunit = get_minimal_deltaunit(accts_deltaunit, sue_bud)

    # THEN
    assert len(new_deltaunit.get_sorted_atomunits()) == 1


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

    accts_deltaunit = deltaunit_shop()
    bob_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_label_str(), run_str)
    yao_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_label_str(), run_str)
    zia_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
    zia_run_atom.set_arg(acct_name_str(), zia_str)
    zia_run_atom.set_arg(group_label_str(), run_str)
    accts_deltaunit.set_atomunit(bob_run_atom)
    accts_deltaunit.set_atomunit(yao_run_atom)
    accts_deltaunit.set_atomunit(zia_run_atom)
    print(f"{len(accts_deltaunit.get_dimen_sorted_atomunits_list())=}")
    assert len(accts_deltaunit.get_dimen_sorted_atomunits_list()) == 3

    # WHEN
    new_deltaunit = get_minimal_deltaunit(accts_deltaunit, sue_bud)

    # THEN
    assert len(new_deltaunit.get_dimen_sorted_atomunits_list()) == 2


# all atom dimens are covered by "sift_atom" tests
