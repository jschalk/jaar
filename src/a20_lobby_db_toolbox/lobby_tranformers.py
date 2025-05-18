from src.a00_data_toolbox.file_toolbox import create_path, get_level1_dirs
from src.a01_way_logic.way import WayStr, WorldID
from src.a02_finance_logic.deal import OwnerName, FiscLabel
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import AwardHeir, GroupUnit, MemberShip
from src.a04_reason_logic.reason_concept import ReasonHeir, PremiseUnit, FactHeir
from src.a04_reason_logic.reason_labor import LaborHeir
from src.a05_concept_logic.healer import HealerLink
from src.a05_concept_logic.concept import ConceptUnit
from src.a06_bud_logic.bud import BudUnit
from src.a12_hub_tools.hub_tool import open_job_file
from src.a20_lobby_db_toolbox.lobby_path import create_fisc_mstr_dir_path, LobbyID
from src.a20_lobby_db_toolbox.lobby_sqlstrs import (
    create_budmemb_metrics_insert_sqlstr,
    create_budacct_metrics_insert_sqlstr,
    create_budgrou_metrics_insert_sqlstr,
    create_budawar_metrics_insert_sqlstr,
    create_budfact_metrics_insert_sqlstr,
    create_budheal_metrics_insert_sqlstr,
    create_budprem_metrics_insert_sqlstr,
    create_budreas_metrics_insert_sqlstr,
    create_budlabor_metrics_insert_sqlstr,
    create_budconc_metrics_insert_sqlstr,
    create_budunit_metrics_insert_sqlstr,
)
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


@dataclass
class ObjKeysHolder:
    world_id: WorldID = None
    fisc_label: FiscLabel = None
    owner_name: OwnerName = None
    way: WayStr = None
    rcontext: WayStr = None
    acct_name: AcctUnit = None
    membership: GroupUnit = None
    group_name: GroupUnit = None
    fact_way: WayStr = None


def insert_job_budmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budacct(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_acct: AcctUnit,
):
    x_dict = copy_deepcopy(x_acct.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budacct_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budgrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budgrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    insert_sqlstr = create_budawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    insert_sqlstr = create_budfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerLink,
):
    x_dict = {
        "world_id": x_objkeysholder.world_id,
        "fisc_label": x_objkeysholder.fisc_label,
        "owner_name": x_objkeysholder.owner_name,
        "concept_way": x_objkeysholder.way,
    }
    for healer_name in sorted(x_healer._healer_names):
        x_dict["healer_name"] = healer_name
        insert_sqlstr = create_budheal_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_budprem(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_premiseunit: PremiseUnit,
):
    x_dict = copy_deepcopy(x_premiseunit.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    x_dict["rcontext"] = x_objkeysholder.rcontext
    insert_sqlstr = create_budprem_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    insert_sqlstr = create_budreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budlabor(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_laborheir: LaborHeir,
):
    x_dict = copy_deepcopy(x_laborheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    for labor_title in sorted(x_laborheir._laborlinks):
        x_dict["labor_title"] = labor_title
        insert_sqlstr = create_budlabor_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_budconc(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_concept: ConceptUnit
):
    x_dict = copy_deepcopy(x_concept.__dict__)
    x_dict["concept_way"] = x_concept.get_concept_way()
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budconc_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_bud: BudUnit
):
    x_dict = copy_deepcopy(x_bud.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    insert_sqlstr = create_budunit_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_obj(cursor: sqlite3_Cursor, world_id: WorldID, job_bud: BudUnit):
    job_bud.settle_bud()
    x_objkeysholder = ObjKeysHolder(world_id, job_bud.fisc_label, job_bud.owner_name)
    insert_job_budunit(cursor, x_objkeysholder, job_bud)
    for x_concept in job_bud.get_concept_dict().values():
        x_objkeysholder.way = x_concept.get_concept_way()
        healerlink = x_concept.healerlink
        laborheir = x_concept._laborheir
        insert_job_budconc(cursor, x_objkeysholder, x_concept)
        insert_job_budheal(cursor, x_objkeysholder, healerlink)
        insert_job_budlabor(cursor, x_objkeysholder, laborheir)
        for x_awardheir in x_concept._awardheirs.values():
            insert_job_budawar(cursor, x_objkeysholder, x_awardheir)
        for rcontext, reasonheir in x_concept._reasonheirs.items():
            insert_job_budreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.rcontext = rcontext
            for prem in reasonheir.premises.values():
                insert_job_budprem(cursor, x_objkeysholder, prem)

    for x_acct in job_bud.accts.values():
        insert_job_budacct(cursor, x_objkeysholder, x_acct)
        for x_membership in x_acct._memberships.values():
            insert_job_budmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in job_bud._groupunits.values():
        insert_job_budgrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_bud.conceptroot._factheirs.values():
        x_objkeysholder.fact_way = job_bud.conceptroot.get_concept_way()
        insert_job_budfact(cursor, x_objkeysholder, x_factheir)


def etl_fisc_jobs_json_to_db(
    conn_or_cursor: sqlite3_Connection, world_id: str, fisc_mstr_dir: str
):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_label in get_level1_dirs(fiscs_dir):
        fisc_path = create_path(fiscs_dir, fisc_label)
        owners_dir = create_path(fisc_path, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            job_obj = open_job_file(fisc_mstr_dir, fisc_label, owner_name)
            insert_job_obj(conn_or_cursor, world_id, job_obj)


def etl_fiscs_jobs_json_to_db(
    conn_or_cursor: sqlite3_Connection,
    lobby_mstr_dir,
    lobby_id: LobbyID,
    worlds: list[WorldID],
):
    for world_id in worlds:
        fisc_mstr_dir = create_fisc_mstr_dir_path(lobby_mstr_dir, lobby_id, world_id)
        etl_fisc_jobs_json_to_db(conn_or_cursor, world_id, fisc_mstr_dir)
