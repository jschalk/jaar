from src.a19_kpi_toolbox.test._util.a19_str import (
    moment_kpi001_partner_nets_str,
    moment_kpi002_belief_tasks_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert moment_kpi001_partner_nets_str() == "moment_kpi001_partner_nets"
    assert moment_kpi002_belief_tasks_str() == "moment_kpi002_belief_tasks"
