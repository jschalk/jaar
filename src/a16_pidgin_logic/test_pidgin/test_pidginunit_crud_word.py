from src.a16_pidgin_logic.map import wordmap_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_wordmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_wordmap = wordmap_shop(face_name=sue_str)
    x_wordmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.wordmap != x_wordmap

    # WHEN
    sue_pidginunit.set_wordmap(x_wordmap)

    # THEN
    assert sue_pidginunit.wordmap == x_wordmap


def test_PidginUnit_set_wordmap_RaisesErrorIf_wordmap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_wordmap = wordmap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_wordmap.otx_bridge
    assert sue_pidginunit.wordmap != x_wordmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_wordmap(x_wordmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_wordmap_RaisesErrorIf_wordmap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_wordmap = wordmap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_wordmap.inx_bridge
    assert sue_pidginunit.wordmap != x_wordmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_wordmap(x_wordmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_wordmap_RaisesErrorIf_wordmap_unknown_term_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_term = "Unknown_casa"
    x_wordmap = wordmap_shop(unknown_term=casa_unknown_term, face_name=sue_str)
    assert sue_pidginunit.unknown_term != x_wordmap.unknown_term
    assert sue_pidginunit.wordmap != x_wordmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_wordmap(x_wordmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_term is '{sue_pidginunit.unknown_term}', MapCore is '{casa_unknown_term}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_wordmap_RaisesErrorIf_wordmap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_wordmap = wordmap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_wordmap.face_name
    assert sue_pidginunit.wordmap != x_wordmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_wordmap(x_wordmap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_wordmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_wordmap = wordmap_shop(face_name=sue_str)
    static_x_wordmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_wordmap(static_x_wordmap)

    # WHEN
    gen_x_wordmap = sue_pidginunit.get_wordmap()

    # THEN
    assert gen_x_wordmap == static_x_wordmap


def test_PidginUnit_set_word_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    wordid_wordmap = zia_pidginunit.get_wordmap()
    assert wordid_wordmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_word(sue_otx, sue_inx)

    # THEN
    assert wordid_wordmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_word_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.word_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_word(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.word_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_word_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_word(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_word(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_word(sue_otx) == sue_inx


def test_PidginUnit_del_word_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_word(sue_otx, sue_inx)
    zia_pidginunit.set_word(zia_str, zia_str)
    assert zia_pidginunit.word_exists(sue_otx, sue_inx)
    assert zia_pidginunit.word_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_word(sue_otx)

    # THEN
    assert zia_pidginunit.word_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.word_exists(zia_str, zia_str)
