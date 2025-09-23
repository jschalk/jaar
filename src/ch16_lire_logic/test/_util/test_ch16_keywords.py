from src.ch16_lire_logic._ref.ch16_keywords import (
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    lire_core_str,
    lire_label_str,
    lire_name_str,
    lire_rope_str,
    lire_title_str,
    lireunit_str,
    otx2inx_str,
    otx_key_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    unknown_str_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert lireunit_str() == "lireunit"
    assert otx_knot_str() == "otx_knot"
    assert inx_knot_str() == "inx_knot"
    assert inx_title_str() == "inx_title"
    assert otx_title_str() == "otx_title"
    assert inx_name_str() == "inx_name"
    assert otx_name_str() == "otx_name"
    assert inx_label_str() == "inx_label"
    assert otx_label_str() == "otx_label"
    assert otx_key_str() == "otx_key"
    assert inx_rope_str() == "inx_rope"
    assert otx_rope_str() == "otx_rope"
    assert unknown_str_str() == "unknown_str"
    assert otx2inx_str() == "otx2inx"
    assert lire_name_str() == "lire_name"
    assert lire_title_str() == "lire_title"
    assert lire_label_str() == "lire_label"
    assert lire_rope_str() == "lire_rope"
    assert lire_core_str() == "lire_core"
