from src.f00_instrument.file import open_file
from src.f00_instrument.dict_tool import get_dict_from_json
from src.f01_road.jaar_config import get_json_filename, get_test_fiscals_dir
from src.f07_fiscal.examples.fiscal_env import env_dir_setup_cleanup
from os import getcwd as os_getcwd


def current_time_str() -> str:
    return "current_time"


def monthday_distortion_str() -> str:
    return "monthday_distortion"


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


def get_fiscal_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_fiscal_config_file_name())
    )
