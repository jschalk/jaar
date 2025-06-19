from src.a06_plan_logic.test._util.a06_str import (
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
    credit_score_str,
    credor_respect_str,
    debt_score_str,
    debtor_respect_str,
    dimen_str,
    dimens_str,
    jkeys_str,
    last_pack_id_str,
    mandate_str,
    max_tree_traverse_str,
    penny_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    planunit_str,
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
    assert credit_score_str() == "credit_score"
    assert credor_respect_str() == "credor_respect"
    assert debt_score_str() == "debt_score"
    assert debtor_respect_str() == "debtor_respect"
    assert planunit_str() == "planunit"
    assert plan_acct_membership_str() == "plan_acct_membership"
    assert plan_acctunit_str() == "plan_acctunit"
    assert plan_conceptunit_str() == "plan_conceptunit"
    assert plan_concept_awardlink_str() == "plan_concept_awardlink"
    assert plan_concept_reasonunit_str() == "plan_concept_reasonunit"
    assert plan_concept_reason_premiseunit_str() == "plan_concept_reason_premiseunit"
    assert plan_concept_laborlink_str() == "plan_concept_laborlink"
    assert plan_concept_healerlink_str() == "plan_concept_healerlink"
    assert plan_concept_factunit_str() == "plan_concept_factunit"
    assert jkeys_str() == "jkeys"
    assert attributes_str() == "attributes"
    assert timeline_str() == "timeline"
    assert ancestors_str() == "ancestors"
    assert mandate_str() == "mandate"
    assert dimen_str() == "dimen"
    assert dimens_str() == "dimens"
