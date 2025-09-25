from src.ch19_kpi_toolbox._ref.ch19_keywords import (
    default_kpi_bundle_str,
    moment_kpi001_voice_nets_str,
    moment_kpi002_belief_tasks_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert default_kpi_bundle_str() == "default_kpi_bundle"
    assert moment_kpi001_voice_nets_str() == "moment_kpi001_voice_nets"
    assert moment_kpi002_belief_tasks_str() == "moment_kpi002_belief_tasks"
