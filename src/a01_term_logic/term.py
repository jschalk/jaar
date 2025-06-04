class BridgeTerm(str):
    """A string to used as a delimiter in WayTerms."""


def default_bridge_if_None(bridge: any = None) -> str:
    if bridge != bridge:  # float("nan")
        bridge = None
    return bridge if bridge is not None else ";"


class LabelTerm(str):
    """A string representation of a tree node. Nodes cannot contain WayTerm bridge"""

    def is_label(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class AxiomLabel(LabelTerm):
    """A string representation of a tree root node. Node cannot contain bridge"""

    pass


class FiscLabel(LabelTerm):  # Created to help track the object class relations
    pass


class NameTerm(str):
    """All Name string classes should inherit from this class"""

    def is_name(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class OwnerName(NameTerm):
    """A NameTerm used to identify a BudUnit's owner"""

    pass


class AcctName(OwnerName):  # Created to help track the object class relations
    """Every AcctName object is OwnerName, must follow OwnerName format."""

    pass


class HealerName(OwnerName):
    """A LabelTerm used to identify a Problem's Healer"""

    pass


class WayTerm(str):
    """A string representation of a tree path. LabelTerms are seperated by way bridge"""

    pass


class YawTerm(str):
    """YawTerm is a WayTerm in reverse direction. A string representation of a tree path. LabelTerms are seperated by way bridge."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains bridges it represents a group otherwise it's a single member group of an AcctName."""


class GroupTitle(TitleTerm):  # Created to help track the object class relations
    pass


class FaceName(NameTerm):
    pass


class EventInt(int):
    pass
