from src.a09_pack_logic._ref.a09_terms import event_int_str, face_name_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert event_int_str() == "event_int"
    assert face_name_str() == "face_name"
