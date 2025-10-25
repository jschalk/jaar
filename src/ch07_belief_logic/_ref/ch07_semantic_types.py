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
from src.ch05_reason._ref.ch05_semantic_types import ContextNum


class MomentLabel(LabelTerm):  # Created to help track the object class relations
    """A LabelTerm for a Moment. Cannot contain knot."""

    pass


class BeliefName(NameTerm):
    """A NameTerm used to identify a BeliefUnit's belief"""

    pass


class ManaGrain(float):
    """Smallest Unit of Mana Num"""

    pass
