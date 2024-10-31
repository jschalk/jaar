from src.f00_instrument.file import open_file
from src.f00_instrument.dict_tool import get_dict_from_json, get_from_nested_dict
from src.f04_gift.atom_config import required_args_str, optional_args_str
from os import getcwd as os_getcwd


def current_time_str() -> str:
    return "current_time"


def amount_str() -> str:
    return "amount"


def month_label_str() -> str:
    return "month_label"


def hour_label_str() -> str:
    return "hour_label"


def cumlative_minute_str() -> str:
    return "cumlative_minute"


def cumlative_day_str() -> str:
    return "cumlative_day"


def weekday_label_str() -> str:
    return "weekday_label"


def weekday_order_str() -> str:
    return "weekday_order"


def get_fiscal_config_file_name() -> str:
    return "fiscal_config.json"


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/f07_fiscal"


# def fiscalunit_str()-> str: return "fiscalunit"
# def fiscal_purviewlog_str()-> str: return "fiscal_purviewlog"
# def fiscal_purview_episode_str()-> str: return "fiscal_purview_episode"
# def fiscal_cashbook_str()-> str: return "fiscal_cashbook"
# def fiscal_timeline_hour_str()-> str: return "fiscal_timeline_hour"
# def fiscal_timeline_month_str()-> str: return "fiscal_timeline_month"
# def fiscal_timeline_weekday_str()-> str: return "fiscal_timeline_weekday"
def fiscalunit_str() -> str:
    return "fiscalunit"


def fiscal_purviewlog_str() -> str:
    return "fiscal_purviewlog"


def fiscal_purview_episode_str() -> str:
    return "fiscal_purview_episode"


def fiscal_cashbook_str() -> str:
    return "fiscal_cashbook"


def fiscal_timeline_hour_str() -> str:
    return "fiscal_timeline_hour"


def fiscal_timeline_month_str() -> str:
    return "fiscal_timeline_month"


def fiscal_timeline_weekday_str() -> str:
    return "fiscal_timeline_weekday"


def get_fiscal_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_fiscal_config_file_name())
    )


def get_fiscal_categorys() -> set[str]:
    return set(get_fiscal_config_dict().keys())


def get_fiscal_config_required_args(x_cat: str) -> dict:
    required_args_key_list = [x_cat, required_args_str()]
    return get_from_nested_dict(get_fiscal_config_dict(), required_args_key_list)


def get_fiscal_config_optional_args(x_cat: str) -> dict:
    optional_args_key_list = [x_cat, optional_args_str()]
    return get_from_nested_dict(get_fiscal_config_dict(), optional_args_key_list)


def get_fiscal_config_args(x_category: str) -> dict[str, dict]:
    args_dict = get_fiscal_config_required_args(x_category)
    args_dict.update(get_fiscal_config_optional_args(x_category))
    return args_dict


def get_fiscal_args_category_mapping() -> dict[str, str]:
    x_dict = {}
    for fiscal_category in get_fiscal_config_dict().keys():
        args_set = set(get_fiscal_config_args(fiscal_category))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {fiscal_category}
            else:
                x_category_set = x_dict.get(x_arg)
                x_category_set.add(fiscal_category)
                x_dict[x_arg] = x_category_set
    return x_dict
