from src.f03_chrono.chrono import (
    c400_config_str,
    timeline_label_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import fiscal_id_str, penny_str
from src.f07_fiscal.fiscal_config import (
    config_file_dir,
    get_fiscal_config_file_name,
    get_fiscal_config_dict,
    current_time_str,
    amount_str,
    month_label_str,
    hour_label_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_label_str,
    weekday_order_str,
)
from os import getcwd as os_getcwd


def test_str_functions_ReturnsObj():
    assert current_time_str() == "current_time"
    assert amount_str() == "amount"
    assert month_label_str() == "month_label"
    assert hour_label_str() == "hour_label"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"


def test_get_fiscal_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_fiscal_config_file_name() == "fiscal_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    assert config_file_dir() == f"{os_getcwd()}/src/f07_fiscal"


def test_get_fiscal_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_fiscal_config = get_fiscal_config_dict()

    # THEN
    assert x_fiscal_config
    fiscal_config_categorys = set(x_fiscal_config.keys())
    assert "fiscalunit" in fiscal_config_categorys
    assert "fiscal_purviewlog" in fiscal_config_categorys
    assert "fiscal_purview_episode" in fiscal_config_categorys
    assert "fiscal_cashbook" in fiscal_config_categorys
    assert "fiscal_timeline_hour" in fiscal_config_categorys
    assert "fiscal_timeline_month" in fiscal_config_categorys
    assert "fiscal_timeline_weekday" in fiscal_config_categorys
    assert len(x_fiscal_config) == 7
