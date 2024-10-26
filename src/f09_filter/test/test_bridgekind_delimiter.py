from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_GroupID_str,
    type_RoadUnit_str,
    type_RoadNode_str,
)
from src.f09_filter.filter import bridgekind_shop


def test_BridgeKind_otx_road_delimiter_in_otx_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    otx_road_delimiter = "/"
    zia_inx = "Zia"
    zia_otx = f"Zia{otx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(None, otx_road_delimiter)
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    assert acct_id_bridgekind._otx_road_delimiter_in_otx_words() is False

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)

    # THEN
    assert acct_id_bridgekind._otx_road_delimiter_in_otx_words()


def test_BridgeKind_inx_road_delimiter_in_otx_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_road_delimiter = "/"
    zia_inx = "Zia"
    zia_otx = f"Zia{inx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(None, None, inx_road_delimiter)
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    assert acct_id_bridgekind._inx_road_delimiter_in_otx_words() is False

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)

    # THEN
    assert acct_id_bridgekind._inx_road_delimiter_in_otx_words()


def test_BridgeKind_otx_road_delimiter_in_inx_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    otx_road_delimiter = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{otx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(None, otx_road_delimiter)
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    assert acct_id_bridgekind._otx_road_delimiter_in_inx_words() is False

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)

    # THEN
    assert acct_id_bridgekind._otx_road_delimiter_in_inx_words()


def test_BridgeKind_inx_road_delimiter_in_inx_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_road_delimiter = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(None, None, inx_road_delimiter)
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    assert acct_id_bridgekind._inx_road_delimiter_in_inx_words() is False

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)

    # THEN
    assert acct_id_bridgekind._inx_road_delimiter_in_inx_words()


def test_BridgeKind_is_inx_delimiter_inclusion_correct_ReturnsObj_AcctID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_road_delimiter = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str(), None, inx_road_delimiter)
    assert acct_id_bridgekind.python_type == type_AcctID_str()
    assert acct_id_bridgekind._is_inx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    # THEN
    assert acct_id_bridgekind._is_inx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    # THEN
    assert acct_id_bridgekind._is_inx_delimiter_inclusion_correct() is False


def test_BridgeKind_is_inx_delimiter_inclusion_correct_ReturnsObj_GroupID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_road_delimiter = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(type_GroupID_str(), None, inx_road_delimiter)
    assert acct_id_bridgekind.python_type == type_GroupID_str()
    assert acct_id_bridgekind._is_inx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    # THEN
    assert acct_id_bridgekind._is_inx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    # THEN
    assert acct_id_bridgekind._is_inx_delimiter_inclusion_correct() is False


def test_BridgeKind_is_inx_delimiter_inclusion_correct_ReturnsObj_RoadUnit():
    # ESTABLISH
    music_str = "music45"
    otx_r_delimiter = "/"
    inx_r_delimiter = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{music_str}{otx_r_delimiter}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_road = f"{music_str}{inx_r_delimiter}{clean_inx_str}"

    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(), otx_r_delimiter, inx_r_delimiter
    )
    assert road_bridgekind.python_type == type_RoadUnit_str()
    assert road_bridgekind._is_inx_delimiter_inclusion_correct()

    # WHEN
    road_bridgekind.set_otx_to_inx(clean_otx_road, clean_inx_road)
    # THEN
    assert road_bridgekind._is_inx_delimiter_inclusion_correct()


def test_BridgeKind_is_otx_delimiter_inclusion_correct_ReturnsObj_AcctID():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_road_delimiter = "/"
    zia_otx = f"Zia{otx_road_delimiter}"
    zia_inx = "Zia"
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str(), otx_road_delimiter)
    assert acct_id_bridgekind.python_type == type_AcctID_str()
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(xio_otx, xio_inx)
    # THEN
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    # THEN
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct() is False


def test_BridgeKind_is_otx_delimiter_inclusion_correct_ReturnsObj_GroupID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    otx_road_delimiter = "/"
    zia_inx = "Zia"
    zia_otx = f"Zia{otx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(type_GroupID_str(), otx_road_delimiter)
    assert acct_id_bridgekind.python_type == type_GroupID_str()
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    # THEN
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    # THEN
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct() is False


def test_BridgeKind_is_otx_delimiter_inclusion_correct_ReturnsObj_RoadNode():
    # ESTABLISH
    clean_str = "clean"
    clean_inx = "propre"
    otx_road_delimiter = "/"
    casa_otx = f"casa{otx_road_delimiter}"
    casa_inx = "casa"
    acct_id_bridgekind = bridgekind_shop(type_RoadNode_str(), otx_road_delimiter)
    assert acct_id_bridgekind.python_type == type_RoadNode_str()
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(clean_str, clean_inx)
    # THEN
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(casa_otx, casa_inx)
    # THEN
    assert acct_id_bridgekind._is_otx_delimiter_inclusion_correct() is False


def test_BridgeKind_is_otx_delimiter_inclusion_correct_ReturnsObj_RoadUnit():
    # ESTABLISH
    music_str = "music45"
    otx_r_delimiter = "/"
    inx_r_delimiter = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{music_str}{otx_r_delimiter}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_road = f"{music_str}{inx_r_delimiter}{clean_inx_str}"

    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(), otx_r_delimiter, inx_r_delimiter
    )
    assert road_bridgekind.python_type == type_RoadUnit_str()
    assert road_bridgekind._is_otx_delimiter_inclusion_correct()

    # WHEN
    road_bridgekind.set_otx_to_inx(clean_otx_road, clean_inx_road)
    # THEN
    assert road_bridgekind._is_otx_delimiter_inclusion_correct()


def test_BridgeKind_all_otx_parent_roads_exist_ReturnsObjAlwaysTrue_GroupID():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    otx_road_delimiter = "/"
    zia_inx = "Zia"
    zia_otx = f"Zia{otx_road_delimiter}"
    acct_id_bridgekind = bridgekind_shop(type_GroupID_str(), otx_road_delimiter)
    assert acct_id_bridgekind.python_type == type_GroupID_str()
    assert acct_id_bridgekind.all_otx_parent_roads_exist()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    # THEN
    assert acct_id_bridgekind.all_otx_parent_roads_exist()

    # WHEN
    acct_id_bridgekind.set_otx_to_inx(xio_str, sue_str)
    # THEN
    assert acct_id_bridgekind.all_otx_parent_roads_exist()


def test_BridgeKind_all_otx_parent_roads_exist_ReturnsObj_RoadUnit():
    # ESTABLISH
    clean_otx_parent_road = "music45"
    otx_r_delimiter = "/"
    clean_otx_str = "clean"
    clean_otx_road = f"{clean_otx_parent_road}{otx_r_delimiter}{clean_otx_str}"

    road_bridgekind = bridgekind_shop(type_RoadUnit_str(), otx_r_delimiter)
    assert road_bridgekind.python_type == type_RoadUnit_str()
    assert road_bridgekind.otx_exists(clean_otx_parent_road) is False
    assert road_bridgekind.otx_exists(clean_otx_road) is False
    assert road_bridgekind.all_otx_parent_roads_exist()

    # WHEN
    road_bridgekind.set_otx_to_inx(clean_otx_road, "any")
    # THEN
    assert road_bridgekind.otx_exists(clean_otx_parent_road) is False
    assert road_bridgekind.otx_exists(clean_otx_road)
    assert road_bridgekind.all_otx_parent_roads_exist() is False

    # WHEN
    road_bridgekind.set_otx_to_inx(clean_otx_parent_road, "any")
    # THEN
    assert road_bridgekind.otx_exists(clean_otx_parent_road)
    assert road_bridgekind.otx_exists(clean_otx_road)
    assert road_bridgekind.all_otx_parent_roads_exist()


def test_BridgeKind_is_valid_ReturnsObj_Scenario0_label_str():
    # ESTABLISH
    clean_str = "clean"
    clean_inx = "propre"
    otx_road_delimiter = "/"
    casa_otx = f"casa{otx_road_delimiter}"
    casa_inx = "casa"
    roadnode_bridgekind = bridgekind_shop(type_RoadNode_str(), otx_road_delimiter)
    assert roadnode_bridgekind.python_type == type_RoadNode_str()
    assert roadnode_bridgekind.is_valid()

    # WHEN
    roadnode_bridgekind.set_otx_to_inx(clean_str, clean_inx)
    # THEN
    assert roadnode_bridgekind.is_valid()

    # WHEN
    roadnode_bridgekind.set_otx_to_inx(casa_otx, casa_inx)
    # THEN
    assert roadnode_bridgekind.is_valid() is False


def test_BridgeKind_is_valid_ReturnsObj_Scenario1_road_str():
    # ESTABLISH
    music_str = "music45"
    otx_r_delimiter = "/"
    inx_r_delimiter = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{music_str}{otx_r_delimiter}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_road = f"{music_str}{inx_r_delimiter}{clean_inx_str}"
    # casa_otx = f"casa{otx_road_delimiter}"
    # casa_inx = f"casa"
    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(), otx_r_delimiter, inx_r_delimiter
    )
    road_bridgekind.set_otx_to_inx(music_str, music_str)
    assert road_bridgekind.python_type == type_RoadUnit_str()
    assert road_bridgekind.is_valid()
    assert road_bridgekind.otx_to_inx_exists(clean_otx_road, clean_inx_road) is False

    # WHEN
    road_bridgekind.set_otx_to_inx(clean_otx_road, clean_inx_road)
    # THEN
    assert road_bridgekind.is_valid()
    assert road_bridgekind.otx_to_inx_exists(clean_otx_road, clean_inx_road)


def test_BridgeKind_is_valid_ReturnsObj_Scenario2_group_id_str():
    # ESTABLISH
    otx_road_delimiter = ":"
    inx_road_delimiter = "/"
    sue_otx = f"Xio{otx_road_delimiter}"
    sue_inx = f"Sue{inx_road_delimiter}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_road_delimiter}"
    group_id_bridgekind = bridgekind_shop(
        type_GroupID_str(), otx_road_delimiter, inx_road_delimiter
    )
    assert group_id_bridgekind.python_type == type_GroupID_str()
    assert group_id_bridgekind.is_valid()

    # WHEN
    group_id_bridgekind.set_otx_to_inx(sue_otx, sue_inx)
    # THEN
    assert group_id_bridgekind.is_valid()

    # WHEN
    group_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    # THEN
    assert group_id_bridgekind.is_valid() is False


def test_BridgeKind_is_valid_ReturnsObj_Scenario3_RoadUnit():
    # ESTABLISH
    clean_otx_parent_road = "music45"
    otx_r_delimiter = "/"
    clean_otx_str = "clean"
    clean_otx_road = f"{clean_otx_parent_road}{otx_r_delimiter}{clean_otx_str}"

    road_bridgekind = bridgekind_shop(type_RoadUnit_str(), otx_r_delimiter)
    assert road_bridgekind.python_type == type_RoadUnit_str()
    assert road_bridgekind.otx_exists(clean_otx_parent_road) is False
    assert road_bridgekind.otx_exists(clean_otx_road) is False
    assert road_bridgekind.all_otx_parent_roads_exist()
    assert road_bridgekind.is_valid()

    # WHEN
    road_bridgekind.set_otx_to_inx(clean_otx_road, "any")
    # THEN
    assert road_bridgekind.otx_exists(clean_otx_parent_road) is False
    assert road_bridgekind.otx_exists(clean_otx_road)
    assert road_bridgekind.all_otx_parent_roads_exist() is False
    assert road_bridgekind.is_valid() is False

    # WHEN
    road_bridgekind.set_otx_to_inx(clean_otx_parent_road, "any")
    # THEN
    assert road_bridgekind.otx_exists(clean_otx_parent_road)
    assert road_bridgekind.otx_exists(clean_otx_road)
    assert road_bridgekind.all_otx_parent_roads_exist()
    assert road_bridgekind.is_valid()
