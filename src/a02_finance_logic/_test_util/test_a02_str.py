from src.a02_finance_logic._test_util.a02_str import (
    acct_name_str,
    addin_str,
    amount_str,
    bridge_str,
    celldepth_str,
    deal_acct_nets_str,
    deal_time_str,
    fund_coin_str,
    magnitude_str,
    offi_time_str,
    owner_name_str,
    penny_str,
    quota_str,
    tran_time_str,
    world_id_str,
)


def test_str_functions_ReturnsObj():
    assert addin_str() == "addin"
    assert bridge_str() == "bridge"
    assert celldepth_str() == "celldepth"
    assert deal_time_str() == "deal_time"
    assert tran_time_str() == "tran_time"
    assert quota_str() == "quota"
    assert magnitude_str() == "magnitude"
    assert deal_acct_nets_str() == "deal_acct_nets"
    assert world_id_str() == "world_id"
    assert acct_name_str() == "acct_name"
    assert owner_name_str() == "owner_name"
    assert offi_time_str() == "offi_time"
    assert amount_str() == "amount"
    assert fund_coin_str() == "fund_coin"
    assert penny_str() == "penny"
