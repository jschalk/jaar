from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_wall_if_None
from src.f08_pidgin.bridge import (
    IdeaBridge,
    ideabridge_shop,
    get_ideabridge_from_dict,
    get_ideabridge_from_json,
    inherit_ideabridge,
)
from pytest import raises as pytest_raises


def test_IdeaBridge_Exists():
    # ESTABLISH
    x_ideabridge = IdeaBridge()

    # WHEN / THEN
    assert not x_ideabridge.face_id
    assert not x_ideabridge.event_id
    assert not x_ideabridge.otx2inx
    assert not x_ideabridge.unknown_word
    assert not x_ideabridge.otx_wall
    assert not x_ideabridge.inx_wall


def test_ideabridge_shop_ReturnsObj_scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_ideabridge = ideabridge_shop()

    # THEN
    assert not x_ideabridge.face_id
    assert x_ideabridge.event_id == 0
    assert x_ideabridge.otx2inx == {}
    assert x_ideabridge.unknown_word == default_unknown_word_if_None()
    assert x_ideabridge.otx_wall == default_wall_if_None()
    assert x_ideabridge.inx_wall == default_wall_if_None()


def test_ideabridge_shop_ReturnsObj_scenario1_WithParameters():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_unknown_word = "UnknownIdeaId"
    slash_otx_wall = "/"
    colon_inx_wall = ":"

    # WHEN
    x_ideabridge = ideabridge_shop(
        face_id=bob_str,
        event_id=event7,
        otx2inx=otx2inx,
        unknown_word=x_unknown_word,
        otx_wall=slash_otx_wall,
        inx_wall=colon_inx_wall,
    )

    # THEN
    assert x_ideabridge.face_id == bob_str
    assert x_ideabridge.event_id == event7
    assert x_ideabridge.otx2inx == otx2inx
    assert x_ideabridge.unknown_word == x_unknown_word
    assert x_ideabridge.otx_wall == slash_otx_wall
    assert x_ideabridge.inx_wall == colon_inx_wall


def test_ideabridge_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_ideabridge = ideabridge_shop(
        face_id=bob_str,
        event_id=event7,
        otx2inx=otx2inx,
        unknown_word=x_nan,
        otx_wall=x_nan,
        inx_wall=x_nan,
    )

    # THEN
    assert x_ideabridge.face_id == bob_str
    assert x_ideabridge.event_id == event7
    assert x_ideabridge.otx2inx == otx2inx
    assert x_ideabridge.unknown_word == default_unknown_word_if_None()
    assert x_ideabridge.otx_wall == default_wall_if_None()
    assert x_ideabridge.inx_wall == default_wall_if_None()


def test_IdeaBridge_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_ideabridge = ideabridge_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_ideabridge.otx2inx != x_otx2inx

    # WHEN
    x_ideabridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_ideabridge.otx2inx == x_otx2inx


def test_IdeaBridge_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownIdeaId"
    x_ideabridge = ideabridge_shop(None, unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_ideabridge.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ideabridge.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_IdeaBridge_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownIdeaId"
    x_ideabridge = ideabridge_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_ideabridge.otx2inx != x_otx2inx

    # WHEN
    x_ideabridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_ideabridge.otx2inx == x_otx2inx


def test_IdeaBridge_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ideabridge = ideabridge_shop(None)
    assert x_ideabridge.otx2inx == {}

    # WHEN
    x_ideabridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideabridge.otx2inx == {xio_str: sue_str}


def test_IdeaBridge_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ideabridge = ideabridge_shop(None)
    assert x_ideabridge._get_inx_value(xio_str) != sue_str

    # WHEN
    x_ideabridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideabridge._get_inx_value(xio_str) == sue_str


def test_IdeaBridge_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ideabridge = ideabridge_shop(None)
    assert x_ideabridge.otx2inx_exists(xio_str, sue_str) is False
    assert x_ideabridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_ideabridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_ideabridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_ideabridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideabridge.otx2inx_exists(xio_str, sue_str)
    assert x_ideabridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_ideabridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_ideabridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_ideabridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_ideabridge.otx2inx_exists(xio_str, sue_str)
    assert x_ideabridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_ideabridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_ideabridge.otx2inx_exists(zia_str, zia_str)


def test_IdeaBridge_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ideabridge = ideabridge_shop(None)
    assert x_ideabridge.otx_exists(xio_str) is False
    assert x_ideabridge.otx_exists(sue_str) is False
    assert x_ideabridge.otx_exists(bob_str) is False
    assert x_ideabridge.otx_exists(zia_str) is False

    # WHEN
    x_ideabridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideabridge.otx_exists(xio_str)
    assert x_ideabridge.otx_exists(sue_str) is False
    assert x_ideabridge.otx_exists(bob_str) is False
    assert x_ideabridge.otx_exists(zia_str) is False

    # WHEN
    x_ideabridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_ideabridge.otx_exists(xio_str)
    assert x_ideabridge.otx_exists(sue_str) is False
    assert x_ideabridge.otx_exists(bob_str) is False
    assert x_ideabridge.otx_exists(zia_str)


def test_IdeaBridge_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ideabridge = ideabridge_shop(None)
    x_ideabridge.set_otx2inx(xio_str, sue_str)
    assert x_ideabridge.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_ideabridge.del_otx2inx(xio_str)

    # THEN
    assert x_ideabridge.otx2inx_exists(xio_str, sue_str) is False


def test_IdeaBridge_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownIdeaId"
    x_ideabridge = ideabridge_shop(None, unknown_word=x_unknown_word)
    x_ideabridge.set_otx2inx(xio_str, sue_str)
    assert x_ideabridge._unknown_word_in_otx2inx() is False

    # WHEN
    x_ideabridge.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_ideabridge._unknown_word_in_otx2inx()


def test_IdeaBridge_reveal_inx_ReturnsObjAndSetsAttr_idea():
    # ESTABLISH
    inx_r_wall = ":"
    otx_r_wall = "/"
    swim_otx = f"swim{otx_r_wall}"
    climb_otx = f"climb{otx_r_wall}_{inx_r_wall}"
    x_ideabridge = ideabridge_shop(otx_wall=otx_r_wall, inx_wall=inx_r_wall)
    x_ideabridge.otx_exists(swim_otx) is False
    x_ideabridge.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_wall}"
    assert x_ideabridge.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_ideabridge.otx_exists(swim_otx)
    assert x_ideabridge.otx_exists(climb_otx) is False
    assert x_ideabridge._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_ideabridge.reveal_inx(climb_otx) is None
    # THEN
    assert x_ideabridge.otx_exists(swim_otx)
    assert x_ideabridge.otx_exists(climb_otx) is False


def test_IdeaBridge_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    event7 = 7
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    x_ideabridge = ideabridge_shop(
        sue_str,
        otx_wall=slash_otx_wall,
        inx_wall=colon_inx_wall,
    )
    x1_road_bridge_dict = {
        "otx_wall": x_ideabridge.otx_wall,
        "inx_wall": x_ideabridge.inx_wall,
        "unknown_word": x_ideabridge.unknown_word,
        "otx2inx": {},
        "face_id": x_ideabridge.face_id,
        "event_id": x_ideabridge.event_id,
    }
    assert x_ideabridge.get_dict() == x1_road_bridge_dict

    # WHEN
    x_ideabridge.set_otx2inx(clean_otx, clean_inx)
    x_ideabridge.event_id = event7
    # THEN
    x2_road_bridge_dict = {
        "otx_wall": x_ideabridge.otx_wall,
        "inx_wall": x_ideabridge.inx_wall,
        "unknown_word": x_ideabridge.unknown_word,
        "otx2inx": {clean_otx: clean_inx},
        "face_id": sue_str,
        "event_id": event7,
    }
    assert x_ideabridge.get_dict() == x2_road_bridge_dict


def test_IdeaBridge_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_wall = "/"
    x_ideabridge = ideabridge_shop(sue_str, otx_wall=slash_otx_wall)
    x1_road_bridge_json = f"""{{
  "event_id": 0,
  "face_id": "{sue_str}",
  "inx_wall": "{x_ideabridge.inx_wall}",
  "otx2inx": {{}},
  "otx_wall": "{x_ideabridge.otx_wall}",
  "unknown_word": "{x_ideabridge.unknown_word}"
}}"""
    print(f"           {x1_road_bridge_json=}")
    print(f"{x_ideabridge.get_json()=}")
    assert x_ideabridge.get_json() == x1_road_bridge_json

    # WHEN
    event7 = 7
    x_ideabridge.set_otx2inx(clean_otx, clean_inx)
    x_ideabridge.event_id = event7
    # THEN
    x2_road_bridge_json = f"""{{
  "event_id": {event7},
  "face_id": "{sue_str}",
  "inx_wall": "{x_ideabridge.inx_wall}",
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_wall": "{x_ideabridge.otx_wall}",
  "unknown_word": "{x_ideabridge.unknown_word}"
}}"""
    print(f"           {x2_road_bridge_json=}")
    print(f"{x_ideabridge.get_json()=}")
    assert x_ideabridge.get_json() == x2_road_bridge_json


def test_get_ideabridge_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_wall = "/"
    x_ideabridge = ideabridge_shop(sue_str, event7, otx_wall=slash_otx_wall)
    x_ideabridge.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_ideabridge = get_ideabridge_from_dict(x_ideabridge.get_dict())

    # THEN
    assert gen_ideabridge.face_id == x_ideabridge.face_id
    assert gen_ideabridge.event_id == x_ideabridge.event_id
    assert gen_ideabridge.event_id == event7
    assert gen_ideabridge == x_ideabridge


def test_get_ideabridge_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    x_ideabridge = ideabridge_shop(slash_otx_wall)
    x_ideabridge.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_ideabridge = get_ideabridge_from_json(x_ideabridge.get_json())

    # THEN
    assert x_ideabridge == x_ideabridge


def test_IdeaBridge_is_inx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_wall = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_ideabridge = ideabridge_shop(inx_wall=inx_wall)
    assert x_ideabridge._is_inx_wall_inclusion_correct()

    # WHEN
    x_ideabridge.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_ideabridge._is_inx_wall_inclusion_correct()

    # WHEN
    x_ideabridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_ideabridge._is_inx_wall_inclusion_correct() is False


def test_IdeaBridge_is_otx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_wall = "/"
    zia_otx = f"Zia{otx_wall}"
    zia_inx = "Zia"
    x_ideabridge = ideabridge_shop(otx_wall=otx_wall)
    assert x_ideabridge._is_otx_wall_inclusion_correct()

    # WHEN
    x_ideabridge.set_otx2inx(xio_otx, xio_inx)
    # THEN
    assert x_ideabridge._is_otx_wall_inclusion_correct()

    # WHEN
    x_ideabridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_ideabridge._is_otx_wall_inclusion_correct() is False


def test_IdeaBridge_is_valid_ReturnsObj():
    # ESTABLISH
    otx_wall = ":"
    inx_wall = "/"
    sue_otx = f"Xio{otx_wall}"
    sue_with_wall = f"Sue{inx_wall}"
    sue_without_wall = f"Sue{otx_wall}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_ideabridge = ideabridge_shop(otx_wall=otx_wall, inx_wall=inx_wall)
    assert x_ideabridge.is_valid()

    # WHEN
    x_ideabridge.set_otx2inx(sue_otx, sue_with_wall)
    # THEN
    assert x_ideabridge.is_valid() is False

    # WHEN
    x_ideabridge.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_ideabridge.is_valid() is False

    # WHEN
    x_ideabridge.set_otx2inx(sue_otx, sue_without_wall)
    # THEN
    assert x_ideabridge.is_valid() is False


def test_inherit_ideabridge_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_ideabridge = ideabridge_shop(zia_str, 3)
    new_ideabridge = ideabridge_shop(zia_str, 5)
    # WHEN
    inherit_ideabridge(new_ideabridge, old_ideabridge)

    # THEN
    assert new_ideabridge
    assert new_ideabridge == ideabridge_shop(zia_str, 5)


def test_inherit_ideabridge_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_wall():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_wall = "/"
    old_ideabridge = ideabridge_shop(sue_str, 0, otx_wall=slash_otx_wall)
    new_ideabridge = ideabridge_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideabridge(new_ideabridge, old_ideabridge)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideabridge_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_wall():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_wall = "/"
    old_ideabridge = ideabridge_shop(sue_str, 0, inx_wall=slash_otx_wall)
    new_ideabridge = ideabridge_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideabridge(new_ideabridge, old_ideabridge)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideabridge_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_word():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    old_ideabridge = ideabridge_shop(sue_str, 0, unknown_word=x_unknown_word)
    new_ideabridge = ideabridge_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideabridge(new_ideabridge, old_ideabridge)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideabridge_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_id():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_ideabridge = ideabridge_shop(sue_str, 0)
    new_ideabridge = ideabridge_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideabridge(new_ideabridge, old_ideabridge)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideabridge_ReturnsObj_Scenario5_RaiseErrorWhenEventIDsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_ideabridge = ideabridge_shop(sue_str, 5)
    new_ideabridge = ideabridge_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideabridge(new_ideabridge, old_ideabridge)
    assert str(excinfo.value) == "older bridgeunit is not older"


def test_inherit_ideabridge_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_ideabridge = ideabridge_shop(zia_str, 3)
    old_ideabridge.set_otx2inx(xio_otx, xio_inx)
    new_ideabridge = ideabridge_shop(zia_str, 7)
    assert new_ideabridge.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_ideabridge = inherit_ideabridge(new_ideabridge, old_ideabridge)

    # THEN
    assert inherited_ideabridge.otx2inx_exists(xio_otx, xio_inx)
