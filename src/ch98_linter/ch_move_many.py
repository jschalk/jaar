from ch00_py.file_toolbox import open_json, save_json
from ch98_linter.ch_move1 import ch_move_main
from os import getcwd as os_getcwd
from os.path import isdir as os_path_isdir, join as os_path_join

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python -m src.linter.chapter_move_main


def ch_many_move_main():
    lower_chxx_str = input("Lower chapter (int): ").strip()
    upper_chxx_str = input("Upper chapter (int): ").strip()
    move_number = input("Move chapters how many? (int): ").strip()
    lower_chxx_int = int(lower_chxx_str)
    upper_chxx_int = int(upper_chxx_str)
    move_number_int = int(move_number)
    for x_num in sorted(range(lower_chxx_int, upper_chxx_int + 1), reverse=True):
        print(f"from {x_num} to {x_num+move_number_int}")


if __name__ == "__main__":
    ch_many_move_main()
