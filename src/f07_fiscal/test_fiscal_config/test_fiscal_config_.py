from src.f03_chrono.chrono import (
    c400_config_str,
    timeline_label_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import (
    fiscal_id_str,
    penny_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    required_args_str,
    optional_args_str,
    atom_update,
    atom_insert,
    atom_delete,
    normal_specs_str,
    obj_class_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
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

    x_fiscalunit_optional_args = {
        current_time_str(),
        fiscal_id_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        "road_delimiter",
        timeline_label_str(),
        yr1_jan1_offset_str(),
    }
    print(f"{fiscalunit_dict.get(optional_args_str()).keys()=}")
    gen_optional_args = set(fiscalunit_dict.get(optional_args_str()).keys())
    assert gen_optional_args == x_fiscalunit_optional_args
    assert len(fiscalunit_dict.get(optional_args_str())) == 9
    assert len(fiscal_purview_episode_dict.get(optional_args_str())) == 1
    assert len(fiscal_cashbook_dict.get(optional_args_str())) == 1
    assert len(fiscal_timeline_hour_dict.get(optional_args_str())) == 0
    assert len(fiscal_timeline_month_dict.get(optional_args_str())) == 0
    assert len(fiscal_timeline_weekday_dict.get(optional_args_str())) == 0


def _validate_fiscal_config(fiscal_config: dict):
    accepted_obj_classes = {
        type_RoadUnit_str(),
        type_AcctID_str(),
        type_GroupID_str(),
        type_RoadNode_str(),
        "int",
        "TimeLinePoint",
        "FiscalID",
        "float",
        "str",
    }

    # for every fiscal_format file there exists a unique fiscal_number always with leading zeros to make 5 digits
    for fiscal_category, cat_dict in fiscal_config.items():
        print(f"_validate_fiscal_config {fiscal_category=}")
        assert cat_dict.get(required_args_str()) is not None
        assert cat_dict.get(optional_args_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        fiscal_required_args_keys = set(cat_dict.get(required_args_str()).keys())
        for required_arg_key in fiscal_required_args_keys:
            required_arg_dict = cat_dict.get(required_args_str())
            print(f"_validate_fiscal_config {fiscal_category=} {required_arg_key=} ")
            arg_dict = required_arg_dict.get(required_arg_key)
            assert arg_dict.get(obj_class_str()) in accepted_obj_classes
        fiscal_optional_args_keys = set(cat_dict.get(optional_args_str()).keys())
        for optional_arg_key in fiscal_optional_args_keys:
            optional_arg_dict = cat_dict.get(optional_args_str())
            print(f"_validate_fiscal_config {fiscal_category=} {optional_arg_key=} ")
            arg_dict = optional_arg_dict.get(optional_arg_key)
            assert arg_dict.get(obj_class_str()) in accepted_obj_classes
