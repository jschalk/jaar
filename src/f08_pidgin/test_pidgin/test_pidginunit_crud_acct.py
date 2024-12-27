from src.f08_pidgin.map import acctmap_shop
from src.f08_pidgin.pidgin import pidginunit_shop
from pytest import raises as pytest_raises


def test_PidginUnit_set_acctmap_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_acctmap = acctmap_shop(face_id=sue_str)
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
        face_id=sue_str, otx_wall=x_nan, inx_wall=x_nan, unknown_word=x_nan
    )
    x_acctmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN
    sue_pidginunit.set_acctmap(x_acctmap)

    # THEN
    assert sue_pidginunit.acctmap == x_acctmap


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_otx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_wall = "/"
    x_acctmap = acctmap_shop(otx_wall=slash_otx_wall, face_id=sue_str)
    assert sue_pidginunit.otx_wall != x_acctmap.otx_wall
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_wall is '{sue_pidginunit.otx_wall}', MapCore is '{slash_otx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_inx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_wall = "/"
    x_acctmap = acctmap_shop(inx_wall=slash_inx_wall, face_id=sue_str)
    assert sue_pidginunit.inx_wall != x_acctmap.inx_wall
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_wall is '{sue_pidginunit.inx_wall}', MapCore is '{slash_inx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    x_acctmap = acctmap_shop(unknown_word=casa_unknown_word, face_id=sue_str)
    assert sue_pidginunit.unknown_word != x_acctmap.unknown_word
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_acctmap_RaisesErrorIf_acctmap_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    x_acctmap = acctmap_shop(face_id=yao_str)
    assert sue_pidginunit.face_id != x_acctmap.face_id
    assert sue_pidginunit.acctmap != x_acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(x_acctmap)
    exception_str = f"set_mapcore Error: PidginUnit face_id is '{sue_pidginunit.face_id}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_acctmap_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_x_acctmap = acctmap_shop(face_id=sue_str)
    static_x_acctmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pidginunit.set_acctmap(static_x_acctmap)

    # WHEN
    gen_x_acctmap = sue_pidginunit.get_acctmap()

    # THEN
    assert gen_x_acctmap == static_x_acctmap


def test_PidginUnit_set_acct_id_SetsAttr_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acct_id_acctmap = zia_pidginunit.get_acctmap()
    assert acct_id_acctmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_acct_id(sue_otx, sue_inx)

    # THEN
    assert acct_id_acctmap.otx2inx_exists(sue_otx, sue_inx)


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
