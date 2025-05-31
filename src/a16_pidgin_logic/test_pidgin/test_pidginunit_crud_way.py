from pytest import raises as pytest_raises
from src.a16_pidgin_logic.map import waymap_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop


def test_PidginUnit_set_waymap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_waymap = waymap_shop(face_name=sue_str)
    x_waymap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.waymap != x_waymap

    # WHEN
    sue_pidginunit.set_waymap(x_waymap)

    # THEN
    assert sue_pidginunit.waymap == x_waymap


def test_PidginUnit_set_waymap_RaisesErrorIf_waymap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_waymap = waymap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_waymap.otx_bridge
    assert sue_pidginunit.waymap != x_waymap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_waymap(x_waymap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_waymap_RaisesErrorIf_waymap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_waymap = waymap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_waymap.inx_bridge
    assert sue_pidginunit.waymap != x_waymap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_waymap(x_waymap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_waymap_RaisesErrorIf_waymap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_waymap = waymap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_pidginunit.unknown_str != x_waymap.unknown_str
    assert sue_pidginunit.waymap != x_waymap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_waymap(x_waymap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_str is '{sue_pidginunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_waymap_RaisesErrorIf_waymap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_waymap = waymap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_waymap.face_name
    assert sue_pidginunit.waymap != x_waymap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_waymap(x_waymap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_waymap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_waymap = waymap_shop(face_name=sue_str)
    static_x_waymap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_waymap(static_x_waymap)

    # WHEN
    gen_x_waymap = sue_pidginunit.get_waymap()

    # THEN
    assert gen_x_waymap == static_x_waymap


def test_PidginUnit_set_way_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    wayid_waymap = zia_pidginunit.get_waymap()
    assert wayid_waymap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_way(sue_otx, sue_inx)

    # THEN
    assert wayid_waymap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_way_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.way_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_way(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.way_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_way_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_way(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_way(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_way(sue_otx) == sue_inx


def test_PidginUnit_del_way_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_way(sue_otx, sue_inx)
    zia_pidginunit.set_way(zia_str, zia_str)
    assert zia_pidginunit.way_exists(sue_otx, sue_inx)
    assert zia_pidginunit.way_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_way(sue_otx)

    # THEN
    assert zia_pidginunit.way_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.way_exists(zia_str, zia_str)
