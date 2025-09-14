from src.a98_docs_builder.test._util.a98_terms import rationale_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert rationale_str() == "rationale"
