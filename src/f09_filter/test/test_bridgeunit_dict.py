from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    get_atom_args_python_types,
    road_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f09_filter.bridge import (
    BridgeUnit,
    bridgeunit_shop,
    bridgekind_shop,
    default_unknown_word,
    filterable_python_types,
    filterable_atom_args,
)
from src.f09_filter.examples.examples_filter import (
    get_invalid_acctid_bridgekind,
    get_invalid_groupid_bridgekind,
    get_invalid_road_bridgekind,
    get_clean_roadunit_bridgekind,
    get_swim_groupid_bridgekind,
    get_suita_acctid_bridgekind,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_BridgeUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)

    # WHEN
    sue_dict = sue_bridgeunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("src_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("dst_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("unknown_word") == default_unknown_word()
    assert sue_dict.get("brandkinds")
    x_brandkinds = sue_dict.get("brandkinds")
    assert len(x_brandkinds) == 3
    assert set(x_brandkinds.keys()) == {
        type_AcctID_str(),
        type_GroupID_str(),
        road_str(),
    }
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert x_brandkinds.get(type_AcctID_str()) == acct_id_bridgekind.get_dict()
    assert x_brandkinds.get(type_GroupID_str()) == group_id_bridgekind.get_dict()
    assert x_brandkinds.get(road_str()) == road_bridgekind.get_dict()


def test_BridgeUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    sue_bridgeunit.set_bridgekind(get_clean_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_swim_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())

    # WHEN
    sue_dict = sue_bridgeunit.get_dict()

    # THEN
    assert sue_dict.get("brandkinds")
    x_brandkinds = sue_dict.get("brandkinds")
    assert len(x_brandkinds) == 3
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert acct_id_bridgekind.get_dict() == get_suita_acctid_bridgekind().get_dict()
    assert group_id_bridgekind.get_dict() == get_swim_groupid_bridgekind().get_dict()
    assert road_bridgekind.get_dict() == get_clean_roadunit_bridgekind().get_dict()

    # # ESTABLISH
    # invalid_acctid_bridgekind = get_invalid_acctid_bridgekind()
    # invalid_groupid_bridgekind = get_invalid_groupid_bridgekind()
    # invalid_road_bridgekind = get_invalid_road_bridgekind()
    # valid_acctid_bridgekind = get_suita_acctid_bridgekind()
    # valid_groupid_bridgekind = get_swim_groupid_bridgekind()
    # valid_road_bridgekind = get_clean_roadunit_bridgekind()
    # assert valid_acctid_bridgekind.is_valid()
    # assert valid_groupid_bridgekind.is_valid()
    # assert valid_road_bridgekind.is_valid()
    # assert invalid_road_bridgekind.is_valid() is False
    # assert invalid_groupid_bridgekind.is_valid() is False
    # assert invalid_acctid_bridgekind.is_valid() is False

    # # WHEN / THEN
    # sue_bridgeunit = bridgeunit_shop("Sue")
    # assert sue_bridgeunit.is_valid()
    # sue_bridgeunit.set_bridgekind(valid_acctid_bridgekind)
    # sue_bridgeunit.set_bridgekind(valid_groupid_bridgekind)
    # sue_bridgeunit.set_bridgekind(valid_road_bridgekind)
    # assert sue_bridgeunit.is_valid()


# def test_BridgeUnit_set_explicit_label_map_SetsAttr():
#     # ESTABLISH
#     xio_str = "Xio"
#     sue_str = "Sue"
#     x_unknown_word = "UnknownAcctId"
#     sue_bridgeunit = bridgeunit_shop(
#         None, acct_id_str(), x_unknown_word=x_unknown_word
#     )
#     assert sue_bridgeunit.explicit_label_map == {}

#     # WHEN
#     sue_bridgeunit.set_explicit_label_map(xio_str, sue_str)

#     # THEN
#     assert sue_bridgeunit.explicit_label_map == {xio_str: sue_str}


# def test_BridgeUnit_get_explicit_dst_label_ReturnsObj():
#     # ESTABLISH
#     xio_str = "Xio"
#     sue_str = "Sue"
#     x_unknown_word = "UnknownAcctId"
#     sue_bridgeunit = bridgeunit_shop(
#         None, acct_id_str(), x_unknown_word=x_unknown_word
#     )
#     assert sue_bridgeunit._get_explicit_dst_label(xio_str) != sue_str

#     # WHEN
#     sue_bridgeunit.set_explicit_label_map(xio_str, sue_str)

#     # THEN
#     assert sue_bridgeunit._get_explicit_dst_label(xio_str) == sue_str


# def test_BridgeUnit_explicit_label_map_exists_ReturnsObj():
#     # ESTABLISH
#     xio_str = "Xio"
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     x_unknown_word = "UnknownAcctId"
#     sue_bridgeunit = bridgeunit_shop(
#         None, acct_id_str(), x_unknown_word=x_unknown_word
#     )
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, sue_str) is False
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, zia_str) is False
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, bob_str) is False
#     assert sue_bridgeunit.explicit_label_map_exists(zia_str, zia_str) is False

#     # WHEN
#     sue_bridgeunit.set_explicit_label_map(xio_str, sue_str)

#     # THEN
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, sue_str)
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, zia_str) is False
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, bob_str) is False
#     assert sue_bridgeunit.explicit_label_map_exists(zia_str, zia_str) is False

#     # WHEN
#     sue_bridgeunit.set_explicit_label_map(zia_str, zia_str)

#     # THEN
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, sue_str)
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, zia_str) is False
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, bob_str) is False
#     assert sue_bridgeunit.explicit_label_map_exists(zia_str, zia_str)


# def test_BridgeUnit_explicit_src_label_exists_ReturnsObj():
#     # ESTABLISH
#     xio_str = "Xio"
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     x_unknown_word = "UnknownAcctId"
#     sue_bridgeunit = bridgeunit_shop(
#         None, acct_id_str(), x_unknown_word=x_unknown_word
#     )
#     assert sue_bridgeunit.explicit_src_label_exists(xio_str) is False
#     assert sue_bridgeunit.explicit_src_label_exists(sue_str) is False
#     assert sue_bridgeunit.explicit_src_label_exists(bob_str) is False
#     assert sue_bridgeunit.explicit_src_label_exists(zia_str) is False

#     # WHEN
#     sue_bridgeunit.set_explicit_label_map(xio_str, sue_str)

#     # THEN
#     assert sue_bridgeunit.explicit_src_label_exists(xio_str)
#     assert sue_bridgeunit.explicit_src_label_exists(sue_str) is False
#     assert sue_bridgeunit.explicit_src_label_exists(bob_str) is False
#     assert sue_bridgeunit.explicit_src_label_exists(zia_str) is False

#     # WHEN
#     sue_bridgeunit.set_explicit_label_map(zia_str, zia_str)

#     # THEN
#     assert sue_bridgeunit.explicit_src_label_exists(xio_str)
#     assert sue_bridgeunit.explicit_src_label_exists(sue_str) is False
#     assert sue_bridgeunit.explicit_src_label_exists(bob_str) is False
#     assert sue_bridgeunit.explicit_src_label_exists(zia_str)


# def test_BridgeUnit_del_explicit_label_map_SetsAttr():
#     # ESTABLISH
#     xio_str = "Xio"
#     sue_str = "Sue"
#     x_unknown_word = "UnknownAcctId"
#     sue_bridgeunit = bridgeunit_shop(
#         None, acct_id_str(), x_unknown_word=x_unknown_word
#     )
#     sue_bridgeunit.set_explicit_label_map(xio_str, sue_str)
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, sue_str)

#     # WHEN
#     sue_bridgeunit.del_explicit_label_map(xio_str)

#     # THEN
#     assert sue_bridgeunit.explicit_label_map_exists(xio_str, sue_str) is False
