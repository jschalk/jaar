from src.ch02_allot._ref.ch02_semantic_types import GrainNum, PoolNum, WeightNum
from src.ch03_voice._ref.ch03_semantic_types import (
    FundGrain,
    FundNum,
    GroupMark,
    GroupTitle,
    HealerName,
    NameTerm,
    RespectGrain,
    RespectNum,
    TitleTerm,
    VoiceName,
)
from src.ch04_rope._ref.ch04_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)


class ContextNum(float):
    """A numeric value that may converted to other Semantic Types by an external process driven by context."""

    pass
