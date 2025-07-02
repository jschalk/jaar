class KnotTerm(str):
    """A string to used as a delimiter in RopeTerms."""


def default_knot_if_None(knot: any = None) -> str:
    if knot != knot:  # float("nan")
        knot = None
    return knot if knot is not None else ";"


class LabelTerm(str):
    """A string representation of a tree node. Nodes cannot contain RopeTerm knot"""

    def is_label(self, knot: str = None) -> bool:
        return len(self) > 0 and self.contains_knot(knot)

    def contains_knot(self, knot: str = None) -> bool:
        return self.find(default_knot_if_None(knot)) == -1


class AxiomLabel(LabelTerm):
    """A string representation of a tree root node. Node cannot contain knot"""

    pass


class BeliefLabel(AxiomLabel):  # Created to help track the object class relations
    """An AxiomLabel for a Belief Belief. Cannot contain knot"""

    pass


class NameTerm(str):
    """All Name string classes should inherit from this class"""

    def is_name(self, knot: str = None) -> bool:
        return len(self) > 0 and self.contains_knot(knot)

    def contains_knot(self, knot: str = None) -> bool:
        return self.find(default_knot_if_None(knot)) == -1


class BelieverName(NameTerm):
    """A NameTerm used to identify a BelieverUnit's believer"""

    pass


class PersonName(BelieverName):  # Created to help track the object class relations
    """Every PersonName object is BelieverName, must follow BelieverName format."""

    pass


class HealerName(BelieverName):
    """A LabelTerm used to identify a Problem's Healer"""

    pass


class RopeTerm(str):
    """A string representation of a tree path. LabelTerms are seperated by rope knot"""

    pass


class EporTerm(str):
    """EporTerm is a RopeTerm in reverse direction. A string representation of a tree path. LabelTerms are seperated by rope knot."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains knots it represents a group otherwise it's a single member group of an PersonName."""


class GroupTitle(TitleTerm):  # Created to help track the object class relations
    pass


class FaceName(NameTerm):
    pass


class EventInt(int):
    pass
