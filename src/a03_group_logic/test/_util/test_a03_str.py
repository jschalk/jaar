from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _groupunits_str,
    _inallocable_voice_debt_points_str,
    _irrational_voice_debt_points_str,
    _laborheir_str,
    _memberships_str,
    _parent_solo_str,
    awardee_title_str,
    awardunits_str,
    belief_name_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    laborunit_str,
    party_title_str,
    respect_bit_str,
    solo_str,
    take_force_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_name_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert _credor_pool_str() == "_credor_pool"
    assert _debtor_pool_str() == "_debtor_pool"
    assert _fund_agenda_give_str() == "_fund_agenda_give"
    assert _fund_agenda_ratio_give_str() == "_fund_agenda_ratio_give"
    assert _fund_agenda_ratio_take_str() == "_fund_agenda_ratio_take"
    assert _fund_agenda_take_str() == "_fund_agenda_take"
    assert _fund_give_str() == "_fund_give"
    assert _fund_take_str() == "_fund_take"
    assert _groupunits_str() == "_groupunits"
    assert _inallocable_voice_debt_points_str() == "_inallocable_voice_debt_points"
    assert _irrational_voice_debt_points_str() == "_irrational_voice_debt_points"
    assert _laborheir_str() == "_laborheir"
    assert _memberships_str() == "_memberships"
    assert _parent_solo_str() == "_parent_solo"
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
    assert party_title_str() == "party_title"
    assert respect_bit_str() == "respect_bit"
    assert solo_str() == "solo"
    assert take_force_str() == "take_force"
