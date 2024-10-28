from src.f03_chrono.chrono import (
    c400_config_str,
    timeline_label_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import (
    fiscal_id_str,
    penny_str,
    required_args_str,
    optional_args_str,
    atom_update,
    atom_insert,
    atom_delete,
    normal_specs_str,
)
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
    fiscalunit_str,
    fiscal_purviewlog_str,
    fiscal_purview_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
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
    assert fiscalunit_str() == "fiscalunit"
    assert fiscal_purviewlog_str() == "fiscal_purviewlog"
    assert fiscal_purview_episode_str() == "fiscal_purview_episode"
    assert fiscal_cashbook_str() == "fiscal_cashbook"
    assert fiscal_timeline_hour_str() == "fiscal_timeline_hour"
    assert fiscal_timeline_month_str() == "fiscal_timeline_month"
    assert fiscal_timeline_weekday_str() == "fiscal_timeline_weekday"


def test_get_fiscal_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_fiscal_config_file_name() == "fiscal_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    assert config_file_dir() == f"{os_getcwd()}/src/f07_fiscal"


def test_get_fiscal_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    fiscal_config = get_fiscal_config_dict()

    # THEN
    assert fiscal_config
    fiscal_config_categorys = set(fiscal_config.keys())
    assert fiscalunit_str() in fiscal_config_categorys
    assert fiscal_purviewlog_str() not in fiscal_config_categorys
    assert fiscal_purview_episode_str() in fiscal_config_categorys
    assert fiscal_cashbook_str() in fiscal_config_categorys
    assert fiscal_timeline_hour_str() in fiscal_config_categorys
    assert fiscal_timeline_month_str() in fiscal_config_categorys
    assert fiscal_timeline_weekday_str() in fiscal_config_categorys
    assert len(fiscal_config) == 6
    _validate_fiscal_config(fiscal_config)
    fiscalunit_dict = fiscal_config.get(fiscalunit_str())
    fiscal_purview_episode_dict = fiscal_config.get(fiscal_purview_episode_str())
    fiscal_cashbook_dict = fiscal_config.get(fiscal_cashbook_str())
    fiscal_timeline_hour_dict = fiscal_config.get(fiscal_timeline_hour_str())
    fiscal_timeline_month_dict = fiscal_config.get(fiscal_timeline_month_str())
    fiscal_timeline_weekday_dict = fiscal_config.get(fiscal_timeline_weekday_str())
    assert len(fiscalunit_dict.get(required_args_str())) == 0
    assert len(fiscal_purview_episode_dict.get(required_args_str())) == 4
    assert len(fiscal_cashbook_dict.get(required_args_str())) == 4
    assert len(fiscal_timeline_hour_dict.get(required_args_str())) == 3
    assert len(fiscal_timeline_month_dict.get(required_args_str())) == 3
    assert len(fiscal_timeline_weekday_dict.get(required_args_str())) == 3
    assert len(fiscalunit_dict.get(optional_args_str())) == 0
    assert len(fiscal_purview_episode_dict.get(optional_args_str())) == 1
    assert len(fiscal_cashbook_dict.get(optional_args_str())) == 1
    assert len(fiscal_timeline_hour_dict.get(optional_args_str())) == 0
    assert len(fiscal_timeline_month_dict.get(optional_args_str())) == 0
    assert len(fiscal_timeline_weekday_dict.get(optional_args_str())) == 0


# fiscalunit        "c400_config,current_time,fiscal_id,fund_coin,monthday_distortion,penny,respect_bit,road_delimiter,timeline_label,yr1_jan1_offset":
# fiscal_timeline_hour        "cumlative_minute,fiscal_id,hour_label"
# fiscal_timeline_month        "cumlative_day,fiscal_id,month_label"
# fiscal_timeline_weekday        "fiscal_id,weekday_label,weekday_order"


def _validate_fiscal_config(fiscal_config: dict):
    # for every fiscal_format file there exists a unique fiscal_number always with leading zeros to make 5 digits
    for fiscal_category, fiscal_dict in fiscal_config.items():
        print(f"_validate_fiscal_config {fiscal_category=}")
        assert fiscal_dict.get(required_args_str()) is not None
        assert fiscal_dict.get(optional_args_str()) is not None
        assert fiscal_dict.get(atom_update()) is None
        assert fiscal_dict.get(atom_insert()) is None
        assert fiscal_dict.get(atom_delete()) is None
        assert fiscal_dict.get(normal_specs_str()) is None

        fiscal_required_args_keys = set(fiscal_dict.get(required_args_str()).keys())
        # print(f"{atom_required_args_keys=}")
        # print(f"{fiscal_required_args_keys=}")
        fiscal_optional_args_keys = set(fiscal_dict.get(optional_args_str()).keys())
        # print(f" {atom_optional_args_keys=}")
        # print(f"{fiscal_optional_args_keys=}")
