from src.f00_instrument.file import open_file
from src.f00_instrument.dict_tool import get_dict_from_json
from os import getcwd as os_getcwd


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/f08__filter"


def get_filter_config_file_name() -> str:
    return "filter_config.json"


def get_filter_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_filter_config_file_name())
    )


def get_filter_categorys() -> set[str]:
    return get_filter_config_dict().keys()


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
