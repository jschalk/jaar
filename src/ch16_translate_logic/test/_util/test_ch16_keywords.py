from src.ch16_translate_logic._ref.ch16_keywords import Ch16Keywords, Ch16Keywords as wx


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
    assert wx.translateunit == "translateunit"
    assert wx.otx_knot == "otx_knot"
    assert wx.inx_knot == "inx_knot"
    assert wx.inx_title == "inx_title"
    assert wx.otx_title == "otx_title"
    assert wx.inx_name == "inx_name"
    assert wx.otx_name == "otx_name"
    assert wx.inx_label == "inx_label"
    assert wx.otx_label == "otx_label"
    assert wx.otx_key == "otx_key"
    assert wx.inx_rope == "inx_rope"
    assert wx.otx_rope == "otx_rope"
    assert wx.unknown_str == "unknown_str"
    assert wx.otx2inx == "otx2inx"
    assert wx.translate_name == "translate_name"
    assert wx.translate_title == "translate_title"
    assert wx.translate_label == "translate_label"
    assert wx.translate_rope == "translate_rope"
    assert wx.translate_core == "translate_core"
