from src.f08_pidgin.map import labelmap_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_labelmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_labelmap = labelmap_shop(face_name=sue_str)
    x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.labelmap != x_labelmap

    # WHEN
    sue_pidginunit.set_labelmap(x_labelmap)

    # THEN
    assert sue_pidginunit.labelmap == x_labelmap


def test_PidginUnit_set_labelmap_RaisesErrorIf_labelmap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_labelmap = labelmap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_labelmap.otx_bridge
    assert sue_pidginunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_labelmap_RaisesErrorIf_labelmap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_labelmap = labelmap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_labelmap.inx_bridge
    assert sue_pidginunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_labelmap_RaisesErrorIf_labelmap_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_labelmap = labelmap_shop(unknown_word=casa_unknown_word, face_name=sue_str)
    assert sue_pidginunit.unknown_word != x_labelmap.unknown_word
    assert sue_pidginunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_labelmap_RaisesErrorIf_labelmap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_labelmap = labelmap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_labelmap.face_name
    assert sue_pidginunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_labelmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_labelmap = labelmap_shop(face_name=sue_str)
    static_x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_labelmap(static_x_labelmap)

    # WHEN
    gen_x_labelmap = sue_pidginunit.get_labelmap()

    # THEN
    assert gen_x_labelmap == static_x_labelmap


def test_PidginUnit_set_labelunit_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acct_name_labelmap = zia_pidginunit.get_labelmap()
    assert acct_name_labelmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_labelunit(sue_otx, sue_inx)

    # THEN
    assert acct_name_labelmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_labelunit_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.labelunit_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_labelunit(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.labelunit_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_label(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_labelunit(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_label(sue_otx) == sue_inx


def test_PidginUnit_del_labelunit_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_labelunit(sue_otx, sue_inx)
    zia_pidginunit.set_labelunit(zia_str, zia_str)
    assert zia_pidginunit.labelunit_exists(sue_otx, sue_inx)
    assert zia_pidginunit.labelunit_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_labelunit(sue_otx)

    # THEN
    assert zia_pidginunit.labelunit_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.labelunit_exists(zia_str, zia_str)
