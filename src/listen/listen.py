from src._road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_node_from_road,
    OwnerID,
)
from src._world.idea import IdeaUnit
from src._world.world import WorldUnit, CharUnit
from src.listen.basis_worlds import create_empty_world, create_listen_basis
from src.listen.hubunit import HubUnit, hubunit_shop
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_char_debtor_poolException(Exception):
    pass


def generate_perspective_agenda(perspective_world: WorldUnit) -> list[IdeaUnit]:
    for x_factunit in perspective_world._idearoot._factunits.values():
        x_factunit.set_pick_to_base()
    return list(perspective_world.get_agenda_dict().values())


def _ingest_perspective_agenda(
    listener: WorldUnit, agenda: list[IdeaUnit]
) -> WorldUnit:
    debtor_amount = listener._char_debtor_pool
    ingest_list = generate_ingest_list(agenda, debtor_amount, listener._pixel)
    for ingest_ideaunit in ingest_list:
        _ingest_single_ideaunit(listener, ingest_ideaunit)
    return listener


def _allocate_irrational_debtor_weight(listener: WorldUnit, speaker_owner_id: OwnerID):
    speaker_charunit = listener.get_char(speaker_owner_id)
    speaker_debtor_weight = speaker_charunit.debtor_weight
    speaker_charunit.add_irrational_debtor_weight(speaker_debtor_weight)
    return listener


def _allocate_inallocable_debtor_weight(listener: WorldUnit, speaker_owner_id: OwnerID):
    speaker_charunit = listener.get_char(speaker_owner_id)
    speaker_charunit.add_inallocable_debtor_weight(speaker_charunit.debtor_weight)
    return listener


def get_speaker_perspective(speaker: WorldUnit, listener_owner_id: OwnerID):
    listener_hubunit = hubunit_shop("", "", listener_owner_id)
    return listener_hubunit.get_perspective_world(speaker)


def _get_pixel_scaled_weight(
    x_world_importance: float, debtor_amount: float, pixel: float
) -> float:
    x_ingest_weight = x_world_importance * debtor_amount
    return int(x_ingest_weight / pixel) * pixel


def _allot_ingest(x_list: list[IdeaUnit], nonallocated_ingest: float, pixel: float):
    # TODO very slow needs to be optimized
    if x_list:
        x_count = 0
        while nonallocated_ingest > 0:
            x_ideaunit = x_list[x_count]
            x_ideaunit._weight += pixel
            nonallocated_ingest -= pixel
            x_count += 1
            if x_count == len(x_list):
                x_count = 0


def create_ingest_idea(
    x_ideaunit: IdeaUnit, debtor_amount: float, pixel: float
) -> IdeaUnit:
    x_ideaunit._weight = _get_pixel_scaled_weight(
        x_world_importance=x_ideaunit._world_importance,
        debtor_amount=debtor_amount,
        pixel=pixel,
    )
    return x_ideaunit


def generate_ingest_list(
    item_list: list[IdeaUnit], debtor_amount: float, pixel: float
) -> list[IdeaUnit]:
    x_list = [
        create_ingest_idea(x_ideaunit, debtor_amount, pixel) for x_ideaunit in item_list
    ]
    sum_scaled_ingest = sum(x_ideaunit._weight for x_ideaunit in item_list)
    nonallocated_ingest = debtor_amount - sum_scaled_ingest
    _allot_ingest(x_list, nonallocated_ingest, pixel)
    return x_list


def _ingest_single_ideaunit(listener: WorldUnit, ingest_ideaunit: IdeaUnit):
    weight_data = _create_weight_data(listener, ingest_ideaunit.get_road())

    if listener.idea_exists(ingest_ideaunit.get_road()) is False:
        x_parent_road = ingest_ideaunit._parent_road
        listener.add_idea(ingest_ideaunit, x_parent_road, create_missing_ideas=True)

    _add_and_replace_ideaunit_weights(
        listener=listener,
        replace_weight_list=weight_data.replace_weight_list,
        add_to_weight_list=weight_data.add_to_weight_list,
        x_weight=ingest_ideaunit._weight,
    )


@dataclass
class WeightReplaceOrAddData:
    add_to_weight_list: list = None
    replace_weight_list: list = None


def _create_weight_data(listener: WorldUnit, x_road: RoadUnit) -> list:
    weight_data = WeightReplaceOrAddData()
    weight_data.add_to_weight_list = []
    weight_data.replace_weight_list = []
    ancestor_roads = get_ancestor_roads(x_road)
    root_road = get_root_node_from_road(x_road)
    for ancestor_road in ancestor_roads:
        if ancestor_road != root_road:
            if listener.idea_exists(ancestor_road):
                weight_data.add_to_weight_list.append(ancestor_road)
            else:
                weight_data.replace_weight_list.append(ancestor_road)
    return weight_data


def _add_and_replace_ideaunit_weights(
    listener: WorldUnit,
    replace_weight_list: list[RoadUnit],
    add_to_weight_list: list[RoadUnit],
    x_weight: float,
):
    for idea_road in replace_weight_list:
        listener.edit_idea_attr(idea_road, weight=x_weight)
    for idea_road in add_to_weight_list:
        x_ideaunit = listener.get_idea_obj(idea_road)
        x_ideaunit._weight += x_weight


def get_debtors_roll(x_duty: WorldUnit) -> list[CharUnit]:
    return [
        x_charunit
        for x_charunit in x_duty._chars.values()
        if x_charunit.debtor_weight != 0
    ]


def get_ordered_debtors_roll(x_world: WorldUnit) -> list[CharUnit]:
    chars_ordered_list = get_debtors_roll(x_world)
    chars_ordered_list.sort(key=lambda x: (x.debtor_weight, x.char_id), reverse=True)
    return chars_ordered_list


def migrate_all_facts(src_listener: WorldUnit, dst_listener: WorldUnit):
    for x_factunit in src_listener._idearoot._factunits.values():
        base_road = x_factunit.base
        pick_road = x_factunit.pick
        if dst_listener.idea_exists(base_road) is False:
            base_idea = src_listener.get_idea_obj(base_road)
            dst_listener.add_idea(base_idea, base_idea._parent_road)
        if dst_listener.idea_exists(pick_road) is False:
            pick_idea = src_listener.get_idea_obj(pick_road)
            dst_listener.add_idea(pick_idea, pick_idea._parent_road)
        dst_listener.set_fact(base_road, pick_road)


def listen_to_speaker_fact(
    listener: WorldUnit,
    speaker: WorldUnit,
    missing_fact_bases: list[RoadUnit] = None,
) -> WorldUnit:
    if missing_fact_bases is None:
        missing_fact_bases = list(listener.get_missing_fact_bases())
    for missing_fact_base in missing_fact_bases:
        x_factunit = speaker.get_fact(missing_fact_base)
        if x_factunit != None:
            listener.set_fact(
                base=x_factunit.base,
                pick=x_factunit.pick,
                open=x_factunit.open,
                nigh=x_factunit.nigh,
                create_missing_ideas=True,
            )


def listen_to_speaker_agenda(listener: WorldUnit, speaker: WorldUnit) -> WorldUnit:
    if listener.char_exists(speaker._owner_id) is False:
        raise Missing_char_debtor_poolException(
            f"listener '{listener._owner_id}' world is assumed to have {speaker._owner_id} charunit."
        )
    perspective_world = get_speaker_perspective(speaker, listener._owner_id)
    if perspective_world._rational is False:
        return _allocate_irrational_debtor_weight(listener, speaker._owner_id)
    if listener._char_debtor_pool is None:
        return _allocate_inallocable_debtor_weight(listener, speaker._owner_id)
    if listener._owner_id != speaker._owner_id:
        agenda = generate_perspective_agenda(perspective_world)
    else:
        agenda = list(perspective_world.get_all_pledges().values())
    if len(agenda) == 0:
        return _allocate_inallocable_debtor_weight(listener, speaker._owner_id)
    return _ingest_perspective_agenda(listener, agenda)


def listen_to_agendas_want_action(
    listener_action: WorldUnit, listener_hubunit: HubUnit
):
    for x_charunit in get_ordered_debtors_roll(listener_action):
        if x_charunit.char_id == listener_action._owner_id:
            listen_to_speaker_agenda(listener_action, listener_hubunit.get_want_world())
        else:
            speaker_id = x_charunit.char_id
            speaker_action = listener_hubunit.dw_speaker_world(speaker_id)
            if speaker_action is None:
                speaker_action = create_empty_world(listener_action, speaker_id)
            listen_to_speaker_agenda(listener_action, speaker_action)


def listen_to_agendas_duty_job(listener_job: WorldUnit, healer_hubunit: HubUnit):
    listener_id = listener_job._owner_id
    for x_charunit in get_ordered_debtors_roll(listener_job):
        if x_charunit.char_id == listener_id:
            listener_duty = healer_hubunit.get_duty_world(listener_id)
            listen_to_speaker_agenda(listener_job, listener_duty)
        else:
            speaker_id = x_charunit.char_id
            healer_id = healer_hubunit.owner_id
            speaker_job = healer_hubunit.rj_speaker_world(healer_id, speaker_id)
            if speaker_job is None:
                speaker_job = create_empty_world(listener_job, speaker_id)
            listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_facts_duty_job(new_job: WorldUnit, healer_hubunit: HubUnit):
    duty = healer_hubunit.get_duty_world(new_job._owner_id)
    migrate_all_facts(duty, new_job)
    for x_charunit in get_ordered_debtors_roll(new_job):
        if x_charunit.char_id != new_job._owner_id:
            speaker_job = healer_hubunit.get_job_world(x_charunit.char_id)
            if speaker_job != None:
                listen_to_speaker_fact(new_job, speaker_job)


def listen_to_facts_want_action(new_action: WorldUnit, listener_hubunit: HubUnit):
    migrate_all_facts(listener_hubunit.get_want_world(), new_action)
    for x_charunit in get_ordered_debtors_roll(new_action):
        speaker_id = x_charunit.char_id
        if speaker_id != new_action._owner_id:
            speaker_action = listener_hubunit.dw_speaker_world(speaker_id)
            if speaker_action != None:
                listen_to_speaker_fact(new_action, speaker_action)


def listen_to_debtors_roll_want_action(listener_hubunit: HubUnit) -> WorldUnit:
    want = listener_hubunit.get_want_world()
    new_world = create_listen_basis(want)
    if want._char_debtor_pool is None:
        return new_world
    listen_to_agendas_want_action(new_world, listener_hubunit)
    listen_to_facts_want_action(new_world, listener_hubunit)
    return new_world


def listen_to_debtors_roll_duty_job(
    healer_hubunit: HubUnit, listener_id: OwnerID
) -> WorldUnit:
    duty = healer_hubunit.get_duty_world(listener_id)
    new_duty = create_listen_basis(duty)
    if duty._char_debtor_pool is None:
        return new_duty
    listen_to_agendas_duty_job(new_duty, healer_hubunit)
    listen_to_facts_duty_job(new_duty, healer_hubunit)
    return new_duty


def listen_to_owner_jobs(listener_hubunit: HubUnit) -> None:
    want = listener_hubunit.get_want_world()
    new_action = create_listen_basis(want)
    pre_action_dict = new_action.get_dict()
    want.calc_world_metrics()
    new_action.calc_world_metrics()

    for x_healer_id, econ_dict in want._healers_dict.items():
        listener_id = listener_hubunit.owner_id
        healer_hubunit = copy_deepcopy(listener_hubunit)
        healer_hubunit.owner_id = x_healer_id
        _pick_econ_jobs_and_listen(listener_id, econ_dict, healer_hubunit, new_action)

    if new_action.get_dict() == pre_action_dict:
        agenda = list(want.get_agenda_dict().values())
        _ingest_perspective_agenda(new_action, agenda)
        listen_to_speaker_fact(new_action, want)

    listener_hubunit.save_action_world(new_action)


def _pick_econ_jobs_and_listen(
    listener_id: OwnerID,
    econ_dict: dict[RoadUnit],
    healer_hubunit: HubUnit,
    new_action: WorldUnit,
):
    for econ_path in econ_dict:
        healer_hubunit.econ_road = econ_path
        pick_econ_job_and_listen(listener_id, healer_hubunit, new_action)


def pick_econ_job_and_listen(
    listener_owner_id: OwnerID, healer_hubunit: HubUnit, new_action: WorldUnit
):
    listener_id = listener_owner_id
    if healer_hubunit.job_file_exists(listener_id):
        econ_job = healer_hubunit.get_job_world(listener_id)
    else:
        econ_job = create_empty_world(new_action, new_action._owner_id)
    listen_to_job_agenda(new_action, econ_job)


def listen_to_job_agenda(listener: WorldUnit, job: WorldUnit):
    for x_idea in job._idea_dict.values():
        if listener.idea_exists(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
        if listener.get_fact(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
    for x_fact_road, x_fact_unit in job._idearoot._factunits.items():
        listener._idearoot.set_factunit(x_fact_unit)
    listener.calc_world_metrics()


def create_job_file_from_duty_file(healer_hubunit: HubUnit, owner_id: OwnerID):
    x_job = listen_to_debtors_roll_duty_job(healer_hubunit, listener_id=owner_id)
    healer_hubunit.save_job_world(x_job)


def create_action_file_from_want_file(hubunit: HubUnit):
    x_action = listen_to_debtors_roll_want_action(hubunit)
    hubunit.save_action_world(x_action)
