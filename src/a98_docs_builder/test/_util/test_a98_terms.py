from src.a98_docs_builder._ref.a98_terms import rationale_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert rationale_str() == "rationale"
