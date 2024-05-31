from src._instrument.file import delete_dir
from src._road.road import default_road_delimiter_if_none
from src.econ.econ import EconUnit, econunit_shop
from src.econ.examples.econ_env_kit import (
    env_dir_setup_cleanup,
    temp_reals_dir,
    temp_reals_dir,
    temp_real_id,
    get_texas_econdir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_EconUnit_exists():
    # GIVEN
    texas_econdir = get_texas_econdir()

    # WHEN
    x_econ = EconUnit(econdir=texas_econdir)

    # THEN
    assert x_econ.econdir == texas_econdir


def test_econunit_shop_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_id = temp_real_id()
    sue_text = "Sue"
    sue_texas_econdir = get_texas_econdir()
    sue_texas_econdir.person_id = sue_text

    # WHEN
    texas_econ = econunit_shop(sue_texas_econdir)

    # THEN
    assert texas_econ != None
    assert texas_econ.econdir.real_id == x_real_id
    assert os_path_exists(sue_texas_econdir.econ_dir())
    assert texas_econ._treasury_db != None
    assert texas_econ.econdir.person_id == sue_text
    assert texas_econ.econdir._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_ReturnsObj_WithTempNames(env_dir_setup_cleanup):
    # GIVEN
    # assert os_path_exists(econ_dir) is False

    # WHEN
    texas_econ = econunit_shop(get_texas_econdir())

    # THEN
    assert texas_econ != None
    assert texas_econ.econdir == get_texas_econdir()
    # assert os_path_exists(econ_dir)
    assert texas_econ._treasury_db != None


def test_econunit_shop_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"
    texas_econdir = get_texas_econdir()
    texas_econdir.real_id = texas_text
    texas_econdir._road_delimiter = slash_text

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        econunit_shop(texas_econdir)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_EconUnit_get_jobs_dir_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN create econ
    texas_econdir = get_texas_econdir()
    x_econ = EconUnit(texas_econdir)

    # WHEN / THEN
    jobs_text = "jobs"
    assert x_econ.get_jobs_dir() == f"{x_econ.econdir.econ_dir()}/{jobs_text}"


def test_EconUnit_get_roles_dir_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN create econ
    texas_econdir = get_texas_econdir()
    x_econ = EconUnit(texas_econdir)

    # WHEN / THEN
    roles_text = "roles"
    assert x_econ.get_roles_dir() == f"{x_econ.econdir.econ_dir()}/{roles_text}"


def test_EconUnit_set_econ_dirs_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create econ
    texas_econdir = get_texas_econdir()
    x_econ = EconUnit(texas_econdir)
    texas_econdir = get_texas_econdir()
    print(f"{temp_reals_dir()=} {x_econ.econdir.econ_dir()=}")
    # delete_dir(x_econ.econdir.econ_dir())
    print(f"delete {x_econ.econdir.econ_dir()=}")
    delete_dir(texas_econdir.reals_dir)
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{texas_econdir.econ_dir()}/{treasury_file_name}"

    assert os_path_exists(texas_econdir.reals_dir) is False
    assert os_path_isdir(texas_econdir.reals_dir) is False
    assert os_path_exists(x_econ.get_jobs_dir()) is False
    assert os_path_exists(x_econ.get_roles_dir()) is False
    assert os_path_exists(treasury_file_path) is False

    # WHEN
    x_econ.set_econ_dirs(in_memory_treasury=False)

    # THEN check agendas src directory created
    assert os_path_exists(texas_econdir.reals_dir)
    assert os_path_isdir(texas_econdir.reals_dir)
    assert os_path_exists(x_econ.get_jobs_dir())
    assert os_path_exists(x_econ.get_roles_dir())
    assert os_path_exists(treasury_file_path)
    assert x_econ.econdir.econ_dir() == texas_econdir.econ_dir()
    assert x_econ.get_jobs_dir() == x_econ.get_jobs_dir()
    assert x_econ.get_roles_dir() == x_econ.get_roles_dir()
    assert x_econ.get_treasury_db_path() == treasury_file_path


# def test_modify_real_id_example_econ_CorrectlyModifiesDirAndFiles(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN create econ
#     texas_econdir = get_texas_econdir()
#     old_x_real_id = texas_econdir.real_id
#     old_econ_dir = texas_econdir.econ_dir()
#     old_jobs_dir = texas_econdir.jobs_dir()
#     old_roles_dir = texas_econdir.roles_dir()
#     print(f"{texas_econdir.econ_road=}")

#     new_econdir = get_texas_econdir()
#     new_econdir.real_id = "music"
#     new_x_real_id = new_econdir.real_id
#     new_econ_dir = new_econdir.econ_dir()
#     new_jobs_dir = new_econdir.jobs_dir()
#     new_roles_dir = new_econdir.roles_dir()
#     delete_dir(dir=new_econ_dir)
#     print(f"{new_econ_dir=}")

#     texas_econ = econunit_shop(texas_econdir)

#     texas_econ.set_econ_dirs(in_memory_treasury=True)

#     assert os_path_exists(old_econ_dir)
#     assert os_path_isdir(old_econ_dir)
#     assert os_path_exists(old_jobs_dir)
#     assert os_path_exists(old_roles_dir)
#     assert texas_econ.get_jobs_dir() == old_jobs_dir
#     assert texas_econ.get_roles_dir() == old_roles_dir

#     assert os_path_exists(new_econ_dir) is False
#     assert os_path_isdir(new_econ_dir) is False
#     assert os_path_exists(new_jobs_dir) is False
#     assert os_path_exists(new_roles_dir) is False
#     assert texas_econ.get_jobs_dir() != new_jobs_dir
#     assert texas_econ.get_roles_dir() != new_roles_dir
#     assert texas_econ.real_id != new_x_real_id

#     # WHEN
#     print(f"{new_x_real_id=} {old_x_real_id=}")
#     print(f"{old_econ_dir=}")
#     assert os_path_exists(old_econ_dir)
#     texas_econdir.save_file_job("sue", "fooboo", True)
#     modify_real_id_example_econ(
#         econ_obj=texas_econ,
#         src_econdir=texas_econdir,
#         dst_econdir=new_econdir,
#         new_real_id=new_x_real_id,
#     )

#     # THEN check agendas src directory created
#     assert os_path_exists(old_econ_dir) is False
#     assert os_path_isdir(old_econ_dir) is False
#     assert os_path_exists(old_jobs_dir) is False
#     assert os_path_exists(old_roles_dir) is False
#     assert texas_econ.real_id == new_x_real_id
#     print(f"{texas_econ.get_jobs_dir()=}")
#     print(f"           {old_jobs_dir=}")
#     assert texas_econ.get_jobs_dir() != old_jobs_dir
#     assert texas_econ.get_roles_dir() != old_roles_dir

#     assert os_path_exists(new_econ_dir)
#     assert os_path_isdir(new_econ_dir)
#     assert os_path_exists(new_jobs_dir)
#     assert os_path_exists(new_roles_dir)
#     assert texas_econ.get_jobs_dir() == new_jobs_dir
#     assert texas_econ.get_roles_dir() == new_roles_dir

#     # Undo modification to directory
#     # delete_dir(dir=old_econ_dir)
#     # print(f"{old_econ_dir=}")
#     delete_dir(dir=new_econ_dir)
#     print(f"{new_econ_dir=}")


# def test_copy_evaluation_econ_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create econ
#     old_x_real_id = temp_real_id()
#     old_econ_dir = f"src/econ/examples/econs/{old_x_real_id}"
#     jobs_text = "jobs"
#     old_jobs_dir = f"{old_econ_dir}/{jobs_text}"
#     roles_text = "roles"
#     old_roles_dir = f"{old_econ_dir}/{roles_text}"
#     texas_econdir = get_texas_econdir()

#     x_econ = econunit_shop(old_x_real_id, temp_reals_dir())
#     x_econ.set_econ_dirs()

#     assert os_path_exists(old_econ_dir)
#     assert os_path_isdir(old_econ_dir)
#     assert os_path_exists(old_jobs_dir)
#     assert os_path_exists(old_roles_dir)
#     assert x_econ.get_jobs_dir() == old_jobs_dir
#     assert x_econ.get_roles_dir() == old_roles_dir

#     new_x_real_id = "ex_env1"
#     new_econ_dir = f"src/econ/examples/econs/{new_x_real_id}"
#     new_jobs_dir = f"{new_econ_dir}/{jobs_text}"
#     new_roles_dir = f"{new_econ_dir}/{roles_text}"

#     assert os_path_exists(new_econ_dir) is False
#     assert os_path_isdir(new_econ_dir) is False
#     assert os_path_exists(new_jobs_dir) is False
#     assert os_path_exists(new_roles_dir) is False
#     assert x_econ.get_jobs_dir() != new_jobs_dir
#     assert x_econ.get_roles_dir() != new_roles_dir
#     assert x_econ.real_id != new_x_real_id

#     # WHEN
#     copy_evaluation_econ(src_real_id=x_econ.real_id, dest_real_id=new_x_real_id)

#     # THEN check agendas src directory created
#     assert os_path_exists(old_econ_dir)
#     assert os_path_isdir(old_econ_dir)
#     assert os_path_exists(old_jobs_dir)
#     assert os_path_exists(old_roles_dir)
#     assert x_econ.get_jobs_dir() == old_jobs_dir
#     assert x_econ.get_roles_dir() == old_roles_dir

#     assert os_path_exists(new_econ_dir)
#     assert os_path_isdir(new_econ_dir)
#     assert os_path_exists(new_jobs_dir)
#     assert os_path_exists(new_roles_dir)
#     assert x_econ.get_jobs_dir() != new_jobs_dir
#     assert x_econ.get_roles_dir() != new_roles_dir
#     assert x_econ.real_id != new_x_real_id

#     # Undo modification to directory
#     # delete_dir(x_econ.econdir.econ_dir())
#     # delete_dir(dir=old_econ_dir)
#     delete_dir(dir=new_econ_dir)


# def test_copy_evaluation_econ_CorrectlyRaisesError(env_dir_setup_cleanup):
#     # GIVEN create econ
#     old_x_real_id = temp_real_id()
#     x_econ = econunit_shop(old_x_real_id, temp_reals_dir())
#     x_econ.set_econ_dirs()

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         copy_evaluation_econ(src_real_id=x_econ.real_id, dest_real_id=old_x_real_id)
#     assert (
#         str(excinfo.value)
#         == f"Cannot copy econ to '{x_econ.econdir.econ_dir()}' directory because '{x_econ.econdir.econ_dir()}' exists."
#     )