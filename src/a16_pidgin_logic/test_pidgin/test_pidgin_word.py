from src.a01_way_logic.way import default_bridge_if_None
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    otx_bridge_str,
    inx_bridge_str,
    unknown_term_str,
    otx2inx_str,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_term_if_None
from src.a16_pidgin_logic.map import (
    WordMap,
    wordmap_shop,
    get_wordmap_from_dict,
    get_wordmap_from_json,
    inherit_wordmap,
)
from pytest import raises as pytest_raises


def test_WordMap_Exists():
    # ESTABLISH
    x_wordmap = WordMap()

    # WHEN / THEN
    assert not x_wordmap.face_name
    assert not x_wordmap.event_int
    assert not x_wordmap.otx2inx
    assert not x_wordmap.unknown_term
    assert not x_wordmap.otx_bridge
    assert not x_wordmap.inx_bridge


def test_wordmap_shop_ReturnsObj_scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_wordmap = wordmap_shop()

    # THEN
    assert not x_wordmap.face_name
    assert x_wordmap.event_int == 0
    assert x_wordmap.otx2inx == {}
    assert x_wordmap.unknown_term == default_unknown_term_if_None()
    assert x_wordmap.otx_bridge == default_bridge_if_None()
    assert x_wordmap.inx_bridge == default_bridge_if_None()


def test_wordmap_shop_ReturnsObj_scenario1_WithParameters():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_unknown_term = "UnknownWordId"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"

    # WHEN
    x_wordmap = wordmap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_term=x_unknown_term,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )

    # THEN
    assert x_wordmap.face_name == bob_str
    assert x_wordmap.event_int == event7
    assert x_wordmap.otx2inx == otx2inx
    assert x_wordmap.unknown_term == x_unknown_term
    assert x_wordmap.otx_bridge == slash_otx_bridge
    assert x_wordmap.inx_bridge == colon_inx_bridge


def test_wordmap_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_wordmap = wordmap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_term=x_nan,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
    )

    # THEN
    assert x_wordmap.face_name == bob_str
    assert x_wordmap.event_int == event7
    assert x_wordmap.otx2inx == otx2inx
    assert x_wordmap.unknown_term == default_unknown_term_if_None()
    assert x_wordmap.otx_bridge == default_bridge_if_None()
    assert x_wordmap.inx_bridge == default_bridge_if_None()


def test_WordMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_wordmap = wordmap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_wordmap.otx2inx != x_otx2inx

    # WHEN
    x_wordmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_wordmap.otx2inx == x_otx2inx


def test_WordMap_set_all_otx2inx_RaisesErrorIf_unknown_term_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_term = "UnknownWordId"
    x_wordmap = wordmap_shop(None, unknown_term=x_unknown_term)
    x_otx2inx = {xio_str: sue_str, x_unknown_term: zia_str}
    assert x_wordmap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_wordmap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_term '{x_unknown_term}' in any str. Affected keys include ['{x_unknown_term}']."
    assert str(excinfo.value) == exception_str


def test_WordMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_term = "UnknownWordId"
    x_wordmap = wordmap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_term: zia_str}
    assert x_wordmap.otx2inx != x_otx2inx

    # WHEN
    x_wordmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_wordmap.otx2inx == x_otx2inx


def test_WordMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_wordmap = wordmap_shop(None)
    assert x_wordmap.otx2inx == {}

    # WHEN
    x_wordmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_wordmap.otx2inx == {xio_str: sue_str}


def test_WordMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_wordmap = wordmap_shop(None)
    assert x_wordmap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_wordmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_wordmap._get_inx_value(xio_str) == sue_str


def test_WordMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_wordmap = wordmap_shop(None)
    assert x_wordmap.otx2inx_exists(xio_str, sue_str) is False
    assert x_wordmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_wordmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_wordmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_wordmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_wordmap.otx2inx_exists(xio_str, sue_str)
    assert x_wordmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_wordmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_wordmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_wordmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_wordmap.otx2inx_exists(xio_str, sue_str)
    assert x_wordmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_wordmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_wordmap.otx2inx_exists(zia_str, zia_str)


def test_WordMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_wordmap = wordmap_shop(None)
    assert x_wordmap.otx_exists(xio_str) is False
    assert x_wordmap.otx_exists(sue_str) is False
    assert x_wordmap.otx_exists(bob_str) is False
    assert x_wordmap.otx_exists(zia_str) is False

    # WHEN
    x_wordmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_wordmap.otx_exists(xio_str)
    assert x_wordmap.otx_exists(sue_str) is False
    assert x_wordmap.otx_exists(bob_str) is False
    assert x_wordmap.otx_exists(zia_str) is False

    # WHEN
    x_wordmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_wordmap.otx_exists(xio_str)
    assert x_wordmap.otx_exists(sue_str) is False
    assert x_wordmap.otx_exists(bob_str) is False
    assert x_wordmap.otx_exists(zia_str)


def test_WordMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_wordmap = wordmap_shop(None)
    x_wordmap.set_otx2inx(xio_str, sue_str)
    assert x_wordmap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_wordmap.del_otx2inx(xio_str)

    # THEN
    assert x_wordmap.otx2inx_exists(xio_str, sue_str) is False


def test_WordMap_unknown_term_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_term = "UnknownWordId"
    x_wordmap = wordmap_shop(None, unknown_term=x_unknown_term)
    x_wordmap.set_otx2inx(xio_str, sue_str)
    assert x_wordmap._unknown_term_in_otx2inx() is False

    # WHEN
    x_wordmap.set_otx2inx(zia_str, x_unknown_term)

    # THEN
    assert x_wordmap._unknown_term_in_otx2inx()


def test_WordMap_reveal_inx_ReturnsObjAndSetsAttr_word():
    # ESTABLISH
    inx_r_bridge = ":"
    otx_r_bridge = "/"
    swim_otx = f"swim{otx_r_bridge}"
    climb_otx = f"climb{otx_r_bridge}_{inx_r_bridge}"
    x_wordmap = wordmap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    x_wordmap.otx_exists(swim_otx) is False
    x_wordmap.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_bridge}"
    assert x_wordmap.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_wordmap.otx_exists(swim_otx)
    assert x_wordmap.otx_exists(climb_otx) is False
    assert x_wordmap._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_wordmap.reveal_inx(climb_otx) is None
    # THEN
    assert x_wordmap.otx_exists(swim_otx)
    assert x_wordmap.otx_exists(climb_otx) is False


def test_WordMap_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    event7 = 7
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    x_wordmap = wordmap_shop(
        sue_str,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )
    x1_way_map_dict = {
        otx_bridge_str(): x_wordmap.otx_bridge,
        inx_bridge_str(): x_wordmap.inx_bridge,
        unknown_term_str(): x_wordmap.unknown_term,
        otx2inx_str(): {},
        face_name_str(): x_wordmap.face_name,
        event_int_str(): x_wordmap.event_int,
    }
    assert x_wordmap.get_dict() == x1_way_map_dict

    # WHEN
    x_wordmap.set_otx2inx(clean_otx, clean_inx)
    x_wordmap.event_int = event7
    # THEN
    x2_way_map_dict = {
        otx_bridge_str(): x_wordmap.otx_bridge,
        inx_bridge_str(): x_wordmap.inx_bridge,
        unknown_term_str(): x_wordmap.unknown_term,
        otx2inx_str(): {clean_otx: clean_inx},
        face_name_str(): sue_str,
        event_int_str(): event7,
    }
    assert x_wordmap.get_dict() == x2_way_map_dict


def test_WordMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_bridge = "/"
    x_wordmap = wordmap_shop(sue_str, otx_bridge=slash_otx_bridge)
    x1_way_map_json = f"""{{
  "{event_int_str()}": 0,
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_wordmap.inx_bridge}",
  "{otx2inx_str()}": {{}},
  "{otx_bridge_str()}": "{x_wordmap.otx_bridge}",
  "{unknown_term_str()}": "{x_wordmap.unknown_term}"
}}"""
    print(f"           {x1_way_map_json=}")
    print(f"{x_wordmap.get_json()=}")
    assert x_wordmap.get_json() == x1_way_map_json

    # WHEN
    event7 = 7
    x_wordmap.set_otx2inx(clean_otx, clean_inx)
    x_wordmap.event_int = event7
    # THEN
    x2_way_map_json = f"""{{
  "{event_int_str()}": {event7},
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_wordmap.inx_bridge}",
  "{otx2inx_str()}": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "{otx_bridge_str()}": "{x_wordmap.otx_bridge}",
  "{unknown_term_str()}": "{x_wordmap.unknown_term}"
}}"""
    print(f"           {x2_way_map_json=}")
    print(f"{x_wordmap.get_json()=}")
    assert x_wordmap.get_json() == x2_way_map_json


def test_get_wordmap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_bridge = "/"
    x_wordmap = wordmap_shop(sue_str, event7, otx_bridge=slash_otx_bridge)
    x_wordmap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_wordmap = get_wordmap_from_dict(x_wordmap.get_dict())

    # THEN
    assert gen_wordmap.face_name == x_wordmap.face_name
    assert gen_wordmap.event_int == x_wordmap.event_int
    assert gen_wordmap.event_int == event7
    assert gen_wordmap == x_wordmap


def test_get_wordmap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_bridge = "/"
    x_wordmap = wordmap_shop(slash_otx_bridge)
    x_wordmap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_wordmap = get_wordmap_from_json(x_wordmap.get_json())

    # THEN
    assert x_wordmap == x_wordmap


def test_WordMap_is_inx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_bridge = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_wordmap = wordmap_shop(inx_bridge=inx_bridge)
    assert x_wordmap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_wordmap.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_wordmap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_wordmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_wordmap._is_inx_bridge_inclusion_correct() is False


def test_WordMap_is_otx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_bridge = "/"
    zia_otx = f"Zia{otx_bridge}"
    zia_inx = "Zia"
    x_wordmap = wordmap_shop(otx_bridge=otx_bridge)
    assert x_wordmap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_wordmap.set_otx2inx(xio_otx, xio_inx)
    # THEN
    assert x_wordmap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_wordmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_wordmap._is_otx_bridge_inclusion_correct() is False


def test_WordMap_is_valid_ReturnsObj():
    # ESTABLISH
    otx_bridge = ":"
    inx_bridge = "/"
    sue_otx = f"Xio{otx_bridge}"
    sue_with_bridge = f"Sue{inx_bridge}"
    sue_without_bridge = f"Sue{otx_bridge}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_wordmap = wordmap_shop(otx_bridge=otx_bridge, inx_bridge=inx_bridge)
    assert x_wordmap.is_valid()

    # WHEN
    x_wordmap.set_otx2inx(sue_otx, sue_with_bridge)
    # THEN
    assert x_wordmap.is_valid() is False

    # WHEN
    x_wordmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_wordmap.is_valid() is False

    # WHEN
    x_wordmap.set_otx2inx(sue_otx, sue_without_bridge)
    # THEN
    assert x_wordmap.is_valid() is False


def test_inherit_wordmap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_wordmap = wordmap_shop(zia_str, 3)
    new_wordmap = wordmap_shop(zia_str, 5)
    # WHEN
    inherit_wordmap(new_wordmap, old_wordmap)

    # THEN
    assert new_wordmap
    assert new_wordmap == wordmap_shop(zia_str, 5)


def test_inherit_wordmap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_wordmap = wordmap_shop(sue_str, 0, otx_bridge=slash_otx_bridge)
    new_wordmap = wordmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_wordmap(new_wordmap, old_wordmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_wordmap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_wordmap = wordmap_shop(sue_str, 0, inx_bridge=slash_otx_bridge)
    new_wordmap = wordmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_wordmap(new_wordmap, old_wordmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_wordmap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_term():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_term = "UnknownTerm"
    old_wordmap = wordmap_shop(sue_str, 0, unknown_term=x_unknown_term)
    new_wordmap = wordmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_wordmap(new_wordmap, old_wordmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_wordmap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_wordmap = wordmap_shop(sue_str, 0)
    new_wordmap = wordmap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_wordmap(new_wordmap, old_wordmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_wordmap_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_wordmap = wordmap_shop(sue_str, 5)
    new_wordmap = wordmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_wordmap(new_wordmap, old_wordmap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_wordmap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_wordmap = wordmap_shop(zia_str, 3)
    old_wordmap.set_otx2inx(xio_otx, xio_inx)
    new_wordmap = wordmap_shop(zia_str, 7)
    assert new_wordmap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_wordmap = inherit_wordmap(new_wordmap, old_wordmap)

    # THEN
    assert inherited_wordmap.otx2inx_exists(xio_otx, xio_inx)
