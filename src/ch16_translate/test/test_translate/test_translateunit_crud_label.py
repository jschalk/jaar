from pytest import raises as pytest_raises
from src.ch16_translate.map import labelmap_shop
from src.ch16_translate.translate_main import translateunit_shop


def test_TranslateUnit_set_labelmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    x_labelmap = labelmap_shop(face_name=sue_str)
    x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN
    sue_translateunit.set_labelmap(x_labelmap)

    # THEN
    assert sue_translateunit.labelmap == x_labelmap


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_otx_knot = "/"
    x_labelmap = labelmap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_translateunit.otx_knot != x_labelmap.otx_knot
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_inx_knot = "/"
    x_labelmap = labelmap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_translateunit.inx_knot != x_labelmap.inx_knot
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_labelmap = labelmap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_translateunit.unknown_str != x_labelmap.unknown_str
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_translateunit = translateunit_shop(sue_str)
    x_labelmap = labelmap_shop(face_name=yao_str)
    assert sue_translateunit.face_name != x_labelmap.face_name
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit face_name is '{sue_translateunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_labelmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    static_x_labelmap = labelmap_shop(face_name=sue_str)
    static_x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    sue_translateunit.set_labelmap(static_x_labelmap)

    # WHEN
    gen_x_labelmap = sue_translateunit.get_labelmap()

    # THEN
    assert gen_x_labelmap == static_x_labelmap


def test_TranslateUnit_set_label_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    labelid_labelmap = zia_translateunit.get_labelmap()
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_label(sue_otx, sue_inx)

    # THEN
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_get_inx_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    assert zia_translateunit._get_inx_label(sue_otx) != sue_inx

    # WHEN
    zia_translateunit.set_label(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit._get_inx_label(sue_otx) == sue_inx


def test_TranslateUnit_del_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)

    zia_translateunit.set_label(sue_otx, sue_inx)
    zia_translateunit.set_label(zia_str, zia_str)
    assert zia_translateunit.label_exists(sue_otx, sue_inx)
    assert zia_translateunit.label_exists(zia_str, zia_str)

    # WHEN
    zia_translateunit.del_label(sue_otx)

    # THEN
    assert zia_translateunit.label_exists(sue_otx, sue_inx) is False
    assert zia_translateunit.label_exists(zia_str, zia_str)
