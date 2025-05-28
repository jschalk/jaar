from src.a06_bud_logic._utils.str_a06 import (
    acct_name_str,
    addin_str,
    awardee_title_str,
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
    fstate_str,
    fnigh_str,
    fopen_str,
    fund_coin_str,
    gogo_want_str,
    group_title_str,
    healer_name_str,
    morph_str,
    pstate_str,
    pnigh_str,
    numor_str,
    popen_str,
    parent_way_str,
    penny_str,
    respect_bit_str,
    concept_way_str,
    stop_want_str,
    labor_title_str,
    type_NameStr_str,
    type_TitleStr_str,
    type_LabelStr_str,
    type_WayStr_str,
)


def test_str_functions_ReturnsObj():
    assert acct_name_str() == "acct_name"
    assert addin_str() == "addin"
    assert awardee_title_str() == "awardee_title"
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
    assert fstate_str() == "fstate"
    assert fnigh_str() == "fnigh"
    assert fopen_str() == "fopen"
    assert fund_coin_str() == "fund_coin"
    assert gogo_want_str() == "gogo_want"
    assert group_title_str() == "group_title"
    assert morph_str() == "morph"
    assert pstate_str() == "pstate"
    assert pnigh_str() == "pnigh"
    assert numor_str() == "numor"
    assert popen_str() == "popen"
    assert parent_way_str() == "parent_way"
    assert penny_str() == "penny"
    assert respect_bit_str() == "respect_bit"
    assert concept_way_str() == "concept_way"
    assert stop_want_str() == "stop_want"
    assert labor_title_str() == "labor_title"
    assert type_NameStr_str() == "NameStr"
    assert type_TitleStr_str() == "TitleStr"
    assert type_LabelStr_str() == "LabelStr"
    assert type_WayStr_str() == "WayStr"
