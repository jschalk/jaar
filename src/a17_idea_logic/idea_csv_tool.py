from src.a00_data_toolbox.dict_toolbox import get_empty_str_if_None as if_none_str
from src.a01_term_logic.term import BeliefLabel, FaceName
from src.a06_believer_logic.believer_main import BelieverUnit
from src.a09_pack_logic.pack import PackUnit
from src.a15_belief_logic.belief_main import BeliefUnit
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
        for partner_name, time_dict in tranunit.items():
            for tran_time, amount in time_dict.items():
                belief_label = x_belief.belief_label
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    belief_label,
                    believer_name,
                    partner_name,
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
    for partnerunit in x_believer.partners.values():
        for membership in partnerunit._memberships.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                partnerunit.partner_name,
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
    for partnerunit in x_believer.partners.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_believer.belief_label,
            x_believer.believer_name,
            partnerunit.partner_name,
            if_none_str(partnerunit.partner_cred_points),
            if_none_str(partnerunit.partner_debt_points),
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
        for awardunit in planunit.awardunits.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_believer.belief_label,
                x_believer.believer_name,
                planunit.get_plan_rope(),
                awardunit.awardee_title,
                if_none_str(awardunit.give_force),
                if_none_str(awardunit.take_force),
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
            factunit.fact_context,
            factunit.fact_state,
            if_none_str(factunit.fact_lower),
            if_none_str(factunit.fact_upper),
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
        for group_title in planunit.laborunit._partys:
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
            for caseunit in reasonunit.cases.values():
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    x_believer.belief_label,
                    x_believer.believer_name,
                    planunit.get_plan_rope(),
                    reasonunit.reason_context,
                    caseunit.reason_state,
                    if_none_str(caseunit.reason_lower),
                    if_none_str(caseunit.reason_upper),
                    if_none_str(caseunit.reason_divisor),
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
                reasonunit.reason_context,
                if_none_str(reasonunit.reason_active_requisite),
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
                if_none_str(planunit.star),
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


def add_pack_to_br00020_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_partner_membership":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("partner_name"),
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
        if believeratom.dimen == "believer_partnerunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("partner_name"),
                if_none_str(believeratom.jvalues.get("partner_cred_points")),
                if_none_str(believeratom.jvalues.get("partner_debt_points")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00022_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_awardunit":
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
                believeratom.jkeys.get("fact_context"),
                if_none_str(believeratom.jvalues.get("fact_state")),
                if_none_str(believeratom.jvalues.get("fact_lower")),
                if_none_str(believeratom.jvalues.get("fact_upper")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00024_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for believeratom in x_packunit._believerdelta.get_ordered_believeratoms().values():
        if believeratom.dimen == "believer_plan_partyunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("party_title"),
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
        if believeratom.dimen == "believer_plan_reason_caseunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.belief_label,
                x_packunit.believer_name,
                believeratom.jkeys.get("plan_rope"),
                believeratom.jkeys.get("reason_context"),
                believeratom.jkeys.get("reason_state"),
                if_none_str(believeratom.jvalues.get("reason_lower")),
                if_none_str(believeratom.jvalues.get("reason_upper")),
                if_none_str(believeratom.jvalues.get("reason_divisor")),
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
                believeratom.jkeys.get("reason_context"),
                if_none_str(believeratom.jvalues.get("reason_active_requisite")),
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
                if_none_str(believeratom.jvalues.get("star")),
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
