from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_acct_debt_points_str,
    _irrational_acct_debt_points_str,
    _memberships_str,
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    awardee_title_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    owner_name_str,
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
    assert _inallocable_acct_debt_points_str() == "_inallocable_acct_debt_points"
    assert _irrational_acct_debt_points_str() == "_irrational_acct_debt_points"
    assert _memberships_str() == "_memberships"
    assert acct_name_str() == "acct_name"
    assert acct_cred_points_str() == "acct_cred_points"
    assert acct_debt_points_str() == "acct_debt_points"
    assert awardee_title_str() == "awardee_title"
    assert group_cred_points_str() == "group_cred_points"
    assert group_title_str() == "group_title"
    assert fund_take_str() == "fund_take"
    assert respect_bit_str() == "respect_bit"
    assert fund_give_str() == "fund_give"
    assert group_debt_points_str() == "group_debt_points"
    assert give_force_str() == "give_force"
    assert owner_name_str() == "owner_name"
    assert take_force_str() == "take_force"
