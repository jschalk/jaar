from src.ch10_pack_logic._ref.ch10_keywords import (
    FaceName_str,
    event_int_str,
    face_name_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert FaceName_str() == "FaceName"
    assert event_int_str() == "event_int"
    assert face_name_str() == "face_name"
