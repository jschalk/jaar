class KnotTerm(str):
    """A string to used as a delimiter in RopePointers."""


def default_knot_if_None(knot: any = None) -> str:
    if knot != knot:  # float("nan")
        knot = None
    return knot if knot is not None else ";"


class LabelTerm(str):
    """A string representation of a tree node. Nodes cannot contain RopePointer knot"""

    def is_label(self, knot: str = None) -> bool:
        return len(self) > 0 and self.contains_knot(knot)

    def contains_knot(self, knot: str = None) -> bool:
        return self.find(default_knot_if_None(knot)) == -1


class CentralLabel(LabelTerm):
    """A string representation of a tree root node. Node cannot contain knot"""

    pass


class MomentLabel(CentralLabel):  # Created to help track the object class relations
    """A CentralLabel for a Moment. Cannot contain knot."""

    pass


class NameTerm(LabelTerm):
    """All Name string classes should inherit from this class"""

    def is_name(self, knot: str = None) -> bool:
        return self.is_label(knot)

    def contains_knot(self, knot: str = None) -> bool:
        return self.find(default_knot_if_None(knot)) == -1


class BeliefName(NameTerm):
    """A NameTerm used to identify a BeliefUnit's belief"""

    pass


class VoiceName(BeliefName):  # Created to help track the object class relations
    """Every VoiceName object is BeliefName, must follow BeliefName format."""

    pass


class HealerName(BeliefName):
    """A LabelTerm used to identify a Problem's Healer"""

    pass


class RopePointer(str):
    """A string representation of a tree path. LabelTerms are seperated by rope knot"""

    pass


class TitleTerm(str):
    """If a TitleTerm contains knots it represents a group otherwise its a single member group of an VoiceName."""


class GroupTitle(TitleTerm):  # Created to help track the object class relations
    pass


class FaceName(NameTerm):
    pass


class EventInt(int):
    pass
