from src.f08_pidgin.bridge_old import (
    bridgeunit_shop,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
)


def test_BridgeUnit_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    sue_str = "Sue"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    roadnode_bridgeunit = bridgeunit_shop(
        x_jaar_type="RoadNode",
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_face_id=sue_str,
    )
    x1_road_bridge_dict = {
        "otx_wall": roadnode_bridgeunit.otx_wall,
        "inx_wall": roadnode_bridgeunit.inx_wall,
        "unknown_word": roadnode_bridgeunit.unknown_word,
        "nub_label": roadnode_bridgeunit.nub_label,
        "otx2inx": {},
        "face_id": roadnode_bridgeunit.face_id,
        "jaar_type": roadnode_bridgeunit.jaar_type,
    }
    assert roadnode_bridgeunit.get_dict() == x1_road_bridge_dict

    # WHEN
    roadnode_bridgeunit.set_otx2inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_nub_label(casa_otx, casa_inx)
    # THEN
    x2_road_bridge_dict = {
        "otx_wall": roadnode_bridgeunit.otx_wall,
        "inx_wall": roadnode_bridgeunit.inx_wall,
        "unknown_word": roadnode_bridgeunit.unknown_word,
        "nub_label": {casa_otx: casa_inx},
        "otx2inx": {clean_otx: clean_inx},
        "face_id": sue_str,
        "jaar_type": "RoadNode",
    }
    assert roadnode_bridgeunit.get_dict() == x2_road_bridge_dict


def test_BridgeUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_wall = "/"
    roadnode_bridgeunit = bridgeunit_shop("RoadNode", slash_otx_wall, x_face_id=sue_str)
    x1_road_bridge_json = f"""{{
  "face_id": "{sue_str}",
  "inx_wall": "{roadnode_bridgeunit.inx_wall}",
  "jaar_type": "RoadNode",
  "nub_label": {roadnode_bridgeunit.nub_label},
  "otx2inx": {{}},
  "otx_wall": "{roadnode_bridgeunit.otx_wall}",
  "unknown_word": "{roadnode_bridgeunit.unknown_word}"
}}"""
    print(f"           {x1_road_bridge_json=}")
    print(f"{roadnode_bridgeunit.get_json()=}")
    assert roadnode_bridgeunit.get_json() == x1_road_bridge_json

    # WHEN
    roadnode_bridgeunit.set_otx2inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_nub_label(casa_otx, casa_inx)
    # THEN
    x2_road_bridge_json = f"""{{
  "face_id": "{sue_str}",
  "inx_wall": "{roadnode_bridgeunit.inx_wall}",
  "jaar_type": "RoadNode",
  "nub_label": {{
    "{casa_otx}": "{casa_inx}"
  }},
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_wall": "{roadnode_bridgeunit.otx_wall}",
  "unknown_word": "{roadnode_bridgeunit.unknown_word}"
}}"""
    print(f"           {x2_road_bridge_json=}")
    print(f"{roadnode_bridgeunit.get_json()=}")
    assert roadnode_bridgeunit.get_json() == x2_road_bridge_json


def test_get_bridgeunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_wall = "/"
    roadnode_bridgeunit = bridgeunit_shop("RoadNode", slash_otx_wall, x_face_id=sue_str)
    roadnode_bridgeunit.set_otx2inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_nub_label(casa_otx, casa_inx)

    # WHEN
    gen_bridgeunit = get_bridgeunit_from_dict(roadnode_bridgeunit.get_dict())

    # THEN
    assert gen_bridgeunit.face_id == roadnode_bridgeunit.face_id
    assert gen_bridgeunit.jaar_type == roadnode_bridgeunit.jaar_type
    assert gen_bridgeunit == roadnode_bridgeunit


def test_get_bridgeunit_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    roadnode_bridgeunit = bridgeunit_shop("RoadNode", slash_otx_wall)
    roadnode_bridgeunit.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_bridgeunit = get_bridgeunit_from_json(roadnode_bridgeunit.get_json())

    # THEN
    assert x_bridgeunit == roadnode_bridgeunit
