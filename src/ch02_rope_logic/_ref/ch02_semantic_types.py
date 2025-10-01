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


class NexusLabel(LabelTerm):
    """A string representation of a tree root node. Node cannot contain knot."""

    pass


class RopeTerm(str):
    """A string representation of a tree path. LabelTerms are seperated by knots."""

    pass
