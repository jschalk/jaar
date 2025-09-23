from os import getcwd as os_getcwd
from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch16_lire_logic._ref.ch16_keywords import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    jkeys_str,
    jvalues_str,
    lire_core_str,
    lire_label_str,
    lire_name_str,
    lire_rope_str,
    lire_title_str,
    lireunit_str,
    normal_specs_str,
    otx2inx_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    reason_context_str,
    unknown_str_str,
    voice_name_str,
)
from src.ch16_lire_logic.lire_config import (
    default_unknown_str,
    default_unknown_str_if_None,
    get_lire_args_dimen_mapping,
    get_lire_config_dict,
    get_lire_dimens,
    get_lire_filename,
    get_quick_lires_column_ref,
    lire_config_path,
)


def test_get_lire_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_lire_filename() == "lire.json"


def test_lire_config_path_ReturnsObj_Lire() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch16_lire_logic")
    assert lire_config_path() == create_path(chapter_dir, "lire_config.json")


def test_get_lire_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    lire_config = get_lire_config_dict()

    # THEN
    assert lire_config
    lire_config_dimens = set(lire_config.keys())
    assert lire_name_str() in lire_config_dimens
    assert lire_title_str() in lire_config_dimens
    assert lire_label_str() in lire_config_dimens
    assert lire_rope_str() in lire_config_dimens
    assert len(lire_config) == 4

    _validate_lire_config(lire_config)
    lire_rope_dict = lire_config.get(lire_rope_str())
    lire_label_dict = lire_config.get(lire_label_str())
    assert len(lire_rope_dict.get(jkeys_str())) == 1
    assert len(lire_label_dict.get(jkeys_str())) == 1
    assert len(lire_rope_dict.get(jvalues_str())) == 4
    assert len(lire_label_dict.get(jvalues_str())) == 4

    # assert gen_jvalues == x_lireunit_jvalues
    # assert len(lireunit_dict.get(jvalues_str())) == 9
    # assert len(lire_budunit_dict.get(jvalues_str())) == 1
    # assert len(lire_paybook_dict.get(jvalues_str())) == 1
    # assert len(lire_timeline_hour_dict.get(jvalues_str())) == 0
    # assert len(lire_timeline_month_dict.get(jvalues_str())) == 0
    # assert len(lire_timeline_weekday_dict.get(jvalues_str())) == 0


def _validate_lire_config(lire_config: dict):
    x_possible_args = {
        inx_knot_str(),
        otx_knot_str(),
        inx_title_str(),
        otx_title_str(),
        inx_name_str(),
        otx_name_str(),
        inx_label_str(),
        otx_label_str(),
        inx_rope_str(),
        otx_rope_str(),
        unknown_str_str(),
    }

    # for every lire_format file there exists a unique lire_number with leading zeros to make 5 digits
    for lire_dimens, dimen_dict in lire_config.items():
        print(f"_validate_lire_config {lire_dimens=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        assert dimen_dict.get(UPDATE_str()) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        lire_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in lire_jkeys_keys:
            print(f"_validate_lire_config {lire_dimens=} {jkey_key=} ")
            assert jkey_key in x_possible_args
        lire_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in lire_jvalues_keys:
            print(f"_validate_lire_config {lire_dimens=} {jvalue_key=} ")
            assert jvalue_key in x_possible_args


def test_get_lire_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    lire_config_dimens = get_lire_dimens()

    # THEN
    assert lire_name_str() in lire_config_dimens
    assert lire_title_str() in lire_config_dimens
    assert lire_label_str() in lire_config_dimens
    assert lire_rope_str() in lire_config_dimens
    assert len(lire_config_dimens) == 4


def test_get_lire_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_lire_args_dimen_mapping = get_lire_args_dimen_mapping()
    print(f"{x_lire_args_dimen_mapping=}")

    # THEN
    assert x_lire_args_dimen_mapping
    assert x_lire_args_dimen_mapping.get(otx_rope_str())
    x_dimens = {lire_rope_str()}
    assert x_lire_args_dimen_mapping.get(otx_rope_str()) == x_dimens
    assert x_lire_args_dimen_mapping.get(inx_knot_str())
    lire_id_dimens = x_lire_args_dimen_mapping.get(inx_knot_str())
    assert len(lire_id_dimens) == 4
    assert len(x_lire_args_dimen_mapping) == 11


def _get_all_lire_config_attrs() -> dict[str, set[str]]:
    lire_config = get_lire_config_dict()
    print(f"{lire_config=}")
    x_lire_attrs = {}
    for lire_dimen, jkeys_jvalues_dict in lire_config.items():
        attrs_set = set(jkeys_jvalues_dict.get("jkeys").keys())
        attrs_set.update(set(jkeys_jvalues_dict.get("jvalues").keys()))
        x_lire_attrs[lire_dimen] = attrs_set
    return x_lire_attrs


def test_get_quick_lires_column_ref_ReturnsObj():
    # ESTABLISH
    all_lire_config_attrs = _get_all_lire_config_attrs()
    # print(f"{all_lire_config_attrs=}")

    # WHEN / THEN
    assert lire_rope_str() in set(get_quick_lires_column_ref().keys())
    assert len(get_quick_lires_column_ref().keys()) == 4
    assert get_quick_lires_column_ref() == all_lire_config_attrs


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
