from src.ch05_reason_logic._ref.ch05_semantic_types import (
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
