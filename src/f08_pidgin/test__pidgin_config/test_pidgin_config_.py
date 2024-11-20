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
    event_id_str,
    otx_wall_str,
    inx_wall_str,
    inx_group_id_str,
    otx_group_id_str,
    inx_acct_id_str,
    otx_acct_id_str,
    inx_node_str,
    otx_node_str,
    inx_road_str,
    otx_road_str,
    inx_label_str,
    otx_label_str,
    unknown_word_str,
    nub_label_str,
    otx2inx_str,
    bridge_otx2inx_str,
    bridge_acct_id_str,
    bridge_group_id_str,
    bridge_node_str,
    bridge_road_str,
    bridge_nub_label_str,
)
from os import getcwd as os_getcwd


def test_str_functions_ReturnsObj():
    assert pidginunit_str() == "pidginunit"
    assert otx_wall_str() == "otx_wall"
    assert inx_wall_str() == "inx_wall"
    assert inx_group_id_str() == "inx_group_id"
    assert otx_group_id_str() == "otx_group_id"
    assert inx_acct_id_str() == "inx_acct_id"
    assert otx_acct_id_str() == "otx_acct_id"
    assert inx_node_str() == "inx_node"
    assert otx_node_str() == "otx_node"
    assert inx_road_str() == "inx_road"
    assert otx_road_str() == "otx_road"
    assert inx_label_str() == "inx_label"
    assert otx_label_str() == "otx_label"
    assert unknown_word_str() == "unknown_word"
    assert nub_label_str() == "nub_label"
    assert otx2inx_str() == "otx2inx"
    assert bridge_acct_id_str() == "bridge_acct_id"
    assert bridge_group_id_str() == "bridge_group_id"
    assert bridge_node_str() == "bridge_node"
    assert bridge_road_str() == "bridge_road"
    assert bridge_otx2inx_str() == "bridge_otx2inx"
    assert bridge_nub_label_str() == "bridge_nub_label"
    assert event_id_str() == "event_id"


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
    assert bridge_acct_id_str() in pidgin_config_categorys
    assert bridge_group_id_str() in pidgin_config_categorys
    assert bridge_node_str() in pidgin_config_categorys
    assert bridge_road_str() in pidgin_config_categorys
    assert bridge_nub_label_str() in pidgin_config_categorys
    assert len(pidgin_config) == 5

    _validate_pidgin_config(pidgin_config)
    bridge_road_dict = pidgin_config.get(bridge_road_str())
    bridge_nub_label_dict = pidgin_config.get(bridge_nub_label_str())
    assert len(bridge_road_dict.get(jkeys_str())) == 1
    assert len(bridge_nub_label_dict.get(jkeys_str())) == 1
    assert len(bridge_road_dict.get(jvalues_str())) == 4
    assert len(bridge_nub_label_dict.get(jvalues_str())) == 4

    # assert gen_jvalues == x_pidginunit_jvalues
    # assert len(pidginunit_dict.get(jvalues_str())) == 9
    # assert len(pidgin_purview_episode_dict.get(jvalues_str())) == 1
    # assert len(pidgin_cashbook_dict.get(jvalues_str())) == 1
    # assert len(pidgin_timeline_hour_dict.get(jvalues_str())) == 0
    # assert len(pidgin_timeline_month_dict.get(jvalues_str())) == 0
    # assert len(pidgin_timeline_weekday_dict.get(jvalues_str())) == 0


def _validate_pidgin_config(pidgin_config: dict):
    x_possible_args = {
        inx_wall_str(),
        otx_wall_str(),
        inx_group_id_str(),
        otx_group_id_str(),
        inx_acct_id_str(),
        otx_acct_id_str(),
        inx_node_str(),
        otx_node_str(),
        inx_road_str(),
        otx_road_str(),
        inx_label_str(),
        otx_label_str(),
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
    assert bridge_acct_id_str() in pidgin_config_categorys
    assert bridge_group_id_str() in pidgin_config_categorys
    assert bridge_node_str() in pidgin_config_categorys
    assert bridge_road_str() in pidgin_config_categorys
    assert bridge_nub_label_str() in pidgin_config_categorys
    assert len(pidgin_config_categorys) == 5


def test_get_pidgin_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidgin_args_category_mapping = get_pidgin_args_category_mapping()
    print(f"{x_pidgin_args_category_mapping=}")

    # THEN
    assert x_pidgin_args_category_mapping
    assert x_pidgin_args_category_mapping.get(otx_road_str())
    x_categorys = {bridge_road_str()}
    assert x_pidgin_args_category_mapping.get(otx_road_str()) == x_categorys
    assert x_pidgin_args_category_mapping.get(inx_wall_str())
    pidgin_id_categorys = x_pidgin_args_category_mapping.get(inx_wall_str())
    assert bridge_nub_label_str() in pidgin_id_categorys
    assert len(pidgin_id_categorys) == 5
    assert len(x_pidgin_args_category_mapping) == 13


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
    assert bridge_road_str() in set(get_quick_pidgens_column_ref().keys())
    assert len(get_quick_pidgens_column_ref().keys()) == 5
    assert get_quick_pidgens_column_ref() == all_pidgen_config_attrs
