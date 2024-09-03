from src._road.road import get_terminus_node, get_parent_road
from src.bud.group import awardlink_shop
from src.bud.reason_idea import factunit_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.gift.atom import atom_update, atom_delete, atom_insert, atomunit_shop
from src.gift.atom_config import (
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_grouphold_text,
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
from src.gift.change import changeunit_shop
from src.gift.examples.example_changes import get_changeunit_example1


# For each of these atom_category, take a changeunit that has
# multiple atoms of delete, and remove those that are not necessary


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_acct_membership(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_acctunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_awardlink(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_factunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_grouphold(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_healerhold(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reason_premiseunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reasonunit(): assert 1==2
# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_ideaunit(): assert 1==2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_acctunit():
#     # ESTABLISH changeunit with 2 acctunits, changeunit DELETE 3 changeunits,
#     # assert changeunit has 3 atoms
#     sue_bud = budunit_shop("Sue")

#     # WHEN

#     # THEN
#     # assert changeunit has 1 atom
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_acct_membership():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_awardlink():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_factunit():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_grouphold():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_healerhold():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reason_premiseunit():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_idea_reasonunit():
#     assert 1 == 2


# def test_refine_ReturnsObjWithoutUnecessaryDELETE_bud_ideaunit():
#     assert 1 == 2
