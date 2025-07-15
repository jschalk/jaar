from src.a19_kpi_toolbox.test._util.a19_str import (
    belief_kpi001_partner_nets_str,
    belief_kpi002_partner_tasks_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert belief_kpi001_partner_nets_str() == "belief_kpi001_partner_nets"
    assert belief_kpi002_partner_tasks_str() == "belief_kpi002_partner_tasks"
