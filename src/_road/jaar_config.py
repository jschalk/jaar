def get_test_tribe_id():
    return "music_45"


def get_tribe_id_if_None(tribe_id: str = None):
    return get_test_tribe_id() if tribe_id is None else tribe_id


def get_test_tribes_dir():
    return "src/tribe/examples/tribes"


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


def action_str() -> str:
    return "action"


def jobs_str() -> str:
    return "jobs"


def dutys_str() -> str:
    return "dutys"


def grades_folder() -> str:
    return "grades"


def get_rootpart_of_econ_dir() -> str:
    return "idearoot"


def treasury_file_name() -> str:
    return "treasury.db"


def max_tree_traverse_default() -> int:
    return 20


def get_descending_str() -> str:
    return "descending"


def default_river_blocks_count() -> int:
    return 40
