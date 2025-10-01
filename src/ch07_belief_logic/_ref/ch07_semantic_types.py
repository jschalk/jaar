from src.ch06_plan_logic._ref.ch06_semantic_types import (
    GroupTitle,
    HealerName,
    LabelTerm,
    NameTerm,
    NexusLabel,
    RopeTerm,
    TitleTerm,
    VoiceName,
    default_knot_if_None,
)


class MomentLabel(NexusLabel):  # Created to help track the object class relations
    """A NexusLabel for a Moment. Cannot contain knot."""

    pass


class BeliefName(NameTerm):
    """A NameTerm used to identify a BeliefUnit's belief"""

    pass
