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
    label_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    x1_label_bridge_dict = {
        "atom_arg": label_bridgekind.atom_arg,
        "src_road_delimiter": label_bridgekind.src_road_delimiter,
        "dst_road_delimiter": label_bridgekind.dst_road_delimiter,
        "unknown_word": label_bridgekind.unknown_word,
        "explicit_label_map": label_bridgekind.explicit_label_map,
        "src_to_dst": {},
    }
    assert label_bridgekind.get_dict() == x1_label_bridge_dict

    # WHEN
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)
    label_bridgekind.set_explicit_label_map(casa_src, casa_dst)
    # THEN
    x2_label_bridge_dict = {
        "atom_arg": label_bridgekind.atom_arg,
        "src_road_delimiter": label_bridgekind.src_road_delimiter,
        "dst_road_delimiter": label_bridgekind.dst_road_delimiter,
        "unknown_word": label_bridgekind.unknown_word,
        "explicit_label_map": {casa_src: casa_dst},
        "src_to_dst": {clean_src: clean_dst},
    }
    assert label_bridgekind.get_dict() == x2_label_bridge_dict


def test_BridgeKind_get_json_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    casa_src = "casa1"
    casa_dst = "casa2"
    slash_src_road_delimiter = "/"
    label_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    x1_label_bridge_json = f"""{{
  "atom_arg": "{label_bridgekind.atom_arg}",
  "dst_road_delimiter": "{label_bridgekind.dst_road_delimiter}",
  "explicit_label_map": {label_bridgekind.explicit_label_map},
  "src_road_delimiter": "{label_bridgekind.src_road_delimiter}",
  "src_to_dst": {{}},
  "unknown_word": "{label_bridgekind.unknown_word}"
}}"""
    print(f"       {x1_label_bridge_json=}")
    print(f"{label_bridgekind.get_json()=}")
    assert label_bridgekind.get_json() == x1_label_bridge_json

    # WHEN
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)
    label_bridgekind.set_explicit_label_map(casa_src, casa_dst)
    # THEN
    x2_label_bridge_json = f"""{{
  "atom_arg": "{label_bridgekind.atom_arg}",
  "dst_road_delimiter": "{label_bridgekind.dst_road_delimiter}",
  "explicit_label_map": {{
    "{casa_src}": "{casa_dst}"
  }},
  "src_road_delimiter": "{label_bridgekind.src_road_delimiter}",
  "src_to_dst": {{
    "{clean_src}": "{clean_dst}"
  }},
  "unknown_word": "{label_bridgekind.unknown_word}"
}}"""
    print(f"       {x2_label_bridge_json=}")
    print(f"{label_bridgekind.get_json()=}")
    assert label_bridgekind.get_json() == x2_label_bridge_json


def test_get_bridgekind_from_dict_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    casa_src = "casa1"
    casa_dst = "casa2"
    slash_src_road_delimiter = "/"
    label_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)
    label_bridgekind.set_explicit_label_map(casa_src, casa_dst)

    # WHEN
    x_bridgekind = get_bridgekind_from_dict(label_bridgekind.get_dict())

    # THEN
    assert x_bridgekind == label_bridgekind


def test_get_bridgekind_from_json_ReturnsObj():
    # ESTABLISH
    clean_src = "clean"
    clean_dst = "prop"
    slash_src_road_delimiter = "/"
    label_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)

    # WHEN
    x_bridgekind = get_bridgekind_from_json(label_bridgekind.get_json())

    # THEN
    assert x_bridgekind == label_bridgekind
