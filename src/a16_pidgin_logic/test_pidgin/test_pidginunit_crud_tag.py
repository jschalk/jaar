from src.a16_pidgin_logic.map import tagmap_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_tagmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_tagmap = tagmap_shop(face_name=sue_str)
    x_tagmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.tagmap != x_tagmap

    # WHEN
    sue_pidginunit.set_tagmap(x_tagmap)

    # THEN
    assert sue_pidginunit.tagmap == x_tagmap


def test_PidginUnit_set_tagmap_RaisesErrorIf_tagmap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_tagmap = tagmap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_tagmap.otx_bridge
    assert sue_pidginunit.tagmap != x_tagmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_tagmap(x_tagmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_tagmap_RaisesErrorIf_tagmap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_tagmap = tagmap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_tagmap.inx_bridge
    assert sue_pidginunit.tagmap != x_tagmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_tagmap(x_tagmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_tagmap_RaisesErrorIf_tagmap_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_tagmap = tagmap_shop(unknown_word=casa_unknown_word, face_name=sue_str)
    assert sue_pidginunit.unknown_word != x_tagmap.unknown_word
    assert sue_pidginunit.tagmap != x_tagmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_tagmap(x_tagmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_tagmap_RaisesErrorIf_tagmap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_tagmap = tagmap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_tagmap.face_name
    assert sue_pidginunit.tagmap != x_tagmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_tagmap(x_tagmap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_tagmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_tagmap = tagmap_shop(face_name=sue_str)
    static_x_tagmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_tagmap(static_x_tagmap)

    # WHEN
    gen_x_tagmap = sue_pidginunit.get_tagmap()

    # THEN
    assert gen_x_tagmap == static_x_tagmap


def test_PidginUnit_set_tag_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    tagid_tagmap = zia_pidginunit.get_tagmap()
    assert tagid_tagmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_tag(sue_otx, sue_inx)

    # THEN
    assert tagid_tagmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_tag_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.tag_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_tag(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.tag_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_tag_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_tag(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_tag(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_tag(sue_otx) == sue_inx


def test_PidginUnit_del_tag_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_tag(sue_otx, sue_inx)
    zia_pidginunit.set_tag(zia_str, zia_str)
    assert zia_pidginunit.tag_exists(sue_otx, sue_inx)
    assert zia_pidginunit.tag_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_tag(sue_otx)

    # THEN
    assert zia_pidginunit.tag_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.tag_exists(zia_str, zia_str)
