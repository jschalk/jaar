from ch09_person_lesson._ref.ch09_semantic_types import MomentRope
from ch99_ref.keywords import Ch09Keywords as kw, ExampleStrs as exx
from inspect import getdoc as inspect_getdoc


def test_MomentRope_Exists():
    # ESTABLISH
    # WHEN
    bob_MomentRope_str = MomentRope(exx.bob)
    # THEN
    assert bob_MomentRope_str == exx.bob
    doc_str = f"The {kw.RopeTerm} for a Moment. Must contain knots."
    assert inspect_getdoc(bob_MomentRope_str) == doc_str
