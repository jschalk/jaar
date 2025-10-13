from inspect import getdoc as inspect_getdoc
from src.ch02_rope._ref.ch02_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from src.ref.keywords import Ch02Keywords as wx


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


def test_LabelTerm_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_rope = LabelTerm(empty_str)
    # THEN
    assert x_rope == empty_str
    doc_str = f"A string representation of a tree node. Nodes cannot contain RopeTerm {wx.knot}"
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


def test_FirstLabel_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_first = FirstLabel(empty_str)
    # THEN
    assert x_first == empty_str
    doc_str = f"The first LabelTerm in a RopeTerm. FirstLabel cannot contain {wx.knot}."
    assert inspect_getdoc(x_first) == doc_str


def test_RopeTerm_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_rope = RopeTerm(empty_str)
    # THEN
    assert x_rope == empty_str
    doc_str = f"A string representation of a tree path. LabelTerms are seperated by {wx.knot}s."
    assert inspect_getdoc(x_rope) == doc_str
