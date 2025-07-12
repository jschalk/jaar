from src.a19_kpi_toolbox.test._util.a19_str import (
    belief_kpi001_person_nets_str,
    belief_kpi002_person_tasks_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert belief_kpi001_person_nets_str() == "belief_kpi001_person_nets"
    assert belief_kpi002_person_tasks_str() == "belief_kpi002_person_tasks"
