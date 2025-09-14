from src.a18_etl_toolbox._ref.a18_terms import (
    belief_net_amount_str,
    brick_agg_str,
    brick_raw_str,
    brick_valid_str,
    events_brick_agg_str,
    events_brick_valid_str,
    heard_agg_str,
    heard_raw_str,
    moment_event_time_agg_str,
    moment_ote1_agg_str,
    moment_voice_nets_str,
    sound_agg_str,
    sound_raw_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert moment_ote1_agg_str() == "moment_ote1_agg"
    assert brick_agg_str() == "brick_agg"
    assert brick_raw_str() == "brick_raw"
    assert brick_valid_str() == "brick_valid"
    assert events_brick_agg_str() == "events_brick_agg"
    assert events_brick_valid_str() == "events_brick_valid"
    assert belief_net_amount_str() == "belief_net_amount"
    assert moment_event_time_agg_str() == "moment_event_time_agg"
    assert moment_voice_nets_str() == "moment_voice_nets"
    assert sound_raw_str() == "sound_raw"
    assert sound_agg_str() == "sound_agg"
    assert heard_raw_str() == "heard_raw"
    assert heard_agg_str() == "heard_agg"
