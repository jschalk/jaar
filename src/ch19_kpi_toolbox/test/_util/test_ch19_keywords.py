from src.ch19_kpi_toolbox._ref.ch19_keywords import Ch19Keywords, Ch19Keywords as wx


def test_Ch19Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch19Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert wx.default_kpi_bundle == "default_kpi_bundle"
    assert wx.moment_kpi001_voice_nets == "moment_kpi001_voice_nets"
    assert wx.moment_kpi002_belief_pledges == "moment_kpi002_belief_pledges"
