from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    type_RoadUnit_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
)
from src.f09_filter.bridge import bridgekind_shop, BridgeKind


def get_clean_roadnode_bridgekind() -> BridgeKind:
    clean_src = "clean"
    clean_dst = "prop"
    casa_src = "casa1"
    casa_dst = "casa2"
    slash_src_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(
        type_RoadNode_str(), slash_src_road_delimiter, x_face_id="Sue"
    )
    roadnode_bridgekind.set_src_to_dst(clean_src, clean_dst)
    roadnode_bridgekind.set_src_to_dst(casa_src, casa_dst)
    return roadnode_bridgekind


def get_clean_roadunit_bridgekind() -> BridgeKind:
    src_music45_str = "music45"
    dst_music87_str = "music87"
    clean_src_str = "clean"
    clean_dst_str = "prop"
    road_delimiter = default_road_delimiter_if_none()
    clean_src_road = f"{src_music45_str}{road_delimiter}{clean_src_str}"
    road_bridgekind = bridgekind_shop(type_RoadUnit_str(), x_face_id="Sue")
    road_bridgekind.set_explicit_label_map(clean_src_str, clean_dst_str)
    road_bridgekind.set_src_to_dst(src_music45_str, dst_music87_str)
    road_bridgekind.get_create_dst(clean_src_road)
    return road_bridgekind


def get_swim_groupid_bridgekind() -> BridgeKind:
    road_delimiter = default_road_delimiter_if_none()
    swim_src = f"swim{road_delimiter}"
    swim_dst = f"nage{road_delimiter}"
    climb_src = f"climb{road_delimiter}"
    group_id_bridgekind = bridgekind_shop(type_GroupID_str(), x_face_id="Sue")
    group_id_bridgekind.set_src_to_dst(swim_src, swim_dst)
    group_id_bridgekind.set_src_to_dst(climb_src, climb_src)
    return group_id_bridgekind


def get_suita_acctid_bridgekind() -> BridgeKind:
    xio_src = "Xio"
    sue_src = "Sue"
    bob_src = "Bob"
    zia_src = "Zia"
    xio_dst = "Xioita"
    sue_dst = "Suita"
    bob_dst = "Bobita"
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str(), x_face_id="Sue")
    acct_id_bridgekind.set_src_to_dst(xio_src, xio_dst)
    acct_id_bridgekind.set_src_to_dst(sue_src, sue_dst)
    acct_id_bridgekind.set_src_to_dst(bob_src, bob_dst)
    return acct_id_bridgekind


def get_invalid_acctid_bridgekind() -> BridgeKind:
    sue_src = f"Xio{default_road_delimiter_if_none()}"
    sue_dst = "Sue"
    zia_src = "Zia"
    zia_dst = "Zia"
    group_id_bridgekind = bridgekind_shop(type_AcctID_str(), x_face_id="Sue")
    group_id_bridgekind.set_src_to_dst(sue_src, sue_dst)
    group_id_bridgekind.set_src_to_dst(zia_src, zia_dst)
    return group_id_bridgekind


def get_invalid_groupid_bridgekind() -> BridgeKind:
    sue_src = f"Xio{default_road_delimiter_if_none()}"
    sue_dst = f"Sue{default_road_delimiter_if_none()}"
    zia_src = "Zia"
    zia_dst = f"Zia{default_road_delimiter_if_none()}"
    group_id_bridgekind = bridgekind_shop(type_GroupID_str(), x_face_id="Sue")
    group_id_bridgekind.set_src_to_dst(sue_src, sue_dst)
    group_id_bridgekind.set_src_to_dst(zia_src, zia_dst)
    return group_id_bridgekind


def get_invalid_road_bridgekind() -> BridgeKind:
    clean_str = "clean"
    clean_dst = "prop"
    casa_src = f"casa{default_road_delimiter_if_none()}"
    casa_dst = "casa"
    roadnode_bridgekind = bridgekind_shop(type_RoadNode_str(), x_face_id="Sue")
    roadnode_bridgekind.set_src_to_dst(clean_str, clean_dst)
    roadnode_bridgekind.set_src_to_dst(casa_src, casa_dst)
    return roadnode_bridgekind


def get_slash_roadunit_bridgekind() -> BridgeKind:
    src_music45_str = "music45"
    dst_music87_str = "music87"
    clean_src_str = "clean"
    clean_dst_str = "prop"
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"
    clean_src_road = f"{src_music45_str}{slash_src_road_delimiter}{clean_src_str}"
    clean_src_road = f"{src_music45_str}{colon_dst_road_delimiter}{clean_src_str}"
    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(),
        x_src_road_delimiter=slash_src_road_delimiter,
        x_dst_road_delimiter=colon_dst_road_delimiter,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    road_bridgekind.set_explicit_label_map(clean_src_str, clean_dst_str)
    road_bridgekind.set_src_to_dst(src_music45_str, dst_music87_str)
    road_bridgekind.get_create_dst(clean_src_road)
    return road_bridgekind


def get_slash_groupid_bridgekind() -> BridgeKind:
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"
    swim_src = f"swim{slash_src_road_delimiter}"
    swim_dst = f"nage{colon_dst_road_delimiter}"
    climb_src = f"climb{slash_src_road_delimiter}"
    climb_dst = f"climb{colon_dst_road_delimiter}"
    group_id_bridgekind = bridgekind_shop(
        type_GroupID_str(),
        x_src_road_delimiter=slash_src_road_delimiter,
        x_dst_road_delimiter=colon_dst_road_delimiter,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    group_id_bridgekind.set_src_to_dst(swim_src, swim_dst)
    group_id_bridgekind.set_src_to_dst(climb_src, climb_dst)
    return group_id_bridgekind


def get_slash_acctid_bridgekind() -> BridgeKind:
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"
    xio_src = "Xio"
    sue_src = "Sue"
    bob_src = "Bob"
    zia_src = "Zia"
    xio_dst = "Xioita"
    sue_dst = "Suita"
    bob_dst = "Bobita"
    acct_id_bridgekind = bridgekind_shop(
        type_AcctID_str(),
        x_src_road_delimiter=slash_src_road_delimiter,
        x_dst_road_delimiter=colon_dst_road_delimiter,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    acct_id_bridgekind.set_src_to_dst(xio_src, xio_dst)
    acct_id_bridgekind.set_src_to_dst(sue_src, sue_dst)
    acct_id_bridgekind.set_src_to_dst(bob_src, bob_dst)
    return acct_id_bridgekind
