from src.ch01_py.file_toolbox import get_dir_file_strs
from src.linter.style import get_chapter_descs


def test_check_Chapters_filenames_FollowFileNameConventions_NoNamingCollision():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    all_level1_py_files = set()
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        level1_py_files = set(get_dir_file_strs(chapter_dir, True, False, True).keys())
        all_level1_py_files.update(level1_py_files)
        # print(f"{level1_py_files=}")
        base_map = {}

        for focus_filenamebase in level1_py_files:
            for check_filenamebase in level1_py_files:
                if check_filenamebase.find(focus_filenamebase) > -1:
                    if base_map.get(focus_filenamebase) is None:
                        base_map[focus_filenamebase] = []
                    base_map[focus_filenamebase].append(check_filenamebase)

        collisions = []
        for name_group in base_map.values():
            if len(name_group) > 1:
                collisions.extend(name_group)
        if collisions:
            print(f"{chapter_desc} {collisions=}")
        assert not collisions

    # CHECK for collisions acress chapters
    # all_base_map = {}

    # for focus_filenamebase in all_level1_py_files:
    #     for check_filenamebase in all_level1_py_files:
    #         if check_filenamebase.find(focus_filenamebase) > -1:
    #             if all_base_map.get(focus_filenamebase) is None:
    #                 all_base_map[focus_filenamebase] = []
    #             all_base_map[focus_filenamebase].append(check_filenamebase)

    # all_collisions = []
    # for name_group in all_base_map.values():
    #     if len(name_group) > 1:
    #         all_collisions.extend(name_group)
    # if all_collisions:
    #     print(f"{chapter_desc} {all_collisions=}")
    # assert not all_collisions
