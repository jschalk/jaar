from pandas import DataFrame
from src.a01_rope_logic.rope import create_rope, default_knot_if_None, to_rope
from src.a16_pidgin_logic._ref.a16_terms import (
    RopePointer_str,
    reason_context_str,
    voice_name_str,
)
from src.a16_pidgin_logic.map import (
    LabelMap,
    NameMap,
    RopeMap,
    TitleMap,
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_str_if_None
from src.a16_pidgin_logic.pidgin_main import PidginUnit, pidginunit_shop


def get_clean_labelmap() -> LabelMap:
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    labelmap = labelmap_shop(face_name="Sue")
    labelmap.set_otx2inx(clean_otx, clean_inx)
    labelmap.set_otx2inx(casa_otx, casa_inx)
    return labelmap


def get_clean_ropemap() -> RopeMap:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    knot = default_knot_if_None()
    clean_otx_rope = create_rope(otx_amy45_str, clean_otx_str, knot)
    # clean_otx_rope = f"{knot}{otx_amy45_str}{knot}{clean_otx_str}{knot}"
    rope_mapunit = ropemap_shop(face_name="Sue")
    rope_mapunit.set_label(clean_otx_str, clean_inx_str)
    rope_mapunit.set_otx2inx(otx_amy45_rope, inx_amy87_rope)
    print(f"{rope_mapunit.otx2inx.keys()=}")
    rope_mapunit.reveal_inx(clean_otx_rope)
    return rope_mapunit


def get_swim_titlemap() -> TitleMap:
    knot = default_knot_if_None()
    swim_otx = f"swim{knot}"
    swim_inx = f"nage{knot}"
    climb_otx = f"climb{knot}"
    x_titlemap = titlemap_shop(face_name="Sue")
    x_titlemap.set_otx2inx(swim_otx, swim_inx)
    x_titlemap.set_otx2inx(climb_otx, climb_otx)
    return x_titlemap


def get_suita_namemap() -> NameMap:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    voice_name_mapunit = namemap_shop(face_name="Sue")
    voice_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    voice_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    voice_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    return voice_name_mapunit


# def get_invalid_voice_name_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_knot_if_None()}"
#     sue_inx = "Sue"
#     zia_otx = "Zia"
#     zia_inx = "Zia"
#     x_titlemap = mapunit_shop(NameTerm_str(), face_name="Sue")
#     x_titlemap.set_otx2inx(sue_otx, sue_inx)
#     x_titlemap.set_otx2inx(zia_otx, zia_inx)
#     return x_titlemap


# def get_invalid_group_title_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_knot_if_None()}"
#     sue_inx = f"Sue{default_knot_if_None()}"
#     zia_otx = "Zia"
#     zia_inx = f"Zia{default_knot_if_None()}"
#     x_titlemap = mapunit_shop(TitleTerm_str(), face_name="Sue")
#     x_titlemap.set_otx2inx(sue_otx, sue_inx)
#     x_titlemap.set_otx2inx(zia_otx, zia_inx)
#     return x_titlemap


# def get_invalid_rope_mapunit() -> MapUnit:
#     clean_str = "clean"
#     clean_inx = "propre"
#     casa_otx = f"casa{default_knot_if_None()}"
#     casa_inx = "casa"
#     labelmap = mapunit_shop(LabelTerm_str(), face_name="Sue")
#     labelmap.set_otx2inx(clean_str, clean_inx)
#     labelmap.set_otx2inx(casa_otx, casa_inx)
#     return labelmap


def get_slash_ropemap() -> RopeMap:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    clean_otx_rope = f"{otx_amy45_str}{slash_otx_knot}{clean_otx_str}"
    clean_otx_rope = f"{otx_amy45_str}{colon_inx_knot}{clean_otx_str}"
    rope_mapunit = ropemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        face_name="Sue",
    )
    rope_mapunit.set_label(clean_otx_str, clean_inx_str)
    rope_mapunit.set_otx2inx(otx_amy45_str, inx_amy87_str)
    rope_mapunit.reveal_inx(clean_otx_rope)
    return rope_mapunit


def get_slash_titlemap() -> TitleMap:
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    swim_otx = f"swim{slash_otx_knot}"
    swim_inx = f"nage{colon_inx_knot}"
    climb_otx = f"climb{slash_otx_knot}"
    climb_inx = f"climb{colon_inx_knot}"
    x_titlemap = titlemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        face_name="Sue",
    )
    x_titlemap.set_otx2inx(swim_otx, swim_inx)
    x_titlemap.set_otx2inx(climb_otx, climb_inx)
    return x_titlemap


def get_slash_namemap() -> NameMap:
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    voice_name_mapunit = namemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        face_name="Sue",
    )
    voice_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    voice_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    voice_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    return voice_name_mapunit


def get_sue_pidginunit() -> PidginUnit:
    sue_pidginunit = pidginunit_shop("Sue")
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_pidginunit.set_titlemap(get_swim_titlemap())
    sue_pidginunit.set_labelmap(get_clean_labelmap())
    sue_pidginunit.set_ropemap(get_clean_ropemap())
    sue_pidginunit.ropemap.labelmap = get_clean_labelmap()
    return sue_pidginunit


def get_suita_voice_name_otx_dt() -> DataFrame:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[voice_name_str()])
    otx_dt.loc[0, voice_name_str()] = zia_otx
    otx_dt.loc[1, voice_name_str()] = sue_otx
    otx_dt.loc[2, voice_name_str()] = bob_otx
    otx_dt.loc[3, voice_name_str()] = xio_otx
    return otx_dt


def get_suita_voice_name_inx_dt() -> DataFrame:
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    zia_otx = "Zia"
    inx_dt = DataFrame(columns=[voice_name_str()])
    inx_dt.loc[0, voice_name_str()] = xio_inx
    inx_dt.loc[1, voice_name_str()] = sue_inx
    inx_dt.loc[2, voice_name_str()] = bob_inx
    inx_dt.loc[3, voice_name_str()] = zia_otx
    return inx_dt


def get_casa_maison_pidginunit_set_by_otx2inx() -> PidginUnit:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_rope, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_rope, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_rope = create_rope(clean_otx_rope, sweep_str)
    sweep_inx_rope = create_rope(clean_inx_rope, sweep_str)

    sue_pidginunit = pidginunit_shop("Sue", 7)
    rx = RopePointer_str()
    sue_pidginunit.set_otx2inx(rx, otx_amy45_rope, inx_amy87_rope)
    sue_pidginunit.set_otx2inx(rx, casa_otx_rope, casa_inx_rope)
    sue_pidginunit.set_otx2inx(rx, clean_otx_rope, clean_inx_rope)
    sue_pidginunit.set_otx2inx(rx, sweep_otx_rope, sweep_inx_rope)
    return sue_pidginunit


def get_casa_maison_pidginunit_set_by_label() -> PidginUnit:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_str, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_rope = create_rope(clean_otx_rope, sweep_str)
    sweep_inx_rope = create_rope(clean_inx_rope, sweep_str)

    sue_pidginunit = pidginunit_shop("Sue", 7)
    sue_pidginunit.set_label(otx_amy45_str, inx_amy87_str)
    sue_pidginunit.set_label(casa_otx_str, casa_inx_str)
    sue_pidginunit.set_label(clean_otx_str, clean_inx_str)
    return sue_pidginunit


def get_casa_maison_rope_otx_dt() -> DataFrame:
    otx_amy45_str = "amy45"
    otx_amy45_rope = to_rope(otx_amy45_str)
    casa_otx_str = "casa"
    casa_otx_rope = create_rope(otx_amy45_str, casa_otx_str)
    clean_otx_str = "clean"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    sweep_str = "sweep"
    sweep_otx_rope = create_rope(clean_otx_rope, sweep_str)
    otx_dt = DataFrame(columns=[reason_context_str()])
    otx_dt.loc[0, reason_context_str()] = otx_amy45_rope
    otx_dt.loc[1, reason_context_str()] = casa_otx_rope
    otx_dt.loc[2, reason_context_str()] = clean_otx_rope
    otx_dt.loc[3, reason_context_str()] = sweep_otx_rope
    return otx_dt


def get_casa_maison_rope_inx_dt() -> DataFrame:
    inx_amy87_str = "amy87"
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_inx_rope = create_rope(inx_amy87_rope, "maison")
    clean_inx_rope = create_rope(casa_inx_rope, "propre")
    sweep_inx_rope = create_rope(clean_inx_rope, "sweep")
    inx_dt = DataFrame(columns=[reason_context_str()])
    inx_dt.loc[0, reason_context_str()] = inx_amy87_rope
    inx_dt.loc[1, reason_context_str()] = casa_inx_rope
    inx_dt.loc[2, reason_context_str()] = clean_inx_rope
    inx_dt.loc[3, reason_context_str()] = sweep_inx_rope
    return inx_dt


def get_casa_maison_rope_otx2inx_dt() -> DataFrame:
    inx_amy87_str = "amy87"
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_inx_rope = create_rope(inx_amy87_str, "maison")
    clean_inx_rope = create_rope(casa_inx_rope, "propre")
    sweep_inx_rope = create_rope(clean_inx_rope, "sweep")
    otx_amy45_str = "amy45"
    otx_amy45_rope = to_rope(otx_amy45_str)
    casa_otx_rope = create_rope(otx_amy45_rope, "casa")
    clean_otx_rope = create_rope(casa_otx_rope, "clean")
    sweep_otx_rope = create_rope(clean_otx_rope, "sweep")
    x_rd = default_knot_if_None()
    e7 = 7
    uw = default_unknown_str_if_None()

    inx_dt = DataFrame(
        columns=[
            "face_name",
            "event_int",
            "otx_knot",
            "inx_knot",
            "unknown_str",
            "otx_rope",
            "inx_rope",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_amy45_rope, inx_amy87_rope]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_rope, casa_inx_rope]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_rope, clean_inx_rope]
    inx_dt.loc[3] = ["Sue", e7, x_rd, x_rd, uw, sweep_otx_rope, sweep_inx_rope]
    return inx_dt


def get_casa_maison_label_dt() -> DataFrame:
    inx_amy87_str = "amy87"
    casa_inx_str = "maison"
    clean_inx_str = "propre"
    sweep_inx_str = "sweep"
    otx_amy45_str = "amy45"
    casa_otx_str = "casa"
    clean_otx_str = "clean"
    sweep_otx_str = "sweep"
    x_rd = default_knot_if_None()
    uw = default_unknown_str_if_None()
    e7 = 7

    inx_dt = DataFrame(
        columns=[
            "face_name",
            "event_int",
            "otx_knot",
            "inx_knot",
            "unknown_str",
            "otx_label",
            "inx_label",
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_amy45_str, inx_amy87_str]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_str, casa_inx_str]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_str, clean_inx_str]
    return inx_dt


def get_invalid_namemap() -> NameMap:
    sue_otx = f"Xio{default_knot_if_None()}"
    sue_inx = "Sue"
    zia_otx = "Zia"
    zia_inx = "Zia"
    namemap = namemap_shop(face_name="Sue")
    namemap.set_otx2inx(sue_otx, sue_inx)
    namemap.set_otx2inx(zia_otx, zia_inx)
    return namemap


def get_invalid_titlemap() -> TitleMap:
    sue_otx = f"Xio{default_knot_if_None()}"
    sue_inx = f"Sue{default_knot_if_None()}"
    zia_otx = "Zia"
    zia_inx = f"Zia{default_knot_if_None()}"
    x_titlemap = titlemap_shop(face_name="Sue")
    x_titlemap.set_otx2inx(sue_otx, sue_inx)
    x_titlemap.set_otx2inx(zia_otx, zia_inx)
    return x_titlemap


def get_invalid_ropemap() -> RopeMap:
    casa_str = "casa"
    casa_otx = create_rope(casa_str)
    casa_inx = create_rope(casa_str)
    clean_str = create_rope(casa_otx, "clean")
    clean_inx = create_rope(casa_inx, "propre")
    ropemap = ropemap_shop(face_name="Sue")
    ropemap.set_otx2inx(clean_str, clean_inx)
    # ropemap.set_otx2inx(casa_otx, casa_inx)
    return ropemap


def get_slash_labelmap() -> LabelMap:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    x_labelmap = labelmap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        face_name="Sue",
        event_int=7,
    )
    x_labelmap.set_otx2inx(otx_amy45_str, inx_amy87_str)
    x_labelmap.set_otx2inx(clean_otx_str, clean_inx_str)
    x_labelmap.reveal_inx("running")
    return x_labelmap


def get_slash_ropemap() -> RopeMap:
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str, slash_otx_knot)
    inx_amy87_rope = to_rope(inx_amy87_str, colon_inx_knot)
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_str = "UnknownTerm"
    clean_otx_rope = create_rope(otx_amy45_rope, clean_otx_str, slash_otx_knot)
    clean_inx_rope = create_rope(inx_amy87_rope, clean_otx_str, colon_inx_knot)
    x_ropemap = ropemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        face_name="Sue",
        event_int=7,
        x_labelmap=get_slash_labelmap(),
    )
    x_ropemap.set_label(clean_otx_str, clean_inx_str)
    x_ropemap.set_otx2inx(otx_amy45_rope, inx_amy87_rope)
    x_ropemap.reveal_inx(clean_otx_rope)
    return x_ropemap


def get_slash_titlemap() -> TitleMap:
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    swim_otx = f"swim{slash_otx_knot}"
    swim_inx = f"nage{colon_inx_knot}"
    climb_otx = f"climb{slash_otx_knot}"
    climb_inx = f"climb{colon_inx_knot}"
    x_titlemap = titlemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        face_name="Sue",
        event_int=7,
    )
    x_titlemap.set_otx2inx(swim_otx, swim_inx)
    x_titlemap.set_otx2inx(climb_otx, climb_inx)
    return x_titlemap


def get_slash_namemap() -> NameMap:
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_namemap = namemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
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
        otx_knot=x_nan,
        inx_knot=x_nan,
        unknown_str=x_nan,
    )
    x_namemap.set_otx2inx(xio_otx, xio_inx)
    x_namemap.set_otx2inx(sue_otx, sue_inx)
    x_namemap.set_otx2inx(bob_otx, bob_inx)
    return x_namemap
