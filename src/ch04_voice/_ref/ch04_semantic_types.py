from src.ch03_rope._ref.ch03_semantic_types import (
    FirstLabel,
    GrainNum,
    LabelTerm,
    PoolNum,
    RopeTerm,
    WeightNum,
    default_knot_if_None,
)


class NameTerm(LabelTerm):
    """All Name string classes should inherit from this class"""


class VoiceName(NameTerm):
    """Every VoiceName object is NameTerm, must follow NameTerm format."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains SepartorTerms(s) it represents a group otherwise its a single member group of an VoiceName."""


class GroupTitle(TitleTerm):
    pass


class HealerName(NameTerm):
    """A LabelTerm used to identify a Problem's Healer"""

    pass


class FundNum(float):
    """FundNum inherits from float class"""

    pass


class FundGrain(float):
    """Smallest Unit of fund_num"""

    pass


class RespectNum(float):
    """RespectNum inherits from float class"""

    pass


class RespectGrain(float):
    """Smallest Unit of score (RespectNum) ala 'the slightest bit of respect!'"""

    pass
