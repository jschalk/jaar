from src.econ.examples.example_clerks import get_clerkunit_2agenda
from src.econ.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_econ_id,
)
from src.agenda.agenda import agendaunit_shop


def test_clerkunit_set_depot_agenda_SetsCorrectInfo(clerk_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    x_clerk = get_clerkunit_2agenda(env_dir, get_temp_econ_id())
    assert x_clerk._plan.get_partys_depotlink_count() == 2
    print(f"{x_clerk._plan._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_clerk.set_depot_agenda(agendaunit_shop(_worker_id=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_clerk.set_depot_agenda(agendaunit_shop(_worker_id=zoa_text), assignment_text)

    # THEN
    print(f"{x_clerk._plan._partys.keys()=}")
    assert x_clerk._plan.get_partys_depotlink_count() == 4
