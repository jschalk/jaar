from inspect import getdoc as inspect_getdoc
from src.ch14_keep._ref.ch14_semantic_types import ManaNum


def test_ManaNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_manaunit = ManaNum(x_float)
    # THEN
    assert y_manaunit == x_float
    assert inspect_getdoc(y_manaunit) == "ManaNum inherits from float class"
