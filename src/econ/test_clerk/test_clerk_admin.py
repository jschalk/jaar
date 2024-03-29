from src.instrument.file import open_file, save_file
from src.econ.clerk import ClerkUnit, clerkunit_shop
from src.econ.examples.example_clerks import (
    get_6node_agenda as example_get_6node_agenda,
    get_6node_agenda as example_get_7nodeJRootWithH_agenda,
)
from src.econ.examples.clerk_env_kit import (
    get_temp_clerkunit_dir,
    get_temp_econ_id,
    clerk_dir_setup_cleanup,
)
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_ClerkUnit_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()

    # WHEN
    bob_clerkadmin = ClerkUnit(bob_text, env_dir, get_temp_econ_id())

    # THEN
    assert bob_clerkadmin._clerk_id != None
    assert bob_clerkadmin._env_dir != None
    assert bob_clerkadmin._econ_id != None
    assert bob_clerkadmin._road_delimiter is None
    assert bob_clerkadmin._clerkunit_dir is None
    assert bob_clerkadmin._role_file_name is None
    assert bob_clerkadmin._role_file_path is None
    assert bob_clerkadmin._job_file_name is None
    assert bob_clerkadmin._job_file_path is None
    assert bob_clerkadmin._forum_file_name is None
    assert bob_clerkadmin._forum_dir is None
    assert bob_clerkadmin._agendas_depot_dir is None
    assert bob_clerkadmin._agendas_ignore_dir is None
    assert bob_clerkadmin._agendas_digest_dir is None


def test_ClerkUnit_set_clerkunit_dirs_CorrectSetsClerkUnitAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_clerkadmin = ClerkUnit(bob_text, env_dir, get_temp_econ_id())
    assert bob_clerkadmin._clerkunit_dir is None
    assert bob_clerkadmin._job_file_name is None
    assert bob_clerkadmin._job_file_path is None
    assert bob_clerkadmin._forum_file_name is None
    assert bob_clerkadmin._forum_dir is None
    assert bob_clerkadmin._agendas_depot_dir is None
    assert bob_clerkadmin._agendas_ignore_dir is None
    assert bob_clerkadmin._agendas_digest_dir is None
    assert bob_clerkadmin._role_file_name is None
    assert bob_clerkadmin._role_file_path is None
    # WHEN
    bob_clerkadmin.set_clerkunit_dirs()

    # THEN
    assert bob_clerkadmin._clerkunit_dir != None
    assert bob_clerkadmin._job_file_name != None
    assert bob_clerkadmin._job_file_path != None
    assert bob_clerkadmin._forum_file_name != None
    assert bob_clerkadmin._forum_dir != None
    assert bob_clerkadmin._agendas_depot_dir != None
    assert bob_clerkadmin._agendas_ignore_dir != None
    assert bob_clerkadmin._agendas_digest_dir != None
    assert bob_clerkadmin._role_file_name != None
    assert bob_clerkadmin._role_file_path != None

    leaders_drectory_folder = "clerkunits"
    x_clerkunits_dir = f"{env_dir}/{leaders_drectory_folder}"
    x_clerkunit_dir = f"{x_clerkunits_dir}/{bob_text}"
    x_forum_file_name = f"{bob_text}.json"
    x_role_file_name = "role_agenda.json"
    x_role_file_path = f"{x_clerkunit_dir}/{x_role_file_name}"
    x_job_file_name = "output_agenda.json"
    x_job_file_path = f"{x_clerkunit_dir}/{x_job_file_name}"
    forum_text = "forum"
    depot_text = "depot"
    x_agendas_depot_dir = f"{x_clerkunit_dir}/{depot_text}"
    x_agendas_ignore_dir = f"{x_clerkunit_dir}/ignores"
    x_agendas_digest_dir = f"{x_clerkunit_dir}/digests"
    x_forum_dir = f"{env_dir}/{forum_text}"
    assert bob_clerkadmin._clerkunits_dir == x_clerkunits_dir
    assert bob_clerkadmin._clerkunit_dir == x_clerkunit_dir
    assert bob_clerkadmin._role_file_name == x_role_file_name
    assert bob_clerkadmin._role_file_path == x_role_file_path
    assert bob_clerkadmin._job_file_name == x_job_file_name
    assert bob_clerkadmin._job_file_path == x_job_file_path
    assert bob_clerkadmin._agendas_depot_dir == x_agendas_depot_dir
    assert bob_clerkadmin._agendas_ignore_dir == x_agendas_ignore_dir
    assert bob_clerkadmin._agendas_digest_dir == x_agendas_digest_dir
    assert bob_clerkadmin._forum_file_name == x_forum_file_name
    assert bob_clerkadmin._forum_dir == x_forum_dir


def test_ClerkUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    clerk_dir_setup_cleanup,
):
    # GIVEN create leader
    jul_text = "julian"
    env_dir = get_temp_clerkunit_dir()
    jul_clerkunit = ClerkUnit(
        _clerk_id=jul_text,
        _env_dir=env_dir,
        _econ_id=get_temp_econ_id(),
        _road_delimiter=",",
    )
    jul_clerkunit.set_clerkunit_dirs()
    assert os_path_exists(jul_clerkunit._clerkunits_dir) is False
    assert os_path_exists(jul_clerkunit._clerkunit_dir) is False
    assert os_path_exists(jul_clerkunit._role_file_path) is False
    assert os_path_isdir(jul_clerkunit._clerkunit_dir) is False
    assert os_path_exists(jul_clerkunit._agendas_depot_dir) is False
    assert os_path_exists(jul_clerkunit._agendas_digest_dir) is False
    assert os_path_exists(jul_clerkunit._agendas_ignore_dir) is False

    # WHEN
    x_agenda = example_get_7nodeJRootWithH_agenda()
    jul_clerkunit.create_core_dir_and_files(x_agenda)

    # THEN check agendas src directory created
    print(f"Checking {jul_clerkunit._clerkunits_dir=}")
    print(f"Checking {jul_clerkunit._clerkunit_dir=}")
    assert os_path_exists(jul_clerkunit._clerkunits_dir)
    assert os_path_exists(jul_clerkunit._clerkunit_dir)
    assert os_path_exists(jul_clerkunit._role_file_path)
    assert os_path_isdir(jul_clerkunit._clerkunit_dir)
    assert os_path_exists(jul_clerkunit._agendas_depot_dir)
    assert os_path_exists(jul_clerkunit._agendas_digest_dir)
    assert os_path_exists(jul_clerkunit._agendas_ignore_dir)


def test_ClerkUnit_create_core_dir_and_files_DoesNotOverWrite_roleAgenda(
    clerk_dir_setup_cleanup,
):
    # GIVEN create leader
    jul_text = "julian"
    env_dir = get_temp_clerkunit_dir()
    jul_clerkunit = clerkunit_shop(jul_text, env_dir, get_temp_econ_id())
    jul_clerkunit.set_clerkunit_dirs()
    x_agenda = example_get_7nodeJRootWithH_agenda()
    jul_clerkunit.create_core_dir_and_files(x_agenda)
    assert os_path_exists(jul_clerkunit._role_file_path)
    # jul_cx = agenda_get_from_json(open_file(jul_clerkunit._role_file_path))
    ex1 = "teesting text"
    save_file(
        dest_dir=jul_clerkunit._clerkunit_dir,
        file_name=jul_clerkunit._role_file_name,
        file_text=ex1,
    )
    assert open_file(jul_clerkunit._clerkunit_dir, jul_clerkunit._role_file_name) == ex1

    # WHEN
    jul_clerkunit.create_core_dir_and_files(x_agenda)

    # THEN
    assert open_file(jul_clerkunit._clerkunit_dir, jul_clerkunit._role_file_name) == ex1


def test_ClerkUnit_set_clerk_id_SetsCorrectAttrs(clerk_dir_setup_cleanup):
    # GIVEN create leader
    env_dir = get_temp_clerkunit_dir()

    old_bob_text = "Bob"
    jul_clerkunit = clerkunit_shop(old_bob_text, env_dir, get_temp_econ_id())
    x_agenda = example_get_7nodeJRootWithH_agenda()
    jul_clerkunit.set_clerkunit_dirs()
    jul_clerkunit.create_core_dir_and_files(x_agenda)
    old_clerkunit_dir = jul_clerkunit._clerkunit_dir
    # old_clerkunit_dir = f"{env_dir}/clerkunits/{old_leader_text}"
    print(f"{jul_clerkunit._clerkunit_dir}")
    clerkunits_text = "clerkunits"
    clerkunits_dir = f"{env_dir}/clerkunits"
    print(f"{clerkunits_dir}/{old_bob_text}")
    role_file_name = "role_agenda.json"
    old_role_file_path = f"{old_clerkunit_dir}/{role_file_name}"

    assert os_path_exists(old_clerkunit_dir)
    assert os_path_isdir(old_clerkunit_dir)
    assert os_path_exists(old_role_file_path)

    tim_text = "Tim"
    new_clerkunit_dir = f"{clerkunits_dir}/{tim_text}"
    new_role_file_path = f"{new_clerkunit_dir}/{role_file_name}"
    assert os_path_exists(new_clerkunit_dir) == False
    assert os_path_isdir(new_clerkunit_dir) == False
    assert os_path_exists(new_role_file_path) == False

    # WHEN
    jul_clerkunit.set_clerk_id(new_clerk_id=tim_text)

    # THEN
    assert os_path_exists(old_clerkunit_dir) == False
    assert os_path_isdir(old_clerkunit_dir) == False
    assert os_path_exists(old_role_file_path) == False
    assert os_path_exists(new_clerkunit_dir)
    assert os_path_isdir(new_clerkunit_dir)
    assert os_path_exists(new_role_file_path)


def test_clerkunit_auto_output_job_to_forum_SavesAgendaToForumDir(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    bob_clerkadmin = clerkunit_shop(
        bob_text, get_temp_clerkunit_dir(), get_temp_econ_id()
    )
    x_agenda = example_get_6node_agenda()
    x_agenda.set_owner_id(new_owner_id=bob_text)
    bob_clerkadmin.create_core_dir_and_files(x_agenda)

    forum_file_path = f"{bob_clerkadmin._forum_dir}/{bob_clerkadmin._forum_file_name}"
    print(f"{forum_file_path=}")
    assert os_path_exists(forum_file_path) is False

    # WHEN
    bob_clerkadmin.save_agenda_to_forum(x_agenda)

    # THEN
    assert os_path_exists(forum_file_path)
