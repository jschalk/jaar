from ch02_allot._ref.ch02_semantic_types import GrainNum, PoolNum, WeightNum
from ch03_contact._ref.ch03_semantic_types import (
    ContactName,
    FundGrain,
    FundNum,
    GroupMark,
    GroupTitle,
    HealerName,
    NameTerm,
    RespectGrain,
    RespectNum,
    TitleTerm,
)
from ch05_rope._ref.ch05_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)


class ReasonNum(float):
    """A numeric value that may converted to other Semantic Types by an external process driven by context."""

    pass


class FactNum(float):
    """A numeric value that may converted to other Semantic Types by an external process driven by context."""

    pass
