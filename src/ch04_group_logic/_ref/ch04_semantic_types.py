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


# def test_NameTerm_Exists():
#     # ESTABLISH
#     bob_str = "Bob"
#     # WHEN
#     bob_nameterm = NameTerm(bob_str)
#     # THEN
#     assert bob_nameterm == bob_str
#     doc_str = "All Name string classes should inherit from this class"
#     assert inspect_getdoc(bob_nameterm) == doc_str


# def test_NameTerm_is_name_ReturnsObj_Scenario0():
#     # ESTABLISH / WHEN / THEN
#     assert NameTerm("").is_name() is False
#     assert NameTerm("A").is_name()

#     # WHEN / THEN
#     x_s = default_knot_if_None()
#     x_nameterm = NameTerm(f"casa{x_s}kitchen")
#     assert x_nameterm.is_name() is False


# def test_NameTerm_is_name_ReturnsObj_Scenario1():
#     # ESTABLISH / WHEN / THEN
#     slash_str = "/"
#     x_nameterm = NameTerm(f"casa{slash_str}kitchen")
#     assert x_nameterm.is_name()
#     assert x_nameterm.is_name(slash_str) is False


# def test_HealerName_Exists():
#     # ESTABLISH
#     bob_str = "Bob"
#     # WHEN
#     bob_healer_str = HealerName(bob_str)
#     # THEN
#     assert bob_healer_str == bob_str
#     doc_str = "A LabelTerm used to identify a Problem's Healer"
#     assert inspect_getdoc(bob_healer_str) == doc_str


# def test_VoiceName_Exists():
#     # ESTABLISH
#     bob_str = "Bob"
#     # WHEN
#     bob_VoiceName = VoiceName(bob_str)
#     # THEN
#     assert bob_VoiceName == bob_str
#     doc_str = "Every VoiceName object is NameTerm, must follow NameTerm format."
#     assert inspect_getdoc(bob_VoiceName) == doc_str


# def test_TitleTerm_Exists():
#     # ESTABLISH
#     bob_str = "Bob"
#     # WHEN
#     bob_nameterm = TitleTerm(bob_str)
#     # THEN
#     assert bob_nameterm == bob_str
#     doc_str = f"""If a TitleTerm contains {knot_str()}s it represents a group otherwise its a single member group of an VoiceName."""
#     assert inspect_getdoc(bob_nameterm) == doc_str


# def test_GroupTitle_Exists():
#     # ESTABLISH / WHEN
#     bikers_GroupTitle = GroupTitle(";bikers")

#     # THEN
#     assert bikers_GroupTitle is not None
