from os import getcwd as os_getcwd
from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a00_data_toolbox.file_toolbox import create_path, open_json


def get_vow_config_filename() -> str:
    return "vow_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "a15_vow_logic")


def get_vow_config_dict() -> dict:
    return open_json(config_file_dir(), get_vow_config_filename())


def get_vow_dimens() -> set[str]:
    return {
        "vowunit",
        "vow_budunit",
        "vow_paybook",
        "vow_timeline_hour",
        "vow_timeline_month",
        "vow_timeline_weekday",
        "vow_timeoffi",
    }


def get_vow_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_vow_config_dict(), jkeys_key_list)


def get_vow_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_vow_config_dict(), jvalues_key_list)


def get_vow_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_vow_config_jkeys(x_dimen)
    args_dict.update(get_vow_config_jvalues(x_dimen))
    return args_dict


def get_vow_args_dimen_mapping() -> dict[str, str]:
    x_dict = {}
    for vow_dimen in get_vow_config_dict().keys():
        args_set = set(get_vow_config_args(vow_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = set()
            x_dimen_set = x_dict.get(x_arg)
            x_dimen_set.add(vow_dimen)
            x_dict[x_arg] = x_dimen_set
    return x_dict


def get_vow_args_class_types() -> dict[str, str]:
    return {
        "acct_name": "NameTerm",
        "amount": "float",
        "knot": "str",
        "celldepth": "int",
        "c400_number": "int",
        "cumulative_day": "int",
        "cumulative_minute": "int",
        "bud_time": "TimeLinePoint",
        "hour_label": "LabelTerm",
        "vow_label": "LabelTerm",
        "fund_iota": "float",
        "month_label": "LabelTerm",
        "monthday_distortion": "int",
        "penny": "float",
        "offi_time": "TimeLinePoint",
        "owner_name": "NameTerm",
        "quota": "int",
        "job_listen_rotations": "int",
        "respect_bit": "float",
        "tran_time": "TimeLinePoint",
        "timeline_label": "LabelTerm",
        "weekday_label": "LabelTerm",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def get_vow_args_set() -> set[str]:
    return {
        "acct_name",
        "amount",
        "knot",
        "c400_number",
        "celldepth",
        "cumulative_day",
        "cumulative_minute",
        "bud_time",
        "hour_label",
        "vow_label",
        "fund_iota",
        "month_label",
        "monthday_distortion",
        "job_listen_rotations",
        "penny",
        "offi_time",
        "owner_name",
        "quota",
        "respect_bit",
        "tran_time",
        "timeline_label",
        "weekday_label",
        "weekday_order",
        "yr1_jan1_offset",
    }
