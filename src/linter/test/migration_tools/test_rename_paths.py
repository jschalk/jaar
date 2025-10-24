from os import mkdir as os_mkdir
from os.path import (
    basename as os_path_basename,
    exists as os_path_exists,
    join as os_path_join,
)
from src.ch01_py.file_toolbox import create_path, get_dir_file_strs, save_file
from src.linter.chapter_migration_tools import (
    delete_if_empty_or_pycache_only,
    first_level_dirs_with_prefix,
    rename_files_and_folders,
    rename_files_and_folders_4times,
)
from src.linter.test._util.linter_env import get_temp_dir, temp_dir_setup
from tempfile import TemporaryDirectory as tempfile_TemporaryDirectory


def test_first_level_dirs_with_prefix_ReturnsObj():
    with tempfile_TemporaryDirectory() as tmpdir:
        # Setup directories
        os_mkdir(os_path_join(tmpdir, "ch03_yahoo"))
        os_mkdir(os_path_join(tmpdir, "ch03_google"))
        os_mkdir(os_path_join(tmpdir, "ch03_yahoo_temp"))
        os_mkdir(os_path_join(tmpdir, "other_dir"))

        # Nested dir should not be included
        nested_dir = os_path_join(tmpdir, "ch03_yahoo", "temp")
        os_mkdir(nested_dir)

        # Test prefix "ch03"
        prefix_path = os_path_join(tmpdir, "ch03")
        result = first_level_dirs_with_prefix(prefix_path)
        result_names = [os_path_basename(p) for p in result]

        assert set(result_names) == {"ch03_yahoo", "ch03_google", "ch03_yahoo_temp"}
        # nested dir should not appear
        assert "temp" not in result_names

        # Test prefix that matches nothing
        prefix_path = os_path_join(tmpdir, "nonexistent")
        result = first_level_dirs_with_prefix(prefix_path)
        assert result == []

        # Test prefix that matches only one
        prefix_path = os_path_join(tmpdir, "other")
        result = first_level_dirs_with_prefix(prefix_path)
        result_names = [os_path_basename(p) for p in result]
        assert result_names == ["other_dir"]


def test_delete_if_empty_or_pycache_only_DeletesDir():
    with tempfile_TemporaryDirectory() as tmpdir:
        # Case 1: empty dir → should delete
        d1 = os_path_join(tmpdir, "empty_dir")
        os_mkdir(d1)
        assert delete_if_empty_or_pycache_only(d1)
        assert not os_path_exists(d1)

        # Case 2: only __pycache__ with .pyc → should delete
        d2 = os_path_join(tmpdir, "only_pycache")
        os_mkdir(d2)
        pyc_dir = os_path_join(d2, "__pycache__")
        os_mkdir(pyc_dir)
        open(os_path_join(pyc_dir, "file.pyc"), "w").close()
        assert delete_if_empty_or_pycache_only(d2)
        assert not os_path_exists(d2)

        # Case 3: __pycache__ with extra non-.pyc file → should NOT delete
        d3 = os_path_join(tmpdir, "bad_pycache")
        os_mkdir(d3)
        pyc_dir = os_path_join(d3, "__pycache__")
        os_mkdir(pyc_dir)
        open(os_path_join(pyc_dir, "file.txt"), "w").close()
        assert os_path_exists(d3)
        # WHEN
        delete_if_empty_or_pycache_only(d3)
        # THEN
        assert os_path_exists(d3)

        # Case 4: directory with a normal file → should NOT delete
        d4 = os_path_join(tmpdir, "nonempty_dir")
        os_mkdir(d4)
        open(os_path_join(d4, "somefile.py"), "w").close()
        assert not delete_if_empty_or_pycache_only(d4)
        assert os_path_exists(d4)

        # Case 5: nonexistent directory → should NOT delete
        d5 = os_path_join(tmpdir, "does_not_exist")
        assert not delete_if_empty_or_pycache_only(d5)


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
    assert os_path_exists(temp_dolphin_path)
    assert os_path_exists(dot_git_file_path)

    # WHEN
    rename_files_and_folders(temp_dir, "dol", "bob")

    # THEN
    assert not os_path_exists(temp_dolphin_path)
    temp_bobphin_path = create_path(temp_dir, "bobphin.txt")
    assert os_path_exists(temp_bobphin_path)
    assert os_path_exists(dot_git_file_path)


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
):  # sourcery skip: extract-duplicate-method
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
):  # sourcery skip: extract-duplicate-method
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
    assert os_path_exists(dolphin_dir)
    assert os_path_exists(bobphin_dir) == False

    # WHEN
    rename_files_and_folders_4times(env_dir, "dol", "bob")

    # THEN
    bobphin_files_dict = get_dir_file_strs(bobphin_dir)
    assert len(bobphin_files_dict) == 2
    assert bobphin_files_dict.get(dolphin_file_name) is None
    bobphin_file_name = f"{bobphin_text}.json"
    assert bobphin_files_dict.get(lopster_file_name) == lopster_file_text
    assert bobphin_files_dict.get(bobphin_file_name) == dolphin_file_text
    assert os_path_exists(dolphin_dir) == False
    assert os_path_exists(bobphin_dir)


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
    assert os_path_exists(dolphin_dir)
    assert os_path_exists(bobphin_dir) == False

    # WHEN
    rename_files_and_folders_4times(env_dir, "dol", "bob")

    # THEN
    bobphin_files_dict = get_dir_file_strs(bobphin_dir)
    assert len(bobphin_files_dict) == 3
    assert bobphin_files_dict.get(dolphin_file_name) is None
    bobphin_file_name = f"{bobphin_text}.json"
    assert bobphin_files_dict.get(lopster_file_name) == lopster_file_text
    assert bobphin_files_dict.get(bobphin_file_name) == dolphin_file_text
    assert os_path_exists(dolphin_dir) == False
    assert os_path_exists(bobphin_dir)
