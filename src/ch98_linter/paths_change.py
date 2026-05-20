from ch98_linter.chapter_move_tool import rename_files_and_dirs_4times
from os import getcwd as os_getcwd
from os.path import isdir as os_path_isdir

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python -m src.linter.paths_change -x


def paths_change_main():
    src_dir = os_getcwd()
    find_str = input("Find string:    ").strip()
    replace_str = input("Replace string: ").strip()
    print(f"Goal is to move {find_str} to {replace_str}")

    if os_path_isdir(src_dir) is False:
        print("Error: directory does not exist.")
        return
