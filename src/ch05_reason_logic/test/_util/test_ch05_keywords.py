from src.ch05_reason_logic._ref.ch05_keywords import Ch05Keywords, Ch05Keywords as wx


def test_Ch05Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch05Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert wx.active == "active"
    assert wx.status == "status"
    assert wx.task == "task"
    assert wx.cases == "cases"
    assert wx.fact_context == "fact_context"
    assert wx.fact_upper == "fact_upper"
    assert wx.fact_lower == "fact_lower"
    assert wx.fact_state == "fact_state"
    assert wx.factheirs == "factheirs"
    assert wx.factunits == "factunits"
    assert wx.reason_divisor == "reason_divisor"
    assert wx.reason_upper == "reason_upper"
    assert wx.reason_lower == "reason_lower"
    assert wx.reason_state == "reason_state"
    assert wx.reason_active_requisite == "reason_active_requisite"
    assert wx.reason_context == "reason_context"
    assert wx.reasonunits == "reasonunits"
