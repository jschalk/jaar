from src.f00_instrument.file import open_file
from src.f00_instrument.dict_toolbox import (
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    create_l2nested_csv_dict,
    get_positional_dict,
    add_headers_to_csv,
    get_empty_str_if_None as if_none_str,
)
from src.f01_road.road import FiscTitle, OwnerName, FaceName
from src.f02_bud.bud import BudUnit
from src.f03_chrono.chrono import timelineunit_shop
from src.f04_gift.atom import atom_insert, atom_delete, AtomUnit, atomrow_shop
from src.f04_gift.delta import buddelta_shop, get_dimens_cruds_buddelta, BudDelta
from src.f04_gift.gift import giftunit_shop, GiftUnit
from src.f05_listen.hubunit import hubunit_shop
from src.f07_fisc.fisc import fiscunit_shop, FiscUnit
from src.f08_pidgin.pidgin import PidginUnit
from src.f09_idea.idea_config import (
    get_idearef_from_file,
    get_idea_format_headers,
    get_idea_config_dict,
    get_idea_format_filename,
    get_idea_format_headers,
)
from src.f09_idea.idea_db_tool import csv_dict_to_excel
from pandas import DataFrame
from csv import reader as csv_reader
from dataclasses import dataclass


def create_init_stance_idea_brick_csv_strs() -> dict[str, str]:
    """Returns strings of csv headers with comma delimiter"""
    stance_idea_bricks = [
        "br00000",
        "br00001",
        "br00002",
        "br00003",
        "br00004",
        "br00005",
        "br00020",
        "br00021",
        "br00022",
        "br00023",
        "br00024",
        "br00025",
        "br00026",
        "br00027",
        "br00028",
        "br00029",
        "br00042",
        "br00043",
        "br00044",
        "br00045",
    ]
    idea_format_headers = get_idea_format_headers()

    fisc_csv_strs = {}
    for idea_brick in stance_idea_bricks:
        idea_format_filename = get_idea_format_filename(idea_brick)
        for idea_columns, idea_file_name in idea_format_headers.items():
            if idea_file_name == idea_format_filename:
                fisc_csv_strs[idea_brick] = f"face_name,event_int,{idea_columns}\n"
    return fisc_csv_strs


def add_fiscunits_to_stance_csv_strs(
    fiscs_dict: dict[FiscTitle, FiscUnit],
    fisc_csv_strs: dict[str, str],
    csv_delimiter: str,
):
    for x_fisc in fiscs_dict.values():
        add_fiscunit_to_stance_csv_strs(x_fisc, fisc_csv_strs, csv_delimiter)


def add_fiscunit_to_stance_csv_strs(
    x_fisc: FiscUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
) -> dict[str, str]:
    br00000_csv = fisc_csv_strs.get("br00000")
    br00001_csv = fisc_csv_strs.get("br00001")
    br00002_csv = fisc_csv_strs.get("br00002")
    br00003_csv = fisc_csv_strs.get("br00003")
    br00004_csv = fisc_csv_strs.get("br00004")
    br00005_csv = fisc_csv_strs.get("br00005")
    br00000_csv = _add_fiscunit_to_br00000_csv(br00000_csv, x_fisc, csv_delimiter)
    br00001_csv = _add_dealunit_to_br00001_csv(br00001_csv, x_fisc, csv_delimiter)
    br00002_csv = _add_cashbook_to_br00002_csv(br00002_csv, x_fisc, csv_delimiter)
    br00003_csv = _add_hours_to_br00003_csv(br00003_csv, x_fisc, csv_delimiter)
    br00004_csv = _add_months_to_br00004_csv(br00004_csv, x_fisc, csv_delimiter)
    br00005_csv = _add_weekdays_to_br00005_csv(br00005_csv, x_fisc, csv_delimiter)
    fisc_csv_strs["br00000"] = br00000_csv
    fisc_csv_strs["br00001"] = br00001_csv
    fisc_csv_strs["br00002"] = br00002_csv
    fisc_csv_strs["br00003"] = br00003_csv
    fisc_csv_strs["br00004"] = br00004_csv
    fisc_csv_strs["br00005"] = br00005_csv


def _add_fiscunit_to_br00000_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    if x_fisc.bridge == csv_delimiter:
        x_bridge = f"""\"{str(x_fisc.bridge)}\""""
    else:
        x_bridge = x_fisc.bridge

    x_row = [
        if_none_str(face_name),
        if_none_str(event_int),
        x_fisc.fisc_title,
        x_fisc.timeline.timeline_title,
        str(x_fisc.timeline.c400_number),
        str(x_fisc.timeline.yr1_jan1_offset),
        str(x_fisc.timeline.monthday_distortion),
        str(x_fisc.fund_coin),
        str(x_fisc.penny),
        str(x_fisc.respect_bit),
        x_bridge,
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def _add_dealunit_to_br00001_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for broker_owner_name, brokerunits in x_fisc.brokerunits.items():
        for time_int, dealunit in brokerunits.deals.items():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_fisc.fisc_title,
                broker_owner_name,
                str(time_int),
                str(dealunit.quota),
                str(dealunit.celldepth),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def _add_cashbook_to_br00002_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for owner_name, tranunit in x_fisc.cashbook.tranunits.items():
        for acct_name, time_dict in tranunit.items():
            for time_int, amount in time_dict.items():
                fisc_title = x_fisc.fisc_title
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    fisc_title,
                    owner_name,
                    acct_name,
                    str(time_int),
                    str(amount),
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def _add_hours_to_br00003_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for hour_item in x_fisc.timeline.hours_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_fisc.fisc_title,
            str(hour_item[1]),
            hour_item[0],
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_months_to_br00004_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for month_item in x_fisc.timeline.months_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_fisc.fisc_title,
            str(month_item[1]),
            month_item[0],
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_weekdays_to_br00005_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for count_x, weekday_title in enumerate(x_fisc.timeline.weekdays_config):
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_fisc.fisc_title,
            str(count_x),
            weekday_title,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_bud_to_br00020_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for acctunit in x_bud.accts.values():
        for membership in acctunit._memberships.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_title,
                x_bud.owner_name,
                acctunit.acct_name,
                membership.group_label,
                if_none_str(membership.credit_vote),
                if_none_str(membership.debtit_vote),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00021_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for acctunit in x_bud.accts.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_bud.fisc_title,
            x_bud.owner_name,
            acctunit.acct_name,
            if_none_str(acctunit.credit_belief),
            if_none_str(acctunit.debtit_belief),
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_bud_to_br00022_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for awardlink in itemunit.awardlinks.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_title,
                x_bud.owner_name,
                itemunit.get_road(),
                awardlink.awardee_tag,
                if_none_str(awardlink.give_force),
                if_none_str(awardlink.take_force),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00023_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for factunit in x_bud.itemroot.factunits.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_bud.fisc_title,
            x_bud.owner_name,
            x_bud.itemroot.get_road(),
            factunit.base,
            factunit.pick,
            if_none_str(factunit.fopen),
            if_none_str(factunit.fnigh),
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_bud_to_br00024_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for group_tag in itemunit.teamunit._teamlinks:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_title,
                x_bud.owner_name,
                itemunit.get_road(),
                group_tag,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00025_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for group_tag in itemunit.healerlink._healer_names:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_title,
                x_bud.owner_name,
                itemunit.get_road(),
                group_tag,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00026_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for reasonunit in itemunit.reasonunits.values():
            for premiseunit in reasonunit.premises.values():
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    x_bud.fisc_title,
                    x_bud.owner_name,
                    itemunit.get_road(),
                    reasonunit.base,
                    premiseunit.need,
                    if_none_str(premiseunit.open),
                    if_none_str(premiseunit.nigh),
                    if_none_str(premiseunit.divisor),
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def add_bud_to_br00027_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for reasonunit in itemunit.reasonunits.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_title,
                x_bud.owner_name,
                itemunit.get_road(),
                reasonunit.base,
                if_none_str(reasonunit.base_item_active_requisite),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00028_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        if itemunit != x_bud.itemroot:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_title,
                x_bud.owner_name,
                itemunit._parent_road,
                itemunit._item_title,
                if_none_str(itemunit.begin),
                if_none_str(itemunit.close),
                if_none_str(itemunit.addin),
                if_none_str(itemunit.numor),
                if_none_str(itemunit.denom),
                if_none_str(itemunit.morph),
                if_none_str(itemunit.gogo_want),
                if_none_str(itemunit.stop_want),
                if_none_str(itemunit.mass),
                if_none_str(itemunit.pledge),
                if_none_str(itemunit.problem_bool),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00029_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    x_row = [
        if_none_str(face_name),
        if_none_str(event_int),
        x_bud.fisc_title,
        x_bud.owner_name,
        if_none_str(x_bud.credor_respect),
        if_none_str(x_bud.debtor_respect),
        if_none_str(x_bud.fund_pool),
        if_none_str(x_bud.max_tree_traverse),
        if_none_str(x_bud.tally),
        if_none_str(x_bud.fund_coin),
        if_none_str(x_bud.penny),
        if_none_str(x_bud.respect_bit),
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def add_budunit_to_stance_csv_strs(
    x_bud: BudUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    br00020_csv = fisc_csv_strs.get("br00020")
    br00021_csv = fisc_csv_strs.get("br00021")
    br00022_csv = fisc_csv_strs.get("br00022")
    br00023_csv = fisc_csv_strs.get("br00023")
    br00024_csv = fisc_csv_strs.get("br00024")
    br00025_csv = fisc_csv_strs.get("br00025")
    br00026_csv = fisc_csv_strs.get("br00026")
    br00027_csv = fisc_csv_strs.get("br00027")
    br00028_csv = fisc_csv_strs.get("br00028")
    br00029_csv = fisc_csv_strs.get("br00029")
    br00020_csv = add_bud_to_br00020_csv(br00020_csv, x_bud, csv_delimiter)
    br00021_csv = add_bud_to_br00021_csv(br00021_csv, x_bud, csv_delimiter)
    br00022_csv = add_bud_to_br00022_csv(br00022_csv, x_bud, csv_delimiter)
    br00023_csv = add_bud_to_br00023_csv(br00023_csv, x_bud, csv_delimiter)
    br00024_csv = add_bud_to_br00024_csv(br00024_csv, x_bud, csv_delimiter)
    br00025_csv = add_bud_to_br00025_csv(br00025_csv, x_bud, csv_delimiter)
    br00026_csv = add_bud_to_br00026_csv(br00026_csv, x_bud, csv_delimiter)
    br00027_csv = add_bud_to_br00027_csv(br00027_csv, x_bud, csv_delimiter)
    br00028_csv = add_bud_to_br00028_csv(br00028_csv, x_bud, csv_delimiter)
    br00029_csv = add_bud_to_br00029_csv(br00029_csv, x_bud, csv_delimiter)
    fisc_csv_strs["br00020"] = br00020_csv
    fisc_csv_strs["br00021"] = br00021_csv
    fisc_csv_strs["br00022"] = br00022_csv
    fisc_csv_strs["br00023"] = br00023_csv
    fisc_csv_strs["br00024"] = br00024_csv
    fisc_csv_strs["br00025"] = br00025_csv
    fisc_csv_strs["br00026"] = br00026_csv
    fisc_csv_strs["br00027"] = br00027_csv
    fisc_csv_strs["br00028"] = br00028_csv
    fisc_csv_strs["br00029"] = br00029_csv


def add_to_br00042_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.labelmap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00043_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.namemap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00044_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.titlemap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00045_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.roadmap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_pidginunit_to_stance_csv_strs(
    x_pidgin: PidginUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    br00042_csv = fisc_csv_strs.get("br00042")
    br00043_csv = fisc_csv_strs.get("br00043")
    br00044_csv = fisc_csv_strs.get("br00044")
    br00045_csv = fisc_csv_strs.get("br00045")
    br00042_csv = add_to_br00042_csv(br00042_csv, x_pidgin, csv_delimiter)
    br00043_csv = add_to_br00043_csv(br00043_csv, x_pidgin, csv_delimiter)
    br00044_csv = add_to_br00044_csv(br00044_csv, x_pidgin, csv_delimiter)
    br00045_csv = add_to_br00045_csv(br00045_csv, x_pidgin, csv_delimiter)
    fisc_csv_strs["br00042"] = br00042_csv
    fisc_csv_strs["br00043"] = br00043_csv
    fisc_csv_strs["br00044"] = br00044_csv
    fisc_csv_strs["br00045"] = br00045_csv


def add_gift_to_br00020_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_acct_membership":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("acct_name"),
                atomunit.jkeys.get("group_label"),
                if_none_str(atomunit.jvalues.get("credit_vote")),
                if_none_str(atomunit.jvalues.get("debtit_vote")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00021_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_acctunit":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("acct_name"),
                if_none_str(atomunit.jvalues.get("credit_belief")),
                if_none_str(atomunit.jvalues.get("debtit_belief")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00022_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_item_awardlink":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("road"),
                atomunit.jkeys.get("awardee_tag"),
                if_none_str(atomunit.jvalues.get("give_force")),
                if_none_str(atomunit.jvalues.get("take_force")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00023_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_item_factunit":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("road"),
                atomunit.jkeys.get("base"),
                if_none_str(atomunit.jvalues.get("pick")),
                if_none_str(atomunit.jvalues.get("fopen")),
                if_none_str(atomunit.jvalues.get("fnigh")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00024_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_item_teamlink":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("road"),
                atomunit.jkeys.get("team_tag"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00025_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_item_healerlink":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("road"),
                atomunit.jkeys.get("healer_name"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00026_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_item_reason_premiseunit":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("road"),
                atomunit.jkeys.get("base"),
                atomunit.jkeys.get("need"),
                if_none_str(atomunit.jvalues.get("open")),
                if_none_str(atomunit.jvalues.get("nigh")),
                if_none_str(atomunit.jvalues.get("divisor")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00027_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_item_reasonunit":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("road"),
                atomunit.jkeys.get("base"),
                if_none_str(atomunit.jvalues.get("base_item_active_requisite")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00028_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "bud_itemunit":
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                atomunit.jkeys.get("parent_road"),
                atomunit.jkeys.get("item_title"),
                if_none_str(atomunit.jvalues.get("begin")),
                if_none_str(atomunit.jvalues.get("close")),
                if_none_str(atomunit.jvalues.get("addin")),
                if_none_str(atomunit.jvalues.get("numor")),
                if_none_str(atomunit.jvalues.get("denom")),
                if_none_str(atomunit.jvalues.get("morph")),
                if_none_str(atomunit.jvalues.get("gogo_want")),
                if_none_str(atomunit.jvalues.get("stop_want")),
                if_none_str(atomunit.jvalues.get("mass")),
                if_none_str(atomunit.jvalues.get("pledge")),
                if_none_str(atomunit.jvalues.get("problem_bool")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_gift_to_br00029_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    for atomunit in x_giftunit._buddelta.get_ordered_atomunits().values():
        if atomunit.dimen == "budunit":
            print(f"{atomunit=} {x_giftunit.owner_name=}")
            x_row = [
                x_giftunit.face_name,
                str(x_giftunit.event_int),
                x_giftunit.fisc_title,
                x_giftunit.owner_name,
                if_none_str(atomunit.jvalues.get("credor_respect")),
                if_none_str(atomunit.jvalues.get("debtor_respect")),
                if_none_str(atomunit.jvalues.get("fund_pool")),
                if_none_str(atomunit.jvalues.get("max_tree_traverse")),
                if_none_str(atomunit.jvalues.get("tally")),
                if_none_str(atomunit.jvalues.get("fund_coin")),
                if_none_str(atomunit.jvalues.get("penny")),
                if_none_str(atomunit.jvalues.get("respect_bit")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_giftunit_to_stance_csv_strs(
    x_gift: GiftUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
):
    br00020_csv = fisc_csv_strs.get("br00020")
    br00021_csv = fisc_csv_strs.get("br00021")
    br00022_csv = fisc_csv_strs.get("br00022")
    br00023_csv = fisc_csv_strs.get("br00023")
    br00024_csv = fisc_csv_strs.get("br00024")
    br00025_csv = fisc_csv_strs.get("br00025")
    br00026_csv = fisc_csv_strs.get("br00026")
    br00027_csv = fisc_csv_strs.get("br00027")
    br00028_csv = fisc_csv_strs.get("br00028")
    br00029_csv = fisc_csv_strs.get("br00029")
    br00020_csv = add_gift_to_br00020_csv(br00020_csv, x_gift, csv_delimiter)
    br00021_csv = add_gift_to_br00021_csv(br00021_csv, x_gift, csv_delimiter)
    br00022_csv = add_gift_to_br00022_csv(br00022_csv, x_gift, csv_delimiter)
    br00023_csv = add_gift_to_br00023_csv(br00023_csv, x_gift, csv_delimiter)
    br00024_csv = add_gift_to_br00024_csv(br00024_csv, x_gift, csv_delimiter)
    br00025_csv = add_gift_to_br00025_csv(br00025_csv, x_gift, csv_delimiter)
    br00026_csv = add_gift_to_br00026_csv(br00026_csv, x_gift, csv_delimiter)
    br00027_csv = add_gift_to_br00027_csv(br00027_csv, x_gift, csv_delimiter)
    br00028_csv = add_gift_to_br00028_csv(br00028_csv, x_gift, csv_delimiter)
    br00029_csv = add_gift_to_br00029_csv(br00029_csv, x_gift, csv_delimiter)
    fisc_csv_strs["br00020"] = br00020_csv
    fisc_csv_strs["br00021"] = br00021_csv
    fisc_csv_strs["br00022"] = br00022_csv
    fisc_csv_strs["br00023"] = br00023_csv
    fisc_csv_strs["br00024"] = br00024_csv
    fisc_csv_strs["br00025"] = br00025_csv
    fisc_csv_strs["br00026"] = br00026_csv
    fisc_csv_strs["br00027"] = br00027_csv
    fisc_csv_strs["br00028"] = br00028_csv
    fisc_csv_strs["br00029"] = br00029_csv
