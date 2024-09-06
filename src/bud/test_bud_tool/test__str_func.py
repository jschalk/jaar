from src.bud.bud_tool import (
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_teamlink_text,
    bud_idea_healerlink_text,
    bud_idea_factunit_text,
)


def test_budunit_text_ReturnsObj():
    assert budunit_text() == "budunit"


def test_bud_acctunit_text_ReturnsObj():
    assert bud_acctunit_text() == "bud_acctunit"


def test_bud_acct_membership_text_ReturnsObj():
    assert bud_acct_membership_text() == "bud_acct_membership"


def test_bud_ideaunit_text_ReturnsObj():
    assert bud_ideaunit_text() == "bud_ideaunit"


def test_bud_idea_awardlink_text_ReturnsObj():
    assert bud_idea_awardlink_text() == "bud_idea_awardlink"


def test_bud_idea_reasonunit_text_ReturnsObj():
    assert bud_idea_reasonunit_text() == "bud_idea_reasonunit"


def test_bud_idea_reason_premiseunit_text_ReturnsObj():
    assert bud_idea_reason_premiseunit_text() == "bud_idea_reason_premiseunit"


def test_bud_idea_teamlink_text_ReturnsObj():
    assert bud_idea_teamlink_text() == "bud_idea_teamlink"


def test_bud_idea_healerlink_text_ReturnsObj():
    assert bud_idea_healerlink_text() == "bud_idea_healerlink"


def test_bud_idea_factunit_text_ReturnsObj():
    assert bud_idea_factunit_text() == "bud_idea_factunit"
