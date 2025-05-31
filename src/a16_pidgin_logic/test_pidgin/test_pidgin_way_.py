from pytest import raises as pytest_raises
from src.a01_term_logic.way import create_way, default_bridge_if_None, to_way
from src.a09_pack_logic._test_util.a09_str import event_int_str, face_name_str
from src.a16_pidgin_logic._test_util.a16_str import (
    inx_bridge_str,
    otx2inx_str,
    otx_bridge_str,
    unknown_str_str,
)
from src.a16_pidgin_logic.map import (
    WayMap,
    get_waymap_from_dict,
    get_waymap_from_json,
    inherit_waymap,
    labelmap_shop,
    waymap_shop,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_str_if_None

# The goal of the pidgin function is to allow a single command, pointing at a bunch of directories
# initialize fiscunits and output acct metrics such as calendars, financial status, healer status


def test_default_unknown_str_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_str_if_None() == "UNKNOWN"


def test_WayMap_Exists():
    # ESTABLISH
    x_waymap = WayMap()

    # WHEN / THEN
    assert not x_waymap.face_name
    assert not x_waymap.event_int
    assert not x_waymap.otx2inx
    assert not x_waymap.unknown_str
    assert not x_waymap.otx_bridge
    assert not x_waymap.inx_bridge
    assert not x_waymap.labelmap


def test_waymap_shop_ReturnsObj_scenario0():
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
    e7_waymap = waymap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_str=x_unknown_str,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )

    # THEN
    assert e7_waymap.face_name == bob_str
    assert e7_waymap.event_int == event7
    assert e7_waymap.otx2inx == otx2inx
    assert e7_waymap.unknown_str == x_unknown_str
    assert e7_waymap.otx_bridge == slash_otx_bridge
    assert e7_waymap.inx_bridge == colon_inx_bridge
    assert e7_waymap.labelmap == labelmap_shop(
        face_name=bob_str,
        event_int=event7,
        unknown_str=x_unknown_str,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )


def test_waymap_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    x_waymap = waymap_shop()

    # THEN
    assert x_waymap.otx2inx == {}
    assert x_waymap.unknown_str == default_unknown_str_if_None()
    assert x_waymap.otx_bridge == default_bridge_if_None()
    assert x_waymap.inx_bridge == default_bridge_if_None()
    assert x_waymap.face_name is None
    assert x_waymap.event_int == 0
    assert x_waymap.labelmap == labelmap_shop(
        event_int=0,
        unknown_str=default_unknown_str_if_None(),
        otx_bridge=default_bridge_if_None(),
        inx_bridge=default_bridge_if_None(),
    )


def test_waymap_shop_ReturnsObj_scenario3_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_waymap = waymap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_str=x_nan,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
    )

    # THEN
    assert x_waymap.face_name == bob_str
    assert x_waymap.event_int == event7
    assert x_waymap.otx2inx == otx2inx
    assert x_waymap.unknown_str == default_unknown_str_if_None()
    assert x_waymap.otx_bridge == default_bridge_if_None()
    assert x_waymap.inx_bridge == default_bridge_if_None()


def test_WayMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    acct_name_waymap = waymap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert acct_name_waymap.otx2inx != x_otx2inx

    # WHEN
    acct_name_waymap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert acct_name_waymap.otx2inx == x_otx2inx


def test_WayMap_set_all_otx2inx_RaisesErrorIf_unknown_str_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    acct_name_waymap = waymap_shop(unknown_str=x_unknown_str)
    x_otx2inx = {xio_str: sue_str, x_unknown_str: zia_str}
    assert acct_name_waymap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acct_name_waymap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_str '{x_unknown_str}' in any str. Affected keys include ['{x_unknown_str}']."
    assert str(excinfo.value) == exception_str


def test_WayMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    x_waymap = waymap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_str: zia_str}
    assert x_waymap.otx2inx != x_otx2inx

    # WHEN
    x_waymap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_waymap.otx2inx == x_otx2inx


def test_WayMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_waymap = waymap_shop(None)
    assert x_waymap.otx2inx == {}

    # WHEN
    x_waymap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_waymap.otx2inx == {xio_str: sue_str}


def test_WayMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_waymap = waymap_shop(None)
    assert x_waymap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_waymap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_waymap._get_inx_value(xio_str) == sue_str


def test_WayMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_waymap = waymap_shop(None)
    assert x_waymap.otx2inx_exists(xio_str, sue_str) is False
    assert x_waymap.otx2inx_exists(xio_str, zia_str) is False
    assert x_waymap.otx2inx_exists(xio_str, bob_str) is False
    assert x_waymap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_waymap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_waymap.otx2inx_exists(xio_str, sue_str)
    assert x_waymap.otx2inx_exists(xio_str, zia_str) is False
    assert x_waymap.otx2inx_exists(xio_str, bob_str) is False
    assert x_waymap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_waymap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_waymap.otx2inx_exists(xio_str, sue_str)
    assert x_waymap.otx2inx_exists(xio_str, zia_str) is False
    assert x_waymap.otx2inx_exists(xio_str, bob_str) is False
    assert x_waymap.otx2inx_exists(zia_str, zia_str)


def test_WayMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_waymap = waymap_shop(None)
    assert x_waymap.otx_exists(xio_str) is False
    assert x_waymap.otx_exists(sue_str) is False
    assert x_waymap.otx_exists(bob_str) is False
    assert x_waymap.otx_exists(zia_str) is False

    # WHEN
    x_waymap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_waymap.otx_exists(xio_str)
    assert x_waymap.otx_exists(sue_str) is False
    assert x_waymap.otx_exists(bob_str) is False
    assert x_waymap.otx_exists(zia_str) is False

    # WHEN
    x_waymap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_waymap.otx_exists(xio_str)
    assert x_waymap.otx_exists(sue_str) is False
    assert x_waymap.otx_exists(bob_str) is False
    assert x_waymap.otx_exists(zia_str)


def test_WayMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_waymap = waymap_shop(None)
    x_waymap.set_otx2inx(xio_str, sue_str)
    assert x_waymap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_waymap.del_otx2inx(xio_str)

    # THEN
    assert x_waymap.otx2inx_exists(xio_str, sue_str) is False


def test_WayMap_unknown_str_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_str = "UnknownTerm"
    x_waymap = waymap_shop(unknown_str=x_unknown_str)
    x_waymap.set_otx2inx(xio_str, sue_str)
    assert x_waymap._unknown_str_in_otx2inx() is False

    # WHEN
    x_waymap.set_otx2inx(zia_str, x_unknown_str)

    # THEN
    assert x_waymap._unknown_str_in_otx2inx()


def test_WayMap_set_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_waymap = waymap_shop(None)
    assert x_waymap.labelmap.otx2inx == {}

    # WHEN
    x_waymap.set_label(xio_str, sue_str)

    # THEN
    assert x_waymap.labelmap.otx2inx == {xio_str: sue_str}


def test_WayMap_set_label_RaisesExceptionWhen_bridge_In_otx_label():
    # ESTABLISH
    x_waymap = waymap_shop(None)
    sue_otx = f"Sue{x_waymap.otx_bridge}"
    sue_inx = "Sue"
    assert x_waymap.labelmap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_waymap.set_label(sue_otx, sue_inx)
    exception_str = f"label cannot have otx_label '{sue_otx}'. It must be not have bridge {x_waymap.otx_bridge}."
    assert str(excinfo.value) == exception_str


def test_WayMap_set_label_RaisesExceptionWhen_bridge_In_inx_label():
    # ESTABLISH
    x_waymap = waymap_shop(None)
    sue_inx = f"Sue{x_waymap.otx_bridge}"
    sue_otx = "Sue"
    assert x_waymap.labelmap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_waymap.set_label(sue_otx, sue_inx)
    exception_str = f"label cannot have inx_label '{sue_inx}'. It must be not have bridge {x_waymap.inx_bridge}."
    assert str(excinfo.value) == exception_str


def test_WayMap_get_inx_label_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_waymap = waymap_shop(None)
    assert x_waymap._get_inx_label(xio_str) != sue_str

    # WHEN
    x_waymap.set_label(xio_str, sue_str)

    # THEN
    assert x_waymap._get_inx_label(xio_str) == sue_str


def test_WayPidgin_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_waymap = waymap_shop(None)
    assert x_waymap.label_exists(xio_str, sue_str) is False
    assert x_waymap.label_exists(xio_str, zia_str) is False
    assert x_waymap.label_exists(xio_str, bob_str) is False
    assert x_waymap.label_exists(zia_str, zia_str) is False

    # WHEN
    x_waymap.set_label(xio_str, sue_str)

    # THEN
    assert x_waymap.label_exists(xio_str, sue_str)
    assert x_waymap.label_exists(xio_str, zia_str) is False
    assert x_waymap.label_exists(xio_str, bob_str) is False
    assert x_waymap.label_exists(zia_str, zia_str) is False

    # WHEN
    x_waymap.set_label(zia_str, zia_str)

    # THEN
    assert x_waymap.label_exists(xio_str, sue_str)
    assert x_waymap.label_exists(xio_str, zia_str) is False
    assert x_waymap.label_exists(xio_str, bob_str) is False
    assert x_waymap.label_exists(zia_str, zia_str)


def test_WayMap_otx_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_waymap = waymap_shop(None)
    assert x_waymap.otx_label_exists(xio_str) is False
    assert x_waymap.otx_label_exists(sue_str) is False
    assert x_waymap.otx_label_exists(bob_str) is False
    assert x_waymap.otx_label_exists(zia_str) is False

    # WHEN
    x_waymap.set_label(xio_str, sue_str)

    # THEN
    assert x_waymap.otx_label_exists(xio_str)
    assert x_waymap.otx_label_exists(sue_str) is False
    assert x_waymap.otx_label_exists(bob_str) is False
    assert x_waymap.otx_label_exists(zia_str) is False

    # WHEN
    x_waymap.set_label(zia_str, zia_str)

    # THEN
    assert x_waymap.otx_label_exists(xio_str)
    assert x_waymap.otx_label_exists(sue_str) is False
    assert x_waymap.otx_label_exists(bob_str) is False
    assert x_waymap.otx_label_exists(zia_str)


def test_WayMap_del_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_waymap = waymap_shop(None)
    x_waymap.set_label(xio_str, sue_str)
    assert x_waymap.label_exists(xio_str, sue_str)

    # WHEN
    x_waymap.del_label(xio_str)

    # THEN
    assert x_waymap.label_exists(xio_str, sue_str) is False


def test_WayMap_set_label_Edits_otx2inx():
    # ESTABLISH
    otx_accord45_str = to_way("accord45")
    inx_accord87_str = to_way("accord87")
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_way = create_way(otx_accord45_str, casa_otx_str)
    casa_inx_way = create_way(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_way = create_way(casa_otx_way, clean_otx_str)
    clean_inx_way = create_way(casa_inx_way, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_way = create_way(clean_otx_way, sweep_str)
    sweep_inx_way = create_way(clean_inx_way, sweep_str)
    x_waymap = waymap_shop()
    x_waymap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    x_waymap.set_otx2inx(casa_otx_way, casa_inx_way)
    x_waymap.set_otx2inx(clean_otx_way, clean_inx_way)
    x_waymap.set_otx2inx(sweep_otx_way, sweep_inx_way)
    assert x_waymap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_waymap.otx2inx_exists(casa_otx_way, casa_inx_way)
    assert x_waymap.otx2inx_exists(clean_otx_way, clean_inx_way)
    assert x_waymap.otx2inx_exists(sweep_otx_way, sweep_inx_way)

    # WHEN
    menage_inx_str = "menage"
    x_waymap.set_label(clean_otx_str, menage_inx_str)

    # THEN
    menage_inx_way = create_way(casa_inx_way, menage_inx_str)
    sweep_menage_inx_way = create_way(menage_inx_way, sweep_str)
    assert x_waymap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_waymap.otx2inx_exists(casa_otx_way, casa_inx_way)
    assert x_waymap.otx2inx_exists(clean_otx_way, menage_inx_way)
    assert x_waymap.otx2inx_exists(sweep_otx_way, sweep_menage_inx_way)


def test_WayMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_bridge = "/"
    x_waymap = waymap_shop(sue_str, otx_bridge=slash_otx_bridge)
    x1_way_map_json = f"""{{
  "{event_int_str()}": 0,
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_waymap.inx_bridge}",
  "{otx2inx_str()}": {{}},
  "{otx_bridge_str()}": "{x_waymap.otx_bridge}",
  "{unknown_str_str()}": "{x_waymap.unknown_str}"
}}"""
    print(f"           {x1_way_map_json=}")
    print(f"{x_waymap.get_json()=}")
    assert x_waymap.get_json() == x1_way_map_json

    # WHEN
    event7 = 7
    x_waymap.set_otx2inx(clean_otx, clean_inx)
    x_waymap.event_int = event7
    # THEN
    x2_way_map_json = f"""{{
  "{event_int_str()}": {event7},
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_waymap.inx_bridge}",
  "{otx2inx_str()}": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "{otx_bridge_str()}": "{x_waymap.otx_bridge}",
  "{unknown_str_str()}": "{x_waymap.unknown_str}"
}}"""
    print(f"           {x2_way_map_json=}")
    print(f"{x_waymap.get_json()=}")
    assert x_waymap.get_json() == x2_way_map_json


def test_get_waymap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_bridge = "/"
    x_waymap = waymap_shop(sue_str, event7, otx_bridge=slash_otx_bridge)
    x_waymap.set_otx2inx(clean_otx, clean_inx)
    x_waymap.set_label("bob", "bobito")

    # WHEN
    gen_waymap = get_waymap_from_dict(x_waymap.get_dict())

    # THEN
    assert gen_waymap.face_name == x_waymap.face_name
    assert gen_waymap.event_int == x_waymap.event_int
    assert gen_waymap.event_int == event7
    assert gen_waymap.labelmap.face_name == x_waymap.labelmap.face_name
    assert gen_waymap.labelmap.otx2inx != x_waymap.labelmap.otx2inx
    assert gen_waymap.labelmap != x_waymap.labelmap
    assert gen_waymap.otx2inx == x_waymap.otx2inx
    assert gen_waymap.otx_bridge == x_waymap.otx_bridge
    assert gen_waymap.inx_bridge == x_waymap.inx_bridge
    assert gen_waymap.unknown_str == x_waymap.unknown_str


def test_get_waymap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_bridge = "/"
    x_waymap = waymap_shop(slash_otx_bridge)
    x_waymap.set_otx2inx(clean_otx, clean_inx)
    x_waymap.set_label("bob", "bobito")

    # WHEN
    x_waymap = get_waymap_from_json(x_waymap.get_json())

    # THEN
    assert x_waymap == x_waymap


def test_WayMap_all_otx_parent_ways_exist_ReturnsObj_WayTerm():
    # ESTABLISH
    otx_r_bridge = "/"
    clean_otx_parent_way = to_way("accord45", otx_r_bridge)
    clean_otx_str = "clean"
    clean_otx_way = create_way(clean_otx_parent_way, clean_otx_str, otx_r_bridge)

    x_waymap = waymap_shop(otx_bridge=otx_r_bridge)
    assert x_waymap.otx_exists(clean_otx_parent_way) is False
    assert x_waymap.otx_exists(clean_otx_way) is False
    assert x_waymap.all_otx_parent_ways_exist()

    # WHEN
    x_waymap.set_otx2inx(clean_otx_way, to_way("any", otx_r_bridge))
    # THEN
    assert x_waymap.otx_exists(clean_otx_parent_way) is False
    assert x_waymap.otx_exists(clean_otx_way)
    assert x_waymap.all_otx_parent_ways_exist() is False

    # WHEN
    x_waymap.set_otx2inx(clean_otx_parent_way, to_way("any"))
    # THEN
    assert x_waymap.otx_exists(clean_otx_parent_way)
    assert x_waymap.otx_exists(clean_otx_way)
    assert x_waymap.all_otx_parent_ways_exist()


def test_WayMap_is_valid_ReturnsObj_Scenario0_concept_label_str():
    # ESTABLISH
    x_otx_bridge = "/"
    x_inx_bridge = ":"
    labelterm_waymap = waymap_shop(otx_bridge=x_otx_bridge, inx_bridge=x_inx_bridge)

    clean_str = "clean"
    clean_inx = to_way("propre", x_inx_bridge)
    casa_otx = to_way("casa", x_otx_bridge)
    mop_otx = create_way(casa_otx, "mop", x_otx_bridge)
    mop_inx = "mop"
    casa_inx = "casa"
    assert labelterm_waymap.is_valid()

    # WHEN
    labelterm_waymap.set_otx2inx(clean_str, clean_inx)
    # THEN
    assert labelterm_waymap.is_valid()

    # WHEN
    labelterm_waymap.set_otx2inx(mop_otx, mop_inx)
    # THEN
    assert labelterm_waymap.is_valid() is False


def test_WayMap_is_valid_ReturnsObj_Scenario1_way_str():
    # ESTABLISH
    accord45_str = "accord45"
    otx_r_bridge = "/"
    inx_r_bridge = ":"
    clean_otx_str = "clean"
    clean_otx_way = f"{accord45_str}{otx_r_bridge}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_way = f"{accord45_str}{inx_r_bridge}{clean_inx_str}"
    # casa_otx = f"casa{otx_bridge}"
    # casa_inx = f"casa"
    x_waymap = waymap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    x_waymap.set_otx2inx(accord45_str, accord45_str)
    assert x_waymap.is_valid()
    assert x_waymap.otx2inx_exists(clean_otx_way, clean_inx_way) is False

    # WHEN
    x_waymap.set_otx2inx(clean_otx_way, clean_inx_way)
    # THEN
    assert x_waymap.is_valid()
    assert x_waymap.otx2inx_exists(clean_otx_way, clean_inx_way)


def test_WayMap_is_valid_ReturnsObj_Scenario3_WayTerm():
    # ESTABLISH
    otx_r_bridge = "/"
    clean_otx_parent_way = to_way("accord45", otx_r_bridge)
    clean_otx_str = "clean"
    clean_otx_way = create_way(clean_otx_parent_way, clean_otx_str, otx_r_bridge)

    x_waymap = waymap_shop(otx_bridge=otx_r_bridge)
    assert x_waymap.otx_exists(clean_otx_parent_way) is False
    assert x_waymap.otx_exists(clean_otx_way) is False
    assert x_waymap.all_otx_parent_ways_exist()
    assert x_waymap.is_valid()

    # WHEN
    x_waymap.set_otx2inx(clean_otx_way, "any")
    # THEN
    assert x_waymap.otx_exists(clean_otx_parent_way) is False
    assert x_waymap.otx_exists(clean_otx_way)
    assert x_waymap.all_otx_parent_ways_exist() is False
    assert x_waymap.is_valid() is False

    # WHEN
    x_waymap.set_otx2inx(clean_otx_parent_way, "any")
    # THEN
    assert x_waymap.otx_exists(clean_otx_parent_way)
    assert x_waymap.otx_exists(clean_otx_way)
    assert x_waymap.all_otx_parent_ways_exist()
    assert x_waymap.is_valid()


def test_inherit_waymap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_waymap = waymap_shop(zia_str, 3)
    new_waymap = waymap_shop(zia_str, 5)
    # WHEN
    inherit_waymap(new_waymap, old_waymap)

    # THEN
    assert new_waymap
    assert new_waymap == waymap_shop(zia_str, 5)


def test_inherit_waymap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_waymap = waymap_shop(sue_str, 0, otx_bridge=slash_otx_bridge)
    new_waymap = waymap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_waymap(new_waymap, old_waymap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_waymap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_waymap = waymap_shop(sue_str, 0, inx_bridge=slash_otx_bridge)
    new_waymap = waymap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_waymap(new_waymap, old_waymap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_waymap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    old_waymap = waymap_shop(sue_str, 0, unknown_str=x_unknown_str)
    new_waymap = waymap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_waymap(new_waymap, old_waymap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_waymap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_waymap = waymap_shop(sue_str, 0)
    new_waymap = waymap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_waymap(new_waymap, old_waymap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_waymap_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_waymap = waymap_shop(sue_str, 5)
    new_waymap = waymap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_waymap(new_waymap, old_waymap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_waymap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_waymap = waymap_shop(zia_str, 3)
    old_waymap.set_otx2inx(xio_otx, xio_inx)
    new_waymap = waymap_shop(zia_str, 7)
    assert new_waymap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_waymap = inherit_waymap(new_waymap, old_waymap)

    # THEN
    assert inherited_waymap.otx2inx_exists(xio_otx, xio_inx)
