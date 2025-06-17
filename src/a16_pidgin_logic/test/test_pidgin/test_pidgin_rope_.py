from pytest import raises as pytest_raises
from src.a01_term_logic.rope import create_rope, default_knot_if_None, to_rope
from src.a09_pack_logic._util.a09_str import event_int_str, face_name_str
from src.a16_pidgin_logic._util.a16_str import (
    inx_knot_str,
    otx2inx_str,
    otx_knot_str,
    unknown_str_str,
)
from src.a16_pidgin_logic.map import (
    RopeMap,
    get_ropemap_from_dict,
    get_ropemap_from_json,
    inherit_ropemap,
    labelmap_shop,
    ropemap_shop,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_str_if_None


def test_default_unknown_str_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_str_if_None() == "UNKNOWN"


def test_RopeMap_Exists():
    # ESTABLISH
    x_ropemap = RopeMap()

    # WHEN / THEN
    assert not x_ropemap.face_name
    assert not x_ropemap.event_int
    assert not x_ropemap.otx2inx
    assert not x_ropemap.unknown_str
    assert not x_ropemap.otx_knot
    assert not x_ropemap.inx_knot
    assert not x_ropemap.labelmap


def test_ropemap_shop_ReturnsObj_scenario0():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    e7_ropemap = ropemap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_str=x_unknown_str,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
    )

    # THEN
    assert e7_ropemap.face_name == bob_str
    assert e7_ropemap.event_int == event7
    assert e7_ropemap.otx2inx == otx2inx
    assert e7_ropemap.unknown_str == x_unknown_str
    assert e7_ropemap.otx_knot == slash_otx_knot
    assert e7_ropemap.inx_knot == colon_inx_knot
    assert e7_ropemap.labelmap == labelmap_shop(
        face_name=bob_str,
        event_int=event7,
        unknown_str=x_unknown_str,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
    )


def test_ropemap_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    x_ropemap = ropemap_shop()

    # THEN
    assert x_ropemap.otx2inx == {}
    assert x_ropemap.unknown_str == default_unknown_str_if_None()
    assert x_ropemap.otx_knot == default_knot_if_None()
    assert x_ropemap.inx_knot == default_knot_if_None()
    assert x_ropemap.face_name is None
    assert x_ropemap.event_int == 0
    assert x_ropemap.labelmap == labelmap_shop(
        event_int=0,
        unknown_str=default_unknown_str_if_None(),
        otx_knot=default_knot_if_None(),
        inx_knot=default_knot_if_None(),
    )


def test_ropemap_shop_ReturnsObj_scenario3_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_ropemap = ropemap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_ropemap.face_name == bob_str
    assert x_ropemap.event_int == event7
    assert x_ropemap.otx2inx == otx2inx
    assert x_ropemap.unknown_str == default_unknown_str_if_None()
    assert x_ropemap.otx_knot == default_knot_if_None()
    assert x_ropemap.inx_knot == default_knot_if_None()


def test_RopeMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    acct_name_ropemap = ropemap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert acct_name_ropemap.otx2inx != x_otx2inx

    # WHEN
    acct_name_ropemap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert acct_name_ropemap.otx2inx == x_otx2inx


def test_RopeMap_set_all_otx2inx_RaisesErrorIf_unknown_str_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    acct_name_ropemap = ropemap_shop(unknown_str=x_unknown_str)
    x_otx2inx = {xio_str: sue_str, x_unknown_str: zia_str}
    assert acct_name_ropemap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acct_name_ropemap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_str '{x_unknown_str}' in any str. Affected keys include ['{x_unknown_str}']."
    assert str(excinfo.value) == exception_str


def test_RopeMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    x_ropemap = ropemap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_str: zia_str}
    assert x_ropemap.otx2inx != x_otx2inx

    # WHEN
    x_ropemap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_ropemap.otx2inx == x_otx2inx


def test_RopeMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx2inx == {}

    # WHEN
    x_ropemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ropemap.otx2inx == {xio_str: sue_str}


def test_RopeMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_ropemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ropemap._get_inx_value(xio_str) == sue_str


def test_RopeMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx2inx_exists(xio_str, sue_str) is False
    assert x_ropemap.otx2inx_exists(xio_str, zia_str) is False
    assert x_ropemap.otx2inx_exists(xio_str, bob_str) is False
    assert x_ropemap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_ropemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ropemap.otx2inx_exists(xio_str, sue_str)
    assert x_ropemap.otx2inx_exists(xio_str, zia_str) is False
    assert x_ropemap.otx2inx_exists(xio_str, bob_str) is False
    assert x_ropemap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_ropemap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_ropemap.otx2inx_exists(xio_str, sue_str)
    assert x_ropemap.otx2inx_exists(xio_str, zia_str) is False
    assert x_ropemap.otx2inx_exists(xio_str, bob_str) is False
    assert x_ropemap.otx2inx_exists(zia_str, zia_str)


def test_RopeMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx_exists(xio_str) is False
    assert x_ropemap.otx_exists(sue_str) is False
    assert x_ropemap.otx_exists(bob_str) is False
    assert x_ropemap.otx_exists(zia_str) is False

    # WHEN
    x_ropemap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_ropemap.otx_exists(xio_str)
    assert x_ropemap.otx_exists(sue_str) is False
    assert x_ropemap.otx_exists(bob_str) is False
    assert x_ropemap.otx_exists(zia_str) is False

    # WHEN
    x_ropemap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_ropemap.otx_exists(xio_str)
    assert x_ropemap.otx_exists(sue_str) is False
    assert x_ropemap.otx_exists(bob_str) is False
    assert x_ropemap.otx_exists(zia_str)


def test_RopeMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ropemap = ropemap_shop(None)
    x_ropemap.set_otx2inx(xio_str, sue_str)
    assert x_ropemap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_ropemap.del_otx2inx(xio_str)

    # THEN
    assert x_ropemap.otx2inx_exists(xio_str, sue_str) is False


def test_RopeMap_unknown_str_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    x_ropemap = ropemap_shop(unknown_str=x_unknown_str)
    x_ropemap.set_otx2inx(xio_str, sue_str)
    assert x_ropemap._unknown_str_in_otx2inx() is False

    # WHEN
    x_ropemap.set_otx2inx(zia_str, x_unknown_str)

    # THEN
    assert x_ropemap._unknown_str_in_otx2inx()


def test_RopeMap_set_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.labelmap.otx2inx == {}

    # WHEN
    x_ropemap.set_label(xio_str, sue_str)

    # THEN
    assert x_ropemap.labelmap.otx2inx == {xio_str: sue_str}


def test_RopeMap_set_label_RaisesExceptionWhen_knot_In_otx_label():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    sue_otx = f"Sue{x_ropemap.otx_knot}"
    sue_inx = "Sue"
    assert x_ropemap.labelmap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ropemap.set_label(sue_otx, sue_inx)
    exception_str = f"label cannot have otx_label '{sue_otx}'. It must be not have knot {x_ropemap.otx_knot}."
    assert str(excinfo.value) == exception_str


def test_RopeMap_set_label_RaisesExceptionWhen_knot_In_inx_label():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    sue_inx = f"Sue{x_ropemap.otx_knot}"
    sue_otx = "Sue"
    assert x_ropemap.labelmap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ropemap.set_label(sue_otx, sue_inx)
    exception_str = f"label cannot have inx_label '{sue_inx}'. It must be not have knot {x_ropemap.inx_knot}."
    assert str(excinfo.value) == exception_str


def test_RopeMap_get_inx_label_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap._get_inx_label(xio_str) != sue_str

    # WHEN
    x_ropemap.set_label(xio_str, sue_str)

    # THEN
    assert x_ropemap._get_inx_label(xio_str) == sue_str


def test_RopePidgin_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.label_exists(xio_str, sue_str) is False
    assert x_ropemap.label_exists(xio_str, zia_str) is False
    assert x_ropemap.label_exists(xio_str, bob_str) is False
    assert x_ropemap.label_exists(zia_str, zia_str) is False

    # WHEN
    x_ropemap.set_label(xio_str, sue_str)

    # THEN
    assert x_ropemap.label_exists(xio_str, sue_str)
    assert x_ropemap.label_exists(xio_str, zia_str) is False
    assert x_ropemap.label_exists(xio_str, bob_str) is False
    assert x_ropemap.label_exists(zia_str, zia_str) is False

    # WHEN
    x_ropemap.set_label(zia_str, zia_str)

    # THEN
    assert x_ropemap.label_exists(xio_str, sue_str)
    assert x_ropemap.label_exists(xio_str, zia_str) is False
    assert x_ropemap.label_exists(xio_str, bob_str) is False
    assert x_ropemap.label_exists(zia_str, zia_str)


def test_RopeMap_otx_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx_label_exists(xio_str) is False
    assert x_ropemap.otx_label_exists(sue_str) is False
    assert x_ropemap.otx_label_exists(bob_str) is False
    assert x_ropemap.otx_label_exists(zia_str) is False

    # WHEN
    x_ropemap.set_label(xio_str, sue_str)

    # THEN
    assert x_ropemap.otx_label_exists(xio_str)
    assert x_ropemap.otx_label_exists(sue_str) is False
    assert x_ropemap.otx_label_exists(bob_str) is False
    assert x_ropemap.otx_label_exists(zia_str) is False

    # WHEN
    x_ropemap.set_label(zia_str, zia_str)

    # THEN
    assert x_ropemap.otx_label_exists(xio_str)
    assert x_ropemap.otx_label_exists(sue_str) is False
    assert x_ropemap.otx_label_exists(bob_str) is False
    assert x_ropemap.otx_label_exists(zia_str)


def test_RopeMap_del_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_ropemap = ropemap_shop(None)
    x_ropemap.set_label(xio_str, sue_str)
    assert x_ropemap.label_exists(xio_str, sue_str)

    # WHEN
    x_ropemap.del_label(xio_str)

    # THEN
    assert x_ropemap.label_exists(xio_str, sue_str) is False


def test_RopeMap_set_label_Edits_otx2inx():
    # ESTABLISH
    otx_accord45_str = to_rope("accord45")
    inx_accord87_str = to_rope("accord87")
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_accord45_str, casa_otx_str)
    casa_inx_rope = create_rope(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_rope = create_rope(clean_otx_rope, sweep_str)
    sweep_inx_rope = create_rope(clean_inx_rope, sweep_str)
    x_ropemap = ropemap_shop()
    x_ropemap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    x_ropemap.set_otx2inx(casa_otx_rope, casa_inx_rope)
    x_ropemap.set_otx2inx(clean_otx_rope, clean_inx_rope)
    x_ropemap.set_otx2inx(sweep_otx_rope, sweep_inx_rope)
    assert x_ropemap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope)
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope)
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_inx_rope)

    # WHEN
    menage_inx_str = "menage"
    x_ropemap.set_label(clean_otx_str, menage_inx_str)

    # THEN
    menage_inx_rope = create_rope(casa_inx_rope, menage_inx_str)
    sweep_menage_inx_rope = create_rope(menage_inx_rope, sweep_str)
    assert x_ropemap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope)
    assert x_ropemap.otx2inx_exists(clean_otx_rope, menage_inx_rope)
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_menage_inx_rope)


def test_RopeMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(sue_str, otx_knot=slash_otx_knot)
    x1_rope_map_json = f"""{{
  "{event_int_str()}": 0,
  "{face_name_str()}": "{sue_str}",
  "{inx_knot_str()}": "{x_ropemap.inx_knot}",
  "{otx2inx_str()}": {{}},
  "{otx_knot_str()}": "{x_ropemap.otx_knot}",
  "{unknown_str_str()}": "{x_ropemap.unknown_str}"
}}"""
    print(f"           {x1_rope_map_json=}")
    print(f"{x_ropemap.get_json()=}")
    assert x_ropemap.get_json() == x1_rope_map_json

    # WHEN
    event7 = 7
    x_ropemap.set_otx2inx(clean_otx, clean_inx)
    x_ropemap.event_int = event7
    # THEN
    x2_rope_map_json = f"""{{
  "{event_int_str()}": {event7},
  "{face_name_str()}": "{sue_str}",
  "{inx_knot_str()}": "{x_ropemap.inx_knot}",
  "{otx2inx_str()}": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "{otx_knot_str()}": "{x_ropemap.otx_knot}",
  "{unknown_str_str()}": "{x_ropemap.unknown_str}"
}}"""
    print(f"           {x2_rope_map_json=}")
    print(f"{x_ropemap.get_json()=}")
    assert x_ropemap.get_json() == x2_rope_map_json


def test_get_ropemap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(sue_str, event7, otx_knot=slash_otx_knot)
    x_ropemap.set_otx2inx(clean_otx, clean_inx)
    x_ropemap.set_label("bob", "bobito")

    # WHEN
    gen_ropemap = get_ropemap_from_dict(x_ropemap.get_dict())

    # THEN
    assert gen_ropemap.face_name == x_ropemap.face_name
    assert gen_ropemap.event_int == x_ropemap.event_int
    assert gen_ropemap.event_int == event7
    assert gen_ropemap.labelmap.face_name == x_ropemap.labelmap.face_name
    assert gen_ropemap.labelmap.otx2inx != x_ropemap.labelmap.otx2inx
    assert gen_ropemap.labelmap != x_ropemap.labelmap
    assert gen_ropemap.otx2inx == x_ropemap.otx2inx
    assert gen_ropemap.otx_knot == x_ropemap.otx_knot
    assert gen_ropemap.inx_knot == x_ropemap.inx_knot
    assert gen_ropemap.unknown_str == x_ropemap.unknown_str


def test_get_ropemap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(slash_otx_knot)
    x_ropemap.set_otx2inx(clean_otx, clean_inx)
    x_ropemap.set_label("bob", "bobito")

    # WHEN
    x_ropemap = get_ropemap_from_json(x_ropemap.get_json())

    # THEN
    assert x_ropemap == x_ropemap


def test_RopeMap_all_otx_parent_ropes_exist_ReturnsObj_RopeTerm():
    # ESTABLISH
    otx_r_knot = "/"
    clean_otx_parent_rope = to_rope("accord45", otx_r_knot)
    clean_otx_str = "clean"
    clean_otx_rope = create_rope(clean_otx_parent_rope, clean_otx_str, otx_r_knot)

    x_ropemap = ropemap_shop(otx_knot=otx_r_knot)
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope) is False
    assert x_ropemap.all_otx_parent_ropes_exist()

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_rope, to_rope("any", otx_r_knot))
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist() is False

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_parent_rope, to_rope("any"))
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope)
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist()


def test_RopeMap_is_valid_ReturnsObj_Scenario0_concept_label_str():
    # ESTABLISH
    x_otx_knot = "/"
    x_inx_knot = ":"
    labelterm_ropemap = ropemap_shop(otx_knot=x_otx_knot, inx_knot=x_inx_knot)

    clean_str = "clean"
    clean_inx = to_rope("propre", x_inx_knot)
    casa_otx = to_rope("casa", x_otx_knot)
    mop_otx = create_rope(casa_otx, "mop", x_otx_knot)
    mop_inx = "mop"
    casa_inx = "casa"
    assert labelterm_ropemap.is_valid()

    # WHEN
    labelterm_ropemap.set_otx2inx(clean_str, clean_inx)
    # THEN
    assert labelterm_ropemap.is_valid()

    # WHEN
    labelterm_ropemap.set_otx2inx(mop_otx, mop_inx)
    # THEN
    assert labelterm_ropemap.is_valid() is False


def test_RopeMap_is_valid_ReturnsObj_Scenario1_rope_str():
    # ESTABLISH
    accord45_str = "accord45"
    otx_r_knot = "/"
    inx_r_knot = ":"
    clean_otx_str = "clean"
    clean_otx_rope = f"{accord45_str}{otx_r_knot}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_rope = f"{accord45_str}{inx_r_knot}{clean_inx_str}"
    # casa_otx = f"casa{otx_knot}"
    # casa_inx = f"casa"
    x_ropemap = ropemap_shop(otx_knot=otx_r_knot, inx_knot=inx_r_knot)
    x_ropemap.set_otx2inx(accord45_str, accord45_str)
    assert x_ropemap.is_valid()
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope) is False

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_rope, clean_inx_rope)
    # THEN
    assert x_ropemap.is_valid()
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope)


def test_RopeMap_is_valid_ReturnsObj_Scenario3_RopeTerm():
    # ESTABLISH
    otx_r_knot = "/"
    clean_otx_parent_rope = to_rope("accord45", otx_r_knot)
    clean_otx_str = "clean"
    clean_otx_rope = create_rope(clean_otx_parent_rope, clean_otx_str, otx_r_knot)

    x_ropemap = ropemap_shop(otx_knot=otx_r_knot)
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope) is False
    assert x_ropemap.all_otx_parent_ropes_exist()
    assert x_ropemap.is_valid()

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_rope, "any")
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist() is False
    assert x_ropemap.is_valid() is False

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_parent_rope, "any")
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope)
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist()
    assert x_ropemap.is_valid()


def test_inherit_ropemap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_ropemap = ropemap_shop(zia_str, 3)
    new_ropemap = ropemap_shop(zia_str, 5)
    # WHEN
    inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert new_ropemap
    assert new_ropemap == ropemap_shop(zia_str, 5)


def test_inherit_ropemap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_ropemap = ropemap_shop(sue_str, 0, otx_knot=slash_otx_knot)
    new_ropemap = ropemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_ropemap = ropemap_shop(sue_str, 0, inx_knot=slash_otx_knot)
    new_ropemap = ropemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    old_ropemap = ropemap_shop(sue_str, 0, unknown_str=x_unknown_str)
    new_ropemap = ropemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_ropemap = ropemap_shop(sue_str, 0)
    new_ropemap = ropemap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_ropemap = ropemap_shop(sue_str, 5)
    new_ropemap = ropemap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_ropemap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_ropemap = ropemap_shop(zia_str, 3)
    old_ropemap.set_otx2inx(xio_otx, xio_inx)
    new_ropemap = ropemap_shop(zia_str, 7)
    assert new_ropemap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_ropemap = inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert inherited_ropemap.otx2inx_exists(xio_otx, xio_inx)
