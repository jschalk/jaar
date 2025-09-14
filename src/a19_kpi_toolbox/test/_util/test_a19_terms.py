from src.a19_kpi_toolbox.test._util.a19_terms import (
    moment_kpi001_voice_nets_str,
    moment_kpi002_belief_tasks_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert moment_kpi001_voice_nets_str() == "moment_kpi001_voice_nets"
    assert moment_kpi002_belief_tasks_str() == "moment_kpi002_belief_tasks"
