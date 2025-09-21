from src.ch00_data_toolbox.dict_toolbox import get_empty_str_if_None as if_none_str
from src.ch01_rope_logic.term import FaceName, MomentLabel
from src.ch06_belief_logic.belief_main import BeliefUnit
from src.ch09_pack_logic.pack import PackUnit
from src.ch15_moment_logic.moment_main import MomentUnit
from src.ch17_idea_logic.idea_config import (
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

    moment_csv_strs = {}
    for idea_number in stance_idea_numbers:
        idea_format_filename = get_idea_format_filename(idea_number)
        for idea_columns, idea_file_name in idea_format_headers.items():
            if idea_file_name == idea_format_filename:
                moment_csv_strs[idea_number] = f"event_int,face_name,{idea_columns}\n"
    return moment_csv_strs


def add_momentunits_to_stance_csv_strs(
    moments_dict: dict[MomentLabel, MomentUnit],
    moment_csv_strs: dict[str, str],
    csv_delimiter: str,
):
    for x_moment in moments_dict.values():
        add_momentunit_to_stance_csv_strs(x_moment, moment_csv_strs, csv_delimiter)


def add_momentunit_to_stance_csv_strs(
    x_moment: MomentUnit, moment_csv_strs: dict[str, str], csv_delimiter: str
) -> dict[str, str]:
    br00000_csv = moment_csv_strs.get("br00000")
    br00001_csv = moment_csv_strs.get("br00001")
    br00002_csv = moment_csv_strs.get("br00002")
    br00003_csv = moment_csv_strs.get("br00003")
    br00004_csv = moment_csv_strs.get("br00004")
    br00005_csv = moment_csv_strs.get("br00005")
    br00000_csv = _add_momentunit_to_br00000_csv(br00000_csv, x_moment, csv_delimiter)
    br00001_csv = _add_budunit_to_br00001_csv(br00001_csv, x_moment, csv_delimiter)
    br00002_csv = _add_paybook_to_br00002_csv(br00002_csv, x_moment, csv_delimiter)
    br00003_csv = _add_hours_to_br00003_csv(br00003_csv, x_moment, csv_delimiter)
    br00004_csv = _add_months_to_br00004_csv(br00004_csv, x_moment, csv_delimiter)
    br00005_csv = _add_weekdays_to_br00005_csv(br00005_csv, x_moment, csv_delimiter)
    moment_csv_strs["br00000"] = br00000_csv
    moment_csv_strs["br00001"] = br00001_csv
    moment_csv_strs["br00002"] = br00002_csv
    moment_csv_strs["br00003"] = br00003_csv
    moment_csv_strs["br00004"] = br00004_csv
    moment_csv_strs["br00005"] = br00005_csv


def _add_momentunit_to_br00000_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    if x_moment.knot == csv_delimiter:
        x_knot = f"""\"{str(x_moment.knot)}\""""
    else:
        x_knot = x_moment.knot

    x_row = [
        if_none_str(face_name),
        if_none_str(event_int),
        x_moment.moment_label,
        x_moment.timeline.timeline_label,
        str(x_moment.timeline.c400_number),
        str(x_moment.timeline.yr1_jan1_offset),
        str(x_moment.timeline.monthday_distortion),
        str(x_moment.fund_iota),
        str(x_moment.penny),
        str(x_moment.respect_bit),
        x_knot,
        str(x_moment.job_listen_rotations),
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def _add_budunit_to_br00001_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for broker_belief_name, brokerunits in x_moment.brokerunits.items():
        for bud_time, budunit in brokerunits.buds.items():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_moment.moment_label,
                broker_belief_name,
                str(bud_time),
                str(budunit.quota),
                str(budunit.celldepth),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def _add_paybook_to_br00002_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for belief_name, tranunit in x_moment.paybook.tranunits.items():
        for voice_name, time_dict in tranunit.items():
            for tran_time, amount in time_dict.items():
                moment_label = x_moment.moment_label
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    moment_label,
                    belief_name,
                    voice_name,
                    str(tran_time),
                    str(amount),
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def _add_hours_to_br00003_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for hour_plan in x_moment.timeline.hours_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_moment.moment_label,
            str(hour_plan[1]),
            hour_plan[0],
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_months_to_br00004_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for month_plan in x_moment.timeline.months_config:
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_moment.moment_label,
            str(month_plan[1]),
            month_plan[0],
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_weekdays_to_br00005_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for count_x, weekday_label in enumerate(x_moment.timeline.weekdays_config):
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_moment.moment_label,
            str(count_x),
            weekday_label,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_belief_to_br00020_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for voiceunit in x_belief.voices.values():
        for membership in voiceunit.memberships.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_belief.moment_label,
                x_belief.belief_name,
                voiceunit.voice_name,
                membership.group_title,
                if_none_str(membership.group_cred_points),
                if_none_str(membership.group_debt_points),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_belief_to_br00021_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for voiceunit in x_belief.voices.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_belief.moment_label,
            x_belief.belief_name,
            voiceunit.voice_name,
            if_none_str(voiceunit.voice_cred_points),
            if_none_str(voiceunit.voice_debt_points),
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_belief_to_br00022_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_belief._plan_dict.values():
        for awardunit in planunit.awardunits.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_belief.moment_label,
                x_belief.belief_name,
                planunit.get_plan_rope(),
                awardunit.awardee_title,
                if_none_str(awardunit.give_force),
                if_none_str(awardunit.take_force),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_belief_to_br00023_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for factunit in x_belief.planroot.factunits.values():
        x_row = [
            if_none_str(face_name),
            if_none_str(event_int),
            x_belief.moment_label,
            x_belief.belief_name,
            x_belief.planroot.get_plan_rope(),
            factunit.fact_context,
            factunit.fact_state,
            if_none_str(factunit.fact_lower),
            if_none_str(factunit.fact_upper),
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_belief_to_br00024_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_belief._plan_dict.values():
        for group_title in planunit.laborunit._partys:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_belief.moment_label,
                x_belief.belief_name,
                planunit.get_plan_rope(),
                group_title,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_belief_to_br00025_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_belief._plan_dict.values():
        for group_title in planunit.healerunit._healer_names:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_belief.moment_label,
                x_belief.belief_name,
                planunit.get_plan_rope(),
                group_title,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_belief_to_br00026_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_belief._plan_dict.values():
        for reasonunit in planunit.reasonunits.values():
            for caseunit in reasonunit.cases.values():
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    x_belief.moment_label,
                    x_belief.belief_name,
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


def add_belief_to_br00027_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_belief._plan_dict.values():
        for reasonunit in planunit.reasonunits.values():
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_belief.moment_label,
                x_belief.belief_name,
                planunit.get_plan_rope(),
                reasonunit.reason_context,
                if_none_str(reasonunit.reason_active_requisite),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_belief_to_br00028_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for planunit in x_belief._plan_dict.values():
        if planunit != x_belief.planroot:
            x_row = [
                if_none_str(face_name),
                if_none_str(event_int),
                x_belief.moment_label,
                x_belief.belief_name,
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


def add_belief_to_br00029_csv(
    x_csv: str,
    x_belief: BeliefUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    x_row = [
        if_none_str(face_name),
        if_none_str(event_int),
        x_belief.moment_label,
        x_belief.belief_name,
        if_none_str(x_belief.credor_respect),
        if_none_str(x_belief.debtor_respect),
        if_none_str(x_belief.fund_pool),
        if_none_str(x_belief.max_tree_traverse),
        if_none_str(x_belief.tally),
        if_none_str(x_belief.fund_iota),
        if_none_str(x_belief.penny),
        if_none_str(x_belief.respect_bit),
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def add_beliefunit_to_stance_csv_strs(
    x_belief: BeliefUnit, moment_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    br00020_csv = moment_csv_strs.get("br00020")
    br00021_csv = moment_csv_strs.get("br00021")
    br00022_csv = moment_csv_strs.get("br00022")
    br00023_csv = moment_csv_strs.get("br00023")
    br00024_csv = moment_csv_strs.get("br00024")
    br00025_csv = moment_csv_strs.get("br00025")
    br00026_csv = moment_csv_strs.get("br00026")
    br00027_csv = moment_csv_strs.get("br00027")
    br00028_csv = moment_csv_strs.get("br00028")
    br00029_csv = moment_csv_strs.get("br00029")
    br00020_csv = add_belief_to_br00020_csv(br00020_csv, x_belief, csv_delimiter)
    br00021_csv = add_belief_to_br00021_csv(br00021_csv, x_belief, csv_delimiter)
    br00022_csv = add_belief_to_br00022_csv(br00022_csv, x_belief, csv_delimiter)
    br00023_csv = add_belief_to_br00023_csv(br00023_csv, x_belief, csv_delimiter)
    br00024_csv = add_belief_to_br00024_csv(br00024_csv, x_belief, csv_delimiter)
    br00025_csv = add_belief_to_br00025_csv(br00025_csv, x_belief, csv_delimiter)
    br00026_csv = add_belief_to_br00026_csv(br00026_csv, x_belief, csv_delimiter)
    br00027_csv = add_belief_to_br00027_csv(br00027_csv, x_belief, csv_delimiter)
    br00028_csv = add_belief_to_br00028_csv(br00028_csv, x_belief, csv_delimiter)
    br00029_csv = add_belief_to_br00029_csv(br00029_csv, x_belief, csv_delimiter)
    moment_csv_strs["br00020"] = br00020_csv
    moment_csv_strs["br00021"] = br00021_csv
    moment_csv_strs["br00022"] = br00022_csv
    moment_csv_strs["br00023"] = br00023_csv
    moment_csv_strs["br00024"] = br00024_csv
    moment_csv_strs["br00025"] = br00025_csv
    moment_csv_strs["br00026"] = br00026_csv
    moment_csv_strs["br00027"] = br00027_csv
    moment_csv_strs["br00028"] = br00028_csv
    moment_csv_strs["br00029"] = br00029_csv


def add_pack_to_br00020_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_voice_membership":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("voice_name"),
                beliefatom.jkeys.get("group_title"),
                if_none_str(beliefatom.jvalues.get("group_cred_points")),
                if_none_str(beliefatom.jvalues.get("group_debt_points")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00021_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_voiceunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("voice_name"),
                if_none_str(beliefatom.jvalues.get("voice_cred_points")),
                if_none_str(beliefatom.jvalues.get("voice_debt_points")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00022_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_plan_awardunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("plan_rope"),
                beliefatom.jkeys.get("awardee_title"),
                if_none_str(beliefatom.jvalues.get("give_force")),
                if_none_str(beliefatom.jvalues.get("take_force")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00023_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_plan_factunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("plan_rope"),
                beliefatom.jkeys.get("fact_context"),
                if_none_str(beliefatom.jvalues.get("fact_state")),
                if_none_str(beliefatom.jvalues.get("fact_lower")),
                if_none_str(beliefatom.jvalues.get("fact_upper")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00024_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_plan_partyunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("plan_rope"),
                beliefatom.jkeys.get("party_title"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00025_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_plan_healerunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("plan_rope"),
                beliefatom.jkeys.get("healer_name"),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00026_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_plan_reason_caseunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("plan_rope"),
                beliefatom.jkeys.get("reason_context"),
                beliefatom.jkeys.get("reason_state"),
                if_none_str(beliefatom.jvalues.get("reason_lower")),
                if_none_str(beliefatom.jvalues.get("reason_upper")),
                if_none_str(beliefatom.jvalues.get("reason_divisor")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00027_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_plan_reasonunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("plan_rope"),
                beliefatom.jkeys.get("reason_context"),
                if_none_str(beliefatom.jvalues.get("reason_active_requisite")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00028_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "belief_planunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                beliefatom.jkeys.get("plan_rope"),
                if_none_str(beliefatom.jvalues.get("begin")),
                if_none_str(beliefatom.jvalues.get("close")),
                if_none_str(beliefatom.jvalues.get("addin")),
                if_none_str(beliefatom.jvalues.get("numor")),
                if_none_str(beliefatom.jvalues.get("denom")),
                if_none_str(beliefatom.jvalues.get("morph")),
                if_none_str(beliefatom.jvalues.get("gogo_want")),
                if_none_str(beliefatom.jvalues.get("stop_want")),
                if_none_str(beliefatom.jvalues.get("star")),
                if_none_str(beliefatom.jvalues.get("task")),
                if_none_str(beliefatom.jvalues.get("problem_bool")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_pack_to_br00029_csv(
    x_csv: str, x_packunit: PackUnit, csv_delimiter: str
) -> str:
    for beliefatom in x_packunit._beliefdelta.get_ordered_beliefatoms().values():
        if beliefatom.dimen == "beliefunit":
            x_row = [
                x_packunit.face_name,
                str(x_packunit.event_int),
                x_packunit.moment_label,
                x_packunit.belief_name,
                if_none_str(beliefatom.jvalues.get("credor_respect")),
                if_none_str(beliefatom.jvalues.get("debtor_respect")),
                if_none_str(beliefatom.jvalues.get("fund_pool")),
                if_none_str(beliefatom.jvalues.get("max_tree_traverse")),
                if_none_str(beliefatom.jvalues.get("tally")),
                if_none_str(beliefatom.jvalues.get("fund_iota")),
                if_none_str(beliefatom.jvalues.get("penny")),
                if_none_str(beliefatom.jvalues.get("respect_bit")),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_packunit_to_stance_csv_strs(
    x_pack: PackUnit, moment_csv_strs: dict[str, str], csv_delimiter: str
):
    br00020_csv = moment_csv_strs.get("br00020")
    br00021_csv = moment_csv_strs.get("br00021")
    br00022_csv = moment_csv_strs.get("br00022")
    br00023_csv = moment_csv_strs.get("br00023")
    br00024_csv = moment_csv_strs.get("br00024")
    br00025_csv = moment_csv_strs.get("br00025")
    br00026_csv = moment_csv_strs.get("br00026")
    br00027_csv = moment_csv_strs.get("br00027")
    br00028_csv = moment_csv_strs.get("br00028")
    br00029_csv = moment_csv_strs.get("br00029")
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
    moment_csv_strs["br00020"] = br00020_csv
    moment_csv_strs["br00021"] = br00021_csv
    moment_csv_strs["br00022"] = br00022_csv
    moment_csv_strs["br00023"] = br00023_csv
    moment_csv_strs["br00024"] = br00024_csv
    moment_csv_strs["br00025"] = br00025_csv
    moment_csv_strs["br00026"] = br00026_csv
    moment_csv_strs["br00027"] = br00027_csv
    moment_csv_strs["br00028"] = br00028_csv
    moment_csv_strs["br00029"] = br00029_csv
