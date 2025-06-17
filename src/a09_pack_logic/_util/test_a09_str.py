from src.a09_pack_logic._util.a09_str import event_int_str, face_name_str


def test_str_functions_ReturnsObj():
    assert event_int_str() == "event_int"
    assert face_name_str() == "face_name"
