from src.ch20_world_logic._ref.ch20_keywords import WorldName_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert WorldName_str() == "WorldName"
