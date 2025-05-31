from pytest import raises as pytest_raises
from src.a16_pidgin_logic.map import namemap_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop


def test_PidginUnit_set_namemap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_namemap = namemap_shop(face_name=sue_str)
    x_namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.namemap != x_namemap

    # WHEN
    sue_pidginunit.set_namemap(x_namemap)

    # THEN
    assert sue_pidginunit.namemap == x_namemap


def test_PidginUnit_set_namemap_SetsAttrWhenAttrIs_float_nan():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_nan = float("nan")
    x_namemap = namemap_shop(
        face_name=sue_str, otx_bridge=x_nan, inx_bridge=x_nan, unknown_str=x_nan
    )
    x_namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.namemap != x_namemap

    # WHEN
    sue_pidginunit.set_namemap(x_namemap)

    # THEN
    assert sue_pidginunit.namemap == x_namemap


def test_PidginUnit_set_namemap_RaisesErrorIf_namemap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_namemap = namemap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_namemap.otx_bridge
    assert sue_pidginunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_namemap_RaisesErrorIf_namemap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_namemap = namemap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_namemap.inx_bridge
    assert sue_pidginunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_namemap_RaisesErrorIf_namemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_namemap = namemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_pidginunit.unknown_str != x_namemap.unknown_str
    assert sue_pidginunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_str is '{sue_pidginunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_namemap_RaisesErrorIf_namemap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_namemap = namemap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_namemap.face_name
    assert sue_pidginunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_namemap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_namemap = namemap_shop(face_name=sue_str)
    static_x_namemap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_namemap(static_x_namemap)

    # WHEN
    gen_x_namemap = sue_pidginunit.get_namemap()

    # THEN
    assert gen_x_namemap == static_x_namemap


def test_PidginUnit_set_nameterm_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acct_name_namemap = zia_pidginunit.get_namemap()
    assert acct_name_namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_nameterm(sue_otx, sue_inx)

    # THEN
    assert acct_name_namemap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_nameterm_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.nameterm_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_nameterm(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.nameterm_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_name_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_name(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_nameterm(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_name(sue_otx) == sue_inx


def test_PidginUnit_del_nameterm_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_nameterm(sue_otx, sue_inx)
    zia_pidginunit.set_nameterm(zia_str, zia_str)
    assert zia_pidginunit.nameterm_exists(sue_otx, sue_inx)
    assert zia_pidginunit.nameterm_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_nameterm(sue_otx)

    # THEN
    assert zia_pidginunit.nameterm_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.nameterm_exists(zia_str, zia_str)
