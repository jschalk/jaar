from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
    type_GroupID_str,
)
from src.f08_brick.pandas_tool import (
    get_ordered_csv,
    get_sorting_priority_column_headers as sorting_columns,
)
from src.f09_filter.filter import (
    bridgeunit_shop,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
    get_otx_to_inx_dt_columns,
    get_explicit_label_columns,
    create_otx_to_inx_dt,
    create_explicit_label_dt,
)
from src.f09_filter.examples.filter_env import (
    env_dir_setup_cleanup,
    get_test_faces_dir,
)
from src.f09_filter.examples.example_filters import (
    get_casa_maison_filterunit_set_by_otx_to_inx,
    get_casa_maison_filterunit_set_by_explicit_label,
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
        x_python_type=type_RoadNode_str(),
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
        "face_id": roadnode_bridgeunit.face_id,
        "python_type": roadnode_bridgeunit.python_type,
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
        "face_id": sue_str,
        "python_type": type_RoadNode_str(),
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
  "face_id": "{sue_str}",
  "inx_road_delimiter": "{roadnode_bridgeunit.inx_road_delimiter}",
  "otx_road_delimiter": "{roadnode_bridgeunit.otx_road_delimiter}",
  "otx_to_inx": {{}},
  "python_type": "{type_RoadNode_str()}",
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
  "face_id": "{sue_str}",
  "inx_road_delimiter": "{roadnode_bridgeunit.inx_road_delimiter}",
  "otx_road_delimiter": "{roadnode_bridgeunit.otx_road_delimiter}",
  "otx_to_inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "python_type": "{type_RoadNode_str()}",
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
    assert gen_bridgeunit.python_type == roadnode_bridgeunit.python_type
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
    assert set(get_otx_to_inx_dt_columns()).issubset(set(sorting_columns()))


def test_create_otx_to_inx_dt_ReturnsObj():
    # ESTABLISH
    casa_filterunit = get_casa_maison_filterunit_set_by_otx_to_inx()
    casa_bridgeunit = casa_filterunit.get_bridgeunit(type_RoadUnit_str())

    # WHEN
    casa_dataframe = create_otx_to_inx_dt(casa_bridgeunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_otx_to_inx_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{casa_csv=}")
    print(f"{get_ordered_csv(get_casa_maison_road_otx_to_inx_dt())=}")
    assert casa_csv == get_ordered_csv(get_casa_maison_road_otx_to_inx_dt())


def test_get_explicit_label_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_explicit_label_columns()
    assert len(get_explicit_label_columns()) == 7
    static_list = [
        "face_id",
        "python_type",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]
    assert get_explicit_label_columns() == static_list
    assert set(get_explicit_label_columns()).issubset(set(sorting_columns()))


def test_create_explicit_label_dt_ReturnsObj():
    # ESTABLISH
    casa_filterunit = get_casa_maison_filterunit_set_by_explicit_label()
    casa_bridgeunit = casa_filterunit.get_bridgeunit(type_RoadUnit_str())

    # WHEN
    casa_dataframe = create_explicit_label_dt(casa_bridgeunit)

    # THEN
    # print(f"{get_explicit_label_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_explicit_label_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_explicit_csv = get_ordered_csv(get_casa_maison_road_explicit_label_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_explicit_csv=}")
    assert casa_csv == ex_explicit_csv
