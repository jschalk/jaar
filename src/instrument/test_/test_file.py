from src.instrument.file import (
    dir_files,
    save_file,
    open_file,
    count_files,
    get_directory_path,
)
from src.agenda.examples.agenda_env import (
    get_agenda_temp_env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_dir_files_correctlyGrabsFileData(env_dir_setup_cleanup):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x1_file_name = "x1.txt"
    x2_file_name = "x2.txt"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN
    files_dict = dir_files(dir_path=env_dir)

    # THEN
    assert len(files_dict) == 2
    assert files_dict.get(x1_file_name) == x1_file_text
    assert files_dict.get(x2_file_name) == x2_file_text


def test_dir_files_delete_extensions_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN
    files_dict = dir_files(dir_path=env_dir, delete_extensions=True)

    # THEN
    assert files_dict.get(x1_name) == x1_file_text
    assert files_dict.get(x2_name) == x2_file_text


def test_dir_files_returnsSubDirs(env_dir_setup_cleanup):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    save_file(
        dest_dir=f"{env_dir}/{x1_name}",
        file_name=x1_file_name,
        file_text=x1_file_text,
    )
    save_file(
        dest_dir=f"{env_dir}/{x2_name}",
        file_name=x2_file_name,
        file_text=x2_file_text,
    )

    # WHEN
    files_dict = dir_files(dir_path=env_dir, delete_extensions=True, include_dirs=True)

    # THEN
    assert files_dict.get(x1_name) == True
    assert files_dict.get(x2_name) == True


def test_dir_files_doesNotReturnsFiles(env_dir_setup_cleanup):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x1_name = "x1"
    x1_file_ext = "txt"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x1_file_text = "trying this"
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    x2_name = "x2"
    x2_file_ext = "json"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x2_file_text = "look there"
    save_file(
        dest_dir=f"{env_dir}/{x2_name}",
        file_name=x2_file_name,
        file_text=x2_file_text,
    )

    # WHEN
    files_dict = dir_files(dir_path=env_dir, include_files=False)

    # THEN
    print(f"{files_dict.get(x1_file_name)=}")
    with pytest_raises(Exception) as excinfo:
        files_dict[x1_file_name]
    assert str(excinfo.value) == "'x1.txt'"
    assert files_dict.get(x2_name) == True
    assert len(files_dict) == 1


def test_open_file_OpensFilesCorrectlyWhenGivenDirectoryAndFileName(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    print(f"{env_dir=} {x1_file_name=}")
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN / THEN
    assert open_file(dest_dir=env_dir, file_name=x1_file_name) == x1_file_text
    assert open_file(dest_dir=env_dir, file_name=x2_file_name) == x2_file_text


def test_open_file_OpensFilesCorrectlyWhenGivenOnlyFilePath(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    x1_file_path = f"{env_dir}/{x1_file_name}"
    x2_file_path = f"{env_dir}/{x2_file_name}"

    print(f"{env_dir=} {x1_file_name=}")
    print(f"{env_dir=} {x1_file_name=}")
    save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN / THEN
    assert open_file(dest_dir=x1_file_path, file_name=None) == x1_file_text
    assert open_file(dest_dir=x2_file_path, file_name=None) == x2_file_text


def test_save_file_ReplacesFileAsDefault(env_dir_setup_cleanup):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x_old_name = "x_old"
    # x_new_name = "x_new"
    x_old_file_ext = "txt"
    # x_new_file_ext = "json"
    x_old_file_name = f"{x_old_name}.{x_old_file_ext}"
    # x_new_file_name = f"{x_new_name}.{x_new_file_ext}"
    x_old_file_text = "trying this"
    x_new_file_text = "look there"
    print(f"{env_dir=} {x_old_file_name=}")
    save_file(dest_dir=env_dir, file_name=x_old_file_name, file_text=x_old_file_text)
    assert open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_old_file_text

    # WHEN
    save_file(
        dest_dir=env_dir,
        file_name=x_old_file_name,
        file_text=x_new_file_text,
        replace=None,
    )

    # THEN
    assert open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_new_file_text


def test_save_file_DoesNotreplaceFile(env_dir_setup_cleanup):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    x_old_name = "x_old"
    # x_new_name = "x_new"
    x_old_file_ext = "txt"
    # x_new_file_ext = "json"
    x_old_file_name = f"{x_old_name}.{x_old_file_ext}"
    # x_new_file_name = f"{x_new_name}.{x_new_file_ext}"
    x_old_file_text = "trying this"
    x_new_file_text = "look there"
    print(f"{env_dir=} {x_old_file_name=}")
    save_file(dest_dir=env_dir, file_name=x_old_file_name, file_text=x_old_file_text)
    assert open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_old_file_text

    # WHEN
    save_file(
        dest_dir=env_dir,
        file_name=x_old_file_name,
        file_text=x_new_file_text,
        replace=False,
    )

    # THEN
    assert open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_old_file_text


def test_count_files_ReturnsNoneIfDirectoryDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_agenda_temp_env_dir()
    does_not_exist_dir = f"{env_dir}/swim"

    # WHEN
    dir_count = count_files(dir_path=does_not_exist_dir)

    # THEN
    assert dir_count is None


def test_get_directory_path_ReturnsCorrectObj():
    # GIVEN
    texas_text = "texas"
    dallas_text = "dallas"
    elpaso_text = "el paso"
    kern_text = "kern"

    # WHEN
    texas_path = get_directory_path([texas_text])
    dallas_path = get_directory_path([texas_text, dallas_text])
    elpaso_path = get_directory_path([texas_text, elpaso_text])
    kern_path = get_directory_path([texas_text, elpaso_text, kern_text])

    # THEN
    assert "" == get_directory_path()
    assert texas_path == f"/{texas_text}"
    assert dallas_path == f"/{texas_text}/{dallas_text}"
    assert elpaso_path == f"/{texas_text}/{elpaso_text}"
    assert kern_path == f"/{texas_text}/{elpaso_text}/{kern_text}"
