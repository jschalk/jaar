from src.f2_bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
)


def test_budunit_str_ReturnsObj():
    assert budunit_str() == "budunit"


def test_bud_acctunit_str_ReturnsObj():
    assert bud_acctunit_str() == "bud_acctunit"


def test_bud_acct_membership_str_ReturnsObj():
    assert bud_acct_membership_str() == "bud_acct_membership"


def test_bud_ideaunit_str_ReturnsObj():
    assert bud_ideaunit_str() == "bud_ideaunit"


def test_bud_idea_awardlink_str_ReturnsObj():
    assert bud_idea_awardlink_str() == "bud_idea_awardlink"


def test_bud_idea_reasonunit_str_ReturnsObj():
    assert bud_idea_reasonunit_str() == "bud_idea_reasonunit"


def test_bud_idea_reason_premiseunit_str_ReturnsObj():
    assert bud_idea_reason_premiseunit_str() == "bud_idea_reason_premiseunit"


def test_bud_idea_teamlink_str_ReturnsObj():
    assert bud_idea_teamlink_str() == "bud_idea_teamlink"


def test_bud_idea_healerlink_str_ReturnsObj():
    assert bud_idea_healerlink_str() == "bud_idea_healerlink"


def test_bud_idea_factunit_str_ReturnsObj():
    assert bud_idea_factunit_str() == "bud_idea_factunit"
