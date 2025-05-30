from src.a06_bud_logic._test_util.a06_str import (
    _keeps_buildable_str,
    _keeps_justified_str,
    _offtrack_fund_str,
    _offtrack_kids_mass_set_str,
    _rational_str,
    _reason_rcontexts_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
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
    last_pack_id_str,
    mandate_str,
    max_tree_traverse_str,
    penny_str,
    respect_bit_str,
    tally_str,
    timeline_str,
)


def test_str_functions_ReturnsObj():
    assert _keeps_buildable_str() == "_keeps_buildable"
    assert _keeps_justified_str() == "_keeps_justified"
    assert _offtrack_fund_str() == "_offtrack_fund"
    assert _offtrack_kids_mass_set_str() == "_offtrack_kids_mass_set"
    assert _rational_str() == "_rational"
    assert _reason_rcontexts_str() == "_reason_rcontexts"
    assert _sum_healerlink_share_str() == "_sum_healerlink_share"
    assert _tree_traverse_count_str() == "_tree_traverse_count"
    assert last_pack_id_str() == "last_pack_id"
    assert max_tree_traverse_str() == "max_tree_traverse"
    assert penny_str() == "penny"
    assert respect_bit_str() == "respect_bit"
    assert tally_str() == "tally"
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
