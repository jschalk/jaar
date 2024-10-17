from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import acct_id_str, label_str, group_id_str
from src.f09_filter.bridge import (
    bridgekind_shop,
    get_bridgekind_from_dict,
    get_bridgekind_from_json,
)


def test_BridgeKind_get_dict_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    casa_src = "casa1"
    casa_dst = "casa2"
    slash_src_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    x1_label_bridge_dict = {
        "src_road_delimiter": roadnode_bridgekind.src_road_delimiter,
        "dst_road_delimiter": roadnode_bridgekind.dst_road_delimiter,
        "unknown_word": roadnode_bridgekind.unknown_word,
        "explicit_label_map": roadnode_bridgekind.explicit_label_map,
        "src_to_dst": {},
    }
    assert roadnode_bridgekind.get_dict() == x1_label_bridge_dict

    # WHEN
    roadnode_bridgekind.set_src_to_dst(clean_src, clean_dst)
    roadnode_bridgekind.set_explicit_label_map(casa_src, casa_dst)
    # THEN
    x2_label_bridge_dict = {
        "src_road_delimiter": roadnode_bridgekind.src_road_delimiter,
        "dst_road_delimiter": roadnode_bridgekind.dst_road_delimiter,
        "unknown_word": roadnode_bridgekind.unknown_word,
        "explicit_label_map": {casa_src: casa_dst},
        "src_to_dst": {clean_src: clean_dst},
    }
    assert roadnode_bridgekind.get_dict() == x2_label_bridge_dict


def test_BridgeKind_get_json_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    casa_src = "casa1"
    casa_dst = "casa2"
    slash_src_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    x1_label_bridge_json = f"""{{
  "dst_road_delimiter": "{roadnode_bridgekind.dst_road_delimiter}",
  "explicit_label_map": {roadnode_bridgekind.explicit_label_map},
  "src_road_delimiter": "{roadnode_bridgekind.src_road_delimiter}",
  "src_to_dst": {{}},
  "unknown_word": "{roadnode_bridgekind.unknown_word}"
}}"""
    print(f"       {x1_label_bridge_json=}")
    print(f"{roadnode_bridgekind.get_json()=}")
    assert roadnode_bridgekind.get_json() == x1_label_bridge_json

    # WHEN
    roadnode_bridgekind.set_src_to_dst(clean_src, clean_dst)
    roadnode_bridgekind.set_explicit_label_map(casa_src, casa_dst)
    # THEN
    x2_label_bridge_json = f"""{{
  "dst_road_delimiter": "{roadnode_bridgekind.dst_road_delimiter}",
  "explicit_label_map": {{
    "{casa_src}": "{casa_dst}"
  }},
  "src_road_delimiter": "{roadnode_bridgekind.src_road_delimiter}",
  "src_to_dst": {{
    "{clean_src}": "{clean_dst}"
  }},
  "unknown_word": "{roadnode_bridgekind.unknown_word}"
}}"""
    print(f"       {x2_label_bridge_json=}")
    print(f"{roadnode_bridgekind.get_json()=}")
    assert roadnode_bridgekind.get_json() == x2_label_bridge_json


def test_get_bridgekind_from_dict_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    casa_src = "casa1"
    casa_dst = "casa2"
    slash_src_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    roadnode_bridgekind.set_src_to_dst(clean_src, clean_dst)
    roadnode_bridgekind.set_explicit_label_map(casa_src, casa_dst)

    # WHEN
    x_bridgekind = get_bridgekind_from_dict(roadnode_bridgekind.get_dict())

    # THEN
    assert x_bridgekind == roadnode_bridgekind


def test_get_bridgekind_from_json_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    slash_src_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    roadnode_bridgekind.set_src_to_dst(clean_src, clean_dst)

    # WHEN
    x_bridgekind = get_bridgekind_from_json(roadnode_bridgekind.get_json())

    # THEN
    assert x_bridgekind == roadnode_bridgekind
