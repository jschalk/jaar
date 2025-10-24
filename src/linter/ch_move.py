from os import getcwd as os_getcwd
from os.path import isdir as os_path_isdir
from src.ch01_py.file_toolbox import create_path
from src.linter.chapter_migration_tools import (
    delete_if_empty_or_pycache_only,
    first_level_dirs_with_prefix,
    rename_files_and_folders_4times,
    replace_in_tracked_python_files,
    string_exists_in_directory,
    string_exists_in_filepaths,
)


def main():
    src_dir = create_path(os_getcwd(), "src")
    src_chxx_str = input("Chapter to move (int): ").strip()
    dst_chxx_str = input("Chapter destina (int): ").strip()
    src_chxx_int = int(src_chxx_str)
    dst_chxx_int = int(dst_chxx_str)
    src_chxx_prefix = f"ch{src_chxx_int:02}"
    dst_chxx_prefix = f"ch{dst_chxx_int:02}"
    print(f"Goal is to move {src_chxx_prefix} to {dst_chxx_prefix}")

    # Sanity checks
    for prefix_dir in first_level_dirs_with_prefix(dst_chxx_prefix):
        delete_if_empty_or_pycache_only(prefix_dir)
    if not os_path_isdir(src_dir):
        print("Error: directory does not exist.")
        return

    if string_exists_in_filepaths(src_dir, dst_chxx_prefix):
        print(f"❌ The new string '{dst_chxx_prefix}' already exists in file paths.")
        return

    if string_exists_in_directory(src_dir, dst_chxx_prefix):
        print(f"❌ The new string '{dst_chxx_prefix}' already exists in file contents.")
        return

    rename_files_and_folders_4times(src_dir, src_chxx_prefix, dst_chxx_prefix)
    replace_in_tracked_python_files(src_chxx_prefix, replace_text=dst_chxx_prefix)
    # print("✅ Replacement complete.")


if __name__ == "__main__":
    main()
