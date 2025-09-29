from os import getcwd as os_getcwd
from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch16_translate_logic._ref.ch16_keywords import (
    Ch09Keywords as wx,
    DELETE_str,
    INSERT_str,
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
    otx2inx_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    reason_context_str,
    translate_core_str,
    translate_label_str,
    translate_name_str,
    translate_rope_str,
    translate_title_str,
    translateunit_str,
    unknown_str_str,
    voice_name_str,
)
from src.ch16_translate_logic.translate_config import (
    default_unknown_str,
    default_unknown_str_if_None,
    get_quick_translates_column_ref,
    get_translate_args_dimen_mapping,
    get_translate_config_dict,
    get_translate_dimens,
    get_translate_filename,
    translate_config_path,
)


def test_get_translate_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_translate_filename() == "translate.json"


def test_translate_config_path_ReturnsObj_Translate() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch16_translate_logic")
    assert translate_config_path() == create_path(chapter_dir, "translate_config.json")


def test_get_translate_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    translate_config = get_translate_config_dict()

    # THEN
    assert translate_config
    translate_config_dimens = set(translate_config.keys())
    assert translate_name_str() in translate_config_dimens
    assert translate_title_str() in translate_config_dimens
    assert translate_label_str() in translate_config_dimens
    assert translate_rope_str() in translate_config_dimens
    assert len(translate_config) == 4

    _validate_translate_config(translate_config)
    translate_rope_dict = translate_config.get(translate_rope_str())
    translate_label_dict = translate_config.get(translate_label_str())
    assert len(translate_rope_dict.get(jkeys_str())) == 1
    assert len(translate_label_dict.get(jkeys_str())) == 1
    assert len(translate_rope_dict.get(jvalues_str())) == 4
    assert len(translate_label_dict.get(jvalues_str())) == 4

    # assert gen_jvalues == x_translateunit_jvalues
    # assert len(translateunit_dict.get(jvalues_str())) == 9
    # assert len(translate_budunit_dict.get(jvalues_str())) == 1
    # assert len(translate_paybook_dict.get(jvalues_str())) == 1
    # assert len(translate_timeline_hour_dict.get(jvalues_str())) == 0
    # assert len(translate_timeline_month_dict.get(jvalues_str())) == 0
    # assert len(translate_timeline_weekday_dict.get(jvalues_str())) == 0


def _validate_translate_config(translate_config: dict):
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

    # for every translate_format file there exists a unique translate_number with leading zeros to make 5 digits
    for translate_dimens, dimen_dict in translate_config.items():
        print(f"_validate_translate_config {translate_dimens=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        assert dimen_dict.get(wx.UPDATE) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        translate_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in translate_jkeys_keys:
            print(f"_validate_translate_config {translate_dimens=} {jkey_key=} ")
            assert jkey_key in x_possible_args
        translate_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in translate_jvalues_keys:
            print(f"_validate_translate_config {translate_dimens=} {jvalue_key=} ")
            assert jvalue_key in x_possible_args


def test_get_translate_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    translate_config_dimens = get_translate_dimens()

    # THEN
    assert translate_name_str() in translate_config_dimens
    assert translate_title_str() in translate_config_dimens
    assert translate_label_str() in translate_config_dimens
    assert translate_rope_str() in translate_config_dimens
    assert len(translate_config_dimens) == 4


def test_get_translate_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_translate_args_dimen_mapping = get_translate_args_dimen_mapping()
    print(f"{x_translate_args_dimen_mapping=}")

    # THEN
    assert x_translate_args_dimen_mapping
    assert x_translate_args_dimen_mapping.get(otx_rope_str())
    x_dimens = {translate_rope_str()}
    assert x_translate_args_dimen_mapping.get(otx_rope_str()) == x_dimens
    assert x_translate_args_dimen_mapping.get(inx_knot_str())
    translate_id_dimens = x_translate_args_dimen_mapping.get(inx_knot_str())
    assert len(translate_id_dimens) == 4
    assert len(x_translate_args_dimen_mapping) == 11


def _get_all_translate_config_attrs() -> dict[str, set[str]]:
    translate_config = get_translate_config_dict()
    print(f"{translate_config=}")
    x_translate_attrs = {}
    for translate_dimen, jkeys_jvalues_dict in translate_config.items():
        attrs_set = set(jkeys_jvalues_dict.get("jkeys").keys())
        attrs_set.update(set(jkeys_jvalues_dict.get("jvalues").keys()))
        x_translate_attrs[translate_dimen] = attrs_set
    return x_translate_attrs


def test_get_quick_translates_column_ref_ReturnsObj():
    # ESTABLISH
    all_translate_config_attrs = _get_all_translate_config_attrs()
    # print(f"{all_translate_config_attrs=}")

    # WHEN / THEN
    assert translate_rope_str() in set(get_quick_translates_column_ref().keys())
    assert len(get_quick_translates_column_ref().keys()) == 4
    assert get_quick_translates_column_ref() == all_translate_config_attrs


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
