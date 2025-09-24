from pytest import raises as pytest_raises
from src.ch16_translate_logic.map import namemap_shop
from src.ch16_translate_logic.translate_main import translateunit_shop


def test_TranslateUnit_set_namemap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    x_namemap = namemap_shop(face_name=sue_str)
    x_namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.namemap != x_namemap

    # WHEN
    sue_translateunit.set_namemap(x_namemap)

    # THEN
    assert sue_translateunit.namemap == x_namemap


def test_TranslateUnit_set_namemap_SetsAttrWhenAttrIs_float_nan():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    x_nan = float("nan")
    x_namemap = namemap_shop(
        face_name=sue_str, otx_knot=x_nan, inx_knot=x_nan, unknown_str=x_nan
    )
    x_namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.namemap != x_namemap

    # WHEN
    sue_translateunit.set_namemap(x_namemap)

    # THEN
    assert sue_translateunit.namemap == x_namemap


def test_TranslateUnit_set_namemap_RaisesErrorIf_namemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_otx_knot = "/"
    x_namemap = namemap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_translateunit.otx_knot != x_namemap.otx_knot
    assert sue_translateunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_namemap_RaisesErrorIf_namemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_inx_knot = "/"
    x_namemap = namemap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_translateunit.inx_knot != x_namemap.inx_knot
    assert sue_translateunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_namemap_RaisesErrorIf_namemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_namemap = namemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_translateunit.unknown_str != x_namemap.unknown_str
    assert sue_translateunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_namemap_RaisesErrorIf_namemap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_translateunit = translateunit_shop(sue_str)
    x_namemap = namemap_shop(face_name=yao_str)
    assert sue_translateunit.face_name != x_namemap.face_name
    assert sue_translateunit.namemap != x_namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(x_namemap)
    exception_str = f"set_mapcore Error: TranslateUnit face_name is '{sue_translateunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_namemap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    static_x_namemap = namemap_shop(face_name=sue_str)
    static_x_namemap.set_otx2inx("Bob", "Bob of Portland")
    sue_translateunit.set_namemap(static_x_namemap)

    # WHEN
    gen_x_namemap = sue_translateunit.get_namemap()

    # THEN
    assert gen_x_namemap == static_x_namemap


def test_TranslateUnit_set_nameterm_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    voice_name_namemap = zia_translateunit.get_namemap()
    assert voice_name_namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_nameterm(sue_otx, sue_inx)

    # THEN
    assert voice_name_namemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_nameterm_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)

    assert zia_translateunit.nameterm_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_nameterm(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.nameterm_exists(sue_otx, sue_inx)


def test_TranslateUnit_get_inx_name_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    assert zia_translateunit._get_inx_name(sue_otx) != sue_inx

    # WHEN
    zia_translateunit.set_nameterm(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit._get_inx_name(sue_otx) == sue_inx


def test_TranslateUnit_del_nameterm_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)

    zia_translateunit.set_nameterm(sue_otx, sue_inx)
    zia_translateunit.set_nameterm(zia_str, zia_str)
    assert zia_translateunit.nameterm_exists(sue_otx, sue_inx)
    assert zia_translateunit.nameterm_exists(zia_str, zia_str)

    # WHEN
    zia_translateunit.del_nameterm(sue_otx)

    # THEN
    assert zia_translateunit.nameterm_exists(sue_otx, sue_inx) is False
    assert zia_translateunit.nameterm_exists(zia_str, zia_str)
