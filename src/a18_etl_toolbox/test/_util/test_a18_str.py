from src.a18_etl_toolbox.test._util.a18_str import (
    belief_net_amount_str,
    brick_agg_str,
    brick_raw_str,
    brick_valid_str,
    coin_event_time_agg_str,
    coin_ote1_agg_str,
    coin_partner_nets_str,
    events_brick_agg_str,
    events_brick_valid_str,
    sound_agg_str,
    sound_raw_str,
    voice_agg_str,
    voice_raw_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert coin_ote1_agg_str() == "coin_ote1_agg"
    assert brick_agg_str() == "brick_agg"
    assert brick_raw_str() == "brick_raw"
    assert brick_valid_str() == "brick_valid"
    assert events_brick_agg_str() == "events_brick_agg"
    assert events_brick_valid_str() == "events_brick_valid"
    assert belief_net_amount_str() == "belief_net_amount"
    assert coin_event_time_agg_str() == "coin_event_time_agg"
    assert coin_partner_nets_str() == "coin_partner_nets"
    assert sound_raw_str() == "sound_raw"
    assert sound_agg_str() == "sound_agg"
    assert voice_raw_str() == "voice_raw"
    assert voice_agg_str() == "voice_agg"
