from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    acct_id_str,
    get_atom_args_python_types,
    credit_vote_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f09_filter.bridge import (
    BridgeKind,
    bridgekind_shop,
    default_unknown_word,
    filterable_python_types,
    filterable_atom_args,
)
from pytest import raises as pytest_raises

# from src.f09_filter.examples.filter_env import get_test_filters_dir, env_dir_setup_cleanup

# The goal of the filter function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_default_unknown_word_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_word() == "UNKNOWN"


def test_filterable_python_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_filterable_python_types = filterable_python_types()

    # THEN
    assert len(x_filterable_python_types) == 4
    assert x_filterable_python_types == {
        type_AcctID_str(),
        type_GroupID_str(),
        type_RoadNode_str(),
        type_RoadUnit_str(),
    }
    print(f"{set(get_atom_args_python_types().values())=}")
    all_atom_python_types = set(get_atom_args_python_types().values())
    inter_x = set(all_atom_python_types).intersection(x_filterable_python_types)
    assert inter_x == x_filterable_python_types


def test_filterable_atom_args_ReturnsObj():
    # ESTABLISH / WHEN
    x_filterable_atom_args = filterable_atom_args()

    # THEN
    assert len(x_filterable_atom_args) == 9
    assert x_filterable_atom_args == {
        "acct_id",
        "road",
        "parent_road",
        "label",
        "healer_id",
        "need",
        "base",
        "pick",
        "group_id",
    }

    print(f"{filterable_python_types()=}")
    static_filterable_atom_args = {
        x_arg
        for x_arg, python_type in get_atom_args_python_types().items()
        if python_type in filterable_python_types()
    }
    assert x_filterable_atom_args == static_filterable_atom_args


def test_BridgeKind_Exists():
    # ESTABLISH
    x_bridgekind = BridgeKind()

    # WHEN / THEN
    assert not x_bridgekind.python_type
    assert not x_bridgekind.atom_arg
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
        x_atom_arg=acct_id_str(),
        x_src_to_dst=src_to_dst,
        x_unknown_word=x_unknown_word,
        x_src_road_delimiter=slash_src_road_delimiter,
        x_dst_road_delimiter=colon_dst_road_delimiter,
        x_face_id=bob_str,
    )

    # THEN
    assert acct_id_bridgekind.python_type == type_AcctID_str()
    assert acct_id_bridgekind.atom_arg == acct_id_str()
    assert acct_id_bridgekind.src_to_dst == src_to_dst
    assert acct_id_bridgekind.unknown_word == x_unknown_word
    assert acct_id_bridgekind.src_road_delimiter == slash_src_road_delimiter
    assert acct_id_bridgekind.dst_road_delimiter == colon_dst_road_delimiter
    assert acct_id_bridgekind.explicit_label_map == {}
    acct_id_python_type = get_atom_args_python_types().get(acct_id_str())
    assert acct_id_bridgekind.python_type == acct_id_python_type
    assert acct_id_bridgekind.face_id == bob_str


def test_bridgekind_shop_ReturnsObj_scenario1():
    # ESTABLISH / WHEN
    credit_vote_bridgekind = bridgekind_shop(None, credit_vote_str())

    # THEN
    assert credit_vote_bridgekind.atom_arg == credit_vote_str()
    assert credit_vote_bridgekind.src_to_dst == {}
    assert credit_vote_bridgekind.unknown_word == default_unknown_word()
    assert credit_vote_bridgekind.src_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgekind.dst_road_delimiter == default_road_delimiter_if_none()
    cv_python_type = get_atom_args_python_types().get(credit_vote_str())
    assert credit_vote_bridgekind.python_type == cv_python_type
    assert credit_vote_bridgekind.face_id is None


def test_bridgekind_shop_ReturnsObj_Scenario2_atom_arg_IsNone():
    # ESTABLISH / WHEN
    credit_vote_bridgekind = bridgekind_shop(type_AcctID_str())

    # THEN
    assert credit_vote_bridgekind.python_type == type_AcctID_str()
    assert credit_vote_bridgekind.atom_arg is None
    assert credit_vote_bridgekind.src_to_dst == {}
    assert credit_vote_bridgekind.unknown_word == default_unknown_word()
    assert credit_vote_bridgekind.src_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgekind.dst_road_delimiter == default_road_delimiter_if_none()
    assert credit_vote_bridgekind.face_id is None


def test_BridgeKind_set_atom_arg_SetsAttr():
    # ESTABLISH
    acct_id_bridgekind = bridgekind_shop(None, acct_id_str())
    acct_id_python_type = type_AcctID_str()
    assert acct_id_bridgekind.atom_arg == acct_id_str()
    assert acct_id_bridgekind.python_type == acct_id_python_type

    # WHEN
    acct_id_bridgekind.set_atom_arg(credit_vote_str())

    # THEN
    assert acct_id_bridgekind.atom_arg == credit_vote_str()
    int_python_type = "int"
    assert acct_id_bridgekind.python_type == int_python_type


def test_BridgeKind_set_atom_arg_RaisesErrorIf_atom_arg_DoesNotExistIn_atom_config():
    # ESTABLISH
    acct_id_bridgekind = bridgekind_shop(None, acct_id_str())
    acct_id_python_type = type_AcctID_str()
    assert acct_id_bridgekind.atom_arg == acct_id_str()
    assert acct_id_bridgekind.python_type == acct_id_python_type

    # WHEN
    rush_acct_id_str = "rush_acct_id"
    with pytest_raises(Exception) as excinfo:
        acct_id_bridgekind.set_atom_arg(rush_acct_id_str)
    exception_str = f"set_atom_arg Error: '{rush_acct_id_str}' not arg in atom_config."
    assert str(excinfo.value) == exception_str


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
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
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
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    x_src_to_dst = {xio_str: sue_str, x_unknown_word: zia_str}
    assert acct_id_bridgekind.src_to_dst != x_src_to_dst

    # WHEN
    acct_id_bridgekind.set_all_src_to_dst(x_src_to_dst)

    # THEN
    assert acct_id_bridgekind.src_to_dst == x_src_to_dst


def test_BridgeKind_set_src_to_dst_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind.src_to_dst == {}

    # WHEN
    acct_id_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind.src_to_dst == {xio_str: sue_str}


def test_BridgeKind_get_dst_value_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind._get_dst_value(xio_str) != sue_str

    # WHEN
    acct_id_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind._get_dst_value(xio_str) == sue_str


def test_BridgeKind_src_to_dst_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, sue_str) is False
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, zia_str) is False
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, bob_str) is False
    assert acct_id_bridgekind.src_to_dst_exists(zia_str, zia_str) is False

    # WHEN
    acct_id_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, sue_str)
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, zia_str) is False
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, bob_str) is False
    assert acct_id_bridgekind.src_to_dst_exists(zia_str, zia_str) is False

    # WHEN
    acct_id_bridgekind.set_src_to_dst(zia_str, zia_str)

    # THEN
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, sue_str)
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, zia_str) is False
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, bob_str) is False
    assert acct_id_bridgekind.src_to_dst_exists(zia_str, zia_str)


def test_BridgeKind_src_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind.src_exists(xio_str) is False
    assert acct_id_bridgekind.src_exists(sue_str) is False
    assert acct_id_bridgekind.src_exists(bob_str) is False
    assert acct_id_bridgekind.src_exists(zia_str) is False

    # WHEN
    acct_id_bridgekind.set_src_to_dst(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind.src_exists(xio_str)
    assert acct_id_bridgekind.src_exists(sue_str) is False
    assert acct_id_bridgekind.src_exists(bob_str) is False
    assert acct_id_bridgekind.src_exists(zia_str) is False

    # WHEN
    acct_id_bridgekind.set_src_to_dst(zia_str, zia_str)

    # THEN
    assert acct_id_bridgekind.src_exists(xio_str)
    assert acct_id_bridgekind.src_exists(sue_str) is False
    assert acct_id_bridgekind.src_exists(bob_str) is False
    assert acct_id_bridgekind.src_exists(zia_str)


def test_BridgeKind_del_src_to_dst_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    acct_id_bridgekind.set_src_to_dst(xio_str, sue_str)
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, sue_str)

    # WHEN
    acct_id_bridgekind.del_src_to_dst(xio_str)

    # THEN
    assert acct_id_bridgekind.src_to_dst_exists(xio_str, sue_str) is False


def test_BridgeKind_unknown_word_in_src_to_dst_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    acct_id_bridgekind.set_src_to_dst(xio_str, sue_str)
    assert acct_id_bridgekind._unknown_word_in_src_to_dst() is False

    # WHEN
    acct_id_bridgekind.set_src_to_dst(zia_str, x_unknown_word)

    # THEN
    assert acct_id_bridgekind._unknown_word_in_src_to_dst()


def test_BridgeKind_set_explicit_label_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind.explicit_label_map == {}

    # WHEN
    acct_id_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind.explicit_label_map == {xio_str: sue_str}


def test_BridgeKind_get_explicit_dst_label_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind._get_explicit_dst_label(xio_str) != sue_str

    # WHEN
    acct_id_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind._get_explicit_dst_label(xio_str) == sue_str


def test_BridgeKind_explicit_label_map_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, sue_str) is False
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, zia_str) is False
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, bob_str) is False
    assert acct_id_bridgekind.explicit_label_map_exists(zia_str, zia_str) is False

    # WHEN
    acct_id_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, sue_str)
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, zia_str) is False
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, bob_str) is False
    assert acct_id_bridgekind.explicit_label_map_exists(zia_str, zia_str) is False

    # WHEN
    acct_id_bridgekind.set_explicit_label_map(zia_str, zia_str)

    # THEN
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, sue_str)
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, zia_str) is False
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, bob_str) is False
    assert acct_id_bridgekind.explicit_label_map_exists(zia_str, zia_str)


def test_BridgeKind_explicit_src_label_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    assert acct_id_bridgekind.explicit_src_label_exists(xio_str) is False
    assert acct_id_bridgekind.explicit_src_label_exists(sue_str) is False
    assert acct_id_bridgekind.explicit_src_label_exists(bob_str) is False
    assert acct_id_bridgekind.explicit_src_label_exists(zia_str) is False

    # WHEN
    acct_id_bridgekind.set_explicit_label_map(xio_str, sue_str)

    # THEN
    assert acct_id_bridgekind.explicit_src_label_exists(xio_str)
    assert acct_id_bridgekind.explicit_src_label_exists(sue_str) is False
    assert acct_id_bridgekind.explicit_src_label_exists(bob_str) is False
    assert acct_id_bridgekind.explicit_src_label_exists(zia_str) is False

    # WHEN
    acct_id_bridgekind.set_explicit_label_map(zia_str, zia_str)

    # THEN
    assert acct_id_bridgekind.explicit_src_label_exists(xio_str)
    assert acct_id_bridgekind.explicit_src_label_exists(sue_str) is False
    assert acct_id_bridgekind.explicit_src_label_exists(bob_str) is False
    assert acct_id_bridgekind.explicit_src_label_exists(zia_str)


def test_BridgeKind_del_explicit_label_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    acct_id_bridgekind = bridgekind_shop(
        None, acct_id_str(), x_unknown_word=x_unknown_word
    )
    acct_id_bridgekind.set_explicit_label_map(xio_str, sue_str)
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, sue_str)

    # WHEN
    acct_id_bridgekind.del_explicit_label_map(xio_str)

    # THEN
    assert acct_id_bridgekind.explicit_label_map_exists(xio_str, sue_str) is False
