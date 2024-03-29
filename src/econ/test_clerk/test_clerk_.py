from src._road.road import default_road_delimiter_if_none
from src.agenda.agenda import agendaunit_shop
from src.instrument.file import delete_dir
from src.econ.clerk import clerkunit_shop, ClerkUnit
from src.econ.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_econ_id,
)
from os import path as os_path


def test_ClerkUnit_exists(clerk_dir_setup_cleanup):
    # GIVEN / WHEN
    x_clerk = ClerkUnit()

    # GIVEN
    assert x_clerk != None
    assert x_clerk._role is None
    assert x_clerk._clerk_id is None
    assert x_clerk._env_dir is None
    assert x_clerk._econ_id is None
    assert x_clerk._clerkunit_dir is None
    assert x_clerk._clerkunits_dir is None
    assert x_clerk._role_file_name is None
    assert x_clerk._role_file_path is None
    assert x_clerk._job_file_name is None
    assert x_clerk._job_file_path is None
    assert x_clerk._forum_file_name is None
    assert x_clerk._forum_dir is None
    assert x_clerk._agendas_depot_dir is None
    assert x_clerk._agendas_ignore_dir is None
    assert x_clerk._agendas_digest_dir is None
    assert x_clerk._road_delimiter is None


def test_clerkunit_shop_exists(clerk_dir_setup_cleanup):
    # GIVEN
    x_owner_id = "test1"

    # WHEN
    x_clerk = clerkunit_shop(
        owner_id=x_owner_id,
        env_dir=get_temp_clerkunit_dir(),
        econ_id=get_temp_econ_id(),
    )

    # GIVEN
    assert x_clerk._clerk_id != None
    assert x_clerk._econ_id != None
    assert x_clerk._econ_id == get_temp_econ_id()
    assert x_clerk._road_delimiter == default_road_delimiter_if_none()
    assert x_clerk._role != None
    assert x_clerk._role._world_id == get_temp_econ_id()


def test_clerkunit_auto_output_job_to_forum_SavesAgendaToForumDirWhenTrue(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    x_econ_id = get_temp_econ_id()
    tim_text = "Tim"
    forum_text = "forum"
    forum_file_name = f"{tim_text}.json"
    forum_file_path = f"{get_temp_clerkunit_dir()}/{forum_text}/{forum_file_name}"
    print(f"{forum_file_path=}")
    # forum_file_path = f"src/econ/examples/ex_env/agendas/{forum_file_name}"
    x_clerk = clerkunit_shop(
        tim_text, env_dir, x_econ_id, _auto_output_job_to_forum=True
    )
    x_clerk.create_core_dir_and_files()
    assert os_path.exists(forum_file_path) is False

    # WHEN
    tim_agenda = agendaunit_shop(_owner_id=tim_text)
    tim_agenda.set_world_id(x_econ_id)
    x_clerk.set_depot_agenda(tim_agenda, "blind_trust")

    # THEN
    assert os_path.exists(forum_file_path)


def test_clerkunit_auto_output_job_to_forum_DoesNotSaveAgendaToForumDirWhenFalse(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    x_econ_id = get_temp_econ_id()
    tim_text = "Tim"
    forum_file_name = f"{tim_text}.json"
    forum_file_path = f"{get_temp_clerkunit_dir()}/agendas/{forum_file_name}"
    print(f"{forum_file_path=}")
    # forum_file_path = f"src/econ/examples/ex_env/agendas/{forum_file_name}"
    x_clerk = clerkunit_shop(tim_text, env_dir, x_econ_id, False)
    x_clerk.create_core_dir_and_files()
    assert os_path.exists(forum_file_path) is False

    # WHEN
    x_clerk.set_depot_agenda(agendaunit_shop(tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(forum_file_path) is False


def test_clerkunit_get_role_createsEmptyAgendaWhenFileDoesNotExist(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    slash_text = "/"
    tim_clerk = ClerkUnit(
        _clerk_id="Tim",
        _env_dir=get_temp_clerkunit_dir(),
        _econ_id=get_temp_econ_id(),
        _road_delimiter=slash_text,
    )
    tim_clerk.set_env_dir(
        env_dir=get_temp_clerkunit_dir(),
        clerk_id="Tim",
        econ_id=get_temp_econ_id(),
        _road_delimiter=default_road_delimiter_if_none(slash_text),
    )
    tim_clerk.set_clerkunit_dirs()
    tim_clerk.create_core_dir_and_files()
    assert os_path.exists(tim_clerk._role_file_path)
    delete_dir(dir=tim_clerk._role_file_path)
    assert os_path.exists(tim_clerk._role_file_path) is False
    assert tim_clerk._role is None

    # WHEN
    role_agenda = tim_clerk.get_role()

    # THEN
    assert os_path.exists(tim_clerk._role_file_path)
    assert tim_clerk._role != None
    assert role_agenda._road_delimiter != None
    assert role_agenda._road_delimiter == slash_text


def test_clerkunit_get_role_getsMemoryAgendaIfExists(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
    tim_clerk.create_core_dir_and_files()
    role_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._role_file_name}"
    role_agenda1 = tim_clerk.get_role()
    assert os_path.exists(role_file_path)
    assert tim_clerk._role != None

    # WHEN
    ray_text = "Ray"
    tim_clerk._role = agendaunit_shop(_owner_id=ray_text)
    role_agenda2 = tim_clerk.get_role()

    # THEN
    assert role_agenda2._owner_id == ray_text
    assert role_agenda2 != role_agenda1

    # WHEN
    tim_clerk._role = None
    role_agenda3 = tim_clerk.get_role()

    # THEN
    assert role_agenda3._owner_id != ray_text
    assert role_agenda3 == role_agenda1


def test_clerkunit_set_role_savesroleAgendaSet_role_None(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
    tim_clerk.create_core_dir_and_files()
    role_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._role_file_name}"
    role_agenda1 = tim_clerk.get_role()
    assert os_path.exists(role_file_path)
    assert tim_clerk._role != None

    # WHEN
    uid_text = "Not a actual uid"
    tim_clerk._role._idearoot._uid = uid_text
    tim_clerk.set_role()

    # THEN
    assert os_path.exists(role_file_path)
    assert tim_clerk._role is None
    role_agenda2 = tim_clerk.get_role()
    assert role_agenda2._idearoot._uid == uid_text


def test_clerkunit_set_role_savesGivenAgendaSet_role_None(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
    tim_clerk.create_core_dir_and_files()
    role_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._role_file_name}"
    role_agenda1 = tim_clerk.get_role()
    assert os_path.exists(role_file_path)
    assert tim_clerk._role != None

    # WHEN
    role_uid_text = "this is ._role uid"
    tim_clerk._role._idearoot._uid = role_uid_text

    new_agenda = agendaunit_shop(_owner_id=tim_text)
    new_agenda_uid_text = "this is pulled AgendaUnit uid"
    new_agenda._idearoot._uid = new_agenda_uid_text

    tim_clerk.set_role(new_agenda)

    # THEN
    assert os_path.exists(role_file_path)
    assert tim_clerk._role is None
    assert tim_clerk.get_role()._idearoot._uid != role_uid_text
    assert tim_clerk.get_role()._idearoot._uid == new_agenda_uid_text

    # GIVEN
    tim_clerk.set_role(new_agenda)
    assert os_path.exists(role_file_path)
    assert tim_clerk._role is None

    # WHEN
    tim_clerk.set_role_if_empty()

    # THEN
    assert tim_clerk._role != None
    assert os_path.exists(role_file_path)

    # WHEN
    role_uid_text = "this is ._role uid"
    tim_clerk._role._idearoot._uid = role_uid_text


def test_clerkunit_set_role_if_emtpy_DoesNotReplace_role(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
    tim_clerk.create_core_dir_and_files()
    saved_agenda = agendaunit_shop(_owner_id=tim_text)
    saved_agenda_uid_text = "this is pulled AgendaUnit uid"
    saved_agenda._idearoot._uid = saved_agenda_uid_text
    tim_clerk.set_role(saved_agenda)
    tim_clerk.get_role()
    assert tim_clerk._role != None

    # WHEN
    role_uid_text = "this is ._role uid"
    tim_clerk._role._idearoot._uid = role_uid_text
    tim_clerk.set_role_if_empty()

    # THEN
    assert tim_clerk._role != None
    assert tim_clerk._role._idearoot._uid == role_uid_text
    assert tim_clerk._role._idearoot._uid != saved_agenda_uid_text
