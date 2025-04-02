from src.f00_instrument.file import open_json, save_json, create_path
from src.f00_instrument.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd


def jmetrics_str() -> str:
    return "jmetrics"


def fund_take_str() -> str:
    return "fund_take"


def fund_give_str() -> str:
    return "fund_give"


def get_fund_metric_config_filename() -> str:
    return "fund_metric_config.json"


def config_file_path() -> str:
    src_dir = create_path(os_getcwd(), "src")
    config_file_dir = create_path(src_dir, "f05_fund_metric")
    return create_path(config_file_dir, get_fund_metric_config_filename())


def get_fund_metric_config_dict() -> dict[str, dict]:
    return open_json(config_file_path())


def get_all_fund_metric_args() -> dict[str, set[str]]:
    fund_metric_config_dict = get_fund_metric_config_dict()
    all_args = set()
    for fund_metric_dimen, dimen_dict in fund_metric_config_dict.items():
        for dimen_key, arg_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                all_args = all_args.union(set(arg_dict.keys()))
    return all_args
