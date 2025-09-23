from src.ch11_bud_logic._ref.ch11_keywords import (
    amount_str,
    ancestors_str,
    beliefadjust_str,
    beliefevent_facts_str,
    boss_facts_str,
    bud_belief_name_str,
    bud_time_str,
    bud_voice_nets_str,
    celldepth_str,
    found_facts_str,
    mandate_str,
    offi_time_str,
    quota_str,
    tran_time_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert amount_str() == "amount"
    assert ancestors_str() == "ancestors"
    assert boss_facts_str() == "boss_facts"
    assert bud_voice_nets_str() == "bud_voice_nets"
    assert bud_belief_name_str() == "bud_belief_name"
    assert bud_time_str() == "bud_time"
    assert celldepth_str() == "celldepth"
    assert found_facts_str() == "found_facts"
    assert mandate_str() == "mandate"
    assert offi_time_str() == "offi_time"
    assert beliefadjust_str() == "beliefadjust"
    assert beliefevent_facts_str() == "beliefevent_facts"
    assert quota_str() == "quota"
    assert tran_time_str() == "tran_time"
