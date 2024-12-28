from src.f08_pidgin.map import groupmap_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_groupmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_groupmap = groupmap_shop(face_name=sue_str)
    x_groupmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.groupmap != x_groupmap

    # WHEN
    sue_pidginunit.set_groupmap(x_groupmap)

    # THEN
    assert sue_pidginunit.groupmap == x_groupmap


def test_PidginUnit_set_groupmap_RaisesErrorIf_groupmap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_groupmap = groupmap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_groupmap.otx_bridge
    assert sue_pidginunit.groupmap != x_groupmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupmap(x_groupmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_groupmap_RaisesErrorIf_groupmap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_groupmap = groupmap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_groupmap.inx_bridge
    assert sue_pidginunit.groupmap != x_groupmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupmap(x_groupmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_groupmap_RaisesErrorIf_groupmap_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_groupmap = groupmap_shop(unknown_word=casa_unknown_word, face_name=sue_str)
    assert sue_pidginunit.unknown_word != x_groupmap.unknown_word
    assert sue_pidginunit.groupmap != x_groupmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupmap(x_groupmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_groupmap_RaisesErrorIf_groupmap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_groupmap = groupmap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_groupmap.face_name
    assert sue_pidginunit.groupmap != x_groupmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupmap(x_groupmap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_groupmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_groupmap = groupmap_shop(face_name=sue_str)
    static_x_groupmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_groupmap(static_x_groupmap)

    # WHEN
    gen_x_groupmap = sue_pidginunit.get_groupmap()

    # THEN
    assert gen_x_groupmap == static_x_groupmap


def test_PidginUnit_set_group_label_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acct_name_groupmap = zia_pidginunit.get_groupmap()
    assert acct_name_groupmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_group_label(sue_otx, sue_inx)

    # THEN
    assert acct_name_groupmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_group_label_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.group_label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_group_label(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.group_label_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_label(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_group_label(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_label(sue_otx) == sue_inx


def test_PidginUnit_del_group_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_group_label(sue_otx, sue_inx)
    zia_pidginunit.set_group_label(zia_str, zia_str)
    assert zia_pidginunit.group_label_exists(sue_otx, sue_inx)
    assert zia_pidginunit.group_label_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_group_label(sue_otx)

    # THEN
    assert zia_pidginunit.group_label_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.group_label_exists(zia_str, zia_str)
