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
    default_unknown_word,
)
from pandas import DataFrame


def get_clean_roadnode_bridgekind() -> BridgeKind:
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_road_delimiter = "/"
    roadnode_bridgekind = bridgekind_shop(
        type_RoadNode_str(), slash_otx_road_delimiter, x_face_id="Sue"
    )
    roadnode_bridgekind.set_otx_to_inx(clean_otx, clean_inx)
    roadnode_bridgekind.set_otx_to_inx(casa_otx, casa_inx)
    return roadnode_bridgekind


def get_clean_roadunit_bridgekind() -> BridgeKind:
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    road_delimiter = default_road_delimiter_if_none()
    clean_otx_road = f"{otx_music45_str}{road_delimiter}{clean_otx_str}"
    road_bridgekind = bridgekind_shop(type_RoadUnit_str(), x_face_id="Sue")
    road_bridgekind.set_explicit_label_map(clean_otx_str, clean_inx_str)
    road_bridgekind.set_otx_to_inx(otx_music45_str, inx_music87_str)
    road_bridgekind.get_create_inx(clean_otx_road)
    return road_bridgekind


def get_swim_groupid_bridgekind() -> BridgeKind:
    road_delimiter = default_road_delimiter_if_none()
    swim_otx = f"swim{road_delimiter}"
    swim_inx = f"nage{road_delimiter}"
    climb_otx = f"climb{road_delimiter}"
    group_id_bridgekind = bridgekind_shop(type_GroupID_str(), x_face_id="Sue")
    group_id_bridgekind.set_otx_to_inx(swim_otx, swim_inx)
    group_id_bridgekind.set_otx_to_inx(climb_otx, climb_otx)
    return group_id_bridgekind


def get_suita_acctid_bridgekind() -> BridgeKind:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str(), x_face_id="Sue")
    acct_id_bridgekind.set_otx_to_inx(xio_otx, xio_inx)
    acct_id_bridgekind.set_otx_to_inx(sue_otx, sue_inx)
    acct_id_bridgekind.set_otx_to_inx(bob_otx, bob_inx)
    return acct_id_bridgekind


def get_invalid_acctid_bridgekind() -> BridgeKind:
    sue_otx = f"Xio{default_road_delimiter_if_none()}"
    sue_inx = "Sue"
    zia_otx = "Zia"
    zia_inx = "Zia"
    group_id_bridgekind = bridgekind_shop(type_AcctID_str(), x_face_id="Sue")
    group_id_bridgekind.set_otx_to_inx(sue_otx, sue_inx)
    group_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    return group_id_bridgekind


def get_invalid_groupid_bridgekind() -> BridgeKind:
    sue_otx = f"Xio{default_road_delimiter_if_none()}"
    sue_inx = f"Sue{default_road_delimiter_if_none()}"
    zia_otx = "Zia"
    zia_inx = f"Zia{default_road_delimiter_if_none()}"
    group_id_bridgekind = bridgekind_shop(type_GroupID_str(), x_face_id="Sue")
    group_id_bridgekind.set_otx_to_inx(sue_otx, sue_inx)
    group_id_bridgekind.set_otx_to_inx(zia_otx, zia_inx)
    return group_id_bridgekind


def get_invalid_road_bridgekind() -> BridgeKind:
    clean_str = "clean"
    clean_inx = "propre"
    casa_otx = f"casa{default_road_delimiter_if_none()}"
    casa_inx = "casa"
    roadnode_bridgekind = bridgekind_shop(type_RoadNode_str(), x_face_id="Sue")
    roadnode_bridgekind.set_otx_to_inx(clean_str, clean_inx)
    roadnode_bridgekind.set_otx_to_inx(casa_otx, casa_inx)
    return roadnode_bridgekind


def get_slash_roadunit_bridgekind() -> BridgeKind:
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    clean_otx_road = f"{otx_music45_str}{slash_otx_road_delimiter}{clean_otx_str}"
    clean_otx_road = f"{otx_music45_str}{colon_inx_road_delimiter}{clean_otx_str}"
    road_bridgekind = bridgekind_shop(
        type_RoadUnit_str(),
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    road_bridgekind.set_explicit_label_map(clean_otx_str, clean_inx_str)
    road_bridgekind.set_otx_to_inx(otx_music45_str, inx_music87_str)
    road_bridgekind.get_create_inx(clean_otx_road)
    return road_bridgekind


def get_slash_groupid_bridgekind() -> BridgeKind:
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    swim_otx = f"swim{slash_otx_road_delimiter}"
    swim_inx = f"nage{colon_inx_road_delimiter}"
    climb_otx = f"climb{slash_otx_road_delimiter}"
    climb_inx = f"climb{colon_inx_road_delimiter}"
    group_id_bridgekind = bridgekind_shop(
        type_GroupID_str(),
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    group_id_bridgekind.set_otx_to_inx(swim_otx, swim_inx)
    group_id_bridgekind.set_otx_to_inx(climb_otx, climb_inx)
    return group_id_bridgekind


def get_slash_acctid_bridgekind() -> BridgeKind:
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_bridgekind = bridgekind_shop(
        type_AcctID_str(),
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    acct_id_bridgekind.set_otx_to_inx(xio_otx, xio_inx)
    acct_id_bridgekind.set_otx_to_inx(sue_otx, sue_inx)
    acct_id_bridgekind.set_otx_to_inx(bob_otx, bob_inx)
    return acct_id_bridgekind


def get_sue_bridgeunit() -> BridgeUnit:
    sue_bridgeunit = bridgeunit_shop("Sue")
    sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_clean_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_swim_groupid_bridgekind())
    return sue_bridgeunit


def get_suita_acctid_otx_dt() -> DataFrame:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[acct_id_str()])
    otx_dt.loc[0, acct_id_str()] = zia_otx
    otx_dt.loc[1, acct_id_str()] = sue_otx
    otx_dt.loc[2, acct_id_str()] = bob_otx
    otx_dt.loc[3, acct_id_str()] = xio_otx
    return otx_dt


def get_suita_acctid_inx_dt() -> DataFrame:
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    zia_otx = "Zia"
    inx_dt = DataFrame(columns=[acct_id_str()])
    inx_dt.loc[0, acct_id_str()] = xio_inx
    inx_dt.loc[1, acct_id_str()] = sue_inx
    inx_dt.loc[2, acct_id_str()] = bob_inx
    inx_dt.loc[3, acct_id_str()] = zia_otx
    return inx_dt


def get_casa_maison_bridgeunit_set_by_otx_to_inx() -> BridgeUnit:
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

    sue_bridgeunit = bridgeunit_shop("Sue")
    rx = type_RoadNode_str()
    sue_bridgeunit.set_otx_to_inx(rx, otx_music45_str, inx_music87_str)
    sue_bridgeunit.set_otx_to_inx(rx, casa_otx_road, casa_inx_road)
    sue_bridgeunit.set_otx_to_inx(rx, clean_otx_road, clean_inx_road)
    sue_bridgeunit.set_otx_to_inx(rx, sweep_otx_road, sweep_inx_road)
    return sue_bridgeunit


def get_casa_maison_bridgeunit_set_by_explicit_label_map() -> BridgeUnit:
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

    sue_bridgeunit = bridgeunit_shop("Sue")
    rx = type_RoadNode_str()
    sue_bridgeunit.set_explicit_label_map(rx, otx_music45_str, inx_music87_str)
    sue_bridgeunit.set_explicit_label_map(rx, casa_otx_str, casa_inx_str)
    sue_bridgeunit.set_explicit_label_map(rx, clean_otx_str, clean_inx_str)
    return sue_bridgeunit


def get_casa_maison_road_otx_dt() -> DataFrame:
    otx_music45_str = "music45"
    casa_otx_str = "casa"
    casa_otx_road = create_road(otx_music45_str, casa_otx_str)
    clean_otx_str = "clean"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    otx_dt = DataFrame(columns=[base_str()])
    otx_dt.loc[0, base_str()] = otx_music45_str
    otx_dt.loc[1, base_str()] = casa_otx_road
    otx_dt.loc[2, base_str()] = clean_otx_road
    otx_dt.loc[3, base_str()] = sweep_otx_road
    return otx_dt


def get_casa_maison_road_inx_dt() -> DataFrame:
    inx_music87_str = "music87"
    casa_inx_road = create_road(inx_music87_str, "maison")
    clean_inx_road = create_road(casa_inx_road, "propre")
    sweep_inx_road = create_road(clean_inx_road, "sweep")
    inx_dt = DataFrame(columns=[base_str()])
    inx_dt.loc[0, base_str()] = inx_music87_str
    inx_dt.loc[1, base_str()] = casa_inx_road
    inx_dt.loc[2, base_str()] = clean_inx_road
    inx_dt.loc[3, base_str()] = sweep_inx_road
    return inx_dt


def get_casa_maison_road_otx_to_inx_dt() -> DataFrame:
    inx_music87_str = "music87"
    casa_inx_road = create_road(inx_music87_str, "maison")
    clean_inx_road = create_road(casa_inx_road, "propre")
    sweep_inx_road = create_road(clean_inx_road, "sweep")
    otx_music45_str = "music45"
    casa_otx_road = create_road(otx_music45_str, "casa")
    clean_otx_road = create_road(casa_otx_road, "clean")
    sweep_otx_road = create_road(clean_otx_road, "sweep")
    x_rd = default_road_delimiter_if_none()
    uw = default_unknown_word()

    inx_dt = DataFrame(
        columns=[
            "face_id",
            "python_type",
            "otx_road_delimiter",
            "inx_road_delimiter",
            "unknown_word",
            "otx_word",
            "inx_word",
        ]
    )
    rt = type_RoadUnit_str()
    inx_dt.loc[0] = [None, rt, x_rd, x_rd, uw, otx_music45_str, inx_music87_str]
    inx_dt.loc[1] = [None, rt, x_rd, x_rd, uw, casa_otx_road, casa_inx_road]
    inx_dt.loc[2] = [None, rt, x_rd, x_rd, uw, clean_otx_road, clean_inx_road]
    inx_dt.loc[3] = [None, rt, x_rd, x_rd, uw, sweep_otx_road, sweep_inx_road]
    return inx_dt
