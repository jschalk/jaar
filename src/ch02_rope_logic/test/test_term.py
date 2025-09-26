from inspect import getdoc as inspect_getdoc
from src.ch02_rope_logic._ref.ch02_keywords import knot_str
from src.ch02_rope_logic._ref.ch02_semantic_types import (
    BeliefName,
    CentralLabel,
    EventInt,
    FaceName,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    MomentLabel,
    NameTerm,
    RopeTerm,
    TitleTerm,
    VoiceName,
    default_knot_if_None,
)


def test_KnotTerm_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_knot = KnotTerm(empty_str)
    # THEN
    assert x_knot == empty_str
    doc_str = "A string to used as a delimiter in RopeTerms."
    assert inspect_getdoc(x_knot) == doc_str


def test_default_knot_if_None_ReturnsObj():
    # ESTABLISH
    semicolon_str = ";"
    slash_str = "/"
    colon_str = ":"
    bob_str = "Bob"

    # WHEN / THEN
    assert default_knot_if_None() == semicolon_str
    assert default_knot_if_None(None) == semicolon_str
    x_nan = float("nan")
    assert default_knot_if_None(x_nan) == semicolon_str
    assert default_knot_if_None(slash_str) == slash_str
    assert default_knot_if_None(colon_str) == colon_str
    assert default_knot_if_None(bob_str) == bob_str


def test_NameTerm_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_nameterm = NameTerm(bob_str)
    # THEN
    assert bob_nameterm == bob_str
    doc_str = "All Name string classes should inherit from this class"
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_NameTerm_is_name_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN / THEN
    assert NameTerm("").is_name() is False
    assert NameTerm("A").is_name()

    # WHEN / THEN
    x_s = default_knot_if_None()
    x_nameterm = NameTerm(f"casa{x_s}kitchen")
    assert x_nameterm.is_name() is False


def test_NameTerm_is_name_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_nameterm = NameTerm(f"casa{slash_str}kitchen")
    assert x_nameterm.is_name()
    assert x_nameterm.is_name(slash_str) is False


def test_HealerName_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_healer_str = HealerName(bob_str)
    # THEN
    assert bob_healer_str == bob_str
    doc_str = "A LabelTerm used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_str) == doc_str


def test_BeliefName_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_BeliefName_str = BeliefName(bob_str)
    # THEN
    assert bob_BeliefName_str == bob_str
    doc_str = "A NameTerm used to identify a BeliefUnit's belief"
    assert inspect_getdoc(bob_BeliefName_str) == doc_str


def test_VoiceName_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_VoiceName = VoiceName(bob_str)
    # THEN
    assert bob_VoiceName == bob_str
    doc_str = "Every VoiceName object is BeliefName, must follow BeliefName format."
    assert inspect_getdoc(bob_VoiceName) == doc_str


def test_TitleTerm_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_nameterm = TitleTerm(bob_str)
    # THEN
    assert bob_nameterm == bob_str
    doc_str = f"""If a TitleTerm contains {knot_str()}s it represents a group otherwise its a single member group of an VoiceName."""
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_GroupTitle_Exists():
    # ESTABLISH / WHEN
    bikers_GroupTitle = GroupTitle(";bikers")

    # THEN
    assert bikers_GroupTitle is not None


def test_LabelTerm_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_rope = LabelTerm(empty_str)
    # THEN
    assert x_rope == empty_str
    doc_str = f"A string representation of a tree node. Nodes cannot contain RopeTerm {knot_str()}"
    assert inspect_getdoc(x_rope) == doc_str


def test_LabelTerm_is_label_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN / THEN
    assert LabelTerm("").is_label() is False
    assert LabelTerm("A").is_label()

    # WHEN / THEN
    x_s = default_knot_if_None()
    x_labelterm = LabelTerm(f"casa{x_s}kitchen")
    assert x_labelterm.is_label() is False


def test_LabelTerm_is_label_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_labelterm = LabelTerm(f"casa{slash_str}kitchen")
    assert x_labelterm.is_label()
    assert x_labelterm.is_label(slash_str) is False


def test_CentralLabel_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_central = CentralLabel(empty_str)
    # THEN
    assert x_central == empty_str
    doc_str = (
        f"A string representation of a tree root node. Node cannot contain {knot_str()}"
    )
    assert inspect_getdoc(x_central) == doc_str


def test_RopeTerm_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_rope = RopeTerm(empty_str)
    # THEN
    assert x_rope == empty_str
    doc_str = f"A string representation of a tree path. LabelTerms are seperated by rope {knot_str()}"
    assert inspect_getdoc(x_rope) == doc_str


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cookie") == "cookie"
    assert not FaceName(f"cookie{default_knot_if_None()}").is_name()


# Move to Bud chapter
def test_EventInt_Exists():
    # ESTABLISH / WHEN / THEN
    assert EventInt() == 0
    assert EventInt(12) == 12
    assert EventInt(12.4) == 12


def test_MomentLabel_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_moment = MomentLabel(empty_str)
    # THEN
    assert x_moment == empty_str
    doc_str = f"A CentralLabel for a Moment. Cannot contain {knot_str()}."
    assert inspect_getdoc(x_moment) == doc_str
