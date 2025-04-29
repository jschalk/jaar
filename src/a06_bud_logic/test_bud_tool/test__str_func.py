from src.a06_bud_logic._utils.a06_str_helpers import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
    bud_groupunit_str,
)


def test_budunit_str_ReturnsObj():
    assert budunit_str() == "budunit"


def test_bud_acctunit_str_ReturnsObj():
    assert bud_acctunit_str() == "bud_acctunit"


def test_bud_acct_membership_str_ReturnsObj():
    assert bud_acct_membership_str() == "bud_acct_membership"


def test_bud_groupunit_str_ReturnsObj():
    assert bud_groupunit_str() == "bud_groupunit"


def test_bud_itemunit_str_ReturnsObj():
    assert bud_itemunit_str() == "bud_itemunit"


def test_bud_item_awardlink_str_ReturnsObj():
    assert bud_item_awardlink_str() == "bud_item_awardlink"


def test_bud_item_reasonunit_str_ReturnsObj():
    assert bud_item_reasonunit_str() == "bud_item_reasonunit"


def test_bud_item_reason_premiseunit_str_ReturnsObj():
    assert bud_item_reason_premiseunit_str() == "bud_item_reason_premiseunit"


def test_bud_item_teamlink_str_ReturnsObj():
    assert bud_item_teamlink_str() == "bud_item_teamlink"


def test_bud_item_healerlink_str_ReturnsObj():
    assert bud_item_healerlink_str() == "bud_item_healerlink"


def test_bud_item_factunit_str_ReturnsObj():
    assert bud_item_factunit_str() == "bud_item_factunit"
