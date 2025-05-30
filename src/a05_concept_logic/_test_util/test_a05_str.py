from src.a05_concept_logic._test_util.a05_str import (
    begin_str,
    close_str,
    concept_label_str,
    concept_way_str,
    denom_str,
    gogo_want_str,
    healer_name_str,
    mass_str,
    morph_str,
    numor_str,
    pledge_str,
    stop_want_str,
)


def test_str_functions_ReturnsObj():
    assert concept_label_str() == "concept_label"
    assert denom_str() == "denom"
    assert numor_str() == "numor"
    assert pledge_str() == "pledge"
    assert begin_str() == "begin"
    assert close_str() == "close"
    assert morph_str() == "morph"
    assert concept_way_str() == "concept_way"
    assert gogo_want_str() == "gogo_want"
    assert stop_want_str() == "stop_want"
    assert mass_str() == "mass"
    assert healer_name_str() == "healer_name"
