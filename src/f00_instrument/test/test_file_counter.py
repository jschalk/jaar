import pytest
from pathlib import Path
import tempfile
import shutil
from src.f00_instrument.file import count_dirs_files, save_file, create_path


@pytest.fixture
def test_directory():
    """Fixture to create a temporary directory with files and subdirectories."""
    test_dir = Path(tempfile.mkdtemp())  # Create a temp directory

    # Create subdirectories
    (test_dir / "subdir1").mkdir()
    (test_dir / "subdir2").mkdir()

    # Create files
    (test_dir / "file1.txt").touch()
    (test_dir / "file2.log").touch()
    (test_dir / "subdir1/file3.doc").touch()  # File inside subdir (should be counted)

    yield test_dir  # Provide the test directory to the test function

    # Cleanup after the test
    shutil.rmtree(test_dir)


def test_count_dirs_files(test_directory):
    # ESTABLISH / WHEN / THEN
    assert count_dirs_files(test_directory) == 5

    # WHEN / THEN
    save_file(test_directory, "testing.txt", "")
    assert count_dirs_files(test_directory) == 6

    # WHEN / THEN
    test2_dir = create_path(test_directory, "testing2")
    save_file(test2_dir, "testing.txt", "")
    assert count_dirs_files(test_directory) == 8
