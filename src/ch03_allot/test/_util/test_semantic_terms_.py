from inspect import getdoc as inspect_getdoc
from src.ch03_allot._ref.ch03_semantic_types import PoolNum, WeightNum


def test_PoolNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_PoolNum = PoolNum(x_float)
    # THEN
    assert y_PoolNum == x_float
    inspect_str = (
        """PoolNum represents any possible subset of the sum of numbers in the pool."""
    )
    assert inspect_getdoc(y_PoolNum) == inspect_str


def test_WeightNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_moneyunit = WeightNum(x_float)
    # THEN
    assert y_moneyunit == x_float
    doc_str = """WeightNum represents the unnormalized value of a ledger key. The sum of all WeightNum values in a ledger is not defined."""
    assert inspect_getdoc(y_moneyunit) == doc_str
