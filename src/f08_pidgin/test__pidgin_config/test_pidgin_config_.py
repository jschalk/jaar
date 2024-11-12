from src.f04_gift.atom_config import (
    required_args_str,
    optional_args_str,
    atom_update,
    atom_insert,
    atom_delete,
    normal_specs_str,
    obj_class_str,
)
from src.f08_pidgin.pidgin_config import (
    config_file_dir,
    get_pidgin_categorys,
    get_pidgin_config_file_name,
    get_pidgin_config_dict,
    get_pidgin_args_category_mapping,
    pidginunit_str,
    eon_id_str,
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
    assert pidginunit_str() == "pidginunit"
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
    assert eon_id_str() == "eon_id"


def test_get_pidgin_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_pidgin_config_file_name() == "pidgin_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    assert config_file_dir() == f"{os_getcwd()}/src/f08_pidgin"


def test_get_pidgin_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_config = get_pidgin_config_dict()

    # THEN
    assert pidgin_config
    pidgin_config_categorys = set(pidgin_config.keys())
    assert bridge_otx_to_inx_str() in pidgin_config_categorys
    assert bridge_explicit_label_str() in pidgin_config_categorys
    assert len(pidgin_config) == 2

    _validate_pidgin_config(pidgin_config)
    bridge_otx_to_inx_dict = pidgin_config.get(bridge_otx_to_inx_str())
    bridge_explicit_label_dict = pidgin_config.get(bridge_explicit_label_str())
    assert len(bridge_otx_to_inx_dict.get(required_args_str())) == 2
    assert len(bridge_explicit_label_dict.get(required_args_str())) == 1
    assert len(bridge_otx_to_inx_dict.get(optional_args_str())) == 4
    assert len(bridge_explicit_label_dict.get(optional_args_str())) == 4

    # assert gen_optional_args == x_pidginunit_optional_args
    # assert len(pidginunit_dict.get(optional_args_str())) == 9
    # assert len(pidgin_purview_episode_dict.get(optional_args_str())) == 1
    # assert len(pidgin_cashbook_dict.get(optional_args_str())) == 1
    # assert len(pidgin_timeline_hour_dict.get(optional_args_str())) == 0
    # assert len(pidgin_timeline_month_dict.get(optional_args_str())) == 0
    # assert len(pidgin_timeline_weekday_dict.get(optional_args_str())) == 0


def _validate_pidgin_config(pidgin_config: dict):
    x_possible_args = {
        inx_road_delimiter_str(),
        otx_road_delimiter_str(),
        obj_class_str(),
        inx_word_str(),
        otx_word_str(),
        inx_label_str(),
        otx_label_str(),
        unknown_word_str(),
    }

    # for every pidgin_format file there exists a unique pidgin_number always with leading zeros to make 5 digits
    for pidgin_categorys, cat_dict in pidgin_config.items():
        print(f"_validate_pidgin_config {pidgin_categorys=}")
        assert cat_dict.get(required_args_str()) is not None
        assert cat_dict.get(optional_args_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        pidgin_required_args_keys = set(cat_dict.get(required_args_str()).keys())
        for required_arg_key in pidgin_required_args_keys:
            print(f"_validate_pidgin_config {pidgin_categorys=} {required_arg_key=} ")
            assert required_arg_key in x_possible_args
        pidgin_optional_args_keys = set(cat_dict.get(optional_args_str()).keys())
        for optional_arg_key in pidgin_optional_args_keys:
            print(f"_validate_pidgin_config {pidgin_categorys=} {optional_arg_key=} ")
            assert optional_arg_key in x_possible_args


def test_get_pidgin_categorys_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_config_categorys = get_pidgin_categorys()

    # THEN
    assert bridge_otx_to_inx_str() in pidgin_config_categorys
    assert bridge_explicit_label_str() in pidgin_config_categorys


def test_get_pidgin_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidgin_args_category_mapping = get_pidgin_args_category_mapping()
    print(f"{x_pidgin_args_category_mapping=}")

    # THEN
    assert x_pidgin_args_category_mapping
    assert x_pidgin_args_category_mapping.get(otx_word_str())
    x_categorys = {bridge_otx_to_inx_str()}
    assert x_pidgin_args_category_mapping.get(otx_word_str()) == x_categorys
    assert x_pidgin_args_category_mapping.get(inx_road_delimiter_str())
    pidgin_id_categorys = x_pidgin_args_category_mapping.get(inx_road_delimiter_str())
    assert bridge_otx_to_inx_str() in pidgin_id_categorys
    assert bridge_explicit_label_str() in pidgin_id_categorys
    assert len(pidgin_id_categorys) == 2
    assert len(x_pidgin_args_category_mapping) == 8
