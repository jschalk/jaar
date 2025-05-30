from src.a00_data_toolbox.dict_toolbox import get_empty_str_if_None as if_none_str
from src.a01_way_logic.way import FiscLabel, FaceName
from src.a06_bud_logic.bud import BudUnit
from src.a09_pack_logic.pack import PackUnit
from src.a15_fisc_logic.fisc import FiscUnit
from src.a16_pidgin_logic.pidgin import PidginUnit
from src.a17_idea_logic.idea_config import (
    get_idea_format_headers,
    get_idea_format_filename,
    get_idea_format_headers,
)


def create_init_stance_idea_csv_strs() -> dict[str, str]:
    """Returns strings of csv headers with comma delimiter"""
    stance_idea_numbers = [
        "br00000",
        "br00001",
        "br00002",
        "br00003",
        "br00004",
        "br00005",
        # "br00006",
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
    for idea_number in stance_idea_numbers:
        idea_format_filename = get_idea_format_filename(idea_number)
        for idea_columns, idea_file_name in idea_format_headers.items():
            if idea_file_name == idea_format_filename:
                fisc_csv_strs[idea_number] = f"event_int,face_name,{idea_columns}\n"
    return fisc_csv_strs


def add_fiscunits_to_stance_csv_strs(
    fiscs_dict: dict[FiscLabel, FiscUnit],
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
        x_fisc.fisc_label,
        x_fisc.timeline.timeline_label,
        str(x_fisc.timeline.c400_number),
        str(x_fisc.timeline.yr1_jan1_offset),
        str(x_fisc.timeline.monthday_distortion),
        str(x_fisc.fund_coin),
        str(x_fisc.penny),
        str(x_fisc.respect_bit),
        x_bridge,
        str(x_fisc.job_listen_rotations),
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
        for deal_time, dealunit in brokerunits.deals.items():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_fisc.fisc_label,
                broker_owner_name,
                str(deal_time),
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
            for tran_time, amount in time_dict.items():
                fisc_label = x_fisc.fisc_label
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    fisc_label,
                    owner_name,
                    acct_name,
                    str(tran_time),
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
    for hour_concept in x_fisc.timeline.hours_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_fisc.fisc_label,
            str(hour_concept[1]),
            hour_concept[0],
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
    for month_concept in x_fisc.timeline.months_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_fisc.fisc_label,
            str(month_concept[1]),
            month_concept[0],
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
    for count_x, weekday_label in enumerate(x_fisc.timeline.weekdays_config):
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_fisc.fisc_label,
            str(count_x),
            weekday_label,
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
                x_bud.fisc_label,
                x_bud.owner_name,
                acctunit.acct_name,
                membership.group_title,
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
            x_bud.fisc_label,
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
    for conceptunit in x_bud._concept_dict.values():
        for awardlink in conceptunit.awardlinks.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_label,
                x_bud.owner_name,
                conceptunit.get_concept_way(),
                awardlink.awardee_title,
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
    for factunit in x_bud.conceptroot.factunits.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_bud.fisc_label,
            x_bud.owner_name,
            x_bud.conceptroot.get_concept_way(),
            factunit.fcontext,
            factunit.fstate,
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
    for conceptunit in x_bud._concept_dict.values():
        for group_title in conceptunit.laborunit._laborlinks:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_label,
                x_bud.owner_name,
                conceptunit.get_concept_way(),
                group_title,
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
    for conceptunit in x_bud._concept_dict.values():
        for group_title in conceptunit.healerlink._healer_names:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_label,
                x_bud.owner_name,
                conceptunit.get_concept_way(),
                group_title,
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
    for conceptunit in x_bud._concept_dict.values():
        for reasonunit in conceptunit.reasonunits.values():
            for premiseunit in reasonunit.premises.values():
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    x_bud.fisc_label,
                    x_bud.owner_name,
                    conceptunit.get_concept_way(),
                    reasonunit.rcontext,
                    premiseunit.pstate,
                    if_none_str(premiseunit.popen),
                    if_none_str(premiseunit.pnigh),
                    if_none_str(premiseunit.pdivisor),
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
    for conceptunit in x_bud._concept_dict.values():
        for reasonunit in conceptunit.reasonunits.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_label,
                x_bud.owner_name,
                conceptunit.get_concept_way(),
                reasonunit.rcontext,
                if_none_str(reasonunit.rconcept_active_requisite),
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
    for conceptunit in x_bud._concept_dict.values():
        if conceptunit != x_bud.conceptroot:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_bud.fisc_label,
                x_bud.owner_name,
                conceptunit.get_concept_way(),
                if_none_str(conceptunit.begin),
                if_none_str(conceptunit.close),
                if_none_str(conceptunit.addin),
                if_none_str(conceptunit.numor),
                if_none_str(conceptunit.denom),
                if_none_str(conceptunit.morph),
                if_none_str(conceptunit.gogo_want),
                if_none_str(conceptunit.stop_want),
                if_none_str(conceptunit.mass),
                if_none_str(conceptunit.pledge),
                if_none_str(conceptunit.problem_bool),
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
        x_bud.fisc_label,
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
    for x_otx, x_inx in x_pidginunit.titlemap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_str,
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
            x_pidginunit.unknown_str,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00044_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.labelmap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_str,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00045_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.waymap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_str,
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


def add_pack_to_br00020_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_acct_membership":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("acct_name"),
                budatom.jkeys.get("group_title"),
                if_none_str(budatom.jvalues.get("credit_vote")),
                if_none_str(budatom.jvalues.get("debtit_vote")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00021_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_acctunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("acct_name"),
                if_none_str(budatom.jvalues.get("credit_belief")),
                if_none_str(budatom.jvalues.get("debtit_belief")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00022_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_concept_awardlink":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("concept_way"),
                budatom.jkeys.get("awardee_title"),
                if_none_str(budatom.jvalues.get("give_force")),
                if_none_str(budatom.jvalues.get("take_force")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00023_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_concept_factunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("concept_way"),
                budatom.jkeys.get("fcontext"),
                if_none_str(budatom.jvalues.get("fstate")),
                if_none_str(budatom.jvalues.get("fopen")),
                if_none_str(budatom.jvalues.get("fnigh")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00024_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_concept_laborlink":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("concept_way"),
                budatom.jkeys.get("labor_title"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00025_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_concept_healerlink":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("concept_way"),
                budatom.jkeys.get("healer_name"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00026_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_concept_reason_premiseunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("concept_way"),
                budatom.jkeys.get("rcontext"),
                budatom.jkeys.get("pstate"),
                if_none_str(budatom.jvalues.get("popen")),
                if_none_str(budatom.jvalues.get("pnigh")),
                if_none_str(budatom.jvalues.get("pdivisor")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00027_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_concept_reasonunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("concept_way"),
                budatom.jkeys.get("rcontext"),
                if_none_str(budatom.jvalues.get("rconcept_active_requisite")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00028_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "bud_conceptunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                budatom.jkeys.get("concept_way"),
                if_none_str(budatom.jvalues.get("begin")),
                if_none_str(budatom.jvalues.get("close")),
                if_none_str(budatom.jvalues.get("addin")),
                if_none_str(budatom.jvalues.get("numor")),
                if_none_str(budatom.jvalues.get("denom")),
                if_none_str(budatom.jvalues.get("morph")),
                if_none_str(budatom.jvalues.get("gogo_want")),
                if_none_str(budatom.jvalues.get("stop_want")),
                if_none_str(budatom.jvalues.get("mass")),
                if_none_str(budatom.jvalues.get("pledge")),
                if_none_str(budatom.jvalues.get("problem_bool")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00029_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for budatom in x_packunit._buddelta.get_ordered_budatoms().values():
        if budatom.dimen == "budunit":
            print(f"{budatom=} {x_packunit.owner_name=}")
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.fisc_label,
                x_packunit.owner_name,
                if_none_str(budatom.jvalues.get("credor_respect")),
                if_none_str(budatom.jvalues.get("debtor_respect")),
                if_none_str(budatom.jvalues.get("fund_pool")),
                if_none_str(budatom.jvalues.get("max_tree_traverse")),
                if_none_str(budatom.jvalues.get("tally")),
                if_none_str(budatom.jvalues.get("fund_coin")),
                if_none_str(budatom.jvalues.get("penny")),
                if_none_str(budatom.jvalues.get("respect_bit")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_packunit_to_stance_csv_strs(
    x_pack: PackUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
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
    br00020_csv = add_pack_to_br00020_csv(br00020_csv, x_pack, csv_delimiter)
    br00021_csv = add_pack_to_br00021_csv(br00021_csv, x_pack, csv_delimiter)
    br00022_csv = add_pack_to_br00022_csv(br00022_csv, x_pack, csv_delimiter)
    br00023_csv = add_pack_to_br00023_csv(br00023_csv, x_pack, csv_delimiter)
    br00024_csv = add_pack_to_br00024_csv(br00024_csv, x_pack, csv_delimiter)
    br00025_csv = add_pack_to_br00025_csv(br00025_csv, x_pack, csv_delimiter)
    br00026_csv = add_pack_to_br00026_csv(br00026_csv, x_pack, csv_delimiter)
    br00027_csv = add_pack_to_br00027_csv(br00027_csv, x_pack, csv_delimiter)
    br00028_csv = add_pack_to_br00028_csv(br00028_csv, x_pack, csv_delimiter)
    br00029_csv = add_pack_to_br00029_csv(br00029_csv, x_pack, csv_delimiter)
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
