from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import acct_id_str, label_str, group_id_str
from src.f09_filter.bridge import (
    bridgeunit_shop,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
)


def test_BridgeUnit_get_dict_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    slash_src_road_delimiter = "/"
    label_bridgeunit = bridgeunit_shop(label_str(), slash_src_road_delimiter)
    x1_label_bridge_dict = {
        "atom_arg": label_bridgeunit.atom_arg,
        "src_road_delimiter": label_bridgeunit.src_road_delimiter,
        "dst_road_delimiter": label_bridgeunit.dst_road_delimiter,
        "unknown_word": label_bridgeunit.unknown_word,
        "src_to_dst": {},
    }
    assert label_bridgeunit.get_dict() == x1_label_bridge_dict

    # WHEN
    label_bridgeunit.set_src_to_dst(clean_src, clean_dst)
    # THEN
    x2_label_bridge_dict = {
        "atom_arg": label_bridgeunit.atom_arg,
        "src_road_delimiter": label_bridgeunit.src_road_delimiter,
        "dst_road_delimiter": label_bridgeunit.dst_road_delimiter,
        "unknown_word": label_bridgeunit.unknown_word,
        "src_to_dst": {clean_src: clean_dst},
    }
    assert label_bridgeunit.get_dict() == x2_label_bridge_dict


def test_BridgeUnit_get_json_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    slash_src_road_delimiter = "/"
    label_bridgeunit = bridgeunit_shop(label_str(), slash_src_road_delimiter)
    x1_label_bridge_json = f"""{{
  "atom_arg": "{label_bridgeunit.atom_arg}",
  "dst_road_delimiter": "{label_bridgeunit.dst_road_delimiter}",
  "src_road_delimiter": "{label_bridgeunit.src_road_delimiter}",
  "src_to_dst": {{}},
  "unknown_word": "{label_bridgeunit.unknown_word}"
}}"""
    print(f"       {x1_label_bridge_json=}")
    print(f"{label_bridgeunit.get_json()=}")
    assert label_bridgeunit.get_json() == x1_label_bridge_json

    # WHEN
    label_bridgeunit.set_src_to_dst(clean_src, clean_dst)
    # THEN
    x2_label_bridge_json = f"""{{
  "atom_arg": "{label_bridgeunit.atom_arg}",
  "dst_road_delimiter": "{label_bridgeunit.dst_road_delimiter}",
  "src_road_delimiter": "{label_bridgeunit.src_road_delimiter}",
  "src_to_dst": {{
    "{clean_src}": "{clean_dst}"
  }},
  "unknown_word": "{label_bridgeunit.unknown_word}"
}}"""
    print(f"       {x2_label_bridge_json=}")
    print(f"{label_bridgeunit.get_json()=}")
    assert label_bridgeunit.get_json() == x2_label_bridge_json


def test_get_bridgeunit_from_dict_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    slash_src_road_delimiter = "/"
    label_bridgeunit = bridgeunit_shop(label_str(), slash_src_road_delimiter)
    label_bridgeunit.set_src_to_dst(clean_src, clean_dst)

    # WHEN
    x_bridgeunit = get_bridgeunit_from_dict(label_bridgeunit.get_dict())

    # THEN
    assert x_bridgeunit == label_bridgeunit


def test_get_bridgeunit_from_json_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    slash_src_road_delimiter = "/"
    label_bridgeunit = bridgeunit_shop(label_str(), slash_src_road_delimiter)
    label_bridgeunit.set_src_to_dst(clean_src, clean_dst)

    # WHEN
    x_bridgeunit = get_bridgeunit_from_json(label_bridgeunit.get_json())

    # THEN
    assert x_bridgeunit == label_bridgeunit
