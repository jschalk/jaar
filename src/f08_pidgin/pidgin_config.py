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


def otx_wall_str() -> str:
    return "otx_wall"


def inx_wall_str() -> str:
    return "inx_wall"


def inx_group_id_str() -> str:
    return "inx_group_id"


def otx_group_id_str() -> str:
    return "otx_group_id"


def inx_acct_id_str() -> str:
    return "inx_acct_id"


def otx_acct_id_str() -> str:
    return "otx_acct_id"


def inx_node_str() -> str:
    return "inx_node"


def otx_node_str() -> str:
    return "otx_node"


def inx_road_str() -> str:
    return "inx_road"


def otx_road_str() -> str:
    return "otx_road"


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


def bridge_acct_id_str() -> str:
    return "bridge_acct_id"


def bridge_group_id_str() -> str:
    return "bridge_group_id"


def bridge_node_str() -> str:
    return "bridge_node"


def bridge_road_str() -> str:
    return "bridge_road"


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
            "unknown_word",
            "inx_wall",
            "inx_label",
            "otx_wall",
            "otx_label",
        },
        "bridge_group_id": {
            "inx_group_id",
            "unknown_word",
            "inx_wall",
            "otx_wall",
            "otx_group_id",
        },
        "bridge_acct_id": {
            "inx_acct_id",
            "unknown_word",
            "inx_wall",
            "otx_wall",
            "otx_acct_id",
        },
        "bridge_node": {
            "inx_node",
            "unknown_word",
            "inx_wall",
            "otx_wall",
            "otx_node",
        },
        "bridge_road": {
            "inx_road",
            "unknown_word",
            "inx_wall",
            "otx_wall",
            "otx_road",
        },
    }
