from src.ch19_kpi_toolbox._ref.ch19_keywords import (
    moment_kpi001_voice_nets_str,
    moment_kpi002_belief_tasks_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert moment_kpi001_voice_nets_str() == "moment_kpi001_voice_nets"
    assert moment_kpi002_belief_tasks_str() == "moment_kpi002_belief_tasks"
