from src.s0_instrument.file import (
    create_file_path,
    dir_files,
    save_file,
    open_file,
    count_files,
    get_directory_path,
    is_path_valid,
    can_active_usser_edit_paths,
    is_path_existent_or_creatable,
    is_path_probably_creatable,
    is_path_existent_or_probably_creatable,
    get_all_dirs_with_file,
    get_integer_filenames,
)
from src.s0_instrument.examples.instrument_env import (
    get_instrument_temp_env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from platform import system as platform_system
from os.path import exists as os_path_exist


def test_create_file_path_ReturnsObj():
    # ESTABLISH
    obj_filename = "obj.json"
    x_dir = ("src/_instrument",)
    x_file_name = "examples"

    # WHEN / THEN
    assert create_file_path(None, None) == ""
    assert create_file_path(None, "") == ""
    assert create_file_path(None, obj_filename) == f"/{obj_filename}"
    assert create_file_path(x_dir, None) == x_dir
    assert create_file_path(x_dir, x_file_name) == f"{x_dir}/{x_file_name}"


def test_save_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x_name = "fizz_buzz"
    x_file_ext = "txt"
    x_file_name = f"{x_name}.{x_file_ext}"
    x_file_str = "trying this"
    print(f"{env_dir=} {x_file_name=}")
    assert not os_path_exist(create_file_path(env_dir, x_file_name))

    # WHEN
    save_file(dest_dir=env_dir, file_name=x_file_name, file_str=x_file_str)

    # THEN
    assert os_path_exist(create_file_path(env_dir, x_file_name))


def test_open_file_OpensFilesCorrectlyWith_dest_dirAnd_file_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    print(f"{env_dir=} {x1_file_name=}")
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_str=x1_file_str)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_str=x2_file_str)

    # WHEN / THEN
    assert open_file(dest_dir=env_dir, file_name=x1_file_name) == x1_file_str
    assert open_file(dest_dir=env_dir, file_name=x2_file_name) == x2_file_str


def test_open_file_OpensFilesCorrectlyWithOnly_dest_dir(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    x1_file_path = f"{env_dir}/{x1_file_name}"
    x2_file_path = f"{env_dir}/{x2_file_name}"

    print(f"{env_dir=} {x1_file_name=}")
    print(f"{env_dir=} {x1_file_name=}")
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_str=x1_file_str)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_str=x2_file_str)

    # WHEN / THEN
    assert open_file(dest_dir=x1_file_path, file_name=None) == x1_file_str
    assert open_file(dest_dir=x2_file_path, file_name=None) == x2_file_str


def test_save_file_ReplacesFileAsDefault(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    swim_str = "swim"
    swim_file_ext = "txt"
    swim_file_name = f"{swim_str}.{swim_file_ext}"
    swim_old_file_str = "swimming is good"
    swim_new_file_str = "swimming is ok"
    print(f"{env_dir=} {swim_file_name=}")
    save_file(dest_dir=env_dir, file_name=swim_file_name, file_str=swim_old_file_str)
    assert open_file(dest_dir=env_dir, file_name=swim_file_name) == swim_old_file_str

    # WHEN
    save_file(
        dest_dir=env_dir,
        file_name=swim_file_name,
        file_str=swim_new_file_str,
        replace=None,
    )

    # THEN
    assert open_file(dest_dir=env_dir, file_name=swim_file_name) == swim_new_file_str


def test_save_file_DoesNotReplaceFile(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    swim_str = "swim"
    swim_file_ext = "txt"
    swim_file_name = f"{swim_str}.{swim_file_ext}"
    swim_old_file_str = "swimming is good"
    swim_new_file_str = "swimming is ok"
    print(f"{env_dir=} {swim_file_name=}")
    save_file(dest_dir=env_dir, file_name=swim_file_name, file_str=swim_old_file_str)
    assert open_file(env_dir, swim_file_name) == swim_old_file_str

    # WHEN
    save_file(
        dest_dir=env_dir,
        file_name=swim_file_name,
        file_str=swim_new_file_str,
        replace=False,
    )

    # THEN
    assert open_file(env_dir, swim_file_name) == swim_old_file_str


def test_dir_files_correctlyGrabsFileData(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_file_name = "x1.txt"
    x2_file_name = "x2.txt"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_str=x1_file_str)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_str=x2_file_str)

    # WHEN
    files_dict = dir_files(dir_path=env_dir)

    # THEN
    assert len(files_dict) == 2
    assert files_dict.get(x1_file_name) == x1_file_str
    assert files_dict.get(x2_file_name) == x2_file_str


def test_dir_files_delete_extensions_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_str=x1_file_str)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_str=x2_file_str)

    # WHEN
    files_dict = dir_files(dir_path=env_dir, delete_extensions=True)

    # THEN
    assert files_dict.get(x1_name) == x1_file_str
    assert files_dict.get(x2_name) == x2_file_str


def test_dir_files_returnsSubDirs(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    save_file(
        dest_dir=f"{env_dir}/{x1_name}",
        file_name=x1_file_name,
        file_str=x1_file_str,
    )
    save_file(
        dest_dir=f"{env_dir}/{x2_name}",
        file_name=x2_file_name,
        file_str=x2_file_str,
    )

    # WHEN
    files_dict = dir_files(dir_path=env_dir, delete_extensions=True, include_dirs=True)

    # THEN
    assert files_dict.get(x1_name) is True
    assert files_dict.get(x2_name) is True


def test_dir_files_doesNotReturnsFiles(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_name = "x1"
    x1_file_ext = "txt"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x1_file_str = "trying this"
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_str=x1_file_str)
    x2_name = "x2"
    x2_file_ext = "json"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x2_file_str = "look there"
    save_file(
        dest_dir=f"{env_dir}/{x2_name}",
        file_name=x2_file_name,
        file_str=x2_file_str,
    )

    # WHEN
    files_dict = dir_files(dir_path=env_dir, include_files=False)

    # THEN
    print(f"{files_dict.get(x1_file_name)=}")
    with pytest_raises(Exception) as excinfo:
        files_dict[x1_file_name]
    assert str(excinfo.value) == "'x1.txt'"
    assert files_dict.get(x2_name) is True
    assert len(files_dict) == 1


def test_get_integer_filenames_ReturnsCoorectObjIfDirectoryDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    temp_dir = f"{env_dir}/temp_does_not_exist"
    assert os_path_exist(temp_dir) is False

    # WHEN
    files_dict = get_integer_filenames(temp_dir, 0)

    # THEN
    assert len(files_dict) == 0
    assert files_dict == set()


def test_get_integer_filenames_GrabsFileNamesWithIntegers_v0(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_file_name = "1.json"
    x2_file_name = "2.json"
    x_file_str = "file text"
    save_file(env_dir, x1_file_name, x_file_str)
    save_file(env_dir, x2_file_name, x_file_str)

    # WHEN
    files_dict = get_integer_filenames(env_dir, 0)

    # THEN
    assert len(files_dict) == 2
    assert files_dict == {1, 2}


def test_get_integer_filenames_GrabsFileNamesWithIntegersWithCorrectExtension(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    z_file_name = "z.json"
    x1_file_name = "1.json"
    x2_file_name = "2.json"
    txt1_file_name = "1.txt"
    txt3_file_name = "3.txt"
    x_file_str = "file text"
    save_file(env_dir, z_file_name, x_file_str)
    save_file(env_dir, x1_file_name, x_file_str)
    save_file(env_dir, x2_file_name, x_file_str)
    save_file(env_dir, txt1_file_name, x_file_str)
    save_file(env_dir, txt3_file_name, x_file_str)

    # WHEN
    files_dict = get_integer_filenames(env_dir, 0)

    # THEN
    assert len(files_dict) == 2
    assert files_dict == {1, 2}

    # WHEN / THEN
    assert get_integer_filenames(env_dir, 0, "txt") == {1, 3}
    assert get_integer_filenames(env_dir, None, "txt") == {1, 3}


def test_get_integer_filenames_GrabsFileNamesWithIntegersGreaterThan_min_integer(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    z_file_name = "z.json"
    x1_file_name = "1.json"
    x2_file_name = "2.json"
    x3_file_name = "3.json"
    txt1_file_name = "1.txt"
    txt3_file_name = "3.txt"
    x_file_str = "file text"
    save_file(env_dir, z_file_name, x_file_str)
    save_file(env_dir, x1_file_name, x_file_str)
    save_file(env_dir, x2_file_name, x_file_str)
    save_file(env_dir, x3_file_name, x_file_str)
    save_file(env_dir, txt1_file_name, x_file_str)
    save_file(env_dir, txt3_file_name, x_file_str)

    # WHEN
    assert get_integer_filenames(env_dir, 2) == {2, 3}
    assert get_integer_filenames(env_dir, 0, "txt") == {1, 3}


def test_count_files_ReturnsNoneIfDirectoryDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    does_not_exist_dir = f"{env_dir}/swim"

    # WHEN
    dir_count = count_files(dir_path=does_not_exist_dir)

    # THEN
    assert dir_count is None


def test_get_directory_path_ReturnsCorrectObj():
    # ESTABLISH
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"

    # WHEN
    texas_path = get_directory_path([texas_str])
    dallas_path = get_directory_path([texas_str, dallas_str])
    elpaso_path = get_directory_path([texas_str, elpaso_str])
    kern_path = get_directory_path([texas_str, elpaso_str, kern_str])

    # THEN
    assert "" == get_directory_path()
    assert texas_path == f"/{texas_str}"
    assert dallas_path == f"/{texas_str}/{dallas_str}"
    assert elpaso_path == f"/{texas_str}/{elpaso_str}"
    assert kern_path == f"/{texas_str}/{elpaso_str}/{kern_str}"


def test_is_path_valid_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert is_path_valid("run")
    assert is_path_valid("run/trail")
    assert is_path_valid("run/,trail")
    assert (
        platform_system() == "Windows" and is_path_valid("trail?") is False
    ) or platform_system() == "Linux"
    assert (
        platform_system() == "Windows" and is_path_valid("run/trail?") is False
    ) or platform_system() == "Linux"
    assert is_path_valid("run//trail////")


def test_can_active_usser_edit_paths_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert can_active_usser_edit_paths()


def test_is_path_existent_or_creatable_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert is_path_existent_or_creatable("run")
    assert (
        platform_system() == "Windows"
        and is_path_existent_or_creatable("run/trail?") is False
    ) or platform_system() == "Linux"
    assert is_path_existent_or_creatable("run///trail")


def test_is_path_probably_creatable_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert is_path_probably_creatable("run")
    assert is_path_probably_creatable("run/trail?") is False
    assert is_path_probably_creatable("run///trail") is False


def test_is_path_existent_or_probably_creatable_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert is_path_existent_or_probably_creatable("run")
    assert is_path_existent_or_probably_creatable("run/trail?") is False
    assert is_path_existent_or_probably_creatable("run///trail") is False


def test_get_all_dirs_with_file_ReturnsCorrectDirectorys(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_instrument_temp_env_dir()
    x1_file_name = "x1.txt"
    x1_file_str = "trying this"
    iowa_rel_dir = "iowa/dallas"
    ohio_rel_dir = "ohio/elpaso"
    iowa_dir = f"{env_dir}/{iowa_rel_dir}"
    ohio_dir = f"{env_dir}/{ohio_rel_dir}"
    save_file(dest_dir=iowa_dir, file_name=x1_file_name, file_str=x1_file_str)
    save_file(dest_dir=ohio_dir, file_name=x1_file_name, file_str=x1_file_str)

    # WHEN
    directory_set = get_all_dirs_with_file(x_file_name=x1_file_name, x_dir=env_dir)

    # THEN
    assert directory_set == {iowa_rel_dir, ohio_rel_dir}
