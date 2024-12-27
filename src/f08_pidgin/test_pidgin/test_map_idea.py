from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_wall_if_None
from src.f08_pidgin.map import (
    IdeaMap,
    ideamap_shop,
    get_ideamap_from_dict,
    get_ideamap_from_json,
    inherit_ideamap,
)
from pytest import raises as pytest_raises


def test_IdeaMap_Exists():
    # ESTABLISH
    x_ideamap = IdeaMap()

    # WHEN / THEN
    assert not x_ideamap.face_id
    assert not x_ideamap.event_id
    assert not x_ideamap.otx2inx
    assert not x_ideamap.unknown_word
    assert not x_ideamap.otx_wall
    assert not x_ideamap.inx_wall


def test_ideamap_shop_ReturnsObj_scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_ideamap = ideamap_shop()

    # THEN
    assert not x_ideamap.face_id
    assert x_ideamap.event_id == 0
    assert x_ideamap.otx2inx == {}
    assert x_ideamap.unknown_word == default_unknown_word_if_None()
    assert x_ideamap.otx_wall == default_wall_if_None()
    assert x_ideamap.inx_wall == default_wall_if_None()


def test_ideamap_shop_ReturnsObj_scenario1_WithParameters():
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
    x_ideamap = ideamap_shop(
        face_id=bob_str,
        event_id=event7,
        otx2inx=otx2inx,
        unknown_word=x_unknown_word,
        otx_wall=slash_otx_wall,
        inx_wall=colon_inx_wall,
    )

    # THEN
    assert x_ideamap.face_id == bob_str
    assert x_ideamap.event_id == event7
    assert x_ideamap.otx2inx == otx2inx
    assert x_ideamap.unknown_word == x_unknown_word
    assert x_ideamap.otx_wall == slash_otx_wall
    assert x_ideamap.inx_wall == colon_inx_wall


def test_ideamap_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_ideamap = ideamap_shop(
        face_id=bob_str,
        event_id=event7,
        otx2inx=otx2inx,
        unknown_word=x_nan,
        otx_wall=x_nan,
        inx_wall=x_nan,
    )

    # THEN
    assert x_ideamap.face_id == bob_str
    assert x_ideamap.event_id == event7
    assert x_ideamap.otx2inx == otx2inx
    assert x_ideamap.unknown_word == default_unknown_word_if_None()
    assert x_ideamap.otx_wall == default_wall_if_None()
    assert x_ideamap.inx_wall == default_wall_if_None()


def test_IdeaMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_ideamap = ideamap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_ideamap.otx2inx != x_otx2inx

    # WHEN
    x_ideamap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_ideamap.otx2inx == x_otx2inx


def test_IdeaMap_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownIdeaId"
    x_ideamap = ideamap_shop(None, unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_ideamap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ideamap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_IdeaMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownIdeaId"
    x_ideamap = ideamap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_ideamap.otx2inx != x_otx2inx

    # WHEN
    x_ideamap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_ideamap.otx2inx == x_otx2inx


def test_IdeaMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ideamap = ideamap_shop(None)
    assert x_ideamap.otx2inx == {}

    # WHEN
    x_ideamap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideamap.otx2inx == {xio_str: sue_str}


def test_IdeaMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ideamap = ideamap_shop(None)
    assert x_ideamap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_ideamap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideamap._get_inx_value(xio_str) == sue_str


def test_IdeaMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ideamap = ideamap_shop(None)
    assert x_ideamap.otx2inx_exists(xio_str, sue_str) is False
    assert x_ideamap.otx2inx_exists(xio_str, zia_str) is False
    assert x_ideamap.otx2inx_exists(xio_str, bob_str) is False
    assert x_ideamap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_ideamap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideamap.otx2inx_exists(xio_str, sue_str)
    assert x_ideamap.otx2inx_exists(xio_str, zia_str) is False
    assert x_ideamap.otx2inx_exists(xio_str, bob_str) is False
    assert x_ideamap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_ideamap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_ideamap.otx2inx_exists(xio_str, sue_str)
    assert x_ideamap.otx2inx_exists(xio_str, zia_str) is False
    assert x_ideamap.otx2inx_exists(xio_str, bob_str) is False
    assert x_ideamap.otx2inx_exists(zia_str, zia_str)


def test_IdeaMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ideamap = ideamap_shop(None)
    assert x_ideamap.otx_exists(xio_str) is False
    assert x_ideamap.otx_exists(sue_str) is False
    assert x_ideamap.otx_exists(bob_str) is False
    assert x_ideamap.otx_exists(zia_str) is False

    # WHEN
    x_ideamap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ideamap.otx_exists(xio_str)
    assert x_ideamap.otx_exists(sue_str) is False
    assert x_ideamap.otx_exists(bob_str) is False
    assert x_ideamap.otx_exists(zia_str) is False

    # WHEN
    x_ideamap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_ideamap.otx_exists(xio_str)
    assert x_ideamap.otx_exists(sue_str) is False
    assert x_ideamap.otx_exists(bob_str) is False
    assert x_ideamap.otx_exists(zia_str)


def test_IdeaMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ideamap = ideamap_shop(None)
    x_ideamap.set_otx2inx(xio_str, sue_str)
    assert x_ideamap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_ideamap.del_otx2inx(xio_str)

    # THEN
    assert x_ideamap.otx2inx_exists(xio_str, sue_str) is False


def test_IdeaMap_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownIdeaId"
    x_ideamap = ideamap_shop(None, unknown_word=x_unknown_word)
    x_ideamap.set_otx2inx(xio_str, sue_str)
    assert x_ideamap._unknown_word_in_otx2inx() is False

    # WHEN
    x_ideamap.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_ideamap._unknown_word_in_otx2inx()


def test_IdeaMap_reveal_inx_ReturnsObjAndSetsAttr_idea():
    # ESTABLISH
    inx_r_wall = ":"
    otx_r_wall = "/"
    swim_otx = f"swim{otx_r_wall}"
    climb_otx = f"climb{otx_r_wall}_{inx_r_wall}"
    x_ideamap = ideamap_shop(otx_wall=otx_r_wall, inx_wall=inx_r_wall)
    x_ideamap.otx_exists(swim_otx) is False
    x_ideamap.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_wall}"
    assert x_ideamap.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_ideamap.otx_exists(swim_otx)
    assert x_ideamap.otx_exists(climb_otx) is False
    assert x_ideamap._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_ideamap.reveal_inx(climb_otx) is None
    # THEN
    assert x_ideamap.otx_exists(swim_otx)
    assert x_ideamap.otx_exists(climb_otx) is False


def test_IdeaMap_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    event7 = 7
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    x_ideamap = ideamap_shop(
        sue_str,
        otx_wall=slash_otx_wall,
        inx_wall=colon_inx_wall,
    )
    x1_road_map_dict = {
        "otx_wall": x_ideamap.otx_wall,
        "inx_wall": x_ideamap.inx_wall,
        "unknown_word": x_ideamap.unknown_word,
        "otx2inx": {},
        "face_id": x_ideamap.face_id,
        "event_id": x_ideamap.event_id,
    }
    assert x_ideamap.get_dict() == x1_road_map_dict

    # WHEN
    x_ideamap.set_otx2inx(clean_otx, clean_inx)
    x_ideamap.event_id = event7
    # THEN
    x2_road_map_dict = {
        "otx_wall": x_ideamap.otx_wall,
        "inx_wall": x_ideamap.inx_wall,
        "unknown_word": x_ideamap.unknown_word,
        "otx2inx": {clean_otx: clean_inx},
        "face_id": sue_str,
        "event_id": event7,
    }
    assert x_ideamap.get_dict() == x2_road_map_dict


def test_IdeaMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_wall = "/"
    x_ideamap = ideamap_shop(sue_str, otx_wall=slash_otx_wall)
    x1_road_map_json = f"""{{
  "event_id": 0,
  "face_id": "{sue_str}",
  "inx_wall": "{x_ideamap.inx_wall}",
  "otx2inx": {{}},
  "otx_wall": "{x_ideamap.otx_wall}",
  "unknown_word": "{x_ideamap.unknown_word}"
}}"""
    print(f"           {x1_road_map_json=}")
    print(f"{x_ideamap.get_json()=}")
    assert x_ideamap.get_json() == x1_road_map_json

    # WHEN
    event7 = 7
    x_ideamap.set_otx2inx(clean_otx, clean_inx)
    x_ideamap.event_id = event7
    # THEN
    x2_road_map_json = f"""{{
  "event_id": {event7},
  "face_id": "{sue_str}",
  "inx_wall": "{x_ideamap.inx_wall}",
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_wall": "{x_ideamap.otx_wall}",
  "unknown_word": "{x_ideamap.unknown_word}"
}}"""
    print(f"           {x2_road_map_json=}")
    print(f"{x_ideamap.get_json()=}")
    assert x_ideamap.get_json() == x2_road_map_json


def test_get_ideamap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_wall = "/"
    x_ideamap = ideamap_shop(sue_str, event7, otx_wall=slash_otx_wall)
    x_ideamap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_ideamap = get_ideamap_from_dict(x_ideamap.get_dict())

    # THEN
    assert gen_ideamap.face_id == x_ideamap.face_id
    assert gen_ideamap.event_id == x_ideamap.event_id
    assert gen_ideamap.event_id == event7
    assert gen_ideamap == x_ideamap


def test_get_ideamap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    x_ideamap = ideamap_shop(slash_otx_wall)
    x_ideamap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_ideamap = get_ideamap_from_json(x_ideamap.get_json())

    # THEN
    assert x_ideamap == x_ideamap


def test_IdeaMap_is_inx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_wall = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_ideamap = ideamap_shop(inx_wall=inx_wall)
    assert x_ideamap._is_inx_wall_inclusion_correct()

    # WHEN
    x_ideamap.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_ideamap._is_inx_wall_inclusion_correct()

    # WHEN
    x_ideamap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_ideamap._is_inx_wall_inclusion_correct() is False


def test_IdeaMap_is_otx_wall_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_wall = "/"
    zia_otx = f"Zia{otx_wall}"
    zia_inx = "Zia"
    x_ideamap = ideamap_shop(otx_wall=otx_wall)
    assert x_ideamap._is_otx_wall_inclusion_correct()

    # WHEN
    x_ideamap.set_otx2inx(xio_otx, xio_inx)
    # THEN
    assert x_ideamap._is_otx_wall_inclusion_correct()

    # WHEN
    x_ideamap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_ideamap._is_otx_wall_inclusion_correct() is False


def test_IdeaMap_is_valid_ReturnsObj():
    # ESTABLISH
    otx_wall = ":"
    inx_wall = "/"
    sue_otx = f"Xio{otx_wall}"
    sue_with_wall = f"Sue{inx_wall}"
    sue_without_wall = f"Sue{otx_wall}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_wall}"
    x_ideamap = ideamap_shop(otx_wall=otx_wall, inx_wall=inx_wall)
    assert x_ideamap.is_valid()

    # WHEN
    x_ideamap.set_otx2inx(sue_otx, sue_with_wall)
    # THEN
    assert x_ideamap.is_valid() is False

    # WHEN
    x_ideamap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_ideamap.is_valid() is False

    # WHEN
    x_ideamap.set_otx2inx(sue_otx, sue_without_wall)
    # THEN
    assert x_ideamap.is_valid() is False


def test_inherit_ideamap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_ideamap = ideamap_shop(zia_str, 3)
    new_ideamap = ideamap_shop(zia_str, 5)
    # WHEN
    inherit_ideamap(new_ideamap, old_ideamap)

    # THEN
    assert new_ideamap
    assert new_ideamap == ideamap_shop(zia_str, 5)


def test_inherit_ideamap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_wall():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_wall = "/"
    old_ideamap = ideamap_shop(sue_str, 0, otx_wall=slash_otx_wall)
    new_ideamap = ideamap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideamap(new_ideamap, old_ideamap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideamap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_wall():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_wall = "/"
    old_ideamap = ideamap_shop(sue_str, 0, inx_wall=slash_otx_wall)
    new_ideamap = ideamap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideamap(new_ideamap, old_ideamap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideamap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_word():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    old_ideamap = ideamap_shop(sue_str, 0, unknown_word=x_unknown_word)
    new_ideamap = ideamap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideamap(new_ideamap, old_ideamap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideamap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_id():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_ideamap = ideamap_shop(sue_str, 0)
    new_ideamap = ideamap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideamap(new_ideamap, old_ideamap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ideamap_ReturnsObj_Scenario5_RaiseErrorWhenEventIDsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_ideamap = ideamap_shop(sue_str, 5)
    new_ideamap = ideamap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ideamap(new_ideamap, old_ideamap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_ideamap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_ideamap = ideamap_shop(zia_str, 3)
    old_ideamap.set_otx2inx(xio_otx, xio_inx)
    new_ideamap = ideamap_shop(zia_str, 7)
    assert new_ideamap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_ideamap = inherit_ideamap(new_ideamap, old_ideamap)

    # THEN
    assert inherited_ideamap.otx2inx_exists(xio_otx, xio_inx)
