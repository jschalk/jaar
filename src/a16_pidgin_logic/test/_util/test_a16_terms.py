from src.a16_pidgin_logic.test._util.a16_terms import (
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    otx2inx_str,
    otx_key_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    pidgin_core_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_rope_str,
    pidgin_title_str,
    pidginunit_str,
    unknown_str_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert pidginunit_str() == "pidginunit"
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
    assert pidgin_name_str() == "pidgin_name"
    assert pidgin_title_str() == "pidgin_title"
    assert pidgin_label_str() == "pidgin_label"
    assert pidgin_rope_str() == "pidgin_rope"
    assert pidgin_core_str() == "pidgin_core"
