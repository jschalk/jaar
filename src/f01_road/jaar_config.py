def get_test_fisc_title():
    return "accord_45"


def get_fisc_title_if_None(fisc_title: str = None):
    return get_test_fisc_title() if fisc_title is None else fisc_title


def get_test_fisc_mstr_dir():
    return "src/f08_fisc/examples/fisc_mstr"


def get_owners_folder() -> str:
    return "owners"


def get_vows_folder() -> str:
    return "vows"


def init_vow_id() -> int:
    return 0


def get_init_vow_id_if_None(x_vow_id: int = None) -> int:
    return init_vow_id() if x_vow_id is None else x_vow_id


def get_json_filename(filename_without_extention) -> str:
    return f"{filename_without_extention}.json"


def voice_str() -> str:
    return "voice"


def forecast_str() -> str:
    return "forecast"


def jobs_str() -> str:
    return "jobs"


def dutys_str() -> str:
    return "dutys"


def grades_folder() -> str:
    return "grades"


def get_rootpart_of_keep_dir() -> str:
    return "itemroot"


def treasury_filename() -> str:
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
