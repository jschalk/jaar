from src.a18_etl_toolbox._util.a18_str import (
    brick_agg_str,
    brick_valid_str,
    events_brick_agg_str,
    events_brick_valid_str,
    owner_net_amount_str,
    sound_agg_str,
    sound_raw_str,
    voice_agg_str,
    voice_raw_str,
    vow_acct_nets_str,
    vow_event_time_agg_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert brick_agg_str() == "brick_agg"
    assert brick_valid_str() == "brick_valid"
    assert events_brick_agg_str() == "events_brick_agg"
    assert events_brick_valid_str() == "events_brick_valid"
    assert owner_net_amount_str() == "owner_net_amount"
    assert vow_event_time_agg_str() == "vow_event_time_agg"
    assert vow_acct_nets_str() == "vow_acct_nets"
    assert sound_raw_str() == "sound_raw"
    assert sound_agg_str() == "sound_agg"
    assert voice_raw_str() == "voice_raw"
    assert voice_agg_str() == "voice_agg"
