from src.a19_kpi_toolbox.test._util.a19_str import (
    coin_kpi001_partner_nets_str,
    coin_kpi002_belief_tasks_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert coin_kpi001_partner_nets_str() == "coin_kpi001_partner_nets"
    assert coin_kpi002_belief_tasks_str() == "coin_kpi002_belief_tasks"
