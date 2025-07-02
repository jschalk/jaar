from inspect import getdoc as inspect_getdoc
from src.a01_term_logic.term import (
    AcctName,
    AxiomLabel,
    BeliefLabel,
    EporTerm,
    EventInt,
    FaceName,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    NameTerm,
    OwnerName,
    RopeTerm,
    TitleTerm,
    default_knot_if_None,
)
from src.a01_term_logic.test._util.a01_str import knot_str


def test_KnotTerm_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_knot = KnotTerm(empty_str)
    # THEN
    assert x_knot == empty_str
    doc_str = f"A string to used as a delimiter in RopeTerms."
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


def test_NameTerm_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_nameterm = NameTerm(bob_str)
    # THEN
    assert bob_nameterm == bob_str
    doc_str = "All Name string classes should inherit from this class"
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_NameTerm_is_name_ReturnsObj_Scenario0():
    # WHEN / THEN
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


def test_HealerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_healer_str = HealerName(bob_str)
    # THEN
    assert bob_healer_str == bob_str
    doc_str = "A LabelTerm used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_str) == doc_str


def test_OwnerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_OwnerName_str = OwnerName(bob_str)
    # THEN
    assert bob_OwnerName_str == bob_str
    doc_str = "A NameTerm used to identify a OwnerUnit's owner"
    assert inspect_getdoc(bob_OwnerName_str) == doc_str


def test_AcctName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_AcctName = AcctName(bob_str)
    # THEN
    assert bob_AcctName == bob_str
    doc_str = "Every AcctName object is OwnerName, must follow OwnerName format."
    assert inspect_getdoc(bob_AcctName) == doc_str


def test_TitleTerm_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_nameterm = TitleTerm(bob_str)
    # THEN
    assert bob_nameterm == bob_str
    doc_str = f"""If a TitleTerm contains {knot_str()}s it represents a group otherwise it's a single member group of an AcctName."""
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_GroupTitle_exists():
    bikers_GroupTitle = GroupTitle(";bikers")
    assert bikers_GroupTitle is not None
    assert str(type(bikers_GroupTitle)).find("src.a01_term_logic.term.GroupTitle") > 0


def test_LabelTerm_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_rope = LabelTerm(empty_str)
    # THEN
    assert x_rope == empty_str
    doc_str = f"A string representation of a tree node. Nodes cannot contain RopeTerm {knot_str()}"
    assert inspect_getdoc(x_rope) == doc_str


def test_LabelTerm_is_label_ReturnsObj_Scenario0():
    # WHEN / THEN
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


def test_AxiomLabel_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_axiom = AxiomLabel(empty_str)
    # THEN
    assert x_axiom == empty_str
    doc_str = (
        f"A string representation of a tree root node. Node cannot contain {knot_str()}"
    )
    assert inspect_getdoc(x_axiom) == doc_str


def test_RopeTerm_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_rope = RopeTerm(empty_str)
    # THEN
    assert x_rope == empty_str
    doc_str = f"A string representation of a tree path. LabelTerms are seperated by rope {knot_str()}"
    assert inspect_getdoc(x_rope) == doc_str


def test_EporTerm_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_rope = EporTerm(empty_str)
    # THEN
    assert x_rope == empty_str
    doc_str = f"EporTerm is a RopeTerm in reverse direction. A string representation of a tree path. LabelTerms are seperated by rope {knot_str()}."
    assert inspect_getdoc(x_rope) == doc_str


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cookie") == "cookie"
    assert not FaceName(f"cookie{default_knot_if_None()}").is_name()


def test_EventInt_Exists():
    # ESTABLISH / WHEN / THEN
    assert EventInt() == 0
    assert EventInt(12) == 12
    assert EventInt(12.4) == 12


def test_BeliefLabel_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_belief = BeliefLabel(empty_str)
    # THEN
    assert x_belief == empty_str
    doc_str = f"An AxiomLabel for a Belief Belief. Cannot contain {knot_str()}"
    assert inspect_getdoc(x_belief) == doc_str
