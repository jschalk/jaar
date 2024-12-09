from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_wall_if_None
from src.f08_pidgin.bridge import (
    AcctBridge,
    acctbridge_shop,
    get_acctbridge_from_dict,
    get_acctbridge_from_json,
)
from pytest import raises as pytest_raises
from numpy import int64 as numpy_int64


def test_AcctBridge_Exists():
    # ESTABLISH
    x_acctbridge = AcctBridge()

    # WHEN / THEN
    assert not x_acctbridge.face_id
    assert not x_acctbridge.event_id
    assert not x_acctbridge.otx2inx
    assert not x_acctbridge.unknown_word
    assert not x_acctbridge.otx_wall
    assert not x_acctbridge.inx_wall


def test_acctbridge_shop_ReturnsObj_scenario0():
    # ESTABLISH / WHEN
    x_acctbridge = acctbridge_shop()

    # THEN
    assert not x_acctbridge.face_id
    assert x_acctbridge.event_id == 0
    assert x_acctbridge.otx2inx == {}
    assert x_acctbridge.unknown_word == default_unknown_word_if_None()
    assert x_acctbridge.otx_wall == default_wall_if_None()
    assert x_acctbridge.inx_wall == default_wall_if_None()


def test_acctbridge_shop_ReturnsObj_scenario1_WithParameters():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"

    # WHEN
    x_acctbridge = acctbridge_shop(
        x_face_id=bob_str,
        x_event_id=event7,
        x_otx2inx=otx2inx,
        x_unknown_word=x_unknown_word,
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
    )

    # THEN
    assert x_acctbridge.face_id == bob_str
    assert x_acctbridge.event_id == event7
    assert x_acctbridge.otx2inx == otx2inx
    assert x_acctbridge.unknown_word == x_unknown_word
    assert x_acctbridge.otx_wall == slash_otx_wall
    assert x_acctbridge.inx_wall == colon_inx_wall


def test_acctbridge_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = numpy_int64(7)
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_acctbridge = acctbridge_shop(
        x_face_id=bob_str,
        x_event_id=numpy_int64(event7),
        x_otx2inx=otx2inx,
        x_unknown_word=x_nan,
        x_otx_wall=x_nan,
        x_inx_wall=x_nan,
    )

    # THEN
    assert x_acctbridge.face_id == bob_str
    assert x_acctbridge.event_id == event7
    assert str(type(x_acctbridge.event_id)) != "<class 'numpy.int64'>"
    assert str(type(x_acctbridge.event_id)) == "<class 'int'>"
    assert x_acctbridge.otx2inx == otx2inx
    assert x_acctbridge.unknown_word == default_unknown_word_if_None()
    assert x_acctbridge.otx_wall == default_wall_if_None()
    assert x_acctbridge.inx_wall == default_wall_if_None()


def test_AcctBridge_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_acctbridge = acctbridge_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_acctbridge.otx2inx != x_otx2inx

    # WHEN
    x_acctbridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_acctbridge.otx2inx == x_otx2inx


def test_AcctBridge_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_acctbridge = acctbridge_shop(None, x_unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_acctbridge.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_acctbridge.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_AcctBridge_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_acctbridge = acctbridge_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_acctbridge.otx2inx != x_otx2inx

    # WHEN
    x_acctbridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_acctbridge.otx2inx == x_otx2inx


def test_AcctBridge_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_acctbridge = acctbridge_shop(None)
    assert x_acctbridge.otx2inx == {}

    # WHEN
    x_acctbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctbridge.otx2inx == {xio_str: sue_str}


def test_AcctBridge_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_acctbridge = acctbridge_shop(None)
    assert x_acctbridge._get_inx_value(xio_str) != sue_str

    # WHEN
    x_acctbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctbridge._get_inx_value(xio_str) == sue_str


def test_AcctBridge_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_acctbridge = acctbridge_shop(None)
    assert x_acctbridge.otx2inx_exists(xio_str, sue_str) is False
    assert x_acctbridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_acctbridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_acctbridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_acctbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctbridge.otx2inx_exists(xio_str, sue_str)
    assert x_acctbridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_acctbridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_acctbridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_acctbridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_acctbridge.otx2inx_exists(xio_str, sue_str)
    assert x_acctbridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_acctbridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_acctbridge.otx2inx_exists(zia_str, zia_str)


def test_AcctBridge_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_acctbridge = acctbridge_shop(None)
    assert x_acctbridge.otx_exists(xio_str) is False
    assert x_acctbridge.otx_exists(sue_str) is False
    assert x_acctbridge.otx_exists(bob_str) is False
    assert x_acctbridge.otx_exists(zia_str) is False

    # WHEN
    x_acctbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_acctbridge.otx_exists(xio_str)
    assert x_acctbridge.otx_exists(sue_str) is False
    assert x_acctbridge.otx_exists(bob_str) is False
    assert x_acctbridge.otx_exists(zia_str) is False

    # WHEN
    x_acctbridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_acctbridge.otx_exists(xio_str)
    assert x_acctbridge.otx_exists(sue_str) is False
    assert x_acctbridge.otx_exists(bob_str) is False
    assert x_acctbridge.otx_exists(zia_str)


def test_AcctBridge_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_acctbridge = acctbridge_shop(None)
    x_acctbridge.set_otx2inx(xio_str, sue_str)
    assert x_acctbridge.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_acctbridge.del_otx2inx(xio_str)

    # THEN
    assert x_acctbridge.otx2inx_exists(xio_str, sue_str) is False


def test_AcctBridge_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_acctbridge = acctbridge_shop(None, x_unknown_word=x_unknown_word)
    x_acctbridge.set_otx2inx(xio_str, sue_str)
    assert x_acctbridge._unknown_word_in_otx2inx() is False

    # WHEN
    x_acctbridge.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_acctbridge._unknown_word_in_otx2inx()


def test_AcctBridge_reveal_inx_ReturnsObjAndSetsAttr_acct_id():
    # ESTABLISH
    inx_r_wall = ":"
    otx_r_wall = "/"
    swim_otx = f"swim{otx_r_wall}"
    climb_otx = f"climb{otx_r_wall}_{inx_r_wall}"
    x_acctbridge = acctbridge_shop(otx_r_wall, inx_r_wall)
    x_acctbridge.otx_exists(swim_otx) is False
    x_acctbridge.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_wall}"
    assert x_acctbridge.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_acctbridge.otx_exists(swim_otx)
    assert x_acctbridge.otx_exists(climb_otx) is False
    assert x_acctbridge._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_acctbridge.reveal_inx(climb_otx) is None
    # THEN
    assert x_acctbridge.otx_exists(swim_otx)
    assert x_acctbridge.otx_exists(climb_otx) is False


def test_AcctBridge_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    event7 = 7
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    ideaunit_acctbridge = acctbridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_face_id=sue_str,
        x_event_id=event7,
    )
    x1_road_bridge_dict = {
        "otx_wall": ideaunit_acctbridge.otx_wall,
        "inx_wall": ideaunit_acctbridge.inx_wall,
        "unknown_word": ideaunit_acctbridge.unknown_word,
        "otx2inx": {},
        "face_id": ideaunit_acctbridge.face_id,
        "event_id": ideaunit_acctbridge.event_id,
    }
    assert ideaunit_acctbridge.get_dict() == x1_road_bridge_dict

    # WHEN
    ideaunit_acctbridge.set_otx2inx(clean_otx, clean_inx)
    # THEN
    x2_road_bridge_dict = {
        "otx_wall": ideaunit_acctbridge.otx_wall,
        "inx_wall": ideaunit_acctbridge.inx_wall,
        "unknown_word": ideaunit_acctbridge.unknown_word,
        "otx2inx": {clean_otx: clean_inx},
        "face_id": sue_str,
        "event_id": event7,
    }
    assert ideaunit_acctbridge.get_dict() == x2_road_bridge_dict


def test_AcctBridge_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    event7 = 7
    slash_otx_wall = "/"
    ideaunit_acctbridge = acctbridge_shop("IdeaUnit", slash_otx_wall, x_face_id=sue_str)
    x1_road_bridge_json = f"""{{
  "event_id": 0,
  "face_id": "{sue_str}",
  "inx_wall": "{ideaunit_acctbridge.inx_wall}",
  "otx2inx": {{}},
  "otx_wall": "{ideaunit_acctbridge.otx_wall}",
  "unknown_word": "{ideaunit_acctbridge.unknown_word}"
}}"""
    print(f"           {x1_road_bridge_json=}")
    print(f"{ideaunit_acctbridge.get_json()=}")
    assert ideaunit_acctbridge.get_json() == x1_road_bridge_json

    # WHEN
    ideaunit_acctbridge.set_otx2inx(clean_otx, clean_inx)
    ideaunit_acctbridge.event_id = event7
    # THEN
    x2_road_bridge_json = f"""{{
  "event_id": {event7},
  "face_id": "{sue_str}",
  "inx_wall": "{ideaunit_acctbridge.inx_wall}",
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_wall": "{ideaunit_acctbridge.otx_wall}",
  "unknown_word": "{ideaunit_acctbridge.unknown_word}"
}}"""
    print(f"           {x2_road_bridge_json=}")
    print(f"{ideaunit_acctbridge.get_json()=}")
    assert ideaunit_acctbridge.get_json() == x2_road_bridge_json


def test_get_acctbridge_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    event7 = 7
    ideaunit_acctbridge = acctbridge_shop(
        slash_otx_wall, x_face_id=sue_str, x_event_id=event7
    )
    ideaunit_acctbridge.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_acctbridge = get_acctbridge_from_dict(ideaunit_acctbridge.get_dict())

    # THEN
    assert gen_acctbridge.face_id == ideaunit_acctbridge.face_id
    assert gen_acctbridge.event_id == ideaunit_acctbridge.event_id
    assert gen_acctbridge.event_id == event7
    assert gen_acctbridge == ideaunit_acctbridge


def test_get_acctbridge_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    ideaunit_acctbridge = acctbridge_shop(slash_otx_wall)
    ideaunit_acctbridge.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_acctbridge = get_acctbridge_from_json(ideaunit_acctbridge.get_json())

    # THEN
    assert x_acctbridge == ideaunit_acctbridge


def test_AcctBridge_is_inx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_wall = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_acctbridge = acctbridge_shop(x_inx_wall=inx_wall)
    assert x_acctbridge._is_inx_wall_inclusion_correct()

    # WHEN
    x_acctbridge.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_acctbridge._is_inx_wall_inclusion_correct()

    # WHEN
    x_acctbridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_acctbridge._is_inx_wall_inclusion_correct() is False


def test_AcctBridge_is_otx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_wall = "/"
    zia_otx = f"Zia{otx_wall}"
    zia_inx = "Zia"
    x_acctbridge = acctbridge_shop(x_otx_wall=otx_wall)
    assert x_acctbridge._is_otx_wall_inclusion_correct()

    # WHEN
    x_acctbridge.set_otx2inx(xio_otx, xio_inx)
    # THEN
    assert x_acctbridge._is_otx_wall_inclusion_correct()

    # WHEN
    x_acctbridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_acctbridge._is_otx_wall_inclusion_correct() is False


def test_AcctBridge_is_valid_ReturnsObj():
    # ESTABLISH
    otx_wall = ":"
    inx_wall = "/"
    sue_otx = f"Xio{otx_wall}"
    sue_with_wall = f"Sue{inx_wall}"
    sue_without_wall = f"Sue{otx_wall}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_acctbridge = acctbridge_shop(otx_wall, x_inx_wall=inx_wall)
    assert x_acctbridge.is_valid()

    # WHEN
    x_acctbridge.set_otx2inx(sue_otx, sue_with_wall)
    # THEN
    assert x_acctbridge.is_valid() is False

    # WHEN
    x_acctbridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_acctbridge.is_valid() is False

    # WHEN
    x_acctbridge.set_otx2inx(sue_otx, sue_without_wall)
    # THEN
    assert x_acctbridge.is_valid() is False
