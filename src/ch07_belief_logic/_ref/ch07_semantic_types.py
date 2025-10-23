from src.ch06_plan._ref.ch06_semantic_types import (
    FirstLabel,
    FundGrain,
    FundNum,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    NameTerm,
    RespectGrain,
    RespectNum,
    RopeTerm,
    TitleTerm,
    VoiceName,
    default_knot_if_None,
)


class MomentLabel(LabelTerm):  # Created to help track the object class relations
    """A LabelTerm for a Moment. Cannot contain knot."""

    pass


class BeliefName(NameTerm):
    """A NameTerm used to identify a BeliefUnit's belief"""

    pass


class ManaGrain(float):
    """Smallest Unit of Mana Num"""

    pass
