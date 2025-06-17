from os.path import exists as os_path_exist, join as os_path_join
from pathlib import Path as pathlib_Path
from platform import system as platform_system
from pytest import raises as pytest_raises
from src.a00_data_toolbox._util.a00_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a00_data_toolbox.dict_toolbox import get_dict_from_json
from src.a00_data_toolbox.file_toolbox import (
    can_usser_edit_paths,
    count_files,
    create_path,
    get_all_dirs_with_file,
    get_dir_file_strs,
    get_dir_filenames,
    get_directory_path,
    get_immediate_subdir,
    get_integer_filenames,
    get_max_file_number,
    is_path_existent_or_creatable,
    is_path_existent_or_probably_creatable,
    is_path_probably_creatable,
    is_path_valid,
    is_subdirectory,
    open_file,
    open_json,
    save_file,
    save_json,
    set_dir,
)


def test_create_path_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    obj_filename = "obj.json"
    x_dir = os_path_join(get_module_temp_dir(), "_instrument")
    x_filename = "examples"

    # WHEN / THEN
    assert create_path(None, None) == ""
    assert create_path(None, "") == ""
    assert create_path(None, obj_filename) == obj_filename
    assert create_path(x_dir, None) == x_dir
    assert create_path(x_dir, x_filename) == os_path_join(x_dir, x_filename)
    assert create_path(x_dir, 1) == os_path_join(x_dir, str(1))


def test_is_subdirectory_ReturnsObj(env_dir_setup_cleanup):
    env_dir = get_module_temp_dir()
    sub = os_path_join(env_dir, "subdir")
    assert is_subdirectory(sub, env_dir)
    assert is_subdirectory(env_dir, sub) is False
    assert is_subdirectory(env_dir, env_dir)


def test_get_immediate_subdir_ReturnsObj(env_dir_setup_cleanup):
    env_dir = get_module_temp_dir()
    level1 = os_path_join(env_dir, "level1")
    level2 = os_path_join(level1, "level2")
    expected_path = str(pathlib_Path(level1).resolve())
    assert get_immediate_subdir(env_dir, level1) == expected_path
    assert get_immediate_subdir(env_dir, level2) == expected_path
    assert get_immediate_subdir(env_dir, level2) == expected_path
    assert get_immediate_subdir(env_dir, env_dir) is None
    assert get_immediate_subdir(level2, env_dir) is None


def test_set_dir_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    fizz_name = "fizz_buzz"
    fizz_dir = f"{env_dir}/{fizz_name}"
    assert not os_path_exist(fizz_dir)

    # WHEN
    set_dir(fizz_dir)

    # THEN
    assert os_path_exist(fizz_dir)

    # WHEN running it again does not error out
    set_dir(fizz_dir)

    # THEN
    assert os_path_exist(fizz_dir)


def test_save_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x_name = "fizz_buzz"
    x_file_ext = "txt"
    x_filename = f"{x_name}.{x_file_ext}"
    x_file_str = "trying this"
    print(f"{env_dir=} {x_filename=}")
    assert not os_path_exist(create_path(env_dir, x_filename))

    # WHEN
    save_file(dest_dir=env_dir, filename=x_filename, file_str=x_file_str)

    # THEN
    assert os_path_exist(create_path(env_dir, x_filename))


def test_open_file_OpensFilesCorrectlyWith_dest_dirAnd_filename(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_filename = f"{x1_name}.{x1_file_ext}"
    x2_filename = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    print(f"{env_dir=} {x1_filename=}")
    save_file(dest_dir=env_dir, filename=x1_filename, file_str=x1_file_str)
    save_file(dest_dir=env_dir, filename=x2_filename, file_str=x2_file_str)

    # WHEN / THEN
    assert open_file(dest_dir=env_dir, filename=x1_filename) == x1_file_str
    assert open_file(dest_dir=env_dir, filename=x2_filename) == x2_file_str


def test_open_file_OpensFilesCorrectlyWithOnly_dest_dir(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_filename = f"{x1_name}.{x1_file_ext}"
    x2_filename = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    x1_file_path = f"{env_dir}/{x1_filename}"
    x2_file_path = f"{env_dir}/{x2_filename}"

    print(f"{env_dir=} {x1_filename=}")
    print(f"{env_dir=} {x1_filename=}")
    save_file(dest_dir=env_dir, filename=x1_filename, file_str=x1_file_str)
    save_file(dest_dir=env_dir, filename=x2_filename, file_str=x2_file_str)

    # WHEN / THEN
    assert open_file(dest_dir=x1_file_path, filename=None) == x1_file_str
    assert open_file(dest_dir=x2_file_path, filename=None) == x2_file_str
    assert open_file(dest_dir=x2_file_path) == x2_file_str


def test_save_json_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    bob_str = "bob"
    yao_str = "yao"
    x_filename = "fizz_buzz.json"
    x_dict = {"users": {bob_str: 1, yao_str: 2}}
    print(f"{env_dir=} {x_filename=}")
    assert not os_path_exist(create_path(env_dir, x_filename))

    # WHEN
    save_json(env_dir, x_filename, x_dict)

    # THEN
    assert os_path_exist(create_path(env_dir, x_filename))
    generated_dict = get_dict_from_json(open_file(env_dir, x_filename))
    print(f"{generated_dict=}")
    expected_dict = {"users": {"bob": 1, "yao": 2}}
    assert generated_dict == expected_dict


def test_open_json_ReturnsObj(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    bob_str = "bob"
    yao_str = "yao"
    x_filename = "fizz_buzz.json"
    x_dict = {"names": {bob_str: 1, yao_str: 2}}
    print(f"{env_dir=} {x_filename=}")
    save_json(env_dir, x_filename, x_dict)
    assert os_path_exist(create_path(env_dir, x_filename))

    # WHEN
    generated_dict = open_json(env_dir, x_filename)

    # THEN
    expected_dict = {"names": {"bob": 1, "yao": 2}}
    assert generated_dict == expected_dict


def test_save_file_ReplacesFileAsDefault(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    swim_str = "swim"
    swim_file_ext = "txt"
    swim_filename = f"{swim_str}.{swim_file_ext}"
    swim_old_file_str = "swimming is good"
    swim_new_file_str = "swimming is ok"
    print(f"{env_dir=} {swim_filename=}")
    save_file(dest_dir=env_dir, filename=swim_filename, file_str=swim_old_file_str)
    assert open_file(dest_dir=env_dir, filename=swim_filename) == swim_old_file_str

    # WHEN
    save_file(
        dest_dir=env_dir,
        filename=swim_filename,
        file_str=swim_new_file_str,
        replace=None,
    )

    # THEN
    assert open_file(dest_dir=env_dir, filename=swim_filename) == swim_new_file_str


def test_save_file_DoesNotReplaceFile(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    swim_str = "swim"
    swim_file_ext = "txt"
    swim_filename = f"{swim_str}.{swim_file_ext}"
    swim_old_file_str = "swimming is good"
    swim_new_file_str = "swimming is ok"
    print(f"{env_dir=} {swim_filename=}")
    save_file(dest_dir=env_dir, filename=swim_filename, file_str=swim_old_file_str)
    assert open_file(env_dir, swim_filename) == swim_old_file_str

    # WHEN
    save_file(
        dest_dir=env_dir,
        filename=swim_filename,
        file_str=swim_new_file_str,
        replace=False,
    )

    # THEN
    assert open_file(env_dir, swim_filename) == swim_old_file_str


def test_save_file_DoesNotRequireSeperateFilename(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    swim_str = "swim"
    swim_file_ext = "txt"
    swim_filename = f"{swim_str}.{swim_file_ext}"
    swim_file_str = "swimming is good"
    print(f"{env_dir=} {swim_filename=}")
    swim_file_path = create_path(env_dir, swim_filename)
    assert os_path_exist(swim_file_path) is False

    # WHEN
    save_file(swim_file_path, filename=None, file_str=swim_file_str)

    # THEN
    assert os_path_exist(swim_file_path)


def test_get_dir_file_strs_correctlyGrabsFileData(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_filename = "x1.txt"
    x2_filename = "x2.txt"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    save_file(dest_dir=env_dir, filename=x1_filename, file_str=x1_file_str)
    save_file(dest_dir=env_dir, filename=x2_filename, file_str=x2_file_str)

    # WHEN
    files_dict = get_dir_file_strs(x_dir=env_dir)

    # THEN
    assert len(files_dict) == 2
    assert files_dict.get(x1_filename) == x1_file_str
    assert files_dict.get(x2_filename) == x2_file_str


def test_get_dir_file_strs_delete_extensions_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_filename = f"{x1_name}.{x1_file_ext}"
    x2_filename = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    save_file(dest_dir=env_dir, filename=x1_filename, file_str=x1_file_str)
    save_file(dest_dir=env_dir, filename=x2_filename, file_str=x2_file_str)

    # WHEN
    files_dict = get_dir_file_strs(x_dir=env_dir, delete_extensions=True)

    # THEN
    assert files_dict.get(x1_name) == x1_file_str
    assert files_dict.get(x2_name) == x2_file_str


def test_get_dir_file_strs_returnsSubDirs(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_filename = f"{x1_name}.{x1_file_ext}"
    x2_filename = f"{x2_name}.{x2_file_ext}"
    x1_file_str = "trying this"
    x2_file_str = "look there"
    save_file(
        dest_dir=f"{env_dir}/{x1_name}",
        filename=x1_filename,
        file_str=x1_file_str,
    )
    save_file(
        dest_dir=f"{env_dir}/{x2_name}",
        filename=x2_filename,
        file_str=x2_file_str,
    )

    # WHEN
    files_dict = get_dir_file_strs(
        x_dir=env_dir, delete_extensions=True, include_dirs=True
    )

    # THEN
    assert files_dict.get(x1_name) is True
    assert files_dict.get(x2_name) is True


def test_get_dir_file_strs_doesNotReturnsFiles(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_name = "x1"
    x1_file_ext = "txt"
    x1_filename = f"{x1_name}.{x1_file_ext}"
    x1_file_str = "trying this"
    save_file(dest_dir=env_dir, filename=x1_filename, file_str=x1_file_str)
    x2_name = "x2"
    x2_file_ext = "json"
    x2_filename = f"{x2_name}.{x2_file_ext}"
    x2_file_str = "look there"
    save_file(
        dest_dir=f"{env_dir}/{x2_name}",
        filename=x2_filename,
        file_str=x2_file_str,
    )

    # WHEN
    files_dict = get_dir_file_strs(x_dir=env_dir, include_files=False)

    # THEN
    print(f"{files_dict.get(x1_filename)=}")
    with pytest_raises(Exception) as excinfo:
        files_dict[x1_filename]
    assert str(excinfo.value) == "'x1.txt'"
    assert files_dict.get(x2_name) is True
    assert len(files_dict) == 1


def test_get_integer_filenames_ReturnsCoorectObjIfDirectoryDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    temp_dir = f"{env_dir}\\temp_does_not_exist"
    assert os_path_exist(temp_dir) is False

    # WHEN
    files_dict = get_integer_filenames(temp_dir, 0)

    # THEN
    assert len(files_dict) == 0
    assert files_dict == set()


def test_get_integer_filenames_GrabsFileNamesWith_Integers_v0(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_filename = "1.json"
    x2_filename = "2.json"
    x_file_str = "file strs"
    save_file(env_dir, x1_filename, x_file_str)
    save_file(env_dir, x2_filename, x_file_str)

    # WHEN
    files_dict = get_integer_filenames(env_dir, 0)

    # THEN
    assert len(files_dict) == 2
    assert files_dict == {1, 2}


def test_get_integer_filenames_GrabsFileNamesWith_IntegersWithCorrectExtension(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    z_filename = "z.json"
    x1_filename = "1.json"
    x2_filename = "2.json"
    txt1_filename = "1.txt"
    txt3_filename = "3.txt"
    x_file_str = "file strs"
    save_file(env_dir, z_filename, x_file_str)
    save_file(env_dir, x1_filename, x_file_str)
    save_file(env_dir, x2_filename, x_file_str)
    save_file(env_dir, txt1_filename, x_file_str)
    save_file(env_dir, txt3_filename, x_file_str)

    # WHEN
    files_dict = get_integer_filenames(env_dir, 0)

    # THEN
    assert len(files_dict) == 2
    assert files_dict == {1, 2}

    # WHEN / THEN
    assert get_integer_filenames(env_dir, 0, "txt") == {1, 3}
    assert get_integer_filenames(env_dir, None, "txt") == {1, 3}


def test_get_integer_filenames_GrabsFileNamesWith_IntegersGreaterThan_min_integer(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    z_filename = "z.json"
    x1_filename = "1.json"
    x2_filename = "2.json"
    x3_filename = "3.json"
    txt1_filename = "1.txt"
    txt3_filename = "3.txt"
    x_file_str = "file str"
    save_file(env_dir, z_filename, x_file_str)
    save_file(env_dir, x1_filename, x_file_str)
    save_file(env_dir, x2_filename, x_file_str)
    save_file(env_dir, x3_filename, x_file_str)
    save_file(env_dir, txt1_filename, x_file_str)
    save_file(env_dir, txt3_filename, x_file_str)

    # WHEN
    assert get_integer_filenames(env_dir, 2) == {2, 3}
    assert get_integer_filenames(env_dir, 0, "txt") == {1, 3}


def test_count_files_ReturnsNoneIfDirectoryDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    does_not_exist_dir = f"{env_dir}/swim"

    # WHEN
    dir_count = count_files(dir_path=does_not_exist_dir)

    # THEN
    assert dir_count is None


def test_get_directory_path_ReturnsObj():
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
    assert texas_path == f"{texas_str}"
    assert dallas_path == create_path(texas_str, dallas_str)
    assert elpaso_path == create_path(texas_str, elpaso_str)
    assert kern_path == create_path(elpaso_path, kern_str)


def test_is_path_valid_ReturnsObj():
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


def test_can_usser_edit_paths_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert can_usser_edit_paths()


def test_is_path_existent_or_creatable_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert is_path_existent_or_creatable("run")
    assert (
        platform_system() == "Windows"
        and is_path_existent_or_creatable("run/trail?") is False
    ) or platform_system() == "Linux"
    assert is_path_existent_or_creatable("run///trail")


def test_is_path_probably_creatable_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert is_path_probably_creatable("run")
    assert is_path_probably_creatable("run/trail?") is False
    assert is_path_probably_creatable("run///trail") is False


def test_is_path_existent_or_probably_creatable_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    """I am not able to test this correctly. For now make sure it runs."""
    assert is_path_existent_or_probably_creatable("run")
    assert is_path_existent_or_probably_creatable("run/trail?") is False
    assert is_path_existent_or_probably_creatable("run///trail") is False


def test_get_all_dirs_with_file_ReturnsCorrectDirectories(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_filename = "x1.txt"
    x1_file_str = "trying this"
    iowa_rel_dir = "iowa/dallas"
    ohio_rel_dir = "ohio/elpaso"
    iowa_dir = f"{env_dir}/{iowa_rel_dir}"
    ohio_dir = f"{env_dir}/{ohio_rel_dir}"
    save_file(dest_dir=iowa_dir, filename=x1_filename, file_str=x1_file_str)
    save_file(dest_dir=ohio_dir, filename=x1_filename, file_str=x1_file_str)

    # WHEN
    directory_set = get_all_dirs_with_file(x_filename=x1_filename, x_dir=env_dir)

    # THEN
    assert directory_set == {iowa_rel_dir, ohio_rel_dir}


def test_get_dir_filenames_ReturnsObj_Scenario0_NoFilter(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_filename = "x1.txt"
    x2_filename = "x2.txt"
    iowa_rel_dir = "iowa/dallas"
    ohio_rel_dir = "ohio/elpaso"
    iowa_dir = f"{env_dir}/{iowa_rel_dir}"
    ohio_dir = f"{env_dir}/{ohio_rel_dir}"
    save_file(iowa_dir, x1_filename, "")
    save_file(iowa_dir, x2_filename, "")
    save_file(ohio_dir, x2_filename, "")

    # WHEN
    filenames_set = get_dir_filenames(env_dir)

    # THEN
    assert (iowa_rel_dir, x1_filename) in filenames_set
    assert (iowa_rel_dir, x2_filename) in filenames_set
    assert (ohio_rel_dir, x2_filename) in filenames_set
    assert len(filenames_set) == 3


def test_get_dir_filenames_ReturnsObj_Scenario0_NoFilter(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_filename = "x1.txt"
    x2_filename = "x2.txt"
    iowa_rel_dir = "iowa/dallas"
    ohio_rel_dir = "ohio/elpaso"
    iowa_dir = f"{env_dir}/{iowa_rel_dir}"
    ohio_dir = f"{env_dir}/{ohio_rel_dir}"
    save_file(iowa_dir, x1_filename, "")
    save_file(iowa_dir, x2_filename, "")
    save_file(ohio_dir, x2_filename, "")

    # WHEN
    filenames_set = get_dir_filenames(env_dir)

    # THEN
    assert (iowa_rel_dir, x1_filename) in filenames_set
    assert (iowa_rel_dir, x2_filename) in filenames_set
    assert (ohio_rel_dir, x2_filename) in filenames_set
    assert len(filenames_set) == 3


def test_get_dir_filenames_ReturnsObj_Scenario1_FilterByExtension(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_filename = "x1.txt"
    x2_filename = "x2.json"
    iowa_rel_dir = "iowa/dallas"
    ohio_rel_dir = "ohio/elpaso"
    iowa_dir = f"{env_dir}/{iowa_rel_dir}"
    ohio_dir = f"{env_dir}/{ohio_rel_dir}"
    save_file(iowa_dir, x1_filename, "")
    save_file(iowa_dir, x2_filename, "")
    save_file(ohio_dir, x2_filename, "")

    # WHEN
    filenames_set = get_dir_filenames(env_dir, include_extensions={"json"})

    # THEN
    print(f"{filenames_set=}")
    assert (iowa_rel_dir, x1_filename) not in filenames_set
    assert (iowa_rel_dir, x2_filename) in filenames_set
    assert (ohio_rel_dir, x2_filename) in filenames_set
    assert len(filenames_set) == 2


def test_get_dir_filenames_ReturnsObj_Scenario2_FilterByExtension(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x1_filename = "br.txt"
    x2_filename = "x2.json"
    x3_filename = "x3.json"
    x4_filename = "x4.json"
    iowa_rel_dir = "iowa/dallas"
    ohio_rel_dir = "ohio/elpaso"
    iowa_dir = f"{env_dir}/{iowa_rel_dir}"
    ohio_dir = f"{env_dir}/{ohio_rel_dir}"
    save_file(iowa_dir, x1_filename, "")
    save_file(iowa_dir, x2_filename, "")
    save_file(ohio_dir, x2_filename, "")
    save_file(ohio_dir, x3_filename, "")
    save_file(ohio_dir, x4_filename, "")

    # WHEN
    filenames_matching = {x1_filename, x3_filename}
    filenames_set = get_dir_filenames(env_dir, matchs=filenames_matching)

    # THEN
    print(f"{filenames_set=}")
    assert (iowa_rel_dir, x1_filename) in filenames_set
    assert (iowa_rel_dir, x2_filename) not in filenames_set
    assert (ohio_rel_dir, x2_filename) not in filenames_set
    assert (ohio_rel_dir, x3_filename) in filenames_set
    assert (ohio_rel_dir, x4_filename) not in filenames_set
    assert len(filenames_set) == 2


def test_get_max_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_module_temp_dir()
    six_int = 6
    ten_int = 10
    save_file(x_dir, f"{six_int}.json", "fizzbuzz")
    save_file(x_dir, f"{ten_int}.json", "fizzbuzz")

    # WHEN / THEN
    assert get_max_file_number(x_dir) == ten_int


def test_get_max_file_number_ReturnsObjWhenDirIsEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_module_temp_dir()

    # WHEN / THEN
    assert get_max_file_number(x_dir) is None
