from src.f08_pidgin.bridge import (
    NodeBridge,
    nodebridge_shop,
    get_nodebridge_from_dict,
    get_nodebridge_from_json,
)
from pytest import raises as pytest_raises


def test_NodeBridge_Exists():
    # ESTABLISH
    x_nodebridge = NodeBridge()

    # WHEN / THEN
    assert not x_nodebridge.otx2inx
    assert not x_nodebridge.unknown_word
    assert not x_nodebridge.otx_wall
    assert not x_nodebridge.inx_wall
    assert not x_nodebridge.face_id


def test_nodebridge_shop_ReturnsObj_scenario0():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    otx2inx = {xio_str: sue_str}
    x_unknown_word = "UnknownNodeId"
    slash_otx_wall = "/"
    colon_inx_wall = ":"

    # WHEN
    x_nodebridge = nodebridge_shop(
        x_otx2inx=otx2inx,
        x_unknown_word=x_unknown_word,
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_face_id=bob_str,
    )

    # THEN
    assert x_nodebridge.otx2inx == otx2inx
    assert x_nodebridge.unknown_word == x_unknown_word
    assert x_nodebridge.otx_wall == slash_otx_wall
    assert x_nodebridge.inx_wall == colon_inx_wall
    assert x_nodebridge.face_id == bob_str


def test_NodeBridge_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_nodebridge = nodebridge_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_nodebridge.otx2inx != x_otx2inx

    # WHEN
    x_nodebridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_nodebridge.otx2inx == x_otx2inx


def test_NodeBridge_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownNodeId"
    x_nodebridge = nodebridge_shop(None, x_unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_nodebridge.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_nodebridge.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_NodeBridge_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownNodeId"
    x_nodebridge = nodebridge_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_nodebridge.otx2inx != x_otx2inx

    # WHEN
    x_nodebridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_nodebridge.otx2inx == x_otx2inx


def test_NodeBridge_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_nodebridge = nodebridge_shop(None)
    assert x_nodebridge.otx2inx == {}

    # WHEN
    x_nodebridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_nodebridge.otx2inx == {xio_str: sue_str}


def test_NodeBridge_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_nodebridge = nodebridge_shop(None)
    assert x_nodebridge._get_inx_value(xio_str) != sue_str

    # WHEN
    x_nodebridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_nodebridge._get_inx_value(xio_str) == sue_str


def test_NodeBridge_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_nodebridge = nodebridge_shop(None)
    assert x_nodebridge.otx2inx_exists(xio_str, sue_str) is False
    assert x_nodebridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_nodebridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_nodebridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_nodebridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_nodebridge.otx2inx_exists(xio_str, sue_str)
    assert x_nodebridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_nodebridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_nodebridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_nodebridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_nodebridge.otx2inx_exists(xio_str, sue_str)
    assert x_nodebridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_nodebridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_nodebridge.otx2inx_exists(zia_str, zia_str)


def test_NodeBridge_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_nodebridge = nodebridge_shop(None)
    assert x_nodebridge.otx_exists(xio_str) is False
    assert x_nodebridge.otx_exists(sue_str) is False
    assert x_nodebridge.otx_exists(bob_str) is False
    assert x_nodebridge.otx_exists(zia_str) is False

    # WHEN
    x_nodebridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_nodebridge.otx_exists(xio_str)
    assert x_nodebridge.otx_exists(sue_str) is False
    assert x_nodebridge.otx_exists(bob_str) is False
    assert x_nodebridge.otx_exists(zia_str) is False

    # WHEN
    x_nodebridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_nodebridge.otx_exists(xio_str)
    assert x_nodebridge.otx_exists(sue_str) is False
    assert x_nodebridge.otx_exists(bob_str) is False
    assert x_nodebridge.otx_exists(zia_str)


def test_NodeBridge_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_nodebridge = nodebridge_shop(None)
    x_nodebridge.set_otx2inx(xio_str, sue_str)
    assert x_nodebridge.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_nodebridge.del_otx2inx(xio_str)

    # THEN
    assert x_nodebridge.otx2inx_exists(xio_str, sue_str) is False


def test_NodeBridge_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownNodeId"
    x_nodebridge = nodebridge_shop(None, x_unknown_word=x_unknown_word)
    x_nodebridge.set_otx2inx(xio_str, sue_str)
    assert x_nodebridge._unknown_word_in_otx2inx() is False

    # WHEN
    x_nodebridge.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_nodebridge._unknown_word_in_otx2inx()


def test_NodeBridge_reveal_inx_ReturnsObjAndSetsAttr_node_id():
    # ESTABLISH
    inx_r_wall = ":"
    otx_r_wall = "/"
    swim_otx = f"swim{otx_r_wall}"
    climb_otx = f"climb{otx_r_wall}_{inx_r_wall}"
    x_nodebridge = nodebridge_shop(otx_r_wall, inx_r_wall)
    x_nodebridge.otx_exists(swim_otx) is False
    x_nodebridge.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_wall}"
    assert x_nodebridge.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_nodebridge.otx_exists(swim_otx)
    assert x_nodebridge.otx_exists(climb_otx) is False
    assert x_nodebridge._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_nodebridge.reveal_inx(climb_otx) is None
    # THEN
    assert x_nodebridge.otx_exists(swim_otx)
    assert x_nodebridge.otx_exists(climb_otx) is False


def test_NodeBridge_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    roadnode_nodebridge = nodebridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_face_id=sue_str,
    )
    x1_road_bridge_dict = {
        "otx_wall": roadnode_nodebridge.otx_wall,
        "inx_wall": roadnode_nodebridge.inx_wall,
        "unknown_word": roadnode_nodebridge.unknown_word,
        "otx2inx": {},
        "face_id": roadnode_nodebridge.face_id,
    }
    assert roadnode_nodebridge.get_dict() == x1_road_bridge_dict

    # WHEN
    roadnode_nodebridge.set_otx2inx(clean_otx, clean_inx)
    # THEN
    x2_road_bridge_dict = {
        "otx_wall": roadnode_nodebridge.otx_wall,
        "inx_wall": roadnode_nodebridge.inx_wall,
        "unknown_word": roadnode_nodebridge.unknown_word,
        "otx2inx": {clean_otx: clean_inx},
        "face_id": sue_str,
    }
    assert roadnode_nodebridge.get_dict() == x2_road_bridge_dict


def test_NodeBridge_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_wall = "/"
    roadnode_nodebridge = nodebridge_shop("RoadNode", slash_otx_wall, x_face_id=sue_str)
    x1_road_bridge_json = f"""{{
  "face_id": "{sue_str}",
  "inx_wall": "{roadnode_nodebridge.inx_wall}",
  "otx2inx": {{}},
  "otx_wall": "{roadnode_nodebridge.otx_wall}",
  "unknown_word": "{roadnode_nodebridge.unknown_word}"
}}"""
    print(f"           {x1_road_bridge_json=}")
    print(f"{roadnode_nodebridge.get_json()=}")
    assert roadnode_nodebridge.get_json() == x1_road_bridge_json

    # WHEN
    roadnode_nodebridge.set_otx2inx(clean_otx, clean_inx)
    # THEN
    x2_road_bridge_json = f"""{{
  "face_id": "{sue_str}",
  "inx_wall": "{roadnode_nodebridge.inx_wall}",
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_wall": "{roadnode_nodebridge.otx_wall}",
  "unknown_word": "{roadnode_nodebridge.unknown_word}"
}}"""
    print(f"           {x2_road_bridge_json=}")
    print(f"{roadnode_nodebridge.get_json()=}")
    assert roadnode_nodebridge.get_json() == x2_road_bridge_json


def test_get_nodebridge_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    roadnode_nodebridge = nodebridge_shop(slash_otx_wall, x_face_id=sue_str)
    roadnode_nodebridge.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_nodebridge = get_nodebridge_from_dict(roadnode_nodebridge.get_dict())

    # THEN
    assert gen_nodebridge.face_id == roadnode_nodebridge.face_id
    assert gen_nodebridge == roadnode_nodebridge


def test_get_nodebridge_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    roadnode_nodebridge = nodebridge_shop(slash_otx_wall)
    roadnode_nodebridge.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_nodebridge = get_nodebridge_from_json(roadnode_nodebridge.get_json())

    # THEN
    assert x_nodebridge == roadnode_nodebridge


def test_NodeBridge_is_inx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_wall = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_nodebridge = nodebridge_shop(x_inx_wall=inx_wall)
    assert x_nodebridge._is_inx_wall_inclusion_correct()

    # WHEN
    x_nodebridge.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_nodebridge._is_inx_wall_inclusion_correct()

    # WHEN
    x_nodebridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_nodebridge._is_inx_wall_inclusion_correct() is False


def test_NodeBridge_is_otx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_wall = "/"
    zia_otx = f"Zia{otx_wall}"
    zia_inx = "Zia"
    x_nodebridge = nodebridge_shop(x_otx_wall=otx_wall)
    assert x_nodebridge._is_otx_wall_inclusion_correct()

    # WHEN
    x_nodebridge.set_otx2inx(xio_otx, xio_inx)
    # THEN
    assert x_nodebridge._is_otx_wall_inclusion_correct()

    # WHEN
    x_nodebridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_nodebridge._is_otx_wall_inclusion_correct() is False


def test_NodeBridge_is_valid_ReturnsObj():
    # ESTABLISH
    otx_wall = ":"
    inx_wall = "/"
    sue_otx = f"Xio{otx_wall}"
    sue_with_wall = f"Sue{inx_wall}"
    sue_without_wall = f"Sue{otx_wall}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_nodebridge = nodebridge_shop(otx_wall, x_inx_wall=inx_wall)
    assert x_nodebridge.is_valid()

    # WHEN
    x_nodebridge.set_otx2inx(sue_otx, sue_with_wall)
    # THEN
    assert x_nodebridge.is_valid() is False

    # WHEN
    x_nodebridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_nodebridge.is_valid() is False

    # WHEN
    x_nodebridge.set_otx2inx(sue_otx, sue_without_wall)
    # THEN
    assert x_nodebridge.is_valid() is False
