from src.f01_road.road import default_road_delimiter_if_none, create_road
from src.f04_gift.atom_config import (
    acct_id_str,
    get_atom_args_obj_classs,
    credit_vote_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f08_filter.filter import BridgeUnit, bridgeunit_shop, default_unknown_word
from pytest import raises as pytest_raises

# from otx.f08_filter.examples.filter_env import get_test_filters_dir, env_dir_setup_cleanup

# The goal of the filter function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_default_unknown_word_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_word() == "UNKNOWN"


def test_BridgeUnit_Exists():
    # ESTABLISH
    x_bridgeunit = BridgeUnit()

    # WHEN / THEN
    assert not x_bridgeunit.obj_class
    assert not x_bridgeunit.otx_to_inx
    assert not x_bridgeunit.unknown_word
    assert not x_bridgeunit.otx_road_delimiter
    assert not x_bridgeunit.inx_road_delimiter
    assert not x_bridgeunit.explicit_label
    assert not x_bridgeunit.face_id


def test_bridgeunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    otx_to_inx = {xio_str: sue_str}
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"

    # WHEN
    acct_id_bridgeunit = bridgeunit_shop(
        x_obj_class=type_AcctID_str(),
        x_otx_to_inx=otx_to_inx,
        x_unknown_word=x_unknown_word,
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_face_id=bob_str,
    )

    # THEN
    assert acct_id_bridgeunit.obj_class == type_AcctID_str()
    assert acct_id_bridgeunit.otx_to_inx == otx_to_inx
    assert acct_id_bridgeunit.unknown_word == x_unknown_word
    assert acct_id_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert acct_id_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter
    assert acct_id_bridgeunit.explicit_label == {}
    assert acct_id_bridgeunit.face_id == bob_str


def test_bridgeunit_shop_ReturnsObj_scenario1():
    # ESTABLISH / WHEN
    cv_obj_class = get_atom_args_obj_classs().get(credit_vote_str())
    credit_vote_bridgeunit = bridgeunit_shop(cv_obj_class)

    # THEN
    assert credit_vote_bridgeunit.otx_to_inx == {}
    assert credit_vote_bridgeunit.unknown_word == default_unknown_word()
    assert credit_vote_bridgeunit.otx_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgeunit.inx_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgeunit.obj_class == cv_obj_class
    assert credit_vote_bridgeunit.face_id is None


def test_bridgeunit_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    credit_vote_bridgeunit = bridgeunit_shop(type_AcctID_str())

    # THEN
    assert credit_vote_bridgeunit.obj_class == type_AcctID_str()
    assert credit_vote_bridgeunit.otx_to_inx == {}
    assert credit_vote_bridgeunit.unknown_word == default_unknown_word()
    assert credit_vote_bridgeunit.otx_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgeunit.inx_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgeunit.face_id is None


def test_BridgeUnit_set_all_otx_to_inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    acct_id_bridgeunit = bridgeunit_shop(None, acct_id_str())
    x_otx_to_inx = {xio_str: sue_str, zia_str: zia_str}
    assert acct_id_bridgeunit.otx_to_inx != x_otx_to_inx

    # WHEN
    acct_id_bridgeunit.set_all_otx_to_inx(x_otx_to_inx)

    # THEN
    assert acct_id_bridgeunit.otx_to_inx == x_otx_to_inx


def test_BridgeUnit_set_all_otx_to_inx_RaisesErrorIf_unknown_word_IsKeyIn_otx_to_inx():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgeunit = bridgeunit_shop(None, x_unknown_word=x_unknown_word)
    x_otx_to_inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert acct_id_bridgeunit.otx_to_inx != x_otx_to_inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acct_id_bridgeunit.set_all_otx_to_inx(x_otx_to_inx, True)
    exception_str = f"otx_to_inx cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_set_all_otx_to_inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(None)
    x_otx_to_inx = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_bridgeunit.otx_to_inx != x_otx_to_inx

    # WHEN
    x_bridgeunit.set_all_otx_to_inx(x_otx_to_inx)

    # THEN
    assert x_bridgeunit.otx_to_inx == x_otx_to_inx


def test_BridgeUnit_set_otx_to_inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit.otx_to_inx == {}

    # WHEN
    x_bridgeunit.set_otx_to_inx(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.otx_to_inx == {xio_str: sue_str}


def test_BridgeUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit._get_inx_value(xio_str) != sue_str

    # WHEN
    x_bridgeunit.set_otx_to_inx(xio_str, sue_str)

    # THEN
    assert x_bridgeunit._get_inx_value(xio_str) == sue_str


def test_BridgeUnit_otx_to_inx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit.otx_to_inx_exists(xio_str, sue_str) is False
    assert x_bridgeunit.otx_to_inx_exists(xio_str, zia_str) is False
    assert x_bridgeunit.otx_to_inx_exists(xio_str, bob_str) is False
    assert x_bridgeunit.otx_to_inx_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgeunit.set_otx_to_inx(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.otx_to_inx_exists(xio_str, sue_str)
    assert x_bridgeunit.otx_to_inx_exists(xio_str, zia_str) is False
    assert x_bridgeunit.otx_to_inx_exists(xio_str, bob_str) is False
    assert x_bridgeunit.otx_to_inx_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgeunit.set_otx_to_inx(zia_str, zia_str)

    # THEN
    assert x_bridgeunit.otx_to_inx_exists(xio_str, sue_str)
    assert x_bridgeunit.otx_to_inx_exists(xio_str, zia_str) is False
    assert x_bridgeunit.otx_to_inx_exists(xio_str, bob_str) is False
    assert x_bridgeunit.otx_to_inx_exists(zia_str, zia_str)


def test_BridgeUnit_otx_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit.otx_exists(xio_str) is False
    assert x_bridgeunit.otx_exists(sue_str) is False
    assert x_bridgeunit.otx_exists(bob_str) is False
    assert x_bridgeunit.otx_exists(zia_str) is False

    # WHEN
    x_bridgeunit.set_otx_to_inx(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.otx_exists(xio_str)
    assert x_bridgeunit.otx_exists(sue_str) is False
    assert x_bridgeunit.otx_exists(bob_str) is False
    assert x_bridgeunit.otx_exists(zia_str) is False

    # WHEN
    x_bridgeunit.set_otx_to_inx(zia_str, zia_str)

    # THEN
    assert x_bridgeunit.otx_exists(xio_str)
    assert x_bridgeunit.otx_exists(sue_str) is False
    assert x_bridgeunit.otx_exists(bob_str) is False
    assert x_bridgeunit.otx_exists(zia_str)


def test_BridgeUnit_del_otx_to_inx_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgeunit = bridgeunit_shop(None)
    x_bridgeunit.set_otx_to_inx(xio_str, sue_str)
    assert x_bridgeunit.otx_to_inx_exists(xio_str, sue_str)

    # WHEN
    x_bridgeunit.del_otx_to_inx(xio_str)

    # THEN
    assert x_bridgeunit.otx_to_inx_exists(xio_str, sue_str) is False


def test_BridgeUnit_unknown_word_in_otx_to_inx_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(None, x_unknown_word=x_unknown_word)
    x_bridgeunit.set_otx_to_inx(xio_str, sue_str)
    assert x_bridgeunit._unknown_word_in_otx_to_inx() is False

    # WHEN
    x_bridgeunit.set_otx_to_inx(zia_str, x_unknown_word)

    # THEN
    assert x_bridgeunit._unknown_word_in_otx_to_inx()


def test_BridgeUnit_set_explicit_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit.explicit_label == {}

    # WHEN
    x_bridgeunit.set_explicit_label(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.explicit_label == {xio_str: sue_str}


def test_BridgeUnit_set_explicit_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit.explicit_label == {}

    # WHEN
    x_bridgeunit.set_explicit_label(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.explicit_label == {xio_str: sue_str}


def test_BridgeUnit_set_explicit_label_RaisesExceptionWhen_road_delimiter_In_otx_label():
    # ESTABLISH
    x_bridgeunit = bridgeunit_shop(None)
    sue_otx = f"Sue{x_bridgeunit.otx_road_delimiter}"
    sue_inx = "Sue"
    assert x_bridgeunit.explicit_label == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_bridgeunit.set_explicit_label(sue_otx, sue_inx)
    exception_str = f"explicit_label cannot have otx_label '{sue_otx}'. It must be not have road_delimiter {x_bridgeunit.otx_road_delimiter}."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_set_explicit_label_RaisesExceptionWhen_road_delimiter_In_inx_label():
    # ESTABLISH
    x_bridgeunit = bridgeunit_shop(None)
    sue_inx = f"Sue{x_bridgeunit.otx_road_delimiter}"
    sue_otx = "Sue"
    assert x_bridgeunit.explicit_label == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_bridgeunit.set_explicit_label(sue_otx, sue_inx)
    exception_str = f"explicit_label cannot have inx_label '{sue_inx}'. It must be not have road_delimiter {x_bridgeunit.inx_road_delimiter}."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_get_explicit_inx_label_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit._get_explicit_inx_label(xio_str) != sue_str

    # WHEN
    x_bridgeunit.set_explicit_label(xio_str, sue_str)

    # THEN
    assert x_bridgeunit._get_explicit_inx_label(xio_str) == sue_str


def test_BridgeUnit_explicit_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit.explicit_label_exists(xio_str, sue_str) is False
    assert x_bridgeunit.explicit_label_exists(xio_str, zia_str) is False
    assert x_bridgeunit.explicit_label_exists(xio_str, bob_str) is False
    assert x_bridgeunit.explicit_label_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgeunit.set_explicit_label(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.explicit_label_exists(xio_str, sue_str)
    assert x_bridgeunit.explicit_label_exists(xio_str, zia_str) is False
    assert x_bridgeunit.explicit_label_exists(xio_str, bob_str) is False
    assert x_bridgeunit.explicit_label_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgeunit.set_explicit_label(zia_str, zia_str)

    # THEN
    assert x_bridgeunit.explicit_label_exists(xio_str, sue_str)
    assert x_bridgeunit.explicit_label_exists(xio_str, zia_str) is False
    assert x_bridgeunit.explicit_label_exists(xio_str, bob_str) is False
    assert x_bridgeunit.explicit_label_exists(zia_str, zia_str)


def test_BridgeUnit_explicit_otx_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgeunit = bridgeunit_shop(None)
    assert x_bridgeunit.explicit_otx_label_exists(xio_str) is False
    assert x_bridgeunit.explicit_otx_label_exists(sue_str) is False
    assert x_bridgeunit.explicit_otx_label_exists(bob_str) is False
    assert x_bridgeunit.explicit_otx_label_exists(zia_str) is False

    # WHEN
    x_bridgeunit.set_explicit_label(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.explicit_otx_label_exists(xio_str)
    assert x_bridgeunit.explicit_otx_label_exists(sue_str) is False
    assert x_bridgeunit.explicit_otx_label_exists(bob_str) is False
    assert x_bridgeunit.explicit_otx_label_exists(zia_str) is False

    # WHEN
    x_bridgeunit.set_explicit_label(zia_str, zia_str)

    # THEN
    assert x_bridgeunit.explicit_otx_label_exists(xio_str)
    assert x_bridgeunit.explicit_otx_label_exists(sue_str) is False
    assert x_bridgeunit.explicit_otx_label_exists(bob_str) is False
    assert x_bridgeunit.explicit_otx_label_exists(zia_str)


def test_BridgeUnit_del_explicit_label_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgeunit = bridgeunit_shop(None)
    x_bridgeunit.set_explicit_label(xio_str, sue_str)
    assert x_bridgeunit.explicit_label_exists(xio_str, sue_str)

    # WHEN
    x_bridgeunit.del_explicit_label(xio_str)

    # THEN
    assert x_bridgeunit.explicit_label_exists(xio_str, sue_str) is False


def test_BridgeUnit_set_explicit_label_Edits_otx_to_inx():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_music45_str, casa_otx_str)
    casa_inx_road = create_road(inx_music87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)
    x_bridgeunit = bridgeunit_shop(type_RoadUnit_str())
    x_bridgeunit.set_otx_to_inx(otx_music45_str, inx_music87_str)
    x_bridgeunit.set_otx_to_inx(casa_otx_road, casa_inx_road)
    x_bridgeunit.set_otx_to_inx(clean_otx_road, clean_inx_road)
    x_bridgeunit.set_otx_to_inx(sweep_otx_road, sweep_inx_road)
    assert x_bridgeunit.otx_to_inx_exists(otx_music45_str, inx_music87_str)
    assert x_bridgeunit.otx_to_inx_exists(casa_otx_road, casa_inx_road)
    assert x_bridgeunit.otx_to_inx_exists(clean_otx_road, clean_inx_road)
    assert x_bridgeunit.otx_to_inx_exists(sweep_otx_road, sweep_inx_road)

    # WHEN
    menage_inx_str = "menage"
    x_bridgeunit.set_explicit_label(clean_otx_str, menage_inx_str)

    # THEN
    menage_inx_road = create_road(casa_inx_road, menage_inx_str)
    sweep_menage_inx_road = create_road(menage_inx_road, sweep_str)
    assert x_bridgeunit.otx_to_inx_exists(otx_music45_str, inx_music87_str)
    assert x_bridgeunit.otx_to_inx_exists(casa_otx_road, casa_inx_road)
    assert x_bridgeunit.otx_to_inx_exists(clean_otx_road, menage_inx_road)
    assert x_bridgeunit.otx_to_inx_exists(sweep_otx_road, sweep_menage_inx_road)
