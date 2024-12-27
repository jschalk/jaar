from src.f08_pidgin.map import roadmap_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_roadmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_roadmap = roadmap_shop(face_id=sue_str)
    x_roadmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.roadmap != x_roadmap

    # WHEN
    sue_pidginunit.set_roadmap(x_roadmap)

    # THEN
    assert sue_pidginunit.roadmap == x_roadmap


def test_PidginUnit_set_roadmap_RaisesErrorIf_roadmap_otx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_wall = "/"
    x_roadmap = roadmap_shop(otx_wall=slash_otx_wall, face_id=sue_str)
    assert sue_pidginunit.otx_wall != x_roadmap.otx_wall
    assert sue_pidginunit.roadmap != x_roadmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadmap(x_roadmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_wall is '{sue_pidginunit.otx_wall}', MapCore is '{slash_otx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_roadmap_RaisesErrorIf_roadmap_inx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_wall = "/"
    x_roadmap = roadmap_shop(inx_wall=slash_inx_wall, face_id=sue_str)
    assert sue_pidginunit.inx_wall != x_roadmap.inx_wall
    assert sue_pidginunit.roadmap != x_roadmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadmap(x_roadmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_wall is '{sue_pidginunit.inx_wall}', MapCore is '{slash_inx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_roadmap_RaisesErrorIf_roadmap_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_roadmap = roadmap_shop(unknown_word=casa_unknown_word, face_id=sue_str)
    assert sue_pidginunit.unknown_word != x_roadmap.unknown_word
    assert sue_pidginunit.roadmap != x_roadmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadmap(x_roadmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_roadmap_RaisesErrorIf_roadmap_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_roadmap = roadmap_shop(face_id=yao_str)
    assert sue_pidginunit.face_id != x_roadmap.face_id
    assert sue_pidginunit.roadmap != x_roadmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_roadmap(x_roadmap)
    exception_str = f"set_mapcore Error: PidginUnit face_id is '{sue_pidginunit.face_id}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_roadmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_roadmap = roadmap_shop(face_id=sue_str)
    static_x_roadmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_roadmap(static_x_roadmap)

    # WHEN
    gen_x_roadmap = sue_pidginunit.get_roadmap()

    # THEN
    assert gen_x_roadmap == static_x_roadmap


def test_PidginUnit_set_road_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadid_roadmap = zia_pidginunit.get_roadmap()
    assert roadid_roadmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_road(sue_otx, sue_inx)

    # THEN
    assert roadid_roadmap.otx2inx_exists(sue_otx, sue_inx)


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
