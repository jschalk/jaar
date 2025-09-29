from src.ch16_translate_logic._ref.ch16_keywords import (
    Ch16Keywords,
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    otx2inx_str,
    otx_key_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    translate_core_str,
    translate_label_str,
    translate_name_str,
    translate_rope_str,
    translate_title_str,
    translateunit_str,
    unknown_str_str,
)


def test_Ch16Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch16Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert translateunit_str() == "translateunit"
    assert otx_knot_str() == "otx_knot"
    assert inx_knot_str() == "inx_knot"
    assert inx_title_str() == "inx_title"
    assert otx_title_str() == "otx_title"
    assert inx_name_str() == "inx_name"
    assert otx_name_str() == "otx_name"
    assert inx_label_str() == "inx_label"
    assert otx_label_str() == "otx_label"
    assert otx_key_str() == "otx_key"
    assert inx_rope_str() == "inx_rope"
    assert otx_rope_str() == "otx_rope"
    assert unknown_str_str() == "unknown_str"
    assert otx2inx_str() == "otx2inx"
    assert translate_name_str() == "translate_name"
    assert translate_title_str() == "translate_title"
    assert translate_label_str() == "translate_label"
    assert translate_rope_str() == "translate_rope"
    assert translate_core_str() == "translate_core"
