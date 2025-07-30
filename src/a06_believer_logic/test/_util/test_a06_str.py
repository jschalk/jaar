from src.a06_believer_logic.test._util.a06_str import (
    _keeps_buildable_str,
    _keeps_justified_str,
    _offtrack_fund_str,
    _offtrack_kids_star_set_str,
    _rational_str,
    _reason_contexts_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
    ancestors_str,
    attributes_str,
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_caseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
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
    penny_str,
    respect_bit_str,
    tally_str,
)


def test_str_functions_ReturnsObj():
    assert _keeps_buildable_str() == "_keeps_buildable"
    assert _keeps_justified_str() == "_keeps_justified"
    assert _offtrack_fund_str() == "_offtrack_fund"
    assert _offtrack_kids_star_set_str() == "_offtrack_kids_star_set"
    assert _rational_str() == "_rational"
    assert _reason_contexts_str() == "_reason_contexts"
    assert _sum_healerlink_share_str() == "_sum_healerlink_share"
    assert _tree_traverse_count_str() == "_tree_traverse_count"
    assert last_pack_id_str() == "last_pack_id"
    assert max_tree_traverse_str() == "max_tree_traverse"
    assert penny_str() == "penny"
    assert respect_bit_str() == "respect_bit"
    assert tally_str() == "tally"
    assert partner_pool_str() == "partner_pool"
    assert partner_cred_points_str() == "partner_cred_points"
    assert credor_respect_str() == "credor_respect"
    assert partner_debt_points_str() == "partner_debt_points"
    assert debtor_respect_str() == "debtor_respect"
    assert believerunit_str() == "believerunit"
    assert believer_partner_membership_str() == "believer_partner_membership"
    assert believer_partnerunit_str() == "believer_partnerunit"
    assert believer_planunit_str() == "believer_planunit"
    assert believer_plan_awardlink_str() == "believer_plan_awardlink"
    assert believer_plan_reasonunit_str() == "believer_plan_reasonunit"
    assert believer_plan_reason_caseunit_str() == "believer_plan_reason_caseunit"
    assert believer_plan_laborlink_str() == "believer_plan_laborlink"
    assert believer_plan_healerlink_str() == "believer_plan_healerlink"
    assert believer_plan_factunit_str() == "believer_plan_factunit"
    assert jkeys_str() == "jkeys"
    assert attributes_str() == "attributes"
    assert ancestors_str() == "ancestors"
    assert mandate_str() == "mandate"
    assert dimen_str() == "dimen"
    assert dimens_str() == "dimens"
