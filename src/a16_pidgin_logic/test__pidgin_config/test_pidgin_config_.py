from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path
from src.a08_bud_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
)
from src.a16_pidgin_logic._test_util.a16_str import (
    inx_bridge_str,
    inx_label_str,
    inx_name_str,
    inx_title_str,
    inx_way_str,
    map_otx2inx_str,
    otx2inx_str,
    otx_bridge_str,
    otx_label_str,
    otx_name_str,
    otx_title_str,
    otx_way_str,
    pidgin_core_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_title_str,
    pidgin_way_str,
    pidginunit_str,
    unknown_str_str,
)
from src.a16_pidgin_logic.pidgin_config import (
    config_file_dir,
    default_unknown_str,
    default_unknown_str_if_None,
    get_pidgin_args_dimen_mapping,
    get_pidgin_config_dict,
    get_pidgin_config_filename,
    get_pidgin_dimens,
    get_pidgin_filename,
    get_quick_pidgens_column_ref,
)


def test_get_pidgin_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_pidgin_config_filename() == "pidgin_config.json"


def test_get_pidgin_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_pidgin_filename() == "pidgin.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "a16_pidgin_logic")


def test_get_pidgin_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_config = get_pidgin_config_dict()

    # THEN
    assert pidgin_config
    pidgin_config_dimens = set(pidgin_config.keys())
    assert pidgin_name_str() in pidgin_config_dimens
    assert pidgin_title_str() in pidgin_config_dimens
    assert pidgin_label_str() in pidgin_config_dimens
    assert pidgin_way_str() in pidgin_config_dimens
    assert len(pidgin_config) == 4

    _validate_pidgin_config(pidgin_config)
    pidgin_way_dict = pidgin_config.get(pidgin_way_str())
    pidgin_label_dict = pidgin_config.get(pidgin_label_str())
    assert len(pidgin_way_dict.get(jkeys_str())) == 1
    assert len(pidgin_label_dict.get(jkeys_str())) == 1
    assert len(pidgin_way_dict.get(jvalues_str())) == 4
    assert len(pidgin_label_dict.get(jvalues_str())) == 4

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
        inx_title_str(),
        otx_title_str(),
        inx_name_str(),
        otx_name_str(),
        inx_label_str(),
        otx_label_str(),
        inx_way_str(),
        otx_way_str(),
        unknown_str_str(),
    }

    # for every pidgin_format file there exists a unique pidgin_number with leading zeros to make 5 digits
    for pidgin_dimens, dimen_dict in pidgin_config.items():
        print(f"_validate_pidgin_config {pidgin_dimens=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        assert dimen_dict.get(UPDATE_str()) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
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
    assert pidgin_name_str() in pidgin_config_dimens
    assert pidgin_title_str() in pidgin_config_dimens
    assert pidgin_label_str() in pidgin_config_dimens
    assert pidgin_way_str() in pidgin_config_dimens
    assert len(pidgin_config_dimens) == 4


def test_get_pidgin_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidgin_args_dimen_mapping = get_pidgin_args_dimen_mapping()
    print(f"{x_pidgin_args_dimen_mapping=}")

    # THEN
    assert x_pidgin_args_dimen_mapping
    assert x_pidgin_args_dimen_mapping.get(otx_way_str())
    x_dimens = {pidgin_way_str()}
    assert x_pidgin_args_dimen_mapping.get(otx_way_str()) == x_dimens
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
    assert pidgin_way_str() in set(get_quick_pidgens_column_ref().keys())
    assert len(get_quick_pidgens_column_ref().keys()) == 4
    assert get_quick_pidgens_column_ref() == all_pidgen_config_attrs


def test_default_unknown_str_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_str() == "UNKNOWN"


def test_default_unknown_str_if_None_ReturnsObj():
    # ESTABLISH
    unknown33_str = "unknown33"
    x_nan = float("nan")

    # WHEN / THEN
    assert default_unknown_str_if_None() == default_unknown_str()
    assert default_unknown_str_if_None(None) == default_unknown_str()
    assert default_unknown_str_if_None(unknown33_str) == unknown33_str
    assert default_unknown_str_if_None(x_nan) == default_unknown_str()
