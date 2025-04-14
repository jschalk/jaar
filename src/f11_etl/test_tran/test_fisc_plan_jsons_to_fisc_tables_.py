from src.a00_data_toolboxs.db_toolbox import get_row_count
from src.a03_group_logic.group import awardlink_shop
from src.f02_bud.healer import healerlink_shop
from src.a04_reason_logic.reason_team import teamunit_shop
from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import (
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_groupunit_str,
    bud_item_awardlink_str,
    bud_item_factunit_str,
    bud_item_healerlink_str,
    bud_item_reason_premiseunit_str,
    bud_item_reasonunit_str,
    bud_item_teamlink_str,
    bud_itemunit_str,
    budunit_str,
)
from src.f06_listen.hub_tool import save_plan_file
from src.f11_etl.tran_sqlstrs import create_plan_tables
from src.f11_etl.transformers import etl_fisc_plan_jsons_to_fisc_db
from src.f11_etl.examples.etl_env import env_dir_setup_cleanup, get_test_etl_dir
from sqlite3 import connect as sqlite3_connect


def test_etl_fisc_plan_jsons_to_fisc_db_SetsDB_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_etl_dir()
    x_world_id = "music23"
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_bud = budunit_shop(sue_str, a23_str)
    sue_bud.add_acctunit(sue_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.get_acct(bob_str).add_membership(run_str)
    casa_road = sue_bud.make_l1_road("casa")
    status_road = sue_bud.make_l1_road("status")
    clean_road = sue_bud.make_road(status_road, "clean")
    dirty_road = sue_bud.make_road(status_road, "dirty")
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    sue_bud.add_item(dirty_road)
    sue_bud.edit_item_attr(
        road=casa_road, reason_base=status_road, reason_premise=dirty_road
    )
    sue_bud.edit_item_attr(road=casa_road, awardlink=awardlink_shop(run_str))
    sue_bud.edit_item_attr(road=casa_road, healerlink=healerlink_shop({bob_str}))
    sue_bud.edit_item_attr(road=casa_road, teamunit=teamunit_shop({sue_str}))
    sue_bud.add_fact(status_road, clean_road)
    print(f"{sue_bud.get_item_obj(casa_road).teamunit=}")
    print(f"{sue_bud.get_item_obj(casa_road).get_dict()=}")
    save_plan_file(fisc_mstr_dir, sue_bud)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_plan_tables(cursor)
        budmemb_plan_table = f"{bud_acct_membership_str()}_plan"
        budacct_plan_table = f"{bud_acctunit_str()}_plan"
        budgrou_plan_table = f"{bud_groupunit_str()}_plan"
        budawar_plan_table = f"{bud_item_awardlink_str()}_plan"
        budfact_plan_table = f"{bud_item_factunit_str()}_plan"
        budheal_plan_table = f"{bud_item_healerlink_str()}_plan"
        budprem_plan_table = f"{bud_item_reason_premiseunit_str()}_plan"
        budreas_plan_table = f"{bud_item_reasonunit_str()}_plan"
        budteam_plan_table = f"{bud_item_teamlink_str()}_plan"
        buditem_plan_table = f"{bud_itemunit_str()}_plan"
        budunit_plan_table = f"{budunit_str()}_plan"
        assert get_row_count(cursor, budunit_plan_table) == 0
        assert get_row_count(cursor, buditem_plan_table) == 0
        assert get_row_count(cursor, budacct_plan_table) == 0
        assert get_row_count(cursor, budmemb_plan_table) == 0
        assert get_row_count(cursor, budgrou_plan_table) == 0
        assert get_row_count(cursor, budawar_plan_table) == 0
        assert get_row_count(cursor, budfact_plan_table) == 0
        assert get_row_count(cursor, budheal_plan_table) == 0
        assert get_row_count(cursor, budreas_plan_table) == 0
        assert get_row_count(cursor, budprem_plan_table) == 0
        assert get_row_count(cursor, budteam_plan_table) == 0

        # WHEN
        etl_fisc_plan_jsons_to_fisc_db(cursor, x_world_id, fisc_mstr_dir)

        # THEN
        assert get_row_count(cursor, budunit_plan_table) == 1
        assert get_row_count(cursor, buditem_plan_table) == 5
        assert get_row_count(cursor, budacct_plan_table) == 2
        assert get_row_count(cursor, budmemb_plan_table) == 3
        assert get_row_count(cursor, budgrou_plan_table) == 3
        assert get_row_count(cursor, budawar_plan_table) == 1
        assert get_row_count(cursor, budfact_plan_table) == 1
        assert get_row_count(cursor, budheal_plan_table) == 1
        assert get_row_count(cursor, budreas_plan_table) == 1
        assert get_row_count(cursor, budprem_plan_table) == 1
        assert get_row_count(cursor, budteam_plan_table) == 1
