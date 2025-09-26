from inspect import getdoc as inspect_getdoc
from src.ch07_belief_logic._ref.ch07_semantic_types import BeliefName


def test_BeliefName_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_BeliefName_str = BeliefName(bob_str)
    # THEN
    assert bob_BeliefName_str == bob_str
    doc_str = "A NameTerm used to identify a BeliefUnit's belief"
    assert inspect_getdoc(bob_BeliefName_str) == doc_str
