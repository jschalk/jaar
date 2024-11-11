from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
    type_GroupID_str,
    face_id_str,
)
from src.f08_pidgin.pidgin import (
    bridgeunit_shop,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
)
from src.f08_pidgin.examples.pidgin_env import (
    env_dir_setup_cleanup,
    get_test_faces_dir,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_casa_maison_pidginunit_set_by_otx_to_inx,
    get_casa_maison_pidginunit_set_by_explicit_label,
    get_casa_maison_road_otx_to_inx_dt,
    get_casa_maison_road_explicit_label_dt,
)


def test_BridgeUnit_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    sue_str = "Sue"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    roadnode_bridgeunit = bridgeunit_shop(
        x_obj_class=type_RoadNode_str(),
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_face_id=sue_str,
    )
    x1_road_bridge_dict = {
        "otx_road_delimiter": roadnode_bridgeunit.otx_road_delimiter,
        "inx_road_delimiter": roadnode_bridgeunit.inx_road_delimiter,
        "unknown_word": roadnode_bridgeunit.unknown_word,
        "explicit_label": roadnode_bridgeunit.explicit_label,
        "otx_to_inx": {},
        face_id_str(): roadnode_bridgeunit.face_id,
        "obj_class": roadnode_bridgeunit.obj_class,
    }
    assert roadnode_bridgeunit.get_dict() == x1_road_bridge_dict

    # WHEN
    roadnode_bridgeunit.set_otx_to_inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_explicit_label(casa_otx, casa_inx)
    # THEN
    x2_road_bridge_dict = {
        "otx_road_delimiter": roadnode_bridgeunit.otx_road_delimiter,
        "inx_road_delimiter": roadnode_bridgeunit.inx_road_delimiter,
        "unknown_word": roadnode_bridgeunit.unknown_word,
        "explicit_label": {casa_otx: casa_inx},
        "otx_to_inx": {clean_otx: clean_inx},
        face_id_str(): sue_str,
        "obj_class": type_RoadNode_str(),
    }
    assert roadnode_bridgeunit.get_dict() == x2_road_bridge_dict


def test_BridgeUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_road_delimiter = "/"
    roadnode_bridgeunit = bridgeunit_shop(
        type_RoadNode_str(), slash_otx_road_delimiter, x_face_id=sue_str
    )
    x1_road_bridge_json = f"""{{
  "explicit_label": {roadnode_bridgeunit.explicit_label},
  "{face_id_str()}": "{sue_str}",
  "inx_road_delimiter": "{roadnode_bridgeunit.inx_road_delimiter}",
  "obj_class": "{type_RoadNode_str()}",
  "otx_road_delimiter": "{roadnode_bridgeunit.otx_road_delimiter}",
  "otx_to_inx": {{}},
  "unknown_word": "{roadnode_bridgeunit.unknown_word}"
}}"""
    print(f"       {x1_road_bridge_json=}")
    print(f"{roadnode_bridgeunit.get_json()=}")
    assert roadnode_bridgeunit.get_json() == x1_road_bridge_json

    # WHEN
    roadnode_bridgeunit.set_otx_to_inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_explicit_label(casa_otx, casa_inx)
    # THEN
    x2_road_bridge_json = f"""{{
  "explicit_label": {{
    "{casa_otx}": "{casa_inx}"
  }},
  "{face_id_str()}": "{sue_str}",
  "inx_road_delimiter": "{roadnode_bridgeunit.inx_road_delimiter}",
  "obj_class": "{type_RoadNode_str()}",
  "otx_road_delimiter": "{roadnode_bridgeunit.otx_road_delimiter}",
  "otx_to_inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "unknown_word": "{roadnode_bridgeunit.unknown_word}"
}}"""
    print(f"       {x2_road_bridge_json=}")
    print(f"{roadnode_bridgeunit.get_json()=}")
    assert roadnode_bridgeunit.get_json() == x2_road_bridge_json


def test_get_bridgeunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_road_delimiter = "/"
    roadnode_bridgeunit = bridgeunit_shop(
        type_RoadNode_str(), slash_otx_road_delimiter, x_face_id=sue_str
    )
    roadnode_bridgeunit.set_otx_to_inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_explicit_label(casa_otx, casa_inx)

    # WHEN
    gen_bridgeunit = get_bridgeunit_from_dict(roadnode_bridgeunit.get_dict())

    # THEN
    assert gen_bridgeunit.face_id == roadnode_bridgeunit.face_id
    assert gen_bridgeunit.obj_class == roadnode_bridgeunit.obj_class
    assert gen_bridgeunit == roadnode_bridgeunit


def test_get_bridgeunit_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_road_delimiter = "/"
    roadnode_bridgeunit = bridgeunit_shop(type_RoadNode_str(), slash_otx_road_delimiter)
    roadnode_bridgeunit.set_otx_to_inx(clean_otx, clean_inx)

    # WHEN
    x_bridgeunit = get_bridgeunit_from_json(roadnode_bridgeunit.get_json())

    # THEN
    assert x_bridgeunit == roadnode_bridgeunit
