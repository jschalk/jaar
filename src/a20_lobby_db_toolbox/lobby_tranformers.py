from src.a00_data_toolboxs.file_toolbox import create_path, get_level1_dirs
from src.a01_word_logic.road import RoadUnit, WorldID
from src.a02_finance_toolboxs.deal import OwnerName, FiscTitle
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import AwardHeir, GroupUnit, MemberShip
from src.a04_reason_logic.reason_item import ReasonHeir, PremiseUnit, FactHeir
from src.a04_reason_logic.reason_team import TeamHeir
from src.a05_item_logic.healer import HealerLink
from src.a05_item_logic.item import ItemUnit
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
    create_budteam_metrics_insert_sqlstr,
    create_buditem_metrics_insert_sqlstr,
    create_budunit_metrics_insert_sqlstr,
)
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


@dataclass
class ObjKeysHolder:
    world_id: WorldID = None
    fisc_title: FiscTitle = None
    owner_name: OwnerName = None
    road: RoadUnit = None
    base: RoadUnit = None
    acct_name: AcctUnit = None
    membership: GroupUnit = None
    group_name: GroupUnit = None
    fact_road: RoadUnit = None


def insert_job_budmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
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
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
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
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
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
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    insert_sqlstr = create_budawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    insert_sqlstr = create_budfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerLink,
):
    x_dict = {
        "world_id": x_objkeysholder.world_id,
        "fisc_title": x_objkeysholder.fisc_title,
        "owner_name": x_objkeysholder.owner_name,
        "road": x_objkeysholder.road,
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
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    x_dict["base"] = x_objkeysholder.base
    insert_sqlstr = create_budprem_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    insert_sqlstr = create_budreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budteam(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_teamheir: TeamHeir,
):
    x_dict = copy_deepcopy(x_teamheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    for team_tag in sorted(x_teamheir._teamlinks):
        x_dict["team_tag"] = team_tag
        insert_sqlstr = create_budteam_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_buditem(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_item: ItemUnit
):
    x_dict = copy_deepcopy(x_item.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_buditem_metrics_insert_sqlstr(x_dict)
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
    x_objkeysholder = ObjKeysHolder(world_id, job_bud.fisc_title, job_bud.owner_name)
    insert_job_budunit(cursor, x_objkeysholder, job_bud)
    for x_item in job_bud.get_item_dict().values():
        x_objkeysholder.road = x_item.get_road()
        healerlink = x_item.healerlink
        teamheir = x_item._teamheir
        insert_job_buditem(cursor, x_objkeysholder, x_item)
        insert_job_budheal(cursor, x_objkeysholder, healerlink)
        insert_job_budteam(cursor, x_objkeysholder, teamheir)
        for x_awardheir in x_item._awardheirs.values():
            insert_job_budawar(cursor, x_objkeysholder, x_awardheir)
        for base, reasonheir in x_item._reasonheirs.items():
            insert_job_budreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.base = base
            for prem in reasonheir.premises.values():
                insert_job_budprem(cursor, x_objkeysholder, prem)

    for x_acct in job_bud.accts.values():
        insert_job_budacct(cursor, x_objkeysholder, x_acct)
        for x_membership in x_acct._memberships.values():
            insert_job_budmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in job_bud._groupunits.values():
        insert_job_budgrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_bud.itemroot._factheirs.values():
        x_objkeysholder.fact_road = job_bud.itemroot.get_road()
        insert_job_budfact(cursor, x_objkeysholder, x_factheir)


def etl_fisc_jobs_json_to_db(
    conn_or_cursor: sqlite3_Connection, world_id: str, fisc_mstr_dir: str
):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        fisc_path = create_path(fiscs_dir, fisc_title)
        owners_dir = create_path(fisc_path, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            job_obj = open_job_file(fisc_mstr_dir, fisc_title, owner_name)
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
