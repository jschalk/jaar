from src.ch11_bud_logic._ref.ch11_keywords import (
    Ch11Keywords,
    EventInt_str,
    amount_str,
    ancestors_str,
    beliefadjust_str,
    beliefevent_facts_str,
    boss_facts_str,
    bud_time_str,
    bud_voice_nets_str,
    celldepth_str,
    found_facts_str,
    mandate_str,
    offi_time_str,
    quota_str,
    tran_time_str,
)


def test_Ch11Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch11Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert EventInt_str() == "EventInt"
    assert amount_str() == "amount"
    assert ancestors_str() == "ancestors"
    assert boss_facts_str() == "boss_facts"
    assert bud_voice_nets_str() == "bud_voice_nets"
    assert bud_time_str() == "bud_time"
    assert celldepth_str() == "celldepth"
    assert found_facts_str() == "found_facts"
    assert mandate_str() == "mandate"
    assert offi_time_str() == "offi_time"
    assert beliefadjust_str() == "beliefadjust"
    assert beliefevent_facts_str() == "beliefevent_facts"
    assert quota_str() == "quota"
    assert tran_time_str() == "tran_time"
