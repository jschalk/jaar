from src.f00_instrument.file import create_path
from src.f03_chrono.chrono import (
    c400_number_str,
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
    jkeys_str,
    jvalues_str,
    atom_update,
    atom_insert,
    atom_delete,
    normal_specs_str,
    jaar_type_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f07_fiscal.fiscal_config import (
    config_file_dir,
    get_fiscal_config_file_name,
    get_fiscal_config_dict,
    get_fiscal_args_category_mapping,
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
    get_fiscal_categorys,
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
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f07_fiscal")


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
    assert len(fiscalunit_dict.get(jkeys_str())) == 0
    assert len(fiscal_purview_episode_dict.get(jkeys_str())) == 4
    assert len(fiscal_cashbook_dict.get(jkeys_str())) == 4
    assert len(fiscal_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(fiscal_timeline_month_dict.get(jkeys_str())) == 2
    assert len(fiscal_timeline_weekday_dict.get(jkeys_str())) == 2

    x_fiscalunit_jvalues = {
        c400_number_str(),
        current_time_str(),
        fiscal_id_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        "wall",
        timeline_label_str(),
        yr1_jan1_offset_str(),
    }
    print(f"{fiscalunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(fiscalunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_fiscalunit_jvalues
    assert len(fiscalunit_dict.get(jvalues_str())) == 10
    assert len(fiscal_purview_episode_dict.get(jvalues_str())) == 1
    assert len(fiscal_cashbook_dict.get(jvalues_str())) == 1
    assert len(fiscal_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(fiscal_timeline_month_dict.get(jvalues_str())) == 1
    assert len(fiscal_timeline_weekday_dict.get(jvalues_str())) == 1


def _validate_fiscal_config(fiscal_config: dict):
    accepted_jaar_typees = {
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
    for fiscal_categorys, cat_dict in fiscal_config.items():
        print(f"_validate_fiscal_config {fiscal_categorys=}")
        assert cat_dict.get(jkeys_str()) is not None
        assert cat_dict.get(jvalues_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        fiscal_jkeys_keys = set(cat_dict.get(jkeys_str()).keys())
        for jkey_key in fiscal_jkeys_keys:
            jkey_dict = cat_dict.get(jkeys_str())
            print(f"_validate_fiscal_config {fiscal_categorys=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees
        fiscal_jvalues_keys = set(cat_dict.get(jvalues_str()).keys())
        for jvalue_key in fiscal_jvalues_keys:
            jvalue_dict = cat_dict.get(jvalues_str())
            print(f"_validate_fiscal_config {fiscal_categorys=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees


def test_get_fiscal_categorys_ReturnsObj():
    # ESTABLISH / WHEN
    fiscal_config_categorys = get_fiscal_categorys()

    # THEN
    assert fiscalunit_str() in fiscal_config_categorys
    assert fiscal_purviewlog_str() not in fiscal_config_categorys
    assert fiscal_purview_episode_str() in fiscal_config_categorys
    assert fiscal_cashbook_str() in fiscal_config_categorys
    assert fiscal_timeline_hour_str() in fiscal_config_categorys
    assert fiscal_timeline_month_str() in fiscal_config_categorys
    assert fiscal_timeline_weekday_str() in fiscal_config_categorys


def test_get_fiscal_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_fiscal_args_category_mapping = get_fiscal_args_category_mapping()

    # THEN
    assert x_fiscal_args_category_mapping
    assert x_fiscal_args_category_mapping.get(current_time_str())
    x_hour = {fiscal_timeline_hour_str()}
    assert x_fiscal_args_category_mapping.get(cumlative_minute_str()) == x_hour
    assert x_fiscal_args_category_mapping.get(fund_coin_str())
    fiscal_id_categorys = x_fiscal_args_category_mapping.get(fiscal_id_str())
    assert fiscal_timeline_hour_str() in fiscal_id_categorys
    assert fiscalunit_str() in fiscal_id_categorys
    assert len(fiscal_id_categorys) == 6
    assert len(x_fiscal_args_category_mapping) == 21
