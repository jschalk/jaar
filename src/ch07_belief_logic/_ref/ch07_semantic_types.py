from src.ch06_plan._ref.ch06_semantic_types import (
    FirstLabel,
    FundGrain,
    FundNum,
    GroupTitle,
    HealerName,
    LabelTerm,
    NameTerm,
    RespectGrain,
    RespectNum,
    RopeTerm,
    TitleTerm,
    VoiceName,
    default_knot_if_None,
)


class NexusLabel(FirstLabel):
    """The Nexus is the FirstLabel of all RopeTerms in a BeliefUnit. NexusLabel cannot contain a knot."""

    pass


class MomentLabel(NexusLabel):  # Created to help track the object class relations
    """A NexusLabel for a Moment. Cannot contain knot."""

    pass


class BeliefName(NameTerm):
    """A NameTerm used to identify a BeliefUnit's belief"""

    pass


class MoneyGrain(float):
    """Smallest Unit of Money Num"""

    pass
