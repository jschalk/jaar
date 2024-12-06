from src.f01_road.road import default_wall_if_none, create_road
from src.f08_pidgin.bridge import (
    RoadBridge,
    roadbridge_shop,
    default_unknown_word,
    get_roadbridge_from_dict,
    get_roadbridge_from_json,
)
from pytest import raises as pytest_raises


# The goal of the pidgin function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_default_unknown_word_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_word() == "UNKNOWN"


def test_RoadBridge_Exists():
    # ESTABLISH
    x_roadbridge = RoadBridge()

    # WHEN / THEN
    assert not x_roadbridge.face_id
    assert not x_roadbridge.event_id
    assert not x_roadbridge.otx2inx
    assert not x_roadbridge.unknown_word
    assert not x_roadbridge.otx_wall
    assert not x_roadbridge.inx_wall
    assert not x_roadbridge.nub_label


def test_roadbridge_shop_ReturnsObj_scenario0():
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
    acct_id_roadbridge = roadbridge_shop(
        x_face_id=bob_str,
        x_event_id=event7,
        x_otx2inx=otx2inx,
        x_unknown_word=x_unknown_word,
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
    )

    # THEN
    assert acct_id_roadbridge.face_id == bob_str
    assert acct_id_roadbridge.event_id == event7
    assert acct_id_roadbridge.otx2inx == otx2inx
    assert acct_id_roadbridge.unknown_word == x_unknown_word
    assert acct_id_roadbridge.otx_wall == slash_otx_wall
    assert acct_id_roadbridge.inx_wall == colon_inx_wall
    assert acct_id_roadbridge.nub_label == {}


def test_roadbridge_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    credit_vote_roadbridge = roadbridge_shop()

    # THEN
    assert credit_vote_roadbridge.otx2inx == {}
    assert credit_vote_roadbridge.unknown_word == default_unknown_word()
    assert credit_vote_roadbridge.otx_wall == default_wall_if_none()
    assert credit_vote_roadbridge.inx_wall == default_wall_if_none()
    assert credit_vote_roadbridge.face_id is None
    assert credit_vote_roadbridge.event_id == 0


def test_RoadBridge_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    acct_id_roadbridge = roadbridge_shop()
    x_otx2inx = {xio_str: sue_str, zia_str: zia_str}
    assert acct_id_roadbridge.otx2inx != x_otx2inx

    # WHEN
    acct_id_roadbridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert acct_id_roadbridge.otx2inx == x_otx2inx


def test_RoadBridge_set_all_otx2inx_RaisesErrorIf_unknown_word_IsKeyIn_otx2inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    acct_id_roadbridge = roadbridge_shop(x_unknown_word=x_unknown_word)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert acct_id_roadbridge.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acct_id_roadbridge.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_RoadBridge_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_roadbridge = roadbridge_shop(None)
    x_otx2inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_roadbridge.otx2inx != x_otx2inx

    # WHEN
    x_roadbridge.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_roadbridge.otx2inx == x_otx2inx


def test_RoadBridge_set_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge.otx2inx == {}

    # WHEN
    x_roadbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadbridge.otx2inx == {xio_str: sue_str}


def test_RoadBridge_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge._get_inx_value(xio_str) != sue_str

    # WHEN
    x_roadbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadbridge._get_inx_value(xio_str) == sue_str


def test_RoadBridge_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge.otx2inx_exists(xio_str, sue_str) is False
    assert x_roadbridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_roadbridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_roadbridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_roadbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadbridge.otx2inx_exists(xio_str, sue_str)
    assert x_roadbridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_roadbridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_roadbridge.otx2inx_exists(zia_str, zia_str) is False

    # WHEN
    x_roadbridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_roadbridge.otx2inx_exists(xio_str, sue_str)
    assert x_roadbridge.otx2inx_exists(xio_str, zia_str) is False
    assert x_roadbridge.otx2inx_exists(xio_str, bob_str) is False
    assert x_roadbridge.otx2inx_exists(zia_str, zia_str)


def test_RoadBridge_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge.otx_exists(xio_str) is False
    assert x_roadbridge.otx_exists(sue_str) is False
    assert x_roadbridge.otx_exists(bob_str) is False
    assert x_roadbridge.otx_exists(zia_str) is False

    # WHEN
    x_roadbridge.set_otx2inx(xio_str, sue_str)

    # THEN
    assert x_roadbridge.otx_exists(xio_str)
    assert x_roadbridge.otx_exists(sue_str) is False
    assert x_roadbridge.otx_exists(bob_str) is False
    assert x_roadbridge.otx_exists(zia_str) is False

    # WHEN
    x_roadbridge.set_otx2inx(zia_str, zia_str)

    # THEN
    assert x_roadbridge.otx_exists(xio_str)
    assert x_roadbridge.otx_exists(sue_str) is False
    assert x_roadbridge.otx_exists(bob_str) is False
    assert x_roadbridge.otx_exists(zia_str)


def test_RoadBridge_del_otx2inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadbridge = roadbridge_shop(None)
    x_roadbridge.set_otx2inx(xio_str, sue_str)
    assert x_roadbridge.otx2inx_exists(xio_str, sue_str)

    # WHEN
    x_roadbridge.del_otx2inx(xio_str)

    # THEN
    assert x_roadbridge.otx2inx_exists(xio_str, sue_str) is False


def test_RoadBridge_unknown_word_in_otx2inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownWord"
    x_roadbridge = roadbridge_shop(x_unknown_word=x_unknown_word)
    x_roadbridge.set_otx2inx(xio_str, sue_str)
    assert x_roadbridge._unknown_word_in_otx2inx() is False

    # WHEN
    x_roadbridge.set_otx2inx(zia_str, x_unknown_word)

    # THEN
    assert x_roadbridge._unknown_word_in_otx2inx()


def test_RoadBridge_set_nub_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge.nub_label == {}

    # WHEN
    x_roadbridge.set_nub_label(xio_str, sue_str)

    # THEN
    assert x_roadbridge.nub_label == {xio_str: sue_str}


def test_RoadBridge_set_nub_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge.nub_label == {}

    # WHEN
    x_roadbridge.set_nub_label(xio_str, sue_str)

    # THEN
    assert x_roadbridge.nub_label == {xio_str: sue_str}


def test_RoadBridge_set_nub_label_RaisesExceptionWhen_wall_In_otx_label():
    # ESTABLISH
    x_roadbridge = roadbridge_shop(None)
    sue_otx = f"Sue{x_roadbridge.otx_wall}"
    sue_inx = "Sue"
    assert x_roadbridge.nub_label == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_roadbridge.set_nub_label(sue_otx, sue_inx)
    exception_str = f"nub_label cannot have otx_label '{sue_otx}'. It must be not have wall {x_roadbridge.otx_wall}."
    assert str(excinfo.value) == exception_str


def test_RoadBridge_set_nub_label_RaisesExceptionWhen_wall_In_inx_label():
    # ESTABLISH
    x_roadbridge = roadbridge_shop(None)
    sue_inx = f"Sue{x_roadbridge.otx_wall}"
    sue_otx = "Sue"
    assert x_roadbridge.nub_label == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_roadbridge.set_nub_label(sue_otx, sue_inx)
    exception_str = f"nub_label cannot have inx_label '{sue_inx}'. It must be not have wall {x_roadbridge.inx_wall}."
    assert str(excinfo.value) == exception_str


def test_RoadBridge_get_nub_inx_label_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge._get_nub_inx_label(xio_str) != sue_str

    # WHEN
    x_roadbridge.set_nub_label(xio_str, sue_str)

    # THEN
    assert x_roadbridge._get_nub_inx_label(xio_str) == sue_str


def test_RoadBridge_nub_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge.nub_label_exists(xio_str, sue_str) is False
    assert x_roadbridge.nub_label_exists(xio_str, zia_str) is False
    assert x_roadbridge.nub_label_exists(xio_str, bob_str) is False
    assert x_roadbridge.nub_label_exists(zia_str, zia_str) is False

    # WHEN
    x_roadbridge.set_nub_label(xio_str, sue_str)

    # THEN
    assert x_roadbridge.nub_label_exists(xio_str, sue_str)
    assert x_roadbridge.nub_label_exists(xio_str, zia_str) is False
    assert x_roadbridge.nub_label_exists(xio_str, bob_str) is False
    assert x_roadbridge.nub_label_exists(zia_str, zia_str) is False

    # WHEN
    x_roadbridge.set_nub_label(zia_str, zia_str)

    # THEN
    assert x_roadbridge.nub_label_exists(xio_str, sue_str)
    assert x_roadbridge.nub_label_exists(xio_str, zia_str) is False
    assert x_roadbridge.nub_label_exists(xio_str, bob_str) is False
    assert x_roadbridge.nub_label_exists(zia_str, zia_str)


def test_RoadBridge_nub_otx_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_roadbridge = roadbridge_shop(None)
    assert x_roadbridge.nub_otx_label_exists(xio_str) is False
    assert x_roadbridge.nub_otx_label_exists(sue_str) is False
    assert x_roadbridge.nub_otx_label_exists(bob_str) is False
    assert x_roadbridge.nub_otx_label_exists(zia_str) is False

    # WHEN
    x_roadbridge.set_nub_label(xio_str, sue_str)

    # THEN
    assert x_roadbridge.nub_otx_label_exists(xio_str)
    assert x_roadbridge.nub_otx_label_exists(sue_str) is False
    assert x_roadbridge.nub_otx_label_exists(bob_str) is False
    assert x_roadbridge.nub_otx_label_exists(zia_str) is False

    # WHEN
    x_roadbridge.set_nub_label(zia_str, zia_str)

    # THEN
    assert x_roadbridge.nub_otx_label_exists(xio_str)
    assert x_roadbridge.nub_otx_label_exists(sue_str) is False
    assert x_roadbridge.nub_otx_label_exists(bob_str) is False
    assert x_roadbridge.nub_otx_label_exists(zia_str)


def test_RoadBridge_del_nub_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_roadbridge = roadbridge_shop(None)
    x_roadbridge.set_nub_label(xio_str, sue_str)
    assert x_roadbridge.nub_label_exists(xio_str, sue_str)

    # WHEN
    x_roadbridge.del_nub_label(xio_str)

    # THEN
    assert x_roadbridge.nub_label_exists(xio_str, sue_str) is False


def test_RoadBridge_set_nub_label_Edits_otx2inx():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_music45_str, casa_otx_str)
    casa_inx_road = create_road(inx_music87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)
    x_roadbridge = roadbridge_shop()
    x_roadbridge.set_otx2inx(otx_music45_str, inx_music87_str)
    x_roadbridge.set_otx2inx(casa_otx_road, casa_inx_road)
    x_roadbridge.set_otx2inx(clean_otx_road, clean_inx_road)
    x_roadbridge.set_otx2inx(sweep_otx_road, sweep_inx_road)
    assert x_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert x_roadbridge.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadbridge.otx2inx_exists(clean_otx_road, clean_inx_road)
    assert x_roadbridge.otx2inx_exists(sweep_otx_road, sweep_inx_road)

    # WHEN
    menage_inx_str = "menage"
    x_roadbridge.set_nub_label(clean_otx_str, menage_inx_str)

    # THEN
    menage_inx_road = create_road(casa_inx_road, menage_inx_str)
    sweep_menage_inx_road = create_road(menage_inx_road, sweep_str)
    assert x_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert x_roadbridge.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadbridge.otx2inx_exists(clean_otx_road, menage_inx_road)
    assert x_roadbridge.otx2inx_exists(sweep_otx_road, sweep_menage_inx_road)


def test_RoadBridge_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_wall = "/"
    x_roadbridge = roadbridge_shop(slash_otx_wall, x_face_id=sue_str)
    x1_road_bridge_json = f"""{{
  "event_id": 0,
  "face_id": "{sue_str}",
  "inx_wall": "{x_roadbridge.inx_wall}",
  "nub_label": {x_roadbridge.nub_label},
  "otx2inx": {{}},
  "otx_wall": "{x_roadbridge.otx_wall}",
  "unknown_word": "{x_roadbridge.unknown_word}"
}}"""
    print(f"           {x1_road_bridge_json=}")
    print(f"{x_roadbridge.get_json()=}")
    assert x_roadbridge.get_json() == x1_road_bridge_json

    # WHEN
    event7 = 7
    x_roadbridge.set_otx2inx(clean_otx, clean_inx)
    x_roadbridge.event_id = event7
    # THEN
    x2_road_bridge_json = f"""{{
  "event_id": {event7},
  "face_id": "{sue_str}",
  "inx_wall": "{x_roadbridge.inx_wall}",
  "nub_label": {x_roadbridge.nub_label},
  "otx2inx": {{
    "{clean_otx}": "{clean_inx}"
  }},
  "otx_wall": "{x_roadbridge.otx_wall}",
  "unknown_word": "{x_roadbridge.unknown_word}"
}}"""
    print(f"           {x2_road_bridge_json=}")
    print(f"{x_roadbridge.get_json()=}")
    assert x_roadbridge.get_json() == x2_road_bridge_json


def test_get_roadbridge_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    clean_otx = "clean"
    clean_inx = "propre"
    event7 = 7
    slash_otx_wall = "/"
    x_roadbridge = roadbridge_shop(slash_otx_wall, x_face_id=sue_str, x_event_id=event7)
    x_roadbridge.set_otx2inx(clean_otx, clean_inx)
    x_roadbridge.set_nub_label("bob", "bobito")

    # WHEN
    gen_roadbridge = get_roadbridge_from_dict(x_roadbridge.get_dict())

    # THEN
    assert gen_roadbridge.face_id == x_roadbridge.face_id
    assert gen_roadbridge.event_id == x_roadbridge.event_id
    assert gen_roadbridge.event_id == event7
    assert gen_roadbridge == x_roadbridge


def test_get_roadbridge_from_json_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    slash_otx_wall = "/"
    x_roadbridge = roadbridge_shop(slash_otx_wall)
    x_roadbridge.set_otx2inx(clean_otx, clean_inx)
    x_roadbridge.set_nub_label("bob", "bobito")

    # WHEN
    x_roadbridge = get_roadbridge_from_json(x_roadbridge.get_json())

    # THEN
    assert x_roadbridge == x_roadbridge


def test_RoadBridge_all_otx_parent_roads_exist_ReturnsObj_RoadUnit():
    # ESTABLISH
    clean_otx_parent_road = "music45"
    otx_r_wall = "/"
    clean_otx_str = "clean"
    clean_otx_road = f"{clean_otx_parent_road}{otx_r_wall}{clean_otx_str}"

    x_roadbridge = roadbridge_shop(otx_r_wall)
    assert x_roadbridge.otx_exists(clean_otx_parent_road) is False
    assert x_roadbridge.otx_exists(clean_otx_road) is False
    assert x_roadbridge.all_otx_parent_roads_exist()

    # WHEN
    x_roadbridge.set_otx2inx(clean_otx_road, "any")
    # THEN
    assert x_roadbridge.otx_exists(clean_otx_parent_road) is False
    assert x_roadbridge.otx_exists(clean_otx_road)
    assert x_roadbridge.all_otx_parent_roads_exist() is False

    # WHEN
    x_roadbridge.set_otx2inx(clean_otx_parent_road, "any")
    # THEN
    assert x_roadbridge.otx_exists(clean_otx_parent_road)
    assert x_roadbridge.otx_exists(clean_otx_road)
    assert x_roadbridge.all_otx_parent_roads_exist()


def test_RoadBridge_is_valid_ReturnsObj_Scenario0_label_str():
    # ESTABLISH
    clean_str = "clean"
    clean_inx = "propre"
    otx_wall = "/"
    casa_otx = f"casa{otx_wall}"
    casa_inx = "casa"
    ideaunit_roadbridge = roadbridge_shop(otx_wall)
    assert ideaunit_roadbridge.is_valid()

    # WHEN
    ideaunit_roadbridge.set_otx2inx(clean_str, clean_inx)
    # THEN
    assert ideaunit_roadbridge.is_valid()

    # WHEN
    ideaunit_roadbridge.set_otx2inx(casa_otx, casa_inx)
    # THEN
    assert ideaunit_roadbridge.is_valid() is False


def test_RoadBridge_is_valid_ReturnsObj_Scenario1_road_str():
    # ESTABLISH
    music_str = "music45"
    otx_r_wall = "/"
    inx_r_wall = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{music_str}{otx_r_wall}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_road = f"{music_str}{inx_r_wall}{clean_inx_str}"
    # casa_otx = f"casa{otx_wall}"
    # casa_inx = f"casa"
    x_roadbridge = roadbridge_shop(otx_r_wall, inx_r_wall)
    x_roadbridge.set_otx2inx(music_str, music_str)
    assert x_roadbridge.is_valid()
    assert x_roadbridge.otx2inx_exists(clean_otx_road, clean_inx_road) is False

    # WHEN
    x_roadbridge.set_otx2inx(clean_otx_road, clean_inx_road)
    # THEN
    assert x_roadbridge.is_valid()
    assert x_roadbridge.otx2inx_exists(clean_otx_road, clean_inx_road)


def test_RoadBridge_is_valid_ReturnsObj_Scenario3_RoadUnit():
    # ESTABLISH
    clean_otx_parent_road = "music45"
    otx_r_wall = "/"
    clean_otx_str = "clean"
    clean_otx_road = f"{clean_otx_parent_road}{otx_r_wall}{clean_otx_str}"

    x_roadbridge = roadbridge_shop(otx_r_wall)
    assert x_roadbridge.otx_exists(clean_otx_parent_road) is False
    assert x_roadbridge.otx_exists(clean_otx_road) is False
    assert x_roadbridge.all_otx_parent_roads_exist()
    assert x_roadbridge.is_valid()

    # WHEN
    x_roadbridge.set_otx2inx(clean_otx_road, "any")
    # THEN
    assert x_roadbridge.otx_exists(clean_otx_parent_road) is False
    assert x_roadbridge.otx_exists(clean_otx_road)
    assert x_roadbridge.all_otx_parent_roads_exist() is False
    assert x_roadbridge.is_valid() is False

    # WHEN
    x_roadbridge.set_otx2inx(clean_otx_parent_road, "any")
    # THEN
    assert x_roadbridge.otx_exists(clean_otx_parent_road)
    assert x_roadbridge.otx_exists(clean_otx_road)
    assert x_roadbridge.all_otx_parent_roads_exist()
    assert x_roadbridge.is_valid()
