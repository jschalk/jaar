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


class VowLabel(AxiomLabel):  # Created to help track the object class relations
    """An AxiomLabel for a Vow Vow. Cannot contain knot"""

    pass


class NameTerm(str):
    """All Name string classes should inherit from this class"""

    def is_name(self, knot: str = None) -> bool:
        return len(self) > 0 and self.contains_knot(knot)

    def contains_knot(self, knot: str = None) -> bool:
        return self.find(default_knot_if_None(knot)) == -1


class OwnerName(NameTerm):
    """A NameTerm used to identify a PlanUnit's owner"""

    pass


class AcctName(OwnerName):  # Created to help track the object class relations
    """Every AcctName object is OwnerName, must follow OwnerName format."""

    pass


class HealerName(OwnerName):
    """A LabelTerm used to identify a Problem's Healer"""

    pass


class RopeTerm(str):
    """A string representation of a tree path. LabelTerms are seperated by rope knot"""

    pass


class YawTerm(str):
    """YawTerm is a RopeTerm in reverse direction. A string representation of a tree path. LabelTerms are seperated by rope knot."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains knots it represents a group otherwise it's a single member group of an AcctName."""


class GroupTitle(TitleTerm):  # Created to help track the object class relations
    pass


class FaceName(NameTerm):
    pass


class EventInt(int):
    pass
