from src.f00_instrument.file import open_file
from src.f00_instrument.dict_toolbox import get_dict_from_json, get_from_nested_dict
from src.f04_gift.atom_config import required_args_str, optional_args_str
from os import getcwd as os_getcwd


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/f08_filter"


def get_filter_config_file_name() -> str:
    return "filter_config.json"


def get_filter_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_filter_config_file_name())
    )


def get_filter_categorys() -> set[str]:
    return set(get_filter_config_dict().keys())


def filterunit_str() -> str:
    return "filterunit"


def eon_id_str() -> str:
    return "eon_id"


def otx_road_delimiter_str() -> str:
    return "otx_road_delimiter"


def inx_road_delimiter_str() -> str:
    return "inx_road_delimiter"


def inx_word_str() -> str:
    return "inx_word"


def otx_word_str() -> str:
    return "otx_word"


def inx_label_str() -> str:
    return "inx_label"


def otx_label_str() -> str:
    return "otx_label"


def unknown_word_str() -> str:
    return "unknown_word"


def explicit_label_str() -> str:
    return "explicit_label"


def otx_to_inx_str() -> str:
    return "otx_to_inx"


def bridge_otx_to_inx_str() -> str:
    return "bridge_otx_to_inx"


def bridge_explicit_label_str() -> str:
    return "bridge_explicit_label"


def get_filter_config_required_args(x_cat: str) -> dict:
    required_args_key_list = [x_cat, required_args_str()]
    return get_from_nested_dict(get_filter_config_dict(), required_args_key_list)


def get_filter_config_optional_args(x_cat: str) -> dict:
    optional_args_key_list = [x_cat, optional_args_str()]
    return get_from_nested_dict(get_filter_config_dict(), optional_args_key_list)


def get_filter_config_args(x_category: str) -> dict[str, dict]:
    args_dict = get_filter_config_required_args(x_category)
    args_dict.update(get_filter_config_optional_args(x_category))
    return args_dict


def get_filter_args_category_mapping() -> dict[str, str]:
    x_dict = {}
    for filter_category in get_filter_config_dict().keys():
        args_set = set(get_filter_config_args(filter_category))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {filter_category}
            else:
                x_category_set = x_dict.get(x_arg)
                x_category_set.add(filter_category)
                x_dict[x_arg] = x_category_set
    return x_dict
