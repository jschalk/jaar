from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    jkeys_str,
    jvalues_str,
    atom_update,
    atom_insert,
    atom_delete,
    normal_specs_str,
    jaar_type_str,
)
from src.f08_pidgin.pidgin_config import (
    config_file_dir,
    get_pidgin_categorys,
    get_pidgin_config_file_name,
    get_pidgin_config_dict,
    get_pidgin_args_category_mapping,
    get_quick_pidgens_column_ref,
    pidginunit_str,
    pidgin_filename,
    event_int_str,
    otx_bridge_str,
    inx_bridge_str,
    inx_label_str,
    otx_label_str,
    inx_name_str,
    otx_name_str,
    inx_idea_str,
    otx_idea_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
    otx2inx_str,
    map_otx2inx_str,
    map_name_str,
    map_label_str,
    map_idea_str,
    map_road_str,
)
from os import getcwd as os_getcwd


def test_str_functions_ReturnsObj():
    assert pidginunit_str() == "pidginunit"
    assert pidgin_filename() == "pidgin.json"
    assert otx_bridge_str() == "otx_bridge"
    assert inx_bridge_str() == "inx_bridge"
    assert inx_label_str() == "inx_label"
    assert otx_label_str() == "otx_label"
    assert inx_name_str() == "inx_name"
    assert otx_name_str() == "otx_name"
    assert inx_idea_str() == "inx_idea"
    assert otx_idea_str() == "otx_idea"
    assert inx_road_str() == "inx_road"
    assert otx_road_str() == "otx_road"
    assert unknown_word_str() == "unknown_word"
    assert otx2inx_str() == "otx2inx"
    assert map_name_str() == "map_name"
    assert map_label_str() == "map_label"
    assert map_idea_str() == "map_idea"
    assert map_road_str() == "map_road"
    assert map_otx2inx_str() == "map_otx2inx"
    assert event_int_str() == "event_int"


def test_get_pidgin_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_pidgin_config_file_name() == "pidgin_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f08_pidgin")


def test_get_pidgin_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_config = get_pidgin_config_dict()

    # THEN
    assert pidgin_config
    pidgin_config_categorys = set(pidgin_config.keys())
    assert map_name_str() in pidgin_config_categorys
    assert map_label_str() in pidgin_config_categorys
    assert map_idea_str() in pidgin_config_categorys
    assert map_road_str() in pidgin_config_categorys
    assert len(pidgin_config) == 4

    _validate_pidgin_config(pidgin_config)
    map_road_dict = pidgin_config.get(map_road_str())
    map_idea_dict = pidgin_config.get(map_idea_str())
    assert len(map_road_dict.get(jkeys_str())) == 1
    assert len(map_idea_dict.get(jkeys_str())) == 1
    assert len(map_road_dict.get(jvalues_str())) == 4
    assert len(map_idea_dict.get(jvalues_str())) == 4

    # assert gen_jvalues == x_pidginunit_jvalues
    # assert len(pidginunit_dict.get(jvalues_str())) == 9
    # assert len(pidgin_turn_episode_dict.get(jvalues_str())) == 1
    # assert len(pidgin_bankbook_dict.get(jvalues_str())) == 1
    # assert len(pidgin_timeline_hour_dict.get(jvalues_str())) == 0
    # assert len(pidgin_timeline_month_dict.get(jvalues_str())) == 0
    # assert len(pidgin_timeline_weekday_dict.get(jvalues_str())) == 0


def _validate_pidgin_config(pidgin_config: dict):
    x_possible_args = {
        inx_bridge_str(),
        otx_bridge_str(),
        inx_label_str(),
        otx_label_str(),
        inx_name_str(),
        otx_name_str(),
        inx_idea_str(),
        otx_idea_str(),
        inx_road_str(),
        otx_road_str(),
        unknown_word_str(),
    }

    # for every pidgin_format file there exists a unique pidgin_number always with leading zeros to make 5 digits
    for pidgin_categorys, cat_dict in pidgin_config.items():
        print(f"_validate_pidgin_config {pidgin_categorys=}")
        assert cat_dict.get(jkeys_str()) is not None
        assert cat_dict.get(jvalues_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        pidgin_jkeys_keys = set(cat_dict.get(jkeys_str()).keys())
        for jkey_key in pidgin_jkeys_keys:
            print(f"_validate_pidgin_config {pidgin_categorys=} {jkey_key=} ")
            assert jkey_key in x_possible_args
        pidgin_jvalues_keys = set(cat_dict.get(jvalues_str()).keys())
        for jvalue_key in pidgin_jvalues_keys:
            print(f"_validate_pidgin_config {pidgin_categorys=} {jvalue_key=} ")
            assert jvalue_key in x_possible_args


def test_get_pidgin_categorys_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_config_categorys = get_pidgin_categorys()

    # THEN
    assert map_name_str() in pidgin_config_categorys
    assert map_label_str() in pidgin_config_categorys
    assert map_idea_str() in pidgin_config_categorys
    assert map_road_str() in pidgin_config_categorys
    assert len(pidgin_config_categorys) == 4


def test_get_pidgin_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidgin_args_category_mapping = get_pidgin_args_category_mapping()
    print(f"{x_pidgin_args_category_mapping=}")

    # THEN
    assert x_pidgin_args_category_mapping
    assert x_pidgin_args_category_mapping.get(otx_road_str())
    x_categorys = {map_road_str()}
    assert x_pidgin_args_category_mapping.get(otx_road_str()) == x_categorys
    assert x_pidgin_args_category_mapping.get(inx_bridge_str())
    pidgin_id_categorys = x_pidgin_args_category_mapping.get(inx_bridge_str())
    assert len(pidgin_id_categorys) == 4
    assert len(x_pidgin_args_category_mapping) == 11


def _get_all_pidgen_config_attrs() -> dict[str, set[str]]:
    pidgin_config = get_pidgin_config_dict()
    print(f"{pidgin_config=}")
    x_pidgen_attrs = {}
    for pidgin_category, jkeys_jvalues_dict in pidgin_config.items():
        attrs_set = set(jkeys_jvalues_dict.get("jkeys").keys())
        attrs_set.update(set(jkeys_jvalues_dict.get("jvalues").keys()))
        x_pidgen_attrs[pidgin_category] = attrs_set
    return x_pidgen_attrs


def test_get_quick_pidgens_column_ref_ReturnsObj():
    # ESTABLISH
    all_pidgen_config_attrs = _get_all_pidgen_config_attrs()
    # print(f"{all_pidgen_config_attrs=}")

    # WHEN / THEN
    assert map_road_str() in set(get_quick_pidgens_column_ref().keys())
    assert len(get_quick_pidgens_column_ref().keys()) == 4
    assert get_quick_pidgens_column_ref() == all_pidgen_config_attrs
