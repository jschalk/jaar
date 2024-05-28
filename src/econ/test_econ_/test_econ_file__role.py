from src.econ.econ import econunit_shop
from src.econ.examples.example_econ_agendas import (
    get_1node_agenda as example_get_1node_agenda,
    get_1node_agenda as example_get_7nodeJRootWithH_agenda,
    get_agenda_2CleanNodesRandomWeights,
)
from src.econ.examples.econ_env_kit import (
    get_temp_env_real_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path


def test_EconUnit_save_role_file_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    bob_text = "Bob"
    bob_role = get_agenda_2CleanNodesRandomWeights(bob_text)
    bob_path = f"{x_econ.get_roles_dir()}/{bob_role._owner_id}.json"
    assert os_path.exists(bob_path) == False

    # WHEN
    x_econ.save_role_file(bob_role)

    # THEN
    print(f"{bob_path=}")
    assert os_path.exists(bob_path)


def test_EconUnit_get_role_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    y_agenda = example_get_7nodeJRootWithH_agenda()
    x_econ.save_role_file(y_agenda)

    # WHEN / THEN
    assert x_econ.get_role_file(owner_id=y_agenda._owner_id) == y_agenda


def test_EconUnit_delete_role_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.get_roles_dir()}/{a_agenda._owner_id}.json"
    x_econ.save_role_file(a_agenda)
    print(f"{a_path=}")
    assert os_path.exists(a_path)

    # WHEN
    x_econ.delete_role_file(a_agenda._owner_id)

    # THEN
    assert os_path.exists(a_path) == False
