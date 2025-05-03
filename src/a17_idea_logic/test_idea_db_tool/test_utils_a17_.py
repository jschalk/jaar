from src.a17_idea_logic._utils.str_a17 import (
    brick_raw_str,
    brick_agg_str,
    brick_valid_str,
    sound_raw_str,
    sound_agg_str,
    voice_raw_str,
    voice_agg_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert brick_raw_str() == "brick_raw"
    assert brick_agg_str() == "brick_agg"
    assert brick_valid_str() == "brick_valid"
    assert sound_raw_str() == "sound_raw"
    assert sound_agg_str() == "sound_agg"
    assert voice_raw_str() == "voice_raw"
    assert voice_agg_str() == "voice_agg"
