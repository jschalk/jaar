from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_bridge_if_None
from src.f08_pidgin.map import (
    GroupMap,
    groupmap_shop,
    get_groupmap_from_dict,
    get_groupmap_from_json,
    inherit_groupmap,
)
from pytest import raises as pytest_raises


def test_GroupMap_Exists():
    # ESTABLISH
    x_groupmap = GroupMap()

    # WHEN / THEN
    assert not x_groupmap.face_id
    assert not x_groupmap.event_id
    assert not x_groupmap.otx2inx
    assert not x_groupmap.unknown_word
    assert not x_groupmap.otx_bridge
    assert not x_groupmap.inx_bridge


def test_groupmap_shop_ReturnsObj_scenario0_NoParameters():
    # ESTABLISH / WHEN
    x_groupmap = groupmap_shop()

    # THEN
    assert not x_groupmap.face_id
    assert x_groupmap.event_id == 0
    assert x_groupmap.otx2inx == {}
    assert x_groupmap.unknown_word == default_unknown_word_if_None()
    assert x_groupmap.otx_bridge == default_bridge_if_None()
    assert x_groupmap.inx_bridge == default_bridge_if_None()


def test_groupmap_shop_ReturnsObj_scenario1_WithParameters():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"

    # WHEN
    x_groupmap = groupmap_shop(
        face_id=bob_str,
        event_id=event7,
        otx2inx=otx2inx,
        unknown_word=x_unknown_word,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )

    # THEN
    assert x_groupmap.face_id == bob_str
    assert x_groupmap.event_id == event7
    assert x_groupmap.otx2inx == otx2inx
    assert x_groupmap.unknown_word == x_unknown_word
    assert x_groupmap.otx_bridge == slash_otx_bridge
    assert x_groupmap.inx_bridge == colon_inx_bridge


def test_groupmap_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_groupmap = groupmap_shop(
        face_id=bob_str,
        event_id=event7,
        otx2inx=otx2inx,
        unknown_word=x_nan,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
    )

    # THEN
    assert x_groupmap.face_id == bob_str
    assert x_groupmap.event_id == event7
    assert x_groupmap.otx2inx == otx2inx
    assert x_groupmap.unknown_word == default_unknown_word_if_None()
    assert x_groupmap.otx_bridge == default_bridge_if_None()
    assert x_groupmap.inx_bridge == default_bridge_if_None()


def test_GroupMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_groupmap = groupmap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_groupmap.otx2inx != x_otx2inx

    # WHEN
    x_groupmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_groupmap.otx2inx == x_otx2inx


def test_GroupMap_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_groupmap = groupmap_shop(unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_groupmap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_groupmap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_GroupMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_groupmap = groupmap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_groupmap.otx2inx != x_otx2inx

    # WHEN
    x_groupmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_groupmap.otx2inx == x_otx2inx


def test_GroupMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_groupmap = groupmap_shop(None)
    assert x_groupmap.otx2inx == {}

    # WHEN
    x_groupmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_groupmap.otx2inx == {xio_str: sue_str}


def test_GroupMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_groupmap = groupmap_shop(None)
    assert x_groupmap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_groupmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_groupmap._get_inx_value(xio_str) == sue_str


def test_GroupMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_groupmap = groupmap_shop(None)
    assert x_groupmap.otx2inx_exists(xio_str, sue_str) is False
    assert x_groupmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_groupmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_groupmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_groupmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_groupmap.otx2inx_exists(xio_str, sue_str)
    assert x_groupmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_groupmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_groupmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_groupmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_groupmap.otx2inx_exists(xio_str, sue_str)
    assert x_groupmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_groupmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_groupmap.otx2inx_exists(zia_str, zia_str)


def test_GroupMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_groupmap = groupmap_shop(None)
    assert x_groupmap.otx_exists(xio_str) is False
    assert x_groupmap.otx_exists(sue_str) is False
    assert x_groupmap.otx_exists(bob_str) is False
    assert x_groupmap.otx_exists(zia_str) is False

    # WHEN
    x_groupmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_groupmap.otx_exists(xio_str)
    assert x_groupmap.otx_exists(sue_str) is False
    assert x_groupmap.otx_exists(bob_str) is False
    assert x_groupmap.otx_exists(zia_str) is False

    # WHEN
    x_groupmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_groupmap.otx_exists(xio_str)
    assert x_groupmap.otx_exists(sue_str) is False
    assert x_groupmap.otx_exists(bob_str) is False
    assert x_groupmap.otx_exists(zia_str)


def test_GroupMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_groupmap = groupmap_shop(None)
    x_groupmap.set_otx2inx(xio_str, sue_str)
    assert x_groupmap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_groupmap.del_otx2inx(xio_str)

    # THEN
    assert x_groupmap.otx2inx_exists(xio_str, sue_str) is False


def test_GroupMap_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_groupmap = groupmap_shop(unknown_word=x_unknown_word)
    x_groupmap.set_otx2inx(xio_str, sue_str)
    assert x_groupmap._unknown_word_in_otx2inx() is False

    # WHEN
    x_groupmap.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_groupmap._unknown_word_in_otx2inx()


def test_GroupMap_reveal_inx_ReturnsObjAndSetsAttr_group_id():
    # ESTABLISH
    inx_r_bridge = ":"
    otx_r_bridge = "/"
    swim_otx = f"swim{otx_r_bridge}"
    climb_otx = f"climb{otx_r_bridge}_{inx_r_bridge}"
    x_groupmap = groupmap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    x_groupmap.otx_exists(swim_otx) is False
    x_groupmap.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_bridge}"
    assert x_groupmap.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_groupmap.otx_exists(swim_otx)
    assert x_groupmap.otx_exists(climb_otx) is False
    assert x_groupmap._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_groupmap.reveal_inx(climb_otx) is None
    # THEN
    assert x_groupmap.otx_exists(swim_otx)
    assert x_groupmap.otx_exists(climb_otx) is False


def test_GroupMap_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    x_groupmap = groupmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        face_id=sue_str,
    )
    x1_road_map_dict = {
        "otx_bridge": x_groupmap.otx_bridge,
        "inx_bridge": x_groupmap.inx_bridge,
        "unknown_word": x_groupmap.unknown_word,
        "otx2inx": {},
        "event_id": x_groupmap.event_id,
        "face_id": x_groupmap.face_id,
    }
    assert x_groupmap.get_dict() == x1_road_map_dict

    # WHEN
    x_groupmap.set_otx2inx(clean_otx, clean_inx)
    # THEN
    x2_road_map_dict = {
        "otx_bridge": x_groupmap.otx_bridge,
        "inx_bridge": x_groupmap.inx_bridge,
        "unknown_word": x_groupmap.unknown_word,
        "otx2inx": {clean_otx: clean_inx},
        "event_id": x_groupmap.event_id,
        "face_id": sue_str,
    }
    assert x_groupmap.get_dict() == x2_road_map_dict


def test_GroupMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    event7 = 7
    slash_otx_bridge = "/"
    x_groupmap = groupmap_shop(sue_str, otx_bridge=slash_otx_bridge)
    x1_road_map_json = f"""{{
  "event_id": 0,
  "face_id": "{sue_str}",
  "inx_bridge": "{x_groupmap.inx_bridge}",
  "otx2inx": {{}},
  "otx_bridge": "{x_groupmap.otx_bridge}",
  "unknown_word": "{x_groupmap.unknown_word}"
}}"""
    print(f"           {x1_road_map_json=}")
    print(f"{x_groupmap.get_json()=}")
    assert x_groupmap.get_json() == x1_road_map_json

    # WHEN
    x_groupmap.set_otx2inx(clean_otx, clean_inx)
    x_groupmap.event_id = event7
    # THEN
    x2_road_map_json = f"""{{
  "event_id": {event7},
  "face_id": "{sue_str}",
  "inx_bridge": "{x_groupmap.inx_bridge}",
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_bridge": "{x_groupmap.otx_bridge}",
  "unknown_word": "{x_groupmap.unknown_word}"
}}"""
    print(f"           {x2_road_map_json=}")
    print(f"{x_groupmap.get_json()=}")
    assert x_groupmap.get_json() == x2_road_map_json


def test_get_groupmap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_bridge = "/"
    x_groupmap = groupmap_shop(sue_str, event7, otx_bridge=slash_otx_bridge)
    x_groupmap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_groupmap = get_groupmap_from_dict(x_groupmap.get_dict())

    # THEN
    assert gen_groupmap.face_id == x_groupmap.face_id
    assert gen_groupmap.event_id == x_groupmap.event_id
    assert gen_groupmap.event_id == event7
    assert gen_groupmap == x_groupmap


def test_get_groupmap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_bridge = "/"
    x_groupmap = groupmap_shop(slash_otx_bridge)
    x_groupmap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_groupmap = get_groupmap_from_json(x_groupmap.get_json())

    # THEN
    assert x_groupmap == x_groupmap


def test_GroupMap_is_inx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_bridge = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_groupmap = groupmap_shop(inx_bridge=inx_bridge)
    assert x_groupmap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_groupmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_groupmap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_groupmap.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_groupmap._is_inx_bridge_inclusion_correct() is False


def test_GroupMap_is_otx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    otx_bridge = "/"
    zia_inx = "Zia"
    zia_otx = f"Zia{otx_bridge}"
    x_groupmap = groupmap_shop(otx_bridge=otx_bridge)
    assert x_groupmap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_groupmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_groupmap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_groupmap.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_groupmap._is_otx_bridge_inclusion_correct() is False


def test_GroupMap_is_valid_ReturnsObj():
    # ESTABLISH
    otx_bridge = ":"
    inx_bridge = "/"
    sue_otx = f"Xio{otx_bridge}"
    sue_inx = f"Sue{inx_bridge}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_groupmap = groupmap_shop(otx_bridge=otx_bridge, inx_bridge=inx_bridge)
    assert x_groupmap.is_valid()

    # WHEN
    x_groupmap.set_otx2inx(sue_otx, sue_inx)
    # THEN
    assert x_groupmap.is_valid()

    # WHEN
    x_groupmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_groupmap.is_valid() is False


def test_inherit_groupmap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_groupmap = groupmap_shop(zia_str, 3)
    new_groupmap = groupmap_shop(zia_str, 5)
    # WHEN
    inherit_groupmap(new_groupmap, old_groupmap)

    # THEN
    assert new_groupmap
    assert new_groupmap == groupmap_shop(zia_str, 5)


def test_inherit_groupmap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_groupmap = groupmap_shop(sue_str, 0, otx_bridge=slash_otx_bridge)
    new_groupmap = groupmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_groupmap(new_groupmap, old_groupmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_groupmap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_groupmap = groupmap_shop(sue_str, 0, inx_bridge=slash_otx_bridge)
    new_groupmap = groupmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_groupmap(new_groupmap, old_groupmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_groupmap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_word():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    old_groupmap = groupmap_shop(sue_str, 0, unknown_word=x_unknown_word)
    new_groupmap = groupmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_groupmap(new_groupmap, old_groupmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_groupmap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_id():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_groupmap = groupmap_shop(sue_str, 0)
    new_groupmap = groupmap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_groupmap(new_groupmap, old_groupmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_groupmap_ReturnsObj_Scenario5_RaiseErrorWhenEventIDsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_groupmap = groupmap_shop(sue_str, 5)
    new_groupmap = groupmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_groupmap(new_groupmap, old_groupmap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_groupmap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_groupmap = groupmap_shop(zia_str, 3)
    old_groupmap.set_otx2inx(xio_otx, xio_inx)
    new_groupmap = groupmap_shop(zia_str, 7)
    assert new_groupmap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_groupmap = inherit_groupmap(new_groupmap, old_groupmap)

    # THEN
    assert inherited_groupmap.otx2inx_exists(xio_otx, xio_inx)
