from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_bridge_if_None, create_road
from src.f04_gift.atom_config import acct_id_str, base_str, type_RoadUnit_str
from src.f08_pidgin.map import (
    groupmap_shop,
    acctmap_shop,
    ideamap_shop,
    roadmap_shop,
    GroupMap,
    AcctMap,
    IdeaMap,
    RoadMap,
)
from src.f08_pidgin.pidgin import PidginUnit, pidginunit_shop
from pandas import DataFrame


def get_clean_ideamap() -> IdeaMap:
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    ideamap = ideamap_shop(face_id="Sue")
    ideamap.set_otx2inx(clean_otx, clean_inx)
    ideamap.set_otx2inx(casa_otx, casa_inx)
    return ideamap


def get_clean_roadmap() -> RoadMap:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    bridge = default_bridge_if_None()
    clean_otx_road = f"{otx_accord45_str}{bridge}{clean_otx_str}"
    road_mapunit = roadmap_shop(face_id="Sue")
    road_mapunit.set_idea(clean_otx_str, clean_inx_str)
    road_mapunit.set_otx2inx(otx_accord45_str, inx_accord87_str)
    road_mapunit.reveal_inx(clean_otx_road)
    return road_mapunit


def get_swim_groupmap() -> GroupMap:
    bridge = default_bridge_if_None()
    swim_otx = f"swim{bridge}"
    swim_inx = f"nage{bridge}"
    climb_otx = f"climb{bridge}"
    x_groupmap = groupmap_shop(face_id="Sue")
    x_groupmap.set_otx2inx(swim_otx, swim_inx)
    x_groupmap.set_otx2inx(climb_otx, climb_otx)
    return x_groupmap


def get_suita_acctmap() -> AcctMap:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_mapunit = acctmap_shop(face_id="Sue")
    acct_id_mapunit.set_otx2inx(xio_otx, xio_inx)
    acct_id_mapunit.set_otx2inx(sue_otx, sue_inx)
    acct_id_mapunit.set_otx2inx(bob_otx, bob_inx)
    return acct_id_mapunit


# def get_invalid_acct_id_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_bridge_if_None()}"
#     sue_inx = "Sue"
#     zia_otx = "Zia"
#     zia_inx = "Zia"
#     x_groupmap = mapunit_shop(type_AcctID_str(), face_id="Sue")
#     x_groupmap.set_otx2inx(sue_otx, sue_inx)
#     x_groupmap.set_otx2inx(zia_otx, zia_inx)
#     return x_groupmap


# def get_invalid_group_id_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_bridge_if_None()}"
#     sue_inx = f"Sue{default_bridge_if_None()}"
#     zia_otx = "Zia"
#     zia_inx = f"Zia{default_bridge_if_None()}"
#     x_groupmap = mapunit_shop(type_GroupID_str(), face_id="Sue")
#     x_groupmap.set_otx2inx(sue_otx, sue_inx)
#     x_groupmap.set_otx2inx(zia_otx, zia_inx)
#     return x_groupmap


# def get_invalid_road_mapunit() -> MapUnit:
#     clean_str = "clean"
#     clean_inx = "propre"
#     casa_otx = f"casa{default_bridge_if_None()}"
#     casa_inx = "casa"
#     ideamap = mapunit_shop(type_IdeaUnit_str(), face_id="Sue")
#     ideamap.set_otx2inx(clean_str, clean_inx)
#     ideamap.set_otx2inx(casa_otx, casa_inx)
#     return ideamap


def get_slash_roadmap() -> RoadMap:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    clean_otx_road = f"{otx_accord45_str}{slash_otx_bridge}{clean_otx_str}"
    clean_otx_road = f"{otx_accord45_str}{colon_inx_bridge}{clean_otx_str}"
    road_mapunit = roadmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
        face_id="Sue",
    )
    road_mapunit.set_idea(clean_otx_str, clean_inx_str)
    road_mapunit.set_otx2inx(otx_accord45_str, inx_accord87_str)
    road_mapunit.reveal_inx(clean_otx_road)
    return road_mapunit


def get_slash_groupmap() -> GroupMap:
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    swim_otx = f"swim{slash_otx_bridge}"
    swim_inx = f"nage{colon_inx_bridge}"
    climb_otx = f"climb{slash_otx_bridge}"
    climb_inx = f"climb{colon_inx_bridge}"
    x_groupmap = groupmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
        face_id="Sue",
    )
    x_groupmap.set_otx2inx(swim_otx, swim_inx)
    x_groupmap.set_otx2inx(climb_otx, climb_inx)
    return x_groupmap


def get_slash_acctmap() -> AcctMap:
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_mapunit = acctmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
        face_id="Sue",
    )
    acct_id_mapunit.set_otx2inx(xio_otx, xio_inx)
    acct_id_mapunit.set_otx2inx(sue_otx, sue_inx)
    acct_id_mapunit.set_otx2inx(bob_otx, bob_inx)
    return acct_id_mapunit


def get_sue_pidginunit() -> PidginUnit:
    sue_pidginunit = pidginunit_shop("Sue")
    sue_pidginunit.set_acctmap(get_suita_acctmap())
    sue_pidginunit.set_groupmap(get_swim_groupmap())
    sue_pidginunit.set_ideamap(get_clean_ideamap())
    sue_pidginunit.set_roadmap(get_clean_roadmap())
    sue_pidginunit.roadmap.ideamap = get_clean_ideamap()
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
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_accord45_str, casa_otx_str)
    casa_inx_road = create_road(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)

    sue_pidginunit = pidginunit_shop("Sue", 7)
    rx = type_RoadUnit_str()
    sue_pidginunit.set_otx2inx(rx, otx_accord45_str, inx_accord87_str)
    sue_pidginunit.set_otx2inx(rx, casa_otx_road, casa_inx_road)
    sue_pidginunit.set_otx2inx(rx, clean_otx_road, clean_inx_road)
    sue_pidginunit.set_otx2inx(rx, sweep_otx_road, sweep_inx_road)
    return sue_pidginunit


def get_casa_maison_pidginunit_set_by_idea() -> PidginUnit:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_accord45_str, casa_otx_str)
    casa_inx_road = create_road(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)

    sue_pidginunit = pidginunit_shop("Sue", 7)
    sue_pidginunit.set_idea(otx_accord45_str, inx_accord87_str)
    sue_pidginunit.set_idea(casa_otx_str, casa_inx_str)
    sue_pidginunit.set_idea(clean_otx_str, clean_inx_str)
    return sue_pidginunit


def get_casa_maison_road_otx_dt() -> DataFrame:
    otx_accord45_str = "accord45"
    casa_otx_str = "casa"
    casa_otx_road = create_road(otx_accord45_str, casa_otx_str)
    clean_otx_str = "clean"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    otx_dt = DataFrame(columns=[base_str()])
    otx_dt.loc[0, base_str()] = otx_accord45_str
    otx_dt.loc[1, base_str()] = casa_otx_road
    otx_dt.loc[2, base_str()] = clean_otx_road
    otx_dt.loc[3, base_str()] = sweep_otx_road
    return otx_dt


def get_casa_maison_road_inx_dt() -> DataFrame:
    inx_accord87_str = "accord87"
    casa_inx_road = create_road(inx_accord87_str, "maison")
    clean_inx_road = create_road(casa_inx_road, "propre")
    sweep_inx_road = create_road(clean_inx_road, "sweep")
    inx_dt = DataFrame(columns=[base_str()])
    inx_dt.loc[0, base_str()] = inx_accord87_str
    inx_dt.loc[1, base_str()] = casa_inx_road
    inx_dt.loc[2, base_str()] = clean_inx_road
    inx_dt.loc[3, base_str()] = sweep_inx_road
    return inx_dt


def get_casa_maison_road_otx2inx_dt() -> DataFrame:
    inx_accord87_str = "accord87"
    casa_inx_road = create_road(inx_accord87_str, "maison")
    clean_inx_road = create_road(casa_inx_road, "propre")
    sweep_inx_road = create_road(clean_inx_road, "sweep")
    otx_accord45_str = "accord45"
    casa_otx_road = create_road(otx_accord45_str, "casa")
    clean_otx_road = create_road(casa_otx_road, "clean")
    sweep_otx_road = create_road(clean_otx_road, "sweep")
    x_rd = default_bridge_if_None()
    e7 = 7
    uw = default_unknown_word_if_None()

    inx_dt = DataFrame(
        columns=[
            "face_id",
            "event_id",
            "otx_bridge",
            "inx_bridge",
            "unknown_word",
            "otx_road",
            "inx_road",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_accord45_str, inx_accord87_str]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_road, casa_inx_road]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_road, clean_inx_road]
    inx_dt.loc[3] = ["Sue", e7, x_rd, x_rd, uw, sweep_otx_road, sweep_inx_road]
    return inx_dt


def get_casa_maison_idea_dt() -> DataFrame:
    inx_accord87_str = "accord87"
    casa_inx_str = "maison"
    clean_inx_str = "propre"
    sweep_inx_str = "sweep"
    otx_accord45_str = "accord45"
    casa_otx_str = "casa"
    clean_otx_str = "clean"
    sweep_otx_str = "sweep"
    x_rd = default_bridge_if_None()
    uw = default_unknown_word_if_None()
    e7 = 7

    inx_dt = DataFrame(
        columns=[
            "face_id",
            "event_id",
            "otx_bridge",
            "inx_bridge",
            "unknown_word",
            "otx_idea",
            "inx_idea",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_accord45_str, inx_accord87_str]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_str, casa_inx_str]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_str, clean_inx_str]
    return inx_dt


def get_invalid_acctmap() -> AcctMap:
    sue_otx = f"Xio{default_bridge_if_None()}"
    sue_inx = "Sue"
    zia_otx = "Zia"
    zia_inx = "Zia"
    acctmap = acctmap_shop(face_id="Sue")
    acctmap.set_otx2inx(sue_otx, sue_inx)
    acctmap.set_otx2inx(zia_otx, zia_inx)
    return acctmap


def get_invalid_groupmap() -> GroupMap:
    sue_otx = f"Xio{default_bridge_if_None()}"
    sue_inx = f"Sue{default_bridge_if_None()}"
    zia_otx = "Zia"
    zia_inx = f"Zia{default_bridge_if_None()}"
    x_groupmap = groupmap_shop(face_id="Sue")
    x_groupmap.set_otx2inx(sue_otx, sue_inx)
    x_groupmap.set_otx2inx(zia_otx, zia_inx)
    return x_groupmap


def get_invalid_ideamap() -> RoadMap:
    clean_str = "clean"
    clean_inx = "propre"
    casa_otx = f"casa{default_bridge_if_None()}"
    casa_inx = "casa"
    roadmap = roadmap_shop(face_id="Sue")
    roadmap.set_otx2inx(clean_str, clean_inx)
    roadmap.set_otx2inx(casa_otx, casa_inx)
    return roadmap


def get_slash_ideamap() -> IdeaMap:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    x_ideamap = ideamap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
        face_id="Sue",
        event_id=7,
    )
    x_ideamap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    x_ideamap.set_otx2inx(clean_otx_str, clean_inx_str)
    x_ideamap.reveal_inx("running")
    return x_ideamap


def get_slash_roadmap() -> RoadMap:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    clean_otx_road = f"{otx_accord45_str}{slash_otx_bridge}{clean_otx_str}"
    clean_otx_road = f"{otx_accord45_str}{colon_inx_bridge}{clean_otx_str}"
    x_roadmap = roadmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
        face_id="Sue",
        event_id=7,
        x_ideamap=get_slash_ideamap(),
    )
    x_roadmap.set_idea(clean_otx_str, clean_inx_str)
    x_roadmap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    x_roadmap.reveal_inx(clean_otx_road)
    return x_roadmap


def get_slash_groupmap() -> GroupMap:
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    swim_otx = f"swim{slash_otx_bridge}"
    swim_inx = f"nage{colon_inx_bridge}"
    climb_otx = f"climb{slash_otx_bridge}"
    climb_inx = f"climb{colon_inx_bridge}"
    x_groupmap = groupmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
        face_id="Sue",
        event_id=7,
    )
    x_groupmap.set_otx2inx(swim_otx, swim_inx)
    x_groupmap.set_otx2inx(climb_otx, climb_inx)
    return x_groupmap


def get_slash_acctmap() -> AcctMap:
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_acctmap = acctmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
        face_id="Sue",
        event_id=7,
    )
    x_acctmap.set_otx2inx(xio_otx, xio_inx)
    x_acctmap.set_otx2inx(sue_otx, sue_inx)
    x_acctmap.set_otx2inx(bob_otx, bob_inx)
    return x_acctmap


def get_pidgin_core_attrs_are_none_acctmap() -> AcctMap:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_nan = float("nan")
    x_acctmap = acctmap_shop(
        face_id="Sue",
        event_id=7,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
        unknown_word=x_nan,
    )
    x_acctmap.set_otx2inx(xio_otx, xio_inx)
    x_acctmap.set_otx2inx(sue_otx, sue_inx)
    x_acctmap.set_otx2inx(bob_otx, bob_inx)
    return x_acctmap
