def get_test_fiscal_title():
    return "accord_45"


def get_fiscal_title_if_None(fiscal_title: str = None):
    return get_test_fiscal_title() if fiscal_title is None else fiscal_title


def get_test_fiscals_dir():
    return "src/f07_fiscal/examples/fiscals"


def get_owners_folder() -> str:
    return "owners"


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
