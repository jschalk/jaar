from src.a06_owner_logic.test._util.a06_str import (
    _keeps_buildable_str,
    _keeps_justified_str,
    _offtrack_fund_str,
    _offtrack_kids_mass_set_str,
    _rational_str,
    _reason_rcontexts_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
    acct_cred_points_str,
    acct_debt_points_str,
    acct_pool_str,
    ancestors_str,
    attributes_str,
    credor_respect_str,
    debtor_respect_str,
    dimen_str,
    dimens_str,
    jkeys_str,
    last_pack_id_str,
    mandate_str,
    max_tree_traverse_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_plan_awardlink_str,
    owner_plan_factunit_str,
    owner_plan_healerlink_str,
    owner_plan_laborlink_str,
    owner_plan_reason_premiseunit_str,
    owner_plan_reasonunit_str,
    owner_planunit_str,
    ownerunit_str,
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
    assert acct_cred_points_str() == "acct_cred_points"
    assert credor_respect_str() == "credor_respect"
    assert acct_debt_points_str() == "acct_debt_points"
    assert debtor_respect_str() == "debtor_respect"
    assert ownerunit_str() == "ownerunit"
    assert owner_acct_membership_str() == "owner_acct_membership"
    assert owner_acctunit_str() == "owner_acctunit"
    assert owner_planunit_str() == "owner_planunit"
    assert owner_plan_awardlink_str() == "owner_plan_awardlink"
    assert owner_plan_reasonunit_str() == "owner_plan_reasonunit"
    assert owner_plan_reason_premiseunit_str() == "owner_plan_reason_premiseunit"
    assert owner_plan_laborlink_str() == "owner_plan_laborlink"
    assert owner_plan_healerlink_str() == "owner_plan_healerlink"
    assert owner_plan_factunit_str() == "owner_plan_factunit"
    assert jkeys_str() == "jkeys"
    assert attributes_str() == "attributes"
    assert timeline_str() == "timeline"
    assert ancestors_str() == "ancestors"
    assert mandate_str() == "mandate"
    assert dimen_str() == "dimen"
    assert dimens_str() == "dimens"
