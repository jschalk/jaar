from src.ch18_etl_toolbox._ref.ch18_keywords import (
    Ch18Keywords,
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


def test_Ch18Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch18Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


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
