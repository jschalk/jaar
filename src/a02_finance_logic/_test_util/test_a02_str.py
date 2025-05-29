from src.a02_finance_logic._test_util.a02_str import (
    quota_str,
    deal_time_str,
    tran_time_str,
    bridge_str,
    celldepth_str,
    magnitude_str,
    deal_acct_nets_str,
    world_id_str,
    acct_name_str,
)


def test_str_functions_ReturnsObj():
    assert bridge_str() == "bridge"
    assert celldepth_str() == "celldepth"
    assert deal_time_str() == "deal_time"
    assert tran_time_str() == "tran_time"
    assert quota_str() == "quota"
    assert magnitude_str() == "magnitude"
    assert deal_acct_nets_str() == "deal_acct_nets"
    assert world_id_str() == "world_id"
    assert acct_name_str() == "acct_name"
