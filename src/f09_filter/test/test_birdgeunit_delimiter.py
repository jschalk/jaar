from src.f04_gift.atom_config import (
    acct_id_str,
    label_str,
    road_str,
    group_id_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadUnit_str,
    type_RoadNode_str,
)
from src.f09_filter.bridge import bridgeunit_shop


def test_BridgeUnit_src_road_delimiter_in_src_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    src_road_delimiter = "/"
    zia_dst = "Zia"
    zia_src = f"Zia{src_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, acct_id_str(), src_road_delimiter)
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    assert acct_id_bridgeunit._src_road_delimiter_in_src_words() is False

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)

    # THEN
    assert acct_id_bridgeunit._src_road_delimiter_in_src_words()


def test_BridgeUnit_dst_road_delimiter_in_src_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    dst_road_delimiter = "/"
    zia_dst = "Zia"
    zia_src = f"Zia{dst_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, acct_id_str(), None, dst_road_delimiter)
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    assert acct_id_bridgeunit._dst_road_delimiter_in_src_words() is False

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)

    # THEN
    assert acct_id_bridgeunit._dst_road_delimiter_in_src_words()


def test_BridgeUnit_src_road_delimiter_in_dst_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    src_road_delimiter = "/"
    zia_src = "Zia"
    zia_dst = f"Zia{src_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, acct_id_str(), src_road_delimiter)
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    assert acct_id_bridgeunit._src_road_delimiter_in_dst_words() is False

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)

    # THEN
    assert acct_id_bridgeunit._src_road_delimiter_in_dst_words()


def test_BridgeUnit_dst_road_delimiter_in_dst_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    dst_road_delimiter = "/"
    zia_src = "Zia"
    zia_dst = f"Zia{dst_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, acct_id_str(), None, dst_road_delimiter)
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    assert acct_id_bridgeunit._dst_road_delimiter_in_dst_words() is False

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)

    # THEN
    assert acct_id_bridgeunit._dst_road_delimiter_in_dst_words()


def test_BridgeUnit_is_dst_delimiter_inclusion_correct_ReturnsObj_AcctID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    dst_road_delimiter = "/"
    zia_src = "Zia"
    zia_dst = f"Zia{dst_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, acct_id_str(), None, dst_road_delimiter)
    assert acct_id_bridgeunit.python_type == type_AcctID_str()
    assert acct_id_bridgeunit._is_dst_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    # THEN
    assert acct_id_bridgeunit._is_dst_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)
    # THEN
    assert acct_id_bridgeunit._is_dst_delimiter_inclusion_correct() is False


def test_BridgeUnit_is_dst_delimiter_inclusion_correct_ReturnsObj_GroupID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    dst_road_delimiter = "/"
    zia_src = "Zia"
    zia_dst = f"Zia{dst_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, group_id_str(), None, dst_road_delimiter)
    assert acct_id_bridgeunit.python_type == type_GroupID_str()
    assert acct_id_bridgeunit._is_dst_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)
    # THEN
    assert acct_id_bridgeunit._is_dst_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    # THEN
    assert acct_id_bridgeunit._is_dst_delimiter_inclusion_correct() is False


def test_BridgeUnit_is_dst_delimiter_inclusion_correct_ReturnsObj_RoadUnit():
    # ESTABLISH
    music_str = "music45"
    src_r_delimiter = "/"
    dst_r_delimiter = ":"
    clean_src_str = "clean"
    clean_src_road = f"{music_str}{src_r_delimiter}{clean_src_str}"
    clean_dst_str = "prop"
    clean_dst_road = f"{music_str}{dst_r_delimiter}{clean_dst_str}"

    road_bridgeunit = bridgeunit_shop(
        None, road_str(), src_r_delimiter, dst_r_delimiter
    )
    assert road_bridgeunit.python_type == type_RoadUnit_str()
    assert road_bridgeunit._is_dst_delimiter_inclusion_correct()

    # WHEN
    road_bridgeunit.set_src_to_dst(clean_src_road, clean_dst_road)
    # THEN
    assert road_bridgeunit._is_dst_delimiter_inclusion_correct()


def test_BridgeUnit_is_src_delimiter_inclusion_correct_ReturnsObj_AcctID():
    # ESTABLISH
    xio_src = "Xio"
    xio_dst = "XioXio"
    src_road_delimiter = "/"
    zia_src = f"Zia{src_road_delimiter}"
    zia_dst = "Zia"
    acct_id_bridgeunit = bridgeunit_shop(None, acct_id_str(), src_road_delimiter)
    assert acct_id_bridgeunit.python_type == type_AcctID_str()
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(xio_src, xio_dst)
    # THEN
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)
    # THEN
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct() is False


def test_BridgeUnit_is_src_delimiter_inclusion_correct_ReturnsObj_GroupID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    src_road_delimiter = "/"
    zia_dst = "Zia"
    zia_src = f"Zia{src_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, group_id_str(), src_road_delimiter)
    assert acct_id_bridgeunit.python_type == type_GroupID_str()
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)
    # THEN
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    # THEN
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct() is False


def test_BridgeUnit_is_src_delimiter_inclusion_correct_ReturnsObj_RoadNode():
    # ESTABLISH
    clean_str = "clean"
    clean_dst = "prop"
    src_road_delimiter = "/"
    casa_src = f"casa{src_road_delimiter}"
    casa_dst = "casa"
    acct_id_bridgeunit = bridgeunit_shop(None, label_str(), src_road_delimiter)
    assert acct_id_bridgeunit.python_type == type_RoadNode_str()
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(clean_str, clean_dst)
    # THEN
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(casa_src, casa_dst)
    # THEN
    assert acct_id_bridgeunit._is_src_delimiter_inclusion_correct() is False


def test_BridgeUnit_is_src_delimiter_inclusion_correct_ReturnsObj_RoadUnit():
    # ESTABLISH
    music_str = "music45"
    src_r_delimiter = "/"
    dst_r_delimiter = ":"
    clean_src_str = "clean"
    clean_src_road = f"{music_str}{src_r_delimiter}{clean_src_str}"
    clean_dst_str = "prop"
    clean_dst_road = f"{music_str}{dst_r_delimiter}{clean_dst_str}"

    road_bridgeunit = bridgeunit_shop(
        None, road_str(), src_r_delimiter, dst_r_delimiter
    )
    assert road_bridgeunit.python_type == type_RoadUnit_str()
    assert road_bridgeunit._is_src_delimiter_inclusion_correct()

    # WHEN
    road_bridgeunit.set_src_to_dst(clean_src_road, clean_dst_road)
    # THEN
    assert road_bridgeunit._is_src_delimiter_inclusion_correct()


def test_BridgeUnit_all_src_parent_roads_exist_ReturnsObjAlwaysTrue_GroupID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    src_road_delimiter = "/"
    zia_dst = "Zia"
    zia_src = f"Zia{src_road_delimiter}"
    acct_id_bridgeunit = bridgeunit_shop(None, group_id_str(), src_road_delimiter)
    assert acct_id_bridgeunit.python_type == type_GroupID_str()
    assert acct_id_bridgeunit.all_src_parent_roads_exist()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)
    # THEN
    assert acct_id_bridgeunit.all_src_parent_roads_exist()

    # WHEN
    acct_id_bridgeunit.set_src_to_dst(xio_str, sue_str)
    # THEN
    assert acct_id_bridgeunit.all_src_parent_roads_exist()


def test_BridgeUnit_all_src_parent_roads_exist_ReturnsObj_RoadUnit():
    # ESTABLISH
    clean_src_parent_road = "music45"
    src_r_delimiter = "/"
    clean_src_str = "clean"
    clean_src_road = f"{clean_src_parent_road}{src_r_delimiter}{clean_src_str}"

    road_bridgeunit = bridgeunit_shop(None, road_str(), src_r_delimiter)
    assert road_bridgeunit.python_type == type_RoadUnit_str()
    assert road_bridgeunit.src_exists(clean_src_parent_road) is False
    assert road_bridgeunit.src_exists(clean_src_road) is False
    assert road_bridgeunit.all_src_parent_roads_exist()

    # WHEN
    road_bridgeunit.set_src_to_dst(clean_src_road, "any")
    # THEN
    assert road_bridgeunit.src_exists(clean_src_parent_road) is False
    assert road_bridgeunit.src_exists(clean_src_road)
    assert road_bridgeunit.all_src_parent_roads_exist() is False

    # WHEN
    road_bridgeunit.set_src_to_dst(clean_src_parent_road, "any")
    # THEN
    assert road_bridgeunit.src_exists(clean_src_parent_road)
    assert road_bridgeunit.src_exists(clean_src_road)
    assert road_bridgeunit.all_src_parent_roads_exist()


def test_BridgeUnit_is_valid_ReturnsObj_Scenario0_label_str():
    # ESTABLISH
    clean_str = "clean"
    clean_dst = "prop"
    src_road_delimiter = "/"
    casa_src = f"casa{src_road_delimiter}"
    casa_dst = "casa"
    label_bridgeunit = bridgeunit_shop(None, label_str(), src_road_delimiter)
    assert label_bridgeunit.python_type == type_RoadNode_str()
    assert label_bridgeunit.is_valid()

    # WHEN
    label_bridgeunit.set_src_to_dst(clean_str, clean_dst)
    # THEN
    assert label_bridgeunit.is_valid()

    # WHEN
    label_bridgeunit.set_src_to_dst(casa_src, casa_dst)
    # THEN
    assert label_bridgeunit.is_valid() is False


def test_BridgeUnit_is_valid_ReturnsObj_Scenario1_road_str():
    # ESTABLISH
    music_str = "music45"
    src_r_delimiter = "/"
    dst_r_delimiter = ":"
    clean_src_str = "clean"
    clean_src_road = f"{music_str}{src_r_delimiter}{clean_src_str}"
    clean_dst_str = "prop"
    clean_dst_road = f"{music_str}{dst_r_delimiter}{clean_dst_str}"
    # casa_src = f"casa{src_road_delimiter}"
    # casa_dst = f"casa"
    road_bridgeunit = bridgeunit_shop(
        None, road_str(), src_r_delimiter, dst_r_delimiter
    )
    road_bridgeunit.set_src_to_dst(music_str, music_str)
    assert road_bridgeunit.python_type == type_RoadUnit_str()
    assert road_bridgeunit.is_valid()
    assert road_bridgeunit.src_to_dst_exists(clean_src_road, clean_dst_road) is False

    # WHEN
    road_bridgeunit.set_src_to_dst(clean_src_road, clean_dst_road)
    # THEN
    assert road_bridgeunit.is_valid()
    assert road_bridgeunit.src_to_dst_exists(clean_src_road, clean_dst_road)


def test_BridgeUnit_is_valid_ReturnsObj_Scenario2_group_id_str():
    # ESTABLISH
    src_road_delimiter = ":"
    dst_road_delimiter = "/"
    sue_src = f"Xio{src_road_delimiter}"
    sue_dst = f"Sue{dst_road_delimiter}"
    zia_src = "Zia"
    zia_dst = f"Zia{dst_road_delimiter}"
    group_id_bridgeunit = bridgeunit_shop(
        None, group_id_str(), src_road_delimiter, dst_road_delimiter
    )
    assert group_id_bridgeunit.python_type == type_GroupID_str()
    assert group_id_bridgeunit.is_valid()

    # WHEN
    group_id_bridgeunit.set_src_to_dst(sue_src, sue_dst)
    # THEN
    assert group_id_bridgeunit.is_valid()

    # WHEN
    group_id_bridgeunit.set_src_to_dst(zia_src, zia_dst)
    # THEN
    assert group_id_bridgeunit.is_valid() is False


def test_BridgeUnit_is_valid_ReturnsObj_Scenario3_RoadUnit():
    # ESTABLISH
    clean_src_parent_road = "music45"
    src_r_delimiter = "/"
    clean_src_str = "clean"
    clean_src_road = f"{clean_src_parent_road}{src_r_delimiter}{clean_src_str}"

    road_bridgeunit = bridgeunit_shop(None, road_str(), src_r_delimiter)
    assert road_bridgeunit.python_type == type_RoadUnit_str()
    assert road_bridgeunit.src_exists(clean_src_parent_road) is False
    assert road_bridgeunit.src_exists(clean_src_road) is False
    assert road_bridgeunit.all_src_parent_roads_exist()
    assert road_bridgeunit.is_valid()

    # WHEN
    road_bridgeunit.set_src_to_dst(clean_src_road, "any")
    # THEN
    assert road_bridgeunit.src_exists(clean_src_parent_road) is False
    assert road_bridgeunit.src_exists(clean_src_road)
    assert road_bridgeunit.all_src_parent_roads_exist() is False
    assert road_bridgeunit.is_valid() is False

    # WHEN
    road_bridgeunit.set_src_to_dst(clean_src_parent_road, "any")
    # THEN
    assert road_bridgeunit.src_exists(clean_src_parent_road)
    assert road_bridgeunit.src_exists(clean_src_road)
    assert road_bridgeunit.all_src_parent_roads_exist()
    assert road_bridgeunit.is_valid()
