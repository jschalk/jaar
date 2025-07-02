from src.a00_data_toolbox.dict_toolbox import get_empty_str_if_None as if_none_str
from src.a01_term_logic.term import BeliefLabel, FaceName
from src.a06_believer_logic.believer import BelieverUnit
from src.a09_pack_logic.pack import PackUnit
from src.a15_belief_logic.belief import BeliefUnit
from src.a16_pidgin_logic.pidgin import PidginUnit
from src.a17_idea_logic.idea_config import (
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

    belief_csv_strs = {}
    for idea_number in stance_idea_numbers:
        idea_format_filename = get_idea_format_filename(idea_number)
        for idea_columns, idea_file_name in idea_format_headers.items():
            if idea_file_name == idea_format_filename:
                belief_csv_strs[idea_number] = f"event_int,face_name,{idea_columns}\n"
    return belief_csv_strs


def add_beliefunits_to_stance_csv_strs(
    beliefs_dict: dict[BeliefLabel, BeliefUnit],
    belief_csv_strs: dict[str, str],
    csv_delimiter: str,
):
    for x_belief in beliefs_dict.values():
        add_beliefunit_to_stance_csv_strs(x_belief, belief_csv_strs, csv_delimiter)


def add_beliefunit_to_stance_csv_strs(
    x_belief: BeliefUnit, belief_csv_strs: dict[str, str], csv_delimiter: str
) -> dict[str, str]:
    br00000_csv = belief_csv_strs.get("br00000")
    br00001_csv = belief_csv_strs.get("br00001")
    br00002_csv = belief_csv_strs.get("br00002")
    br00003_csv = belief_csv_strs.get("br00003")
    br00004_csv = belief_csv_strs.get("br00004")
    br00005_csv = belief_csv_strs.get("br00005")
    br00000_csv = _add_beliefunit_to_br00000_csv(br00000_csv, x_belief, csv_delimiter)
    br00001_csv = _add_budunit_to_br00001_csv(br00001_csv, x_belief, csv_delimiter)
    br00002_csv = _add_paybook_to_br00002_csv(br00002_csv, x_belief, csv_delimiter)
    br00003_csv = _add_hours_to_br00003_csv(br00003_csv, x_belief, csv_delimiter)
    br00004_csv = _add_months_to_br00004_csv(br00004_csv, x_belief, csv_delimiter)
    br00005_csv = _add_weekdays_to_br00005_csv(br00005_csv, x_belief, csv_delimiter)
    belief_csv_strs["br00000"] = br00000_csv
    belief_csv_strs["br00001"] = br00001_csv
    belief_csv_strs["br00002"] = br00002_csv
    belief_csv_strs["br00003"] = br00003_csv
    belief_csv_strs["br00004"] = br00004_csv
    belief_csv_strs["br00005"] = br00005_csv


def _add_beliefunit_to_br00000_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    if x_belief.knot == csv_delimiter:
        x_knot = f"""\"{str(x_belief.knot)}\""""
    else:
        x_knot = x_belief.knot

    x_row = [
        if_none_str(face_name),
        if_none_str(event_int),
        x_belief.belief_label,
        x_belief.timeline.timeline_label,
        str(x_belief.timeline.c400_number),
        str(x_belief.timeline.yr1_jan1_offset),
        str(x_belief.timeline.monthday_distortion),
        str(x_belief.fund_iota),
        str(x_belief.penny),
        str(x_belief.respect_bit),
        x_knot,
        str(x_belief.job_listen_rotations),
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def _add_budunit_to_br00001_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for broker_believer_name, brokerunits in x_belief.brokerunits.items():
        for bud_time, budunit in brokerunits.buds.items():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_belief.belief_label,
                broker_believer_name,
                str(bud_time),
                str(budunit.quota),
                str(budunit.celldepth),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def _add_paybook_to_br00002_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for believer_name, tranunit in x_belief.paybook.tranunits.items():
        for acct_name, time_dict in tranunit.items():
            for tran_time, amount in time_dict.items():
                belief_label = x_belief.belief_label
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    belief_label,
                    believer_name,
                    acct_name,
                    str(tran_time),
                    str(amount),
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def _add_hours_to_br00003_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for hour_plan in x_belief.timeline.hours_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_belief.belief_label,
            str(hour_plan[1]),
            hour_plan[0],
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_months_to_br00004_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for month_plan in x_belief.timeline.months_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_belief.belief_label,
            str(month_plan[1]),
            month_plan[0],
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_weekdays_to_br00005_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for count_x, weekday_label in enumerate(x_belief.timeline.weekdays_config):
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_belief.belief_label,
            str(count_x),
            weekday_label,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_believer_to_br00020_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for acctunit in x_believer.accts.values():
        for membership in acctunit._memberships.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                acctunit.acct_name,
                membership.group_title,
                if_none_str(membership.group_cred_points),
                if_none_str(membership.group_debt_points),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_believer_to_br00021_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for acctunit in x_believer.accts.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_believer.belief_label,
            x_believer.believer_name,
            acctunit.acct_name,
            if_none_str(acctunit.acct_cred_points),
            if_none_str(acctunit.acct_debt_points),
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_believer_to_br00022_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_believer._plan_dict.values():
        for awardlink in planunit.awardlinks.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                planunit.get_plan_rope(),
                awardlink.awardee_title,
                if_none_str(awardlink.give_force),
                if_none_str(awardlink.take_force),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_believer_to_br00023_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for factunit in x_believer.planroot.factunits.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_believer.belief_label,
            x_believer.believer_name,
            x_believer.planroot.get_plan_rope(),
            factunit.fcontext,
            factunit.fstate,
            if_none_str(factunit.fopen),
            if_none_str(factunit.fnigh),
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_believer_to_br00024_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_believer._plan_dict.values():
        for group_title in planunit.laborunit._laborlinks:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                planunit.get_plan_rope(),
                group_title,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_believer_to_br00025_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_believer._plan_dict.values():
        for group_title in planunit.healerlink._healer_names:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                planunit.get_plan_rope(),
                group_title,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_believer_to_br00026_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_believer._plan_dict.values():
        for reasonunit in planunit.reasonunits.values():
            for premiseunit in reasonunit.premises.values():
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    x_believer.belief_label,
                    x_believer.believer_name,
                    planunit.get_plan_rope(),
                    reasonunit.rcontext,
                    premiseunit.pstate,
                    if_none_str(premiseunit.popen),
                    if_none_str(premiseunit.pnigh),
                    if_none_str(premiseunit.pdivisor),
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def add_believer_to_br00027_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_believer._plan_dict.values():
        for reasonunit in planunit.reasonunits.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                planunit.get_plan_rope(),
                reasonunit.rcontext,
                if_none_str(reasonunit.rplan_active_requisite),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_believer_to_br00028_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_believer._plan_dict.values():
        if planunit != x_believer.planroot:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                planunit.get_plan_rope(),
                if_none_str(planunit.begin),
                if_none_str(planunit.close),
                if_none_str(planunit.addin),
                if_none_str(planunit.numor),
                if_none_str(planunit.denom),
                if_none_str(planunit.morph),
                if_none_str(planunit.gogo_want),
                if_none_str(planunit.stop_want),
                if_none_str(planunit.mass),
                if_none_str(planunit.task),
                if_none_str(planunit.problem_bool),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_believer_to_br00029_csv(
    x_csv: str,
    x_believer: BelieverUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    x_row = [
        if_none_str(face_name),
        if_none_str(event_int),
        x_believer.belief_label,
        x_believer.believer_name,
        if_none_str(x_believer.credor_respect),
        if_none_str(x_believer.debtor_respect),
        if_none_str(x_believer.fund_pool),
        if_none_str(x_believer.max_tree_traverse),
        if_none_str(x_believer.tally),
        if_none_str(x_believer.fund_iota),
        if_none_str(x_believer.penny),
        if_none_str(x_believer.respect_bit),
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def add_believerunit_to_stance_csv_strs(
    x_believer: BelieverUnit, belief_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    br00020_csv = belief_csv_strs.get("br00020")
    br00021_csv = belief_csv_strs.get("br00021")
    br00022_csv = belief_csv_strs.get("br00022")
    br00023_csv = belief_csv_strs.get("br00023")
    br00024_csv = belief_csv_strs.get("br00024")
    br00025_csv = belief_csv_strs.get("br00025")
    br00026_csv = belief_csv_strs.get("br00026")
    br00027_csv = belief_csv_strs.get("br00027")
    br00028_csv = belief_csv_strs.get("br00028")
    br00029_csv = belief_csv_strs.get("br00029")
    br00020_csv = add_believer_to_br00020_csv(br00020_csv, x_believer, csv_delimiter)
    br00021_csv = add_believer_to_br00021_csv(br00021_csv, x_believer, csv_delimiter)
    br00022_csv = add_believer_to_br00022_csv(br00022_csv, x_believer, csv_delimiter)
    br00023_csv = add_believer_to_br00023_csv(br00023_csv, x_believer, csv_delimiter)
    br00024_csv = add_believer_to_br00024_csv(br00024_csv, x_believer, csv_delimiter)
    br00025_csv = add_believer_to_br00025_csv(br00025_csv, x_believer, csv_delimiter)
    br00026_csv = add_believer_to_br00026_csv(br00026_csv, x_believer, csv_delimiter)
    br00027_csv = add_believer_to_br00027_csv(br00027_csv, x_believer, csv_delimiter)
    br00028_csv = add_believer_to_br00028_csv(br00028_csv, x_believer, csv_delimiter)
    br00029_csv = add_believer_to_br00029_csv(br00029_csv, x_believer, csv_delimiter)
    belief_csv_strs["br00020"] = br00020_csv
    belief_csv_strs["br00021"] = br00021_csv
    belief_csv_strs["br00022"] = br00022_csv
    belief_csv_strs["br00023"] = br00023_csv
    belief_csv_strs["br00024"] = br00024_csv
    belief_csv_strs["br00025"] = br00025_csv
    belief_csv_strs["br00026"] = br00026_csv
    belief_csv_strs["br00027"] = br00027_csv
    belief_csv_strs["br00028"] = br00028_csv
    belief_csv_strs["br00029"] = br00029_csv


def add_to_br00042_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.titlemap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_knot,
            x_inx,
            x_pidginunit.inx_knot,
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
            x_pidginunit.otx_knot,
            x_inx,
            x_pidginunit.inx_knot,
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
            x_pidginunit.otx_knot,
            x_inx,
            x_pidginunit.inx_knot,
            x_pidginunit.unknown_str,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00045_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.ropemap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_knot,
            x_inx,
            x_pidginunit.inx_knot,
            x_pidginunit.unknown_str,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_pidginunit_to_stance_csv_strs(
    x_pidgin: PidginUnit, belief_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    br00042_csv = belief_csv_strs.get("br00042")
    br00043_csv = belief_csv_strs.get("br00043")
    br00044_csv = belief_csv_strs.get("br00044")
    br00045_csv = belief_csv_strs.get("br00045")
    br00042_csv = add_to_br00042_csv(br00042_csv, x_pidgin, csv_delimiter)
    br00043_csv = add_to_br00043_csv(br00043_csv, x_pidgin, csv_delimiter)
    br00044_csv = add_to_br00044_csv(br00044_csv, x_pidgin, csv_delimiter)
    br00045_csv = add_to_br00045_csv(br00045_csv, x_pidgin, csv_delimiter)
    belief_csv_strs["br00042"] = br00042_csv
    belief_csv_strs["br00043"] = br00043_csv
    belief_csv_strs["br00044"] = br00044_csv
    belief_csv_strs["br00045"] = br00045_csv


def add_pack_to_br00020_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_acct_membership":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("acct_name"),
                believeratom.jkeys.get("group_title"),
                if_none_str(believeratom.jvalues.get("group_cred_points")),
                if_none_str(believeratom.jvalues.get("group_debt_points")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00021_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_acctunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("acct_name"),
                if_none_str(believeratom.jvalues.get("acct_cred_points")),
                if_none_str(believeratom.jvalues.get("acct_debt_points")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00022_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_awardlink":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("awardee_title"),
                if_none_str(believeratom.jvalues.get("give_force")),
                if_none_str(believeratom.jvalues.get("take_force")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00023_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_factunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("fcontext"),
                if_none_str(believeratom.jvalues.get("fstate")),
                if_none_str(believeratom.jvalues.get("fopen")),
                if_none_str(believeratom.jvalues.get("fnigh")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00024_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_laborlink":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("labor_title"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00025_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_healerlink":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("healer_name"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00026_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_reason_premiseunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("rcontext"),
                believeratom.jkeys.get("pstate"),
                if_none_str(believeratom.jvalues.get("popen")),
                if_none_str(believeratom.jvalues.get("pnigh")),
                if_none_str(believeratom.jvalues.get("pdivisor")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00027_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_reasonunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("rcontext"),
                if_none_str(believeratom.jvalues.get("rplan_active_requisite")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00028_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_planunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                if_none_str(believeratom.jvalues.get("begin")),
                if_none_str(believeratom.jvalues.get("close")),
                if_none_str(believeratom.jvalues.get("addin")),
                if_none_str(believeratom.jvalues.get("numor")),
                if_none_str(believeratom.jvalues.get("denom")),
                if_none_str(believeratom.jvalues.get("morph")),
                if_none_str(believeratom.jvalues.get("gogo_want")),
                if_none_str(believeratom.jvalues.get("stop_want")),
                if_none_str(believeratom.jvalues.get("mass")),
                if_none_str(believeratom.jvalues.get("task")),
                if_none_str(believeratom.jvalues.get("problem_bool")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00029_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believerunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                if_none_str(believeratom.jvalues.get("credor_respect")),
                if_none_str(believeratom.jvalues.get("debtor_respect")),
                if_none_str(believeratom.jvalues.get("fund_pool")),
                if_none_str(believeratom.jvalues.get("max_tree_traverse")),
                if_none_str(believeratom.jvalues.get("tally")),
                if_none_str(believeratom.jvalues.get("fund_iota")),
                if_none_str(believeratom.jvalues.get("penny")),
                if_none_str(believeratom.jvalues.get("respect_bit")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_packunit_to_stance_csv_strs(
    x_pack: PackUnit, belief_csv_strs: dict[str, str], csv_delimiter: str
):
    br00020_csv = belief_csv_strs.get("br00020")
    br00021_csv = belief_csv_strs.get("br00021")
    br00022_csv = belief_csv_strs.get("br00022")
    br00023_csv = belief_csv_strs.get("br00023")
    br00024_csv = belief_csv_strs.get("br00024")
    br00025_csv = belief_csv_strs.get("br00025")
    br00026_csv = belief_csv_strs.get("br00026")
    br00027_csv = belief_csv_strs.get("br00027")
    br00028_csv = belief_csv_strs.get("br00028")
    br00029_csv = belief_csv_strs.get("br00029")
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
    belief_csv_strs["br00020"] = br00020_csv
    belief_csv_strs["br00021"] = br00021_csv
    belief_csv_strs["br00022"] = br00022_csv
    belief_csv_strs["br00023"] = br00023_csv
    belief_csv_strs["br00024"] = br00024_csv
    belief_csv_strs["br00025"] = br00025_csv
    belief_csv_strs["br00026"] = br00026_csv
    belief_csv_strs["br00027"] = br00027_csv
    belief_csv_strs["br00028"] = br00028_csv
    belief_csv_strs["br00029"] = br00029_csv


# TODO #834
# def add_pidginunits_to_stance_csv_strs():
#     pass
