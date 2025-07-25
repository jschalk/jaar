from pytest import raises as pytest_raises
from src.a16_pidgin_logic.map import ropemap_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop


def test_PidginUnit_set_ropemap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_ropemap = ropemap_shop(face_name=sue_str)
    x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.ropemap != x_ropemap

    # WHEN
    sue_pidginunit.set_ropemap(x_ropemap)

    # THEN
    assert sue_pidginunit.ropemap == x_ropemap


def test_PidginUnit_set_ropemap_RaisesErrorIf_ropemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_pidginunit.otx_knot != x_ropemap.otx_knot
    assert sue_pidginunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: PidginUnit otx_knot is '{sue_pidginunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_ropemap_RaisesErrorIf_ropemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_knot = "/"
    x_ropemap = ropemap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_pidginunit.inx_knot != x_ropemap.inx_knot
    assert sue_pidginunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: PidginUnit inx_knot is '{sue_pidginunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_ropemap_RaisesErrorIf_ropemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_ropemap = ropemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_pidginunit.unknown_str != x_ropemap.unknown_str
    assert sue_pidginunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_str is '{sue_pidginunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_ropemap_RaisesErrorIf_ropemap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_ropemap = ropemap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_ropemap.face_name
    assert sue_pidginunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_ropemap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_ropemap = ropemap_shop(face_name=sue_str)
    static_x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_ropemap(static_x_ropemap)

    # WHEN
    gen_x_ropemap = sue_pidginunit.get_ropemap()

    # THEN
    assert gen_x_ropemap == static_x_ropemap


def test_PidginUnit_set_rope_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    ropeid_ropemap = zia_pidginunit.get_ropemap()
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_rope_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.rope_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.rope_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_rope_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_rope(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_rope(sue_otx) == sue_inx


def test_PidginUnit_del_rope_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_rope(sue_otx, sue_inx)
    zia_pidginunit.set_rope(zia_str, zia_str)
    assert zia_pidginunit.rope_exists(sue_otx, sue_inx)
    assert zia_pidginunit.rope_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_rope(sue_otx)

    # THEN
    assert zia_pidginunit.rope_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.rope_exists(zia_str, zia_str)
