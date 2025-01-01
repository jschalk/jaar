def get_test_cmty_idea():
    return "accord_45"


def get_cmty_idea_if_None(cmty_idea: str = None):
    return get_test_cmty_idea() if cmty_idea is None else cmty_idea


def get_test_cmtys_dir():
    return "src/f07_cmty/examples/cmtys"


def get_gifts_folder() -> str:
    return "gifts"


def init_gift_id() -> int:
    return 0


def get_init_gift_id_if_None(x_gift_id: int = None) -> int:
    return init_gift_id() if x_gift_id is None else x_gift_id


def get_json_filename(filename_without_extention) -> str:
    return f"{filename_without_extention}.json"


def voice_str() -> str:
    return "voice"


def final_str() -> str:
    return "final"


def jobs_str() -> str:
    return "jobs"


def dutys_str() -> str:
    return "dutys"


def grades_folder() -> str:
    return "grades"


def get_rootpart_of_keep_dir() -> str:
    return "itemroot"


def treasury_file_name() -> str:
    return "treasury.db"


def max_tree_traverse_default() -> int:
    return 20


def get_descending_str() -> str:
    return "descending"


def default_river_blocks_count() -> int:
    return 40


def default_unknown_word() -> str:
    return "UNKNOWN"


def default_unknown_word_if_None(unknown_word: any = None) -> str:
    if unknown_word != unknown_word:
        unknown_word = None
    if unknown_word is None:
        unknown_word = default_unknown_word()
    return unknown_word
