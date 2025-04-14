from src.f02_bud.bud_config import max_tree_traverse_default


def test_max_tree_traverse_default_ReturnsObj() -> str:
    assert max_tree_traverse_default() == 20
