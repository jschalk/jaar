from src.a16_pidgin_logic._test_util.a16_str import (
    pidginunit_str,
    otx_bridge_str,
    inx_bridge_str,
    inx_title_str,
    otx_title_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    otx_key_str,
    inx_way_str,
    otx_way_str,
    unknown_term_str,
    otx2inx_str,
    map_otx2inx_str,
    pidgin_name_str,
    pidgin_title_str,
    pidgin_label_str,
    pidgin_way_str,
    pidgin_core_str,
)


def test_str_functions_ReturnsObj():
    assert pidginunit_str() == "pidginunit"
    assert otx_bridge_str() == "otx_bridge"
    assert inx_bridge_str() == "inx_bridge"
    assert inx_title_str() == "inx_title"
    assert otx_title_str() == "otx_title"
    assert inx_name_str() == "inx_name"
    assert otx_name_str() == "otx_name"
    assert inx_label_str() == "inx_label"
    assert otx_label_str() == "otx_label"
    assert otx_key_str() == "otx_key"
    assert inx_way_str() == "inx_way"
    assert otx_way_str() == "otx_way"
    assert unknown_term_str() == "unknown_term"
    assert otx2inx_str() == "otx2inx"
    assert pidgin_name_str() == "pidgin_name"
    assert pidgin_title_str() == "pidgin_title"
    assert pidgin_label_str() == "pidgin_label"
    assert pidgin_way_str() == "pidgin_way"
    assert pidgin_core_str() == "pidgin_core"
    assert map_otx2inx_str() == "map_otx2inx"
