from src.a02_finance_logic._test_util.a02_str import (
    acct_name_str,
    amount_str,
    bridge_str,
    celldepth_str,
    deal_acct_nets_str,
    deal_time_str,
    fisc_label_str,
    fund_iota_str,
    fund_pool_str,
    magnitude_str,
    offi_time_str,
    owner_name_str,
    penny_str,
    quota_str,
    tran_time_str,
)


def test_str_functions_ReturnsObj():
    assert bridge_str() == "bridge"
    assert celldepth_str() == "celldepth"
    assert deal_time_str() == "deal_time"
    assert fisc_label_str() == "fisc_label"
    assert fund_pool_str() == "fund_pool"
    assert tran_time_str() == "tran_time"
    assert quota_str() == "quota"
    assert magnitude_str() == "magnitude"
    assert deal_acct_nets_str() == "deal_acct_nets"
    assert acct_name_str() == "acct_name"
    assert owner_name_str() == "owner_name"
    assert offi_time_str() == "offi_time"
    assert amount_str() == "amount"
    assert fund_iota_str() == "fund_iota"
    assert penny_str() == "penny"
