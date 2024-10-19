from src.f01_road.road import default_road_delimiter_if_none, create_road
from src.f04_gift.atom_config import (
    acct_id_str,
    get_atom_args_python_types,
    credit_vote_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f09_filter.bridge import BridgeKind, bridgekind_shop, default_unknown_word
from pytest import raises as pytest_raises

# from src.f09_filter.examples.filter_env import get_test_filters_dir, env_dir_setup_cleanup

# The goal of the filter function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_default_unknown_word_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_word() == "UNKNOWN"


def test_BridgeKind_Exists():
    # ESTABLISH
    x_bridgekind = BridgeKind()

    # WHEN / THEN
    assert not x_bridgekind.python_type
    assert not x_bridgekind.src_to_dst
    assert not x_bridgekind.unknown_word
    assert not x_bridgekind.src_road_delimiter
    assert not x_bridgekind.dst_road_delimiter
    assert not x_bridgekind.explicit_label_map
    assert not x_bridgekind.face_id


def test_bridgekind_shop_ReturnsObj_scenario0():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    src_to_dst = {xio_str: sue_str}
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"

    # WHEN
    acct_id_bridgekind = bridgekind_shop(
        x_python_type=type_AcctID_str(),
        x_src_to_dst=src_to_dst,
        x_unknown_word=x_unknown_word,
        x_src_road_delimiter=slash_src_road_delimiter,
        x_dst_road_delimiter=colon_dst_road_delimiter,
        x_face_id=bob_str,
    )

    # THEN
    assert acct_id_bridgekind.python_type == type_AcctID_str()
    assert acct_id_bridgekind.src_to_dst == src_to_dst
    assert acct_id_bridgekind.unknown_word == x_unknown_word
    assert acct_id_bridgekind.src_road_delimiter == slash_src_road_delimiter
    assert acct_id_bridgekind.dst_road_delimiter == colon_dst_road_delimiter
    assert acct_id_bridgekind.explicit_label_map == {}
    assert acct_id_bridgekind.face_id == bob_str


def test_bridgekind_shop_ReturnsObj_scenario1():
    # ESTABLISH / WHEN
    cv_python_type = get_atom_args_python_types().get(credit_vote_str())
    credit_vote_bridgekind = bridgekind_shop(cv_python_type)

    # THEN
    assert credit_vote_bridgekind.src_to_dst == {}
    assert credit_vote_bridgekind.unknown_word == default_unknown_word()
    assert credit_vote_bridgekind.src_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgekind.dst_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgekind.python_type == cv_python_type
    assert credit_vote_bridgekind.face_id is None


def test_bridgekind_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    credit_vote_bridgekind = bridgekind_shop(type_AcctID_str())

    # THEN
    assert credit_vote_bridgekind.python_type == type_AcctID_str()
    assert credit_vote_bridgekind.src_to_dst == {}
    assert credit_vote_bridgekind.unknown_word == default_unknown_word()
    assert credit_vote_bridgekind.src_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgekind.dst_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgekind.face_id is None


def test_BridgeKind_set_all_src_to_dst_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    acct_id_bridgekind = bridgekind_shop(None, acct_id_str())
    x_src_to_dst = {xio_str: sue_str, zia_str: zia_str}
    assert acct_id_bridgekind.src_to_dst != x_src_to_dst

    # WHEN
    acct_id_bridgekind.set_all_src_to_dst(x_src_to_dst)

    # THEN
    assert acct_id_bridgekind.src_to_dst == x_src_to_dst


def test_BridgeKind_set_all_src_to_dst_RaisesErrorIf_unknown_word_IsKeyIn_src_to_dst():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(None, x_unknown_word=x_unknown_word)
    x_src_to_dst = {xio_str: sue_str, x_unknown_word: zia_str}
    assert acct_id_bridgekind.src_to_dst != x_src_to_dst

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acct_id_bridgekind.set_all_src_to_dst(x_src_to_dst, True)
    exception_str = f"src_to_dst cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_BridgeKind_set_all_src_to_dst_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    x_bridgekind = bridgekind_shop(None)
    x_src_to_dst = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_bridgekind.src_to_dst != x_src_to_dst

    # WHEN
    x_bridgekind.set_all_src_to_dst(x_src_to_dst)

    # THEN
    assert x_bridgekind.src_to_dst == x_src_to_dst


def test_BridgeKind_set_src_to_dst_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind.src_to_dst == {}

    # WHEN
    x_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert x_bridgekind.src_to_dst == {xio_str: sue_str}


def test_BridgeKind_get_dst_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind._get_dst_value(xio_str) != sue_str

    # WHEN
    x_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert x_bridgekind._get_dst_value(xio_str) == sue_str


def test_BridgeKind_src_to_dst_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind.src_to_dst_exists(xio_str, sue_str) is False
    assert x_bridgekind.src_to_dst_exists(xio_str, zia_str) is False
    assert x_bridgekind.src_to_dst_exists(xio_str, bob_str) is False
    assert x_bridgekind.src_to_dst_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert x_bridgekind.src_to_dst_exists(xio_str, sue_str)
    assert x_bridgekind.src_to_dst_exists(xio_str, zia_str) is False
    assert x_bridgekind.src_to_dst_exists(xio_str, bob_str) is False
    assert x_bridgekind.src_to_dst_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgekind.set_src_to_dst(zia_str, zia_str)

    # THEN
    assert x_bridgekind.src_to_dst_exists(xio_str, sue_str)
    assert x_bridgekind.src_to_dst_exists(xio_str, zia_str) is False
    assert x_bridgekind.src_to_dst_exists(xio_str, bob_str) is False
    assert x_bridgekind.src_to_dst_exists(zia_str, zia_str)


def test_BridgeKind_src_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind.src_exists(xio_str) is False
    assert x_bridgekind.src_exists(sue_str) is False
    assert x_bridgekind.src_exists(bob_str) is False
    assert x_bridgekind.src_exists(zia_str) is False

    # WHEN
    x_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert x_bridgekind.src_exists(xio_str)
    assert x_bridgekind.src_exists(sue_str) is False
    assert x_bridgekind.src_exists(bob_str) is False
    assert x_bridgekind.src_exists(zia_str) is False

    # WHEN
    x_bridgekind.set_src_to_dst(zia_str, zia_str)

    # THEN
    assert x_bridgekind.src_exists(xio_str)
    assert x_bridgekind.src_exists(sue_str) is False
    assert x_bridgekind.src_exists(bob_str) is False
    assert x_bridgekind.src_exists(zia_str)


def test_BridgeKind_del_src_to_dst_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgekind = bridgekind_shop(None)
    x_bridgekind.set_src_to_dst(xio_str, sue_str)
    assert x_bridgekind.src_to_dst_exists(xio_str, sue_str)

    # WHEN
    x_bridgekind.del_src_to_dst(xio_str)

    # THEN
    assert x_bridgekind.src_to_dst_exists(xio_str, sue_str) is False


def test_BridgeKind_unknown_word_in_src_to_dst_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    x_bridgekind = bridgekind_shop(None, x_unknown_word=x_unknown_word)
    x_bridgekind.set_src_to_dst(xio_str, sue_str)
    assert x_bridgekind._unknown_word_in_src_to_dst() is False

    # WHEN
    x_bridgekind.set_src_to_dst(zia_str, x_unknown_word)

    # THEN
    assert x_bridgekind._unknown_word_in_src_to_dst()


def test_BridgeKind_set_explicit_label_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind.explicit_label_map == {}

    # WHEN
    x_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert x_bridgekind.explicit_label_map == {xio_str: sue_str}


def test_BridgeKind_set_explicit_label_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind.explicit_label_map == {}

    # WHEN
    x_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert x_bridgekind.explicit_label_map == {xio_str: sue_str}


def test_BridgeKind_set_explicit_label_map_RaisesExceptionWhen_road_delimiter_In_src_label():
    # ESTABLISH
    x_bridgekind = bridgekind_shop(None)
    sue_src = f"Sue{x_bridgekind.src_road_delimiter}"
    sue_dst = "Sue"
    assert x_bridgekind.explicit_label_map == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_bridgekind.set_explicit_label_map(sue_src, sue_dst)
    exception_str = f"explicit_label_map cannot have src_label '{sue_src}'. It must be not have road_delimiter {x_bridgekind.src_road_delimiter}."
    assert str(excinfo.value) == exception_str


def test_BridgeKind_set_explicit_label_map_RaisesExceptionWhen_road_delimiter_In_dst_label():
    # ESTABLISH
    x_bridgekind = bridgekind_shop(None)
    sue_dst = f"Sue{x_bridgekind.src_road_delimiter}"
    sue_src = "Sue"
    assert x_bridgekind.explicit_label_map == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_bridgekind.set_explicit_label_map(sue_src, sue_dst)
    exception_str = f"explicit_label_map cannot have dst_label '{sue_dst}'. It must be not have road_delimiter {x_bridgekind.dst_road_delimiter}."
    assert str(excinfo.value) == exception_str


def test_BridgeKind_get_explicit_dst_label_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind._get_explicit_dst_label(xio_str) != sue_str

    # WHEN
    x_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert x_bridgekind._get_explicit_dst_label(xio_str) == sue_str


def test_BridgeKind_explicit_label_map_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind.explicit_label_map_exists(xio_str, sue_str) is False
    assert x_bridgekind.explicit_label_map_exists(xio_str, zia_str) is False
    assert x_bridgekind.explicit_label_map_exists(xio_str, bob_str) is False
    assert x_bridgekind.explicit_label_map_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert x_bridgekind.explicit_label_map_exists(xio_str, sue_str)
    assert x_bridgekind.explicit_label_map_exists(xio_str, zia_str) is False
    assert x_bridgekind.explicit_label_map_exists(xio_str, bob_str) is False
    assert x_bridgekind.explicit_label_map_exists(zia_str, zia_str) is False

    # WHEN
    x_bridgekind.set_explicit_label_map(zia_str, zia_str)

    # THEN
    assert x_bridgekind.explicit_label_map_exists(xio_str, sue_str)
    assert x_bridgekind.explicit_label_map_exists(xio_str, zia_str) is False
    assert x_bridgekind.explicit_label_map_exists(xio_str, bob_str) is False
    assert x_bridgekind.explicit_label_map_exists(zia_str, zia_str)


def test_BridgeKind_explicit_src_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bridgekind = bridgekind_shop(None)
    assert x_bridgekind.explicit_src_label_exists(xio_str) is False
    assert x_bridgekind.explicit_src_label_exists(sue_str) is False
    assert x_bridgekind.explicit_src_label_exists(bob_str) is False
    assert x_bridgekind.explicit_src_label_exists(zia_str) is False

    # WHEN
    x_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert x_bridgekind.explicit_src_label_exists(xio_str)
    assert x_bridgekind.explicit_src_label_exists(sue_str) is False
    assert x_bridgekind.explicit_src_label_exists(bob_str) is False
    assert x_bridgekind.explicit_src_label_exists(zia_str) is False

    # WHEN
    x_bridgekind.set_explicit_label_map(zia_str, zia_str)

    # THEN
    assert x_bridgekind.explicit_src_label_exists(xio_str)
    assert x_bridgekind.explicit_src_label_exists(sue_str) is False
    assert x_bridgekind.explicit_src_label_exists(bob_str) is False
    assert x_bridgekind.explicit_src_label_exists(zia_str)


def test_BridgeKind_del_explicit_label_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_bridgekind = bridgekind_shop(None)
    x_bridgekind.set_explicit_label_map(xio_str, sue_str)
    assert x_bridgekind.explicit_label_map_exists(xio_str, sue_str)

    # WHEN
    x_bridgekind.del_explicit_label_map(xio_str)

    # THEN
    assert x_bridgekind.explicit_label_map_exists(xio_str, sue_str) is False


def test_BridgeKind_set_explicit_label_map_Edits_src_to_dst():
    # ESTABLISH
    src_music45_str = "music45"
    dst_music87_str = "music87"
    casa_src_str = "casa"
    casa_dst_str = "maison"
    casa_src_road = create_road(src_music45_str, casa_src_str)
    casa_dst_road = create_road(dst_music87_str, casa_dst_str)
    clean_src_str = "clean"
    clean_dst_str = "propre"
    clean_src_road = create_road(casa_src_road, clean_src_str)
    clean_dst_road = create_road(casa_dst_road, clean_dst_str)
    sweep_str = "sweep"
    sweep_src_road = create_road(clean_src_road, sweep_str)
    sweep_dst_road = create_road(clean_dst_road, sweep_str)
    x_bridgekind = bridgekind_shop(type_RoadUnit_str())
    x_bridgekind.set_src_to_dst(src_music45_str, dst_music87_str)
    x_bridgekind.set_src_to_dst(casa_src_road, casa_dst_road)
    x_bridgekind.set_src_to_dst(clean_src_road, clean_dst_road)
    x_bridgekind.set_src_to_dst(sweep_src_road, sweep_dst_road)
    assert x_bridgekind.src_to_dst_exists(src_music45_str, dst_music87_str)
    assert x_bridgekind.src_to_dst_exists(casa_src_road, casa_dst_road)
    assert x_bridgekind.src_to_dst_exists(clean_src_road, clean_dst_road)
    assert x_bridgekind.src_to_dst_exists(sweep_src_road, sweep_dst_road)

    # WHEN
    menage_dst_str = "menage"
    x_bridgekind.set_explicit_label_map(clean_src_str, menage_dst_str)

    # THEN
    menage_dst_road = create_road(casa_dst_road, menage_dst_str)
    sweep_menage_dst_road = create_road(menage_dst_road, sweep_str)
    assert x_bridgekind.src_to_dst_exists(src_music45_str, dst_music87_str)
    assert x_bridgekind.src_to_dst_exists(casa_src_road, casa_dst_road)
    assert x_bridgekind.src_to_dst_exists(clean_src_road, menage_dst_road)
    assert x_bridgekind.src_to_dst_exists(sweep_src_road, sweep_menage_dst_road)
