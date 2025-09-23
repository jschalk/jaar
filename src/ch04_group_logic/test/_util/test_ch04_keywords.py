from src.ch04_group_logic._ref.ch04_keywords import (
    awardee_title_str,
    awardunits_str,
    belief_name_str,
    credor_pool_str,
    debtor_pool_str,
    fund_agenda_give_str,
    fund_agenda_ratio_give_str,
    fund_agenda_ratio_take_str,
    fund_agenda_take_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    groupunits_str,
    inallocable_voice_debt_points_str,
    irrational_voice_debt_points_str,
    laborheir_str,
    laborunit_str,
    memberships_str,
    parent_solo_str,
    party_title_str,
    rational_str,
    respect_bit_str,
    solo_str,
    take_force_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_name_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert credor_pool_str() == "credor_pool"
    assert debtor_pool_str() == "debtor_pool"
    assert fund_agenda_give_str() == "fund_agenda_give"
    assert fund_agenda_ratio_give_str() == "fund_agenda_ratio_give"
    assert fund_agenda_ratio_take_str() == "fund_agenda_ratio_take"
    assert fund_agenda_take_str() == "fund_agenda_take"
    assert fund_give_str() == "fund_give"
    assert fund_take_str() == "fund_take"
    assert groupunits_str() == "groupunits"
    assert inallocable_voice_debt_points_str() == "inallocable_voice_debt_points"
    assert irrational_voice_debt_points_str() == "irrational_voice_debt_points"
    assert laborheir_str() == "laborheir"
    assert memberships_str() == "memberships"
    assert parent_solo_str() == "parent_solo"
    assert awardunits_str() == "awardunits"
    assert awardee_title_str() == "awardee_title"
    assert belief_name_str() == "belief_name"
    assert fund_give_str() == "fund_give"
    assert fund_take_str() == "fund_take"
    assert give_force_str() == "give_force"
    assert group_cred_points_str() == "group_cred_points"
    assert group_debt_points_str() == "group_debt_points"
    assert group_title_str() == "group_title"
    assert laborunit_str() == "laborunit"
    assert voice_cred_points_str() == "voice_cred_points"
    assert voice_debt_points_str() == "voice_debt_points"
    assert voice_name_str() == "voice_name"
    assert rational_str() == "rational"
    assert party_title_str() == "party_title"
    assert respect_bit_str() == "respect_bit"
    assert solo_str() == "solo"
    assert take_force_str() == "take_force"
