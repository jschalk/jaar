from src.a02_finance_logic.allot import allot_scale
from src.a01_way_logic.way import (
    get_ancestor_ways,
    WayStr,
    get_root_word_from_way,
    OwnerName,
)
from src.a05_idea_logic.idea import IdeaUnit
from src.a06_bud_logic.bud import BudUnit, AcctUnit
from src.a12_hub_tools.basis_buds import create_empty_bud_from_bud, create_listen_basis
from src.a12_hub_tools.hub_tool import (
    save_job_file,
    open_job_file,
    open_gut_file,
)
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_debtor_respectException(Exception):
    pass


def generate_perspective_agenda(perspective_bud: BudUnit) -> list[IdeaUnit]:
    for x_factunit in perspective_bud.idearoot.factunits.values():
        x_factunit.set_fbranch_to_fcontext()
    return list(perspective_bud.get_agenda_dict().values())


def _ingest_perspective_agenda(listener: BudUnit, agenda: list[IdeaUnit]) -> BudUnit:
    debtor_amount = listener.debtor_respect
    ingest_list = generate_ingest_list(agenda, debtor_amount, listener.respect_bit)
    for ingest_ideaunit in ingest_list:
        _ingest_single_ideaunit(listener, ingest_ideaunit)
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
    idea_list: list[IdeaUnit], debtor_amount: float, respect_bit: float
) -> list[IdeaUnit]:
    idea_ledger = {x_idea.get_idea_way(): x_idea.mass for x_idea in idea_list}
    mass_allot = allot_scale(idea_ledger, debtor_amount, respect_bit)
    for x_ideaunit in idea_list:
        x_ideaunit.mass = mass_allot.get(x_ideaunit.get_idea_way())
    return idea_list


def _ingest_single_ideaunit(listener: BudUnit, ingest_ideaunit: IdeaUnit):
    mass_data = _create_mass_data(listener, ingest_ideaunit.get_idea_way())

    if listener.idea_exists(ingest_ideaunit.get_idea_way()) is False:
        x_parent_way = ingest_ideaunit.parent_way
        listener.set_idea(ingest_ideaunit, x_parent_way, create_missing_ideas=True)

    _add_and_replace_ideaunit_masss(
        listener=listener,
        replace_mass_list=mass_data.replace_mass_list,
        add_to_mass_list=mass_data.add_to_mass_list,
        x_mass=ingest_ideaunit.mass,
    )


@dataclass
class MassReplaceOrAddData:
    add_to_mass_list: list = None
    replace_mass_list: list = None


def _create_mass_data(listener: BudUnit, x_way: WayStr) -> list:
    mass_data = MassReplaceOrAddData()
    mass_data.add_to_mass_list = []
    mass_data.replace_mass_list = []
    ancestor_ways = get_ancestor_ways(x_way, listener.bridge)
    root_way = get_root_word_from_way(x_way, listener.bridge)
    for ancestor_way in ancestor_ways:
        if ancestor_way != root_way:
            if listener.idea_exists(ancestor_way):
                mass_data.add_to_mass_list.append(ancestor_way)
            else:
                mass_data.replace_mass_list.append(ancestor_way)
    return mass_data


def _add_and_replace_ideaunit_masss(
    listener: BudUnit,
    replace_mass_list: list[WayStr],
    add_to_mass_list: list[WayStr],
    x_mass: float,
):
    for idea_way in replace_mass_list:
        listener.edit_idea_attr(idea_way, mass=x_mass)
    for idea_way in add_to_mass_list:
        x_ideaunit = listener.get_idea_obj(idea_way)
        x_ideaunit.mass += x_mass


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
    for x_factunit in src_listener.idearoot.factunits.values():
        fcontext_way = x_factunit.fcontext
        fbranch_way = x_factunit.fbranch
        if dst_listener.idea_exists(fcontext_way) is False:
            rcontext_idea = src_listener.get_idea_obj(fcontext_way)
            dst_listener.set_idea(rcontext_idea, rcontext_idea.parent_way)
        if dst_listener.idea_exists(fbranch_way) is False:
            fbranch_idea = src_listener.get_idea_obj(fbranch_way)
            dst_listener.set_idea(fbranch_idea, fbranch_idea.parent_way)
        dst_listener.add_fact(fcontext_way, fbranch_way)


def listen_to_speaker_fact(
    listener: BudUnit,
    speaker: BudUnit,
    missing_fact_rcontexts: list[WayStr] = None,
) -> BudUnit:
    if missing_fact_rcontexts is None:
        missing_fact_rcontexts = list(listener.get_missing_fact_rcontexts())
    for missing_fact_rcontext in missing_fact_rcontexts:
        x_factunit = speaker.get_fact(missing_fact_rcontext)
        if x_factunit is not None:
            listener.add_fact(
                fcontext=x_factunit.fcontext,
                fbranch=x_factunit.fbranch,
                fopen=x_factunit.fopen,
                fnigh=x_factunit.fnigh,
                create_missing_ideas=True,
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


def listen_to_agendas_create_init_job_from_guts(
    fisc_mstr_dir: str, listener_job: BudUnit
):
    fisc_word = listener_job.fisc_word
    for x_acctunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_acctunit.acct_name
        speaker_gut = open_gut_file(fisc_mstr_dir, fisc_word, speaker_id)
        if speaker_gut is None:
            speaker_gut = create_empty_bud_from_bud(listener_job, speaker_id)
        if speaker_gut:
            listen_to_speaker_agenda(listener_job, speaker_gut)


def listen_to_agendas_jobs_into_job(fisc_mstr_dir: str, listener_job: BudUnit):
    fisc_word = listener_job.fisc_word
    for x_acctunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_acctunit.acct_name
        speaker_job = open_job_file(fisc_mstr_dir, fisc_word, speaker_id)
        if speaker_job is None:
            speaker_job = create_empty_bud_from_bud(listener_job, speaker_id)
        listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_agendas_duty_plan(listener_plan: BudUnit, healer_hubunit: HubUnit):
    listener_id = listener_plan.owner_name
    for x_acctunit in get_ordered_debtors_roll(listener_plan):
        if x_acctunit.acct_name == listener_id:
            listener_duty = healer_hubunit.get_duty_bud(listener_id)
            listen_to_speaker_agenda(listener_plan, listener_duty)
        else:
            speaker_id = x_acctunit.acct_name
            healer_name = healer_hubunit.owner_name
            speaker_plan = healer_hubunit.rj_speaker_bud(healer_name, speaker_id)
            if speaker_plan is None:
                speaker_plan = create_empty_bud_from_bud(listener_plan, speaker_id)
            listen_to_speaker_agenda(listener_plan, speaker_plan)


def listen_to_facts_duty_plan(new_plan: BudUnit, healer_hubunit: HubUnit):
    duty = healer_hubunit.get_duty_bud(new_plan.owner_name)
    migrate_all_facts(duty, new_plan)
    for x_acctunit in get_ordered_debtors_roll(new_plan):
        if x_acctunit.acct_name != new_plan.owner_name:
            speaker_plan = healer_hubunit.get_plan_bud(x_acctunit.acct_name)
            if speaker_plan is not None:
                listen_to_speaker_fact(new_plan, speaker_plan)


def listen_to_facts_gut_job(fisc_mstr_dir: str, new_job: BudUnit):
    fisc_word = new_job.fisc_word
    old_job = open_job_file(fisc_mstr_dir, fisc_word, new_job.owner_name)
    for x_acctunit in get_ordered_debtors_roll(old_job):
        speaker_id = x_acctunit.acct_name
        speaker_job = open_job_file(fisc_mstr_dir, fisc_word, speaker_id)
        if speaker_job is not None:
            listen_to_speaker_fact(new_job, speaker_job)


def listen_to_debtors_roll_jobs_into_job(
    fisc_mstr_dir: str, fisc_word: str, owner_name: OwnerName
) -> BudUnit:
    old_job = open_job_file(fisc_mstr_dir, fisc_word, owner_name)
    new_job = create_listen_basis(old_job)
    if old_job.debtor_respect is None:
        return new_job
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_job)
    listen_to_facts_gut_job(fisc_mstr_dir, new_job)
    return new_job


def listen_to_debtors_roll_duty_plan(
    healer_hubunit: HubUnit, listener_id: OwnerName
) -> BudUnit:
    duty = healer_hubunit.get_duty_bud(listener_id)
    new_duty = create_listen_basis(duty)
    if duty.debtor_respect is None:
        return new_duty
    listen_to_agendas_duty_plan(new_duty, healer_hubunit)
    listen_to_facts_duty_plan(new_duty, healer_hubunit)
    return new_duty


def listen_to_owner_plans(listener_hubunit: HubUnit) -> None:
    gut = open_gut_file(
        listener_hubunit.fisc_mstr_dir,
        listener_hubunit.fisc_word,
        listener_hubunit.owner_name,
    )
    new_job = create_listen_basis(gut)
    pre_job_dict = new_job.get_dict()
    gut.settle_bud()
    new_job.settle_bud()

    for x_healer_name, keep_dict in gut._healers_dict.items():
        listener_id = listener_hubunit.owner_name
        healer_hubunit = copy_deepcopy(listener_hubunit)
        healer_hubunit.owner_name = x_healer_name
        _fbranch_keep_plans_and_listen(listener_id, keep_dict, healer_hubunit, new_job)

    if new_job.get_dict() == pre_job_dict:
        agenda = list(gut.get_agenda_dict().values())
        _ingest_perspective_agenda(new_job, agenda)
        listen_to_speaker_fact(new_job, gut)

    save_job_file(listener_hubunit.fisc_mstr_dir, new_job)


def _fbranch_keep_plans_and_listen(
    listener_id: OwnerName,
    keep_dict: dict[WayStr],
    healer_hubunit: HubUnit,
    new_job: BudUnit,
):
    for keep_path in keep_dict:
        healer_hubunit.keep_way = keep_path
        fbranch_keep_plan_and_listen(listener_id, healer_hubunit, new_job)


def fbranch_keep_plan_and_listen(
    listener_owner_name: OwnerName, healer_hubunit: HubUnit, new_job: BudUnit
):
    listener_id = listener_owner_name
    if healer_hubunit.plan_file_exists(listener_id):
        keep_plan = healer_hubunit.get_plan_bud(listener_id)
    else:
        keep_plan = create_empty_bud_from_bud(new_job, new_job.owner_name)
    listen_to_plan_agenda(new_job, keep_plan)


def listen_to_plan_agenda(listener: BudUnit, plan: BudUnit):
    for x_idea in plan._idea_dict.values():
        if listener.idea_exists(x_idea.get_idea_way()) is False:
            listener.set_idea(x_idea, x_idea.parent_way)
        if listener.get_fact(x_idea.get_idea_way()) is False:
            listener.set_idea(x_idea, x_idea.parent_way)
    for x_fact_way, x_fact_unit in plan.idearoot.factunits.items():
        listener.idearoot.set_factunit(x_fact_unit)
    listener.settle_bud()


def create_plan_file_from_duty_file(healer_hubunit: HubUnit, owner_name: OwnerName):
    x_plan = listen_to_debtors_roll_duty_plan(healer_hubunit, listener_id=owner_name)
    healer_hubunit.save_plan_bud(x_plan)
