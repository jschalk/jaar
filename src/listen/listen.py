from src._road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_node_from_road,
    PersonID,
)
from src._truth.idea import IdeaUnit
from src._truth.truth import TruthUnit, OtherUnit
from src.listen.basis_truths import create_empty_truth, create_listen_basis
from src.listen.userhub import UserHub, userhub_shop
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_other_debtor_poolException(Exception):
    pass


def generate_perspective_agenda(perspective_truth: TruthUnit) -> list[IdeaUnit]:
    for x_factunit in perspective_truth._idearoot._factunits.values():
        x_factunit.set_pick_to_base()
    return list(perspective_truth.get_agenda_dict().values())


def _ingest_perspective_agenda(
    listener: TruthUnit, agenda: list[IdeaUnit]
) -> TruthUnit:
    debtor_amount = listener._other_debtor_pool
    ingest_list = generate_ingest_list(agenda, debtor_amount, listener._pixel)
    for ingest_ideaunit in ingest_list:
        _ingest_single_ideaunit(listener, ingest_ideaunit)
    return listener


def _allocate_irrational_debtor_weight(listener: TruthUnit, speaker_owner_id: PersonID):
    speaker_otherunit = listener.get_other(speaker_owner_id)
    speaker_debtor_weight = speaker_otherunit.debtor_weight
    speaker_otherunit.add_irrational_debtor_weight(speaker_debtor_weight)
    return listener


def _allocate_inallocable_debtor_weight(
    listener: TruthUnit, speaker_owner_id: PersonID
):
    speaker_otherunit = listener.get_other(speaker_owner_id)
    speaker_otherunit.add_inallocable_debtor_weight(speaker_otherunit.debtor_weight)
    return listener


def get_speaker_perspective(speaker: TruthUnit, listener_owner_id: PersonID):
    listener_userhub = userhub_shop("", "", listener_owner_id)
    return listener_userhub.get_perspective_truth(speaker)


def _get_pixel_scaled_weight(
    x_truth_importance: float, debtor_amount: float, pixel: float
) -> float:
    x_ingest_weight = x_truth_importance * debtor_amount
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
        x_truth_importance=x_ideaunit._truth_importance,
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


def _ingest_single_ideaunit(listener: TruthUnit, ingest_ideaunit: IdeaUnit):
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


def _create_weight_data(listener: TruthUnit, x_road: RoadUnit) -> list:
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
    listener: TruthUnit,
    replace_weight_list: list[RoadUnit],
    add_to_weight_list: list[RoadUnit],
    x_weight: float,
):
    for idea_road in replace_weight_list:
        listener.edit_idea_attr(idea_road, weight=x_weight)
    for idea_road in add_to_weight_list:
        x_ideaunit = listener.get_idea_obj(idea_road)
        x_ideaunit._weight += x_weight


def get_debtors_roll(x_role: TruthUnit) -> list[OtherUnit]:
    return [
        x_otherunit
        for x_otherunit in x_role._others.values()
        if x_otherunit.debtor_weight != 0
    ]


def get_ordered_debtors_roll(x_truth: TruthUnit) -> list[OtherUnit]:
    others_ordered_list = get_debtors_roll(x_truth)
    others_ordered_list.sort(key=lambda x: (x.debtor_weight, x.other_id), reverse=True)
    return others_ordered_list


def migrate_all_facts(src_listener: TruthUnit, dst_listener: TruthUnit):
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
    listener: TruthUnit,
    speaker: TruthUnit,
    missing_fact_bases: list[RoadUnit] = None,
) -> TruthUnit:
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


def listen_to_speaker_agenda(listener: TruthUnit, speaker: TruthUnit) -> TruthUnit:
    if listener.other_exists(speaker._owner_id) is False:
        raise Missing_other_debtor_poolException(
            f"listener '{listener._owner_id}' truth is assumed to have {speaker._owner_id} otherunit."
        )
    perspective_truth = get_speaker_perspective(speaker, listener._owner_id)
    if perspective_truth._rational is False:
        return _allocate_irrational_debtor_weight(listener, speaker._owner_id)
    if listener._other_debtor_pool is None:
        return _allocate_inallocable_debtor_weight(listener, speaker._owner_id)
    if listener._owner_id != speaker._owner_id:
        agenda = generate_perspective_agenda(perspective_truth)
    else:
        agenda = list(perspective_truth.get_all_pledges().values())
    if len(agenda) == 0:
        return _allocate_inallocable_debtor_weight(listener, speaker._owner_id)
    return _ingest_perspective_agenda(listener, agenda)


def listen_to_agendas_same_live(listener_live: TruthUnit, listener_userhub: UserHub):
    for x_otherunit in get_ordered_debtors_roll(listener_live):
        if x_otherunit.other_id == listener_live._owner_id:
            listen_to_speaker_agenda(listener_live, listener_userhub.get_same_truth())
        else:
            speaker_id = x_otherunit.other_id
            speaker_live = listener_userhub.dw_speaker_truth(speaker_id)
            if speaker_live is None:
                speaker_live = create_empty_truth(listener_live, speaker_id)
            listen_to_speaker_agenda(listener_live, speaker_live)


def listen_to_agendas_role_job(listener_job: TruthUnit, healer_userhub: UserHub):
    listener_id = listener_job._owner_id
    for x_otherunit in get_ordered_debtors_roll(listener_job):
        if x_otherunit.other_id == listener_id:
            listener_role = healer_userhub.get_role_truth(listener_id)
            listen_to_speaker_agenda(listener_job, listener_role)
        else:
            speaker_id = x_otherunit.other_id
            healer_id = healer_userhub.person_id
            speaker_job = healer_userhub.rj_speaker_truth(healer_id, speaker_id)
            if speaker_job is None:
                speaker_job = create_empty_truth(listener_job, speaker_id)
            listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_facts_role_job(new_job: TruthUnit, healer_userhub: UserHub):
    role = healer_userhub.get_role_truth(new_job._owner_id)
    migrate_all_facts(role, new_job)
    for x_otherunit in get_ordered_debtors_roll(new_job):
        if x_otherunit.other_id != new_job._owner_id:
            speaker_job = healer_userhub.get_job_truth(x_otherunit.other_id)
            if speaker_job != None:
                listen_to_speaker_fact(new_job, speaker_job)


def listen_to_facts_same_live(new_live: TruthUnit, listener_userhub: UserHub):
    migrate_all_facts(listener_userhub.get_same_truth(), new_live)
    for x_otherunit in get_ordered_debtors_roll(new_live):
        speaker_id = x_otherunit.other_id
        if speaker_id != new_live._owner_id:
            speaker_live = listener_userhub.dw_speaker_truth(speaker_id)
            if speaker_live != None:
                listen_to_speaker_fact(new_live, speaker_live)


def listen_to_debtors_roll_same_live(listener_userhub: UserHub) -> TruthUnit:
    same = listener_userhub.get_same_truth()
    new_truth = create_listen_basis(same)
    if same._other_debtor_pool is None:
        return new_truth
    listen_to_agendas_same_live(new_truth, listener_userhub)
    listen_to_facts_same_live(new_truth, listener_userhub)
    return new_truth


def listen_to_debtors_roll_role_job(
    healer_userhub: UserHub, listener_id: PersonID
) -> TruthUnit:
    role = healer_userhub.get_role_truth(listener_id)
    new_role = create_listen_basis(role)
    if role._other_debtor_pool is None:
        return new_role
    listen_to_agendas_role_job(new_role, healer_userhub)
    listen_to_facts_role_job(new_role, healer_userhub)
    return new_role


def listen_to_person_jobs(listener_userhub: UserHub) -> None:
    same = listener_userhub.get_same_truth()
    new_live = create_listen_basis(same)
    pre_live_dict = new_live.get_dict()
    same.calc_truth_metrics()
    new_live.calc_truth_metrics()

    for x_healer_id, econ_dict in same._healers_dict.items():
        listener_id = listener_userhub.person_id
        healer_userhub = copy_deepcopy(listener_userhub)
        healer_userhub.person_id = x_healer_id
        _pick_econ_jobs_and_listen(listener_id, econ_dict, healer_userhub, new_live)

    if new_live.get_dict() == pre_live_dict:
        agenda = list(same.get_agenda_dict().values())
        _ingest_perspective_agenda(new_live, agenda)
        listen_to_speaker_fact(new_live, same)

    listener_userhub.save_live_truth(new_live)


def _pick_econ_jobs_and_listen(
    listener_id: PersonID,
    econ_dict: dict[RoadUnit],
    healer_userhub: UserHub,
    new_live: TruthUnit,
):
    for econ_path in econ_dict:
        healer_userhub.econ_road = econ_path
        pick_econ_job_and_listen(listener_id, healer_userhub, new_live)


def pick_econ_job_and_listen(
    listener_person_id: PersonID, healer_userhub: UserHub, new_live: TruthUnit
):
    listener_id = listener_person_id
    if healer_userhub.job_file_exists(listener_id):
        econ_job = healer_userhub.get_job_truth(listener_id)
    else:
        econ_job = create_empty_truth(new_live, new_live._owner_id)
    listen_to_job_agenda(new_live, econ_job)


def listen_to_job_agenda(listener: TruthUnit, job: TruthUnit):
    for x_idea in job._idea_dict.values():
        if listener.idea_exists(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
        if listener.get_fact(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
    for x_fact_road, x_fact_unit in job._idearoot._factunits.items():
        listener._idearoot.set_factunit(x_fact_unit)
    listener.calc_truth_metrics()


def create_job_file_from_role_file(healer_userhub: UserHub, person_id: PersonID):
    x_job = listen_to_debtors_roll_role_job(healer_userhub, listener_id=person_id)
    healer_userhub.save_job_truth(x_job)


def create_live_file_from_same_file(userhub: UserHub):
    x_live = listen_to_debtors_roll_same_live(userhub)
    userhub.save_live_truth(x_live)
