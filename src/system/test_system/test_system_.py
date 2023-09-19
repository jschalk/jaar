from src.system.system import SystemUnit, systemunit_shop
from src.calendar.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    rename_example_system,
    copy_evaluation_system,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_system_exists():
    system_name = "test1"
    sx = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    assert sx.name == system_name
    assert sx.systems_dir == get_test_systems_dir()


def test_system_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create system
    system_name = get_temp_env_name()
    sx = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    print(f"{get_test_systems_dir()=} {sx.systems_dir=}")
    # x_func_delete_dir(sx.get_object_root_dir())
    print(f"delete {sx.get_object_root_dir()=}")
    system_dir = f"src/system/examples/systems/{system_name}"
    system_file_name = "system.json"
    system_file_path = f"{system_dir}/{system_file_name}"
    calendars_dir = f"{system_dir}/calendars"
    authors_dir = f"{system_dir}/authors"
    bank_file_name = "bank.db"
    bank_file_path = f"{system_dir}/{bank_file_name}"

    assert os_path.exists(system_dir) is False
    assert os_path.isdir(system_dir) is False
    assert os_path.exists(system_file_path) is False
    assert os_path.exists(calendars_dir) is False
    assert os_path.exists(authors_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=False)

    # THEN check calendars src directory created
    assert os_path.exists(system_dir)
    assert os_path.isdir(system_dir)
    assert os_path.exists(system_file_path)
    assert os_path.exists(calendars_dir)
    assert os_path.exists(authors_dir)
    assert os_path.exists(bank_file_path)
    assert sx.get_object_root_dir() == system_dir
    assert sx.get_public_dir() == calendars_dir
    assert sx.get_authors_dir() == authors_dir
    assert sx.get_bank_db_path() == bank_file_path


def test_rename_example_system_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create system
    old_system_name = get_temp_env_name()
    old_system_dir = f"src/system/examples/systems/{old_system_name}"
    old_system_file_name = "system.json"
    old_system_file_path = f"{old_system_dir}/{old_system_file_name}"
    old_calendars_dir = f"{old_system_dir}/calendars"
    old_authors_dir = f"{old_system_dir}/authors"

    new_system_name = "ex_env1"
    new_system_dir = f"src/system/examples/systems/{new_system_name}"
    new_system_file_name = "system.json"
    new_system_file_path = f"{new_system_dir}/{new_system_file_name}"
    new_calendars_dir = f"{new_system_dir}/calendars"
    new_authors_dir = f"{new_system_dir}/authors"
    x_func_delete_dir(dir=new_system_dir)
    print(f"{new_system_dir=}")

    sx = systemunit_shop(name=old_system_name, systems_dir=get_test_systems_dir())
    # x_func_delete_dir(sx.get_object_root_dir())
    # print(f"{sx.get_object_root_dir()=}")

    sx.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_system_dir)
    assert os_path.isdir(old_system_dir)
    assert os_path.exists(old_system_file_path)
    assert os_path.exists(old_calendars_dir)
    assert os_path.exists(old_authors_dir)
    assert sx.get_public_dir() == old_calendars_dir
    assert sx.get_authors_dir() == old_authors_dir

    assert os_path.exists(new_system_dir) is False
    assert os_path.isdir(new_system_dir) is False
    assert os_path.exists(new_system_file_path) is False
    assert os_path.exists(new_calendars_dir) is False
    assert os_path.exists(new_authors_dir) is False
    assert sx.get_public_dir() != new_calendars_dir
    assert sx.get_authors_dir() != new_authors_dir
    assert sx.name != new_system_name

    # WHEN
    rename_example_system(system_obj=sx, new_name=new_system_name)

    # THEN check calendars src directory created
    assert os_path.exists(old_system_dir) is False
    assert os_path.isdir(old_system_dir) is False
    assert os_path.exists(old_system_file_path) is False
    assert os_path.exists(old_calendars_dir) is False
    assert os_path.exists(old_authors_dir) is False
    assert sx.get_public_dir() != old_calendars_dir
    assert sx.get_authors_dir() != old_authors_dir

    assert os_path.exists(new_system_dir)
    assert os_path.isdir(new_system_dir)
    assert os_path.exists(new_system_file_path)
    assert os_path.exists(new_calendars_dir)
    assert os_path.exists(new_authors_dir)
    assert sx.get_public_dir() == new_calendars_dir
    assert sx.get_authors_dir() == new_authors_dir
    assert sx.name == new_system_name

    # Undo change to directory
    # x_func_delete_dir(dir=old_system_dir)
    # print(f"{old_system_dir=}")
    x_func_delete_dir(dir=new_system_dir)
    print(f"{new_system_dir=}")


def test_copy_evaluation_system_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create system
    old_system_name = get_temp_env_name()
    old_system_dir = f"src/system/examples/systems/{old_system_name}"
    old_system_file_name = "system.json"
    old_system_file_path = f"{old_system_dir}/{old_system_file_name}"
    old_calendars_dir = f"{old_system_dir}/calendars"
    old_authors_dir = f"{old_system_dir}/authors"

    sx = systemunit_shop(name=old_system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null()

    assert os_path.exists(old_system_dir)
    assert os_path.isdir(old_system_dir)
    assert os_path.exists(old_system_file_path)
    assert os_path.exists(old_calendars_dir)
    assert os_path.exists(old_authors_dir)
    assert sx.get_public_dir() == old_calendars_dir
    assert sx.get_authors_dir() == old_authors_dir

    new_system_name = "ex_env1"
    new_system_dir = f"src/system/examples/systems/{new_system_name}"
    new_system_file_name = "system.json"
    new_system_file_path = f"{new_system_dir}/{new_system_file_name}"
    new_calendars_dir = f"{new_system_dir}/calendars"
    new_authors_dir = f"{new_system_dir}/authors"

    assert os_path.exists(new_system_dir) is False
    assert os_path.isdir(new_system_dir) is False
    assert os_path.exists(new_system_file_path) is False
    assert os_path.exists(new_calendars_dir) is False
    assert os_path.exists(new_authors_dir) is False
    assert sx.get_public_dir() != new_calendars_dir
    assert sx.get_authors_dir() != new_authors_dir
    assert sx.name != new_system_name

    # WHEN
    copy_evaluation_system(src_name=sx.name, dest_name=new_system_name)

    # THEN check calendars src directory created
    assert os_path.exists(old_system_dir)
    assert os_path.isdir(old_system_dir)
    assert os_path.exists(old_system_file_path)
    assert os_path.exists(old_calendars_dir)
    assert os_path.exists(old_authors_dir)
    assert sx.get_public_dir() == old_calendars_dir
    assert sx.get_authors_dir() == old_authors_dir

    assert os_path.exists(new_system_dir)
    assert os_path.isdir(new_system_dir)
    assert os_path.exists(new_system_file_path)
    assert os_path.exists(new_calendars_dir)
    assert os_path.exists(new_authors_dir)
    assert sx.get_public_dir() != new_calendars_dir
    assert sx.get_authors_dir() != new_authors_dir
    assert sx.name != new_system_name

    # Undo change to directory
    # x_func_delete_dir(sx.get_object_root_dir())
    # x_func_delete_dir(dir=old_system_dir)
    x_func_delete_dir(dir=new_system_dir)


def test_copy_evaluation_system_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create system
    old_system_name = get_temp_env_name()
    sx = systemunit_shop(name=old_system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_system(src_name=sx.name, dest_name=old_system_name)
    assert (
        str(excinfo.value)
        == f"Cannot copy system to '{sx.get_object_root_dir()}' directory because '{sx.get_object_root_dir()}' exists."
    )


def test_systemunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_name()
    system_dir = f"src/system/examples/systems/{park_text}"
    assert os_path.exists(system_dir) is False

    # WHEN
    sx = systemunit_shop(name=park_text, systems_dir=get_test_systems_dir())

    # THEN
    assert sx != None
    assert sx.name == park_text
    assert os_path.exists(system_dir)
    assert sx._bank_db != None
