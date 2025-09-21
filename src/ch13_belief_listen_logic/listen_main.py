from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a01_rope_logic.rope import get_ancestor_ropes, get_root_label_from_rope
from src.a01_rope_logic.term import BeliefName, RopePointer
from src.a02_finance_logic.allot import allot_scale
from src.a05_plan_logic.plan import PlanUnit
from src.a06_belief_logic.belief_main import BeliefUnit, VoiceUnit
from src.ch12_hub_toolbox.hub_tool import open_gut_file, open_job_file, save_job_file
from src.ch12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.ch12_hub_toolbox.keep_tool import get_duty_belief
from src.ch13_belief_listen_logic.basis_beliefs import (
    create_empty_belief_from_belief,
    create_listen_basis,
)


class Missing_debtor_respectException(Exception):
    pass


def generate_perspective_agenda(perspective_belief: BeliefUnit) -> list[PlanUnit]:
    for x_factunit in perspective_belief.planroot.factunits.values():
        x_factunit.set_fact_state_to_fact_context()
    return list(perspective_belief.get_agenda_dict().values())


def _ingest_perspective_agenda(
    listener: BeliefUnit, agenda: list[PlanUnit]
) -> BeliefUnit:
    debtor_amount = listener.debtor_respect
    ingest_list = generate_ingest_list(agenda, debtor_amount, listener.respect_bit)
    for ingest_planunit in ingest_list:
        _ingest_single_planunit(listener, ingest_planunit)
    return listener


def _allocate_irrational_voice_debt_points(
    listener: BeliefUnit, speaker_belief_name: BeliefName
) -> BeliefUnit:
    speaker_voiceunit = listener.get_voice(speaker_belief_name)
    speaker_voice_debt_points = speaker_voiceunit.voice_debt_points
    speaker_voiceunit.add_irrational_voice_debt_points(speaker_voice_debt_points)
    return listener


def _allocate_inallocable_voice_debt_points(
    listener: BeliefUnit, speaker_belief_name: BeliefName
) -> BeliefUnit:
    speaker_voiceunit = listener.get_voice(speaker_belief_name)
    speaker_voiceunit.add_inallocable_voice_debt_points(
        speaker_voiceunit.voice_debt_points
    )
    return listener


def get_speaker_perspective(speaker: BeliefUnit, listener_belief_name: BeliefName):
    listener_hubunit = hubunit_shop("", "", listener_belief_name)
    return listener_hubunit.get_perspective_belief(speaker)


def generate_ingest_list(
    plan_list: list[PlanUnit], debtor_amount: float, respect_bit: float
) -> list[PlanUnit]:
    plan_ledger = {x_plan.get_plan_rope(): x_plan.star for x_plan in plan_list}
    star_allot = allot_scale(plan_ledger, debtor_amount, respect_bit)
    for x_planunit in plan_list:
        x_planunit.star = star_allot.get(x_planunit.get_plan_rope())
    return plan_list


def _ingest_single_planunit(listener: BeliefUnit, ingest_planunit: PlanUnit):
    star_data = _create_star_data(listener, ingest_planunit.get_plan_rope())

    if listener.plan_exists(ingest_planunit.get_plan_rope()) is False:
        x_parent_rope = ingest_planunit.parent_rope
        listener.set_plan(ingest_planunit, x_parent_rope, create_missing_plans=True)

    _add_and_replace_planunit_stars(
        listener=listener,
        replace_star_list=star_data.replace_star_list,
        add_to_star_list=star_data.add_to_star_list,
        x_star=ingest_planunit.star,
    )


@dataclass
class starReplaceOrAddData:
    add_to_star_list: list = None
    replace_star_list: list = None


def _create_star_data(listener: BeliefUnit, x_rope: RopePointer) -> list:
    star_data = starReplaceOrAddData()
    star_data.add_to_star_list = []
    star_data.replace_star_list = []
    ancestor_ropes = get_ancestor_ropes(x_rope, listener.knot)
    root_rope = get_root_label_from_rope(x_rope, listener.knot)
    for ancestor_rope in ancestor_ropes:
        if ancestor_rope != root_rope:
            if listener.plan_exists(ancestor_rope):
                star_data.add_to_star_list.append(ancestor_rope)
            else:
                star_data.replace_star_list.append(ancestor_rope)
    return star_data


def _add_and_replace_planunit_stars(
    listener: BeliefUnit,
    replace_star_list: list[RopePointer],
    add_to_star_list: list[RopePointer],
    x_star: float,
) -> None:
    for plan_rope in replace_star_list:
        listener.edit_plan_attr(plan_rope, star=x_star)
    for plan_rope in add_to_star_list:
        x_planunit = listener.get_plan_obj(plan_rope)
        x_planunit.star += x_star


def get_debtors_roll(x_duty: BeliefUnit) -> list[VoiceUnit]:
    return [
        x_voiceunit
        for x_voiceunit in x_duty.voices.values()
        if x_voiceunit.voice_debt_points != 0
    ]


def get_ordered_debtors_roll(x_belief: BeliefUnit) -> list[VoiceUnit]:
    voices_ordered_list = get_debtors_roll(x_belief)
    voices_ordered_list.sort(
        key=lambda x: (x.voice_debt_points, x.voice_name), reverse=True
    )
    return voices_ordered_list


def migrate_all_facts(src_listener: BeliefUnit, dst_listener: BeliefUnit):
    for x_factunit in src_listener.planroot.factunits.values():
        fact_context_rope = x_factunit.fact_context
        fact_state_rope = x_factunit.fact_state
        if dst_listener.plan_exists(fact_context_rope) is False:
            reason_context_plan = src_listener.get_plan_obj(fact_context_rope)
            dst_listener.set_plan(reason_context_plan, reason_context_plan.parent_rope)
        if dst_listener.plan_exists(fact_state_rope) is False:
            fact_state_plan = src_listener.get_plan_obj(fact_state_rope)
            dst_listener.set_plan(fact_state_plan, fact_state_plan.parent_rope)
        dst_listener.add_fact(fact_context_rope, fact_state_rope)


def listen_to_speaker_fact(
    listener: BeliefUnit,
    speaker: BeliefUnit,
    missing_fact_reason_contexts: list[RopePointer] = None,
) -> BeliefUnit:
    if missing_fact_reason_contexts is None:
        missing_fact_reason_contexts = list(listener.get_missing_fact_reason_contexts())
    for missing_fact_reason_context in missing_fact_reason_contexts:
        x_factunit = speaker.get_fact(missing_fact_reason_context)
        if x_factunit is not None:
            listener.add_fact(
                fact_context=x_factunit.fact_context,
                fact_state=x_factunit.fact_state,
                fact_lower=x_factunit.fact_lower,
                fact_upper=x_factunit.fact_upper,
                create_missing_plans=True,
            )


def listen_to_speaker_agenda(listener: BeliefUnit, speaker: BeliefUnit) -> BeliefUnit:
    if listener.voice_exists(speaker.belief_name) is False:
        raise Missing_debtor_respectException(
            f"listener '{listener.belief_name}' belief is assumed to have {speaker.belief_name} voiceunit."
        )
    perspective_belief = get_speaker_perspective(speaker, listener.belief_name)
    if perspective_belief.rational is False:
        return _allocate_irrational_voice_debt_points(listener, speaker.belief_name)
    if listener.debtor_respect is None:
        return _allocate_inallocable_voice_debt_points(listener, speaker.belief_name)
    if listener.belief_name != speaker.belief_name:
        agenda = generate_perspective_agenda(perspective_belief)
    else:
        agenda = list(perspective_belief.get_all_tasks().values())
    if len(agenda) == 0:
        return _allocate_inallocable_voice_debt_points(listener, speaker.belief_name)
    return _ingest_perspective_agenda(listener, agenda)


def listen_to_agendas_create_init_job_from_guts(
    moment_mstr_dir: str, listener_job: BeliefUnit
):
    moment_label = listener_job.moment_label
    for x_voiceunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_voiceunit.voice_name
        speaker_gut = open_gut_file(moment_mstr_dir, moment_label, speaker_id)
        if speaker_gut is None:
            speaker_gut = create_empty_belief_from_belief(listener_job, speaker_id)
        if speaker_gut:
            listen_to_speaker_agenda(listener_job, speaker_gut)


def listen_to_agendas_jobs_into_job(moment_mstr_dir: str, listener_job: BeliefUnit):
    moment_label = listener_job.moment_label
    for x_voiceunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_voiceunit.voice_name
        speaker_job = open_job_file(moment_mstr_dir, moment_label, speaker_id)
        if speaker_job is None:
            speaker_job = create_empty_belief_from_belief(listener_job, speaker_id)
        listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_agendas_duty_vision(listener_vision: BeliefUnit, healer_hubunit: HubUnit):
    listener_id = listener_vision.belief_name
    for x_voiceunit in get_ordered_debtors_roll(listener_vision):
        if x_voiceunit.voice_name == listener_id:
            listener_duty = get_duty_belief(
                moment_mstr_dir=healer_hubunit.moment_mstr_dir,
                belief_name=healer_hubunit.belief_name,
                moment_label=healer_hubunit.moment_label,
                keep_rope=healer_hubunit.keep_rope,
                knot=healer_hubunit.knot,
                duty_belief_name=listener_id,
            )
            listen_to_speaker_agenda(listener_vision, listener_duty)
        else:
            speaker_id = x_voiceunit.voice_name
            healer_name = healer_hubunit.belief_name
            speaker_vision = healer_hubunit.rj_speaker_belief(healer_name, speaker_id)
            if speaker_vision is None:
                speaker_vision = create_empty_belief_from_belief(
                    listener_vision, speaker_id
                )
            listen_to_speaker_agenda(listener_vision, speaker_vision)


def listen_to_facts_duty_vision(new_vision: BeliefUnit, healer_hubunit: HubUnit):
    duty = get_duty_belief(
        moment_mstr_dir=healer_hubunit.moment_mstr_dir,
        belief_name=healer_hubunit.belief_name,
        moment_label=healer_hubunit.moment_label,
        keep_rope=healer_hubunit.keep_rope,
        knot=healer_hubunit.knot,
        duty_belief_name=new_vision.belief_name,
    )
    migrate_all_facts(duty, new_vision)
    for x_voiceunit in get_ordered_debtors_roll(new_vision):
        if x_voiceunit.voice_name != new_vision.belief_name:
            speaker_vision = healer_hubunit.get_vision_belief(x_voiceunit.voice_name)
            if speaker_vision is not None:
                listen_to_speaker_fact(new_vision, speaker_vision)


def listen_to_facts_gut_job(moment_mstr_dir: str, new_job: BeliefUnit):
    moment_label = new_job.moment_label
    old_job = open_job_file(moment_mstr_dir, moment_label, new_job.belief_name)
    for x_voiceunit in get_ordered_debtors_roll(old_job):
        speaker_id = x_voiceunit.voice_name
        speaker_job = open_job_file(moment_mstr_dir, moment_label, speaker_id)
        if speaker_job is not None:
            listen_to_speaker_fact(new_job, speaker_job)


def listen_to_debtors_roll_jobs_into_job(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> BeliefUnit:
    old_job = open_job_file(moment_mstr_dir, moment_label, belief_name)
    new_job = create_listen_basis(old_job)
    if old_job.debtor_respect is None:
        return new_job
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_job)
    listen_to_facts_gut_job(moment_mstr_dir, new_job)
    return new_job


def listen_to_debtors_roll_duty_vision(
    healer_hubunit: HubUnit, listener_id: BeliefName
) -> BeliefUnit:
    duty = get_duty_belief(
        moment_mstr_dir=healer_hubunit.moment_mstr_dir,
        belief_name=healer_hubunit.belief_name,
        moment_label=healer_hubunit.moment_label,
        keep_rope=healer_hubunit.keep_rope,
        knot=healer_hubunit.knot,
        duty_belief_name=listener_id,
    )
    new_duty = create_listen_basis(duty)
    if duty.debtor_respect is None:
        return new_duty
    listen_to_agendas_duty_vision(new_duty, healer_hubunit)
    listen_to_facts_duty_vision(new_duty, healer_hubunit)
    return new_duty


def listen_to_belief_visions(listener_hubunit: HubUnit) -> None:
    gut = open_gut_file(
        listener_hubunit.moment_mstr_dir,
        listener_hubunit.moment_label,
        listener_hubunit.belief_name,
    )
    new_job = create_listen_basis(gut)
    pre_job_dict = new_job.to_dict()
    gut.cashout()
    new_job.cashout()

    for x_healer_name, keep_dict in gut._healers_dict.items():
        listener_id = listener_hubunit.belief_name
        healer_hubunit = copy_deepcopy(listener_hubunit)
        healer_hubunit.belief_name = x_healer_name
        fact_state_keep_visions_and_listen(
            listener_id, keep_dict, healer_hubunit, new_job
        )

    if new_job.to_dict() == pre_job_dict:
        agenda = list(gut.get_agenda_dict().values())
        _ingest_perspective_agenda(new_job, agenda)
        listen_to_speaker_fact(new_job, gut)

    save_job_file(listener_hubunit.moment_mstr_dir, new_job)


def fact_state_keep_visions_and_listen(
    listener_id: BeliefName,
    keep_dict: dict[RopePointer],
    healer_hubunit: HubUnit,
    new_job: BeliefUnit,
):
    for keep_path in keep_dict:
        healer_hubunit.keep_rope = keep_path
        fact_state_keep_vision_and_listen(listener_id, healer_hubunit, new_job)


def fact_state_keep_vision_and_listen(
    listener_belief_name: BeliefName, healer_hubunit: HubUnit, new_job: BeliefUnit
):
    listener_id = listener_belief_name
    if healer_hubunit.vision_file_exists(listener_id):
        keep_vision = healer_hubunit.get_vision_belief(listener_id)
    else:
        keep_vision = create_empty_belief_from_belief(new_job, new_job.belief_name)
    listen_to_vision_agenda(new_job, keep_vision)


def listen_to_vision_agenda(listener: BeliefUnit, vision: BeliefUnit):
    for x_plan in vision._plan_dict.values():
        if listener.plan_exists(x_plan.get_plan_rope()) is False:
            listener.set_plan(x_plan, x_plan.parent_rope)
        if listener.get_fact(x_plan.get_plan_rope()) is False:
            listener.set_plan(x_plan, x_plan.parent_rope)
    for x_fact_rope, x_fact_unit in vision.planroot.factunits.items():
        listener.planroot.set_factunit(x_fact_unit)
    listener.cashout()


def create_vision_file_from_duty_file(healer_hubunit: HubUnit, belief_name: BeliefName):
    x_vision = listen_to_debtors_roll_duty_vision(
        healer_hubunit, listener_id=belief_name
    )
    healer_hubunit.save_vision_belief(x_vision)
