from src.a01_way_logic.way import default_bridge_if_None, create_way, to_way
from src.a06_bud_logic._utils.str_a06 import (
    acct_name_str,
    rcontext_str,
    type_WayStr_str,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_term_if_None
from src.a16_pidgin_logic.map import (
    labelmap_shop,
    namemap_shop,
    tagmap_shop,
    waymap_shop,
    LabelMap,
    NameMap,
    TagMap,
    WayMap,
)
from src.a16_pidgin_logic.pidgin import PidginUnit, pidginunit_shop
from pandas import DataFrame


def get_clean_tagmap() -> TagMap:
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    tagmap = tagmap_shop(face_name="Sue")
    tagmap.set_otx2inx(clean_otx, clean_inx)
    tagmap.set_otx2inx(casa_otx, casa_inx)
    return tagmap


def get_clean_waymap() -> WayMap:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    bridge = default_bridge_if_None()
    clean_otx_way = f"{otx_accord45_str}{bridge}{clean_otx_str}"
    way_mapunit = waymap_shop(face_name="Sue")
    way_mapunit.set_tag(clean_otx_str, clean_inx_str)
    way_mapunit.set_otx2inx(otx_accord45_str, inx_accord87_str)
    way_mapunit.reveal_inx(clean_otx_way)
    return way_mapunit


def get_swim_labelmap() -> LabelMap:
    bridge = default_bridge_if_None()
    swim_otx = f"swim{bridge}"
    swim_inx = f"nage{bridge}"
    climb_otx = f"climb{bridge}"
    x_labelmap = labelmap_shop(face_name="Sue")
    x_labelmap.set_otx2inx(swim_otx, swim_inx)
    x_labelmap.set_otx2inx(climb_otx, climb_otx)
    return x_labelmap


def get_suita_namemap() -> NameMap:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_name_mapunit = namemap_shop(face_name="Sue")
    acct_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    acct_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    acct_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    return acct_name_mapunit


# def get_invalid_acct_name_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_bridge_if_None()}"
#     sue_inx = "Sue"
#     zia_otx = "Zia"
#     zia_inx = "Zia"
#     x_labelmap = mapunit_shop(type_NameStr_str(), face_name="Sue")
#     x_labelmap.set_otx2inx(sue_otx, sue_inx)
#     x_labelmap.set_otx2inx(zia_otx, zia_inx)
#     return x_labelmap


# def get_invalid_group_label_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_bridge_if_None()}"
#     sue_inx = f"Sue{default_bridge_if_None()}"
#     zia_otx = "Zia"
#     zia_inx = f"Zia{default_bridge_if_None()}"
#     x_labelmap = mapunit_shop(type_LabelStr_str(), face_name="Sue")
#     x_labelmap.set_otx2inx(sue_otx, sue_inx)
#     x_labelmap.set_otx2inx(zia_otx, zia_inx)
#     return x_labelmap


# def get_invalid_way_mapunit() -> MapUnit:
#     clean_str = "clean"
#     clean_inx = "propre"
#     casa_otx = f"casa{default_bridge_if_None()}"
#     casa_inx = "casa"
#     tagmap = mapunit_shop(type_TagStr_str(), face_name="Sue")
#     tagmap.set_otx2inx(clean_str, clean_inx)
#     tagmap.set_otx2inx(casa_otx, casa_inx)
#     return tagmap


def get_slash_waymap() -> WayMap:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    clean_otx_way = f"{otx_accord45_str}{slash_otx_bridge}{clean_otx_str}"
    clean_otx_way = f"{otx_accord45_str}{colon_inx_bridge}{clean_otx_str}"
    way_mapunit = waymap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
        face_name="Sue",
    )
    way_mapunit.set_tag(clean_otx_str, clean_inx_str)
    way_mapunit.set_otx2inx(otx_accord45_str, inx_accord87_str)
    way_mapunit.reveal_inx(clean_otx_way)
    return way_mapunit


def get_slash_labelmap() -> LabelMap:
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    swim_otx = f"swim{slash_otx_bridge}"
    swim_inx = f"nage{colon_inx_bridge}"
    climb_otx = f"climb{slash_otx_bridge}"
    climb_inx = f"climb{colon_inx_bridge}"
    x_labelmap = labelmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
        face_name="Sue",
    )
    x_labelmap.set_otx2inx(swim_otx, swim_inx)
    x_labelmap.set_otx2inx(climb_otx, climb_inx)
    return x_labelmap


def get_slash_namemap() -> NameMap:
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_name_mapunit = namemap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
        face_name="Sue",
    )
    acct_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    acct_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    acct_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    return acct_name_mapunit


def get_sue_pidginunit() -> PidginUnit:
    sue_pidginunit = pidginunit_shop("Sue")
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_pidginunit.set_labelmap(get_swim_labelmap())
    sue_pidginunit.set_tagmap(get_clean_tagmap())
    sue_pidginunit.set_waymap(get_clean_waymap())
    sue_pidginunit.waymap.tagmap = get_clean_tagmap()
    return sue_pidginunit


def get_suita_acct_name_otx_dt() -> DataFrame:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[acct_name_str()])
    otx_dt.loc[0, acct_name_str()] = zia_otx
    otx_dt.loc[1, acct_name_str()] = sue_otx
    otx_dt.loc[2, acct_name_str()] = bob_otx
    otx_dt.loc[3, acct_name_str()] = xio_otx
    return otx_dt


def get_suita_acct_name_inx_dt() -> DataFrame:
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    zia_otx = "Zia"
    inx_dt = DataFrame(columns=[acct_name_str()])
    inx_dt.loc[0, acct_name_str()] = xio_inx
    inx_dt.loc[1, acct_name_str()] = sue_inx
    inx_dt.loc[2, acct_name_str()] = bob_inx
    inx_dt.loc[3, acct_name_str()] = zia_otx
    return inx_dt


def get_casa_maison_pidginunit_set_by_otx2inx() -> PidginUnit:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    otx_accord45_way = to_way(otx_accord45_str)
    inx_accord87_way = to_way(inx_accord87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_way = create_way(otx_accord45_way, casa_otx_str)
    casa_inx_way = create_way(inx_accord87_way, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_way = create_way(casa_otx_way, clean_otx_str)
    clean_inx_way = create_way(casa_inx_way, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_way = create_way(clean_otx_way, sweep_str)
    sweep_inx_way = create_way(clean_inx_way, sweep_str)

    sue_pidginunit = pidginunit_shop("Sue", 7)
    rx = type_WayStr_str()
    sue_pidginunit.set_otx2inx(rx, otx_accord45_way, inx_accord87_way)
    sue_pidginunit.set_otx2inx(rx, casa_otx_way, casa_inx_way)
    sue_pidginunit.set_otx2inx(rx, clean_otx_way, clean_inx_way)
    sue_pidginunit.set_otx2inx(rx, sweep_otx_way, sweep_inx_way)
    return sue_pidginunit


def get_casa_maison_pidginunit_set_by_tag() -> PidginUnit:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_way = create_way(otx_accord45_str, casa_otx_str)
    casa_inx_way = create_way(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_way = create_way(casa_otx_way, clean_otx_str)
    clean_inx_way = create_way(casa_inx_way, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_way = create_way(clean_otx_way, sweep_str)
    sweep_inx_way = create_way(clean_inx_way, sweep_str)

    sue_pidginunit = pidginunit_shop("Sue", 7)
    sue_pidginunit.set_tag(otx_accord45_str, inx_accord87_str)
    sue_pidginunit.set_tag(casa_otx_str, casa_inx_str)
    sue_pidginunit.set_tag(clean_otx_str, clean_inx_str)
    return sue_pidginunit


def get_casa_maison_way_otx_dt() -> DataFrame:
    otx_accord45_str = "accord45"
    otx_accord45_way = to_way(otx_accord45_str)
    casa_otx_str = "casa"
    casa_otx_way = create_way(otx_accord45_str, casa_otx_str)
    clean_otx_str = "clean"
    clean_otx_way = create_way(casa_otx_way, clean_otx_str)
    sweep_str = "sweep"
    sweep_otx_way = create_way(clean_otx_way, sweep_str)
    otx_dt = DataFrame(columns=[rcontext_str()])
    otx_dt.loc[0, rcontext_str()] = otx_accord45_way
    otx_dt.loc[1, rcontext_str()] = casa_otx_way
    otx_dt.loc[2, rcontext_str()] = clean_otx_way
    otx_dt.loc[3, rcontext_str()] = sweep_otx_way
    return otx_dt


def get_casa_maison_way_inx_dt() -> DataFrame:
    inx_accord87_str = "accord87"
    inx_accord87_way = to_way(inx_accord87_str)
    casa_inx_way = create_way(inx_accord87_way, "maison")
    clean_inx_way = create_way(casa_inx_way, "propre")
    sweep_inx_way = create_way(clean_inx_way, "sweep")
    inx_dt = DataFrame(columns=[rcontext_str()])
    inx_dt.loc[0, rcontext_str()] = inx_accord87_way
    inx_dt.loc[1, rcontext_str()] = casa_inx_way
    inx_dt.loc[2, rcontext_str()] = clean_inx_way
    inx_dt.loc[3, rcontext_str()] = sweep_inx_way
    return inx_dt


def get_casa_maison_way_otx2inx_dt() -> DataFrame:
    inx_accord87_str = "accord87"
    inx_accord87_way = to_way(inx_accord87_str)
    casa_inx_way = create_way(inx_accord87_str, "maison")
    clean_inx_way = create_way(casa_inx_way, "propre")
    sweep_inx_way = create_way(clean_inx_way, "sweep")
    otx_accord45_str = "accord45"
    otx_accord45_way = to_way(otx_accord45_str)
    casa_otx_way = create_way(otx_accord45_way, "casa")
    clean_otx_way = create_way(casa_otx_way, "clean")
    sweep_otx_way = create_way(clean_otx_way, "sweep")
    x_rd = default_bridge_if_None()
    e7 = 7
    uw = default_unknown_term_if_None()

    inx_dt = DataFrame(
        columns=[
            "face_name",
            "event_int",
            "otx_bridge",
            "inx_bridge",
            "unknown_term",
            "otx_way",
            "inx_way",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_accord45_way, inx_accord87_way]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_way, casa_inx_way]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_way, clean_inx_way]
    inx_dt.loc[3] = ["Sue", e7, x_rd, x_rd, uw, sweep_otx_way, sweep_inx_way]
    return inx_dt


def get_casa_maison_tag_dt() -> DataFrame:
    inx_accord87_str = "accord87"
    casa_inx_str = "maison"
    clean_inx_str = "propre"
    sweep_inx_str = "sweep"
    otx_accord45_str = "accord45"
    casa_otx_str = "casa"
    clean_otx_str = "clean"
    sweep_otx_str = "sweep"
    x_rd = default_bridge_if_None()
    uw = default_unknown_term_if_None()
    e7 = 7

    inx_dt = DataFrame(
        columns=[
            "face_name",
            "event_int",
            "otx_bridge",
            "inx_bridge",
            "unknown_term",
            "otx_tag",
            "inx_tag",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_accord45_str, inx_accord87_str]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_str, casa_inx_str]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_str, clean_inx_str]
    return inx_dt


def get_invalid_namemap() -> NameMap:
    sue_otx = f"Xio{default_bridge_if_None()}"
    sue_inx = "Sue"
    zia_otx = "Zia"
    zia_inx = "Zia"
    namemap = namemap_shop(face_name="Sue")
    namemap.set_otx2inx(sue_otx, sue_inx)
    namemap.set_otx2inx(zia_otx, zia_inx)
    return namemap


def get_invalid_labelmap() -> LabelMap:
    sue_otx = f"Xio{default_bridge_if_None()}"
    sue_inx = f"Sue{default_bridge_if_None()}"
    zia_otx = "Zia"
    zia_inx = f"Zia{default_bridge_if_None()}"
    x_labelmap = labelmap_shop(face_name="Sue")
    x_labelmap.set_otx2inx(sue_otx, sue_inx)
    x_labelmap.set_otx2inx(zia_otx, zia_inx)
    return x_labelmap


def get_invalid_waymap() -> WayMap:
    casa_str = "casa"
    casa_otx = create_way(casa_str)
    casa_inx = create_way(casa_str)
    clean_str = create_way(casa_otx, "clean")
    clean_inx = create_way(casa_inx, "propre")
    waymap = waymap_shop(face_name="Sue")
    waymap.set_otx2inx(clean_str, clean_inx)
    # waymap.set_otx2inx(casa_otx, casa_inx)
    return waymap


def get_slash_tagmap() -> TagMap:
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    x_tagmap = tagmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
        face_name="Sue",
        event_int=7,
    )
    x_tagmap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    x_tagmap.set_otx2inx(clean_otx_str, clean_inx_str)
    x_tagmap.reveal_inx("running")
    return x_tagmap


def get_slash_waymap() -> WayMap:
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    otx_accord45_way = to_way(otx_accord45_str, slash_otx_bridge)
    inx_accord87_way = to_way(inx_accord87_str, colon_inx_bridge)
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_term = "UnknownTerm"
    clean_otx_way = create_way(otx_accord45_way, clean_otx_str, slash_otx_bridge)
    clean_inx_way = create_way(inx_accord87_way, clean_otx_str, colon_inx_bridge)
    x_waymap = waymap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
        face_name="Sue",
        event_int=7,
        x_tagmap=get_slash_tagmap(),
    )
    x_waymap.set_tag(clean_otx_str, clean_inx_str)
    x_waymap.set_otx2inx(otx_accord45_way, inx_accord87_way)
    x_waymap.reveal_inx(clean_otx_way)
    return x_waymap


def get_slash_labelmap() -> LabelMap:
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    swim_otx = f"swim{slash_otx_bridge}"
    swim_inx = f"nage{colon_inx_bridge}"
    climb_otx = f"climb{slash_otx_bridge}"
    climb_inx = f"climb{colon_inx_bridge}"
    x_labelmap = labelmap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
        face_name="Sue",
        event_int=7,
    )
    x_labelmap.set_otx2inx(swim_otx, swim_inx)
    x_labelmap.set_otx2inx(climb_otx, climb_inx)
    return x_labelmap


def get_slash_namemap() -> NameMap:
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_namemap = namemap_shop(
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
        face_name="Sue",
        event_int=7,
    )
    x_namemap.set_otx2inx(xio_otx, xio_inx)
    x_namemap.set_otx2inx(sue_otx, sue_inx)
    x_namemap.set_otx2inx(bob_otx, bob_inx)
    return x_namemap


def get_pidgin_core_attrs_are_none_namemap() -> NameMap:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_nan = float("nan")
    x_namemap = namemap_shop(
        face_name="Sue",
        event_int=7,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
        unknown_term=x_nan,
    )
    x_namemap.set_otx2inx(xio_otx, xio_inx)
    x_namemap.set_otx2inx(sue_otx, sue_inx)
    x_namemap.set_otx2inx(bob_otx, bob_inx)
    return x_namemap
