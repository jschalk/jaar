from pytest import raises as pytest_raises
from src.a01_term_logic.way import default_bridge_if_None
from src.a09_pack_logic._test_util.a09_str import event_int_str, face_name_str
from src.a16_pidgin_logic._test_util.a16_str import (
    inx_bridge_str,
    otx2inx_str,
    otx_bridge_str,
    unknown_str_str,
)
from src.a16_pidgin_logic.map import (
    TitleMap,
    get_titlemap_from_dict,
    get_titlemap_from_json,
    inherit_titlemap,
    titlemap_shop,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_str_if_None


def test_TitleMap_Exists():
    # ESTABLISH
    x_titlemap = TitleMap()

    # WHEN / THEN
    assert not x_titlemap.face_name
    assert not x_titlemap.event_int
    assert not x_titlemap.otx2inx
    assert not x_titlemap.unknown_str
    assert not x_titlemap.otx_bridge
    assert not x_titlemap.inx_bridge


def test_titlemap_shop_ReturnsObj_scenario0_NoParameters():
    # ESTABLISH / WHEN
    x_titlemap = titlemap_shop()

    # THEN
    assert not x_titlemap.face_name
    assert x_titlemap.event_int == 0
    assert x_titlemap.otx2inx == {}
    assert x_titlemap.unknown_str == default_unknown_str_if_None()
    assert x_titlemap.otx_bridge == default_bridge_if_None()
    assert x_titlemap.inx_bridge == default_bridge_if_None()


def test_titlemap_shop_ReturnsObj_scenario1_WithParameters():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_unknown_str = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"

    # WHEN
    x_titlemap = titlemap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_str=x_unknown_str,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )

    # THEN
    assert x_titlemap.face_name == bob_str
    assert x_titlemap.event_int == event7
    assert x_titlemap.otx2inx == otx2inx
    assert x_titlemap.unknown_str == x_unknown_str
    assert x_titlemap.otx_bridge == slash_otx_bridge
    assert x_titlemap.inx_bridge == colon_inx_bridge


def test_titlemap_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_titlemap = titlemap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_str=x_nan,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
    )

    # THEN
    assert x_titlemap.face_name == bob_str
    assert x_titlemap.event_int == event7
    assert x_titlemap.otx2inx == otx2inx
    assert x_titlemap.unknown_str == default_unknown_str_if_None()
    assert x_titlemap.otx_bridge == default_bridge_if_None()
    assert x_titlemap.inx_bridge == default_bridge_if_None()


def test_TitleMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_titlemap = titlemap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert x_titlemap.otx2inx != x_otx2inx

    # WHEN
    x_titlemap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_titlemap.otx2inx == x_otx2inx


def test_TitleMap_set_all_otx2inx_RaisesErrorIf_unknown_str_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    x_titlemap = titlemap_shop(unknown_str=x_unknown_str)
    x_otx2inx = {xio_str: sue_str, x_unknown_str: zia_str}
    assert x_titlemap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_titlemap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_str '{x_unknown_str}' in any str. Affected keys include ['{x_unknown_str}']."
    assert str(excinfo.value) == exception_str


def test_TitleMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    x_titlemap = titlemap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_str: zia_str}
    assert x_titlemap.otx2inx != x_otx2inx

    # WHEN
    x_titlemap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_titlemap.otx2inx == x_otx2inx


def test_TitleMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_titlemap = titlemap_shop(None)
    assert x_titlemap.otx2inx == {}

    # WHEN
    x_titlemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_titlemap.otx2inx == {xio_str: sue_str}


def test_TitleMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_titlemap = titlemap_shop(None)
    assert x_titlemap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_titlemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_titlemap._get_inx_value(xio_str) == sue_str


def test_TitleMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_titlemap = titlemap_shop(None)
    assert x_titlemap.otx2inx_exists(xio_str, sue_str) is False
    assert x_titlemap.otx2inx_exists(xio_str, zia_str) is False
    assert x_titlemap.otx2inx_exists(xio_str, bob_str) is False
    assert x_titlemap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_titlemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_titlemap.otx2inx_exists(xio_str, sue_str)
    assert x_titlemap.otx2inx_exists(xio_str, zia_str) is False
    assert x_titlemap.otx2inx_exists(xio_str, bob_str) is False
    assert x_titlemap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_titlemap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_titlemap.otx2inx_exists(xio_str, sue_str)
    assert x_titlemap.otx2inx_exists(xio_str, zia_str) is False
    assert x_titlemap.otx2inx_exists(xio_str, bob_str) is False
    assert x_titlemap.otx2inx_exists(zia_str, zia_str)


def test_TitleMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_titlemap = titlemap_shop(None)
    assert x_titlemap.otx_exists(xio_str) is False
    assert x_titlemap.otx_exists(sue_str) is False
    assert x_titlemap.otx_exists(bob_str) is False
    assert x_titlemap.otx_exists(zia_str) is False

    # WHEN
    x_titlemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_titlemap.otx_exists(xio_str)
    assert x_titlemap.otx_exists(sue_str) is False
    assert x_titlemap.otx_exists(bob_str) is False
    assert x_titlemap.otx_exists(zia_str) is False

    # WHEN
    x_titlemap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_titlemap.otx_exists(xio_str)
    assert x_titlemap.otx_exists(sue_str) is False
    assert x_titlemap.otx_exists(bob_str) is False
    assert x_titlemap.otx_exists(zia_str)


def test_TitleMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_titlemap = titlemap_shop(None)
    x_titlemap.set_otx2inx(xio_str, sue_str)
    assert x_titlemap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_titlemap.del_otx2inx(xio_str)

    # THEN
    assert x_titlemap.otx2inx_exists(xio_str, sue_str) is False


def test_TitleMap_unknown_str_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    x_titlemap = titlemap_shop(unknown_str=x_unknown_str)
    x_titlemap.set_otx2inx(xio_str, sue_str)
    assert x_titlemap._unknown_str_in_otx2inx() is False

    # WHEN
    x_titlemap.set_otx2inx(zia_str, x_unknown_str)

    # THEN
    assert x_titlemap._unknown_str_in_otx2inx()


def test_TitleMap_reveal_inx_ReturnsObjAndSetsAttr_group_title():
    # ESTABLISH
    inx_r_bridge = ":"
    otx_r_bridge = "/"
    swim_otx = f"swim{otx_r_bridge}"
    climb_otx = f"climb{otx_r_bridge}_{inx_r_bridge}"
    x_titlemap = titlemap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    x_titlemap.otx_exists(swim_otx) is False
    x_titlemap.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_bridge}"
    assert x_titlemap.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert x_titlemap.otx_exists(swim_otx)
    assert x_titlemap.otx_exists(climb_otx) is False
    assert x_titlemap._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert x_titlemap.reveal_inx(climb_otx) is None
    # THEN
    assert x_titlemap.otx_exists(swim_otx)
    assert x_titlemap.otx_exists(climb_otx) is False


def test_TitleMap_get_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    sue_str = "Sue"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    x_titlemap = titlemap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        face_name=sue_str,
    )
    x1_way_map_dict = {
        otx_bridge_str(): x_titlemap.otx_bridge,
        inx_bridge_str(): x_titlemap.inx_bridge,
        unknown_str_str(): x_titlemap.unknown_str,
        otx2inx_str(): {},
        event_int_str(): x_titlemap.event_int,
        face_name_str(): x_titlemap.face_name,
    }
    assert x_titlemap.get_dict() == x1_way_map_dict

    # WHEN
    x_titlemap.set_otx2inx(clean_otx, clean_inx)
    # THEN
    x2_way_map_dict = {
        otx_bridge_str(): x_titlemap.otx_bridge,
        inx_bridge_str(): x_titlemap.inx_bridge,
        unknown_str_str(): x_titlemap.unknown_str,
        otx2inx_str(): {clean_otx: clean_inx},
        event_int_str(): x_titlemap.event_int,
        face_name_str(): sue_str,
    }
    assert x_titlemap.get_dict() == x2_way_map_dict


def test_TitleMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    event7 = 7
    slash_otx_bridge = "/"
    x_titlemap = titlemap_shop(sue_str, otx_bridge=slash_otx_bridge)
    x1_way_map_json = f"""{{
  "{event_int_str()}": 0,
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_titlemap.inx_bridge}",
  "{otx2inx_str()}": {{}},
  "{otx_bridge_str()}": "{x_titlemap.otx_bridge}",
  "{unknown_str_str()}": "{x_titlemap.unknown_str}"
}}"""
    print(f"           {x1_way_map_json=}")
    print(f"{x_titlemap.get_json()=}")
    assert x_titlemap.get_json() == x1_way_map_json

    # WHEN
    x_titlemap.set_otx2inx(clean_otx, clean_inx)
    x_titlemap.event_int = event7
    # THEN
    x2_way_map_json = f"""{{
  "{event_int_str()}": {event7},
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_titlemap.inx_bridge}",
  "{otx2inx_str()}": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "{otx_bridge_str()}": "{x_titlemap.otx_bridge}",
  "{unknown_str_str()}": "{x_titlemap.unknown_str}"
}}"""
    print(f"           {x2_way_map_json=}")
    print(f"{x_titlemap.get_json()=}")
    assert x_titlemap.get_json() == x2_way_map_json


def test_get_titlemap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_bridge = "/"
    x_titlemap = titlemap_shop(sue_str, event7, otx_bridge=slash_otx_bridge)
    x_titlemap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_titlemap = get_titlemap_from_dict(x_titlemap.get_dict())

    # THEN
    assert gen_titlemap.face_name == x_titlemap.face_name
    assert gen_titlemap.event_int == x_titlemap.event_int
    assert gen_titlemap.event_int == event7
    assert gen_titlemap == x_titlemap


def test_get_titlemap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_bridge = "/"
    x_titlemap = titlemap_shop(slash_otx_bridge)
    x_titlemap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    x_titlemap = get_titlemap_from_json(x_titlemap.get_json())

    # THEN
    assert x_titlemap == x_titlemap


def test_TitleMap_is_inx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    inx_bridge = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_titlemap = titlemap_shop(inx_bridge=inx_bridge)
    assert x_titlemap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_titlemap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_titlemap._is_inx_bridge_inclusion_correct()

    # WHEN
    x_titlemap.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_titlemap._is_inx_bridge_inclusion_correct() is False


def test_TitleMap_is_otx_bridge_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    otx_bridge = "/"
    zia_inx = "Zia"
    zia_otx = f"Zia{otx_bridge}"
    x_titlemap = titlemap_shop(otx_bridge=otx_bridge)
    assert x_titlemap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_titlemap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_titlemap._is_otx_bridge_inclusion_correct()

    # WHEN
    x_titlemap.set_otx2inx(xio_str, sue_str)
    # THEN
    assert x_titlemap._is_otx_bridge_inclusion_correct() is False


def test_TitleMap_is_valid_ReturnsObj():
    # ESTABLISH
    otx_bridge = ":"
    inx_bridge = "/"
    sue_otx = f"Xio{otx_bridge}"
    sue_inx = f"Sue{inx_bridge}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_bridge}"
    x_titlemap = titlemap_shop(otx_bridge=otx_bridge, inx_bridge=inx_bridge)
    assert x_titlemap.is_valid()

    # WHEN
    x_titlemap.set_otx2inx(sue_otx, sue_inx)
    # THEN
    assert x_titlemap.is_valid()

    # WHEN
    x_titlemap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_titlemap.is_valid() is False


def test_inherit_titlemap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_titlemap = titlemap_shop(zia_str, 3)
    new_titlemap = titlemap_shop(zia_str, 5)
    # WHEN
    inherit_titlemap(new_titlemap, old_titlemap)

    # THEN
    assert new_titlemap
    assert new_titlemap == titlemap_shop(zia_str, 5)


def test_inherit_titlemap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_titlemap = titlemap_shop(sue_str, 0, otx_bridge=slash_otx_bridge)
    new_titlemap = titlemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_titlemap(new_titlemap, old_titlemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_titlemap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_titlemap = titlemap_shop(sue_str, 0, inx_bridge=slash_otx_bridge)
    new_titlemap = titlemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_titlemap(new_titlemap, old_titlemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_titlemap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    old_titlemap = titlemap_shop(sue_str, 0, unknown_str=x_unknown_str)
    new_titlemap = titlemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_titlemap(new_titlemap, old_titlemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_titlemap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_titlemap = titlemap_shop(sue_str, 0)
    new_titlemap = titlemap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_titlemap(new_titlemap, old_titlemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_titlemap_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_titlemap = titlemap_shop(sue_str, 5)
    new_titlemap = titlemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_titlemap(new_titlemap, old_titlemap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_titlemap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_titlemap = titlemap_shop(zia_str, 3)
    old_titlemap.set_otx2inx(xio_otx, xio_inx)
    new_titlemap = titlemap_shop(zia_str, 7)
    assert new_titlemap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_titlemap = inherit_titlemap(new_titlemap, old_titlemap)

    # THEN
    assert inherited_titlemap.otx2inx_exists(xio_otx, xio_inx)
