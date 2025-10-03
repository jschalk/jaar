from inspect import getdoc as inspect_getdoc
from src.ch07_belief_logic._ref.ch07_keywords import Ch07Keywords as wx
from src.ch07_belief_logic._ref.ch07_semantic_types import (
    BeliefName,
    MomentLabel,
    MoneyGrain,
    NexusLabel,
)


def test_BeliefName_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_BeliefName_str = BeliefName(bob_str)
    # THEN
    assert bob_BeliefName_str == bob_str
    doc_str = "A NameTerm used to identify a BeliefUnit's belief"
    assert inspect_getdoc(bob_BeliefName_str) == doc_str


def test_NexusLabel_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_nexus = NexusLabel(empty_str)
    # THEN
    assert x_nexus == empty_str
    doc_str = f"The Nexus is the FirstLabel of all RopeTerms in a BeliefUnit. NexusLabel cannot contain a {wx.knot}."
    assert inspect_getdoc(x_nexus) == doc_str


def test_MomentLabel_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_MomentLabel_str = MomentLabel(bob_str)
    # THEN
    assert bob_MomentLabel_str == bob_str
    doc_str = "A NexusLabel for a Moment. Cannot contain knot."
    assert inspect_getdoc(bob_MomentLabel_str) == doc_str


def test_MoneyGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_money_grain = MoneyGrain(x_float)
    # THEN
    assert y_money_grain == x_float
    assert inspect_getdoc(y_money_grain) == "Smallest Unit of MoneyNum"
