from src.a16_pidgin_logic.map import titlemap_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_titlemap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_titlemap = titlemap_shop(face_name=sue_str)
    x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.titlemap != x_titlemap

    # WHEN
    sue_pidginunit.set_titlemap(x_titlemap)

    # THEN
    assert sue_pidginunit.titlemap == x_titlemap


def test_PidginUnit_set_titlemap_RaisesErrorIf_titlemap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_titlemap = titlemap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_titlemap.otx_bridge
    assert sue_pidginunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_titlemap_RaisesErrorIf_titlemap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_titlemap = titlemap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_titlemap.inx_bridge
    assert sue_pidginunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_titlemap_RaisesErrorIf_titlemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_titlemap = titlemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_pidginunit.unknown_str != x_titlemap.unknown_str
    assert sue_pidginunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_str is '{sue_pidginunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_titlemap_RaisesErrorIf_titlemap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_titlemap = titlemap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_titlemap.face_name
    assert sue_pidginunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_titlemap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_titlemap = titlemap_shop(face_name=sue_str)
    static_x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_titlemap(static_x_titlemap)

    # WHEN
    gen_x_titlemap = sue_pidginunit.get_titlemap()

    # THEN
    assert gen_x_titlemap == static_x_titlemap


def test_PidginUnit_set_titleterm_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acct_name_titlemap = zia_pidginunit.get_titlemap()
    assert acct_name_titlemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert acct_name_titlemap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_titleterm_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.titleterm_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.titleterm_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_title_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_title(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_title(sue_otx) == sue_inx


def test_PidginUnit_del_titleterm_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_titleterm(sue_otx, sue_inx)
    zia_pidginunit.set_titleterm(zia_str, zia_str)
    assert zia_pidginunit.titleterm_exists(sue_otx, sue_inx)
    assert zia_pidginunit.titleterm_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_titleterm(sue_otx)

    # THEN
    assert zia_pidginunit.titleterm_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.titleterm_exists(zia_str, zia_str)
