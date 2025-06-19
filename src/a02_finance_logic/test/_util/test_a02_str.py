from src.a02_finance_logic.test._util.a02_str import (
    acct_name_str,
    amount_str,
    bud_acct_nets_str,
    bud_time_str,
    celldepth_str,
    fund_iota_str,
    fund_pool_str,
    knot_str,
    magnitude_str,
    offi_time_str,
    owner_name_str,
    penny_str,
    quota_str,
    tran_time_str,
    vow_label_str,
)


def test_str_functions_ReturnsObj():
    assert knot_str() == "knot"
    assert celldepth_str() == "celldepth"
    assert bud_time_str() == "bud_time"
    assert vow_label_str() == "vow_label"
    assert fund_pool_str() == "fund_pool"
    assert tran_time_str() == "tran_time"
    assert quota_str() == "quota"
    assert magnitude_str() == "magnitude"
    assert bud_acct_nets_str() == "bud_acct_nets"
    assert acct_name_str() == "acct_name"
    assert owner_name_str() == "owner_name"
    assert offi_time_str() == "offi_time"
    assert amount_str() == "amount"
    assert fund_iota_str() == "fund_iota"
    assert penny_str() == "penny"
