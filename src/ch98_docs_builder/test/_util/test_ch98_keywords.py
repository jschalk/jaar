from src.ch98_docs_builder._ref.ch98_keywords import rationale_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert rationale_str() == "rationale"
