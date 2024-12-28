from src.f01_road.finance import allot_scale
from src.f01_road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_idea_from_road,
    OwnerName,
)
from src.f02_bud.item import ItemUnit
from src.f02_bud.bud import BudUnit, AcctUnit
from src.f05_listen.basis_buds import create_empty_bud, create_listen_basis
from src.f05_listen.hubunit import HubUnit, hubunit_shop
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_debtor_respectException(Exception):
    pass


def generate_perspective_agenda(perspective_bud: BudUnit) -> list[ItemUnit]:
    for x_factunit in perspective_bud.itemroot.factunits.values():
        x_factunit.set_pick_to_base()
    return list(perspective_bud.get_agenda_dict().values())


def _ingest_perspective_agenda(listener: BudUnit, agenda: list[ItemUnit]) -> BudUnit:
    debtor_amount = listener.debtor_respect
    ingest_list = generate_ingest_list(agenda, debtor_amount, listener.respect_bit)
    for ingest_itemunit in ingest_list:
        _ingest_single_itemunit(listener, ingest_itemunit)
    return listener


def _allocate_irrational_debtit_belief(
    listener: BudUnit, speaker_owner_name: OwnerName
):
    speaker_acctunit = listener.get_acct(speaker_owner_name)
    speaker_debtit_belief = speaker_acctunit.debtit_belief
    speaker_acctunit.add_irrational_debtit_belief(speaker_debtit_belief)
    return listener


def _allocate_inallocable_debtit_belief(
    listener: BudUnit, speaker_owner_name: OwnerName
):
    speaker_acctunit = listener.get_acct(speaker_owner_name)
    speaker_acctunit.add_inallocable_debtit_belief(speaker_acctunit.debtit_belief)
    return listener


def get_speaker_perspective(speaker: BudUnit, listener_owner_name: OwnerName):
    listener_hubunit = hubunit_shop("", "", listener_owner_name)
    return listener_hubunit.get_perspective_bud(speaker)


def generate_ingest_list(
    item_list: list[ItemUnit], debtor_amount: float, respect_bit: float
) -> list[ItemUnit]:
    item_ledger = {x_item.get_road(): x_item.mass for x_item in item_list}
    mass_allot = allot_scale(item_ledger, debtor_amount, respect_bit)
    for x_itemunit in item_list:
        x_itemunit.mass = mass_allot.get(x_itemunit.get_road())
    return item_list


def _ingest_single_itemunit(listener: BudUnit, ingest_itemunit: ItemUnit):
    mass_data = _create_mass_data(listener, ingest_itemunit.get_road())

    if listener.item_exists(ingest_itemunit.get_road()) is False:
        x_parent_road = ingest_itemunit._parent_road
        listener.set_item(ingest_itemunit, x_parent_road, create_missing_items=True)

    _add_and_replace_itemunit_masss(
        listener=listener,
        replace_mass_list=mass_data.replace_mass_list,
        add_to_mass_list=mass_data.add_to_mass_list,
        x_mass=ingest_itemunit.mass,
    )


@dataclass
class MassReplaceOrAddData:
    add_to_mass_list: list = None
    replace_mass_list: list = None


def _create_mass_data(listener: BudUnit, x_road: RoadUnit) -> list:
    mass_data = MassReplaceOrAddData()
    mass_data.add_to_mass_list = []
    mass_data.replace_mass_list = []
    ancestor_roads = get_ancestor_roads(x_road)
    root_road = get_root_idea_from_road(x_road)
    for ancestor_road in ancestor_roads:
        if ancestor_road != root_road:
            if listener.item_exists(ancestor_road):
                mass_data.add_to_mass_list.append(ancestor_road)
            else:
                mass_data.replace_mass_list.append(ancestor_road)
    return mass_data


def _add_and_replace_itemunit_masss(
    listener: BudUnit,
    replace_mass_list: list[RoadUnit],
    add_to_mass_list: list[RoadUnit],
    x_mass: float,
):
    for item_road in replace_mass_list:
        listener.edit_item_attr(item_road, mass=x_mass)
    for item_road in add_to_mass_list:
        x_itemunit = listener.get_item_obj(item_road)
        x_itemunit.mass += x_mass


def get_debtors_roll(x_duty: BudUnit) -> list[AcctUnit]:
    return [
        x_acctunit
        for x_acctunit in x_duty.accts.values()
        if x_acctunit.debtit_belief != 0
    ]


def get_ordered_debtors_roll(x_bud: BudUnit) -> list[AcctUnit]:
    accts_ordered_list = get_debtors_roll(x_bud)
    accts_ordered_list.sort(key=lambda x: (x.debtit_belief, x.acct_name), reverse=True)
    return accts_ordered_list


def migrate_all_facts(src_listener: BudUnit, dst_listener: BudUnit):
    for x_factunit in src_listener.itemroot.factunits.values():
        base_road = x_factunit.base
        pick_road = x_factunit.pick
        if dst_listener.item_exists(base_road) is False:
            base_item = src_listener.get_item_obj(base_road)
            dst_listener.set_item(base_item, base_item._parent_road)
        if dst_listener.item_exists(pick_road) is False:
            pick_item = src_listener.get_item_obj(pick_road)
            dst_listener.set_item(pick_item, pick_item._parent_road)
        dst_listener.set_fact(base_road, pick_road)


def listen_to_speaker_fact(
    listener: BudUnit,
    speaker: BudUnit,
    missing_fact_bases: list[RoadUnit] = None,
) -> BudUnit:
    if missing_fact_bases is None:
        missing_fact_bases = list(listener.get_missing_fact_bases())
    for missing_fact_base in missing_fact_bases:
        x_factunit = speaker.get_fact(missing_fact_base)
        if x_factunit is not None:
            listener.set_fact(
                base=x_factunit.base,
                pick=x_factunit.pick,
                fopen=x_factunit.fopen,
                fnigh=x_factunit.fnigh,
                create_missing_items=True,
            )


def listen_to_speaker_agenda(listener: BudUnit, speaker: BudUnit) -> BudUnit:
    if listener.acct_exists(speaker.owner_name) is False:
        raise Missing_debtor_respectException(
            f"listener '{listener.owner_name}' bud is assumed to have {speaker.owner_name} acctunit."
        )
    perspective_bud = get_speaker_perspective(speaker, listener.owner_name)
    if perspective_bud._rational is False:
        return _allocate_irrational_debtit_belief(listener, speaker.owner_name)
    if listener.debtor_respect is None:
        return _allocate_inallocable_debtit_belief(listener, speaker.owner_name)
    if listener.owner_name != speaker.owner_name:
        agenda = generate_perspective_agenda(perspective_bud)
    else:
        agenda = list(perspective_bud.get_all_pledges().values())
    if len(agenda) == 0:
        return _allocate_inallocable_debtit_belief(listener, speaker.owner_name)
    return _ingest_perspective_agenda(listener, agenda)


def listen_to_agendas_voice_final(listener_final: BudUnit, listener_hubunit: HubUnit):
    for x_acctunit in get_ordered_debtors_roll(listener_final):
        if x_acctunit.acct_name == listener_final.owner_name:
            listen_to_speaker_agenda(listener_final, listener_hubunit.get_voice_bud())
        else:
            speaker_id = x_acctunit.acct_name
            speaker_final = listener_hubunit.dw_speaker_bud(speaker_id)
            if speaker_final is None:
                speaker_final = create_empty_bud(listener_final, speaker_id)
            listen_to_speaker_agenda(listener_final, speaker_final)


def listen_to_agendas_duty_job(listener_job: BudUnit, healer_hubunit: HubUnit):
    listener_id = listener_job.owner_name
    for x_acctunit in get_ordered_debtors_roll(listener_job):
        if x_acctunit.acct_name == listener_id:
            listener_duty = healer_hubunit.get_duty_bud(listener_id)
            listen_to_speaker_agenda(listener_job, listener_duty)
        else:
            speaker_id = x_acctunit.acct_name
            healer_name = healer_hubunit.owner_name
            speaker_job = healer_hubunit.rj_speaker_bud(healer_name, speaker_id)
            if speaker_job is None:
                speaker_job = create_empty_bud(listener_job, speaker_id)
            listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_facts_duty_job(new_job: BudUnit, healer_hubunit: HubUnit):
    duty = healer_hubunit.get_duty_bud(new_job.owner_name)
    migrate_all_facts(duty, new_job)
    for x_acctunit in get_ordered_debtors_roll(new_job):
        if x_acctunit.acct_name != new_job.owner_name:
            speaker_job = healer_hubunit.get_job_bud(x_acctunit.acct_name)
            if speaker_job is not None:
                listen_to_speaker_fact(new_job, speaker_job)


def listen_to_facts_voice_final(new_final: BudUnit, listener_hubunit: HubUnit):
    migrate_all_facts(listener_hubunit.get_voice_bud(), new_final)
    for x_acctunit in get_ordered_debtors_roll(new_final):
        speaker_id = x_acctunit.acct_name
        if speaker_id != new_final.owner_name:
            speaker_final = listener_hubunit.dw_speaker_bud(speaker_id)
            if speaker_final is not None:
                listen_to_speaker_fact(new_final, speaker_final)


def listen_to_debtors_roll_voice_final(listener_hubunit: HubUnit) -> BudUnit:
    voice = listener_hubunit.get_voice_bud()
    new_bud = create_listen_basis(voice)
    if voice.debtor_respect is None:
        return new_bud
    listen_to_agendas_voice_final(new_bud, listener_hubunit)
    listen_to_facts_voice_final(new_bud, listener_hubunit)
    return new_bud


def listen_to_debtors_roll_duty_job(
    healer_hubunit: HubUnit, listener_id: OwnerName
) -> BudUnit:
    duty = healer_hubunit.get_duty_bud(listener_id)
    new_duty = create_listen_basis(duty)
    if duty.debtor_respect is None:
        return new_duty
    listen_to_agendas_duty_job(new_duty, healer_hubunit)
    listen_to_facts_duty_job(new_duty, healer_hubunit)
    return new_duty


def listen_to_owner_jobs(listener_hubunit: HubUnit) -> None:
    voice = listener_hubunit.get_voice_bud()
    new_final = create_listen_basis(voice)
    pre_final_dict = new_final.get_dict()
    voice.settle_bud()
    new_final.settle_bud()

    for x_healer_name, keep_dict in voice._healers_dict.items():
        listener_id = listener_hubunit.owner_name
        healer_hubunit = copy_deepcopy(listener_hubunit)
        healer_hubunit.owner_name = x_healer_name
        _pick_keep_jobs_and_listen(listener_id, keep_dict, healer_hubunit, new_final)

    if new_final.get_dict() == pre_final_dict:
        agenda = list(voice.get_agenda_dict().values())
        _ingest_perspective_agenda(new_final, agenda)
        listen_to_speaker_fact(new_final, voice)

    listener_hubunit.save_final_bud(new_final)


def _pick_keep_jobs_and_listen(
    listener_id: OwnerName,
    keep_dict: dict[RoadUnit],
    healer_hubunit: HubUnit,
    new_final: BudUnit,
):
    for keep_path in keep_dict:
        healer_hubunit.keep_road = keep_path
        pick_keep_job_and_listen(listener_id, healer_hubunit, new_final)


def pick_keep_job_and_listen(
    listener_owner_name: OwnerName, healer_hubunit: HubUnit, new_final: BudUnit
):
    listener_id = listener_owner_name
    if healer_hubunit.job_file_exists(listener_id):
        keep_job = healer_hubunit.get_job_bud(listener_id)
    else:
        keep_job = create_empty_bud(new_final, new_final.owner_name)
    listen_to_job_agenda(new_final, keep_job)


def listen_to_job_agenda(listener: BudUnit, job: BudUnit):
    for x_item in job._item_dict.values():
        if listener.item_exists(x_item.get_road()) is False:
            listener.set_item(x_item, x_item._parent_road)
        if listener.get_fact(x_item.get_road()) is False:
            listener.set_item(x_item, x_item._parent_road)
    for x_fact_road, x_fact_unit in job.itemroot.factunits.items():
        listener.itemroot.set_factunit(x_fact_unit)
    listener.settle_bud()


def create_job_file_from_duty_file(healer_hubunit: HubUnit, owner_name: OwnerName):
    x_job = listen_to_debtors_roll_duty_job(healer_hubunit, listener_id=owner_name)
    healer_hubunit.save_job_bud(x_job)


def create_final_file_from_voice_file(hubunit: HubUnit):
    x_final = listen_to_debtors_roll_voice_final(hubunit)
    hubunit.save_final_bud(x_final)
