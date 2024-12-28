from src.f08_pidgin.map import acctmap_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_acctmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_acctmap = acctmap_shop(face_name=sue_str)
    x_acctmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN
    sue_pidginunit.set_acctmap(x_acctmap)

    # THEN
    assert sue_pidginunit.acctmap == x_acctmap


def test_PidginUnit_set_acctmap_SetsAttrWhenAttrIs_float_nan():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_nan = float("nan")
    x_acctmap = acctmap_shop(
        face_name=sue_str, otx_bridge=x_nan, inx_bridge=x_nan, unknown_word=x_nan
    )
    x_acctmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN
    sue_pidginunit.set_acctmap(x_acctmap)

    # THEN
    assert sue_pidginunit.acctmap == x_acctmap


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    x_acctmap = acctmap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != x_acctmap.otx_bridge
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    x_acctmap = acctmap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != x_acctmap.inx_bridge
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_acctmap = acctmap_shop(unknown_word=casa_unknown_word, face_name=sue_str)
    assert sue_pidginunit.unknown_word != x_acctmap.unknown_word
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_acctmap = acctmap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != x_acctmap.face_name
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_acctmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_acctmap = acctmap_shop(face_name=sue_str)
    static_x_acctmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_acctmap(static_x_acctmap)

    # WHEN
    gen_x_acctmap = sue_pidginunit.get_acctmap()

    # THEN
    assert gen_x_acctmap == static_x_acctmap


def test_PidginUnit_set_acct_name_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acct_name_acctmap = zia_pidginunit.get_acctmap()
    assert acct_name_acctmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_acct_name(sue_otx, sue_inx)

    # THEN
    assert acct_name_acctmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_acct_name_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    assert zia_pidginunit.acct_name_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_acct_name(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.acct_name_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_acct_name_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_acct_name(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_acct_name(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_acct_name(sue_otx) == sue_inx


def test_PidginUnit_del_acct_name_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)

    zia_pidginunit.set_acct_name(sue_otx, sue_inx)
    zia_pidginunit.set_acct_name(zia_str, zia_str)
    assert zia_pidginunit.acct_name_exists(sue_otx, sue_inx)
    assert zia_pidginunit.acct_name_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_acct_name(sue_otx)

    # THEN
    assert zia_pidginunit.acct_name_exists(sue_otx, sue_inx) is False
    assert zia_pidginunit.acct_name_exists(zia_str, zia_str)
