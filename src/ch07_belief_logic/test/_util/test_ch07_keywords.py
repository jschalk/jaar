from src.ch07_belief_logic._ref.ch07_keywords import (
    BeliefName_str,
    Ch03Keywords as wx,
    Ch07Keywords,
    ancestors_str,
    attributes_str,
    belief_groupunit_str,
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    belief_voice_membership_str,
    belief_voiceunit_str,
    beliefunit_str,
    class_type_str,
    credor_respect_str,
    debtor_respect_str,
    dimen_str,
    dimens_str,
    jkeys_str,
    jvalues_str,
    keeps_buildable_str,
    keeps_justified_str,
    last_pack_id_str,
    mandate_str,
    max_tree_traverse_str,
    offtrack_fund_str,
    offtrack_kids_star_set_str,
    planroot_str,
    reason_contexts_str,
    respect_bit_str,
    sum_healerunit_share_str,
    tally_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_pool_str,
    voices_str,
)


def test_Ch07Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch07Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert attributes_str() == "attributes"
    assert ancestors_str() == "ancestors"
    assert beliefunit_str() == "beliefunit"
    assert belief_groupunit_str() == "belief_groupunit"
    assert belief_voice_membership_str() == "belief_voice_membership"
    assert belief_voiceunit_str() == "belief_voiceunit"
    assert belief_planunit_str() == "belief_planunit"
    assert belief_plan_awardunit_str() == "belief_plan_awardunit"
    assert belief_plan_reasonunit_str() == "belief_plan_reasonunit"
    assert belief_plan_reason_caseunit_str() == "belief_plan_reason_caseunit"
    assert belief_plan_partyunit_str() == "belief_plan_partyunit"
    assert belief_plan_healerunit_str() == "belief_plan_healerunit"
    assert belief_plan_factunit_str() == "belief_plan_factunit"
    assert BeliefName_str() == "BeliefName"
    assert class_type_str() == "class_type"
    assert credor_respect_str() == "credor_respect"
    assert debtor_respect_str() == "debtor_respect"
    assert dimen_str() == "dimen"
    assert dimens_str() == "dimens"
    assert jkeys_str() == "jkeys"
    assert jvalues_str() == "jvalues"
    assert keeps_buildable_str() == "keeps_buildable"
    assert keeps_justified_str() == "keeps_justified"
    assert last_pack_id_str() == "last_pack_id"
    assert mandate_str() == "mandate"
    assert max_tree_traverse_str() == "max_tree_traverse"
    assert offtrack_fund_str() == "offtrack_fund"
    assert offtrack_kids_star_set_str() == "offtrack_kids_star_set"
    assert planroot_str() == "planroot"
    assert respect_bit_str() == "respect_bit"
    assert reason_contexts_str() == "reason_contexts"
    assert sum_healerunit_share_str() == "sum_healerunit_share"
    assert tally_str() == "tally"
    assert voice_pool_str() == "voice_pool"
    assert voice_cred_points_str() == "voice_cred_points"
    assert voice_debt_points_str() == "voice_debt_points"
    assert voices_str() == "voices"
