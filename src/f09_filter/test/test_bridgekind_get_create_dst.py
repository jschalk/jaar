from src.f04_gift.atom_config import (
    type_RoadNode_str,
    type_RoadUnit_str,
    type_GroupID_str,
)
from src.f09_filter.bridge import bridgekind_shop


def test_BridgeKind_get_create_dst_ReturnsObjAndSetsAttr_label():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    src_r_delimiter = "/"
    casa_src = "casa"
    casa_dst = "casa"
    dst_r_delimiter = ":"
    label_bridgekind = bridgekind_shop(
        type_RoadNode_str(), src_r_delimiter, dst_r_delimiter
    )
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)
    label_bridgekind.set_src_to_dst(casa_src, casa_dst)
    assert label_bridgekind.is_valid()

    # WHEN / THEN
    assert label_bridgekind.get_create_dst(clean_src) == clean_dst
    assert label_bridgekind.get_create_dst(casa_src) == casa_dst
    swim_str = "swim"
    assert label_bridgekind.get_create_dst(swim_str, False) is None
    assert label_bridgekind.src_exists(swim_str) is False

    # WHEN
    assert label_bridgekind.get_create_dst(swim_str) == swim_str
    # THEN
    assert label_bridgekind.src_exists(swim_str)

    # WHEN / THEN
    fail_clean_src = f"clean{dst_r_delimiter}"
    assert label_bridgekind.src_exists(fail_clean_src) is False
    assert label_bridgekind.get_create_dst(fail_clean_src) is None
    assert label_bridgekind.src_exists(fail_clean_src) is False


def test_BridgeKind_get_create_dst_ReturnsObjAndSetsAttr_label_With_explicit_label_map():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    src_r_delimiter = "/"
    casa_src = "casa"
    casa_dst = "house"
    dst_r_delimiter = ":"
    label_bridgekind = bridgekind_shop(
        type_RoadNode_str(), src_r_delimiter, dst_r_delimiter
    )
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)
    label_bridgekind.set_explicit_label_map(casa_src, casa_dst)
    assert casa_src != casa_dst
    assert label_bridgekind.explicit_label_map_exists(casa_src, casa_dst)
    assert label_bridgekind.src_to_dst_exists(casa_src, casa_dst) is False

    # WHEN
    generated_dst = label_bridgekind.get_create_dst(casa_src)

    # THEN
    assert generated_dst == casa_dst
    assert label_bridgekind.explicit_label_map_exists(casa_src, casa_dst)
    assert label_bridgekind.src_to_dst_exists(casa_src, casa_dst)
    print(f"{casa_dst=}")


def test_BridgeKind_get_create_dst_ReturnsObjAndSetsAttr_road_Scenario0():
    # ESTABLISH
    src_music45_str = "music45"
    src_r_delimiter = "/"
    dst_r_delimiter = ":"
    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(), src_r_delimiter, dst_r_delimiter
    )
    assert road_bridgekind.src_exists(src_music45_str) is False
    assert road_bridgekind.src_to_dst_exists(src_music45_str, src_music45_str) is False

    # WHEN
    gen_dst_road = road_bridgekind.get_create_dst(src_music45_str)

    # THEN
    assert gen_dst_road == src_music45_str
    assert road_bridgekind.src_exists(src_music45_str)
    assert road_bridgekind.src_to_dst_exists(src_music45_str, src_music45_str)


def test_BridgeKind_get_create_dst_ReturnsObjAndSetsAttr_road_Scenario1():
    # ESTABLISH
    src_music45_str = "music45"
    dst_music87_str = "music87"
    src_r_delimiter = "/"
    dst_r_delimiter = ":"
    clean_src_str = "clean"
    clean_src_road = f"{src_music45_str}{src_r_delimiter}{clean_src_str}"
    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(), src_r_delimiter, dst_r_delimiter
    )
    assert road_bridgekind.src_exists(src_music45_str) is False
    assert road_bridgekind.src_exists(clean_src_road) is False

    # WHEN
    gen_dst_road = road_bridgekind.get_create_dst(clean_src_road)

    # THEN
    assert gen_dst_road is None
    assert road_bridgekind.src_exists(src_music45_str) is False
    assert road_bridgekind.src_exists(clean_src_road) is False
    assert road_bridgekind.src_to_dst_exists(src_music45_str, dst_music87_str) is False

    # ESTABLISH
    road_bridgekind.set_src_to_dst(src_music45_str, dst_music87_str)
    assert road_bridgekind.src_to_dst_exists(src_music45_str, dst_music87_str)
    assert road_bridgekind.src_exists(clean_src_road) is False

    # WHEN
    gen_dst_road = road_bridgekind.get_create_dst(clean_src_road)

    # THEN
    assert road_bridgekind.src_exists(clean_src_road)
    assert road_bridgekind.src_to_dst_exists(clean_src_road, gen_dst_road)
    assert gen_dst_road == f"{dst_music87_str}{dst_r_delimiter}{clean_src_str}"


def test_BridgeKind_get_create_dst_ReturnsObjAndSetsAttr_road_Scenario2_With_explicit_label_map():
    # ESTABLISH
    src_music45_str = "music45"
    dst_music87_str = "music87"
    src_r_delimiter = "/"
    dst_r_delimiter = ":"
    clean_src_str = "clean"
    clean_dst_str = "prop"
    clean_src_road = f"{src_music45_str}{src_r_delimiter}{clean_src_str}"
    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(), src_r_delimiter, dst_r_delimiter
    )
    road_bridgekind.set_explicit_label_map(clean_src_str, clean_dst_str)
    assert road_bridgekind.src_exists(src_music45_str) is False
    assert road_bridgekind.src_exists(clean_src_road) is False

    # WHEN
    gen_dst_road = road_bridgekind.get_create_dst(clean_src_road)

    # THEN
    assert gen_dst_road is None
    assert road_bridgekind.src_exists(src_music45_str) is False
    assert road_bridgekind.src_exists(clean_src_road) is False
    assert road_bridgekind.src_to_dst_exists(src_music45_str, dst_music87_str) is False

    # ESTABLISH
    road_bridgekind.set_src_to_dst(src_music45_str, dst_music87_str)
    assert road_bridgekind.src_to_dst_exists(src_music45_str, dst_music87_str)
    assert road_bridgekind.src_exists(clean_src_road) is False

    # WHEN
    gen_dst_road = road_bridgekind.get_create_dst(clean_src_road)

    # THEN
    assert road_bridgekind.src_to_dst_exists(src_music45_str, dst_music87_str)
    assert road_bridgekind.src_exists(clean_src_road)
    assert road_bridgekind.src_to_dst_exists(clean_src_road, gen_dst_road)
    assert gen_dst_road == f"{dst_music87_str}{dst_r_delimiter}{clean_dst_str}"


def test_BridgeKind_get_create_dst_ReturnsObjAndSetsAttr_group_id():
    # ESTABLISH
    dst_r_delimiter = ":"
    src_r_delimiter = "/"
    swim_src = f"swim{src_r_delimiter}"
    climb_src = f"climb{src_r_delimiter}_{dst_r_delimiter}"
    group_id_bridgekind = bridgekind_shop(
        type_GroupID_str(), src_r_delimiter, dst_r_delimiter
    )
    group_id_bridgekind.src_exists(swim_src) is False
    group_id_bridgekind.src_exists(climb_src) is False

    # WHEN
    swim_dst = f"swim{dst_r_delimiter}"
    assert group_id_bridgekind.get_create_dst(swim_src) == swim_dst

    # THEN
    assert group_id_bridgekind.src_exists(swim_src)
    assert group_id_bridgekind.src_exists(climb_src) is False
    assert group_id_bridgekind._get_dst_value(swim_src) == swim_dst

    # WHEN
    assert group_id_bridgekind.get_create_dst(climb_src) is None
    # THEN
    assert group_id_bridgekind.src_exists(swim_src)
    assert group_id_bridgekind.src_exists(climb_src) is False


def test_BridgeKind_get_create_dst_AddsMissingElementsTo_src_to_dst():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    src_r_delimiter = "/"
    casa_src = "casa"
    casa_dst = "casa"
    dst_r_delimiter = ":"
    label_bridgekind = bridgekind_shop(
        type_RoadNode_str(), src_r_delimiter, dst_r_delimiter
    )
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)
    label_bridgekind.set_src_to_dst(casa_src, casa_dst)
    swim_str = "swim"
    assert label_bridgekind.src_exists(swim_str) is False

    # WHEN
    assert label_bridgekind.get_create_dst(swim_str, True) == swim_str

    # THEN
    assert label_bridgekind.src_exists(swim_str)
    assert label_bridgekind.src_to_dst_exists(swim_str, swim_str)
