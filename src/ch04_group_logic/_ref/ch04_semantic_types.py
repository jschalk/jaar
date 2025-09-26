from src.ch02_rope_logic._ref.ch02_semantic_types import (
    LabelTerm,
    MomentLabel,
    RopeTerm,
    default_knot_if_None,
)


class NameTerm(LabelTerm):
    """All Name string classes should inherit from this class"""

    def is_name(self, knot: str = None) -> bool:
        return self.is_label(knot)


class VoiceName(NameTerm):  # Created to help track the object class relations
    """Every VoiceName object is NameTerm, must follow NameTerm format."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains knots it represents a group otherwise its a single member group of an VoiceName."""


class GroupTitle(TitleTerm):  # Created to help track the object class relations
    pass


class HealerName(NameTerm):
    """A LabelTerm used to identify a Problem's Healer"""

    pass
