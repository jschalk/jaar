from pytest import raises as pytest_raises
from src.ch16_translate.map import ropemap_shop
from src.ch16_translate.translate_main import translateunit_shop


def test_TranslateUnit_set_ropemap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    x_ropemap = ropemap_shop(face_name=sue_str)
    x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN
    sue_translateunit.set_ropemap(x_ropemap)

    # THEN
    assert sue_translateunit.ropemap == x_ropemap


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_translateunit.otx_knot != x_ropemap.otx_knot
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_inx_knot = "/"
    x_ropemap = ropemap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_translateunit.inx_knot != x_ropemap.inx_knot
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_ropemap = ropemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_translateunit.unknown_str != x_ropemap.unknown_str
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_translateunit = translateunit_shop(sue_str)
    x_ropemap = ropemap_shop(face_name=yao_str)
    assert sue_translateunit.face_name != x_ropemap.face_name
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit face_name is '{sue_translateunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_ropemap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    static_x_ropemap = ropemap_shop(face_name=sue_str)
    static_x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    sue_translateunit.set_ropemap(static_x_ropemap)

    # WHEN
    gen_x_ropemap = sue_translateunit.get_ropemap()

    # THEN
    assert gen_x_ropemap == static_x_ropemap


def test_TranslateUnit_set_rope_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    ropeid_ropemap = zia_translateunit.get_ropemap()
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_rope_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)

    assert zia_translateunit.rope_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.rope_exists(sue_otx, sue_inx)


def test_TranslateUnit_get_inx_rope_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    assert zia_translateunit._get_inx_rope(sue_otx) != sue_inx

    # WHEN
    zia_translateunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit._get_inx_rope(sue_otx) == sue_inx


def test_TranslateUnit_del_rope_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)

    zia_translateunit.set_rope(sue_otx, sue_inx)
    zia_translateunit.set_rope(zia_str, zia_str)
    assert zia_translateunit.rope_exists(sue_otx, sue_inx)
    assert zia_translateunit.rope_exists(zia_str, zia_str)

    # WHEN
    zia_translateunit.del_rope(sue_otx)

    # THEN
    assert zia_translateunit.rope_exists(sue_otx, sue_inx) is False
    assert zia_translateunit.rope_exists(zia_str, zia_str)
