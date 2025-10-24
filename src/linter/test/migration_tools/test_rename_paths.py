from os.path import exists as os_path_exist
from src.ch01_py.file_toolbox import create_path, get_dir_file_strs, save_file
from src.linter.chapter_migration_tools import (
    rename_files_and_folders,
    rename_files_and_folders_4times,
)
from src.linter.test._util.linter_env import get_temp_dir, temp_dir_setup


def test_rename_files_and_folders_NotChangesWhenNoneNeeded(temp_dir_setup):
    # GIVEN
    env_dir = get_temp_dir()
    dolphin_file_name = "dolphin.txt"
    lopster_file_name = "lopster.txt"
    dolphin_file_text = "trying this"
    lopster_file_text = "look there"
    save_file(env_dir, filename=dolphin_file_name, file_str=dolphin_file_text)
    save_file(env_dir, filename=lopster_file_name, file_str=lopster_file_text)
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) == dolphin_file_text
    assert files_dict.get(lopster_file_name) == lopster_file_text

    # WHEN
    rename_files_and_folders(env_dir, "Bob", "Sue")

    # THEN
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) == dolphin_file_text
    assert files_dict.get(lopster_file_name) == lopster_file_text


def test_rename_files_and_folders_NoChangeTo_dot_git_Folders(temp_dir_setup):
    # GIVEN
    temp_dir = get_temp_dir()
    dot_git_dir = create_path(temp_dir, ".git")
    dolphin_file_name = "dolphin.txt"
    dot_git_file_path = create_path(dot_git_dir, dolphin_file_name)
    temp_dolphin_path = create_path(temp_dir, dolphin_file_name)
    dolphin_file_text = "trying this"
    save_file(dot_git_file_path, None, dolphin_file_text)
    save_file(temp_dolphin_path, None, dolphin_file_text)
    assert os_path_exist(temp_dolphin_path)
    assert os_path_exist(dot_git_file_path)

    # WHEN
    rename_files_and_folders(temp_dir, "dol", "bob")

    # THEN
    assert not os_path_exist(temp_dolphin_path)
    temp_bobphin_path = create_path(temp_dir, "bobphin.txt")
    assert os_path_exist(temp_bobphin_path)
    assert os_path_exist(dot_git_file_path)


def test_rename_files_and_folders_ChangesWhenNeeded_lowercase(temp_dir_setup):
    # GIVEN
    env_dir = get_temp_dir()
    dolphin_file_name = "dolphin.json"
    lopster_file_name = "lopster.json"
    dolphin_file_text = "trying this"
    lopster_file_text = "look there"
    save_file(env_dir, filename=dolphin_file_name, file_str=dolphin_file_text)
    save_file(env_dir, filename=lopster_file_name, file_str=lopster_file_text)
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) == dolphin_file_text
    assert files_dict.get(lopster_file_name) == lopster_file_text

    # WHEN
    rename_files_and_folders(env_dir, "dol", "bob")

    # THEN
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) is None
    bobphin_file_name = "bobphin.json"
    assert files_dict.get(lopster_file_name) == lopster_file_text
    assert files_dict.get(bobphin_file_name) == dolphin_file_text


def test_rename_files_and_folders_NoChangesWith_lowercase_parameters(
    temp_dir_setup,
):
    # GIVEN
    env_dir = get_temp_dir()
    dolphin_file_name = "dolphin.json"
    lopster_file_name = "lopster.json"
    dolphin_file_text = "trying this"
    lopster_file_text = "look there"
    save_file(env_dir, filename=dolphin_file_name, file_str=dolphin_file_text)
    save_file(env_dir, filename=lopster_file_name, file_str=lopster_file_text)
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) == dolphin_file_text
    assert files_dict.get(lopster_file_name) == lopster_file_text

    # WHEN
    rename_files_and_folders(env_dir, "Dol", "bob")

    # THEN
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) == dolphin_file_text
    bobphin_file_name = "bobphin.json"
    assert files_dict.get(lopster_file_name) == lopster_file_text
    assert files_dict.get(bobphin_file_name) is None


def test_rename_files_and_folders_NoChangesWith_lowercase_filenames(
    temp_dir_setup,
):
    # GIVEN
    env_dir = get_temp_dir()
    dolphin_file_name = "Dolphin.json"
    lopster_file_name = "lopster.json"
    dolphin_file_text = "trying this"
    lopster_file_text = "look there"
    save_file(env_dir, filename=dolphin_file_name, file_str=dolphin_file_text)
    save_file(env_dir, filename=lopster_file_name, file_str=lopster_file_text)
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) == dolphin_file_text
    assert files_dict.get(lopster_file_name) == lopster_file_text

    # WHEN
    rename_files_and_folders(env_dir, "dol", "bob")

    # THEN
    files_dict = get_dir_file_strs(env_dir)
    assert len(files_dict) == 2
    assert files_dict.get(dolphin_file_name) == dolphin_file_text
    bobphin_file_name = "bobphin.json"
    assert files_dict.get(lopster_file_name) == lopster_file_text
    assert files_dict.get(bobphin_file_name) is None


def test_rename_files_and_folders_ChangesWhenNeeded_directory(
    temp_dir_setup,
):
    # GIVEN
    env_dir = get_temp_dir()
    dolphine_text = "dolphin"
    dolphin_dir = f"{env_dir}/{dolphine_text}"
    dolphin_file_name = f"{dolphine_text}.json"
    lopster_file_name = "lopster.json"
    dolphin_file_text = "trying this"
    lopster_file_text = "look there"
    save_file(dolphin_dir, dolphin_file_name, file_str=dolphin_file_text)
    save_file(dolphin_dir, lopster_file_name, file_str=lopster_file_text)
    dolphin_files_dict = get_dir_file_strs(dolphin_dir)
    assert len(dolphin_files_dict) == 2
    assert dolphin_files_dict.get(dolphin_file_name) == dolphin_file_text
    assert dolphin_files_dict.get(lopster_file_name) == lopster_file_text
    bobphin_text = "bobphin"
    bobphin_dir = f"{env_dir}/{bobphin_text}"
    assert os_path_exist(dolphin_dir)
    assert os_path_exist(bobphin_dir) == False

    # WHEN
    rename_files_and_folders_4times(env_dir, "dol", "bob")

    # THEN
    bobphin_files_dict = get_dir_file_strs(bobphin_dir)
    assert len(bobphin_files_dict) == 2
    assert bobphin_files_dict.get(dolphin_file_name) is None
    bobphin_file_name = f"{bobphin_text}.json"
    assert bobphin_files_dict.get(lopster_file_name) == lopster_file_text
    assert bobphin_files_dict.get(bobphin_file_name) == dolphin_file_text
    assert os_path_exist(dolphin_dir) == False
    assert os_path_exist(bobphin_dir)


def test_rename_files_and_folders_ChangesWhenNeeded_delete_old_directorys(
    temp_dir_setup,
):
    # GIVEN
    env_dir = get_temp_dir()
    dolphine_text = "dolphin"
    dolphin_dir = f"{env_dir}/{dolphine_text}"
    dolphin_file_name = f"{dolphine_text}.json"
    lopster_file_name = "lopster.json"
    dolphin_file_text = "trying this"
    lopster_file_text = "look there"
    save_file(dolphin_dir, dolphin_file_name, file_str=dolphin_file_text)
    save_file(dolphin_dir, lopster_file_name, file_str=lopster_file_text)
    save_file(dolphin_dir, "penguin.txt", file_str="huh")
    dolphin_files_dict = get_dir_file_strs(dolphin_dir)
    assert len(dolphin_files_dict) == 3
    assert dolphin_files_dict.get(dolphin_file_name) == dolphin_file_text
    assert dolphin_files_dict.get(lopster_file_name) == lopster_file_text
    bobphin_text = "bobphin"
    bobphin_dir = f"{env_dir}/{bobphin_text}"
    assert os_path_exist(dolphin_dir)
    assert os_path_exist(bobphin_dir) == False

    # WHEN
    rename_files_and_folders_4times(env_dir, "dol", "bob")

    # THEN
    bobphin_files_dict = get_dir_file_strs(bobphin_dir)
    assert len(bobphin_files_dict) == 3
    assert bobphin_files_dict.get(dolphin_file_name) is None
    bobphin_file_name = f"{bobphin_text}.json"
    assert bobphin_files_dict.get(lopster_file_name) == lopster_file_text
    assert bobphin_files_dict.get(bobphin_file_name) == dolphin_file_text
    assert os_path_exist(dolphin_dir) == False
    assert os_path_exist(bobphin_dir)
