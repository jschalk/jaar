from src.a18_etl_toolbox._test_util.a18_str import (
    events_brick_agg_str,
    events_brick_valid_str,
    owner_net_amount_str,
    vow_acct_nets_str,
    vow_event_time_agg_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert events_brick_agg_str() == "events_brick_agg"
    assert events_brick_valid_str() == "events_brick_valid"
    assert owner_net_amount_str() == "owner_net_amount"
    assert vow_event_time_agg_str() == "vow_event_time_agg"
    assert vow_acct_nets_str() == "vow_acct_nets"
