from src.ch02_rope._ref.ch02_semantic_types import (
    FirstLabel,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)


class GrainNum(float):
    """GrainNum represents the smallest fraction allowed"""

    pass


class PoolNum(float):
    """PoolNum represents any possible subset of the sum of numbers in the pool."""

    pass


class WeightNum(float):
    """WeightNum represents the unnormalized value of a ledger key. The sum of all WeightNum values in a ledger is not defined."""

    pass
