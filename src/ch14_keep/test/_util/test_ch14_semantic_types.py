from inspect import getdoc as inspect_getdoc
from src.ch14_keep._ref.ch14_semantic_types import MoneyNum


def test_MoneyNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_moneyunit = MoneyNum(x_float)
    # THEN
    assert y_moneyunit == x_float
    assert inspect_getdoc(y_moneyunit) == "MoneyNum inherits from float class"
