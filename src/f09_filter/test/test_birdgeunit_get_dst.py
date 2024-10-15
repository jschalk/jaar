from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import acct_id_str, label_str, group_id_str
from src.f09_filter.filter import (
    bridgeunit_shop,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
)


def test_BridgeUnit_get_dst_ReturnsObjAndSetsAttr():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    src_r_delimiter = "/"
    casa_src = "casa"
    casa_dst = "casa"
    dst_r_delimiter = ":"
    label_bridgeunit = bridgeunit_shop(label_str(), src_r_delimiter, dst_r_delimiter)
    label_bridgeunit.set_src_to_dst(clean_src, clean_dst)
    label_bridgeunit.set_src_to_dst(casa_src, casa_dst)
    assert label_bridgeunit.is_valid()

    # WHEN / THEN
    assert label_bridgeunit.get_dst(clean_src) == clean_dst
    assert label_bridgeunit.get_dst(casa_src) == casa_dst
    swim_str = "swim"
    assert label_bridgeunit.get_dst(swim_str, False) is None
    assert label_bridgeunit.src_exists(swim_str) is False

    # WHEN
    assert label_bridgeunit.get_dst(swim_str) == swim_str
    # THEN
    assert label_bridgeunit.src_exists(swim_str)

    # WHEN / THEN
    fail_clean_src = f"clean{dst_r_delimiter}"
    assert label_bridgeunit.src_exists(fail_clean_src) is False
    assert label_bridgeunit.get_dst(fail_clean_src) is None
    assert label_bridgeunit.src_exists(fail_clean_src) is False


def test_BridgeUnit_get_dst_AddsMissingElementsTo_src_to_dst():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    src_r_delimiter = "/"
    casa_src = "casa"
    casa_dst = "casa"
    dst_r_delimiter = ":"
    label_bridgeunit = bridgeunit_shop(label_str(), src_r_delimiter, dst_r_delimiter)
    label_bridgeunit.set_src_to_dst(clean_src, clean_dst)
    label_bridgeunit.set_src_to_dst(casa_src, casa_dst)
    swim_str = "swim"
    assert label_bridgeunit.src_exists(swim_str) is False

    # WHEN
    assert label_bridgeunit.get_dst(swim_str, True) == swim_str

    # THEN
    assert label_bridgeunit.src_exists(swim_str)
    assert label_bridgeunit.src_to_dst_exists(swim_str, swim_str)
