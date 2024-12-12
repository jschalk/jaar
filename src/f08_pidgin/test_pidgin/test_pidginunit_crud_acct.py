from src.f08_pidgin.bridge import acctbridge_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_acctbridge_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_acctbridge = acctbridge_shop(face_id=sue_str)
    x_acctbridge.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.acctbridge != x_acctbridge

    # WHEN
    sue_pidginunit.set_acctbridge(x_acctbridge)

    # THEN
    assert sue_pidginunit.acctbridge == x_acctbridge


def test_PidginUnit_set_acctbridge_SetsAttrWhenAttrIs_float_nan():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_nan = float("nan")
    x_acctbridge = acctbridge_shop(
        face_id=sue_str, otx_wall=x_nan, inx_wall=x_nan, unknown_word=x_nan
    )
    x_acctbridge.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.acctbridge != x_acctbridge

    # WHEN
    sue_pidginunit.set_acctbridge(x_acctbridge)

    # THEN
    assert sue_pidginunit.acctbridge == x_acctbridge


def test_PidginUnit_set_acctbridge_RaisesErrorIf_acctbridge_otx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_wall = "/"
    x_acctbridge = acctbridge_shop(otx_wall=slash_otx_wall, face_id=sue_str)
    assert sue_pidginunit.otx_wall != x_acctbridge.otx_wall
    assert sue_pidginunit.acctbridge != x_acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(x_acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit otx_wall is '{sue_pidginunit.otx_wall}', BridgeCore is '{slash_otx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctbridge_RaisesErrorIf_acctbridge_inx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_wall = "/"
    x_acctbridge = acctbridge_shop(inx_wall=slash_inx_wall, face_id=sue_str)
    assert sue_pidginunit.inx_wall != x_acctbridge.inx_wall
    assert sue_pidginunit.acctbridge != x_acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(x_acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit inx_wall is '{sue_pidginunit.inx_wall}', BridgeCore is '{slash_inx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctbridge_RaisesErrorIf_acctbridge_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_acctbridge = acctbridge_shop(unknown_word=casa_unknown_word, face_id=sue_str)
    assert sue_pidginunit.unknown_word != x_acctbridge.unknown_word
    assert sue_pidginunit.acctbridge != x_acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(x_acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', BridgeCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctbridge_RaisesErrorIf_acctbridge_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_acctbridge = acctbridge_shop(face_id=yao_str)
    assert sue_pidginunit.face_id != x_acctbridge.face_id
    assert sue_pidginunit.acctbridge != x_acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(x_acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit face_id is '{sue_pidginunit.face_id}', BridgeCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_acctbridge_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_acctbridge = acctbridge_shop(face_id=sue_str)
    static_x_acctbridge.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_acctbridge(static_x_acctbridge)

    # WHEN
    gen_x_acctbridge = sue_pidginunit.get_acctbridge()

    # THEN
    assert gen_x_acctbridge == static_x_acctbridge


def test_PidginUnit_set_acct_id_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acct_id_acctbridge = zia_pidginunit.get_acctbridge()
    assert acct_id_acctbridge.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_acct_id(sue_otx, sue_inx)

    # THEN
    assert acct_id_acctbridge.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_acct_id_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.acct_id_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_acct_id(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.acct_id_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_acct_id_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_acct_id(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_acct_id(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_acct_id(sue_otx) == sue_inx


def test_PidginUnit_del_acct_id_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_acct_id(sue_otx, sue_inx)
    zia_pidginunit.set_acct_id(zia_str, zia_str)
    assert zia_pidginunit.acct_id_exists(sue_otx, sue_inx)
    assert zia_pidginunit.acct_id_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_acct_id(sue_otx)

    # THEN
    assert zia_pidginunit.acct_id_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.acct_id_exists(zia_str, zia_str)
