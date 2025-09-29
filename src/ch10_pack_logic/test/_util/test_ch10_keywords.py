from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch10Keywords,
    FaceName_str,
    event_int_str,
    face_name_str,
)


def test_Ch10Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch10Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert FaceName_str() == "FaceName"
    assert event_int_str() == "event_int"
    assert face_name_str() == "face_name"
