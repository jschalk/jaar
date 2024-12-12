from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_wall_if_None, create_road
from src.f04_gift.atom_config import acct_id_str, base_str, type_RoadUnit_str
from src.f08_pidgin.bridge import (
    groupbridge_shop,
    acctbridge_shop,
    ideabridge_shop,
    roadbridge_shop,
    GroupBridge,
    AcctBridge,
    IdeaBridge,
    RoadBridge,
)
from src.f08_pidgin.pidgin import PidginUnit, pidginunit_shop
from pandas import DataFrame


def get_clean_ideabridge() -> IdeaBridge:
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    ideabridge = ideabridge_shop(x_face_id="Sue")
    ideabridge.set_otx2inx(clean_otx, clean_inx)
    ideabridge.set_otx2inx(casa_otx, casa_inx)
    return ideabridge


def get_clean_roadbridge() -> RoadBridge:
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    wall = default_wall_if_None()
    clean_otx_road = f"{otx_music45_str}{wall}{clean_otx_str}"
    road_bridgeunit = roadbridge_shop(x_face_id="Sue")
    road_bridgeunit.set_idea(clean_otx_str, clean_inx_str)
    road_bridgeunit.set_otx2inx(otx_music45_str, inx_music87_str)
    road_bridgeunit.reveal_inx(clean_otx_road)
    return road_bridgeunit


def get_swim_groupbridge() -> GroupBridge:
    wall = default_wall_if_None()
    swim_otx = f"swim{wall}"
    swim_inx = f"nage{wall}"
    climb_otx = f"climb{wall}"
    x_groupbridge = groupbridge_shop(x_face_id="Sue")
    x_groupbridge.set_otx2inx(swim_otx, swim_inx)
    x_groupbridge.set_otx2inx(climb_otx, climb_otx)
    return x_groupbridge


def get_suita_acctbridge() -> AcctBridge:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_bridgeunit = acctbridge_shop(x_face_id="Sue")
    acct_id_bridgeunit.set_otx2inx(xio_otx, xio_inx)
    acct_id_bridgeunit.set_otx2inx(sue_otx, sue_inx)
    acct_id_bridgeunit.set_otx2inx(bob_otx, bob_inx)
    return acct_id_bridgeunit


# def get_invalid_acct_id_bridgeunit() -> BridgeUnit:
#     sue_otx = f"Xio{default_wall_if_None()}"
#     sue_inx = "Sue"
#     zia_otx = "Zia"
#     zia_inx = "Zia"
#     x_groupbridge = bridgeunit_shop(type_AcctID_str(), x_face_id="Sue")
#     x_groupbridge.set_otx2inx(sue_otx, sue_inx)
#     x_groupbridge.set_otx2inx(zia_otx, zia_inx)
#     return x_groupbridge


# def get_invalid_group_id_bridgeunit() -> BridgeUnit:
#     sue_otx = f"Xio{default_wall_if_None()}"
#     sue_inx = f"Sue{default_wall_if_None()}"
#     zia_otx = "Zia"
#     zia_inx = f"Zia{default_wall_if_None()}"
#     x_groupbridge = bridgeunit_shop(type_GroupID_str(), x_face_id="Sue")
#     x_groupbridge.set_otx2inx(sue_otx, sue_inx)
#     x_groupbridge.set_otx2inx(zia_otx, zia_inx)
#     return x_groupbridge


# def get_invalid_road_bridgeunit() -> BridgeUnit:
#     clean_str = "clean"
#     clean_inx = "propre"
#     casa_otx = f"casa{default_wall_if_None()}"
#     casa_inx = "casa"
#     ideabridge = bridgeunit_shop(type_IdeaUnit_str(), x_face_id="Sue")
#     ideabridge.set_otx2inx(clean_str, clean_inx)
#     ideabridge.set_otx2inx(casa_otx, casa_inx)
#     return ideabridge


def get_slash_roadbridge() -> RoadBridge:
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    clean_otx_road = f"{otx_music45_str}{slash_otx_wall}{clean_otx_str}"
    clean_otx_road = f"{otx_music45_str}{colon_inx_wall}{clean_otx_str}"
    road_bridgeunit = roadbridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    road_bridgeunit.set_idea(clean_otx_str, clean_inx_str)
    road_bridgeunit.set_otx2inx(otx_music45_str, inx_music87_str)
    road_bridgeunit.reveal_inx(clean_otx_road)
    return road_bridgeunit


def get_slash_groupbridge() -> GroupBridge:
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    swim_otx = f"swim{slash_otx_wall}"
    swim_inx = f"nage{colon_inx_wall}"
    climb_otx = f"climb{slash_otx_wall}"
    climb_inx = f"climb{colon_inx_wall}"
    x_groupbridge = groupbridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    x_groupbridge.set_otx2inx(swim_otx, swim_inx)
    x_groupbridge.set_otx2inx(climb_otx, climb_inx)
    return x_groupbridge


def get_slash_acctbridge() -> AcctBridge:
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_bridgeunit = acctbridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
    )
    acct_id_bridgeunit.set_otx2inx(xio_otx, xio_inx)
    acct_id_bridgeunit.set_otx2inx(sue_otx, sue_inx)
    acct_id_bridgeunit.set_otx2inx(bob_otx, bob_inx)
    return acct_id_bridgeunit


def get_sue_pidginunit() -> PidginUnit:
    sue_pidginunit = pidginunit_shop("Sue")
    sue_pidginunit.set_acctbridge(get_suita_acctbridge())
    sue_pidginunit.set_groupbridge(get_swim_groupbridge())
    sue_pidginunit.set_ideabridge(get_clean_ideabridge())
    sue_pidginunit.set_roadbridge(get_clean_roadbridge())
    sue_pidginunit.roadbridge.ideabridge = get_clean_ideabridge()
    return sue_pidginunit


def get_suita_acct_id_otx_dt() -> DataFrame:
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


def get_suita_acct_id_inx_dt() -> DataFrame:
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


def get_casa_maison_pidginunit_set_by_otx2inx() -> PidginUnit:
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

    sue_pidginunit = pidginunit_shop("Sue", 7)
    rx = type_RoadUnit_str()
    sue_pidginunit.set_otx2inx(rx, otx_music45_str, inx_music87_str)
    sue_pidginunit.set_otx2inx(rx, casa_otx_road, casa_inx_road)
    sue_pidginunit.set_otx2inx(rx, clean_otx_road, clean_inx_road)
    sue_pidginunit.set_otx2inx(rx, sweep_otx_road, sweep_inx_road)
    return sue_pidginunit


def get_casa_maison_pidginunit_set_by_idea() -> PidginUnit:
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

    sue_pidginunit = pidginunit_shop("Sue", 7)
    sue_pidginunit.set_idea(otx_music45_str, inx_music87_str)
    sue_pidginunit.set_idea(casa_otx_str, casa_inx_str)
    sue_pidginunit.set_idea(clean_otx_str, clean_inx_str)
    return sue_pidginunit


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


def get_casa_maison_road_otx2inx_dt() -> DataFrame:
    inx_music87_str = "music87"
    casa_inx_road = create_road(inx_music87_str, "maison")
    clean_inx_road = create_road(casa_inx_road, "propre")
    sweep_inx_road = create_road(clean_inx_road, "sweep")
    otx_music45_str = "music45"
    casa_otx_road = create_road(otx_music45_str, "casa")
    clean_otx_road = create_road(casa_otx_road, "clean")
    sweep_otx_road = create_road(clean_otx_road, "sweep")
    x_rd = default_wall_if_None()
    e7 = 7
    uw = default_unknown_word_if_None()

    inx_dt = DataFrame(
        columns=[
            "face_id",
            "event_id",
            "otx_wall",
            "inx_wall",
            "unknown_word",
            "otx_road",
            "inx_road",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_music45_str, inx_music87_str]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_road, casa_inx_road]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_road, clean_inx_road]
    inx_dt.loc[3] = ["Sue", e7, x_rd, x_rd, uw, sweep_otx_road, sweep_inx_road]
    return inx_dt


def get_casa_maison_idea_dt() -> DataFrame:
    inx_music87_str = "music87"
    casa_inx_str = "maison"
    clean_inx_str = "propre"
    sweep_inx_str = "sweep"
    otx_music45_str = "music45"
    casa_otx_str = "casa"
    clean_otx_str = "clean"
    sweep_otx_str = "sweep"
    x_rd = default_wall_if_None()
    uw = default_unknown_word_if_None()
    e7 = 7

    inx_dt = DataFrame(
        columns=[
            "face_id",
            "event_id",
            "otx_wall",
            "inx_wall",
            "unknown_word",
            "otx_idea",
            "inx_idea",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_music45_str, inx_music87_str]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_str, casa_inx_str]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_str, clean_inx_str]
    return inx_dt


def get_invalid_acctbridge() -> AcctBridge:
    sue_otx = f"Xio{default_wall_if_None()}"
    sue_inx = "Sue"
    zia_otx = "Zia"
    zia_inx = "Zia"
    acctbridge = acctbridge_shop(x_face_id="Sue")
    acctbridge.set_otx2inx(sue_otx, sue_inx)
    acctbridge.set_otx2inx(zia_otx, zia_inx)
    return acctbridge


def get_invalid_groupbridge() -> GroupBridge:
    sue_otx = f"Xio{default_wall_if_None()}"
    sue_inx = f"Sue{default_wall_if_None()}"
    zia_otx = "Zia"
    zia_inx = f"Zia{default_wall_if_None()}"
    x_groupbridge = groupbridge_shop(x_face_id="Sue")
    x_groupbridge.set_otx2inx(sue_otx, sue_inx)
    x_groupbridge.set_otx2inx(zia_otx, zia_inx)
    return x_groupbridge


def get_invalid_ideabridge() -> RoadBridge:
    clean_str = "clean"
    clean_inx = "propre"
    casa_otx = f"casa{default_wall_if_None()}"
    casa_inx = "casa"
    roadbridge = roadbridge_shop(x_face_id="Sue")
    roadbridge.set_otx2inx(clean_str, clean_inx)
    roadbridge.set_otx2inx(casa_otx, casa_inx)
    return roadbridge


def get_slash_ideabridge() -> IdeaBridge:
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    x_ideabridge = ideabridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
        x_event_id=7,
    )
    x_ideabridge.set_otx2inx(otx_music45_str, inx_music87_str)
    x_ideabridge.set_otx2inx(clean_otx_str, clean_inx_str)
    x_ideabridge.reveal_inx("running")
    return x_ideabridge


def get_slash_roadbridge() -> RoadBridge:
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    clean_otx_road = f"{otx_music45_str}{slash_otx_wall}{clean_otx_str}"
    clean_otx_road = f"{otx_music45_str}{colon_inx_wall}{clean_otx_str}"
    x_roadbridge = roadbridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
        x_event_id=7,
        x_ideabridge=get_slash_ideabridge(),
    )
    x_roadbridge.set_idea(clean_otx_str, clean_inx_str)
    x_roadbridge.set_otx2inx(otx_music45_str, inx_music87_str)
    x_roadbridge.reveal_inx(clean_otx_road)
    return x_roadbridge


def get_slash_groupbridge() -> GroupBridge:
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    swim_otx = f"swim{slash_otx_wall}"
    swim_inx = f"nage{colon_inx_wall}"
    climb_otx = f"climb{slash_otx_wall}"
    climb_inx = f"climb{colon_inx_wall}"
    x_groupbridge = groupbridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
        x_event_id=7,
    )
    x_groupbridge.set_otx2inx(swim_otx, swim_inx)
    x_groupbridge.set_otx2inx(climb_otx, climb_inx)
    return x_groupbridge


def get_slash_acctbridge() -> AcctBridge:
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_acctbridge = acctbridge_shop(
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
        x_face_id="Sue",
        x_event_id=7,
    )
    x_acctbridge.set_otx2inx(xio_otx, xio_inx)
    x_acctbridge.set_otx2inx(sue_otx, sue_inx)
    x_acctbridge.set_otx2inx(bob_otx, bob_inx)
    return x_acctbridge


def get_pidgin_core_attrs_are_none_acctbridge() -> AcctBridge:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_nan = float("nan")
    x_acctbridge = acctbridge_shop(
        x_face_id="Sue",
        x_event_id=7,
        x_otx_wall=x_nan,
        x_inx_wall=x_nan,
        x_unknown_word=x_nan,
    )
    x_acctbridge.set_otx2inx(xio_otx, xio_inx)
    x_acctbridge.set_otx2inx(sue_otx, sue_inx)
    x_acctbridge.set_otx2inx(bob_otx, bob_inx)
    return x_acctbridge
