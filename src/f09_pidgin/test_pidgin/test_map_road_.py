from src.a01_word_logic.road import default_bridge_if_None, create_road
from src.f04_pack.atom_config import event_int_str, face_name_str
from src.f09_pidgin.pidgin_config import default_unknown_word_if_None
from src.f09_pidgin.pidgin_config import (
    inx_bridge_str,
    otx2inx_str,
    otx_bridge_str,
    unknown_word_str,
)
from src.f09_pidgin.map import (
    titlemap_shop,
    RoadMap,
    roadmap_shop,
    get_roadmap_from_dict,
    get_roadmap_from_json,
    inherit_roadmap,
)
from pytest import raises as pytest_raises


# The goal of the pidgin function is to allow a single command, pointing at a bunch of directories
# initialize fiscunits and output acct metrics such as calendars, financial status, healer status


def test_default_unknown_word_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_word_if_None() == "UNKNOWN"


def test_RoadMap_Exists():
    # ESTABLISH
    x_roadmap = RoadMap()

    # WHEN / THEN
    assert not x_roadmap.face_name
    assert not x_roadmap.event_int
    assert not x_roadmap.otx2inx
    assert not x_roadmap.unknown_word
    assert not x_roadmap.otx_bridge
    assert not x_roadmap.inx_bridge
    assert not x_roadmap.titlemap


def test_roadmap_shop_ReturnsObj_scenario0():
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
    e7_roadmap = roadmap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_word=x_unknown_word,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )

    # THEN
    assert e7_roadmap.face_name == bob_str
    assert e7_roadmap.event_int == event7
    assert e7_roadmap.otx2inx == otx2inx
    assert e7_roadmap.unknown_word == x_unknown_word
    assert e7_roadmap.otx_bridge == slash_otx_bridge
    assert e7_roadmap.inx_bridge == colon_inx_bridge
    assert e7_roadmap.titlemap == titlemap_shop(
        face_name=bob_str,
        event_int=event7,
        unknown_word=x_unknown_word,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
    )


def test_roadmap_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    x_roadmap = roadmap_shop()

    # THEN
    assert x_roadmap.otx2inx == {}
    assert x_roadmap.unknown_word == default_unknown_word_if_None()
    assert x_roadmap.otx_bridge == default_bridge_if_None()
    assert x_roadmap.inx_bridge == default_bridge_if_None()
    assert x_roadmap.face_name is None
    assert x_roadmap.event_int == 0
    assert x_roadmap.titlemap == titlemap_shop(
        event_int=0,
        unknown_word=default_unknown_word_if_None(),
        otx_bridge=default_bridge_if_None(),
        inx_bridge=default_bridge_if_None(),
    )


def test_roadmap_shop_ReturnsObj_scenario3_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_roadmap = roadmap_shop(
        face_name=bob_str,
        event_int=event7,
        otx2inx=otx2inx,
        unknown_word=x_nan,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
    )

    # THEN
    assert x_roadmap.face_name == bob_str
    assert x_roadmap.event_int == event7
    assert x_roadmap.otx2inx == otx2inx
    assert x_roadmap.unknown_word == default_unknown_word_if_None()
    assert x_roadmap.otx_bridge == default_bridge_if_None()
    assert x_roadmap.inx_bridge == default_bridge_if_None()


def test_RoadMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    acct_name_roadmap = roadmap_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert acct_name_roadmap.otx2inx != x_otx2inx

    # WHEN
    acct_name_roadmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert acct_name_roadmap.otx2inx == x_otx2inx


def test_RoadMap_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    acct_name_roadmap = roadmap_shop(unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert acct_name_roadmap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acct_name_roadmap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_RoadMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_roadmap = roadmap_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_roadmap.otx2inx != x_otx2inx

    # WHEN
    x_roadmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_roadmap.otx2inx == x_otx2inx


def test_RoadMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap.otx2inx == {}

    # WHEN
    x_roadmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadmap.otx2inx == {xio_str: sue_str}


def test_RoadMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap._get_inx_value(xio_str) != sue_str

    # WHEN
    x_roadmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadmap._get_inx_value(xio_str) == sue_str


def test_RoadMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap.otx2inx_exists(xio_str, sue_str) is False
    assert x_roadmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_roadmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_roadmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_roadmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadmap.otx2inx_exists(xio_str, sue_str)
    assert x_roadmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_roadmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_roadmap.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_roadmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_roadmap.otx2inx_exists(xio_str, sue_str)
    assert x_roadmap.otx2inx_exists(xio_str, zia_str) is False
    assert x_roadmap.otx2inx_exists(xio_str, bob_str) is False
    assert x_roadmap.otx2inx_exists(zia_str, zia_str)


def test_RoadMap_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap.otx_exists(xio_str) is False
    assert x_roadmap.otx_exists(sue_str) is False
    assert x_roadmap.otx_exists(bob_str) is False
    assert x_roadmap.otx_exists(zia_str) is False

    # WHEN
    x_roadmap.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadmap.otx_exists(xio_str)
    assert x_roadmap.otx_exists(sue_str) is False
    assert x_roadmap.otx_exists(bob_str) is False
    assert x_roadmap.otx_exists(zia_str) is False

    # WHEN
    x_roadmap.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_roadmap.otx_exists(xio_str)
    assert x_roadmap.otx_exists(sue_str) is False
    assert x_roadmap.otx_exists(bob_str) is False
    assert x_roadmap.otx_exists(zia_str)


def test_RoadMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadmap = roadmap_shop(None)
    x_roadmap.set_otx2inx(xio_str, sue_str)
    assert x_roadmap.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_roadmap.del_otx2inx(xio_str)

    # THEN
    assert x_roadmap.otx2inx_exists(xio_str, sue_str) is False


def test_RoadMap_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_roadmap = roadmap_shop(unknown_word=x_unknown_word)
    x_roadmap.set_otx2inx(xio_str, sue_str)
    assert x_roadmap._unknown_word_in_otx2inx() is False

    # WHEN
    x_roadmap.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_roadmap._unknown_word_in_otx2inx()


def test_RoadMap_set_title_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap.titlemap.otx2inx == {}

    # WHEN
    x_roadmap.set_title(xio_str, sue_str)

    # THEN
    assert x_roadmap.titlemap.otx2inx == {xio_str: sue_str}


def test_RoadMap_set_title_RaisesExceptionWhen_bridge_In_otx_title():
    # ESTABLISH
    x_roadmap = roadmap_shop(None)
    sue_otx = f"Sue{x_roadmap.otx_bridge}"
    sue_inx = "Sue"
    assert x_roadmap.titlemap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_roadmap.set_title(sue_otx, sue_inx)
    exception_str = f"title cannot have otx_title '{sue_otx}'. It must be not have bridge {x_roadmap.otx_bridge}."
    assert str(excinfo.value) == exception_str


def test_RoadMap_set_title_RaisesExceptionWhen_bridge_In_inx_title():
    # ESTABLISH
    x_roadmap = roadmap_shop(None)
    sue_inx = f"Sue{x_roadmap.otx_bridge}"
    sue_otx = "Sue"
    assert x_roadmap.titlemap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_roadmap.set_title(sue_otx, sue_inx)
    exception_str = f"title cannot have inx_title '{sue_inx}'. It must be not have bridge {x_roadmap.inx_bridge}."
    assert str(excinfo.value) == exception_str


def test_RoadMap_get_inx_title_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap._get_inx_title(xio_str) != sue_str

    # WHEN
    x_roadmap.set_title(xio_str, sue_str)

    # THEN
    assert x_roadmap._get_inx_title(xio_str) == sue_str


def test_RoadMap_title_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap.title_exists(xio_str, sue_str) is False
    assert x_roadmap.title_exists(xio_str, zia_str) is False
    assert x_roadmap.title_exists(xio_str, bob_str) is False
    assert x_roadmap.title_exists(zia_str, zia_str) is False

    # WHEN
    x_roadmap.set_title(xio_str, sue_str)

    # THEN
    assert x_roadmap.title_exists(xio_str, sue_str)
    assert x_roadmap.title_exists(xio_str, zia_str) is False
    assert x_roadmap.title_exists(xio_str, bob_str) is False
    assert x_roadmap.title_exists(zia_str, zia_str) is False

    # WHEN
    x_roadmap.set_title(zia_str, zia_str)

    # THEN
    assert x_roadmap.title_exists(xio_str, sue_str)
    assert x_roadmap.title_exists(xio_str, zia_str) is False
    assert x_roadmap.title_exists(xio_str, bob_str) is False
    assert x_roadmap.title_exists(zia_str, zia_str)


def test_RoadMap_otx_title_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadmap = roadmap_shop(None)
    assert x_roadmap.otx_title_exists(xio_str) is False
    assert x_roadmap.otx_title_exists(sue_str) is False
    assert x_roadmap.otx_title_exists(bob_str) is False
    assert x_roadmap.otx_title_exists(zia_str) is False

    # WHEN
    x_roadmap.set_title(xio_str, sue_str)

    # THEN
    assert x_roadmap.otx_title_exists(xio_str)
    assert x_roadmap.otx_title_exists(sue_str) is False
    assert x_roadmap.otx_title_exists(bob_str) is False
    assert x_roadmap.otx_title_exists(zia_str) is False

    # WHEN
    x_roadmap.set_title(zia_str, zia_str)

    # THEN
    assert x_roadmap.otx_title_exists(xio_str)
    assert x_roadmap.otx_title_exists(sue_str) is False
    assert x_roadmap.otx_title_exists(bob_str) is False
    assert x_roadmap.otx_title_exists(zia_str)


def test_RoadMap_del_title_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadmap = roadmap_shop(None)
    x_roadmap.set_title(xio_str, sue_str)
    assert x_roadmap.title_exists(xio_str, sue_str)

    # WHEN
    x_roadmap.del_title(xio_str)

    # THEN
    assert x_roadmap.title_exists(xio_str, sue_str) is False


def test_RoadMap_set_title_Edits_otx2inx():
    # ESTABLISH
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_accord45_str, casa_otx_str)
    casa_inx_road = create_road(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)
    x_roadmap = roadmap_shop()
    x_roadmap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    x_roadmap.set_otx2inx(casa_otx_road, casa_inx_road)
    x_roadmap.set_otx2inx(clean_otx_road, clean_inx_road)
    x_roadmap.set_otx2inx(sweep_otx_road, sweep_inx_road)
    assert x_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_roadmap.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadmap.otx2inx_exists(clean_otx_road, clean_inx_road)
    assert x_roadmap.otx2inx_exists(sweep_otx_road, sweep_inx_road)

    # WHEN
    menage_inx_str = "menage"
    x_roadmap.set_title(clean_otx_str, menage_inx_str)

    # THEN
    menage_inx_road = create_road(casa_inx_road, menage_inx_str)
    sweep_menage_inx_road = create_road(menage_inx_road, sweep_str)
    assert x_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_roadmap.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadmap.otx2inx_exists(clean_otx_road, menage_inx_road)
    assert x_roadmap.otx2inx_exists(sweep_otx_road, sweep_menage_inx_road)


def test_RoadMap_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_bridge = "/"
    x_roadmap = roadmap_shop(sue_str, otx_bridge=slash_otx_bridge)
    x1_road_map_json = f"""{{
  "{event_int_str()}": 0,
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_roadmap.inx_bridge}",
  "{otx2inx_str()}": {{}},
  "{otx_bridge_str()}": "{x_roadmap.otx_bridge}",
  "{unknown_word_str()}": "{x_roadmap.unknown_word}"
}}"""
    print(f"           {x1_road_map_json=}")
    print(f"{x_roadmap.get_json()=}")
    assert x_roadmap.get_json() == x1_road_map_json

    # WHEN
    event7 = 7
    x_roadmap.set_otx2inx(clean_otx, clean_inx)
    x_roadmap.event_int = event7
    # THEN
    x2_road_map_json = f"""{{
  "{event_int_str()}": {event7},
  "{face_name_str()}": "{sue_str}",
  "{inx_bridge_str()}": "{x_roadmap.inx_bridge}",
  "{otx2inx_str()}": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "{otx_bridge_str()}": "{x_roadmap.otx_bridge}",
  "{unknown_word_str()}": "{x_roadmap.unknown_word}"
}}"""
    print(f"           {x2_road_map_json=}")
    print(f"{x_roadmap.get_json()=}")
    assert x_roadmap.get_json() == x2_road_map_json


def test_get_roadmap_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_bridge = "/"
    x_roadmap = roadmap_shop(sue_str, event7, otx_bridge=slash_otx_bridge)
    x_roadmap.set_otx2inx(clean_otx, clean_inx)
    x_roadmap.set_title("bob", "bobito")

    # WHEN
    gen_roadmap = get_roadmap_from_dict(x_roadmap.get_dict())

    # THEN
    assert gen_roadmap.face_name == x_roadmap.face_name
    assert gen_roadmap.event_int == x_roadmap.event_int
    assert gen_roadmap.event_int == event7
    assert gen_roadmap.titlemap.face_name == x_roadmap.titlemap.face_name
    assert gen_roadmap.titlemap.otx2inx != x_roadmap.titlemap.otx2inx
    assert gen_roadmap.titlemap != x_roadmap.titlemap
    assert gen_roadmap.otx2inx == x_roadmap.otx2inx
    assert gen_roadmap.otx_bridge == x_roadmap.otx_bridge
    assert gen_roadmap.inx_bridge == x_roadmap.inx_bridge
    assert gen_roadmap.unknown_word == x_roadmap.unknown_word


def test_get_roadmap_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_bridge = "/"
    x_roadmap = roadmap_shop(slash_otx_bridge)
    x_roadmap.set_otx2inx(clean_otx, clean_inx)
    x_roadmap.set_title("bob", "bobito")

    # WHEN
    x_roadmap = get_roadmap_from_json(x_roadmap.get_json())

    # THEN
    assert x_roadmap == x_roadmap


def test_RoadMap_all_otx_parent_roads_exist_ReturnsObj_RoadUnit():
    # ESTABLISH
    clean_otx_parent_road = "accord45"
    otx_r_bridge = "/"
    clean_otx_str = "clean"
    clean_otx_road = f"{clean_otx_parent_road}{otx_r_bridge}{clean_otx_str}"

    x_roadmap = roadmap_shop(otx_bridge=otx_r_bridge)
    assert x_roadmap.otx_exists(clean_otx_parent_road) is False
    assert x_roadmap.otx_exists(clean_otx_road) is False
    assert x_roadmap.all_otx_parent_roads_exist()

    # WHEN
    x_roadmap.set_otx2inx(clean_otx_road, "any")
    # THEN
    assert x_roadmap.otx_exists(clean_otx_parent_road) is False
    assert x_roadmap.otx_exists(clean_otx_road)
    assert x_roadmap.all_otx_parent_roads_exist() is False

    # WHEN
    x_roadmap.set_otx2inx(clean_otx_parent_road, "any")
    # THEN
    assert x_roadmap.otx_exists(clean_otx_parent_road)
    assert x_roadmap.otx_exists(clean_otx_road)
    assert x_roadmap.all_otx_parent_roads_exist()


def test_RoadMap_is_valid_ReturnsObj_Scenario0_item_title_str():
    # ESTABLISH
    clean_str = "clean"
    clean_inx = "propre"
    otx_bridge = "/"
    casa_otx = f"casa{otx_bridge}"
    casa_inx = "casa"
    titleunit_roadmap = roadmap_shop(otx_bridge=otx_bridge)
    assert titleunit_roadmap.is_valid()

    # WHEN
    titleunit_roadmap.set_otx2inx(clean_str, clean_inx)
    # THEN
    assert titleunit_roadmap.is_valid()

    # WHEN
    titleunit_roadmap.set_otx2inx(casa_otx, casa_inx)
    # THEN
    assert titleunit_roadmap.is_valid() is False


def test_RoadMap_is_valid_ReturnsObj_Scenario1_road_str():
    # ESTABLISH
    accord45_str = "accord45"
    otx_r_bridge = "/"
    inx_r_bridge = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{accord45_str}{otx_r_bridge}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_road = f"{accord45_str}{inx_r_bridge}{clean_inx_str}"
    # casa_otx = f"casa{otx_bridge}"
    # casa_inx = f"casa"
    x_roadmap = roadmap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    x_roadmap.set_otx2inx(accord45_str, accord45_str)
    assert x_roadmap.is_valid()
    assert x_roadmap.otx2inx_exists(clean_otx_road, clean_inx_road) is False

    # WHEN
    x_roadmap.set_otx2inx(clean_otx_road, clean_inx_road)
    # THEN
    assert x_roadmap.is_valid()
    assert x_roadmap.otx2inx_exists(clean_otx_road, clean_inx_road)


def test_RoadMap_is_valid_ReturnsObj_Scenario3_RoadUnit():
    # ESTABLISH
    clean_otx_parent_road = "accord45"
    otx_r_bridge = "/"
    clean_otx_str = "clean"
    clean_otx_road = f"{clean_otx_parent_road}{otx_r_bridge}{clean_otx_str}"

    x_roadmap = roadmap_shop(otx_bridge=otx_r_bridge)
    assert x_roadmap.otx_exists(clean_otx_parent_road) is False
    assert x_roadmap.otx_exists(clean_otx_road) is False
    assert x_roadmap.all_otx_parent_roads_exist()
    assert x_roadmap.is_valid()

    # WHEN
    x_roadmap.set_otx2inx(clean_otx_road, "any")
    # THEN
    assert x_roadmap.otx_exists(clean_otx_parent_road) is False
    assert x_roadmap.otx_exists(clean_otx_road)
    assert x_roadmap.all_otx_parent_roads_exist() is False
    assert x_roadmap.is_valid() is False

    # WHEN
    x_roadmap.set_otx2inx(clean_otx_parent_road, "any")
    # THEN
    assert x_roadmap.otx_exists(clean_otx_parent_road)
    assert x_roadmap.otx_exists(clean_otx_road)
    assert x_roadmap.all_otx_parent_roads_exist()
    assert x_roadmap.is_valid()


def test_inherit_roadmap_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_roadmap = roadmap_shop(zia_str, 3)
    new_roadmap = roadmap_shop(zia_str, 5)
    # WHEN
    inherit_roadmap(new_roadmap, old_roadmap)

    # THEN
    assert new_roadmap
    assert new_roadmap == roadmap_shop(zia_str, 5)


def test_inherit_roadmap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_roadmap = roadmap_shop(sue_str, 0, otx_bridge=slash_otx_bridge)
    new_roadmap = roadmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_roadmap(new_roadmap, old_roadmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_roadmap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_roadmap = roadmap_shop(sue_str, 0, inx_bridge=slash_otx_bridge)
    new_roadmap = roadmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_roadmap(new_roadmap, old_roadmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_roadmap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_word():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    old_roadmap = roadmap_shop(sue_str, 0, unknown_word=x_unknown_word)
    new_roadmap = roadmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_roadmap(new_roadmap, old_roadmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_roadmap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_roadmap = roadmap_shop(sue_str, 0)
    new_roadmap = roadmap_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_roadmap(new_roadmap, old_roadmap)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_inherit_roadmap_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_roadmap = roadmap_shop(sue_str, 5)
    new_roadmap = roadmap_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_roadmap(new_roadmap, old_roadmap)
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_roadmap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    zia_str = "Zia"
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_roadmap = roadmap_shop(zia_str, 3)
    old_roadmap.set_otx2inx(xio_otx, xio_inx)
    new_roadmap = roadmap_shop(zia_str, 7)
    assert new_roadmap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_roadmap = inherit_roadmap(new_roadmap, old_roadmap)

    # THEN
    assert inherited_roadmap.otx2inx_exists(xio_otx, xio_inx)
