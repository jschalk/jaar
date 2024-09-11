from src._road.finance import allot_scale
from src._road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_node_from_road,
    OwnerID,
)
from src.bud.idea import IdeaUnit
from src.bud.bud import BudUnit, AcctUnit
from src.hear.basis_buds import create_empty_bud, create_hear_basis
from src.hear.hubunit import HubUnit, hubunit_shop
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_debtor_respectException(Exception):
    pass


def generate_perspective_agenda(perspective_bud: BudUnit) -> list[IdeaUnit]:
    for x_factunit in perspective_bud._idearoot.factunits.values():
        x_factunit.set_pick_to_base()
    return list(perspective_bud.get_agenda_dict().values())


def _ingest_perspective_agenda(hearer: BudUnit, agenda: list[IdeaUnit]) -> BudUnit:
    debtor_amount = hearer._debtor_respect
    ingest_list = generate_ingest_list(agenda, debtor_amount, hearer._bit)
    for ingest_ideaunit in ingest_list:
        _ingest_single_ideaunit(hearer, ingest_ideaunit)
    return hearer


def _allocate_irrational_debtit_belief(hearer: BudUnit, speaker_owner_id: OwnerID):
    speaker_acctunit = hearer.get_acct(speaker_owner_id)
    speaker_debtit_belief = speaker_acctunit.debtit_belief
    speaker_acctunit.add_irrational_debtit_belief(speaker_debtit_belief)
    return hearer


def _allocate_inallocable_debtit_belief(hearer: BudUnit, speaker_owner_id: OwnerID):
    speaker_acctunit = hearer.get_acct(speaker_owner_id)
    speaker_acctunit.add_inallocable_debtit_belief(speaker_acctunit.debtit_belief)
    return hearer


def get_speaker_perspective(speaker: BudUnit, hearer_owner_id: OwnerID):
    hearer_hubunit = hubunit_shop("", "", hearer_owner_id)
    return hearer_hubunit.get_perspective_bud(speaker)


def generate_ingest_list(
    item_list: list[IdeaUnit], debtor_amount: float, bit: float
) -> list[IdeaUnit]:
    idea_ledger = {x_idea.get_road(): x_idea.mass for x_idea in item_list}
    mass_allot = allot_scale(idea_ledger, debtor_amount, bit)
    for x_ideaunit in item_list:
        x_ideaunit.mass = mass_allot.get(x_ideaunit.get_road())
    return item_list


def _ingest_single_ideaunit(hearer: BudUnit, ingest_ideaunit: IdeaUnit):
    mass_data = _create_mass_data(hearer, ingest_ideaunit.get_road())

    if hearer.idea_exists(ingest_ideaunit.get_road()) is False:
        x_parent_road = ingest_ideaunit._parent_road
        hearer.set_idea(ingest_ideaunit, x_parent_road, create_missing_ideas=True)

    _add_and_replace_ideaunit_masss(
        hearer=hearer,
        replace_mass_list=mass_data.replace_mass_list,
        add_to_mass_list=mass_data.add_to_mass_list,
        x_mass=ingest_ideaunit.mass,
    )


@dataclass
class MassReplaceOrAddData:
    add_to_mass_list: list = None
    replace_mass_list: list = None


def _create_mass_data(hearer: BudUnit, x_road: RoadUnit) -> list:
    mass_data = MassReplaceOrAddData()
    mass_data.add_to_mass_list = []
    mass_data.replace_mass_list = []
    ancestor_roads = get_ancestor_roads(x_road)
    root_road = get_root_node_from_road(x_road)
    for ancestor_road in ancestor_roads:
        if ancestor_road != root_road:
            if hearer.idea_exists(ancestor_road):
                mass_data.add_to_mass_list.append(ancestor_road)
            else:
                mass_data.replace_mass_list.append(ancestor_road)
    return mass_data


def _add_and_replace_ideaunit_masss(
    hearer: BudUnit,
    replace_mass_list: list[RoadUnit],
    add_to_mass_list: list[RoadUnit],
    x_mass: float,
):
    for idea_road in replace_mass_list:
        hearer.edit_idea_attr(idea_road, mass=x_mass)
    for idea_road in add_to_mass_list:
        x_ideaunit = hearer.get_idea_obj(idea_road)
        x_ideaunit.mass += x_mass


def get_debtors_roll(x_duty: BudUnit) -> list[AcctUnit]:
    return [
        x_acctunit
        for x_acctunit in x_duty._accts.values()
        if x_acctunit.debtit_belief != 0
    ]


def get_ordered_debtors_roll(x_bud: BudUnit) -> list[AcctUnit]:
    accts_ordered_list = get_debtors_roll(x_bud)
    accts_ordered_list.sort(key=lambda x: (x.debtit_belief, x.acct_id), reverse=True)
    return accts_ordered_list


def migrate_all_facts(src_hearer: BudUnit, dst_hearer: BudUnit):
    for x_factunit in src_hearer._idearoot.factunits.values():
        base_road = x_factunit.base
        pick_road = x_factunit.pick
        if dst_hearer.idea_exists(base_road) is False:
            base_idea = src_hearer.get_idea_obj(base_road)
            dst_hearer.set_idea(base_idea, base_idea._parent_road)
        if dst_hearer.idea_exists(pick_road) is False:
            pick_idea = src_hearer.get_idea_obj(pick_road)
            dst_hearer.set_idea(pick_idea, pick_idea._parent_road)
        dst_hearer.set_fact(base_road, pick_road)


def hear_to_speaker_fact(
    hearer: BudUnit,
    speaker: BudUnit,
    missing_fact_bases: list[RoadUnit] = None,
) -> BudUnit:
    if missing_fact_bases is None:
        missing_fact_bases = list(hearer.get_missing_fact_bases())
    for missing_fact_base in missing_fact_bases:
        x_factunit = speaker.get_fact(missing_fact_base)
        if x_factunit is not None:
            hearer.set_fact(
                base=x_factunit.base,
                pick=x_factunit.pick,
                fopen=x_factunit.fopen,
                fnigh=x_factunit.fnigh,
                create_missing_ideas=True,
            )


def hear_to_speaker_agenda(hearer: BudUnit, speaker: BudUnit) -> BudUnit:
    if hearer.acct_exists(speaker._owner_id) is False:
        raise Missing_debtor_respectException(
            f"hearer '{hearer._owner_id}' bud is assumed to have {speaker._owner_id} acctunit."
        )
    perspective_bud = get_speaker_perspective(speaker, hearer._owner_id)
    if perspective_bud._rational is False:
        return _allocate_irrational_debtit_belief(hearer, speaker._owner_id)
    if hearer._debtor_respect is None:
        return _allocate_inallocable_debtit_belief(hearer, speaker._owner_id)
    if hearer._owner_id != speaker._owner_id:
        agenda = generate_perspective_agenda(perspective_bud)
    else:
        agenda = list(perspective_bud.get_all_pledges().values())
    if len(agenda) == 0:
        return _allocate_inallocable_debtit_belief(hearer, speaker._owner_id)
    return _ingest_perspective_agenda(hearer, agenda)


def hear_to_agendas_voice_action(hearer_action: BudUnit, hearer_hubunit: HubUnit):
    for x_acctunit in get_ordered_debtors_roll(hearer_action):
        if x_acctunit.acct_id == hearer_action._owner_id:
            hear_to_speaker_agenda(hearer_action, hearer_hubunit.get_voice_bud())
        else:
            speaker_id = x_acctunit.acct_id
            speaker_action = hearer_hubunit.dw_speaker_bud(speaker_id)
            if speaker_action is None:
                speaker_action = create_empty_bud(hearer_action, speaker_id)
            hear_to_speaker_agenda(hearer_action, speaker_action)


def hear_to_agendas_duty_job(hearer_job: BudUnit, healer_hubunit: HubUnit):
    hearer_id = hearer_job._owner_id
    for x_acctunit in get_ordered_debtors_roll(hearer_job):
        if x_acctunit.acct_id == hearer_id:
            hearer_duty = healer_hubunit.get_duty_bud(hearer_id)
            hear_to_speaker_agenda(hearer_job, hearer_duty)
        else:
            speaker_id = x_acctunit.acct_id
            healer_id = healer_hubunit.owner_id
            speaker_job = healer_hubunit.rj_speaker_bud(healer_id, speaker_id)
            if speaker_job is None:
                speaker_job = create_empty_bud(hearer_job, speaker_id)
            hear_to_speaker_agenda(hearer_job, speaker_job)


def hear_to_facts_duty_job(new_job: BudUnit, healer_hubunit: HubUnit):
    duty = healer_hubunit.get_duty_bud(new_job._owner_id)
    migrate_all_facts(duty, new_job)
    for x_acctunit in get_ordered_debtors_roll(new_job):
        if x_acctunit.acct_id != new_job._owner_id:
            speaker_job = healer_hubunit.get_job_bud(x_acctunit.acct_id)
            if speaker_job is not None:
                hear_to_speaker_fact(new_job, speaker_job)


def hear_to_facts_voice_action(new_action: BudUnit, hearer_hubunit: HubUnit):
    migrate_all_facts(hearer_hubunit.get_voice_bud(), new_action)
    for x_acctunit in get_ordered_debtors_roll(new_action):
        speaker_id = x_acctunit.acct_id
        if speaker_id != new_action._owner_id:
            speaker_action = hearer_hubunit.dw_speaker_bud(speaker_id)
            if speaker_action is not None:
                hear_to_speaker_fact(new_action, speaker_action)


def hear_to_debtors_roll_voice_action(hearer_hubunit: HubUnit) -> BudUnit:
    voice = hearer_hubunit.get_voice_bud()
    new_bud = create_hear_basis(voice)
    if voice._debtor_respect is None:
        return new_bud
    hear_to_agendas_voice_action(new_bud, hearer_hubunit)
    hear_to_facts_voice_action(new_bud, hearer_hubunit)
    return new_bud


def hear_to_debtors_roll_duty_job(
    healer_hubunit: HubUnit, hearer_id: OwnerID
) -> BudUnit:
    duty = healer_hubunit.get_duty_bud(hearer_id)
    new_duty = create_hear_basis(duty)
    if duty._debtor_respect is None:
        return new_duty
    hear_to_agendas_duty_job(new_duty, healer_hubunit)
    hear_to_facts_duty_job(new_duty, healer_hubunit)
    return new_duty


def hear_to_owner_jobs(hearer_hubunit: HubUnit) -> None:
    voice = hearer_hubunit.get_voice_bud()
    new_action = create_hear_basis(voice)
    pre_action_dict = new_action.get_dict()
    voice.settle_bud()
    new_action.settle_bud()

    for x_healer_id, econ_dict in voice._healers_dict.items():
        hearer_id = hearer_hubunit.owner_id
        healer_hubunit = copy_deepcopy(hearer_hubunit)
        healer_hubunit.owner_id = x_healer_id
        _pick_econ_jobs_and_hear(hearer_id, econ_dict, healer_hubunit, new_action)

    if new_action.get_dict() == pre_action_dict:
        agenda = list(voice.get_agenda_dict().values())
        _ingest_perspective_agenda(new_action, agenda)
        hear_to_speaker_fact(new_action, voice)

    hearer_hubunit.save_action_bud(new_action)


def _pick_econ_jobs_and_hear(
    hearer_id: OwnerID,
    econ_dict: dict[RoadUnit],
    healer_hubunit: HubUnit,
    new_action: BudUnit,
):
    for econ_path in econ_dict:
        healer_hubunit.econ_road = econ_path
        pick_econ_job_and_hear(hearer_id, healer_hubunit, new_action)


def pick_econ_job_and_hear(
    hearer_owner_id: OwnerID, healer_hubunit: HubUnit, new_action: BudUnit
):
    hearer_id = hearer_owner_id
    if healer_hubunit.job_file_exists(hearer_id):
        econ_job = healer_hubunit.get_job_bud(hearer_id)
    else:
        econ_job = create_empty_bud(new_action, new_action._owner_id)
    hear_to_job_agenda(new_action, econ_job)


def hear_to_job_agenda(hearer: BudUnit, job: BudUnit):
    for x_idea in job._idea_dict.values():
        if hearer.idea_exists(x_idea.get_road()) is False:
            hearer.set_idea(x_idea, x_idea._parent_road)
        if hearer.get_fact(x_idea.get_road()) is False:
            hearer.set_idea(x_idea, x_idea._parent_road)
    for x_fact_road, x_fact_unit in job._idearoot.factunits.items():
        hearer._idearoot.set_factunit(x_fact_unit)
    hearer.settle_bud()


def create_job_file_from_duty_file(healer_hubunit: HubUnit, owner_id: OwnerID):
    x_job = hear_to_debtors_roll_duty_job(healer_hubunit, hearer_id=owner_id)
    healer_hubunit.save_job_bud(x_job)


def create_action_file_from_voice_file(hubunit: HubUnit):
    x_action = hear_to_debtors_roll_voice_action(hubunit)
    hubunit.save_action_bud(x_action)
