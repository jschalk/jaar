from inspect import getdoc as inspect_getdoc
from src.ch05_reason._ref.ch05_semantic_types import ContextNum
from src.ref.keywords import Ch05Keywords as kw


def test_ContextNum_Exists():
    # ESTABLISH
    four_int = 4
    # WHEN
    four_context_num = ContextNum(four_int)
    # THEN
    assert four_int == four_context_num
    doc_str = """A numeric value that may converted to other Semantic Types by an external process driven by context."""
    assert inspect_getdoc(four_context_num) == doc_str
