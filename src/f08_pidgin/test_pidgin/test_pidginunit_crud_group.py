from src.f08_pidgin.bridge_new import groupbridge_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_groupbridge_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_groupbridge = groupbridge_shop(x_face_id=sue_str)
    x_groupbridge.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.groupbridge != x_groupbridge

    # WHEN
    sue_pidginunit.set_groupbridge(x_groupbridge)

    # THEN
    assert sue_pidginunit.groupbridge == x_groupbridge


def test_PidginUnit_set_groupbridge_RaisesErrorIf_groupbridge_otx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_wall = "/"
    x_groupbridge = groupbridge_shop(x_otx_wall=slash_otx_wall, x_face_id=sue_str)
    assert sue_pidginunit.otx_wall != x_groupbridge.otx_wall
    assert sue_pidginunit.groupbridge != x_groupbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupbridge(x_groupbridge)
    exception_str = f"set_bridgecore Error: BridgeCore otx_wall is '{sue_pidginunit.otx_wall}', BridgeCore is '{slash_otx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_groupbridge_RaisesErrorIf_groupbridge_inx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_wall = "/"
    x_groupbridge = groupbridge_shop(x_inx_wall=slash_inx_wall, x_face_id=sue_str)
    assert sue_pidginunit.inx_wall != x_groupbridge.inx_wall
    assert sue_pidginunit.groupbridge != x_groupbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupbridge(x_groupbridge)
    exception_str = f"set_bridgecore Error: BridgeCore inx_wall is '{sue_pidginunit.inx_wall}', BridgeCore is '{slash_inx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_groupbridge_RaisesErrorIf_groupbridge_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_groupbridge = groupbridge_shop(
        x_unknown_word=casa_unknown_word, x_face_id=sue_str
    )
    assert sue_pidginunit.unknown_word != x_groupbridge.unknown_word
    assert sue_pidginunit.groupbridge != x_groupbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupbridge(x_groupbridge)
    exception_str = f"set_bridgecore Error: BridgeCore unknown_word is '{sue_pidginunit.unknown_word}', BridgeCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_groupbridge_RaisesErrorIf_groupbridge_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_groupbridge = groupbridge_shop(x_face_id=yao_str)
    assert sue_pidginunit.face_id != x_groupbridge.face_id
    assert sue_pidginunit.groupbridge != x_groupbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_groupbridge(x_groupbridge)
    exception_str = f"set_bridgecore Error: BridgeCore face_id is '{sue_pidginunit.face_id}', BridgeCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_groupbridge_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_groupbridge = groupbridge_shop(x_face_id=sue_str)
    static_x_groupbridge.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_groupbridge(static_x_groupbridge)

    # WHEN
    gen_x_groupbridge = sue_pidginunit.get_groupbridge()

    # THEN
    assert gen_x_groupbridge == static_x_groupbridge


def test_PidginUnit_set_group_id_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acctid_groupbridge = zia_pidginunit.get_groupbridge()
    assert acctid_groupbridge.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_group_id(sue_otx, sue_inx)

    # THEN
    assert acctid_groupbridge.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_group_id_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.group_id_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_group_id(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.group_id_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_group_id_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_group_id(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_group_id(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_group_id(sue_otx) == sue_inx


def test_PidginUnit_del_group_id_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_group_id(sue_otx, sue_inx)
    zia_pidginunit.set_group_id(zia_str, zia_str)
    assert zia_pidginunit.group_id_exists(sue_otx, sue_inx)
    assert zia_pidginunit.group_id_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_group_id(sue_otx)

    # THEN
    assert zia_pidginunit.group_id_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.group_id_exists(zia_str, zia_str)
