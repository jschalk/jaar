from src.f01_road.road import default_road_delimiter_if_none, create_road
from src.f04_gift.atom_config import (
    acct_id_str,
    base_str,
    type_RoadUnit_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
)
from src.f09_filter.bridge import (
    bridgekind_shop,
    BridgeKind,
    BridgeUnit,
    bridgeunit_shop,
)
from pandas import DataFrame


def get_clean_roadnode_bridgekind() -> BridgeKind:
    clean_src = "clean"
    clean_dst = "propre"
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
    clean_dst = "propre"
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


def get_sue_bridgeunit() -> BridgeUnit:
    sue_bridgeunit = bridgeunit_shop("Sue")
    sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_clean_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_swim_groupid_bridgekind())
    return sue_bridgeunit


def get_suita_acctid_src_dt() -> DataFrame:
    xio_src = "Xio"
    sue_src = "Sue"
    bob_src = "Bob"
    zia_src = "Zia"
    src_dt = DataFrame(columns=[acct_id_str()])
    src_dt.loc[0, acct_id_str()] = zia_src
    src_dt.loc[1, acct_id_str()] = sue_src
    src_dt.loc[2, acct_id_str()] = bob_src
    src_dt.loc[3, acct_id_str()] = xio_src
    return src_dt


def get_suita_acctid_dst_dt() -> DataFrame:
    xio_dst = "Xioita"
    sue_dst = "Suita"
    bob_dst = "Bobita"
    zia_src = "Zia"
    dst_dt = DataFrame(columns=[acct_id_str()])
    dst_dt.loc[0, acct_id_str()] = xio_dst
    dst_dt.loc[1, acct_id_str()] = sue_dst
    dst_dt.loc[2, acct_id_str()] = bob_dst
    dst_dt.loc[3, acct_id_str()] = zia_src
    return dst_dt


def get_casa_maison_bridgeunit_set_by_src_to_dst() -> BridgeUnit:
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

    sue_bridgeunit = bridgeunit_shop("Sue")
    rx = type_RoadNode_str()
    sue_bridgeunit.set_src_to_dst(rx, src_music45_str, dst_music87_str)
    sue_bridgeunit.set_src_to_dst(rx, casa_src_road, casa_dst_road)
    sue_bridgeunit.set_src_to_dst(rx, clean_src_road, clean_dst_road)
    sue_bridgeunit.set_src_to_dst(rx, sweep_src_road, sweep_dst_road)
    return sue_bridgeunit


def get_casa_maison_bridgeunit_set_by_explicit_label_map() -> BridgeUnit:
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

    sue_bridgeunit = bridgeunit_shop("Sue")
    rx = type_RoadNode_str()
    sue_bridgeunit.set_explicit_label_map(rx, src_music45_str, dst_music87_str)
    sue_bridgeunit.set_explicit_label_map(rx, casa_src_road, casa_dst_road)
    sue_bridgeunit.set_explicit_label_map(rx, clean_src_road, clean_dst_road)
    sue_bridgeunit.set_explicit_label_map(rx, sweep_src_road, sweep_dst_road)
    return sue_bridgeunit


def get_casa_maison_road_src_dt() -> DataFrame:
    src_music45_str = "music45"
    casa_src_str = "casa"
    casa_src_road = create_road(src_music45_str, casa_src_str)
    clean_src_str = "clean"
    clean_src_road = create_road(casa_src_road, clean_src_str)
    sweep_str = "sweep"
    sweep_src_road = create_road(clean_src_road, sweep_str)
    src_dt = DataFrame(columns=[base_str()])
    src_dt.loc[0, base_str()] = src_music45_str
    src_dt.loc[1, base_str()] = casa_src_road
    src_dt.loc[2, base_str()] = clean_src_road
    src_dt.loc[3, base_str()] = sweep_src_road
    return src_dt


def get_casa_maison_road_dst_dt() -> DataFrame:
    dst_music87_str = "music87"
    casa_dst_road = create_road(dst_music87_str, "maison")
    clean_dst_road = create_road(casa_dst_road, "propre")
    sweep_dst_road = create_road(clean_dst_road, "sweep")
    dst_dt = DataFrame(columns=[base_str()])
    dst_dt.loc[0, base_str()] = dst_music87_str
    dst_dt.loc[1, base_str()] = casa_dst_road
    dst_dt.loc[2, base_str()] = clean_dst_road
    dst_dt.loc[3, base_str()] = sweep_dst_road
    return dst_dt
