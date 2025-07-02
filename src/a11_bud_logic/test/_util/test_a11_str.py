from src.a11_bud_logic.test._util.a11_str import (
    amount_str,
    ancestors_str,
    boss_facts_str,
    bud_acct_nets_str,
    bud_owner_name_str,
    bud_time_str,
    celldepth_str,
    found_facts_str,
    mandate_str,
    offi_time_str,
    owneradjust_str,
    ownerevent_facts_str,
    quota_str,
    tran_time_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert amount_str() == "amount"
    assert ancestors_str() == "ancestors"
    assert boss_facts_str() == "boss_facts"
    assert bud_acct_nets_str() == "bud_acct_nets"
    assert bud_owner_name_str() == "bud_owner_name"
    assert bud_time_str() == "bud_time"
    assert celldepth_str() == "celldepth"
    assert found_facts_str() == "found_facts"
    assert mandate_str() == "mandate"
    assert offi_time_str() == "offi_time"
    assert owneradjust_str() == "owneradjust"
    assert ownerevent_facts_str() == "ownerevent_facts"
    assert quota_str() == "quota"
    assert tran_time_str() == "tran_time"
