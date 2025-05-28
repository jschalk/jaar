from src.a06_bud_logic._test_util.a06_str import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
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


def test_bud_conceptunit_str_ReturnsObj():
    assert bud_conceptunit_str() == "bud_conceptunit"


def test_bud_concept_awardlink_str_ReturnsObj():
    assert bud_concept_awardlink_str() == "bud_concept_awardlink"


def test_bud_concept_reasonunit_str_ReturnsObj():
    assert bud_concept_reasonunit_str() == "bud_concept_reasonunit"


def test_bud_concept_reason_premiseunit_str_ReturnsObj():
    assert bud_concept_reason_premiseunit_str() == "bud_concept_reason_premiseunit"


def test_bud_concept_laborlink_str_ReturnsObj():
    assert bud_concept_laborlink_str() == "bud_concept_laborlink"


def test_bud_concept_healerlink_str_ReturnsObj():
    assert bud_concept_healerlink_str() == "bud_concept_healerlink"


def test_bud_concept_factunit_str_ReturnsObj():
    assert bud_concept_factunit_str() == "bud_concept_factunit"
