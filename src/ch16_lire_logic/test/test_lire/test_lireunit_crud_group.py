from pytest import raises as pytest_raises
from src.ch16_lire_logic.lire_main import lireunit_shop
from src.ch16_lire_logic.map import titlemap_shop


def test_LireUnit_set_titlemap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    x_titlemap = titlemap_shop(face_name=sue_str)
    x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_lireunit.titlemap != x_titlemap

    # WHEN
    sue_lireunit.set_titlemap(x_titlemap)

    # THEN
    assert sue_lireunit.titlemap == x_titlemap


def test_LireUnit_set_titlemap_RaisesErrorIf_titlemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    slash_otx_knot = "/"
    x_titlemap = titlemap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_lireunit.otx_knot != x_titlemap.otx_knot
    assert sue_lireunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: LireUnit otx_knot is '{sue_lireunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_set_titlemap_RaisesErrorIf_titlemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    slash_inx_knot = "/"
    x_titlemap = titlemap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_lireunit.inx_knot != x_titlemap.inx_knot
    assert sue_lireunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: LireUnit inx_knot is '{sue_lireunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_set_titlemap_RaisesErrorIf_titlemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    x_titlemap = titlemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_lireunit.unknown_str != x_titlemap.unknown_str
    assert sue_lireunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: LireUnit unknown_str is '{sue_lireunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_set_titlemap_RaisesErrorIf_titlemap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_lireunit = lireunit_shop(sue_str)
    x_titlemap = titlemap_shop(face_name=yao_str)
    assert sue_lireunit.face_name != x_titlemap.face_name
    assert sue_lireunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: LireUnit face_name is '{sue_lireunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_get_titlemap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    static_x_titlemap = titlemap_shop(face_name=sue_str)
    static_x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    sue_lireunit.set_titlemap(static_x_titlemap)

    # WHEN
    gen_x_titlemap = sue_lireunit.get_titlemap()

    # THEN
    assert gen_x_titlemap == static_x_titlemap


def test_LireUnit_set_titleterm_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    voice_name_titlemap = zia_lireunit.get_titlemap()
    assert voice_name_titlemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_lireunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert voice_name_titlemap.otx2inx_exists(sue_otx, sue_inx)


def test_LireUnit_titleterm_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)

    assert zia_lireunit.titleterm_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_lireunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_lireunit.titleterm_exists(sue_otx, sue_inx)


def test_LireUnit_get_inx_title_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    assert zia_lireunit._get_inx_title(sue_otx) != sue_inx

    # WHEN
    zia_lireunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_lireunit._get_inx_title(sue_otx) == sue_inx


def test_LireUnit_del_titleterm_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)

    zia_lireunit.set_titleterm(sue_otx, sue_inx)
    zia_lireunit.set_titleterm(zia_str, zia_str)
    assert zia_lireunit.titleterm_exists(sue_otx, sue_inx)
    assert zia_lireunit.titleterm_exists(zia_str, zia_str)

    # WHEN
    zia_lireunit.del_titleterm(sue_otx)

    # THEN
    assert zia_lireunit.titleterm_exists(sue_otx, sue_inx) is False
    assert zia_lireunit.titleterm_exists(zia_str, zia_str)
