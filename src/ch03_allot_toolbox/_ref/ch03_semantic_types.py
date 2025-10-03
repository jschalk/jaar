from src.ch02_rope_logic._ref.ch02_semantic_types import (
    FirstLabel,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)


class GrainNum(float):
    """GrainNum represents the smallest fraction allowed"""

    pass


class PoolNum(float):
    """PoolNum represents the sum of all numbers in play."""

    pass


class MoneyNum(float):
    """MoneyNum inherits from float class"""

    pass


class RespectNum(float):
    """RespectNum inherits from float class"""

    pass


class RespectGrain(float):
    """Smallest Unit of score (RespectNum) ala 'the slightest bit of respect!'"""

    pass
