from src.a06_bud_logic._test_util.a06_str import (
    acct_pool_str,
    ancestors_str,
    attributes_str,
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_concept_awardlink_str,
    bud_concept_factunit_str,
    bud_concept_healerlink_str,
    bud_concept_laborlink_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_reasonunit_str,
    bud_conceptunit_str,
    budunit_str,
    credit_belief_str,
    credor_respect_str,
    debtit_belief_str,
    debtor_respect_str,
    dimen_str,
    dimens_str,
    jkeys_str,
    mandate_str,
    timeline_str,
)


def test_str_functions_ReturnsObj():
    assert acct_pool_str() == "acct_pool"
    assert credit_belief_str() == "credit_belief"
    assert credor_respect_str() == "credor_respect"
    assert debtit_belief_str() == "debtit_belief"
    assert debtor_respect_str() == "debtor_respect"
    assert budunit_str() == "budunit"
    assert bud_acct_membership_str() == "bud_acct_membership"
    assert bud_acctunit_str() == "bud_acctunit"
    assert bud_conceptunit_str() == "bud_conceptunit"
    assert bud_concept_awardlink_str() == "bud_concept_awardlink"
    assert bud_concept_reasonunit_str() == "bud_concept_reasonunit"
    assert bud_concept_reason_premiseunit_str() == "bud_concept_reason_premiseunit"
    assert bud_concept_laborlink_str() == "bud_concept_laborlink"
    assert bud_concept_healerlink_str() == "bud_concept_healerlink"
    assert bud_concept_factunit_str() == "bud_concept_factunit"
    assert jkeys_str() == "jkeys"
    assert attributes_str() == "attributes"
    assert timeline_str() == "timeline"
    assert ancestors_str() == "ancestors"
    assert mandate_str() == "mandate"
    assert dimen_str() == "dimen"
    assert dimens_str() == "dimens"
