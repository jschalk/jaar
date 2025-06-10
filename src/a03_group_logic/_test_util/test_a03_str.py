from src.a03_group_logic._test_util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_debtit_score_str,
    _irrational_debtit_score_str,
    _memberships_str,
    awardee_title_str,
    credit_score_str,
    credit_vote_str,
    debtit_score_str,
    debtit_vote_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_title_str,
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
    assert _inallocable_debtit_score_str() == "_inallocable_debtit_score"
    assert _irrational_debtit_score_str() == "_irrational_debtit_score"
    assert _memberships_str() == "_memberships"
    assert credit_score_str() == "credit_score"
    assert debtit_score_str() == "debtit_score"
    assert credit_vote_str() == "credit_vote"
    assert group_title_str() == "group_title"
    assert fund_take_str() == "fund_take"
    assert respect_bit_str() == "respect_bit"
    assert fund_give_str() == "fund_give"
    assert debtit_vote_str() == "debtit_vote"
    assert give_force_str() == "give_force"
    assert awardee_title_str() == "awardee_title"
    assert take_force_str() == "take_force"
