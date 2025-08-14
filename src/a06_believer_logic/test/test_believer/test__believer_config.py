from src.a06_believer_logic.believer_config import max_tree_traverse_default


def test_max_tree_traverse_default_ReturnsObj() -> str:
    # ESTABLISH / WHEN / THEN
    assert max_tree_traverse_default() == 20
