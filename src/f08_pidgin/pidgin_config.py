from src.f00_instrument.file import open_file
from src.f00_instrument.dict_toolbox import get_dict_from_json, get_from_nested_dict
from src.f04_gift.atom_config import jkeys_str, jvalues_str
from os import getcwd as os_getcwd


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/f08_pidgin"


def get_pidgin_config_file_name() -> str:
    return "pidgin_config.json"


def get_pidgin_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_pidgin_config_file_name())
    )


def get_pidgin_categorys() -> set[str]:
    return set(get_pidgin_config_dict().keys())


def pidginunit_str() -> str:
    return "pidginunit"


def event_id_str() -> str:
    return "event_id"


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


def nub_label_str() -> str:
    return "nub_label"


def otx2inx_str() -> str:
    return "otx2inx"


def bridge_otx2inx_str() -> str:
    return "bridge_otx2inx"


def bridge_nub_label_str() -> str:
    return "bridge_nub_label"


def get_pidgin_config_jkeys(x_cat: str) -> dict:
    jkeys_key_list = [x_cat, jkeys_str()]
    return get_from_nested_dict(get_pidgin_config_dict(), jkeys_key_list)


def get_pidgin_config_jvalues(x_cat: str) -> dict:
    jvalues_key_list = [x_cat, jvalues_str()]
    return get_from_nested_dict(get_pidgin_config_dict(), jvalues_key_list)


def get_pidgin_config_args(x_category: str) -> dict[str, dict]:
    args_dict = get_pidgin_config_jkeys(x_category)
    args_dict.update(get_pidgin_config_jvalues(x_category))
    return args_dict


def get_pidgin_args_category_mapping() -> dict[str, str]:
    x_dict = {}
    for pidgin_category in get_pidgin_config_dict().keys():
        args_set = set(get_pidgin_config_args(pidgin_category))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {pidgin_category}
            else:
                x_category_set = x_dict.get(x_arg)
                x_category_set.add(pidgin_category)
                x_dict[x_arg] = x_category_set
    return x_dict


def get_quick_pidgens_column_ref() -> dict[str, set[str]]:
    """for each pidgin_config category contains the associated columns"""
    return {
        "bridge_nub_label": {
            "jaar_type",
            "unknown_word",
            "inx_road_delimiter",
            "inx_label",
            "otx_road_delimiter",
            "otx_label",
        },
        "bridge_otx2inx": {
            "inx_word",
            "jaar_type",
            "unknown_word",
            "inx_road_delimiter",
            "otx_road_delimiter",
            "otx_word",
        },
    }
