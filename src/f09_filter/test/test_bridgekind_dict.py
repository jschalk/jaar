from src.f00_instrument.pandas_tool import get_orderd_csv
from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
    type_GroupID_str,
)
from src.f09_filter.bridge import (
    bridgekind_shop,
    get_bridgekind_from_dict,
    get_bridgekind_from_json,
    create_otx_to_inx_dt,
    get_otx_to_inx_dt_columns,
)
from src.f09_filter.examples.filter_env import (
    env_dir_setup_cleanup,
    get_test_faces_dir,
)
from src.f09_filter.examples.example_bridges import (
    get_casa_maison_bridgeunit_set_by_otx_to_inx,
    get_casa_maison_road_otx_to_inx_dt,
)


def test_BridgeKind_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    sue_str = "Sue"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    roadnode_bridgekind = bridgekind_shop(
        x_python_type=type_RoadNode_str(),
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_face_id=sue_str,
    )
    x1_road_bridge_dict = {
        "otx_road_delimiter": roadnode_bridgekind.otx_road_delimiter,
        "inx_road_delimiter": roadnode_bridgekind.inx_road_delimiter,
        "unknown_word": roadnode_bridgekind.unknown_word,
        "explicit_label_map": roadnode_bridgekind.explicit_label_map,
        "otx_to_inx": {},
        "face_id": roadnode_bridgekind.face_id,
        "python_type": roadnode_bridgekind.python_type,
    }
    assert roadnode_bridgekind.get_dict() == x1_road_bridge_dict

    # WHEN
    roadnode_bridgekind.set_otx_to_inx(clean_otx, clean_inx)
    roadnode_bridgekind.set_explicit_label_map(casa_otx, casa_inx)
    # THEN
    x2_road_bridge_dict = {
        "otx_road_delimiter": roadnode_bridgekind.otx_road_delimiter,
        "inx_road_delimiter": roadnode_bridgekind.inx_road_delimiter,
        "unknown_word": roadnode_bridgekind.unknown_word,
        "explicit_label_map": {casa_otx: casa_inx},
        "otx_to_inx": {clean_otx: clean_inx},
        "face_id": sue_str,
        "python_type": type_RoadNode_str(),
    }
    assert roadnode_bridgekind.get_dict() == x2_road_bridge_dict


def test_BridgeKind_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(
        type_RoadNode_str(), slash_otx_road_delimiter, x_face_id=sue_str
    )
    x1_road_bridge_json = f"""{{
  "explicit_label_map": {roadnode_bridgekind.explicit_label_map},
  "face_id": "{sue_str}",
  "inx_road_delimiter": "{roadnode_bridgekind.inx_road_delimiter}",
  "otx_road_delimiter": "{roadnode_bridgekind.otx_road_delimiter}",
  "otx_to_inx": {{}},
  "python_type": "{type_RoadNode_str()}",
  "unknown_word": "{roadnode_bridgekind.unknown_word}"
}}"""
    print(f"       {x1_road_bridge_json=}")
    print(f"{roadnode_bridgekind.get_json()=}")
    assert roadnode_bridgekind.get_json() == x1_road_bridge_json

    # WHEN
    roadnode_bridgekind.set_otx_to_inx(clean_otx, clean_inx)
    roadnode_bridgekind.set_explicit_label_map(casa_otx, casa_inx)
    # THEN
    x2_road_bridge_json = f"""{{
  "explicit_label_map": {{
    "{casa_otx}": "{casa_inx}"
  }},
  "face_id": "{sue_str}",
  "inx_road_delimiter": "{roadnode_bridgekind.inx_road_delimiter}",
  "otx_road_delimiter": "{roadnode_bridgekind.otx_road_delimiter}",
  "otx_to_inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "python_type": "{type_RoadNode_str()}",
  "unknown_word": "{roadnode_bridgekind.unknown_word}"
}}"""
    print(f"       {x2_road_bridge_json=}")
    print(f"{roadnode_bridgekind.get_json()=}")
    assert roadnode_bridgekind.get_json() == x2_road_bridge_json


def test_get_bridgekind_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(
        type_RoadNode_str(), slash_otx_road_delimiter, x_face_id=sue_str
    )
    roadnode_bridgekind.set_otx_to_inx(clean_otx, clean_inx)
    roadnode_bridgekind.set_explicit_label_map(casa_otx, casa_inx)

    # WHEN
    gen_bridgekind = get_bridgekind_from_dict(roadnode_bridgekind.get_dict())

    # THEN
    assert gen_bridgekind.face_id == roadnode_bridgekind.face_id
    assert gen_bridgekind.python_type == roadnode_bridgekind.python_type
    assert gen_bridgekind == roadnode_bridgekind


def test_get_bridgekind_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(type_RoadNode_str(), slash_otx_road_delimiter)
    roadnode_bridgekind.set_otx_to_inx(clean_otx, clean_inx)

    # WHEN
    x_bridgekind = get_bridgekind_from_json(roadnode_bridgekind.get_json())

    # THEN
    assert x_bridgekind == roadnode_bridgekind


def test_get_otx_to_inx_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_otx_to_inx_dt_columns()
    assert len(get_otx_to_inx_dt_columns()) == 7
    static_list = [
        "face_id",
        "python_type",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_word",
        "inx_word",
    ]
    assert get_otx_to_inx_dt_columns() == static_list


def test_create_otx_to_inx_dt_ReturnsObj():
    # ESTABLISH
    casa_bridgeunit = get_casa_maison_bridgeunit_set_by_otx_to_inx()
    casa_bridgekind = casa_bridgeunit.get_bridgekind(type_RoadUnit_str())

    # WHEN
    casa_dataframe = create_otx_to_inx_dt(casa_bridgekind)

    # THEN
    assert list(casa_dataframe.columns) == get_otx_to_inx_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_orderd_csv(casa_dataframe)
    print(f"{casa_csv=}")
    assert casa_csv == get_orderd_csv(get_casa_maison_road_otx_to_inx_dt())
