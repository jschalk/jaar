from os import chdir as os_chdir
from pathlib import Path
from src.linter.chapter_migration_tools import (
    replace_in_tracked_python_files,
    string_exists_in_directory,
    string_exists_in_filepaths,
)
from subprocess import run as subprocess_run

# replace with your actual module name


def test_string_exists_in_filepaths(tmp_path):
    # sourcery skip: extract-duplicate-method
    # Setup: create some files and folders
    subdir = tmp_path / "project_data"
    subdir.mkdir()
    (subdir / "notes.txt").write_text("irrelevant text", encoding="utf-8")
    (subdir / "script.py").write_text("print('ok')", encoding="utf-8")

    hidden_dir = tmp_path / "backup_hidden"
    hidden_dir.mkdir()
    (hidden_dir / "old_version.txt").write_text("outdated", encoding="utf-8")

    assert not string_exists_in_filepaths(tmp_path, "forbidden")
    assert string_exists_in_filepaths(tmp_path, "backup")
    assert string_exists_in_filepaths(tmp_path, "notes")
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    assert not string_exists_in_filepaths(empty_dir, "anything")


def test_string_exists_in_directory(tmp_path):
    # Setup: create temporary directory with files
    dir1 = tmp_path / "dir1"
    dir1.mkdir()

    file1 = dir1 / "a.txt"
    file2 = dir1 / "b.txt"
    file3 = dir1 / "c.bin"

    file1.write_text("This is a test file.\nNothing special here.", encoding="utf-8")
    file2.write_text("Another file with a secret keyword inside.", encoding="utf-8")
    file3.write_bytes(b"\x00\x01\x02")  # binary file (should be skipped safely)

    # Case 1: keyword exists in one file
    assert string_exists_in_directory(tmp_path, "keyword") is True

    # Case 2: keyword does not exist anywhere
    assert string_exists_in_directory(tmp_path, "nonexistentstring") is False

    # Case 3: empty directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    assert string_exists_in_directory(empty_dir, "anything") is False


def test_replace_in_tracked_python_files(tmp_path):
    # Create a temporary git repo
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess_run(["git", "init"], cwd=repo_dir, check=True)

    # Create a tracked Python file
    py_file = repo_dir / "example.py"
    py_file.write_text("print('hello world')\n", encoding="utf-8")
    subprocess_run(["git", "add", "example.py"], cwd=repo_dir, check=True)
    subprocess_run(["git", "commit", "-m", "initial commit"], cwd=repo_dir, check=True)

    # Create an untracked Python file (should not be touched)
    untracked = repo_dir / "temp.py"
    untracked.write_text("print('hello world')\n", encoding="utf-8")

    # Run replacement
    os_chdir(repo_dir)  # must be inside the repo for git ls-files
    replace_in_tracked_python_files("hello world", "goodbye")

    # Verify tracked file was changed
    new_content = py_file.read_text(encoding="utf-8")
    assert "goodbye" in new_content
    assert "hello world" not in new_content

    # Verify untracked file was not changed
    untracked_content = untracked.read_text(encoding="utf-8")
    assert "hello world" in untracked_content
