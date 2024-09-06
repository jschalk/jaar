from src.bud.bud import budunit_shop
from src.bud.bud_tool import (
    budunit_exists,
    bud_acctunit_exists,
    bud_acct_membership_exists,
    bud_ideaunit_exists,
    bud_idea_awardlink_exists,
    bud_idea_reasonunit_exists,
    bud_idea_reason_premiseunit_exists,
    bud_idea_teamlink_exists,
    bud_idea_healerhold_exists,
    bud_idea_factunit_exists,
)
from src.gift.atom import atom_update, atom_delete, atom_insert, atomunit_shop
from src.gift.atom_config import (
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_teamlink_text,
    bud_idea_healerhold_text,
    bud_idea_factunit_text,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    base_idea_active_requisite_str,
    pledge_str,
    begin_str,
    close_str,
    credit_vote_str,
    debtit_vote_str,
    gogo_want_str,
    stop_want_str,
    fopen_str,
    fnigh_str,
)
from src.gift.change import changeunit_shop, refine_changeunit
from src.gift.examples.example_changes import get_changeunit_example1


# For each of these atom_category, take a changeunit that has
# multiple atoms of delete, and remove those that are not necessary


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_acct_membership(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_acctunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_awardlink(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_factunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_teamlink(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_healerhold(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reason_premiseunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reasonunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_ideaunit(): assert 1==2


def test_refine_changeunit_ReturnsObjWithoutUnecessaryDELETE_bud_acctunit():
    # ESTABLISH changeunit with 2 acctunits, changeunit DELETE 3 changeunits,
    # assert changeunit has 3 atoms
    bob_text = "Bob"
    yao_text = "Yao"
    zia_text = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_text)
    sue_bud.add_acctunit(bob_text)

    accts_changeunit = changeunit_shop()
    bob_atom = atomunit_shop(bud_acctunit_text(), atom_delete())
    bob_atom.set_arg(acct_id_str(), bob_text)
    yao_atom = atomunit_shop(bud_acctunit_text(), atom_delete())
    yao_atom.set_arg(acct_id_str(), yao_text)
    zia_atom = atomunit_shop(bud_acctunit_text(), atom_delete())
    zia_atom.set_arg(acct_id_str(), zia_text)
    accts_changeunit.set_atomunit(bob_atom)
    accts_changeunit.set_atomunit(yao_atom)
    accts_changeunit.set_atomunit(zia_atom)
    assert len(accts_changeunit.get_sorted_atomunits()) == 3
    assert len(sue_bud._accts) == 2

    # WHEN
    new_changeunit = refine_changeunit(accts_changeunit, sue_bud)

    # THEN
    assert len(new_changeunit.get_sorted_atomunits()) == 2


def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_acct_membership():
    # ESTABLISH changeunit with 2 acctunits, changeunit DELETE 3 changeunits,
    # assert changeunit has 3 atoms
    bob_text = "Bob"
    yao_text = "Yao"
    zia_text = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_text)
    sue_bud.add_acctunit(bob_text)
    yao_acctunit = sue_bud.get_acct(yao_text)
    bob_acctunit = sue_bud.get_acct(bob_text)
    zia_acctunit = sue_bud.get_acct(zia_text)
    run_text = ";run"
    swim_text = ";swim"
    run_text = ";run"
    yao_acctunit.add_membership(run_text)
    yao_acctunit.add_membership(swim_text)
    print(f"{yao_acctunit._memberships.keys()=}")

    accts_changeunit = changeunit_shop()
    bob_run_atom = atomunit_shop(bud_acct_membership_text(), atom_delete())
    bob_run_atom.set_arg(acct_id_str(), bob_text)
    bob_run_atom.set_arg(group_id_str(), run_text)
    yao_run_atom = atomunit_shop(bud_acct_membership_text(), atom_delete())
    yao_run_atom.set_arg(acct_id_str(), yao_text)
    yao_run_atom.set_arg(group_id_str(), run_text)
    zia_run_atom = atomunit_shop(bud_acct_membership_text(), atom_delete())
    zia_run_atom.set_arg(acct_id_str(), zia_text)
    zia_run_atom.set_arg(group_id_str(), run_text)
    accts_changeunit.set_atomunit(bob_run_atom)
    accts_changeunit.set_atomunit(yao_run_atom)
    accts_changeunit.set_atomunit(zia_run_atom)
    print(f"{len(accts_changeunit.get_category_sorted_atomunits_list())=}")
    assert len(accts_changeunit.get_category_sorted_atomunits_list()) == 3
    assert bud_acct_membership_exists(sue_bud, yao_text, run_text)
    assert bud_acct_membership_exists(sue_bud, yao_text, swim_text)
    assert not bud_acct_membership_exists(sue_bud, bob_text, swim_text)
    assert not bud_acct_membership_exists(sue_bud, zia_text, swim_text)

    # WHEN
    new_changeunit = refine_changeunit(accts_changeunit, sue_bud)

    # THEN
    assert len(new_changeunit.get_category_sorted_atomunits_list()) == 1


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_awardlink():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_factunit():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_teamlink():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_healerhold():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reason_premiseunit():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reasonunit():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_ideaunit():
#     assert 1 == 2
