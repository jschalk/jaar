from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    acct_name_str,
    believer_acct_membership_str,
    believer_acctunit_str,
    group_title_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.delta import believerdelta_shop, get_minimal_believerdelta


def test_get_minimal_believerdelta_ReturnsObjWithoutUnecessaryINSERT_believer_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_acctunit(yao_str)
    sue_believer.add_acctunit(bob_str)

    accts_believerdelta = believerdelta_shop()
    bob_atom = believeratom_shop(believer_acctunit_str(), INSERT_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    yao_atom = believeratom_shop(believer_acctunit_str(), INSERT_str())
    yao_atom.set_arg(acct_name_str(), yao_str)
    zia_atom = believeratom_shop(believer_acctunit_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)
    accts_believerdelta.set_believeratom(bob_atom)
    accts_believerdelta.set_believeratom(yao_atom)
    accts_believerdelta.set_believeratom(zia_atom)
    assert len(accts_believerdelta.get_sorted_believeratoms()) == 3
    assert len(sue_believer.accts) == 2

    # WHEN
    new_believerdelta = get_minimal_believerdelta(accts_believerdelta, sue_believer)

    # THEN
    assert len(new_believerdelta.get_sorted_believeratoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_believer_acct_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_acctunit(yao_str)
    sue_believer.add_acctunit(bob_str)
    yao_acctunit = sue_believer.get_acct(yao_str)
    run_str = ";run"
    run_str = ";run"
    yao_acctunit.add_membership(run_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    accts_believerdelta = believerdelta_shop()
    bob_run_atom = believeratom_shop(believer_acct_membership_str(), INSERT_str())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = believeratom_shop(believer_acct_membership_str(), INSERT_str())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)
    zia_run_atom = believeratom_shop(believer_acct_membership_str(), INSERT_str())
    zia_run_atom.set_arg(acct_name_str(), zia_str)
    zia_run_atom.set_arg(group_title_str(), run_str)
    accts_believerdelta.set_believeratom(bob_run_atom)
    accts_believerdelta.set_believeratom(yao_run_atom)
    accts_believerdelta.set_believeratom(zia_run_atom)
    print(f"{len(accts_believerdelta.get_dimen_sorted_believeratoms_list())=}")
    assert len(accts_believerdelta.get_dimen_sorted_believeratoms_list()) == 3

    # WHEN
    new_believerdelta = get_minimal_believerdelta(accts_believerdelta, sue_believer)

    # THEN
    assert len(new_believerdelta.get_dimen_sorted_believeratoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
