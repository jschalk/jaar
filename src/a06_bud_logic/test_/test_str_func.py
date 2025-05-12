from src.a06_bud_logic._utils.str_a06 import (
    acct_name_str,
    addin_str,
    awardee_label_str,
    rcontext_str,
    begin_str,
    close_str,
    credit_belief_str,
    credor_respect_str,
    credit_vote_str,
    debtit_belief_str,
    debtor_respect_str,
    debtit_vote_str,
    denom_str,
    event_int_str,
    fcontext_str,
    fbranch_str,
    fnigh_str,
    fopen_str,
    fund_coin_str,
    gogo_want_str,
    group_label_str,
    healer_name_str,
    morph_str,
    rbranch_str,
    pnigh_str,
    numor_str,
    open_str,
    parent_way_str,
    penny_str,
    respect_bit_str,
    idea_way_str,
    stop_want_str,
    team_label_str,
    type_NameStr_str,
    type_LabelStr_str,
    type_TagStr_str,
    type_WayStr_str,
)


def test_str_functions_ReturnsObj():
    assert acct_name_str() == "acct_name"
    assert addin_str() == "addin"
    assert awardee_label_str() == "awardee_label"
    assert rcontext_str() == "rcontext"
    assert fcontext_str() == "fcontext"
    assert begin_str() == "begin"
    assert close_str() == "close"
    assert credit_belief_str() == "credit_belief"
    assert credor_respect_str() == "credor_respect"
    assert credit_vote_str() == "credit_vote"
    assert debtit_belief_str() == "debtit_belief"
    assert debtor_respect_str() == "debtor_respect"
    assert debtit_vote_str() == "debtit_vote"
    assert denom_str() == "denom"
    assert event_int_str() == "event_int"
    assert fbranch_str() == "fbranch"
    assert fnigh_str() == "fnigh"
    assert fopen_str() == "fopen"
    assert fund_coin_str() == "fund_coin"
    assert gogo_want_str() == "gogo_want"
    assert group_label_str() == "group_label"
    assert morph_str() == "morph"
    assert rbranch_str() == "rbranch"
    assert pnigh_str() == "pnigh"
    assert numor_str() == "numor"
    assert open_str() == "open"
    assert parent_way_str() == "parent_way"
    assert penny_str() == "penny"
    assert respect_bit_str() == "respect_bit"
    assert idea_way_str() == "idea_way"
    assert stop_want_str() == "stop_want"
    assert team_label_str() == "team_label"
    assert type_NameStr_str() == "NameStr"
    assert type_LabelStr_str() == "LabelStr"
    assert type_TagStr_str() == "TagStr"
    assert type_WayStr_str() == "WayStr"
