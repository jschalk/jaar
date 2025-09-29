from src.ch18_etl_toolbox._ref.ch18_keywords import Ch18Keywords, Ch18Keywords as wx


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
    assert wx.moment_ote1_agg == "moment_ote1_agg"
    assert wx.brick_agg == "brick_agg"
    assert wx.brick_raw == "brick_raw"
    assert wx.brick_valid == "brick_valid"
    assert wx.events_brick_agg == "events_brick_agg"
    assert wx.events_brick_valid == "events_brick_valid"
    assert wx.belief_net_amount == "belief_net_amount"
    assert wx.moment_event_time_agg == "moment_event_time_agg"
    assert wx.moment_voice_nets == "moment_voice_nets"
    assert wx.sound_raw == "sound_raw"
    assert wx.sound_agg == "sound_agg"
    assert wx.heard_raw == "heard_raw"
    assert wx.heard_agg == "heard_agg"
