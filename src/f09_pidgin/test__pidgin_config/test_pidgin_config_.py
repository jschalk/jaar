from src.f00_instrument.file import create_path
from src.f04_vow.atom_config import (
    jkeys_str,
    jvalues_str,
    atom_update,
    atom_insert,
    atom_delete,
    normal_specs_str,
    class_type_str,
    event_int_str,
)
from src.f09_pidgin.pidgin_config import (
    config_file_dir,
    get_pidgin_dimens,
    get_pidgin_config_filename,
    get_pidgin_config_dict,
    get_pidgin_args_dimen_mapping,
    get_quick_pidgens_column_ref,
    pidginunit_str,
    pidgin_filename,
    otx_bridge_str,
    inx_bridge_str,
    inx_label_str,
    otx_label_str,
    inx_name_str,
    otx_name_str,
    inx_title_str,
    otx_title_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
    otx2inx_str,
    map_otx2inx_str,
    map_name_str,
    map_label_str,
    map_title_str,
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
    assert inx_title_str() == "inx_title"
    assert otx_title_str() == "otx_title"
    assert inx_road_str() == "inx_road"
    assert otx_road_str() == "otx_road"
    assert unknown_word_str() == "unknown_word"
    assert otx2inx_str() == "otx2inx"
    assert map_name_str() == "map_name"
    assert map_label_str() == "map_label"
    assert map_title_str() == "map_title"
    assert map_road_str() == "map_road"
    assert map_otx2inx_str() == "map_otx2inx"


def test_get_pidgin_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_pidgin_config_filename() == "pidgin_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f09_pidgin")


def test_get_pidgin_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_config = get_pidgin_config_dict()

    # THEN
    assert pidgin_config
    pidgin_config_dimens = set(pidgin_config.keys())
    assert map_name_str() in pidgin_config_dimens
    assert map_label_str() in pidgin_config_dimens
    assert map_title_str() in pidgin_config_dimens
    assert map_road_str() in pidgin_config_dimens
    assert len(pidgin_config) == 4

    _validate_pidgin_config(pidgin_config)
    map_road_dict = pidgin_config.get(map_road_str())
    map_title_dict = pidgin_config.get(map_title_str())
    assert len(map_road_dict.get(jkeys_str())) == 1
    assert len(map_title_dict.get(jkeys_str())) == 1
    assert len(map_road_dict.get(jvalues_str())) == 4
    assert len(map_title_dict.get(jvalues_str())) == 4

    # assert gen_jvalues == x_pidginunit_jvalues
    # assert len(pidginunit_dict.get(jvalues_str())) == 9
    # assert len(pidgin_dealunit_dict.get(jvalues_str())) == 1
    # assert len(pidgin_cashbook_dict.get(jvalues_str())) == 1
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
        inx_title_str(),
        otx_title_str(),
        inx_road_str(),
        otx_road_str(),
        unknown_word_str(),
    }

    # for every pidgin_format file there exists a unique pidgin_number always with leading zeros to make 5 digits
    for pidgin_dimens, dimen_dict in pidgin_config.items():
        print(f"_validate_pidgin_config {pidgin_dimens=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        assert dimen_dict.get(atom_update()) is None
        assert dimen_dict.get(atom_insert()) is None
        assert dimen_dict.get(atom_delete()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        pidgin_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in pidgin_jkeys_keys:
            print(f"_validate_pidgin_config {pidgin_dimens=} {jkey_key=} ")
            assert jkey_key in x_possible_args
        pidgin_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in pidgin_jvalues_keys:
            print(f"_validate_pidgin_config {pidgin_dimens=} {jvalue_key=} ")
            assert jvalue_key in x_possible_args


def test_get_pidgin_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_config_dimens = get_pidgin_dimens()

    # THEN
    assert map_name_str() in pidgin_config_dimens
    assert map_label_str() in pidgin_config_dimens
    assert map_title_str() in pidgin_config_dimens
    assert map_road_str() in pidgin_config_dimens
    assert len(pidgin_config_dimens) == 4


def test_get_pidgin_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidgin_args_dimen_mapping = get_pidgin_args_dimen_mapping()
    print(f"{x_pidgin_args_dimen_mapping=}")

    # THEN
    assert x_pidgin_args_dimen_mapping
    assert x_pidgin_args_dimen_mapping.get(otx_road_str())
    x_dimens = {map_road_str()}
    assert x_pidgin_args_dimen_mapping.get(otx_road_str()) == x_dimens
    assert x_pidgin_args_dimen_mapping.get(inx_bridge_str())
    pidgin_id_dimens = x_pidgin_args_dimen_mapping.get(inx_bridge_str())
    assert len(pidgin_id_dimens) == 4
    assert len(x_pidgin_args_dimen_mapping) == 11


def _get_all_pidgen_config_attrs() -> dict[str, set[str]]:
    pidgin_config = get_pidgin_config_dict()
    print(f"{pidgin_config=}")
    x_pidgen_attrs = {}
    for pidgin_dimen, jkeys_jvalues_dict in pidgin_config.items():
        attrs_set = set(jkeys_jvalues_dict.get("jkeys").keys())
        attrs_set.update(set(jkeys_jvalues_dict.get("jvalues").keys()))
        x_pidgen_attrs[pidgin_dimen] = attrs_set
    return x_pidgen_attrs


def test_get_quick_pidgens_column_ref_ReturnsObj():
    # ESTABLISH
    all_pidgen_config_attrs = _get_all_pidgen_config_attrs()
    # print(f"{all_pidgen_config_attrs=}")

    # WHEN / THEN
    assert map_road_str() in set(get_quick_pidgens_column_ref().keys())
    assert len(get_quick_pidgens_column_ref().keys()) == 4
    assert get_quick_pidgens_column_ref() == all_pidgen_config_attrs
