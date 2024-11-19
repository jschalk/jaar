from src.f08_pidgin.bridge_new import nodebridge_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_nodebridge_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_nodebridge = nodebridge_shop(x_face_id=sue_str)
    x_nodebridge.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.nodebridge != x_nodebridge

    # WHEN
    sue_pidginunit.set_nodebridge(x_nodebridge)

    # THEN
    assert sue_pidginunit.nodebridge == x_nodebridge


def test_PidginUnit_set_nodebridge_RaisesErrorIf_nodebridge_otx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_wall = "/"
    x_nodebridge = nodebridge_shop(x_otx_wall=slash_otx_wall, x_face_id=sue_str)
    assert sue_pidginunit.otx_wall != x_nodebridge.otx_wall
    assert sue_pidginunit.nodebridge != x_nodebridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_nodebridge(x_nodebridge)
    exception_str = f"set_bridgecore Error: BridgeCore otx_wall is '{sue_pidginunit.otx_wall}', BridgeCore is '{slash_otx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_nodebridge_RaisesErrorIf_nodebridge_inx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_wall = "/"
    x_nodebridge = nodebridge_shop(x_inx_wall=slash_inx_wall, x_face_id=sue_str)
    assert sue_pidginunit.inx_wall != x_nodebridge.inx_wall
    assert sue_pidginunit.nodebridge != x_nodebridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_nodebridge(x_nodebridge)
    exception_str = f"set_bridgecore Error: BridgeCore inx_wall is '{sue_pidginunit.inx_wall}', BridgeCore is '{slash_inx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_nodebridge_RaisesErrorIf_nodebridge_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_nodebridge = nodebridge_shop(x_unknown_word=casa_unknown_word, x_face_id=sue_str)
    assert sue_pidginunit.unknown_word != x_nodebridge.unknown_word
    assert sue_pidginunit.nodebridge != x_nodebridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_nodebridge(x_nodebridge)
    exception_str = f"set_bridgecore Error: BridgeCore unknown_word is '{sue_pidginunit.unknown_word}', BridgeCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_nodebridge_RaisesErrorIf_nodebridge_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_nodebridge = nodebridge_shop(x_face_id=yao_str)
    assert sue_pidginunit.face_id != x_nodebridge.face_id
    assert sue_pidginunit.nodebridge != x_nodebridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_nodebridge(x_nodebridge)
    exception_str = f"set_bridgecore Error: BridgeCore face_id is '{sue_pidginunit.face_id}', BridgeCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_nodebridge_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_nodebridge = nodebridge_shop(x_face_id=sue_str)
    static_x_nodebridge.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_nodebridge(static_x_nodebridge)

    # WHEN
    gen_x_nodebridge = sue_pidginunit.get_nodebridge()

    # THEN
    assert gen_x_nodebridge == static_x_nodebridge


def test_PidginUnit_set_node_id_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    nodeid_nodebridge = zia_pidginunit.get_nodebridge()
    assert nodeid_nodebridge.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_node_id(sue_otx, sue_inx)

    # THEN
    assert nodeid_nodebridge.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_node_id_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.node_id_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_node_id(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.node_id_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_node_id_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_node_id(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_node_id(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_node_id(sue_otx) == sue_inx


def test_PidginUnit_del_node_id_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_node_id(sue_otx, sue_inx)
    zia_pidginunit.set_node_id(zia_str, zia_str)
    assert zia_pidginunit.node_id_exists(sue_otx, sue_inx)
    assert zia_pidginunit.node_id_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_node_id(sue_otx)

    # THEN
    assert zia_pidginunit.node_id_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.node_id_exists(zia_str, zia_str)
