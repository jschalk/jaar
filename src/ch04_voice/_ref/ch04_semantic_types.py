from src.ch03_rope._ref.ch03_semantic_types import (
    FirstLabel,
    GrainNum,
    LabelTerm,
    PoolNum,
    RopeTerm,
    WeightNum,
    default_knot_if_None,
)


class GroupMark(str):
    """GroupMark(s) exist in TitleTerms to indicate its a group, no GroupMark indicates it is a VoiceName."""

    pass


def default_groupmark_if_None(groupmark: GroupMark = None) -> GroupMark:
    if groupmark != groupmark:  # float("nan")
        groupmark = None
    return groupmark if groupmark is not None else ";"


class NameTerm(LabelTerm):
    """All Name string classes should inherit from this class"""

    def is_name(self, groupmark: GroupMark = None) -> bool:
        return len(self) > 0 and self.contains_groupmark(groupmark)

    def contains_groupmark(self, groupmark: str = None) -> bool:
        return self.find(default_groupmark_if_None(groupmark)) == -1


class VoiceName(NameTerm):
    """Every VoiceName object is NameTerm, must follow NameTerm format."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains SepartorTerms(s) it represents a group otherwise its a single member group of an VoiceName."""


class GroupTitle(TitleTerm):
    pass


class HealerName(NameTerm):
    """A NameTerm used to identify a Problem's Healer"""

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
