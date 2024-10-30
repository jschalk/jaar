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
    get_fiscal_categorys,
)
from src.f08_brick.filter_config import (
    config_file_dir,
    get_filter_categorys,
    get_filter_config_file_name,
    get_filter_config_dict,
    otx_road_delimiter_str,
    inx_road_delimiter_str,
    inx_word_str,
    otx_word_str,
    inx_label_str,
    otx_label_str,
    unknown_word_str,
    explicit_label_str,
    otx_to_inx_str,
    bridge_otx_to_inx_str,
    bridge_explicit_label_str,
)
from os import getcwd as os_getcwd


def test_str_functions_ReturnsObj():
    assert otx_road_delimiter_str() == "otx_road_delimiter"
    assert inx_road_delimiter_str() == "inx_road_delimiter"
    assert inx_word_str() == "inx_word"
    assert otx_word_str() == "otx_word"
    assert inx_label_str() == "inx_label"
    assert otx_label_str() == "otx_label"
    assert unknown_word_str() == "unknown_word"
    assert explicit_label_str() == "explicit_label"
    assert otx_to_inx_str() == "otx_to_inx"
    assert bridge_otx_to_inx_str() == "bridge_otx_to_inx"
    assert bridge_explicit_label_str() == "bridge_explicit_label"


def test_get_filter_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_filter_config_file_name() == "filter_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    assert config_file_dir() == f"{os_getcwd()}/src/f08_brick"


def test_get_filter_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    filter_config = get_filter_config_dict()

    # THEN
    assert filter_config
    filter_config_categorys = set(filter_config.keys())
    assert bridge_otx_to_inx_str() in filter_config_categorys
    assert bridge_explicit_label_str() in filter_config_categorys
    assert len(filter_config) == 2

    _validate_filter_config(filter_config)
    bridge_otx_to_inx_dict = filter_config.get(bridge_otx_to_inx_str())
    bridge_explicit_label_dict = filter_config.get(bridge_explicit_label_str())
    assert len(bridge_otx_to_inx_dict.get(required_args_str())) == 5
    assert len(bridge_explicit_label_dict.get(required_args_str())) == 5
    assert len(bridge_otx_to_inx_dict.get(optional_args_str())) == 0
    assert len(bridge_explicit_label_dict.get(optional_args_str())) == 0

    # assert gen_optional_args == x_filterunit_optional_args
    # assert len(filterunit_dict.get(optional_args_str())) == 9
    # assert len(filter_purview_episode_dict.get(optional_args_str())) == 1
    # assert len(filter_cashbook_dict.get(optional_args_str())) == 1
    # assert len(filter_timeline_hour_dict.get(optional_args_str())) == 0
    # assert len(filter_timeline_month_dict.get(optional_args_str())) == 0
    # assert len(filter_timeline_weekday_dict.get(optional_args_str())) == 0


def _validate_filter_config(filter_config: dict):
    accepted_obj_classes = {"str"}
    x_possible_args = {
        inx_road_delimiter_str(),
        otx_road_delimiter_str(),
        inx_word_str(),
        otx_word_str(),
        inx_label_str(),
        otx_label_str(),
        unknown_word_str(),
    }

    # for every filter_format file there exists a unique filter_number always with leading zeros to make 5 digits
    for filter_categorys, cat_dict in filter_config.items():
        print(f"_validate_filter_config {filter_categorys=}")
        assert cat_dict.get(required_args_str()) is not None
        assert cat_dict.get(optional_args_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        filter_required_args_keys = set(cat_dict.get(required_args_str()).keys())
        for required_arg_key in filter_required_args_keys:
            required_arg_dict = cat_dict.get(required_args_str())
            print(f"_validate_filter_config {filter_categorys=} {required_arg_key=} ")
            arg_dict = required_arg_dict.get(required_arg_key)
            assert arg_dict.get(obj_class_str()) in accepted_obj_classes
            assert required_arg_key in x_possible_args
        filter_optional_args_keys = set(cat_dict.get(optional_args_str()).keys())
        for optional_arg_key in filter_optional_args_keys:
            optional_arg_dict = cat_dict.get(optional_args_str())
            print(f"_validate_filter_config {filter_categorys=} {optional_arg_key=} ")
            arg_dict = optional_arg_dict.get(optional_arg_key)
            assert arg_dict.get(obj_class_str()) in accepted_obj_classes
            assert optional_arg_key in x_possible_args


def test_get_filter_categorys_ReturnsObj():
    # ESTABLISH / WHEN
    filter_config_categorys = get_filter_categorys()

    # THEN
    assert bridge_otx_to_inx_str() in filter_config_categorys
    assert bridge_explicit_label_str() in filter_config_categorys
