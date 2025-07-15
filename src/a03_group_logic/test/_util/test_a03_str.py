from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_partner_debt_points_str,
    _irrational_partner_debt_points_str,
    _memberships_str,
    awardee_title_str,
    believer_name_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    respect_bit_str,
    take_force_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH
    assert _credor_pool_str() == "_credor_pool"
    assert _debtor_pool_str() == "_debtor_pool"
    assert _fund_agenda_give_str() == "_fund_agenda_give"
    assert _fund_agenda_ratio_give_str() == "_fund_agenda_ratio_give"
    assert _fund_agenda_ratio_take_str() == "_fund_agenda_ratio_take"
    assert _fund_agenda_take_str() == "_fund_agenda_take"
    assert _fund_give_str() == "_fund_give"
    assert _fund_take_str() == "_fund_take"
    assert _inallocable_partner_debt_points_str() == "_inallocable_partner_debt_points"
    assert _irrational_partner_debt_points_str() == "_irrational_partner_debt_points"
    assert _memberships_str() == "_memberships"
    assert partner_name_str() == "partner_name"
    assert partner_cred_points_str() == "partner_cred_points"
    assert partner_debt_points_str() == "partner_debt_points"
    assert awardee_title_str() == "awardee_title"
    assert group_cred_points_str() == "group_cred_points"
    assert group_title_str() == "group_title"
    assert fund_take_str() == "fund_take"
    assert respect_bit_str() == "respect_bit"
    assert fund_give_str() == "fund_give"
    assert group_debt_points_str() == "group_debt_points"
    assert give_force_str() == "give_force"
    assert believer_name_str() == "believer_name"
    assert take_force_str() == "take_force"
