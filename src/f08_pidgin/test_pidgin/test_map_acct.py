from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_bridge_if_None
from src.f08_pidgin.map import (
    AcctMap,
    acctmap_shop,
    get_acctmap_from_dict,
    get_acctmap_from_json,
    inherit_acctmap,
)
from pytest import raises as pytest_raises
from numpy import int64 as numpy_int64


def test_AcctMap_Exists():
    # ESTABLISH
    x_acctmap = AcctMap()

    # WHEN / THEN
    assert not x_acctmap.face_id
    assert not x_acctmap.event_int
    assert not x_acctmap.otx2inx
    assert not x_acctmap.unknown_word
    assert not x_acctmap.otx_bridge
    assert not x_acctmap.inx_bridge


def test_acctmap_shop_ReturnsObj_scenario0():
    # ESTABLISH / WHEN
    x_acctmap = acctmap_shop()

    # THEN
    assert not x_acctmap.face_id
    assert x_acctmap.event_int == 0
    assert x_acctmap.otx2inx == {}
    assert x_acctmap.unknown_word == default_unknown_word_if_None()
    assert x_acctmap.otx_bridge == default_bridge_if_None()
    assert x_acctmap.inx_bridge == default_bridge_if_None()


def test_acctmap_shop_ReturnsObj_scenario1_WithParameters():
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
    x_acctmap = acctmap_shop(
        face_id=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_word=x_unknown_word,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )

    # THEN
    assert x_acctmap.face_id == bob_str
    assert x_acctmap.event_int == event7
    assert x_acctmap.otx2inx == otx2inx
    assert x_acctmap.unknown_word == x_unknown_word
    assert x_acctmap.otx_bridge == slash_otx_bridge
    assert x_acctmap.inx_bridge == colon_inx_bridge


def test_acctmap_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = numpy_int64(7)
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_acctmap = acctmap_shop(
        face_id=bob_str,
        event_int=numpy_int64(event7),
        otx2inx=otx2inx,
        unknown_word=x_nan,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
    )

    # THEN
    assert x_acctmap.face_id == bob_str
    assert x_acctmap.event_int == event7
    assert str(type(x_acctmap.event_int)) != "<class 'numpy.int64'>"
    assert str(type(x_acctmap.event_int)) == "<class 'int'>"
    assert x_acctmap.otx2inx == otx2inx
    assert x_acctmap.unknown_word == default_unknown_word_if_None()
    assert x_acctmap.otx_bridge == default_bridge_if_None()
    assert x_acctmap.inx_bridge == default_bridge_if_None()


def test_AcctMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_acctmap = acctmap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_acctmap.otx2inx != x_otx2inx

    # WHEN
    x_acctmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_acctmap.otx2inx == x_otx2inx


def test_AcctMap_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_acctmap = acctmap_shop(None, unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_acctmap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_acctmap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_AcctMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_acctmap = acctmap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_acctmap.otx2inx != x_otx2inx

    # WHEN
    x_acctmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_acctmap.otx2inx == x_otx2inx


def test_AcctMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_acctmap = acctmap_shop(None)
    assert x_acctmap.otx2inx == {}

    # WHEN
    x_acctmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctmap.otx2inx == {xio_str: sue_str}


def test_AcctMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_acctmap = acctmap_shop(None)
    assert x_acctmap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_acctmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctmap._get_inx_value(xio_str) == sue_str


def test_AcctMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_acctmap = acctmap_shop(None)
    assert x_acctmap.otx2inx_exists(xio_str, sue_str) is False
    assert x_acctmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_acctmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_acctmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_acctmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctmap.otx2inx_exists(xio_str, sue_str)
    assert x_acctmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_acctmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_acctmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_acctmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_acctmap.otx2inx_exists(xio_str, sue_str)
    assert x_acctmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_acctmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_acctmap.otx2inx_exists(zia_str, zia_str)


def test_AcctMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_acctmap = acctmap_shop(None)
    assert x_acctmap.otx_exists(xio_str) is False
    assert x_acctmap.otx_exists(sue_str) is False
    assert x_acctmap.otx_exists(bob_str) is False
    assert x_acctmap.otx_exists(zia_str) is False

    # WHEN
    x_acctmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctmap.otx_exists(xio_str)
    assert x_acctmap.otx_exists(sue_str) is False
    assert x_acctmap.otx_exists(bob_str) is False
    assert x_acctmap.otx_exists(zia_str) is False

    # WHEN
    x_acctmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_acctmap.otx_exists(xio_str)
    assert x_acctmap.otx_exists(sue_str) is False
    assert x_acctmap.otx_exists(bob_str) is False
    assert x_acctmap.otx_exists(zia_str)


def test_AcctMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_acctmap = acctmap_shop(None)
    x_acctmap.set_otx2inx(xio_str, sue_str)
    assert x_acctmap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_acctmap.del_otx2inx(xio_str)

    # THEN
    assert x_acctmap.otx2inx_exists(xio_str, sue_str) is False


def test_AcctMap_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_acctmap = acctmap_shop(None, unknown_word=x_unknown_word)
    x_acctmap.set_otx2inx(xio_str, sue_str)
    assert x_acctmap._unknown_word_in_otx2inx() is False

    # WHEN
    x_acctmap.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_acctmap._unknown_word_in_otx2inx()


def test_AcctMap_reveal_inx_ReturnsObjAndSetsAttr_acct_id():
    # ESTABLISH
    inx_r_bridge = ":"
    otx_r_bridge = "/"
    swim_otx = f"swim{otx_r_bridge}"
    climb_otx = f"climb{otx_r_bridge}_{inx_r_bridge}"
    x_acctmap = acctmap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    x_acctmap.otx_exists(swim_otx) is False
    x_acctmap.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_bridge}"
    assert x_acctmap.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_acctmap.otx_exists(swim_otx)
    assert x_acctmap.otx_exists(climb_otx) is False
    assert x_acctmap._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_acctmap.reveal_inx(climb_otx) is None
    # THEN
    assert x_acctmap.otx_exists(swim_otx)
    assert x_acctmap.otx_exists(climb_otx) is False


def test_AcctMap_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    event7 = 7
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    x_acctmap = acctmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        face_id=sue_str,
        event_int=event7,
    )
    x1_road_map_dict = {
        "otx_bridge": x_acctmap.otx_bridge,
        "inx_bridge": x_acctmap.inx_bridge,
        "unknown_word": x_acctmap.unknown_word,
        "otx2inx": {},
        "face_id": x_acctmap.face_id,
        "event_int": x_acctmap.event_int,
    }
    assert x_acctmap.get_dict() == x1_road_map_dict

    # WHEN
    x_acctmap.set_otx2inx(clean_otx, clean_inx)
    # THEN
    x2_road_map_dict = {
        "otx_bridge": x_acctmap.otx_bridge,
        "inx_bridge": x_acctmap.inx_bridge,
        "unknown_word": x_acctmap.unknown_word,
        "otx2inx": {clean_otx: clean_inx},
        "face_id": sue_str,
        "event_int": event7,
    }
    assert x_acctmap.get_dict() == x2_road_map_dict


def test_AcctMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    event7 = 7
    slash_otx_bridge = "/"
    x_acctmap = acctmap_shop(sue_str, otx_bridge=slash_otx_bridge)
    x1_road_map_json = f"""{{
  "event_int": 0,
  "face_id": "{sue_str}",
  "inx_bridge": "{x_acctmap.inx_bridge}",
  "otx2inx": {{}},
  "otx_bridge": "{x_acctmap.otx_bridge}",
  "unknown_word": "{x_acctmap.unknown_word}"
}}"""
    print(f"           {x1_road_map_json=}")
    print(f"{x_acctmap.get_json()=}")
    assert x_acctmap.get_json() == x1_road_map_json

    # WHEN
    x_acctmap.set_otx2inx(clean_otx, clean_inx)
    x_acctmap.event_int = event7
    # THEN
    x2_road_map_json = f"""{{
  "event_int": {event7},
  "face_id": "{sue_str}",
  "inx_bridge": "{x_acctmap.inx_bridge}",
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_bridge": "{x_acctmap.otx_bridge}",
  "unknown_word": "{x_acctmap.unknown_word}"
}}"""
    print(f"           {x2_road_map_json=}")
    print(f"{x_acctmap.get_json()=}")
    assert x_acctmap.get_json() == x2_road_map_json


def test_get_acctmap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_bridge = "/"
    event7 = 7
    x_acctmap = acctmap_shop(sue_str, event7, otx_bridge=slash_otx_bridge)
    x_acctmap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_acctmap = get_acctmap_from_dict(x_acctmap.get_dict())

    # THEN
    assert gen_acctmap.face_id == x_acctmap.face_id
    assert gen_acctmap.event_int == x_acctmap.event_int
    assert gen_acctmap.event_int == event7
    assert gen_acctmap == x_acctmap


def test_get_acctmap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_bridge = "/"
    x_acctmap = acctmap_shop(slash_otx_bridge)
    x_acctmap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_acctmap = get_acctmap_from_json(x_acctmap.get_json())

    # THEN
    assert x_acctmap == x_acctmap


def test_AcctMap_is_inx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_bridge = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_acctmap = acctmap_shop(inx_bridge=inx_bridge)
    assert x_acctmap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_acctmap.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_acctmap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_acctmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_acctmap._is_inx_bridge_inclusion_correct() is False


def test_AcctMap_is_otx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_bridge = "/"
    zia_otx = f"Zia{otx_bridge}"
    zia_inx = "Zia"
    x_acctmap = acctmap_shop(otx_bridge=otx_bridge)
    assert x_acctmap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_acctmap.set_otx2inx(xio_otx, xio_inx)
    # THEN
    assert x_acctmap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_acctmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_acctmap._is_otx_bridge_inclusion_correct() is False


def test_AcctMap_is_valid_ReturnsObj():
    # ESTABLISH
    otx_bridge = ":"
    inx_bridge = "/"
    sue_otx = f"Xio{otx_bridge}"
    sue_with_bridge = f"Sue{inx_bridge}"
    sue_without_bridge = f"Sue{otx_bridge}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_acctmap = acctmap_shop(otx_bridge=otx_bridge, inx_bridge=inx_bridge)
    assert x_acctmap.is_valid()

    # WHEN
    x_acctmap.set_otx2inx(sue_otx, sue_with_bridge)
    # THEN
    assert x_acctmap.is_valid() is False

    # WHEN
    x_acctmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_acctmap.is_valid() is False

    # WHEN
    x_acctmap.set_otx2inx(sue_otx, sue_without_bridge)
    # THEN
    assert x_acctmap.is_valid() is False


def test_inherit_acctmap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_acctmap = acctmap_shop(zia_str, 3)
    new_acctmap = acctmap_shop(zia_str, 5)
    # WHEN
    inherit_acctmap(new_acctmap, old_acctmap)

    # THEN
    assert new_acctmap
    assert new_acctmap == acctmap_shop(zia_str, 5)


def test_inherit_acctmap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_acctmap = acctmap_shop(sue_str, 0, otx_bridge=slash_otx_bridge)
    new_acctmap = acctmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_acctmap(new_acctmap, old_acctmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_acctmap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_acctmap = acctmap_shop(sue_str, 0, inx_bridge=slash_otx_bridge)
    new_acctmap = acctmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_acctmap(new_acctmap, old_acctmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_acctmap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_word():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    old_acctmap = acctmap_shop(sue_str, 0, unknown_word=x_unknown_word)
    new_acctmap = acctmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_acctmap(new_acctmap, old_acctmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_acctmap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_id():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_acctmap = acctmap_shop(sue_str, 0)
    new_acctmap = acctmap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_acctmap(new_acctmap, old_acctmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_acctmap_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_acctmap = acctmap_shop(sue_str, 5)
    new_acctmap = acctmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_acctmap(new_acctmap, old_acctmap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_acctmap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_acctmap = acctmap_shop(zia_str, 3)
    old_acctmap.set_otx2inx(xio_otx, xio_inx)
    new_acctmap = acctmap_shop(zia_str, 7)
    assert new_acctmap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_acctmap = inherit_acctmap(new_acctmap, old_acctmap)

    # THEN
    assert inherited_acctmap.otx2inx_exists(xio_otx, xio_inx)
