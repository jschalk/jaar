from src.ch19_kpi_toolbox._ref.ch19_keywords import (
    Ch19Keywords,
    default_kpi_bundle_str,
    moment_kpi001_voice_nets_str,
    moment_kpi002_belief_pledges_str,
)


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

    assert default_kpi_bundle_str() == "default_kpi_bundle"
    assert moment_kpi001_voice_nets_str() == "moment_kpi001_voice_nets"
    assert moment_kpi002_belief_pledges_str() == "moment_kpi002_belief_pledges"
