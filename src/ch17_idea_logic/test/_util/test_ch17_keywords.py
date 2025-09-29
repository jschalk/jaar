from src.ch17_idea_logic._ref.ch17_keywords import Ch17Keywords, Ch17Keywords as wx


def test_Ch17Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch17Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert wx.allowed_crud == "allowed_crud"
    assert wx.build_order == "build_order"
    assert wx.delete_insert == "delete_insert"
    assert wx.delete_insert_update == "delete_insert_update"
    assert wx.delete_update == "delete_update"
    assert wx.error_message == "error_message"
    assert wx.idea_number == "idea_number"
    assert wx.idea_category == "idea_category"
    assert wx.insert_one_time == "insert_one_time"
    assert wx.insert_multiple == "insert_multiple"
    assert wx.insert_update == "insert_update"
    assert wx.world_name == "world_name"
