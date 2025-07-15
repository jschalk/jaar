from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a01_term_logic.rope import get_ancestor_ropes, get_root_label_from_rope
from src.a01_term_logic.term import BelieverName, RopeTerm
from src.a02_finance_logic.allot import allot_scale
from src.a05_plan_logic.plan import PlanUnit
from src.a06_believer_logic.believer import BelieverUnit, PartnerUnit
from src.a12_hub_toolbox.hub_tool import open_gut_file, open_job_file, save_job_file
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a12_hub_toolbox.keep_tool import get_duty_believer
from src.a13_believer_listen_logic.basis_believers import (
    create_empty_believer_from_believer,
    create_listen_basis,
)


class Missing_debtor_respectException(Exception):
    pass


def generate_perspective_agenda(perspective_believer: BelieverUnit) -> list[PlanUnit]:
    for x_factunit in perspective_believer.planroot.factunits.values():
        x_factunit.set_fstate_to_fcontext()
    return list(perspective_believer.get_agenda_dict().values())


def _ingest_perspective_agenda(
    listener: BelieverUnit, agenda: list[PlanUnit]
) -> BelieverUnit:
    debtor_amount = listener.debtor_respect
    ingest_list = generate_ingest_list(agenda, debtor_amount, listener.respect_bit)
    for ingest_planunit in ingest_list:
        _ingest_single_planunit(listener, ingest_planunit)
    return listener


def _allocate_irrational_partner_debt_points(
    listener: BelieverUnit, speaker_believer_name: BelieverName
) -> BelieverUnit:
    speaker_partnerunit = listener.get_partner(speaker_believer_name)
    speaker_partner_debt_points = speaker_partnerunit.partner_debt_points
    speaker_partnerunit.add_irrational_partner_debt_points(speaker_partner_debt_points)
    return listener


def _allocate_inallocable_partner_debt_points(
    listener: BelieverUnit, speaker_believer_name: BelieverName
) -> BelieverUnit:
    speaker_partnerunit = listener.get_partner(speaker_believer_name)
    speaker_partnerunit.add_inallocable_partner_debt_points(
        speaker_partnerunit.partner_debt_points
    )
    return listener


def get_speaker_perspective(
    speaker: BelieverUnit, listener_believer_name: BelieverName
):
    listener_hubunit = hubunit_shop("", "", listener_believer_name)
    return listener_hubunit.get_perspective_believer(speaker)


def generate_ingest_list(
    plan_list: list[PlanUnit], debtor_amount: float, respect_bit: float
) -> list[PlanUnit]:
    plan_ledger = {x_plan.get_plan_rope(): x_plan.mass for x_plan in plan_list}
    mass_allot = allot_scale(plan_ledger, debtor_amount, respect_bit)
    for x_planunit in plan_list:
        x_planunit.mass = mass_allot.get(x_planunit.get_plan_rope())
    return plan_list


def _ingest_single_planunit(listener: BelieverUnit, ingest_planunit: PlanUnit):
    mass_data = _create_mass_data(listener, ingest_planunit.get_plan_rope())

    if listener.plan_exists(ingest_planunit.get_plan_rope()) is False:
        x_parent_rope = ingest_planunit.parent_rope
        listener.set_plan(ingest_planunit, x_parent_rope, create_missing_plans=True)

    _add_and_replace_planunit_masss(
        listener=listener,
        replace_mass_list=mass_data.replace_mass_list,
        add_to_mass_list=mass_data.add_to_mass_list,
        x_mass=ingest_planunit.mass,
    )


@dataclass
class MassReplaceOrAddData:
    add_to_mass_list: list = None
    replace_mass_list: list = None


def _create_mass_data(listener: BelieverUnit, x_rope: RopeTerm) -> list:
    mass_data = MassReplaceOrAddData()
    mass_data.add_to_mass_list = []
    mass_data.replace_mass_list = []
    ancestor_ropes = get_ancestor_ropes(x_rope, listener.knot)
    root_rope = get_root_label_from_rope(x_rope, listener.knot)
    for ancestor_rope in ancestor_ropes:
        if ancestor_rope != root_rope:
            if listener.plan_exists(ancestor_rope):
                mass_data.add_to_mass_list.append(ancestor_rope)
            else:
                mass_data.replace_mass_list.append(ancestor_rope)
    return mass_data


def _add_and_replace_planunit_masss(
    listener: BelieverUnit,
    replace_mass_list: list[RopeTerm],
    add_to_mass_list: list[RopeTerm],
    x_mass: float,
) -> None:
    for plan_rope in replace_mass_list:
        listener.edit_plan_attr(plan_rope, mass=x_mass)
    for plan_rope in add_to_mass_list:
        x_planunit = listener.get_plan_obj(plan_rope)
        x_planunit.mass += x_mass


def get_debtors_roll(x_duty: BelieverUnit) -> list[PartnerUnit]:
    return [
        x_partnerunit
        for x_partnerunit in x_duty.partners.values()
        if x_partnerunit.partner_debt_points != 0
    ]


def get_ordered_debtors_roll(x_believer: BelieverUnit) -> list[PartnerUnit]:
    partners_ordered_list = get_debtors_roll(x_believer)
    partners_ordered_list.sort(
        key=lambda x: (x.partner_debt_points, x.partner_name), reverse=True
    )
    return partners_ordered_list


def migrate_all_facts(src_listener: BelieverUnit, dst_listener: BelieverUnit):
    for x_factunit in src_listener.planroot.factunits.values():
        fcontext_rope = x_factunit.fcontext
        fstate_rope = x_factunit.fstate
        if dst_listener.plan_exists(fcontext_rope) is False:
            rcontext_plan = src_listener.get_plan_obj(fcontext_rope)
            dst_listener.set_plan(rcontext_plan, rcontext_plan.parent_rope)
        if dst_listener.plan_exists(fstate_rope) is False:
            fstate_plan = src_listener.get_plan_obj(fstate_rope)
            dst_listener.set_plan(fstate_plan, fstate_plan.parent_rope)
        dst_listener.add_fact(fcontext_rope, fstate_rope)


def listen_to_speaker_fact(
    listener: BelieverUnit,
    speaker: BelieverUnit,
    missing_fact_rcontexts: list[RopeTerm] = None,
) -> BelieverUnit:
    if missing_fact_rcontexts is None:
        missing_fact_rcontexts = list(listener.get_missing_fact_rcontexts())
    for missing_fact_rcontext in missing_fact_rcontexts:
        x_factunit = speaker.get_fact(missing_fact_rcontext)
        if x_factunit is not None:
            listener.add_fact(
                fcontext=x_factunit.fcontext,
                fstate=x_factunit.fstate,
                fopen=x_factunit.fopen,
                fnigh=x_factunit.fnigh,
                create_missing_plans=True,
            )


def listen_to_speaker_agenda(
    listener: BelieverUnit, speaker: BelieverUnit
) -> BelieverUnit:
    if listener.partner_exists(speaker.believer_name) is False:
        raise Missing_debtor_respectException(
            f"listener '{listener.believer_name}' believer is assumed to have {speaker.believer_name} partnerunit."
        )
    perspective_believer = get_speaker_perspective(speaker, listener.believer_name)
    if perspective_believer._rational is False:
        return _allocate_irrational_partner_debt_points(listener, speaker.believer_name)
    if listener.debtor_respect is None:
        return _allocate_inallocable_partner_debt_points(
            listener, speaker.believer_name
        )
    if listener.believer_name != speaker.believer_name:
        agenda = generate_perspective_agenda(perspective_believer)
    else:
        agenda = list(perspective_believer.get_all_tasks().values())
    if len(agenda) == 0:
        return _allocate_inallocable_partner_debt_points(
            listener, speaker.believer_name
        )
    return _ingest_perspective_agenda(listener, agenda)


def listen_to_agendas_create_init_job_from_guts(
    belief_mstr_dir: str, listener_job: BelieverUnit
):
    belief_label = listener_job.belief_label
    for x_partnerunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_partnerunit.partner_name
        speaker_gut = open_gut_file(belief_mstr_dir, belief_label, speaker_id)
        if speaker_gut is None:
            speaker_gut = create_empty_believer_from_believer(listener_job, speaker_id)
        if speaker_gut:
            listen_to_speaker_agenda(listener_job, speaker_gut)


def listen_to_agendas_jobs_into_job(belief_mstr_dir: str, listener_job: BelieverUnit):
    belief_label = listener_job.belief_label
    for x_partnerunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_partnerunit.partner_name
        speaker_job = open_job_file(belief_mstr_dir, belief_label, speaker_id)
        if speaker_job is None:
            speaker_job = create_empty_believer_from_believer(listener_job, speaker_id)
        listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_agendas_duty_vision(
    listener_vision: BelieverUnit, healer_hubunit: HubUnit
):
    listener_id = listener_vision.believer_name
    for x_partnerunit in get_ordered_debtors_roll(listener_vision):
        if x_partnerunit.partner_name == listener_id:
            listener_duty = get_duty_believer(
                belief_mstr_dir=healer_hubunit.belief_mstr_dir,
                believer_name=healer_hubunit.believer_name,
                belief_label=healer_hubunit.belief_label,
                keep_rope=healer_hubunit.keep_rope,
                knot=healer_hubunit.knot,
                duty_believer_name=listener_id,
            )
            listen_to_speaker_agenda(listener_vision, listener_duty)
        else:
            speaker_id = x_partnerunit.partner_name
            healer_name = healer_hubunit.believer_name
            speaker_vision = healer_hubunit.rj_speaker_believer(healer_name, speaker_id)
            if speaker_vision is None:
                speaker_vision = create_empty_believer_from_believer(
                    listener_vision, speaker_id
                )
            listen_to_speaker_agenda(listener_vision, speaker_vision)


def listen_to_facts_duty_vision(new_vision: BelieverUnit, healer_hubunit: HubUnit):
    duty = get_duty_believer(
        belief_mstr_dir=healer_hubunit.belief_mstr_dir,
        believer_name=healer_hubunit.believer_name,
        belief_label=healer_hubunit.belief_label,
        keep_rope=healer_hubunit.keep_rope,
        knot=healer_hubunit.knot,
        duty_believer_name=new_vision.believer_name,
    )
    migrate_all_facts(duty, new_vision)
    for x_partnerunit in get_ordered_debtors_roll(new_vision):
        if x_partnerunit.partner_name != new_vision.believer_name:
            speaker_vision = healer_hubunit.get_vision_believer(
                x_partnerunit.partner_name
            )
            if speaker_vision is not None:
                listen_to_speaker_fact(new_vision, speaker_vision)


def listen_to_facts_gut_job(belief_mstr_dir: str, new_job: BelieverUnit):
    belief_label = new_job.belief_label
    old_job = open_job_file(belief_mstr_dir, belief_label, new_job.believer_name)
    for x_partnerunit in get_ordered_debtors_roll(old_job):
        speaker_id = x_partnerunit.partner_name
        speaker_job = open_job_file(belief_mstr_dir, belief_label, speaker_id)
        if speaker_job is not None:
            listen_to_speaker_fact(new_job, speaker_job)


def listen_to_debtors_roll_jobs_into_job(
    belief_mstr_dir: str, belief_label: str, believer_name: BelieverName
) -> BelieverUnit:
    old_job = open_job_file(belief_mstr_dir, belief_label, believer_name)
    new_job = create_listen_basis(old_job)
    if old_job.debtor_respect is None:
        return new_job
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_job)
    listen_to_facts_gut_job(belief_mstr_dir, new_job)
    return new_job


def listen_to_debtors_roll_duty_vision(
    healer_hubunit: HubUnit, listener_id: BelieverName
) -> BelieverUnit:
    duty = get_duty_believer(
        belief_mstr_dir=healer_hubunit.belief_mstr_dir,
        believer_name=healer_hubunit.believer_name,
        belief_label=healer_hubunit.belief_label,
        keep_rope=healer_hubunit.keep_rope,
        knot=healer_hubunit.knot,
        duty_believer_name=listener_id,
    )
    new_duty = create_listen_basis(duty)
    if duty.debtor_respect is None:
        return new_duty
    listen_to_agendas_duty_vision(new_duty, healer_hubunit)
    listen_to_facts_duty_vision(new_duty, healer_hubunit)
    return new_duty


def listen_to_believer_visions(listener_hubunit: HubUnit) -> None:
    gut = open_gut_file(
        listener_hubunit.belief_mstr_dir,
        listener_hubunit.belief_label,
        listener_hubunit.believer_name,
    )
    new_job = create_listen_basis(gut)
    pre_job_dict = new_job.get_dict()
    gut.settle_believer()
    new_job.settle_believer()

    for x_healer_name, keep_dict in gut._healers_dict.items():
        listener_id = listener_hubunit.believer_name
        healer_hubunit = copy_deepcopy(listener_hubunit)
        healer_hubunit.believer_name = x_healer_name
        _fstate_keep_visions_and_listen(listener_id, keep_dict, healer_hubunit, new_job)

    if new_job.get_dict() == pre_job_dict:
        agenda = list(gut.get_agenda_dict().values())
        _ingest_perspective_agenda(new_job, agenda)
        listen_to_speaker_fact(new_job, gut)

    save_job_file(listener_hubunit.belief_mstr_dir, new_job)


def _fstate_keep_visions_and_listen(
    listener_id: BelieverName,
    keep_dict: dict[RopeTerm],
    healer_hubunit: HubUnit,
    new_job: BelieverUnit,
):
    for keep_path in keep_dict:
        healer_hubunit.keep_rope = keep_path
        fstate_keep_vision_and_listen(listener_id, healer_hubunit, new_job)


def fstate_keep_vision_and_listen(
    listener_believer_name: BelieverName, healer_hubunit: HubUnit, new_job: BelieverUnit
):
    listener_id = listener_believer_name
    if healer_hubunit.vision_file_exists(listener_id):
        keep_vision = healer_hubunit.get_vision_believer(listener_id)
    else:
        keep_vision = create_empty_believer_from_believer(
            new_job, new_job.believer_name
        )
    listen_to_vision_agenda(new_job, keep_vision)


def listen_to_vision_agenda(listener: BelieverUnit, vision: BelieverUnit):
    for x_plan in vision._plan_dict.values():
        if listener.plan_exists(x_plan.get_plan_rope()) is False:
            listener.set_plan(x_plan, x_plan.parent_rope)
        if listener.get_fact(x_plan.get_plan_rope()) is False:
            listener.set_plan(x_plan, x_plan.parent_rope)
    for x_fact_rope, x_fact_unit in vision.planroot.factunits.items():
        listener.planroot.set_factunit(x_fact_unit)
    listener.settle_believer()


def create_vision_file_from_duty_file(
    healer_hubunit: HubUnit, believer_name: BelieverName
):
    x_vision = listen_to_debtors_roll_duty_vision(
        healer_hubunit, listener_id=believer_name
    )
    healer_hubunit.save_vision_believer(x_vision)
