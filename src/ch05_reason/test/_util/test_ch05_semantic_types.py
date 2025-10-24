from inspect import getdoc as inspect_getdoc
from src.ch05_reason._ref.ch05_semantic_types import MaybeEpoch
from src.ref.keywords import Ch05Keywords as kw


def test_MaybeEpoch_Exists():
    # ESTABLISH
    four_int = 4
    # WHEN
    maybe_four_int = MaybeEpoch(four_int)
    # THEN
    assert four_int == maybe_four_int
    doc_str = """A numeric value that may or may not represent an min in an Epoch.
It's Epoch-relatedness is determined externally by context."""
    assert inspect_getdoc(maybe_four_int) == doc_str
