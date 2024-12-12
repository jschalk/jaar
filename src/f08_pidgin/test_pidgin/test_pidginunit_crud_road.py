from src.f08_pidgin.bridge import roadbridge_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_roadbridge_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_roadbridge = roadbridge_shop(face_id=sue_str)
    x_roadbridge.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.roadbridge != x_roadbridge

    # WHEN
    sue_pidginunit.set_roadbridge(x_roadbridge)

    # THEN
    assert sue_pidginunit.roadbridge == x_roadbridge


def test_PidginUnit_set_roadbridge_RaisesErrorIf_roadbridge_otx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_wall = "/"
    x_roadbridge = roadbridge_shop(otx_wall=slash_otx_wall, face_id=sue_str)
    assert sue_pidginunit.otx_wall != x_roadbridge.otx_wall
    assert sue_pidginunit.roadbridge != x_roadbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadbridge(x_roadbridge)
    exception_str = f"set_bridgecore Error: PidginUnit otx_wall is '{sue_pidginunit.otx_wall}', BridgeCore is '{slash_otx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_roadbridge_RaisesErrorIf_roadbridge_inx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_wall = "/"
    x_roadbridge = roadbridge_shop(inx_wall=slash_inx_wall, face_id=sue_str)
    assert sue_pidginunit.inx_wall != x_roadbridge.inx_wall
    assert sue_pidginunit.roadbridge != x_roadbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadbridge(x_roadbridge)
    exception_str = f"set_bridgecore Error: PidginUnit inx_wall is '{sue_pidginunit.inx_wall}', BridgeCore is '{slash_inx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_roadbridge_RaisesErrorIf_roadbridge_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_roadbridge = roadbridge_shop(unknown_word=casa_unknown_word, face_id=sue_str)
    assert sue_pidginunit.unknown_word != x_roadbridge.unknown_word
    assert sue_pidginunit.roadbridge != x_roadbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadbridge(x_roadbridge)
    exception_str = f"set_bridgecore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', BridgeCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_roadbridge_RaisesErrorIf_roadbridge_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_roadbridge = roadbridge_shop(face_id=yao_str)
    assert sue_pidginunit.face_id != x_roadbridge.face_id
    assert sue_pidginunit.roadbridge != x_roadbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadbridge(x_roadbridge)
    exception_str = f"set_bridgecore Error: PidginUnit face_id is '{sue_pidginunit.face_id}', BridgeCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_roadbridge_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_roadbridge = roadbridge_shop(face_id=sue_str)
    static_x_roadbridge.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_roadbridge(static_x_roadbridge)

    # WHEN
    gen_x_roadbridge = sue_pidginunit.get_roadbridge()

    # THEN
    assert gen_x_roadbridge == static_x_roadbridge


def test_PidginUnit_set_road_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadid_roadbridge = zia_pidginunit.get_roadbridge()
    assert roadid_roadbridge.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_road(sue_otx, sue_inx)

    # THEN
    assert roadid_roadbridge.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_road_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.road_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_road(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.road_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_road_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_road(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_road(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_road(sue_otx) == sue_inx


def test_PidginUnit_del_road_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_road(sue_otx, sue_inx)
    zia_pidginunit.set_road(zia_str, zia_str)
    assert zia_pidginunit.road_exists(sue_otx, sue_inx)
    assert zia_pidginunit.road_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_road(sue_otx)

    # THEN
    assert zia_pidginunit.road_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.road_exists(zia_str, zia_str)
