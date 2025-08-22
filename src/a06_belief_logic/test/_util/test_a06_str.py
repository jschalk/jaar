from src.a06_belief_logic.test._util.a06_str import (
    _groupunits_str,
    _keeps_buildable_str,
    _keeps_justified_str,
    _offtrack_fund_str,
    _offtrack_kids_star_set_str,
    _rational_str,
    _reason_contexts_str,
    _sum_healerunit_share_str,
    _tree_traverse_count_str,
    ancestors_str,
    attributes_str,
    belief_partner_membership_str,
    belief_partnerunit_str,
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    beliefunit_str,
    credor_respect_str,
    debtor_respect_str,
    dimen_str,
    dimens_str,
    jkeys_str,
    last_pack_id_str,
    mandate_str,
    max_tree_traverse_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_pool_str,
    partners_str,
    penny_str,
    planroot_str,
    respect_bit_str,
    tally_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert _groupunits_str() == "_groupunits"
    assert _keeps_buildable_str() == "_keeps_buildable"
    assert _keeps_justified_str() == "_keeps_justified"
    assert _offtrack_fund_str() == "_offtrack_fund"
    assert _offtrack_kids_star_set_str() == "_offtrack_kids_star_set"
    assert _rational_str() == "_rational"
    assert _reason_contexts_str() == "_reason_contexts"
    assert _sum_healerunit_share_str() == "_sum_healerunit_share"
    assert _tree_traverse_count_str() == "_tree_traverse_count"
    assert last_pack_id_str() == "last_pack_id"
    assert max_tree_traverse_str() == "max_tree_traverse"
    assert penny_str() == "penny"
    assert respect_bit_str() == "respect_bit"
    assert tally_str() == "tally"
    assert planroot_str() == "planroot"
    assert partner_pool_str() == "partner_pool"
    assert partner_cred_points_str() == "partner_cred_points"
    assert partners_str() == "partners"
    assert credor_respect_str() == "credor_respect"
    assert partner_debt_points_str() == "partner_debt_points"
    assert debtor_respect_str() == "debtor_respect"
    assert beliefunit_str() == "beliefunit"
    assert belief_partner_membership_str() == "belief_partner_membership"
    assert belief_partnerunit_str() == "belief_partnerunit"
    assert belief_planunit_str() == "belief_planunit"
    assert belief_plan_awardunit_str() == "belief_plan_awardunit"
    assert belief_plan_reasonunit_str() == "belief_plan_reasonunit"
    assert belief_plan_reason_caseunit_str() == "belief_plan_reason_caseunit"
    assert belief_plan_partyunit_str() == "belief_plan_partyunit"
    assert belief_plan_healerunit_str() == "belief_plan_healerunit"
    assert belief_plan_factunit_str() == "belief_plan_factunit"
    assert jkeys_str() == "jkeys"
    assert attributes_str() == "attributes"
    assert ancestors_str() == "ancestors"
    assert mandate_str() == "mandate"
    assert dimen_str() == "dimen"
    assert dimens_str() == "dimens"
