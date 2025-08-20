from os import getcwd as os_getcwd
from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a00_data_toolbox.file_toolbox import create_path, open_json


def coin_config_path() -> str:
    "Returns Path: a15_coin_logic/coin_config.json"
    src_dir = create_path(os_getcwd(), "src")
    module_dir = create_path(src_dir, "a15_coin_logic")
    return create_path(module_dir, "coin_config.json")


def get_coin_config_dict() -> dict:
    return open_json(coin_config_path())


def get_coin_dimens() -> set[str]:
    return {
        "coinunit",
        "coin_budunit",
        "coin_paybook",
        "coin_timeline_hour",
        "coin_timeline_month",
        "coin_timeline_weekday",
        "coin_timeoffi",
    }


def get_coin_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_coin_config_dict(), jkeys_key_list)


def get_coin_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_coin_config_dict(), jvalues_key_list)


def get_coin_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_coin_config_jkeys(x_dimen)
    args_dict.update(get_coin_config_jvalues(x_dimen))
    return args_dict


def get_coin_args_dimen_mapping() -> dict[str, str]:
    x_dict = {}
    for coin_dimen in get_coin_config_dict().keys():
        args_set = set(get_coin_config_args(coin_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = set()
            x_dimen_set = x_dict.get(x_arg)
            x_dimen_set.add(coin_dimen)
            x_dict[x_arg] = x_dimen_set
    return x_dict


def get_coin_args_class_types() -> dict[str, str]:
    return {
        "partner_name": "NameTerm",
        "amount": "float",
        "knot": "str",
        "celldepth": "int",
        "c400_number": "int",
        "cumulative_day": "int",
        "cumulative_minute": "int",
        "bud_time": "TimeLinePoint",
        "hour_label": "LabelTerm",
        "coin_label": "LabelTerm",
        "fund_iota": "float",
        "month_label": "LabelTerm",
        "monthday_distortion": "int",
        "penny": "float",
        "offi_time": "TimeLinePoint",
        "belief_name": "NameTerm",
        "quota": "int",
        "job_listen_rotations": "int",
        "respect_bit": "float",
        "tran_time": "TimeLinePoint",
        "timeline_label": "LabelTerm",
        "weekday_label": "LabelTerm",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def get_coin_args_set() -> set[str]:
    return {
        "partner_name",
        "amount",
        "knot",
        "c400_number",
        "celldepth",
        "cumulative_day",
        "cumulative_minute",
        "bud_time",
        "hour_label",
        "coin_label",
        "fund_iota",
        "month_label",
        "monthday_distortion",
        "job_listen_rotations",
        "penny",
        "offi_time",
        "belief_name",
        "quota",
        "respect_bit",
        "tran_time",
        "timeline_label",
        "weekday_label",
        "weekday_order",
        "yr1_jan1_offset",
    }
