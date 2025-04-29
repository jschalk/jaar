from src.a06_bud_logic._utils.str_a06 import (
    acct_name_str,
    addin_str,
    awardee_title_str,
    base_str,
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
    fnigh_str,
    fopen_str,
    fund_coin_str,
    gogo_want_str,
    group_label_str,
    healer_name_str,
    morph_str,
    numor_str,
    parent_road_str,
    penny_str,
    respect_bit_str,
    road_str,
    stop_want_str,
    team_title_str,
    type_NameUnit_str,
    type_LabelUnit_str,
    type_TagUnit_str,
    type_RoadUnit_str,
)


def test_str_functions_ReturnsObj():
    assert acct_name_str() == "acct_name"
    assert addin_str() == "addin"
    assert awardee_title_str() == "awardee_title"
    assert base_str() == "base"
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
    assert fnigh_str() == "fnigh"
    assert fopen_str() == "fopen"
    assert fund_coin_str() == "fund_coin"
    assert gogo_want_str() == "gogo_want"
    assert group_label_str() == "group_label"
    assert morph_str() == "morph"
    assert numor_str() == "numor"
    assert parent_road_str() == "parent_road"
    assert penny_str() == "penny"
    assert respect_bit_str() == "respect_bit"
    assert road_str() == "road"
    assert stop_want_str() == "stop_want"
    assert team_title_str() == "team_title"
    assert type_NameUnit_str() == "NameUnit"
    assert type_LabelUnit_str() == "LabelUnit"
    assert type_TagUnit_str() == "TagUnit"
    assert type_RoadUnit_str() == "RoadUnit"
